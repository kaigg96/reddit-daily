"""Upload/experiment log (PRD R0.2): one row per successful live upload,
committed back by the workflow. Joins against YouTube analytics on video_id."""

import csv

from . import config

FIELDS = [
    "timestamp_utc", "video_id", "subreddit", "post_title", "video_title",
    "title_style", "voice", "bg_clip", "music_track", "format_version", "duration_s",
    # Added 2026-08-23 to test whether deviating from Reddit's own ranking costs
    # anything, before building any ranker on top of it (PRD R4.4 Step 0).
    "candidate_rank", "topic",
    # Added 2026-09-07: fail-soft API outcomes previously printed to stdout and
    # vanished with the Actions log, so a failed caption upload was only
    # discoverable by querying YouTube directly.
    "caption_ok", "comment_ok",
]


SCREEN_FIELDS = [
    "timestamp_utc", "subreddit", "post_title", "action",
    "category", "reason", "source", "dropped_comments",
]


def _migrate_header(path, fields):
    """Rewrite an existing CSV under a new column set, backfilling blanks.

    Without this, appending rows with added fields to a file whose header
    predates them silently misaligns every new row against the old header.
    """
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and list(rows[0].keys()) == fields:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: (r.get(k) or "") for k in fields})
    print(f"Log schema migrated: {path.name} -> {len(fields)} columns")


def _append(path, fields, row):
    is_new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not is_new:
        _migrate_header(path, fields)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if is_new:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def append_upload_log(row):
    _append(config.UPLOAD_LOG, FIELDS, row)


def append_screen_log(row):
    """R4.6 audit trail — one row per non-pass screen verdict, for weekly
    false-positive review."""
    _append(config.SCREEN_LOG, SCREEN_FIELDS, row)
