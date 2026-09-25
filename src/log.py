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
    # Added 2026-09-19: the other three fail-soft Gemini calls. Only the screen
    # was observable (via screen_source/topic); a failed keyword, title or CTA
    # call left no trace, and the title regression that prompted these columns
    # was found by comparing video_title back to post_title -- an inference
    # that breaks the moment a generated title happens to match the question.
    "title_ok", "keywords_ok", "cta_ok",
    # Added 2026-09-09: 14% of uploads since the screen shipped carry no topic,
    # meaning the Gemini call failed and the run shipped on the keyword backstop
    # — invisible in the logs, and it makes the R4.6 audit an audit of a screen
    # nobody can confirm ran.
    "screen_source",
    # Added 2026-09-24: why the metadata call failed, blank when it answered.
    # The ok-flags above say THAT it failed; a 429 on the shared daily cap and
    # a timeout need different fixes, and the flags cannot tell them apart.
    "meta_failure",
    # Added 2026-09-24 (PRD R4.4 Step 0.5): the topic of every eligible
    # candidate, in rank order, "|"-joined ("?" = unrecognised label, blank =
    # not collected). The log kept only the selected post's topic, so how often
    # a topic ranker would override Reddit's order -- and therefore how long
    # its own bake would take -- could not be estimated.
    "slate_topics",
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
