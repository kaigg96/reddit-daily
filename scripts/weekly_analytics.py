"""Weekly analytics snapshot (PRD R4.2).

Appends one row per channel video to analysis/analytics_snapshots.csv using the
YouTube Analytics API (OAuth, yt-analytics.readonly scope). Repeated weekly runs
build per-video time series, so views@7d/views@28d deltas and retention trends
become computable — the measurement backbone for every format/title experiment.

Read-only against YouTube; the only side effect is the CSV append (committed by
the weekly workflow). Safe to run manually; refuses to double-append same-day.

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

from googleapiclient.discovery import build

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import config  # noqa: E402
from src.youtube import _authenticate  # noqa: E402

OUT = config.ROOT / "analysis" / "analytics_snapshots.csv"
FIELDS = ["snapshot_date", "video_id", "published_at", "views", "likes", "comments",
          "shares", "est_minutes_watched", "avg_view_duration_s", "avg_view_pct"]
METRICS = ("views,likes,comments,shares,estimatedMinutesWatched,"
           "averageViewDuration,averageViewPercentage")
CHUNK = 200  # Analytics API filter-list limit is 500; stay well under


def all_uploads(yt):
    """[(video_id, published_at)] for every video on the channel, via OAuth."""
    channel = yt.channels().list(mine=True, part="contentDetails").execute()
    playlist = channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    videos, page = [], None
    while True:
        kwargs = {"pageToken": page} if page else {}
        resp = yt.playlistItems().list(
            part="contentDetails", playlistId=playlist, maxResults=50, **kwargs
        ).execute()
        videos += [
            (it["contentDetails"]["videoId"], it["contentDetails"].get("videoPublishedAt", ""))
            for it in resp["items"]
        ]
        page = resp.get("nextPageToken")
        if not page:
            break
    return videos


def fetch_stats(ya, video_ids, end_date):
    stats = {}
    for i in range(0, len(video_ids), CHUNK):
        chunk = video_ids[i:i + CHUNK]
        resp = ya.reports().query(
            ids="channel==MINE",
            startDate="2024-01-01",
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


def median(xs):
    return sorted(xs)[len(xs) // 2] if xs else float("nan")


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
            print(f"  {key}={name}: n={len(vals)} median avg_view_pct={median(vals):.1f}")


def main():
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    if OUT.exists():
        with open(OUT) as f:
            if any(row.startswith(today) for row in f):
                sys.exit(f"snapshot for {today} already present; refusing to double-append")

    creds = _authenticate()
    yt = build("youtube", "v3", credentials=creds)
    ya = build("youtubeAnalytics", "v2", credentials=creds)

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


if __name__ == "__main__":
    main()
