"""Our own question with the host's own three takes, for a sample render only
(PLAN C16).

Reddit's free API ends by March 2027, and the 5 November review weighs what
could replace it: the owner watches a narrated sample of each candidate. This
is the one that needs no licence. Nobody else wrote these takes, so they may
never read as a real person's answer (PRD §4: the free model once invented "My
boss once read my medical notes"): the screen labels each one the host's
take, and the host does not react to its own words. One request on the upload
model, as the show would make it. This branch is never merged, and nothing
here is screened for upload.
"""
import json
import re

from . import config, llm
from .content import Answer, PostContent

PROMPT = (
    "You host a YouTube Shorts show that asks one everyday question and gives "
    "three quick takes on it, then asks viewers which take they pick. Write "
    "today's episode.\n"
    "- The question: open, about everyday life, answerable by anyone in a "
    "sentence, at most 12 words, ending in a question mark. Not about news, "
    "politics, religion, health, sex or a named person or brand.\n"
    "- Three takes that genuinely disagree with each other, each ONE sentence "
    "of at most 18 words, plain and spoken, with a clear opinion.\n"
    "- The takes are your opinions, never experiences: no story about yourself, "
    "a job, a family, or anything that happened to you. No jokes built on a "
    "comparison (\"X is like Y\").\n"
    "Reply with only JSON: {\"question\": \"...\", \"takes\": [\"...\", \"...\", \"...\"]}")

# A take that tells a story about the teller would be an invented person.
_STORY = re.compile(r"\b(my (boss|wife|husband|mom|mum|dad|kids?|son|daughter|job|"
                    r"friend|partner|ex)|when i was|i once|once i|years ago)\b", re.I)


def _usable(question, takes):
    return (isinstance(question, str) and question.strip().endswith("?")
            and 0 < len(question) <= config.MAX_TITLE_LENGTH
            and isinstance(takes, list) and len(takes) == 3
            and all(isinstance(t, str) and 0 < len(t.strip()) <= config.MAX_COMMENT_LENGTH
                    and not _STORY.search(t) for t in takes)
            and len({t.strip().lower() for t in takes}) == 3)


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


def select_post(prev_title=""):
    """Today's question and three takes, written in one request."""
    episode = parse(llm.generate_retrying(PROMPT, model=llm.MODEL))
    if not episode or episode[0] == prev_title:
        raise RuntimeError("the episode request gave no usable question and three takes")
    question, takes = episode
    return PostContent(subreddit="", title=question, shortlink="",
                       comments=[Answer(t, "") for t in takes],
                       topic="other", screen_source="own")


# Shown over the question, so the viewer knows whose takes follow.
OWN_SETUP = "Three takes. All mine."


def as_host(host):
    """The host's lines for its own takes: it says over the question that the
    takes are its own, and reacts to none of them (reacting to its own words
    would be talking to itself). The vote stays: it is the closing line."""
    return host._replace(setup=OWN_SETUP, reactions=[""] * len(host.reactions))
