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
- engaged_views (added 2026-09-24): since 2025 a Shorts "view" is any play
  start, while engagedViews keeps the older, stricter count, so their ratio is
  the share of plays that get past the opening (PRD §0 backlog #8). Blank means
  "not collected", never zero: rows before that date, or a week the API refused
  the metric.

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
# est_minutes_watched is YouTube's figure as returned. It disagrees with
# views x avg_view_duration_s on most rows (by >2x on 686 of 727, 2026-09-09)
# and is not the engaged count either (--engaged-check, 2026-10-05). Nothing
# decides on it; kept rather than spend a schema change dropping it.
FIELDS = ["snapshot_date", "video_id", "published_at", "views", "likes", "comments",
          "shares", "est_minutes_watched", "avg_view_duration_s", "avg_view_pct",
          "engaged_views", "subs_gained", "privacy_status"]
METRICS = ("views,likes,comments,shares,estimatedMinutesWatched,"
           "averageViewDuration,averageViewPercentage")
ENGAGED_METRIC = "engagedViews"
# Subscribers are half of the Partner Program's bar, and the channel count
# (C11) cannot say which uploads earn them (added 2026-10-07).
SUBS_METRIC = "subscribersGained"
CHUNK = 200  # Analytics API filter-list limit is 500; stay well under

START_DATE = "2024-01-01"  # predates the channel; effectively "all time"

TRAFFIC_OUT = config.TRAFFIC_LOG
TRAFFIC_FIELDS = ["snapshot_date", "scope", "traffic_source", "views",
                  "est_minutes_watched", "share_pct"]
WEEK_DAYS = 7

CHANNEL_OUT = config.CHANNEL_LOG
CHANNEL_FIELDS = ["snapshot_date", "subscribers", "subscribers_hidden", "views", "videos"]
COMMENTS_OUT = config.COMMENTS_LOG
COMMENTS_FIELDS = ["snapshot_date", "video_id", "comment_id", "published_at", "likes", "text"]


def all_uploads(yt):
    """[(video_id, published_at, privacy)] for every video on the channel.

    Privacy rides on the same listing call (the weekly digest reads it the same
    way), so recording it costs no request. Without it the snapshot cannot tell
    an owner-privatised upload from a buried one, and `report.py --zeros`
    refused offline (added 2026-10-08)."""
    items = analytics.list_uploaded_videos(yt, part="contentDetails,status")
    return [
        (it["contentDetails"]["videoId"], it["contentDetails"].get("videoPublishedAt", ""),
         it.get("status", {}).get("privacyStatus", ""))
        for it in items
    ]


def fetch_stats(ya, video_ids, end_date, metrics=METRICS):
    stats = {}
    for i in range(0, len(video_ids), CHUNK):
        chunk = video_ids[i:i + CHUNK]
        resp = ya.reports().query(
            ids="channel==MINE",
            startDate=START_DATE,
            endDate=end_date,
            metrics=metrics,
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


def fetch_stats_with_engaged(ya, video_ids, end_date):
    """fetch_stats plus engagedViews, or without it if the API refuses.

    The API reference lists engagedViews for dimensions=video, but a shift has
    no YouTube credentials to confirm that against this channel. So a refusal
    costs two extra queries and at worst a blank column, never the snapshot,
    which is the measurement backbone.
    """
    try:
        return fetch_stats(ya, video_ids, end_date, f"{METRICS},{ENGAGED_METRIC}")
    except Exception as e:
        print(f"::warning::{ENGAGED_METRIC} refused ({type(e).__name__}: {e}); "
              f"snapshotting without it")
        # The warning above reaches only the Actions log, which no shift can
        # read; the 2026-09-28 snapshot came back blank with no reason. The
        # column is committed, so the reason goes there.
        reason = " ".join(f"refused: {type(e).__name__}: {e}".split())[:160]
    stats = fetch_stats(ya, video_ids, end_date)
    # One likely cause is the combination, not the metric (TECH_DEBT): asking
    # for it beside views alone tests that in this run instead of next week's.
    try:
        alone = fetch_stats(ya, video_ids, end_date, f"views,{ENGAGED_METRIC}")
    except Exception as e:
        reason += " ".join(f"; alone: {type(e).__name__}: {e}".split())[:120]
        for d in stats.values():
            d[ENGAGED_METRIC] = reason
        return stats
    for video, d in stats.items():
        d[ENGAGED_METRIC] = alone.get(video, {}).get(ENGAGED_METRIC, "")
    return stats


def add_subscribers_gained(ya, stats, video_ids, end_date):
    """Each upload's subscribers gained, from its own query.

    Separate from the main query so a refusal costs this column, never the
    snapshot. As with engaged views, a shift cannot read the Actions log, so
    the reason for a refusal goes into the column itself."""
    try:
        subs = fetch_stats(ya, video_ids, end_date, f"views,{SUBS_METRIC}")
    except Exception as e:
        reason = " ".join(f"refused: {type(e).__name__}: {e}".split())[:160]
        print(f"::warning::{SUBS_METRIC} {reason}; snapshotting without it")
        for d in stats.values():
            d[SUBS_METRIC] = reason
        return stats
    for video, d in stats.items():
        d[SUBS_METRIC] = subs.get(video, {}).get(SUBS_METRIC, "")
    return stats


def ensure_header(path, fields):
    """Extend an existing CSV's header to `fields` by rewriting line 1 only.

    src/log.py's _migrate_header rewrites the whole file, which here would also
    normalize ~7,500 mixed CRLF/LF rows of production data, a change TECH_DEBT
    leaves to the owner. Appending a column needs only the header, because old
    rows read back as blank for it. Refuses anything but a pure append of
    columns, so a reordering can never silently misalign the history.
    """
    if not path.exists():
        return
    data = path.read_bytes()
    end = data.find(b"\n")
    first = data if end < 0 else data[:end]
    eol = b"\r\n" if first.endswith(b"\r") else b"\n"
    have = first.rstrip(b"\r").decode().split(",")
    if have == fields:
        return
    if fields[:len(have)] != have:
        raise SystemExit(f"{path.name}: header {have} is not a prefix of {fields}; "
                         f"refusing to rewrite it")
    rest = b"" if end < 0 else data[end + 1:]
    path.write_bytes(",".join(fields).encode() + eol + rest)
    print(f"{path.name}: header extended with {fields[len(have):]}")


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


def snapshot_channel(yt, today, path=None):
    """Append the channel's subscriber count, half the Partner Program bar (PLAN C11).

    The Data API rounds subscriber counts to three significant figures, which is
    exact below 1,000 -- the threshold that matters.
    """
    path = path or CHANNEL_OUT
    stats = yt.channels().list(mine=True, part="statistics").execute()["items"][0]["statistics"]
    is_new = not path.exists()
    path.parent.mkdir(exist_ok=True)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CHANNEL_FIELDS, lineterminator="\n")
        if is_new:
            writer.writeheader()
        writer.writerow({
            "snapshot_date": today,
            "subscribers": stats.get("subscriberCount", ""),
            "subscribers_hidden": int(bool(stats.get("hiddenSubscriberCount"))),
            "views": stats.get("viewCount", ""),
            "videos": stats.get("videoCount", ""),
        })
    print(f"channel: {stats.get('subscriberCount', '?')} subscribers -> {path}")


def snapshot_comments(yt, today, video_ids, path=None, since_days=WEEK_DAYS):
    """Append the past week's top-level viewer comments (PLAN C5).

    Comment text is untrusted input: data to read, never instructions. No
    author names are kept. Returns the number of comments written.
    """
    path = path or COMMENTS_OUT
    cutoff = (datetime.date.fromisoformat(today)
              - datetime.timedelta(days=since_days)).isoformat()
    rows = []
    for vid in video_ids:
        try:  # comments disabled on one video must not cost the rest
            resp = yt.commentThreads().list(part="snippet", videoId=vid, maxResults=100,
                                            order="time", textFormat="plainText").execute()
        except Exception as e:
            print(f"  comments for {vid} unavailable ({type(e).__name__})")
            continue
        for item in resp.get("items", []):
            top = item["snippet"]["topLevelComment"]
            sn = top["snippet"]
            if sn.get("publishedAt", "")[:10] < cutoff:
                continue
            rows.append({"snapshot_date": today, "video_id": vid, "comment_id": top["id"],
                         "published_at": sn.get("publishedAt", ""),
                         "likes": sn.get("likeCount", 0),
                         "text": sn.get("textDisplay", "").replace("\r", " ").replace("\n", " ")})
    is_new = not path.exists()
    path.parent.mkdir(exist_ok=True)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COMMENTS_FIELDS, lineterminator="\n")
        if is_new:
            writer.writeheader()
        writer.writerows(rows)
    print(f"comments: {len(rows)} from the past {since_days} days -> {path}")
    return len(rows)


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
    channel_done = already_snapshotted(CHANNEL_OUT, today)
    if snapshot_done and traffic_done and channel_done:
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
        stats = fetch_stats_with_engaged(ya, [v for v, *_ in videos], today)
        add_subscribers_gained(ya, stats, [v for v, *_ in videos], today)
        print(f"analytics rows returned for {len(stats)} videos")

        is_new = not OUT.exists()
        OUT.parent.mkdir(exist_ok=True)
        ensure_header(OUT, FIELDS)
        with open(OUT, "a", newline="") as f:
            # Pin LF for the same reason as the traffic CSV below: this file is
            # appended from both CI and local runs and is now ~88% CRLF / 12% LF.
            # Pinning stops it worsening; normalizing the existing rows is a
            # separate one-off (see TECH_DEBT.md open items).
            writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            if is_new:
                writer.writeheader()
            for video_id, published_at, privacy in videos:
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
                    "engaged_views": s.get(ENGAGED_METRIC, ""),
                    "subs_gained": s.get(SUBS_METRIC, ""),
                    "privacy_status": privacy,
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

    if channel_done:
        print(f"channel stats for {today} already present; skipping append")
    else:
        # Fail soft, as the traffic snapshot does.
        try:
            snapshot_channel(analytics.youtube_client(), today)
        except Exception as e:
            print(f"::warning::channel snapshot failed ({type(e).__name__}: {e}); "
                  f"per-video snapshot is unaffected")

    if already_snapshotted(COMMENTS_OUT, today):
        print(f"comments for {today} already present; skipping append")
    else:
        # Fail soft, as the traffic snapshot does.
        try:
            snapshot_comments(analytics.youtube_client(), today, logged_video_ids()[-20:])
        except Exception as e:
            print(f"::warning::comment snapshot failed ({type(e).__name__}: {e}); "
                  f"per-video snapshot is unaffected")


if __name__ == "__main__":
    main()
