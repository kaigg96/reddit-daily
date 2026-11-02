#!/usr/bin/env python3
"""Post the queued replies to viewer comments (PLAN C10; ORG.md, Audience &
community). Run only by the replies workflow, which holds the YouTube keys;
a shift drafts into analysis/replies.csv and never runs this for real.

    DRY_RUN=1 venv/bin/python scripts/post_replies.py   # reads YouTube, posts and spends nothing

It screens each reply, which spends Gemini from the allowance uploads share,
so the workflow runs it after the day's second upload (src/replies.py).
Everything it posts stays in the queue file, which the workflow commits.
"""
import csv
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import config, replies  # noqa: E402


def titles():
    """The question each upload asked, the screen's context for a reply."""
    if not config.UPLOAD_LOG.exists():
        return {}
    with open(config.UPLOAD_LOG, newline="", encoding="utf-8") as f:
        return {r["video_id"]: r.get("post_title", "") for r in csv.DictReader(f)}


def main():
    from src import screen, youtube
    rows = replies.load()
    if not any(r.get("status") == "queued" for r in rows):
        print("No replies queued.")
        return 0
    client = youtube.ReplyClient()
    channel = client.channel_id()
    if not channel:
        sys.exit("Could not read our channel's ID: not replying, as our own comments could not be told apart.")
    now = datetime.datetime.now(datetime.timezone.utc)
    for line in replies.post_due(rows, now.date(), client, screen.screen, channel, titles(), now,
                                 dry_run=config.DRY_RUN):
        print(line)
    if not config.DRY_RUN:
        replies.save(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
