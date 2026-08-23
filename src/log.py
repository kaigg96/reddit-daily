"""Upload/experiment log (PRD R0.2): one row per successful live upload,
committed back by the workflow. Joins against YouTube analytics on video_id."""

import csv

from . import config

FIELDS = [
    "timestamp_utc", "video_id", "subreddit", "post_title", "video_title",
    "title_style", "voice", "bg_clip", "music_track", "format_version", "duration_s",
]


SCREEN_FIELDS = [
    "timestamp_utc", "subreddit", "post_title", "action",
    "category", "reason", "source", "dropped_comments",
]


def _append(path, fields, row):
    is_new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if is_new:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def append_upload_log(row):
    _append(config.UPLOAD_LOG, FIELDS, row)


def append_screen_log(row):
    """R4.6 audit trail — one row per non-pass screen verdict, for weekly
    false-positive review."""
    _append(config.SCREEN_LOG, SCREEN_FIELDS, row)
