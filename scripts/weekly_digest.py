"""Weekly digest generator (PRD R4.2 digest).

Builds the Monday check-in issue body from the fresh analytics snapshot,
upload_log.csv, and live channel reads. Writes:
  assets/gen/digest.md        — issue body (markdown)
  assets/gen/digest_title.txt — issue title (status surfaces in the email subject)

Read-only against YouTube; the workflow posts the issue via `gh`.

Content contract (owner-approved 2026-07-20): Status line, Pipeline health,
Performance, Video of the week, TODOs. Deliberately excluded: experiments
readout, analytics-lag footnotes, per-video engagement tables, subscriber
attribution — see PRD R4.2 deferred-metrics note.
"""

import csv
import datetime
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import analytics, config  # noqa: E402

RETENTION_TARGET = 70
LAG_DAYS = 2      # Analytics API lag: younger uploads aren't "measurable" yet
ZERO_VIEW_DAYS = 3  # logged uploads older than this with 0 views get flagged


def fetch_channel(yt):
    ch = yt.channels().list(mine=True, part="statistics").execute()["items"][0]
    subs = int(ch["statistics"]["subscriberCount"])
    items = analytics.list_uploaded_videos(yt, part="snippet,contentDetails,status")
    videos = [
        {
            "id": it["contentDetails"]["videoId"],
            "published": it["contentDetails"].get("videoPublishedAt", ""),
            "title": it["snippet"]["title"],
            "privacy": it.get("status", {}).get("privacyStatus", "unknown"),
        }
        for it in items
    ]
    return subs, videos


def screen_skips(days=7):
    """R4.6 audit: skips logged in the window, for the weekly false-positive review."""
    path = config.SCREEN_LOG
    if not path.exists():
        return []
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(days=days)).isoformat()
    with open(path) as f:
        return [r for r in csv.DictReader(f)
                if r["timestamp_utc"] >= cutoff and r["action"].startswith("skip")]


def humanize(n):
    return f"{n / 1_000_000:.1f}M" if n >= 1_000_000 else (f"{n / 1000:.1f}K" if n >= 1000 else str(n))


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    iso = lambda days: (now - datetime.timedelta(days=days)).isoformat()

    yt = analytics.youtube_client()
    subs, channel_videos = fetch_channel(yt)
    channel_ids = {v["id"] for v in channel_videos}

    snap_rows = list(csv.DictReader(open(config.ROOT / "analysis" / "analytics_snapshots.csv")))
    snap_dates = sorted({r["snapshot_date"] for r in snap_rows})
    latest = {r["video_id"]: r for r in snap_rows if r["snapshot_date"] == snap_dates[-1]}
    snap_age = (now.date() - datetime.date.fromisoformat(snap_dates[-1])).days

    log_rows = list(csv.DictReader(open(config.UPLOAD_LOG))) if config.UPLOAD_LOG.exists() else []
    log_ids = {r["video_id"] for r in log_rows}

    # --- pipeline health ---
    # Cadence over complete calendar days (a rolling cutoff would clip the
    # earliest day's uploads and report false misses at the boundary).
    last_7_days = [(now.date() - datetime.timedelta(days=d)).isoformat() for d in range(1, 8)]
    per_day = Counter(v["published"][:10] for v in channel_videos if v["published"] >= iso(9))
    week_count = sum(per_day.get(d, 0) for d in last_7_days)
    missed_days = [d for d in last_7_days if per_day.get(d, 0) < 2]
    week_videos = [v for v in channel_videos if v["published"][:10] in last_7_days]

    # Unlogged = on the channel but absent from upload_log: catches uploads
    # where the run died between upload and logging. 15-min buffer covers a
    # failed-then-retried first attempt; 7-day window makes flags transient
    # rather than permanent noise.
    unlogged = []
    if log_rows:
        era_start = min(r["timestamp_utc"] for r in log_rows)
        buffered = (datetime.datetime.fromisoformat(era_start)
                    - datetime.timedelta(minutes=15)).isoformat()
        unlogged = [v for v in channel_videos
                    if v["published"] >= max(buffered, iso(7))
                    and v["id"] not in log_ids]
    logged_gone = sorted(log_ids - channel_ids)
    # Zero-view flags mean suppression only if (a) the snapshot actually covers
    # the video — one published after the last snapshot has no data, not zero
    # views — and (b) the video is public; an owner-privatized video looks
    # identical to a suppressed one in the analytics data.
    privacy = {v["id"]: v["privacy"] for v in channel_videos}
    # A video must have been at least ZERO_VIEW_DAYS old *at snapshot time* for
    # its zero to mean anything (analytics lag ~1-2 days behind the snapshot).
    zero_cutoff = (datetime.date.fromisoformat(snap_dates[-1])
                   - datetime.timedelta(days=ZERO_VIEW_DAYS)).isoformat()
    zero_views = [r for r in log_rows
                  if r["timestamp_utc"][:10] < zero_cutoff
                  and int(latest.get(r["video_id"], {}).get("views", 0)) == 0
                  and privacy.get(r["video_id"], "public") == "public"]
    non_public = [r for r in log_rows
                  if r["timestamp_utc"] >= iso(7)
                  and privacy.get(r["video_id"], "public") != "public"]
    skips = screen_skips()

    # --- status ---
    hard, soft = [], []
    if missed_days:
        hard.append(f"missed uploads on {', '.join(sorted(missed_days))}")
    if logged_gone:
        hard.append(f"{len(logged_gone)} logged video(s) missing from channel")
    if snap_age > 8:
        hard.append(f"analytics snapshot is {snap_age} days old")
    if unlogged:
        soft.append(f"{len(unlogged)} unlogged video{'s' if len(unlogged) > 1 else ''}")
    if zero_views:
        soft.append(f"{len(zero_views)} upload(s) still at 0 views after {ZERO_VIEW_DAYS}+ days")
    if non_public:
        soft.append(f"{len(non_public)} upload(s) not public")

    date_label = f"{now:%b} {now.day}"
    if hard:
        title = f"Weekly digest — {date_label} — ACTION NEEDED: {hard[0]}"
        status = f"**Status: ACTION NEEDED — {'; '.join(hard + soft)}.**"
    elif soft:
        title = f"Weekly digest — {date_label} — ran clean; {soft[0]}"
        noun = "One item" if len(soft) == 1 else f"{len(soft)} items"
        status = f"**Status: all scheduled runs completed. {noun} flagged below.**"
    else:
        title = f"Weekly digest — {date_label} — ran clean"
        status = "**Status: all scheduled runs completed.**"

    # --- performance (measurable = old enough for analytics data + views > 0) ---
    def views(vid):
        return int(latest.get(vid, {}).get("views", 0))

    def pct(vid):
        return float(latest.get(vid, {}).get("avg_view_pct", 0))

    measurable = [v for v in week_videos if v["published"] < iso(LAG_DAYS) and views(v["id"]) > 0]
    d90 = [v for v in channel_videos
           if iso(90) <= v["published"] < iso(LAG_DAYS) and views(v["id"]) > 0]
    med_week = analytics.median([views(v["id"]) for v in measurable])
    med_pct = analytics.median([pct(v["id"]) for v in measurable])
    med_90 = analytics.median([views(v["id"]) for v in d90])
    views_90 = sum(views(v["id"]) for v in d90)

    cadence = f"{week_count}/14 uploads"
    cadence += " (no missed days)" if not missed_days else f" — **missed: {', '.join(sorted(missed_days))}**"
    if unlogged:
        diff = (f"**{len(unlogged)} unlogged video{'s' if len(unlogged) > 1 else ''}** ("
                + ", ".join(v["published"][:10] for v in unlogged[:3]) + ")")
    elif logged_gone:
        diff = f"**missing from channel:** {', '.join(f'`{i}`' for i in logged_gone[:3])}"
    else:
        diff = "clean"
    freshness = "current" if snap_age <= 8 else f"**{snap_age} days stale**"

    lines = [status, ""]
    lines.append(f"**Pipeline health** — Cadence: {cadence} · Log↔channel diff: {diff} · "
                 f"Analytics data: {freshness}")
    lines.append("")
    lines.append("**Performance**")
    if measurable:
        lines.append(f"- Median views (this week's measurable uploads): **{med_week}** — 90d median: {med_90}")
        lines.append(f"- Avg % viewed: **{med_pct:.0f}%** vs ≥{RETENTION_TARGET}% target")
    else:
        lines.append("- No measurable uploads yet this week")
    lines.append(f"- Subscribers: **{subs}**")
    lines.append(f"- ~90d views: ~{humanize(views_90)} (approx)")
    lines.append("")
    if measurable:
        top = max(measurable, key=lambda v: views(v["id"]))
        lines.append(f"**🏆 Video of the week** — [{top['title']}]"
                     f"(https://youtube.com/shorts/{top['id']}) — "
                     f"{views(top['id'])} views, {pct(top['id']):.0f}% avg viewed")
        lines.append("")

    # R4.6 audit line — only when the screen actually skipped something, so a
    # quiet week stays quiet.
    if skips:
        cats = ", ".join(sorted({s["category"] for s in skips if s["category"]}))
        lines.append(f"**Suppression screen** — {len(skips)} post(s) skipped this week ({cats}). "
                     f"Review `analysis/screen_log.csv` for false positives.")
        lines.append("")

    todos = []
    if log_rows and all(r["bg_clip"].startswith("procedural") for r in log_rows):
        todos.append("b-roll library still empty (all uploads on procedural background)")
    if log_rows and len({r["music_track"] for r in log_rows}) <= 1:
        todos.append("music variety (single track in rotation)")
    if todos:
        lines.append("**TODOs** — " + " · ".join(todos))

    body = "\n".join(lines).rstrip() + "\n"
    (config.GEN / "digest.md").write_text(body)
    (config.GEN / "digest_title.txt").write_text(title)
    print(f"title: {title}\n---\n{body}")


if __name__ == "__main__":
    main()
