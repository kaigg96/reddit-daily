"""Gemini calls. Every function fails soft: the video must ship without them."""

import collections
import json
import os
import re
import time

import emoji
import requests

from . import config  # also ensures .env is loaded for direct imports


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
    "Groq failed" from "Groq off".

    A 429 whose retry-after is Groq's per-minute cap waits once and tries
    again: on a day Gemini's allowance is spent, up to four screens reach
    Groq back to back and the metadata call, which carries bet 1's host
    lines, lands in the same minute (review, 2026-10-12)."""
    if not (config.GROQ_FALLBACK and os.environ.get("GROQ_API_KEY")):
        return None, ""
    for last in (False, True):
        try:
            return _generate_groq(prompt, reasoning=reasoning), ""
        except Exception as e:
            wait = None if last else _groq_minute_wait(e)
            if wait is None:
                return None, _failure_kind(e)
            # A wait that then succeeds leaves no failure label, so say so.
            print(f"Groq rescue: waiting {wait:.0f}s on its per-minute cap, then one retry")
            time.sleep(wait)


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
    if provider() != "groq":
        return None
    return _groq_minute_wait(exc)


def _groq_minute_wait(exc):
    """Seconds a Groq 429 asks for, if short enough to be its per-minute cap;
    None for anything else, a missing header, or a longer wait."""
    response = getattr(exc, "response", None)
    if response is None or response.status_code != 429:
        return None
    try:
        wait = float(response.headers.get("retry-after", ""))
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
# `failure` says WHY the fields came back empty: `http_429` (the shared daily
# cap), another `http_<status>`, `timeout`, `no_json`, `bad_json`. Blank when
# Gemini answered with JSON. The upload log keeps it because the ok-flags alone
# made a 429 and a timeout look identical -- the 2026-09-24 morning title loss
# could only be blamed on the quota by its timing.
MetadataResult = collections.namedtuple("MetadataResult", "title keywords cta source failure commentary")
MetadataResult.__new__.__defaults__ = ("gemini", "", None)

# Bet 1's host lines (config.COMMENTARY): a setup, one reaction per answer read,
# and the verdict, which is also the CTA. Voiced, all or nothing: a partial set
# would leave answers unreacted to, so it falls back to today's video instead.
# Shown as text, a line too long is "" and the rest still ship (_clean_commentary).
Commentary = collections.namedtuple("Commentary", "setup reactions verdict")


def _failure_kind(exc):
    """A short label for a request that never landed. Never the message: an
    HTTPError's message embeds the keyed URL."""
    response = getattr(exc, "response", None)
    if isinstance(exc, requests.HTTPError) and response is not None:
        return f"http_{response.status_code}"
    if isinstance(exc, requests.Timeout):
        return "timeout"
    return type(exc).__name__


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


# Bet 1 (#70, PRD R3.2's commentary-led variant). The rules are the ones the
# 2026-10-09 drafts needed (PRD §4): each failure they showed has a line here.
# The first real sample (2026-10-10, a politics thread) added two: its setup
# restated the question as "Reddit weighs in on ...", a frame that would repeat
# across uploads, and a reaction took a side ("skips right over the diplomatic
# fallout"). Politics is 5 of 86 topic-tagged uploads: too many to skip.
# Re-tried on the sample model: both fixed, but its vote said "the second one",
# so the vote's own instruction repeats the never-by-number rule.
# Word caps keep narration near today's ~455 characters (drafts: 410-546) with
# our own words at half or more, which is the done-when.
_COMMENTARY_ASK = """3. COMMENTARY — this show's host reacts to the answers. Its stance is a show
   of hands: it hears the answers, then raises its hand for one. Spoken lines:
   - "setup": AT MOST 15 words, after the question and before the first answer:
     the host's own hunch or angle on this question. Never restate the
     question, and never open on "Reddit" or a stock frame like "weighs in".
   - "reactions": exactly {n} lines of AT MOST 12 words each, in order; each is
     heard straight after its answer and reacts to that answer only.
   - "cta": the host's vote, AT MOST 15 words: which answer it raises its hand
     for, named by what it says (never "the first" or "the second one"), and
     in a few words why, then ask which one gets the viewer's vote.
   Rules for every line:
   - Name something specific from this thread, never a stock phrase.
   - React with opinion, humour or a question. Never state a fact, statistic or
     diagnosis in your own voice. Judge, never advise: no advice on health,
     law, money or politics.
   - Refer to an answer by what it says, never by its number.
   - Vote on the answer, never on the person: no claims about health
     conditions, identities or groups of people.
   - On threads about illness, injury, death or crime, be warm or wry about the
     people, never about the harm.
   - On politics or news threads, take no side on the issue itself: react to
     how an answer is put (its wit, its nerve), and vote on that.
   - Every line must make sense heard once. Plain spoken words. No hashtags, no
     emoji, no profanity."""


# The prompt's word caps, enforced with slack: a line well past its cap would
# push the video toward the 60s limit and Polly's per-run budget, either of
# which would cost the upload, so it falls back instead.
_HOST_CAPS = {"setup": 15, "reaction": 12, "cta": 15}
# Shown as text (config.HOST_TEXT, #71), a line must read in about two
# seconds and fit two lines on screen; the vote is still spoken.
_TEXT_CAPS = {"setup": 10, "reaction": 10, "cta": 15}
_CAP_SLACK = 1.5

# What changes in the ask when the host is read, not heard (#71). Each pair
# must match the voiced ask exactly; a test holds them to it.
_TEXT_EDITS = [
    ("Spoken lines:",
     "Lines shown on screen as text, never spoken (the narrator speaks only the vote):"),
    ('"setup": AT MOST 15 words, after the question and before the first answer:',
     '"setup": AT MOST 10 words, shown under the question:'),
    ("lines of AT MOST 12 words each, in order; each is\n     heard straight after its answer and reacts to that answer only.",
     "lines of AT MOST 10 words each, in order; each is\n     shown while its answer is read and reacts to that answer only. Never\n     repeat the answer's own words: they are already on screen."),
    ("Every line must make sense heard once.", "Every line must make sense read once, in two seconds."),
    ("Plain spoken words.", "Plain words."),
]
# A note past about 12 words runs to four lines and meets the watermark
# (measured at 64px, 900px wide, 2026-10-11), so text lines get less slack.
_TEXT_SLACK = 1.2


def _commentary_ask(n):
    """The host's instructions, for a voiced host or a text-only one."""
    ask = _COMMENTARY_ASK
    if config.HOST_TEXT:
        for old, new in _TEXT_EDITS:
            ask = ask.replace(old, new)
    return ask.format(n=n)


def _within_cap(line, kind):
    if config.HOST_TEXT:
        return len(line.split()) <= _TEXT_CAPS[kind] * _TEXT_SLACK
    return len(line.split()) <= _HOST_CAPS[kind] * _CAP_SLACK


def _usable(line, kind):
    """Within its cap, with a letter in it (a weak reply can echo the shape's
    "...") and no emoji, which the note's font draws as an empty box."""
    return (_within_cap(line, kind) and re.search(r"[^\W\d_]", line) is not None
            and not any(emoji.is_emoji(ch) and ch not in _TEXT_SYMBOLS for ch in line))


# The emoji package counts these as emoji, but they are text marks the font draws.
_TEXT_SYMBOLS = "©®™"


def _clean_commentary(data, n):
    """The host's lines, or None when they cannot ship (see Commentary).

    Shown as text, an over-long line is dropped alone: a note costs no time,
    and one long line cost a whole upload its host in one of four samples
    (2026-10-13). Its note is left blank, and a long vote leaves the generic
    closing line. With no note left, the upload is today's reading."""
    setup, verdict = _clean_str(data.get("setup")), _clean_str(data.get("cta"))
    reactions = data.get("reactions")
    if not isinstance(reactions, list) or len(reactions) != n:
        return None
    reactions = [_clean_str(r) for r in reactions]
    if not (setup and verdict and all(reactions)):
        return None
    if (_usable(setup, "setup") and _usable(verdict, "cta")
            and all(_usable(r, "reaction") for r in reactions)):
        return Commentary(setup, reactions, verdict)
    print("Commentary: a host line ran past its length cap, or was a placeholder or emoji")
    if not config.HOST_TEXT:
        return None
    setup = setup if _usable(setup, "setup") else ""
    reactions = [r if _usable(r, "reaction") else "" for r in reactions]
    verdict = verdict if _usable(verdict, "cta") else ""
    if not (setup or any(reactions)):
        return None
    print("Commentary: dropped only the long line(s)")
    return Commentary(setup, reactions, verdict)


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


_PLAIN_SHAPE = '{"title": "...", "keywords": ["...", "..."], "cta": "..."}'
_COMMENTARY_SHAPE = ('{"title": "...", "keywords": ["...", "..."], "setup": "...", '
                     '"reactions": ["...", "..."], "cta": "..."}')


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
    template = _STYLE_GUIDANCE.get(style, _STYLE_GUIDANCE["A"])
    if config.COMMENTARY:
        # Style C's examples promise a count; two answers are read, not three.
        # Replaced before the question goes in, so the question is never edited.
        template = template.replace('"3 ', f'"{config.COMMENTARY_ANSWERS} ')
    guidance = template.format(reddit_title=reddit_title)
    if caps is not None:
        guidance += _CAPS_GUIDANCE[bool(caps)] + _NO_SHOCK
    commentary = config.COMMENTARY
    if commentary:
        comments = comments[:config.COMMENTARY_ANSWERS]
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

{_commentary_ask(len(comments)) if commentary
 else _cta_instruction(config.HOUSE_VOTE_RULE)}

Return ONLY a JSON object, no markdown fence, in exactly this shape:
{_COMMENTARY_SHAPE if commentary else _PLAIN_SHAPE}
"""
    route, prior = provider(), ""
    try:
        raw = generate_retrying(prompt)
    except Exception as e:
        prior = _failure_kind(e)
        # PRD §0 #13: Groq answers before the fields fall back, as it does for
        # the screen, and on the same terms: Gemini only, never in a dry run.
        raw, missed = (groq_rescue(prompt) if route == "gemini" and not config.DRY_RUN
                       else (None, ""))
        if raw is None:
            # never echo the exception body: HTTPError messages embed the keyed URL
            # The reason, not just the type: a dry run writes no upload log, so
            # its "HTTPError" could not be told apart as a 429 or a 503 (2026-10-08).
            print(f"{provider().title()} metadata failed with {type(e).__name__} "
                  f"({prior}; title, keywords and CTA all fall back)")
            # The request never landed -- a 429 on the shared daily cap, a timeout,
            # a transport error. Nothing was learned about the prompt's quality.
            return MetadataResult(None, None, None, "error", _then(prior, missed))
        print(f"Gemini metadata failed ({prior}); Groq answered instead")
        route = GROQ_SOURCE

    # On a Groq answer the Gemini failure stays first, as the screen's does, so
    # the log shows why it ran: a blank failure is still "Gemini answered".
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        print(f"{route} metadata returned no JSON object (all fields fall back)")
        return MetadataResult(None, None, None, route, _then(prior, "no_json"))
    try:
        data = json.loads(match.group(0))
    except ValueError:
        print(f"{route} metadata returned unparseable JSON (all fields fall back)")
        return MetadataResult(None, None, None, route, _then(prior, "bad_json"))

    return MetadataResult(
        title=_clean_str(data.get("title")),
        keywords=_clean_keywords(data.get("keywords")),
        cta=_clean_str(data.get("cta")),
        source=route,
        failure=prior,
        commentary=_clean_commentary(data, len(comments)) if commentary else None,
    )


def _then(prior, failure):
    """The failure label after Groq's try: Gemini's first, then Groq's, named
    `groq_` as the screen names them. Gemini's alone when no try was made."""
    if not failure:
        return prior
    return f"{prior};groq_{failure}" if prior else failure


def _clean_str(value):
    """A usable non-empty string, or None. Strips the quoting LLMs add."""
    if not isinstance(value, str):
        return None
    value = re.sub(r"[*_`]", "", value)                    # markdown emphasis
    value = re.sub(r"\s+", " ", value).strip().strip('"').strip("'").strip()
    return value or None


def _clean_keywords(value):
    """A list of non-empty keyword strings, or None if the field was absent.

    [] and None mean different things here, same as the old get_keywords: None
    is "the model didn't give us this field", [] is "it gave us nothing usable".
    Only the first tells us the call is unhealthy.
    """
    if not isinstance(value, list):
        return None
    return [k for k in (_clean_str(v) for v in value) if k]


# R2.2, weighted by PRD §0 #10: B ("You...") 4 : A 1 : C 1, with A and C kept as
# the control. One style per calendar day, so both daily uploads share it; with
# two rotating subreddits each day also splits them, keeping both reads balanced.
TITLE_STYLE_CYCLE = "BABBCB"


def title_style_for(day):
    return TITLE_STYLE_CYCLE[day.toordinal() % len(TITLE_STYLE_CYCLE)]


TitleResult = collections.namedtuple("TitleResult", "title style ok")


def resolve_title(generated, style, fallback, max_len=100):
    """Decide the shipped title, the style to log, and whether generation worked.

    The style is blanked whenever generation failed, because an upload carrying
    the raw Reddit question is not evidence about style A, B or C. Logging it as
    such contaminated the R2.2 cohorts unevenly (A 7%, B 12%, C 5% mislabelled,
    and 23% of the last 30 uploads) — a bias, not just noise. Keeping the rule
    here rather than in run.py means the log and the experiment can't disagree.
    """
    ok = bool(generated and generated.strip())
    return TitleResult(
        title=sanitize_title(generated, fallback, max_len),
        style=style if ok else "",
        ok=ok,
    )


def sanitize_title(title, fallback, max_len=100):
    """Strip LLM artifacts (R0.5). 100 is YouTube's title limit."""
    if not title:
        return fallback[:max_len]
    title = re.sub(r"\s+", " ", title).strip().strip('"').strip("'").strip()
    if not title:
        return fallback[:max_len]
    return title[:max_len]
