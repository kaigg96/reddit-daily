"""Performance analysis — the single place "did X work?" gets answered.

This module exists because ad-hoc analysis produced four wrong conclusions in
two weeks (see TECH_DEBT.md Pass 2), two of which nearly caused wasted builds.
The rules below were learned the hard way; encoding them here means they apply
by default instead of being remembered:

1. **Watch-seconds is primary, avg-%-viewed is diagnostic.** Avg-% is a ratio
   whose denominator we control — trimming a video inflates it while adding
   zero real watch time. `Metric.WATCH` is the default for every comparison.
2. **Cohorts must be age-matched.** Retention and views both drift with video
   age, so an unmatched comparison measures age, not the change.
3. **Thin slices report "insufficient", never a median.** A median over 3
   videos on a high-variance channel is noise wearing a number's clothes.
4. **Zero-view videos are excluded from central tendency and counted
   separately.** They're suppression events (R4.6), not weak performance —
   averaging them in hides both signals.

Pure functions here are unit-tested (tests/test_insights.py); the I/O wrappers
that hit the YouTube API are not.
"""

import csv
import datetime
import math
import statistics
from dataclasses import dataclass, field

from . import config

# A comparison needs at least this many videos per side to report a number.
MIN_COHORT = 8
# Analytics lags ~1-2 days; younger videos have meaningless stats.
MIN_AGE_DAYS = 3


class Metric:
    WATCH = "watch_seconds"      # primary — cannot be gamed by trimming
    VIEWS = "views"
    PCT = "avg_view_pct"         # diagnostic only; valid at fixed duration
    LIKES = "likes"
    COMMENTS = "comments"


@dataclass
class Video:
    video_id: str
    published: datetime.datetime
    views: float = 0.0
    watch_seconds: float = 0.0
    avg_view_pct: float = 0.0
    likes: float = 0.0
    comments: float = 0.0
    meta: dict = field(default_factory=dict)   # upload_log row (format_version, topic, ...)

    def age_days(self, now):
        return (now - self.published).total_seconds() / 86400

    def get(self, metric):
        return getattr(self, metric)


@dataclass
class Cohort:
    label: str
    n: int
    median: float
    zero_view_count: int
    median_age: float

    @property
    def sufficient(self):
        return self.n >= MIN_COHORT


@dataclass
class Comparison:
    metric: str
    a: Cohort
    b: Cohort
    age_matched: bool

    @property
    def verdict(self):
        if not (self.a.sufficient and self.b.sufficient):
            return "insufficient data"
        if not self.age_matched:
            return "not age-matched — unreliable"
        if self.b.median == 0:
            return "no baseline"
        delta = (self.a.median - self.b.median) / self.b.median
        if abs(delta) < 0.05:
            return "no material difference"
        return f"{'better' if delta > 0 else 'worse'} by {abs(delta):.0%}"

    def render(self):
        lines = [f"{self.metric}: {self.a.label} vs {self.b.label} -> {self.verdict}"]
        for c in (self.a, self.b):
            flag = "" if c.sufficient else f"  (below MIN_COHORT={MIN_COHORT})"
            zeros = f", {c.zero_view_count} zero-view excluded" if c.zero_view_count else ""
            lines.append(f"    {c.label:24} n={c.n:<4} median={c.median:<8.1f} "
                         f"med_age={c.median_age:.0f}d{zeros}{flag}")
        if not self.age_matched:
            lines.append("    WARNING: cohort ages differ enough to confound this comparison.")
        return "\n".join(lines)


# ---------------------------------------------------------------- pure logic


def median(values):
    return statistics.median(values) if values else float("nan")


def summarize(videos, label, metric, now):
    """Cohort summary. Zero-view videos are counted, not averaged in (rule 4)."""
    live = [v for v in videos if v.views > 0]
    zeros = len(videos) - len(live)
    return Cohort(
        label=label,
        n=len(live),
        median=median([v.get(metric) for v in live]),
        zero_view_count=zeros,
        median_age=median([v.age_days(now) for v in live]) if live else float("nan"),
    )


def ages_comparable(a, b, tolerance=0.5):
    """True when two cohorts' median ages are close enough to compare.

    Tolerance is relative (default 50%) because age effects are roughly
    logarithmic — 10d vs 15d matters far less than 10d vs 200d.
    """
    if not a or not b:
        return False
    ma, mb = median([v.age_days_cached for v in a]), median([v.age_days_cached for v in b])
    if ma <= 0 or mb <= 0:
        return False
    return abs(math.log(ma) - math.log(mb)) <= math.log(1 + tolerance)


def compare(videos_a, videos_b, label_a, label_b, now, metric=Metric.WATCH):
    """Compare two cohorts on `metric`, refusing to mislead when the data can't
    support a conclusion (rules 2 and 3)."""
    for v in videos_a + videos_b:
        v.age_days_cached = v.age_days(now)
    return Comparison(
        metric=metric,
        a=summarize(videos_a, label_a, metric, now),
        b=summarize(videos_b, label_b, metric, now),
        age_matched=ages_comparable(videos_a, videos_b),
    )


def split_by(videos, key):
    """Group videos by an upload_log field (format_version, topic, ...)."""
    out = {}
    for v in videos:
        out.setdefault(str(v.meta.get(key, "")).strip() or "(unset)", []).append(v)
    return out


def age_adjusted_residuals(videos, now):
    """Residual of log-views against the channel's own log-age trend.

    Use when cohorts *can't* be age-matched (e.g. comparing topics across the
    channel's whole history) — it removes the age trend rather than requiring
    similar ages. Returns {video_id: residual}; >0 means it beat the trend.
    """
    pts = [(math.log(max(v.age_days(now), 0.5)), math.log1p(v.views))
           for v in videos if v.views > 0]
    if len(pts) < 3:
        return {}
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    if statistics.stdev(xs) == 0:
        return {}
    slope = statistics.correlation(xs, ys) * statistics.stdev(ys) / statistics.stdev(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return {v.video_id: math.log1p(v.views) - (my + slope * (math.log(max(v.age_days(now), 0.5)) - mx))
            for v in videos if v.views > 0}


# ---------------------------------------------------------------- I/O


def _parse_ts(value):
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_videos(now=None, min_age_days=MIN_AGE_DAYS):
    """Join upload_log.csv against live Analytics. Only logged uploads appear,
    since analysis needs the experiment metadata to be meaningful."""
    from . import analytics  # local import keeps pure logic importable without API deps

    now = now or datetime.datetime.now(datetime.timezone.utc)
    if not config.UPLOAD_LOG.exists():
        return []
    with open(config.UPLOAD_LOG) as f:
        rows = [r for r in csv.DictReader(f) if r.get("video_id")]

    ya = analytics.youtube_analytics_client()
    stats, ids = {}, [r["video_id"] for r in rows]
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        resp = ya.reports().query(
            ids="channel==MINE", startDate="2024-01-01",
            endDate=now.date().isoformat(),
            metrics="views,averageViewDuration,averageViewPercentage,likes,comments",
            dimensions="video", filters="video==" + ",".join(chunk),
            maxResults=len(chunk)).execute()
        cols = [h["name"] for h in resp.get("columnHeaders", [])]
        for row in resp.get("rows", []):
            d = dict(zip(cols, row))
            stats[d["video"]] = d

    videos = []
    for r in rows:
        s = stats.get(r["video_id"])
        if not s:
            continue
        published = _parse_ts(r["timestamp_utc"])
        # Derived dimensions — raw bg_clip is per-file ("pexels_123.mp4",
        # "procedural:8471"), which is too granular to group on.
        r = dict(r)
        bg = (r.get("bg_clip") or "").strip()
        r["background_type"] = ("(unknown)" if not bg else
                                "procedural" if bg.startswith("procedural") else "broll")
        v = Video(
            video_id=r["video_id"], published=published,
            views=float(s.get("views", 0)),
            watch_seconds=float(s.get("averageViewDuration", 0)),
            avg_view_pct=float(s.get("averageViewPercentage", 0)),
            likes=float(s.get("likes", 0)), comments=float(s.get("comments", 0)),
            meta=r,
        )
        if v.age_days(now) >= min_age_days:
            videos.append(v)
    return videos


# ---------------------------------------------------------------- zero-view analysis

ZERO_NEIGHBOURS = 4          # uploads either side used to judge "was the channel alive?"
COLD_SPELL_MEDIAN = 5        # neighbour median at/below this = channel-wide dead patch


def classify_zero_views(channel_videos):
    """Classify every 0-view video, encoding the two traps that have produced
    wrong conclusions on this channel:

    1. **Non-public videos are not suppression.** An owner-privatised video is
       indistinguishable from a suppressed one by view count alone. 10 of this
       channel's 41 zeroes are private; three were once cited as evidence that
       the R4.6 screen was missing benign content.
    2. **A zero inside a channel-wide cold spell is not per-video moderation.**
       Judge each zero against its publish-order neighbours. The chiropractic
       video — once recorded as confirmed suppression case #2 — sat in a patch
       reading `1, 0, 0, 3, 1, [0], 37`; the whole channel was dead.

    `channel_videos` = [{id, published, views, privacy, title}] sorted or not.
    Returns {"non_public": [...], "cold_spell": [...], "isolated": [...]} —
    only `isolated` are genuine per-video suppression candidates.
    """
    vids = sorted(channel_videos, key=lambda v: v["published"])
    public = [v for v in vids if v.get("privacy") == "public"]
    by_id = {v["id"]: i for i, v in enumerate(public)}

    out = {"non_public": [], "cold_spell": [], "isolated": []}
    for v in vids:
        if int(v["views"]) != 0:
            continue
        if v.get("privacy") != "public":
            out["non_public"].append(v)
            continue
        i = by_id[v["id"]]
        before = [int(n["views"]) for n in public[max(0, i - ZERO_NEIGHBOURS):i]]
        after = [int(n["views"]) for n in public[i + 1:i + 1 + ZERO_NEIGHBOURS]]
        # Judge each side separately. A symmetric median straddles a collapse and
        # its recovery, which mis-read the chiropractic video (before: 0,0,3,1 —
        # clearly dead; after: 37,15,43,210 — recovered) as isolated.
        sides = [median(s) for s in (before, after) if s]
        v = dict(v, neighbour_median=min(sides) if sides else float("nan"),
                 before_median=median(before) if before else float("nan"),
                 after_median=median(after) if after else float("nan"))
        bucket = ("cold_spell" if sides and min(sides) <= COLD_SPELL_MEDIAN
                  else "isolated")
        out[bucket].append(v)
    return out


def load_channel_videos(now=None):
    """Every channel video with views + privacy (Data API, near-real-time).

    Deliberately separate from load_videos(): that one joins upload_log against
    the Analytics API, which lags 1-2 days and omits non-logged and private
    videos — all three of which matter for suppression questions.
    """
    from . import analytics
    yt = analytics.youtube_client()
    items = analytics.list_uploaded_videos(yt, part="contentDetails")
    ids = [it["contentDetails"]["videoId"] for it in items]
    out = []
    for i in range(0, len(ids), 50):
        for d in analytics.fetch_video_details(yt, ids[i:i + 50],
                                               part="snippet,statistics,status"):
            out.append({
                "id": d["id"],
                "published": d["snippet"]["publishedAt"],
                "title": d["snippet"]["title"],
                "views": int(d.get("statistics", {}).get("viewCount", 0)),
                "privacy": d["status"]["privacyStatus"],
            })
    return out


# ---------------------------------------------------------------- traffic sources (R4.7)

# The Analytics API does NOT support dimensions="video,insightTrafficSourceType"
# (400 "query is not supported"), and filtering by a video list AGGREGATES that
# list rather than breaking it down. So a true per-video mix costs one API call
# per video — ~1000/week here — for denominators (~100 views) too small to read.
# Traffic mix is therefore collected at cohort level only; the cohorts are
# defined by traffic_scopes() in scripts/weekly_analytics.py.

# Analytics returns opaque enum codes; these are the labels YouTube Studio uses.
# Unmapped codes fall through as-is rather than being dropped or renamed.
TRAFFIC_LABELS = {
    "SHORTS": "Shorts feed",
    "YT_SEARCH": "Search",
    "YT_CHANNEL": "Channel pages",
    "YT_OTHER_PAGE": "Other YouTube pages",
    "RELATED_VIDEO": "Suggested videos",
    "SUBSCRIBER": "Browse/subscriptions",
    "EXT_URL": "External",
    "NOTIFICATION": "Notifications",
    "PLAYLIST": "Playlists",
    "HASHTAGS": "Hashtag pages",
    "SOUND_PAGE": "Sound page",
    "ADVERTISING": "Advertising",
    "NO_LINK_OTHER": "Direct/unknown",
    "NO_LINK_EMBEDDED": "Embedded",
}

# Sources that represent someone actively looking for content, as opposed to
# being served it by the feed. This is the number R4.7 exists to produce: it
# decides whether SEO work (tags, search-oriented titles, SRT) is worth revisiting.
DISCOVERY_SOURCES = ("YT_SEARCH", "HASHTAGS", "EXT_URL")


@dataclass
class TrafficRow:
    source: str
    views: float
    minutes: float
    share_pct: float = 0.0

    @property
    def label(self):
        return TRAFFIC_LABELS.get(self.source, self.source)


def aggregate_traffic(rows):
    """Sum (source, views, minutes) triples by source and attach view shares.

    Chunked queries (the video filter caps out well before this channel's
    upload count) each return their own breakdown, so the chunks must be summed
    before shares mean anything. Sorted by views desc; ties broken by source
    name so the committed CSV has a stable row order across runs.
    """
    totals = {}
    for source, views, minutes in rows:
        v, m = totals.get(source, (0.0, 0.0))
        totals[source] = (v + float(views), m + float(minutes))
    grand = sum(v for v, _ in totals.values())
    out = [TrafficRow(source=s, views=v, minutes=m,
                      share_pct=(100.0 * v / grand) if grand else 0.0)
           for s, (v, m) in totals.items()]
    out.sort(key=lambda r: (-r.views, r.source))
    return out


def discovery_share(rows):
    """Percent of views from search/hashtag/external — the SEO-surface read."""
    return sum(r.share_pct for r in rows if r.source in DISCOVERY_SOURCES)


def format_traffic_mix(rows, top_n=3, min_share=1.0):
    """One-line readout: 'Shorts feed 94.2% · Search 3.4% · other 2.4%'.

    Everything past top_n, and anything below min_share, collapses into 'other'
    so a long tail of sub-1% sources can't crowd out the line.
    """
    if not rows:
        return "no data"
    named = [r for r in rows[:top_n] if r.share_pct >= min_share]
    parts = [f"{r.label} {r.share_pct:.1f}%" for r in named]
    rest = 100.0 - sum(r.share_pct for r in named)
    if rest >= 0.05:
        parts.append(f"other {rest:.1f}%")
    return " · ".join(parts)
