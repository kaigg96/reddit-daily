"""Weekly analytics snapshot (PRD R4.2) + traffic-source telemetry (R4.7).

Appends one row per channel video to analysis/analytics_snapshots.csv using the
YouTube Analytics API (OAuth, yt-analytics.readonly scope). Repeated weekly runs
build per-video time series, so views@7d/views@28d deltas and retention trends
become computable — the measurement backbone for every format/title experiment.

Also appends the traffic-source mix (R4.7) to analysis/traffic_sources.csv:
what share of views arrives from the Shorts feed vs search vs everything else,
which decides whether SEO-oriented work is ever worth revisiting.

Read-only against YouTube; the only side effects are the two CSV appends
(committed by the weekly workflow). Safe to run manually; each file refuses to
double-append on the same day, independently — so a rerun after a partial
failure fills in only what is missing.

Notes:
- averageViewPercentage can exceed 100 for Shorts (loops count as re-watches).
- Thumbnail impressions / swipe-away rate are NOT exposed by the Analytics API
  (Studio-only), so they are deliberately absent here.

Usage: venv/bin/python scripts/weekly_analytics.py
Env:   YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN
"""

import csv
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import analytics, config, insights  # noqa: E402

OUT = config.ANALYTICS_SNAPSHOTS
FIELDS = ["snapshot_date", "video_id", "published_at", "views", "likes", "comments",
          "shares", "est_minutes_watched", "avg_view_duration_s", "avg_view_pct"]
METRICS = ("views,likes,comments,shares,estimatedMinutesWatched,"
           "averageViewDuration,averageViewPercentage")
CHUNK = 200  # Analytics API filter-list limit is 500; stay well under

START_DATE = "2024-01-01"  # predates the channel; effectively "all time"

TRAFFIC_OUT = config.TRAFFIC_LOG
TRAFFIC_FIELDS = ["snapshot_date", "scope", "traffic_source", "views",
                  "est_minutes_watched", "share_pct"]
WEEK_DAYS = 7


def all_uploads(yt):
    """[(video_id, published_at)] for every video on the channel."""
    items = analytics.list_uploaded_videos(yt, part="contentDetails")
    return [
        (it["contentDetails"]["videoId"], it["contentDetails"].get("videoPublishedAt", ""))
        for it in items
    ]


def fetch_stats(ya, video_ids, end_date):
    stats = {}
    for i in range(0, len(video_ids), CHUNK):
        chunk = video_ids[i:i + CHUNK]
        resp = ya.reports().query(
            ids="channel==MINE",
            startDate=START_DATE,
            endDate=end_date,
            metrics=METRICS,
            dimensions="video",
            filters="video==" + ",".join(chunk),
            maxResults=len(chunk),
            sort="-views",
        ).execute()
        columns = [h["name"] for h in resp.get("columnHeaders", [])]
        for row in resp.get("rows", []):
            d = dict(zip(columns, row))
            stats[d["video"]] = d
    return stats


def print_experiment_summary(stats):
    """Small log-visible readout: retention by format_version and title_style."""
    if not config.UPLOAD_LOG.exists():
        return
    with open(config.UPLOAD_LOG) as f:
        log_rows = [r for r in csv.DictReader(f) if r["video_id"] in stats]
    for key in ("format_version", "title_style"):
        groups = {}
        for r in log_rows:
            groups.setdefault(r[key], []).append(
                float(stats[r["video_id"]].get("averageViewPercentage", 0)))
        for name, vals in sorted(groups.items()):
            print(f"  {key}={name}: n={len(vals)} median avg_view_pct={analytics.median(vals):.1f}")


# ---------------------------------------------------------------- R4.7 traffic sources


def logged_video_ids():
    """Video ids from upload_log.csv — the current-format cohort.

    The channel's all-time mix is dominated by ~900 pre-overhaul v1 uploads, so
    the question "does search earn anything *under the format we ship today*"
    needs this narrower cohort to be answerable at all.
    """
    if not config.UPLOAD_LOG.exists():
        return []
    with open(config.UPLOAD_LOG) as f:
        ids = [r["video_id"].strip() for r in csv.DictReader(f) if r.get("video_id")]
    return list(dict.fromkeys(ids))  # dedupe; a repeated id would double-count


def fetch_traffic(ya, start_date, end_date, video_ids=None):
    """[(source, views, minutes)] for one scope; video_ids=None → whole channel.

    dimensions="video,insightTrafficSourceType" is rejected by the API, and a
    video filter aggregates the whole list rather than splitting it — so a
    chunked cohort comes back as several partial breakdowns that the caller
    must sum (insights.aggregate_traffic does).
    """
    if video_ids is None:
        chunks = [None]
    else:
        chunks = [video_ids[i:i + CHUNK] for i in range(0, len(video_ids), CHUNK)]

    rows = []
    for chunk in chunks:
        kwargs = {"filters": "video==" + ",".join(chunk)} if chunk else {}
        resp = ya.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched",
            dimensions="insightTrafficSourceType",
            sort="-views",
            **kwargs,
        ).execute()
        columns = [h["name"] for h in resp.get("columnHeaders", [])]
        for row in resp.get("rows", []):
            d = dict(zip(columns, row))
            rows.append((d["insightTrafficSourceType"],
                         d.get("views", 0),
                         d.get("estimatedMinutesWatched", 0)))
    return rows


def traffic_scopes(today):
    """(scope name, startDate, video_ids) for each cohort we track weekly.

    channel_7d is the time series: one non-overlapping window per weekly run.
    Its endDate is today, and Analytics lags 1-2 days, so it really covers ~5-6
    settled days — a constant bias, so week-over-week comparison stays valid.
    """
    week_start = (datetime.date.fromisoformat(today)
                  - datetime.timedelta(days=WEEK_DAYS)).isoformat()
    return [
        ("channel_lifetime", START_DATE, None),
        ("channel_7d", week_start, None),
        ("logged_uploads", START_DATE, logged_video_ids()),
    ]


def snapshot_traffic(ya, today):
    """Append one row per (scope, traffic source) to analysis/traffic_sources.csv."""
    is_new = not TRAFFIC_OUT.exists()
    TRAFFIC_OUT.parent.mkdir(exist_ok=True)
    written = 0
    with open(TRAFFIC_OUT, "a", newline="") as f:
        # Pin LF: csv defaults to CRLF, and this file gets appended to from both
        # CI (autocrlf off) and local runs (autocrlf=input, which normalizes on
        # add) — which is how analytics_snapshots.csv ended up with 6601 CRLF
        # lines and ~900 LF ones. Harmless to parse, ugly in every diff.
        writer = csv.DictWriter(f, fieldnames=TRAFFIC_FIELDS, lineterminator="\n")
        if is_new:
            writer.writeheader()
        for scope, start_date, video_ids in traffic_scopes(today):
            if video_ids is not None and not video_ids:
                print(f"  {scope}: no videos in cohort; skipped")
                continue
            rows = insights.aggregate_traffic(
                fetch_traffic(ya, start_date, today, video_ids))
            for r in rows:
                writer.writerow({
                    "snapshot_date": today,
                    "scope": scope,
                    "traffic_source": r.source,
                    "views": int(r.views),
                    "est_minutes_watched": int(r.minutes),
                    "share_pct": f"{r.share_pct:.2f}",
                })
            written += len(rows)
            print(f"  {scope}: {insights.format_traffic_mix(rows)}  "
                  f"[discovery {insights.discovery_share(rows):.1f}% of "
                  f"{int(sum(r.views for r in rows))} views]")
    print(f"appended {written} traffic-source rows to {TRAFFIC_OUT}")


def already_snapshotted(path, today):
    """True if this file already has rows for today (both CSVs lead with the date)."""
    if not path.exists():
        return False
    with open(path) as f:
        return any(row.startswith(today) for row in f)


def main():
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    snapshot_done = already_snapshotted(OUT, today)
    traffic_done = already_snapshotted(TRAFFIC_OUT, today)
    if snapshot_done and traffic_done:
        # benign: manual rerun on snapshot day — keep exit 0 so the digest step
        # still runs afterward
        print(f"snapshot and traffic for {today} already present; skipping append")
        return

    ya = analytics.youtube_analytics_client()

    if snapshot_done:
        print(f"per-video snapshot for {today} already present; skipping append")
    else:
        yt = analytics.youtube_client()
        videos = all_uploads(yt)
        print(f"channel has {len(videos)} videos")
        stats = fetch_stats(ya, [v for v, _ in videos], today)
        print(f"analytics rows returned for {len(stats)} videos")

        is_new = not OUT.exists()
        OUT.parent.mkdir(exist_ok=True)
        with open(OUT, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if is_new:
                writer.writeheader()
            for video_id, published_at in videos:
                s = stats.get(video_id, {})
                writer.writerow({
                    "snapshot_date": today,
                    "video_id": video_id,
                    "published_at": published_at,
                    "views": s.get("views", 0),
                    "likes": s.get("likes", 0),
                    "comments": s.get("comments", 0),
                    "shares": s.get("shares", 0),
                    "est_minutes_watched": s.get("estimatedMinutesWatched", 0),
                    "avg_view_duration_s": s.get("averageViewDuration", 0),
                    "avg_view_pct": s.get("averageViewPercentage", 0),
                })
        print(f"appended {len(videos)} rows to {OUT}")
        print_experiment_summary(stats)

    if traffic_done:
        print(f"traffic sources for {today} already present; skipping append")
    else:
        # Fail soft: the per-video snapshot is the measurement backbone and must
        # not be lost to a failure in the telemetry that rides alongside it.
        try:
            snapshot_traffic(ya, today)
        except Exception as e:
            print(f"::warning::traffic-source snapshot failed ({type(e).__name__}: {e}); "
                  f"per-video snapshot is unaffected")


if __name__ == "__main__":
    main()
