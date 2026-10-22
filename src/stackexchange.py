"""A Stack Exchange question as the post, for a sample render only (PLAN C16).

Reddit's free API ends by March 2027, and the 5 November review weighs what
could replace it. Stack Exchange licenses its posts under CC BY-SA 4.0, which
allows our use if each author is credited and linked, and lets us shorten an
answer (a shortened answer makes the video share-alike). Its answers run 100
to 360 words against our ~12, so each is cut to one spoken sentence by the
free Groq model. This branch exists to render one narrated sample of that
show; it is never merged, and nothing here is screened for upload.
"""
import html
import json
import re

import requests

from . import config, llm
from .content import Answer, PostContent

API = "https://api.stackexchange.com/2.3"
SITE = "workplace"


def _plain(body):
    """An answer's HTML as one line of text, code and quotes included."""
    text = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def condense(question, answers):
    """Each answer as one spoken sentence in its author's own voice, or None
    if the model's reply is unusable."""
    prompt = (
        "Below is a question from a Q&A site and its three top answers. "
        "Shorten each answer to ONE sentence a narrator can read aloud, at most "
        "20 words and 140 characters. Keep the answerer's own point and tone, "
        "first person if they wrote in it; add nothing they did not say. "
        "Reply with only a JSON array of three strings, in order.\n\n"
        f"Question: {question}\n\n"
        + "\n\n".join(f"Answer {i}: {a[:2500]}" for i, a in enumerate(answers, 1)))
    reply = llm._generate_groq(prompt)
    match = re.search(r"\[.*\]", reply, re.S)
    try:
        lines = json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None
    if (not isinstance(lines, list) or len(lines) != 3
            or not all(isinstance(s, str) and 0 < len(s.strip()) <= config.MAX_COMMENT_LENGTH
                       for s in lines)):
        return None
    return [s.strip() for s in lines]


def select_post(prev_title=""):
    """Today's first hot question with three answers that condense."""
    questions = requests.get(f"{API}/questions", timeout=20, params={
        "order": "desc", "sort": "hot", "site": SITE, "pagesize": 15}).json()["items"]
    for q in questions:
        title = html.unescape(q["title"])
        if q["answer_count"] < 3 or title == prev_title or len(title) > config.MAX_TITLE_LENGTH:
            continue
        answers = requests.get(f"{API}/questions/{q['question_id']}/answers", timeout=20, params={
            "order": "desc", "sort": "votes", "site": SITE, "filter": "withbody",
            "pagesize": 3}).json()["items"]
        if len(answers) < 3:
            continue
        lines = condense(title, [_plain(a["body"]) for a in answers])
        if not lines:
            continue
        return PostContent(
            subreddit="Workplace", title=title, shortlink=q["link"],
            comments=[Answer(line, html.unescape(a["owner"].get("display_name", "")))
                      for line, a in zip(lines, answers)],
            topic="money-work", screen_source="stackexchange",
            author=html.unescape(q["owner"].get("display_name", "")))
    raise RuntimeError("no hot Stack Exchange question with three answers condensed")
