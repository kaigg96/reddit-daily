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
- never quoting the viewer: a reply sharing a run of words with the comment
  would put viewer text into public history, past YouTube's 30 days.
The posting job, which holds the keys, owns the rest: never replying to our
own comment (only it can read the author); the safety screen on every post
(it spends Gemini), which also catches a claim like "I'm a dad" no pattern
can; and, before each post, checking the thread for a reply from us already,
since a stale copy of this file saved over a "posted" row would re-queue it.
"""
import csv
import datetime
import re

from . import config
from .content import _profane

QUEUE = config.ROOT / "analysis" / "replies.csv"   # beside the data the jobs commit back
FIELDS = ["queued_utc", "video_id", "parent_id", "reply", "status", "posted_utc", "note"]
REPLIES_PER_DAY = 5
REPLY_MAX_CHARS = 200

_LINK = re.compile(r"https?://|www\.|\b[\w-]+(?:\.|\s+\.\s+)(com|net|org|io|ly|be|co|tv|gg|me|app|uk|dev|xyz)\b"
                   r"|\bdot\s+(com|net|org)\b", re.IGNORECASE)
# Any mention of AI or automation, and any claim to be a person: the policy
# leaves questions about who runs the channel unanswered, so a reply never
# raises it either way. Over-matching costs one draft.
_ABOUT_US = re.compile(
    r"\b(a\.?i\.?|ais|artificial intelligence|(chat|ro)?bots?|automated|generated|chat ?gpt|gpt|"
    r"claude|gemini|openai|anthropic|llms?|language models?|algorithm|humans?|real person|"
    r"a person|i'?m real)\b",
    re.IGNORECASE)


QUOTE_WORDS = 6


def _quotes(reply, comment, n=QUOTE_WORDS):
    """Does the reply repeat `n` or more words of the comment in a row, or a
    shorter comment whole (three words or more)?"""
    words = lambda t: re.findall(r"\w+", (t or "").lower())
    c = words(comment)
    n = max(3, min(n, len(c)))
    runs = {tuple(c[i:i + n]) for i in range(len(c) - n + 1)}
    r = words(reply)
    return any(tuple(r[i:i + n]) in runs for i in range(len(r) - n + 1))


def check_reply(text, comment=""):
    """Why a drafted reply may not be posted, or None when it may. `comment`
    is the viewer's text, read at drafting time and never stored."""
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
    if comment and _quotes(text, comment):
        return "quotes the viewer"
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
    """(to post, to refuse) among the queued rows. To post: oldest first, at
    most `cap` less those already posted today, one per parent comment. To
    refuse: rows whose text fails `check_reply` or whose comment already has
    a posted reply, for the job to mark refused rather than leave queued."""
    posted_today = sum(1 for r in rows if r.get("status") == "posted"
                       and (r.get("posted_utc") or "")[:10] == today.isoformat())
    replied = {r.get("parent_id") for r in rows if r.get("status") == "posted"}
    out, refuse = [], []
    for r in sorted((r for r in rows if r.get("status") == "queued"),
                    key=lambda r: r.get("queued_utc") or ""):
        if r.get("parent_id") in replied or check_reply(r.get("reply")):
            refuse.append(r)
        elif len(out) < cap - posted_today:
            replied.add(r.get("parent_id"))
            out.append(r)
    return out, refuse


def queue_reply(rows, video_id, parent_id, reply, comment="", now=None):
    """Append a drafted reply, refusing it at once if it breaks a rule.
    `comment` is the viewer's text, checked against and never stored.
    Returns the reason it was refused, or None."""
    reason = check_reply(reply, comment)
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


def post_due(rows, today, client, screen_fn, channel_id, titles, now, dry_run=True,
             cap=REPLIES_PER_DAY):
    """The posting job's pass over the queue, rows updated in place; returns
    one line per row acted on, for the job's log.

    `client` reads and posts through YouTube: `comment(parent_id)` gives
    (author channel ID, text) or None when the comment is gone;
    `replied(parent_id, channel_id)` says whether we answered it already;
    `post(parent_id, text)` returns True once posted. `screen_fn(question,
    comments)` is `screen.screen`, which fails open by design; a reply needs
    a real pass, so a backstop verdict refuses it. `titles` maps a video to
    the question it asked. Under `dry_run` nothing is posted or marked."""
    post, refuse = due(rows, today, cap)
    out = []

    def mark(r, status, note):
        out.append(f"{status:8} {r.get('parent_id')}  {note}")
        if not dry_run:
            r.update(status=status, note=note,
                     posted_utc=now.isoformat(timespec="seconds") if status == "posted" else "")

    for r in refuse:
        mark(r, "refused", check_reply(r.get("reply")) or "comment already answered")
    for r in post:
        found = client.comment(r["parent_id"])
        if found is None:
            mark(r, "refused", "comment gone")
            continue
        author, text = found
        if author == channel_id:
            mark(r, "refused", "our own comment")
            continue
        if client.replied(r["parent_id"], channel_id):
            mark(r, "refused", "already answered on YouTube")
            continue
        reason = check_reply(r["reply"], text)
        if reason:
            mark(r, "refused", reason)
            continue
        verdict = screen_fn(titles.get(r.get("video_id"), ""), [r["reply"]])
        if verdict.verdict != "pass" or verdict.unsafe or verdict.source == "backstop":
            mark(r, "refused", f"screen: {verdict.verdict}, {verdict.category or verdict.source}")
            continue
        if dry_run:
            out.append(f"would post {r['parent_id']}  {r['reply']}")
        elif client.post(r["parent_id"], r["reply"]):
            mark(r, "posted", "")
        else:
            out.append(f"failed   {r['parent_id']}  left queued")
    return out
