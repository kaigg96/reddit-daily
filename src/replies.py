"""Replies to viewer comments: the queue a shift drafts into (PLAN C10).

The publishing policy (ORG.md, Audience & community) lets agents publish
beyond the upload, but no shift publishes directly: a shift holds no YouTube
keys. It drafts replies into a committed queue, and a workflow that holds the
keys posts them. This module is that queue and its rules, kept pure so they
are tested; nothing here calls YouTube.

Each row is ours alone: the video, the comment replied to (its ID only, never
its text, which YouTube lets us keep 30 days, #75) and the reply. The policy's
rules each have a check here:
- no links, no AI attribution (CLAUDE.md §5), never claiming to be a person;
- a daily cap;
- never replying to our own comment, which the posting job checks against the
  comment's author, since only it can read that.
Every post also passes the safety screen, which spends Gemini and so runs in
the posting job, not here.
"""
import csv
import datetime
import re

from . import config
from .content import _profane

QUEUE = config.ROOT / "analysis" / "replies.csv"   # beside the data the jobs commit back
FIELDS = ["queued_utc", "video_id", "parent_id", "reply", "status", "posted_utc", "note"]
STATUSES = {"queued", "posted", "refused"}
REPLIES_PER_DAY = 5
REPLY_MAX_CHARS = 200

_LINK = re.compile(r"https?://|www\.|\b[\w-]+\.(com|net|org|io|ly|be|co|tv|gg|me|app)\b",
                   re.IGNORECASE)
# Any mention of AI or automation, and any claim to be a person: the policy
# leaves questions about who runs the channel unanswered, so a reply never
# raises it either way. Over-matching costs one draft.
_ABOUT_US = re.compile(
    r"\b(a\.?i\.?|artificial intelligence|bots?|automated|generated|chat ?gpt|gpt|claude|"
    r"gemini|llm|language model|algorithm|human|real person|a person|i'?m real)\b",
    re.IGNORECASE)


def check_reply(text):
    """Why a drafted reply may not be posted, or None when it may."""
    text = (text or "").strip()
    if not text:
        return "empty"
    if len(text) > REPLY_MAX_CHARS:
        return f"over {REPLY_MAX_CHARS} characters"
    if _LINK.search(text):
        return "contains a link"
    if _ABOUT_US.search(text):
        return "mentions AI, automation or being a person"
    if _profane(text):
        return "profanity"
    return None


def load(path=QUEUE):
    """The queue's rows, [] when it does not exist yet."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def save(rows, path=QUEUE):
    """Write the queue with LF endings, as every committed CSV here is."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in rows)


def due(rows, today, cap=REPLIES_PER_DAY):
    """The queued rows the posting job may post today, oldest first: at most
    `cap` less those already posted today, one per parent comment, and none
    whose text fails `check_reply` (those are for the job to mark refused)."""
    posted_today = sum(1 for r in rows if r.get("status") == "posted"
                       and (r.get("posted_utc") or "")[:10] == today.isoformat())
    replied = {r.get("parent_id") for r in rows if r.get("status") == "posted"}
    out = []
    for r in sorted((r for r in rows if r.get("status") == "queued"),
                    key=lambda r: r.get("queued_utc") or ""):
        if len(out) >= cap - posted_today:
            break
        if r.get("parent_id") in replied or check_reply(r.get("reply")):
            continue
        replied.add(r.get("parent_id"))
        out.append(r)
    return out


def queue_reply(rows, video_id, parent_id, reply, now=None):
    """Append a drafted reply, refusing it at once if it breaks a rule.
    Returns the reason it was refused, or None."""
    reason = check_reply(reply)
    if not video_id or not parent_id:
        reason = "needs the video and the comment replied to"
    if any(r.get("parent_id") == parent_id and r.get("status") in ("queued", "posted") for r in rows):
        reason = "already replied or queued"
    if reason:
        return reason
    now = now or datetime.datetime.now(datetime.timezone.utc)
    rows.append({"queued_utc": now.isoformat(timespec="seconds"), "video_id": video_id,
                 "parent_id": parent_id, "reply": reply.strip(), "status": "queued",
                 "posted_utc": "", "note": ""})
    return None
