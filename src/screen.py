"""Suppression-risk screen at selection (PRD R4.6).

Two channel uploads have been silently zeroed by YouTube "limited
distribution" — public, processed, *not* age-restricted via API, yet exactly 0
views while same-period uploads got 50–1000. Limited distribution is
Studio-only, so the API can't detect it after the fact; the only lever is to
avoid publishing the risky candidate in the first place.

The screen is deliberately NARROW. Evidence says the trigger is *framing*, not
topic: videos naming real people, covering dark subjects, or discussing
politics all serve fine. Over-filtering would cost more than the occasional
zeroed slot, so every non-pass verdict is logged for weekly audit.

**Two tiers, because skipping and dropping cost very different amounts.**
Skipping a post discards the top-ranked candidate of the day — a whole slot.
Dropping an answer costs one answer and the pool backfills. So a category only
earns post-skip authority if a real zeroed upload supports it; everything else
is answer-level, where being wrong is nearly free. See PRD R4.6 for the
2026-08-30 evidence correction that forced this split.

Fails open: any Gemini error leaves a keyword backstop as the only check, and
if that also passes, the post ships.
"""

import json
import re
import time

import requests

from . import config, llm

# Categories that may discard the whole post. Each addition risks over-filtering,
# so the bar is high: either a confirmed zeroed upload of that shape, or a
# severity that makes a false positive cheap because it never fires here anyway.
SKIP_CATEGORIES = (
    "sexual_suggestive",   # confirmed zeroed: sexual acts/performance framing as the premise
    "named_wrongdoing",    # confirmed zeroed: solicits unproven misconduct claims about named real people
    "minors_sexual",       # severity guard — has never fired on this channel
    "hard_drugs",          # severity guard — has never fired on this channel
    "slurs",               # severity guard — has never fired on this channel
)

# Answer-level only: these may drop an individual answer but never discard the
# post. Demoted 2026-09-09 — `graphic_harm`'s only confirmed case was retracted
# (cold-spell artifact, PRD R4.6) and `graphic_violence` never had one, yet
# between them they caused 2 of the 3 post-skips in the first audit window.
DROP_ONLY_CATEGORIES = (
    "graphic_harm",        # graphic injury/medical-harm detail (dissections, wounds)
    "graphic_violence",    # violence described in gratuitous detail
)

# Fires only when Gemini is unavailable, so it must be unambiguous — anything
# debatable is left to the model rather than hardcoded here.
# Split on the same two tiers: graphic terms drop an answer, they never skip a post.
_BACKSTOP_POST = re.compile(
    r"\b(in bed|sexual|blowjob|orgasm|porn|masturbat|genital|"
    r"overdos(e|ing) on|how to (get|score) (heroin|meth|coke))\b",
    re.I,
)
_BACKSTOP_COMMENT = re.compile(
    _BACKSTOP_POST.pattern + r"|\b(artery dissection|pneumothorax|disembowel|decapitat)\b",
    re.I,
)

_PROMPT = """You screen Reddit content before it becomes a YouTube Short, to avoid
uploads that YouTube silently suppresses ("limited distribution").

Flag the QUESTION (post_risk) ONLY for these categories:
- sexual_suggestive: sexual acts/performance/innuendo as the premise
- named_wrongdoing: solicits specific unproven misconduct allegations about named real people
- minors_sexual: any sexualized context involving minors
- hard_drugs: hard-drug use/acquisition framed approvingly or instructionally
- slurs: slurs or dehumanizing language toward protected groups

Graphic injury, medical-harm detail and gratuitous violence are handled at the
ANSWER level only: list such answers in unsafe_comments. A question that merely
invites them is NOT post_risk — asking about scary symptoms, ER stories, injuries
or things going wrong is a normal, well-performing question here.

Do NOT flag merely dark, sad, morbid, political, embarrassing, or controversial
content — that performs well and must pass.

Real examples from this channel that WERE suppressed:
- "What's a sign outside of bed that hints someone's excellent in bed?" -> sexual_suggestive
- "What's a horrible thing that a famous person did that everyone forgot about but you?"
  (answers alleged specific misconduct by named celebrities) -> named_wrongdoing

Same premise, different wording — still sexual_suggestive, because the trigger is
sexual/romantic performance framed as intrigue, not the literal words above:
- "What's something innocent that feels dangerously flirty?" -> sexual_suggestive

Real examples that were FINE and must NOT be flagged:
- "What was one name mentioned in The Epstein Files which shocked you?"
- "Which famous person died in the dumbest way possible?"
- "Which celebrity downfall can you absolutely not wait for?"
- "What YouTuber really fell off?"
- "What do you think about Ossoff denouncing Trump as a 'Draft Dodger, crook President'?"

Questions this screen wrongly skipped before, which must now PASS:
- "Doctors/nurses of Reddit, what's a symptom patients brush off that actually terrifies you?"
- "Bartenders of Reddit, what was a 'cut off' gone wrong?"
- "ER workers, what stories do you have involving chiropractic patients?"

Also classify the question's topic into exactly one of:
{topics}

QUESTION: {question}

COMMENTS:
{numbered}

Return ONLY compact JSON, no markdown fence:
{{"post_risk": "none" or one category, "reason": "<12 words", "unsafe_comments": [numbers], "topic": "one topic"}}
- post_risk: flag the QUESTION itself only if the question inherently invites flagged content.
- unsafe_comments: numbers of individual comments that are risky (empty list if none).
- topic: for performance tracking only — never a reason to flag.
"""

# Same taxonomy as R4.3's historical analysis, so logged topics join cleanly
# against analysis/topic_performance.md.
TOPICS = (
    "relationships-dating", "money-work", "dark-morbid", "politics-news",
    "fame-celebrity", "nostalgia", "humor-absurd", "sex-adjacent",
    "health-body", "hypotheticals", "life-advice", "other",
)


class ScreenResult:
    def __init__(self, verdict, unsafe=(), category="", reason="", source="gemini",
                 topic="", demoted="", failure=""):
        self.verdict = verdict          # "pass" | "skip_post"
        self.unsafe = set(unsafe)       # 0-based indices into the comment pool
        self.category = category
        self.reason = reason
        self.source = source            # gemini | backstop | error
        self.topic = topic              # R4.3 taxonomy, logged for performance tracking
        self.demoted = demoted          # a DROP_ONLY category the model raised on the post
        self.failure = failure          # why Gemini never answered, when source=backstop

    def __repr__(self):
        return (f"ScreenResult({self.verdict}, unsafe={sorted(self.unsafe)}, "
                f"category={self.category!r}, source={self.source})")


def _backstop(question, comments, failure=""):
    """Keyword-only fallback used when Gemini is unavailable."""
    if _BACKSTOP_POST.search(question):
        return ScreenResult("skip_post", category="backstop_match",
                            reason="keyword backstop matched question", source="backstop",
                            failure=failure)
    unsafe = [i for i, c in enumerate(comments) if _BACKSTOP_COMMENT.search(c)]
    return ScreenResult("pass", unsafe=unsafe,
                        category="backstop_match" if unsafe else "",
                        reason="keyword backstop matched comment(s)" if unsafe else "",
                        source="backstop", failure=failure)


# The screen is the one genuine judgment task in the pipeline, and disabling
# reasoning broke it: with thinking off it passed "What's something innocent
# that feels dangerously flirty?", replay_screen.py's paraphrase of the same
# `sexual_suggestive` shape as the confirmed zeroed upload VDH3pSafyE0 ("...hints
# someone's excellent in bed?"). Caught by the 2026-09-20 CI gate.
#
# Keywords, titles and CTAs are transformations and stay at zero — this budget
# buys reasoning only where it demonstrably changes the verdict. It is small
# because latency is what broke this module before: default thinking spent 546
# tokens and 33s on a title, past the old 30s timeout.
#
# 512 tokens is not sufficient on its own: a same-day replay (still on this
# budget) missed the flirty paraphrase again while correctly catching the
# literal example already in the prompt — one example doesn't generalize. The
# paraphrase is now a second in-prompt example above; reasoning budget alone
# was the wrong lever.
SCREEN_THINKING_BUDGET = 512


def _generate_screened(prompt, tries=2):
    """Retry a transient failure once — falling back to the keyword backstop is
    a real downgrade in protection, so it is worth a few seconds to avoid.

    **A 429 is never retried.** On this project's free tier a 429 is a *daily*
    budget exhaustion, not a per-minute burst: it persists for hours and clears
    at midnight PT. Retrying it cannot succeed, and every wasted request comes
    out of the same budget the title, keyword and CTA calls later in this run
    still need — so retrying a 429 makes the run's output worse, not better.
    Measured 2026-09-11: a verification pass retried 429s and burned ~40
    requests to make 8 useful calls.

    Timeouts and 503s are genuinely transient and are retried once. The budget
    is tight enough that `tries` is deliberately 2, not 3."""
    for attempt in range(tries):
        last = attempt == tries - 1
        try:
            return llm._generate(prompt, thinking_budget=SCREEN_THINKING_BUDGET)
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


def _fall_back(question, comments, failure):
    print(f"Screen: Gemini failed ({failure}) — using keyword backstop")
    return _backstop(question, comments, failure=failure)


def screen(question, comments):
    """Screen one candidate. Never raises — worst case returns a permissive result."""
    numbered = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(comments))
    try:
        raw = _generate_screened(_PROMPT.format(
            question=question, numbered=numbered, topics=", ".join(TOPICS)))
    except Exception as e:
        return _fall_back(question, comments, llm._failure_kind(e))
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        # Parsing this as {} would pass the post as screened by Gemini while
        # skipping even the backstop. Labels match llm.get_metadata's.
        return _fall_back(question, comments, "no_json")
    try:
        data = json.loads(match.group(0))
    except ValueError:
        return _fall_back(question, comments, "bad_json")

    risk = str(data.get("post_risk", "none")).strip().lower()
    topic = str(data.get("topic", "")).strip().lower()
    topic = topic if topic in TOPICS else ""
    reason = str(data.get("reason", ""))[:120]
    unsafe = {int(n) - 1 for n in data.get("unsafe_comments", [])
              if str(n).isdigit() and 0 < int(n) <= len(comments)}

    if risk in SKIP_CATEGORIES:
        return ScreenResult("skip_post", unsafe=unsafe, category=risk, reason=reason, topic=topic)

    # The prompt already tells the model these are answer-level, but a prompt is
    # not an enforcement mechanism — never let them cost a slot. Logged as
    # `demoted` so the audit trail keeps the counterfactual visible.
    demoted = risk if risk in DROP_ONLY_CATEGORIES else ""
    return ScreenResult("pass", unsafe=unsafe,
                        category="unsafe_comments" if unsafe else "",
                        reason=reason if (unsafe or demoted) else "",
                        topic=topic, demoted=demoted)


# --- R4.4 Step 0.5: slate telemetry ---------------------------------------

_SLATE_PROMPT = """Classify each AskReddit question's topic into exactly one of:
{topics}

Questions:
{numbered}

Reply with JSON only: a list of {n} topic strings, in order."""


class SlateFailed(Exception):
    """Why the slate went unlogged, as `kind`: safe to write to the log because
    it is never the exception text, which for an HTTPError embeds the keyed URL."""

    def __init__(self, kind):
        super().__init__(kind)
        self.kind = kind


def classify_slate(titles):
    """Topics for every eligible candidate, in rank order, from ONE request.

    Telemetry only: nothing reads it at selection time. The ranker R4.4 would
    build fires only when the top candidate sits in a weak topic and one just
    below it sits in a strong one, and how often that happens cannot be
    known from the log's one topic per upload. This logs the whole slate.

    Titles only, no comments, which is what makes one request enough. It runs
    on config.SLATE_MODEL, whose free allowance is separate from the model
    titles and the screen use. Never retried. Returns a list the length of
    `titles` ("" where the answer was not a known topic), None for an empty
    slate, and raises SlateFailed on any failure so the log records why: the
    first two live runs logged nothing and the reason only reached the console.
    The caller catches it, so nothing here can block an upload.
    """
    if not titles:
        return None
    numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(titles, 1))
    try:
        raw = llm._generate(_SLATE_PROMPT.format(
            topics=", ".join(TOPICS), numbered=numbered, n=len(titles)),
            model=config.SLATE_MODEL)
        match = re.search(r"\[.*\]", raw, re.S)
        got = json.loads(match.group(0)) if match else None
    except Exception as e:
        # never echo the exception body: HTTPError messages embed the keyed URL
        status = getattr(getattr(e, "response", None), "status_code", None)
        kind = f"{type(e).__name__} {status}" if status else type(e).__name__
        print(f"Slate: topic call failed with {kind} (not logged this run)")
        raise SlateFailed(kind) from None
    if not isinstance(got, list) or len(got) != len(titles):
        kind = f"shape {len(got)}/{len(titles)}" if isinstance(got, list) else "shape"
        print(f"Slate: topic call returned the wrong {kind} (not logged this run)")
        raise SlateFailed(kind)
    return [t if t in TOPICS else "" for t in (str(x).strip().lower() for x in got)]
