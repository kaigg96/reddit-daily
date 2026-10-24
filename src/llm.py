"""Gemini calls. Every function fails soft: the video must ship without them."""

import collections
import json
import os
import re
import time

import requests

from . import config  # also ensures .env is loaded for direct imports
from . import content


# gemini-2.5-flash "thinks" by default, and on these prompts that is pure
# latency: measured 2026-09-19, one title call spent 546 reasoning tokens to
# emit an 8-token title and took 33.1s — past the 30s timeout this module used
# to use, so the call raised ReadTimeout and the run shipped the raw Reddit
# question instead of a generated title. Disabling thinking put the same call
# at 0.6s. Every task here (keyword extraction, title rephrasing, a one-line
# CTA, the R4.6 screen's JSON verdict) is a short transformation, not a
# reasoning problem.
#
# thinkingConfig requires v1beta: v1 rejects it with "Thinking is not enabled
# for api version v1." That is the only reason this module is on v1beta.
_ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
             "{model}:generateContent")
MODEL = "gemini-2.5-flash"
# The free tier is counted per model (our 429 names the quota
# GenerateRequestsPerDayPerProjectPerModel). A dry run's calls go to a model
# with its own allowance, so a sample never spends the requests the next
# upload needs -- the 07:00 window also pays for the following 05:00 upload.
# Release validation does not set DRY_RUN, so it still tests MODEL.
SAMPLE_MODEL = "gemini-3.5-flash-lite"  # 2.5-flash-lite: 404 "no longer available to new users" (2026-09-26)
# One try on this model once MODEL has failed, for the screen and the metadata
# call alike: an overload or spent cap on one model rarely means the other.
# Every sample render already writes its title and CTA on it.
FALLBACK_MODEL = SAMPLE_MODEL
FALLBACK_SOURCE = "gemini_fallback"

# Generous because it is now only a backstop against a pathological response,
# not a routine limit — with thinking off, calls land in about a second.
# requests' timeout is per-read, not a total deadline, so this does not bound
# total call duration; it only stops a stalled socket hanging the run.
_TIMEOUT = 60
# How long a 503 ("model overloaded") waits before its one retry. 4s did not
# clear the 503 on the 2026-10-02 14:46 release check or the 2026-10-04 06:04
# upload, which lost its title. The run has no deadline to protect, and the
# wait costs no requests, so wait long enough for an overload to pass.
_OVERLOAD_WAIT = 30
# A Groq 429 is usually its per-minute token cap (8K a minute free), which
# clears in seconds, unlike Gemini's daily one. Retried once when Groq's own
# retry-after is at most this; a longer wait is its daily cap, and is not.
_GROQ_RATE_WAIT_MAX = 60

_warned_no_key = False


def provider():
    """Who answers this run's AI calls: "groq" when switched on and its key is
    set, else "gemini". A switched-on route with no key falls back to Gemini,
    as today, rather than costing the upload its title. The log's source
    columns record which one answered, so the fallback shows there."""
    global _warned_no_key
    if config.AI_PROVIDER != "groq":
        return "gemini"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if not _warned_no_key:
        print("AI_PROVIDER=groq but GROQ_API_KEY is not set: using Gemini")
        _warned_no_key = True
    return "gemini"


def _generate(prompt, thinking_budget=0, model=None):
    """One Gemini call. `thinking_budget=0` disables reasoning tokens (the
    default, and what every caller here wants); pass a token budget only for a
    task where reasoning demonstrably helps. `model` exists because the free
    tier is counted per model: a caller on another model draws on its own
    daily allowance, not the one titles and the screen share (PRD §5 no. 3)."""
    if provider() == "groq":
        return _generate_groq(prompt, reasoning=thinking_budget > 0)
    model = model or (SAMPLE_MODEL if config.DRY_RUN else MODEL)
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    # Gemini 3.x answers thinkingBudget with HTTP 400 (measured 2026-09-26),
    # so the budget goes only to the 2.5 models that take it.
    if model.startswith("gemini-2.5"):
        body["generationConfig"] = {"thinkingConfig": {"thinkingBudget": thinking_budget}}
    # The key goes in a header, not the URL: HTTP errors quote the URL, which
    # put the key in any log or file that recorded a failed request.
    resp = requests.post(
        _ENDPOINT.format(model=model),
        headers={"Content-Type": "application/json",
                 "x-goog-api-key": os.environ["GEMINI_API_KEY"]},
        json=body,
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


_GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"


def _generate_groq(prompt, reasoning=False):
    """The same call on Groq (config.AI_PROVIDER). Its model always reasons;
    the effort follows the caller's choice, so only the screen pays for depth.
    Errors raise as Gemini's do; generate_retrying waits out a per-minute 429."""
    resp = requests.post(
        _GROQ_ENDPOINT,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={"model": config.GROQ_MODEL,
              "messages": [{"role": "user", "content": prompt}],
              "reasoning_effort": "medium" if reasoning else "low"},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"] or ""


GROQ_SOURCE = "groq_fallback"


def groq_rescue(prompt, reasoning=False):
    """One try on Groq after Gemini has failed: (reply, failure). Shared by the
    screen and the metadata call, so the switch (config.GROQ_FALLBACK) means
    the same thing for both. The reply is None when off, keyless or missing;
    the failure is blank unless a try was made and missed, so the log tells
    "Groq failed" from "Groq off"."""
    if not (config.GROQ_FALLBACK and os.environ.get("GROQ_API_KEY")):
        return None, ""
    try:
        return _generate_groq(prompt, reasoning=reasoning), ""
    except Exception as e:
        return None, _failure_kind(e)


def generate_retrying(prompt, tries=2, **kw):
    """`_generate`, retrying a transient failure once. Shared by the screen and
    the metadata call so the two cannot drift: the metadata call had no retry,
    and one 503 cost the 2026-10-01 18:29 upload its title, keywords and CTA.

    **A 429 is never retried.** On this project's free tier a 429 is a *daily*
    budget exhaustion, not a per-minute burst: it persists for hours and clears
    at midnight PT. Retrying it cannot succeed, and every wasted request comes
    out of the same budget the rest of the run still needs. Measured
    2026-09-11: a verification pass retried 429s and burned ~40 requests to
    make 8 useful calls. The exception is Groq's per-minute cap, which its
    retry-after header tells apart from its daily one (`_groq_rate_wait`).
    The log's `http_429_day` / `_minute` says which cap each 429 hit; a
    Gemini `_minute` would be the evidence to revisit this rule.

    Timeouts and 503s are genuinely transient and are retried once. The budget
    is tight enough that `tries` is deliberately 2, not 3; a 503 waits
    `_OVERLOAD_WAIT` first, since a 4s wait twice failed to outlast one."""
    for attempt in range(tries):
        last = attempt == tries - 1
        try:
            return _generate(prompt, **kw)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else 0
            if code == 503 and not last:
                time.sleep(_OVERLOAD_WAIT * (attempt + 1))
                continue
            wait = _groq_rate_wait(e) if code == 429 and not last else None
            if wait is not None:
                time.sleep(wait)
                continue
            raise
        except (requests.Timeout, requests.ConnectionError):
            if last:
                raise
            time.sleep(4 * (attempt + 1))


def _groq_rate_wait(exc):
    """Seconds a Groq 429 asks us to wait, if short enough to be its
    per-minute cap; None for Gemini, a missing header, or a longer wait."""
    if provider() != "groq" or exc.response is None:
        return None
    try:
        wait = float(exc.response.headers.get("retry-after", ""))
    except ValueError:
        return None
    return wait if 0 <= wait <= _GROQ_RATE_WAIT_MAX else None


# PRD R2.2: three title-style experiments, rotated deterministically per day
# and logged per upload so performance is comparable offline.
_STYLE_GUIDANCE = {
    "A": """
- Be a captivating and concise rephrasing or transformation of the original Reddit question: "{reddit_title}".
- Spark strong curiosity and make viewers eager to see the answers.""",
    "B": """
- Address the viewer directly in the second person ("You...", "Which one are you?", "You'll wish you knew this...").
- Make it feel like a personal question or challenge aimed at the viewer, derived from the original Reddit question: "{reddit_title}".""",
    "C": """
- Lead with the number of answers, list-style (e.g. "3 Answers That...", "3 People Reveal...").
- Frame the video as a countable list distilled from the original Reddit question: "{reddit_title}".""",
}


# `source` mirrors ScreenResult.source: it says whether Gemini answered at all,
# which all-None fields cannot. Both a spent quota and a prompt that produces
# junk return None for every field, and the release gate has to tell them apart
# -- one is "could not check", the other is "do not merge". Defaulted so the
# upload path, which only ever reads the three content fields, is untouched.
#
# `failure` says WHY the fields came back empty: `http_429` (a cap; `_day` or
# `_minute` when the body names which), another `http_<status>`, `timeout`,
# `no_json`, `bad_json`. Blank when
# Gemini answered with JSON. The upload log keeps it because the ok-flags alone
# made a 429 and a timeout look identical -- the 2026-09-24 morning title loss
# could only be blamed on the quota by its timing.
MetadataResult = collections.namedtuple("MetadataResult", "title keywords cta source failure")
MetadataResult.__new__.__defaults__ = ("gemini", "")


def _failure_kind(exc):
    """A short label for a request that never landed. Never the message: an
    HTTPError's message embeds the keyed URL."""
    response = getattr(exc, "response", None)
    if isinstance(exc, requests.HTTPError) and response is not None:
        kind = f"http_{response.status_code}"
        return kind + _quota_window(response) if response.status_code == 429 else kind
    if isinstance(exc, requests.Timeout):
        return "timeout"
    return type(exc).__name__


def _quota_window(response):
    """"_day" or "_minute": which cap a 429's body names, "" when it names none.

    A bare `http_429` could not say whether the day's 20 requests were spent
    (the next upload loses its title) or a burst hit a per-minute cap (a wait
    would have cleared it). The 2026-10-20 13:34 release check 429'd on its
    fifth screen case after a shift's trials, and nothing recorded which.
    Gemini's body names its quotaId (`GenerateRequestsPerDayPerProjectPerModel`),
    Groq's message its window ("tokens per minute"). Only the label is kept,
    never the body. A day cap wins when both are named: it is the one that
    lasts."""
    try:
        body = response.text
    except Exception:
        return ""
    flat = re.sub(r"[\s_-]", "", body).lower() if isinstance(body, str) else ""
    if "perday" in flat:
        return "_day"
    return "_minute" if "perminute" in flat else ""


_CTA_ASK = """3. CTA — a spoken outro line of AT MOST 12 words asking viewers to comment
   their own answer to this specific question. Direct, punchy, conversational.
   No hashtags, no emoji, no profanity."""


def _cta_instruction(vote_rule):
    """The closing line: today's ask for the viewer's answer, or the host's vote.

    Bet 1 (PRD R3.2): YouTube pays for the creator's own perspective, and every
    video already ends on this line, so the host's vote can replace it at no
    added length or request. The rule that earns the vote is the owner's (#55);
    until it is set, the prompt is unchanged byte for byte."""
    if not vote_rule:
        return _CTA_ASK
    return f"""3. CTA — the show's host casts its vote, spoken in AT MOST 12 words: which
   answer it raises its hand for and, in a few words, why, then ask which one
   gets the viewer's vote. What earns the host's vote: {vote_rule}
   Name something specific from these answers, never a stock phrase. Judge,
   never advise: no advice on health, law, money or politics. Vote on the
   answer, never on the person: no claims about health conditions, identities
   or groups of people. Plain spoken words. No hashtags, no emoji, no profanity."""


# PRD §0 #14: titles with a capitalised word earned ~2x the views at 7 days,
# observationally (PRD §4, 2026-10-09). Each run's coin assigns an arm, so the
# read is causal. Both arms ban shock phrases: YouTube's monetization review
# reads titles and refuses content "designed to shock or surprise viewers for
# the sole purpose of getting views" (PLAN §4). None leaves the prompt as it was.
_CAPS_GUIDANCE = {
    True: """
   - Write exactly ONE word in capitals for emphasis (such as "YOU" or "REALLY"); no other word in capitals.""",
    False: """
   - Do not write any word in capitals for emphasis; only real acronyms may be in capitals.""",
}
_NO_SHOCK = """
   - Never use shock phrases such as "shocking", "you won't believe" or "insane"."""


def title_caps_arm(rng):
    """PRD §0 #14's coin: True asks the title for one capitalised word."""
    return rng.random() < 0.5


def get_metadata(reddit_title, comments, style="A", caps=None):
    """Title + SEO keywords + CTA in ONE Gemini request.

    These were three separate calls until 2026-09-19. The free-tier cap is 20
    requests/day and production already spends 8-14 of them (PRD §2), so three
    requests about the same post was the most obviously removable third of the
    budget. The quota counts requests, not tokens, so merging the prompts is a
    straight saving: 4-7 requests per run becomes 2-5.

    Fail-soft stays PER FIELD, which is the part worth being careful about. A
    response missing a CTA must not cost us the title, so each field comes back
    None independently and the caller falls back on just that one. Returning a
    single all-or-nothing result would have made one bad field as expensive as
    a dead API.
    """
    guidance = _STYLE_GUIDANCE.get(style, _STYLE_GUIDANCE["A"]).format(reddit_title=reddit_title)
    if caps is not None:
        guidance += _CAPS_GUIDANCE[bool(caps)] + _NO_SHOCK
    numbered = "\n".join(f'{i}. "{c}"' for i, c in enumerate(comments[:3], 1))
    prompt = f"""
I'm creating a YouTube Short based on the Reddit question: "{reddit_title}".
It features these answers:
{numbered}

Produce three things.

1. TITLE — a YouTube title that maximizes click-through rate.
   The title should:{guidance}
   - Use impactful, engaging language; under 70 characters is ideal.
   - Hint at the nature of the answers without giving away specifics.
   - NOT be overly clickbaity or sensational. No emoji.

2. KEYWORDS — the 10 best search keywords for this video, mixing short-tail and
   long-tail terms someone looking for this discussion would actually type.

{_cta_instruction(config.HOUSE_VOTE_RULE)}

Return ONLY a JSON object, no markdown fence, in exactly this shape:
{{"title": "...", "keywords": ["...", "..."], "cta": "..."}}
"""
    route, prior = provider(), ""
    try:
        raw = generate_retrying(prompt)
    except Exception as e:
        prior = _failure_kind(e)
        # Gemini only, never in a dry run (already on FALLBACK_MODEL), as for
        # the screen.
        if route == "gemini" and not config.DRY_RUN:
            raw, route, prior = _rescue_metadata(prompt, prior)
        else:
            raw = None
        if raw is None:
            # never echo the exception body: HTTPError messages embed the keyed URL
            # The reason, not just the type: a dry run writes no upload log, so
            # its "HTTPError" could not be told apart as a 429 or a 503 (2026-10-08).
            print(f"{provider().title()} metadata failed with {type(e).__name__} "
                  f"({prior}; title, keywords and CTA all fall back)")
            # The request never landed -- a 429 on the shared daily cap, a timeout,
            # a transport error. Nothing was learned about the prompt's quality.
            return MetadataResult(None, None, None, "error", prior)

    # On a rescued answer the Gemini failure stays first, as the screen's does,
    # so the log shows why it ran: a blank failure is still "Gemini answered".
    tag = "fallback" if route == FALLBACK_SOURCE else "groq"
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        print(f"{route} metadata returned no JSON object (all fields fall back)")
        return MetadataResult(None, None, None, route, _then(prior, "no_json", tag))
    try:
        data = json.loads(match.group(0))
    except ValueError:
        print(f"{route} metadata returned unparseable JSON (all fields fall back)")
        return MetadataResult(None, None, None, route, _then(prior, "bad_json", tag))

    return MetadataResult(
        title=_clean_published(data.get("title")),
        keywords=_clean_keywords(data.get("keywords")),
        cta=_clean_published(data.get("cta")),
        source=route,
        failure=prior,
    )


def _rescue_metadata(prompt, prior):
    """Once MODEL has failed: one try on FALLBACK_MODEL, then Groq's (PRD §0
    #13): (reply, route, failure). Two 503s 30s apart cost the 2026-10-18 16:02
    upload its title, keywords and CTA, which the screen's second model would
    have answered. Each route that misses adds its reason after Gemini's.
    `validate_release.py` sets FALLBACK_MODEL to None: an answer from it tests
    the wrong model, so there it would only spend a request."""
    if FALLBACK_MODEL:
        try:
            reply = generate_retrying(prompt, tries=1, model=FALLBACK_MODEL)
        except Exception as e:
            prior = _then(prior, _failure_kind(e), "fallback")
        else:
            print(f"Gemini metadata failed ({prior}); {FALLBACK_MODEL} answered instead")
            return reply, FALLBACK_SOURCE, prior
    reply, missed = groq_rescue(prompt)
    if reply is None:
        return None, "gemini", _then(prior, missed)
    print(f"Gemini metadata failed ({prior}); Groq answered instead")
    return reply, GROQ_SOURCE, prior


def _then(prior, failure, route="groq"):
    """The failure label after a later route's try: Gemini's first, then the
    route's, named `fallback_` or `groq_` as the screen names them. Gemini's
    alone when no try was made."""
    if not failure:
        return prior
    return f"{prior};{route}_{failure}" if prior else failure


def _clean_str(value):
    """A usable non-empty string, or None. Strips the quoting LLMs add."""
    if not isinstance(value, str):
        return None
    value = re.sub(r"[*_`]", "", value)                    # markdown emphasis
    value = re.sub(r"\s+", " ", value).strip().strip('"').strip("'").strip()
    return value or None


def _clean_published(value):
    """`_clean_str` for the title, closing line and keywords, refusing a swear
    word or emoji so the field falls back as if it were missing: the prompt's
    "no profanity, no emoji" alone let an emoji title ship on 2026-09-01.
    Checked before the emphasis strip too, which would turn "f**k" into "fk".
    Not for the host's lines: the word list also holds "god", "hell" and
    "damn", so "Oh god" would be refused as a reaction."""
    cleaned = _clean_str(value)
    if cleaned and any(content._profane(v) or content._has_emoji(v) for v in (value, cleaned)):
        print("An AI-written field was refused for a swear word or emoji")  # not echoed: logs are public
        return None
    return cleaned


def _clean_keywords(value):
    """A list of non-empty keyword strings, or None if the field was absent.

    [] and None mean different things here, same as the old get_keywords: None
    is "the model didn't give us this field", [] is "it gave us nothing usable".
    Only the first tells us the call is unhealthy.
    """
    if not isinstance(value, list):
        return None
    return [k for k in (_clean_published(v) for v in value) if k]


# R2.2, weighted by PRD §0 #10: B ("You...") 4 : A 1 : C 1, with A and C kept as
# the control. One style per calendar day, so both daily uploads share it; with
# two rotating subreddits each day also splits them, keeping both reads balanced.
TITLE_STYLE_CYCLE = "BABBCB"


def title_style_for(day):
    return TITLE_STYLE_CYCLE[day.toordinal() % len(TITLE_STYLE_CYCLE)]


TitleResult = collections.namedtuple("TitleResult", "title style ok")


def resolve_title(generated, style, fallback, max_len=100, caps=None, source=""):
    """Decide the shipped title, the style to log, and whether generation worked.

    The style is blanked whenever generation failed, because an upload carrying
    the raw Reddit question is not evidence about style A, B or C. Logging it as
    such contaminated the R2.2 cohorts unevenly (A 7%, B 12%, C 5% mislabelled,
    and 23% of the last 30 uploads) — a bias, not just noise. Keeping the rule
    here rather than in run.py means the log and the experiment can't disagree.
    `caps` is #14's arm and `source` the Reddit text the title was written from.
    """
    # ok follows the cleaned title: a reply that cleans to nothing (a lone
    # quote) ships the fallback, so it must not claim a style.
    cleaned = sanitize_title(generated, "", max_len)
    ok = bool(cleaned)
    if ok and caps is False:
        cleaned = drop_emphasis_caps(cleaned, source)
    return TitleResult(
        title=sentence_case(cleaned) if ok else sanitize_title(None, fallback, max_len),
        style=style if ok else "",
        ok=ok,
    )


_CAPS_WORD = re.compile(r"\b[A-Z]{2,}(?:['’][A-Za-z]+)?\b")


def drop_emphasis_caps(title, source=""):
    """Hold PRD §0 #14's no-capitals arm to its word; the prompt alone leaked.

    1 of the arm's 9 titles from 10-10 to 10-16 shipped a word in capitals
    ("What's YOUR unforgetable deathbed confession?"): the other arm's
    treatment, which shrinks the lead the test has to show. A word in capitals
    stays when it is a known acronym or the Reddit text writes it in capitals
    ("ICU nurses"); any other takes the case of the words around it. Emphasis
    copied from the Reddit text ("I was SO angry") passes as written there.
    """
    keep = config.TITLE_ACRONYMS | set(re.findall(r"\b([A-Z]{2,})s?\b", source))
    # Title Case when three in four words after the first are capitalised; a
    # plain majority read "Tom Hanks in New York" as Title Case.
    words = [w for w in re.findall(r"[A-Za-z][\w'’]*", title)
             if not _CAPS_WORD.fullmatch(w)][1:]
    titled = bool(words) and sum(w[0].isupper() for w in words) * 4 >= len(words) * 3

    def recase(m):
        word = m.group(0)
        if re.split("['’]", word)[0] in keep:
            return word
        starts = re.search(r"(^[\d\W]*|[.?!:]\s+\W*)$", title[:m.start()]) is not None
        return word.capitalize() if titled or starts else word.lower()

    return _CAPS_WORD.sub(recase, title)


def sentence_case(title):
    """Capitalise a generated title written with no capital letter at all.

    PRD §0 #14's no-capitals arm asks for no word in capitals for emphasis, and
    the model read it as no capitals at all: 4 of the arm's first 5 titles
    shipped entirely lower case ("how to get jehovah's witnesses to leave you
    alone"), so the test was comparing capitals against titles that look
    unfinished. A title with any capital letter is the model's own choice and
    is left exactly as it is; the raw Reddit fallback never comes here.
    """
    if not title or any(c.isupper() for c in title):
        return title
    # A sentence ends at ? or !, or at a full stop after a word of two or more
    # letters: not an ellipsis ("self... and why") or "i.e." / "a.i.".
    title = re.sub(r"(^\W*|(?:(?<=\w\w)\.|[?!])\s+\W*)([a-z])",
                   lambda m: m.group(1) + m.group(2).upper(), title)
    return re.sub(r"(?<![./])\bi\b(?![./])", "I", title)


def sanitize_title(title, fallback, max_len=100):
    """Strip LLM artifacts (R0.5). 100 is YouTube's title limit."""
    if not title:
        return fallback[:max_len]
    title = re.sub(r"\s+", " ", title).strip().strip('"').strip("'").strip()
    if not title:
        return fallback[:max_len]
    return title[:max_len]
