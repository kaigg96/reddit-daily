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
