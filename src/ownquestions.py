"""Our own question with the host's three takes: the source after Reddit
(PLAN C16), built switched off (`config.SOURCE`).

Reddit's free API ends by March 2027 whether or not our app is registered, and
unregistered apps lose it on 2027-01-12 (#82). This source needs no licence,
since nobody else wrote the takes. That is also its risk: they may never read
as a real person's answer (PRD §4: the free model once invented "My boss once
read my medical notes"), so the screen labels each one a take, and a take
about its teller is refused. Ported from `strategy/own-questions-sample`
(reviewed 10-25) onto the live format, with what the sample skipped: the R4.6
screen and a repeat check against every shipped title.
"""
import json
import re

from . import config, content, llm
from .content import Answer, PostContent

PROMPT = (
    "You host a YouTube Shorts show that asks one everyday question and gives "
    "three quick takes on it, then asks viewers which take they pick. Write "
    "today's episode.\n"
    "- The question: open, about everyday life, answerable by anyone in a "
    "sentence, at most 12 words, ending in a question mark. Not about news, "
    "politics, religion, health, sex or a named person or brand.\n"
    "- Three takes that genuinely disagree with each other, each ONE sentence "
    "of at most 18 words, plain and spoken, stating a stance.\n"
    "- A take is a stance, never a person: no character (\"As a parent\"), no "
    "story or anything that happened, and no \"I\", \"me\", \"my\", \"we\" or "
    "\"our\" (three takes in the first person would read as three people). No "
    "jokes built on a comparison (\"X is like Y\").\n"
    "Reply with only JSON: {\"question\": \"...\", \"takes\": [\"...\", \"...\", \"...\"]}")

# A take about its teller would be an invented person: a story ("My boss
# once…"), or a first-person preference, which across three contradicting
# takes reads as three people ("Coffee fuels my focus" beside "I skip
# stimulants", a trial reply, 2026-10-25).
# "I'm" and "I’ve" match on their "I". A character ("As a parent") or a time
# that happened ("Growing up", "Last week") is a story too.
_STORY = re.compile(r"\b(i|me|my|mine|myself|we|our|us)\b|^as an? |\bgrowing up\b|"
                    r"\b(last|one) (week|month|year|time)\b", re.I)


def _usable(question, takes):
    return (isinstance(question, str) and question.strip().endswith("?")
            and 0 < len(question) <= config.MAX_TITLE_LENGTH
            and isinstance(takes, list) and len(takes) == 3
            and all(isinstance(t, str) and 0 < len(t.strip()) <= config.MAX_COMMENT_LENGTH
                    and not _STORY.search(t) for t in takes)
            and len({t.strip().lower() for t in takes}) == 3
            # Narrated and captioned word for word, so the filters Reddit text
            # passes apply too; the screen does not catch mild swearing.
            and not any(content._profane(x) or content._has_emoji(x) for x in [question, *takes]))


def parse(reply):
    """The episode as (question, takes), or None if the reply is unusable."""
    match = re.search(r"\{.*\}", reply or "", re.S)
    try:
        data = json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or not _usable(data.get("question"), data.get("takes")):
        return None
    return data["question"].strip(), [t.strip() for t in data["takes"]]


def select_post(prev_title="", uploaded=frozenset(), screener=None, on_verdict=None):
    """Today's question and three takes. One request on the upload model, then
    one free Groq request if that reply is refused: unusable, a repeat of any
    shipped title (a model writing questions repeats itself), or skipped by the
    R4.6 screen, whose dropped takes refuse the whole episode, as three takes
    are the show. Raises when neither route gives one, so the run fails loudly
    rather than shipping a reading. Groq only while `GROQ_FALLBACK` is on, as
    every other call. No model is named: a dry run writes on the sample model,
    so a render never spends the uploads' allowance."""
    shipped = {t.strip().lower() for t in uploaded} | {prev_title.strip().lower()}
    for route in ("upload model",) + (("groq",) if config.GROQ_FALLBACK else ()):
        try:
            reply = (llm.generate_retrying(PROMPT)
                     if route == "upload model" else llm._generate_groq(PROMPT))
        except Exception as e:   # noqa: BLE001 -- the other route may still answer
            print(f"Own question: the {route} failed ({type(e).__name__})")
            continue
        episode = parse(reply)
        if not episode:
            print(f"Own question: the {route}'s reply was refused: {(reply or '')[:300]!r}")
            continue
        question, takes = episode
        if question.lower() in shipped:
            print(f"Own question: the {route} repeated a shipped question: {question[:60]}")
            continue
        result = screener(question, takes) if screener else None
        if result and (result.verdict == "skip_post" or result.unsafe):
            print(f"Own question: the screen refused the {route}'s episode "
                  f"({result.category or 'unsafe takes'})")
            if on_verdict:
                on_verdict(question, result, "skip_post")
            continue
        print(f"Own question: written on the {route}")
        return PostContent(subreddit="", title=question, shortlink="",
                           comments=[Answer(t, "") for t in takes],
                           topic=result.topic if result else "other",
                           screen_source=result.source if result else "",
                           screen_failure=result.failure if result else "")
    raise RuntimeError("neither route gave a usable, unshipped, screened question and three takes")
