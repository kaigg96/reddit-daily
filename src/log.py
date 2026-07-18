"""Upload/experiment log (PRD R0.2): one row per successful live upload,
committed back by the workflow. Joins against YouTube analytics on video_id."""

import csv

from . import config

FIELDS = [
    "timestamp_utc", "video_id", "subreddit", "post_title", "video_title",
    "title_style", "voice", "bg_clip", "music_track", "format_version", "duration_s",
]


def append_upload_log(row):
    is_new = not config.UPLOAD_LOG.exists()
    with open(config.UPLOAD_LOG, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in FIELDS})
