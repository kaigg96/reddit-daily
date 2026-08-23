"""Suppression-risk screen at selection (PRD R4.6).

Three channel uploads have been silently zeroed by YouTube "limited
distribution" — public, processed, *not* age-restricted via API, yet exactly 0
views while same-period uploads got 50–1000. Limited distribution is
Studio-only, so the API can't detect it after the fact; the only lever is to
avoid publishing the risky candidate in the first place.

The screen is deliberately NARROW. Evidence says the trigger is *framing*, not
topic: videos naming real people, covering dark subjects, or discussing
politics all serve fine. Over-filtering would cost more than the occasional
zeroed slot, so every non-pass verdict is logged for weekly audit.

Fails open: any Gemini error leaves a keyword backstop as the only check, and
if that also passes, the post ships.
"""

import json
import re
import time

import requests

from . import llm

# Categories YouTube's classifiers demonstrably enforce on this channel.
# Keep this list short — each addition risks over-filtering.
CATEGORIES = (
    "sexual_suggestive",   # sexual acts/performance framing, innuendo as the premise
    "graphic_harm",        # graphic injury/medical-harm detail (dissections, wounds)
    "named_wrongdoing",    # solicits specific unproven misconduct claims about named real people
    "minors_sexual",       # any sexualized context involving minors
    "hard_drugs",          # hard-drug use/acquisition framed approvingly or instructionally
    "graphic_violence",    # violence described in gratuitous detail
    "slurs",               # slurs or dehumanizing language toward protected groups
)

# Fires only when Gemini is unavailable, so it must be unambiguous — anything
# debatable is left to the model rather than hardcoded here.
_BACKSTOP = re.compile(
    r"\b(in bed|sexual|blowjob|orgasm|porn|masturbat|genital|"
    r"artery dissection|pneumothorax|disembowel|decapitat|"
    r"overdos(e|ing) on|how to (get|score) (heroin|meth|coke))\b",
    re.I,
)

_PROMPT = """You screen Reddit content before it becomes a YouTube Short, to avoid
uploads that YouTube silently suppresses ("limited distribution").

Flag ONLY these categories:
- sexual_suggestive: sexual acts/performance/innuendo as the premise
- graphic_harm: graphic injury or medical-harm detail
- named_wrongdoing: solicits specific unproven misconduct allegations about named real people
- minors_sexual: any sexualized context involving minors
- hard_drugs: hard-drug use/acquisition framed approvingly or instructionally
- graphic_violence: violence in gratuitous detail
- slurs: slurs or dehumanizing language toward protected groups

Do NOT flag merely dark, sad, morbid, political, embarrassing, or controversial
content — that performs well and must pass.

Real examples from this channel that WERE suppressed:
- "What's a sign outside of bed that hints someone's excellent in bed?" -> sexual_suggestive
- "ER workers, what stories do you have involving chiropractic patients?" (answers described
  cervical artery dissection, pneumothorax) -> graphic_harm
- "What's a horrible thing that a famous person did that everyone forgot about but you?"
  (answers alleged specific misconduct by named celebrities) -> named_wrongdoing

Real examples that were FINE and must NOT be flagged:
- "What was one name mentioned in The Epstein Files which shocked you?"
- "Which famous person died in the dumbest way possible?"
- "Which celebrity downfall can you absolutely not wait for?"
- "What YouTuber really fell off?"
- "What do you think about Ossoff denouncing Trump as a 'Draft Dodger, crook President'?"

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
    def __init__(self, verdict, unsafe=(), category="", reason="", source="gemini", topic=""):
        self.verdict = verdict          # "pass" | "skip_post"
        self.unsafe = set(unsafe)       # 0-based indices into the comment pool
        self.category = category
        self.reason = reason
        self.source = source            # gemini | backstop | error
        self.topic = topic              # R4.3 taxonomy, logged for performance tracking

    def __repr__(self):
        return (f"ScreenResult({self.verdict}, unsafe={sorted(self.unsafe)}, "
                f"category={self.category!r}, source={self.source})")


def _backstop(question, comments):
    """Keyword-only fallback used when Gemini is unavailable."""
    if _BACKSTOP.search(question):
        return ScreenResult("skip_post", category="backstop_match",
                            reason="keyword backstop matched question", source="backstop")
    unsafe = [i for i, c in enumerate(comments) if _BACKSTOP.search(c)]
    return ScreenResult("pass", unsafe=unsafe,
                        category="backstop_match" if unsafe else "",
                        reason="keyword backstop matched comment(s)" if unsafe else "",
                        source="backstop")


def _generate_screened(prompt, tries=3):
    """Retry transient rate limits — falling back to the keyword backstop is a
    real downgrade in protection, so it's worth a couple of seconds to avoid."""
    for attempt in range(tries):
        try:
            return llm._generate(prompt)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else 0
            if code in (429, 503) and attempt < tries - 1:
                time.sleep(4 * (attempt + 1))
                continue
            raise


def screen(question, comments):
    """Screen one candidate. Never raises — worst case returns a permissive result."""
    numbered = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(comments))
    try:
        raw = _generate_screened(_PROMPT.format(
            question=question, numbered=numbered, topics=", ".join(TOPICS)))
        match = re.search(r"\{.*\}", raw, re.S)
        data = json.loads(match.group(0)) if match else {}
    except Exception as e:
        print(f"Screen: Gemini failed with {type(e).__name__} — using keyword backstop")
        return _backstop(question, comments)

    risk = str(data.get("post_risk", "none")).strip().lower()
    topic = str(data.get("topic", "")).strip().lower()
    topic = topic if topic in TOPICS else ""
    reason = str(data.get("reason", ""))[:120]
    unsafe = {int(n) - 1 for n in data.get("unsafe_comments", [])
              if str(n).isdigit() and 0 < int(n) <= len(comments)}

    if risk in CATEGORIES:
        return ScreenResult("skip_post", unsafe=unsafe, category=risk, reason=reason, topic=topic)
    return ScreenResult("pass", unsafe=unsafe,
                        category="unsafe_comments" if unsafe else "",
                        reason=reason if unsafe else "", topic=topic)
