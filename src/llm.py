"""Gemini calls. Every function fails soft: the video must ship without them."""

import collections
import json
import os
import re
import time

import requests

from . import config  # noqa: F401  (ensures .env is loaded for direct imports)


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


def _generate(prompt, thinking_budget=0, model=None):
    """One Gemini call. `thinking_budget=0` disables reasoning tokens (the
    default, and what every caller here wants); pass a token budget only for a
    task where reasoning demonstrably helps. `model` exists because the free
    tier is counted per model: a caller on another model draws on its own
    daily allowance, not the one titles and the screen share (PRD §5 no. 3)."""
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


def generate_retrying(prompt, tries=2, **kw):
    """`_generate`, retrying a transient failure once. Shared by the screen and
    the metadata call so the two cannot drift: the metadata call had no retry,
    and one 503 cost the 2026-10-01 18:29 upload its title, keywords and CTA.

    **A 429 is never retried.** On this project's free tier a 429 is a *daily*
    budget exhaustion, not a per-minute burst: it persists for hours and clears
    at midnight PT. Retrying it cannot succeed, and every wasted request comes
    out of the same budget the rest of the run still needs. Measured
    2026-09-11: a verification pass retried 429s and burned ~40 requests to
    make 8 useful calls.

    Timeouts and 503s are genuinely transient and are retried once. The budget
    is tight enough that `tries` is deliberately 2, not 3."""
    for attempt in range(tries):
        last = attempt == tries - 1
        try:
            return _generate(prompt, **kw)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else 0
            if code == 503 and not last:
                time.sleep(4 * (attempt + 1))
                continue
            raise
        except (requests.Timeout, requests.ConnectionError):
            if last:
                raise
            time.sleep(4 * (attempt + 1))


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
MetadataResult = collections.namedtuple("MetadataResult", "title keywords cta source failure")
MetadataResult.__new__.__defaults__ = ("gemini", "")


def _failure_kind(exc):
    """A short label for a request that never landed. Never the message: an
    HTTPError's message embeds the keyed URL."""
    response = getattr(exc, "response", None)
    if isinstance(exc, requests.HTTPError) and response is not None:
        return f"http_{response.status_code}"
    if isinstance(exc, requests.Timeout):
        return "timeout"
    return type(exc).__name__


def get_metadata(reddit_title, comments, style="A"):
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

3. CTA — a spoken outro line of AT MOST 12 words asking viewers to comment
   their own answer to this specific question. Direct, punchy, conversational.
   No hashtags, no emoji, no profanity.

Return ONLY a JSON object, no markdown fence, in exactly this shape:
{{"title": "...", "keywords": ["...", "..."], "cta": "..."}}
"""
    try:
        raw = generate_retrying(prompt)
    except Exception as e:
        # never echo the exception body: HTTPError messages embed the keyed URL
        print(f"Gemini metadata failed with {type(e).__name__} "
              f"(title, keywords and CTA all fall back)")
        # The request never landed -- a 429 on the shared daily cap, a timeout,
        # a transport error. Nothing was learned about the prompt's quality.
        return MetadataResult(None, None, None, "error", _failure_kind(e))

    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        print("Gemini metadata returned no JSON object (all fields fall back)")
        return MetadataResult(None, None, None, failure="no_json")
    try:
        data = json.loads(match.group(0))
    except ValueError:
        print("Gemini metadata returned unparseable JSON (all fields fall back)")
        return MetadataResult(None, None, None, failure="bad_json")

    return MetadataResult(
        title=_clean_str(data.get("title")),
        keywords=_clean_keywords(data.get("keywords")),
        cta=_clean_str(data.get("cta")),
    )


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
