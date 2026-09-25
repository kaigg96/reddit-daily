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
# Below this relative change, two cohorts are "the same".
MATERIAL = 0.05
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
    # Set only by load_videos_at_age, where `published` is deliberately
    # synthetic so that every age rule applies unchanged. See that docstring.
    true_published: datetime.datetime = None

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
        if abs(self.delta) < MATERIAL:
            return "no material difference"
        return f"{'better' if self.delta > 0 else 'worse'} by {abs(self.delta):.0%}"

    @property
    def delta(self):
        """Relative change of a against b — None when nothing can be concluded."""
        if not (self.a.sufficient and self.b.sufficient) or not self.age_matched:
            return None
        if not self.b.median:
            return None
        return (self.a.median - self.b.median) / self.b.median

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


def split_cohorts(videos, key, value):
    """Two-way split on an upload_log field, for an age-matched comparison.

    Returns (matching, other, unset_count). Videos where the field is unset are
    in NEITHER cohort. Every field was added to the log at some point, so a
    naive `!= value` split silently files the whole pre-field history under
    "not that value" — for `candidate_rank=1` that meant 24 ranked videos
    against 75 supposedly-unranked ones, of which only 3 carried a rank at all,
    and the comparison rendered a confident-looking median either way."""
    a, b, unset = [], [], 0
    for v in videos:
        got = str(v.meta.get(key, "")).strip()
        if not got:
            unset += 1
        elif got == value:
            a.append(v)
        else:
            b.append(v)
    return a, b, unset


def within(videos, spec):
    """Keep only videos whose upload_log field equals a value ("key=value").

    Lets one comparison be read inside another's halves, e.g. question length
    within similar-length videos, so a mechanical cause can be ruled out."""
    key, _, value = spec.partition("=")
    return [v for v in videos if str(v.meta.get(key, "")).strip() == value]


def split_by(videos, key):
    """Group videos by an upload_log field (format_version, topic, ...)."""
    out = {}
    for v in videos:
        out.setdefault(str(v.meta.get(key, "")).strip() or "(unset)", []).append(v)
    return out


def release_cohorts(videos, key, value):
    """Split for a revert decision: the release against **what preceded it**.

    `split_cohorts` answers "this value vs every other value", which is right
    for a dimension like topic and wrong for a release. Once a later version
    ships, "every other value" mixes the predecessor era with the successor
    era, and the question being answered stops being the revert question —
    *was this worse than the thing it replaced?* Uploads published after the
    release began are dropped rather than folded into its baseline.

    Returns (release, preceding, unset, later_count).
    """
    a, b, unset = split_cohorts(videos, key, value)
    if not a:
        return a, b, unset, 0
    started = min((v.true_published or v.published) for v in a)
    preceding = [v for v in b if (v.true_published or v.published) < started]
    return a, preceding, unset, len(b) - len(preceding)


def drift_floor(videos, metric, block=MIN_COHORT):
    """How much `metric` moves between consecutive groups of uploads anyway.

    Age-matching removes the age confound; it does not remove the *calendar*
    one. Measured on the real channel, median views at seven days old run 82 →
    228 → 114 → 62 by half-month while the format was unchanged for most of it
    — a 2.8x swing inside a single version. Any release-vs-predecessor test on
    views will attribute that swing to the release: the first two run against
    live data said "revert" for both `v5` and the b-roll library on drops of
    50% and 39%, which is ordinary weather on this channel.

    So the release check carries its own detection limit. Blocks are
    `MIN_COHORT` uploads in publish order — the smallest group this module will
    report a median for at all — and the floor is the median absolute change
    between adjacent blocks. Returns None when there is not enough history.

    Known limit, worth stating rather than hiding: the era used as the
    reference contains the releases that preceded this one, so it measures
    "how much this moves between consecutive batches in normal operation",
    not pure noise. That makes the floor generous and the check conservative —
    it will miss a small real regression before it invents one.
    """
    live = sorted([v for v in videos if v.views > 0],
                  key=lambda v: v.true_published or v.published)
    blocks = [live[i:i + block] for i in range(0, len(live) - block + 1, block)]
    deltas = []
    for x, y in zip(blocks, blocks[1:]):
        mx, my = median([v.get(metric) for v in x]), median([v.get(metric) for v in y])
        if mx:
            deltas.append(abs(my - mx) / mx)
    return median(deltas) if deltas else None


# What may fire a revert. The owner settled it on #18 (2026-09-22): "the rule
# now triggers on watch-seconds only, with views reported but never firing it".
# Views at a fixed age move 27-52% between batches with nothing changed, five
# times watch-seconds' 6-15%, so a views trigger fires on noise. Views are
# still compared and printed, with their own detection limit.
REVERT_TRIGGER = (Metric.WATCH,)


def release_verdict(comparisons, floors=None):
    """Fold `/shift` §5: a release that degraded **watch-seconds** is reverted,
    unless the drop is no bigger than the channel's own drift. Other metrics
    are reported beside it and never fire (REVERT_TRIGGER).

    Everything short of a clean, separable answer is an explicit "no verdict",
    never silence. The guardrail spent four releases returning nothing at all
    and reading, to anyone glancing at it, like approval.
    """
    if not comparisons:
        return "NO VERDICT — nothing to compare"
    if not any(c.metric in REVERT_TRIGGER for c in comparisons):
        return f"NO VERDICT — {' / '.join(REVERT_TRIGGER)} was not compared"
    for c in comparisons:
        if not (c.a.sufficient and c.b.sufficient):
            return (f"NO VERDICT — under {MIN_COHORT} measurable uploads on one side; "
                    f"bake longer")
        if not c.age_matched:
            return "NO VERDICT — cohorts are not age-matched"
    floors = floors or {}
    worse = []
    for c in comparisons:
        floor = floors.get(c.metric)
        if (c.metric in REVERT_TRIGGER
                and c.delta is not None and c.delta < 0 and abs(c.delta) >= MATERIAL
                and (floor is None or abs(c.delta) > floor)):
            worse.append(c.metric)
    if worse:
        return f"REVERT — {' and '.join(worse)} degraded beyond the channel's own drift"
    return (f"KEEP — {' / '.join(REVERT_TRIGGER)} did not degrade beyond the "
            f"channel's own drift")


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def early_read_stability(early_days=3, late_days=7, metric=Metric.WATCH):
    """(n, Spearman rho) between each upload's early and late reading.

    Research row R3: if the early reading ranks uploads as the late one does,
    a release can be judged sooner. Within tolerance one weekly snapshot can
    match both ages, which would correlate a reading with itself; a pair is
    kept only when its two readings came from different snapshots."""
    early, late = load_videos_at_age(early_days), load_videos_at_age(late_days)
    if not early.videos or not late.videos:
        return 0, None
    e = {v.video_id: v for v in early.videos}
    pairs = []
    for v in late.videos:
        u = e.get(v.video_id)
        if u is None:
            continue
        age_u = (early.anchor - u.published).total_seconds() / 86400
        age_v = (late.anchor - v.published).total_seconds() / 86400
        if abs(age_v - age_u) < 1:
            continue    # same snapshot
        pairs.append((getattr(u, metric), getattr(v, metric)))
    if len(pairs) < 3:
        return len(pairs), None
    rx, ry = _ranks([p[0] for p in pairs]), _ranks([p[1] for p in pairs])
    mx, my = statistics.mean(rx), statistics.mean(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    sy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return len(pairs), (cov / (sx * sy) if sx and sy else None)


def median_duration(videos):
    """Median logged video length, or None when no video records one.

    Watch-seconds rises with length (+22% for videos over ~20s, 2026-09-25),
    so a release that shifts length can pass or fail its trigger metric
    mechanically. The b-roll switch moved it 19.3s -> 20.4s."""
    d = [float(v.meta["duration_s"]) for v in videos
         if str(v.meta.get("duration_s", "")).strip()]
    return statistics.median(d) if d else None


def render_duration(release, before, threshold=1.0):
    """One line beside the release verdict: each cohort's median length."""
    a, b = median_duration(release), median_duration(before)
    if a is None or b is None:
        return "duration: not measurable in both cohorts"
    line = f"duration: {a:.1f}s vs {b:.1f}s before"
    if abs(a - b) >= threshold:
        line += " -- SHIFTED: watch-seconds rises with length, so part of this verdict is length"
    return line


def render_release(comparisons, floors):
    """The release answer in full: both metrics, each with the size of change
    that would have to be exceeded to mean anything, then the verdict."""
    out = []
    for c in comparisons:
        out.append(c.render())
        floor = floors.get(c.metric)
        if floor is None:
            out.append(f"    detection limit: not measurable — under {2 * MIN_COHORT} "
                       f"measured uploads before this change")
        else:
            out.append(f"    detection limit: {floor:.0%} — median move in {c.metric} "
                       f"between consecutive groups of {MIN_COHORT} uploads in the era "
                       f"before it. Smaller than that is ordinary channel drift.")
    # Only REVERT_TRIGGER fires (#18), so a metric that moved beyond its own
    # limit without firing has to be said out loud, or the one-line verdict
    # reads as if every metric agreed with it.
    moved = {c.metric: c.delta for c in comparisons
             if c.delta is not None and floors.get(c.metric) is not None
             and abs(c.delta) > floors[c.metric]}
    quiet = {m: d for m, d in moved.items() if m not in REVERT_TRIGGER and d < 0}
    if quiet:
        also = ", ".join(f"{m} {d:+.0%}" for m, d in quiet.items())
        out.append(f"    NOT A TRIGGER: {also}, beyond its detection limit. Reported only; "
                   f"a revert fires on {' / '.join(REVERT_TRIGGER)} alone (owner, #18).")
    if any(d > 0 for d in moved.values()) and any(d < 0 for d in moved.values()):
        better = ", ".join(f"{m} {d:+.0%}" for m, d in moved.items() if d > 0)
        worse = ", ".join(f"{m} {d:+.0%}" for m, d in moved.items() if d < 0)
        out.append(f"    CONFLICT: {better} but {worse}. The verdict follows "
                   f"{' / '.join(REVERT_TRIGGER)}.")
    out.append("")
    out.append(f"{release_verdict(comparisons, floors)}   (/shift §5 auto-revert rule)")
    return "\n".join(out)


# ---------------------------------------------------------------- trajectory

TRAJECTORY_AT_AGE = 7      # days old at which every upload is read
TRAJECTORY_MIN_N = 5       # periods thinner than this are not reported
TRAJECTORY_HALF = 3        # periods per half when comparing then-vs-now


def trajectory(snapshot_rows, at_age=TRAJECTORY_AT_AGE, tolerance=4):
    """Median metric per publish-week, every upload read at the same age.

    Answers the one question no other surface here answers: **is the channel
    getting better?** `--by` groups, `--compare` tests two cohorts and
    `--release` judges one release — all of them point-in-time. A system can
    pass every one of those while the channel flatlines for months, which is
    the failure this exists to catch.

    Reading at a fixed age is what makes months comparable: the weekly snapshot
    holds ~10 readings per video, so a July upload can be read at seven days
    old alongside a September one. Returns [(period, n, median)] oldest first.
    """
    best = {}
    for row in snapshot_rows:
        pub, snap = row.get("published"), row.get("snapshot")
        value = row.get("value")
        if not pub or not snap or not value or value <= 0:
            continue
        age = (snap - pub).days
        if abs(age - at_age) > tolerance:
            continue
        key = row.get("video_id")
        prev = best.get(key)
        if prev is None or abs(age - at_age) < abs(prev[0] - at_age):
            best[key] = (age, value, pub)

    buckets = {}
    for _, value, pub in best.values():
        buckets.setdefault(pub.strftime("%Y-W%V"), []).append(value)
    return [(period, len(v), median(v))
            for period, v in sorted(buckets.items())
            if len(v) >= TRAJECTORY_MIN_N]


def trajectory_verdict(series, floor=None, half=TRAJECTORY_HALF):
    """Rising, flat or falling — against the channel's own noise, not zero.

    A flat verdict is the actionable one and the whole point: it means the work
    being done is not moving the outcome, which no amount of process metrics
    would reveal. `floor` is the ordinary between-batch swing (see
    `drift_floor`); without it a 1s wobble reads as progress.
    """
    if len(series) < half * 2:
        return "unknown", f"only {len(series)} comparable periods"
    recent = median([m for _, _, m in series[-half:]])
    prior = median([m for _, _, m in series[-half * 2:-half]])
    change = recent - prior
    span = f"{prior:.1f} → {recent:.1f}"
    if floor is not None and abs(change) <= floor:
        return "flat", (f"{span} over {half * 2} periods — inside the "
                        f"channel's own {floor:.1f} drift")
    if abs(change) < 0.5:
        return "flat", f"{span} over {half * 2} periods"
    return ("rising" if change > 0 else "falling"), f"{span} over {half * 2} periods"


# ------------------------------------------------------------ scorecard
#
# One metric cannot judge this channel, and the project has the scar to prove
# it: avg-%-viewed was dropped as a target because trimming a video inflates it
# without adding a second of watch time (PRD §4, Review 2). Watch-seconds has
# the mirror flaw -- lengthen a video and it rises while the share watched
# falls. Either number alone will call that success.
#
# So metrics are typed, which is the standard treatment: one SUCCESS metric
# that must improve, GUARDRAILS that must not degrade beyond a stated margin,
# and DIAGNOSTICS that explain a disagreement without voting. The decision is
# deliberately conservative -- a guardrail breach is not outweighed by the
# success metric rising, because that combination is usually an artefact.
#
# Adding guardrails is not free: each one costs statistical power, and with
# cohorts of 5-14 uploads a week there is little to spend. Hence a short fixed
# list that decides, and a wider panel that only informs.

SUCCESS_METRIC = "watch_seconds"
# A fixed margin is only honest for a metric whose ordinary swing we know.
# Views is not one: measured on this channel it runs 82 -> 228 -> 114 -> 62 by
# half-month with the format unchanged, a 2.8x swing. A hardcoded margin on it
# fires on weather -- the first real scorecard run breached on a 2x drop that
# is well inside that. So views carries no fixed margin and is reported as a
# diagnostic unless a measured floor is supplied by the caller.
GUARDRAILS = {
    # metric: how much worse it may get before it blocks, in its own units
    "avg_view_pct": 5.0,      # catches "we just made videos longer"
    "zero_rate": 3.0,         # suppression creeping up, in percentage points
}
DIAGNOSTICS = ("views", "duration_s", "likes_per_100", "comments_per_100")


def scorecard(then, now, guardrails=None):
    """Compare two periods across typed metrics and return one honest verdict.

    `then` and `now` are {metric: value}. Returns (verdict, rows, notes) where
    verdict is one of BETTER / MIXED / WORSE / FLAT and rows carry every metric
    with its own read, so a disagreement is visible rather than averaged away.
    """
    # A caller with a measured drift floor for a metric can promote it to a
    # guardrail; without one it stays diagnostic rather than blocking on noise.
    margins = dict(GUARDRAILS) if guardrails is None else dict(guardrails)
    diagnostics = [m for m in DIAGNOSTICS if m not in margins]
    rows, notes = [], []
    breached, improved = [], False

    for metric in [SUCCESS_METRIC] + list(margins) + diagnostics:
        a, b = then.get(metric), now.get(metric)
        if a is None or b is None:
            continue
        change = b - a
        kind = ("success" if metric == SUCCESS_METRIC
                else "guardrail" if metric in margins else "diagnostic")
        read = ""
        if kind == "success":
            improved = change > 0
            read = "up" if change > 0 else ("down" if change < 0 else "level")
        elif kind == "guardrail":
            if -change > margins[metric]:
                read = "BREACHED"
                breached.append(metric)
            else:
                read = "ok"
        rows.append({"metric": metric, "kind": kind, "then": a, "now": b,
                     "change": change, "read": read})

    if breached and improved:
        verdict = "MIXED"
        notes.append("the success metric rose while " + ", ".join(breached)
                     + " degraded — usually an artefact, not an improvement")
    elif breached:
        verdict = "WORSE"
        notes.append("guardrail breach: " + ", ".join(breached))
    elif improved:
        verdict = "BETTER"
    else:
        verdict = "FLAT"

    # A diagnostic does not vote, but a large move must not be silent either:
    # the first real run read BETTER while views and engagement had both
    # roughly halved. Not blocking on that is right; hiding it is not.
    moved = []
    for r in rows:
        if r["kind"] != "diagnostic" or not r["then"]:
            continue
        if abs(r["change"]) / abs(r["then"]) >= 0.30:
            moved.append(f"{r['metric']} {r['then']:.1f}→{r['now']:.1f}")
    if moved:
        notes.append("large diagnostic moves (not blocking, but watch if they "
                     "repeat): " + "; ".join(moved))

    # The honest caveat, every time: this is a small channel.
    notes.append("each guardrail costs power; on cohorts this size read a "
                 "single period's move as weather unless it repeats")
    return verdict, rows, notes


# A Short replays in the feed until swiped and YouTube counts every loop, so an
# average view above 100% of the video's length can only come from replays.
# Thin videos are left out: at a handful of views one rewatcher decides it.
REPLAY_MIN_VIEWS = 20


def replay_share(videos, min_views=REPLAY_MIN_VIEWS):
    """(replaying, eligible): of the videos with at least `min_views`, how many
    average over 100% viewed. Backlog #9's first test — almost none, drop it."""
    eligible = [x for x in videos if x.views >= min_views]
    return sum(1 for x in eligible if x.avg_view_pct > 100), len(eligible)


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


def _with_derived_dimensions(row):
    """Group-able dimensions computed from an upload_log row.

    Shared by both loaders on purpose: raw bg_clip is per-file
    ("pexels_123.mp4", "procedural:8471"), too granular to group on, and two
    loaders deriving it separately is a rule that drifts.
    """
    r = dict(row)
    bg = (r.get("bg_clip") or "").strip()
    r["background_type"] = ("(unknown)" if not bg else
                            "procedural" if bg.startswith("procedural") else "broll")
    # The two daily runs have drifted (01-05 and 12-19 UTC), so split on noon
    # rather than on a cron hour.
    ts = (r.get("timestamp_utc") or "").strip()
    r["slot"] = "" if not ts else "morning" if _parse_ts(ts).hour < 12 else "evening"
    # 63 characters is the logged median (2026-09-25), so the halves are even.
    q = (r.get("post_title") or "").strip()
    r["question_length"] = "" if not q else "short" if len(q) <= 63 else "long"
    # ~20 s: the logged median duration is 20.2 s (2026-09-25).
    d = (r.get("duration_s") or "").strip()
    r["video_length"] = "" if not d else "short" if float(d) <= 20.0 else "long"
    return r


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

    # A video with exactly 0 views has NO row in the Analytics response, so
    # `stats` is missing precisely the uploads that matter most: on 2026-09-19
    # the three dropped uploads old enough to have data were the 2026-09-14
    # zero and BOTH surviving confirmed-suppression cases (VDH3pSafyE0,
    # _0MNAf8AzNg) — the entire evidence base for R4.6's skip categories,
    # invisible to the tool that answers "did X work?". Dropping them also bias
    # every median upward, since they are the worst performers by definition.
    #
    # So a missing row is treated as a genuine zero, except where the video is
    # non-public (owner-privatised), which is a different thing entirely and is
    # excluded — the same distinction `classify_zero_views` already encodes.
    missing_ids = [r["video_id"] for r in rows if r["video_id"] not in stats]
    privacy = {}
    if missing_ids:
        yt = analytics.youtube_client()
        for d in analytics.fetch_video_details(yt, missing_ids, part="status"):
            privacy[d["id"]] = d.get("status", {}).get("privacyStatus", "unknown")

    videos = []
    excluded_non_public = []
    for r in rows:
        s = stats.get(r["video_id"])
        if not s:
            vid = r["video_id"]
            if privacy.get(vid, "unknown") != "public":
                # Privatised or deleted: not a performance data point either way.
                excluded_non_public.append(vid)
                continue
            s = {"views": 0, "averageViewDuration": 0, "averageViewPercentage": 0,
                 "likes": 0, "comments": 0}
        published = _parse_ts(r["timestamp_utc"])
        r = _with_derived_dimensions(r)
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
    if excluded_non_public:
        print(f"note: {len(excluded_non_public)} logged upload(s) excluded as "
              f"non-public (owner-privatised), not counted as zero-view")
    return videos


# ------------------------------------------------- offline I/O (weekly snapshot)


@dataclass
class OfflineLoad:
    """What the snapshot could and could not measure — returned together so a
    caller cannot report the numbers without the caveats."""
    videos: list
    asof: datetime.datetime = None
    too_new: list = field(default_factory=list)   # published after the snapshot
    absent: list = field(default_factory=list)    # older, yet missing from it

    def caveats(self):
        if self.asof is None:
            return ["no analytics snapshot on disk — nothing to report"]
        out = [f"weekly snapshot as of {self.asof.date()}; every age and median "
               f"below is measured at that date, not today"]
        if self.too_new:
            out.append(f"{len(self.too_new)} logged upload(s) postdate the snapshot "
                       f"and are excluded as unmeasured — NOT counted as zero-view")
        if self.absent:
            out.append(f"WARNING: {len(self.absent)} upload(s) older than the snapshot "
                       f"are missing from it (deleted from the channel?): "
                       f"{', '.join(self.absent[:5])}")
        out.append("privacy is not recorded in the snapshot, so an owner-privatised "
                   "upload reads here as zero-view; medians are unaffected (zeros are "
                   "excluded from them) but the zero count may overstate suppression")
        return out


def load_videos_offline(min_age_days=MIN_AGE_DAYS):
    """Join upload_log.csv against the newest weekly analytics snapshot — the
    read-only path, for callers with no YouTube credentials (every scheduled
    shift: `shift.yml` withholds them deliberately, and correctly, so a shift
    cannot upload). Live `load_videos` remains the authority.

    Three rules the live path gets from the API and this one has to encode:

    1. **Measure ages at the snapshot, not at wall-clock time.** The metrics
       were frozen when the snapshot ran, so a video published the day before
       it had one day to earn them however old it is now. Hence no `now`
       parameter: `asof` is returned instead, and callers must pass it on to
       every age-matched comparison.
    2. **A logged upload absent from the snapshot is unmeasured, never a
       zero.** These are the ~2/day published since it ran. Scoring them zero
       invents suppression events wholesale — the exact false positive the
       digest's zero-view alert was fixed for on 2026-08-23 (12 alerts → 1).
    3. **A row that IS present with 0 views is a genuine zero.** The snapshot
       writes one row per channel video and defaults a missing Analytics row to
       0, so `load_videos`' hard-won "missing row means zero" is already baked
       into the file.

    The one thing it cannot do: the snapshot records no privacy status, so
    owner-privatised uploads — which `load_videos` excludes — read as
    zero-view. Bounded, not silent: see `OfflineLoad.caveats()`.
    """
    if not (config.ANALYTICS_SNAPSHOTS.exists() and config.UPLOAD_LOG.exists()):
        return OfflineLoad([])
    with open(config.ANALYTICS_SNAPSHOTS, newline="") as f:
        snapshot_rows = [r for r in csv.DictReader(f) if r.get("snapshot_date")]
    if not snapshot_rows:
        return OfflineLoad([])

    latest = max(r["snapshot_date"] for r in snapshot_rows)
    # Midnight of the snapshot date: the run happens during that day, so this
    # understates ages by under a day — conservative in the direction that
    # drops a borderline-young video rather than admitting one.
    asof = datetime.datetime.fromisoformat(latest).replace(tzinfo=datetime.timezone.utc)
    stats = {r["video_id"]: r for r in snapshot_rows if r["snapshot_date"] == latest}

    with open(config.UPLOAD_LOG) as f:
        rows = [r for r in csv.DictReader(f) if r.get("video_id")]

    videos, too_new, absent = [], [], []
    for r in rows:
        published = _parse_ts(r["timestamp_utc"])
        s = stats.get(r["video_id"])
        if s is None:
            (too_new if published > asof else absent).append(r["video_id"])
            continue
        r = _with_derived_dimensions(r)
        v = Video(
            video_id=r["video_id"], published=published,
            views=float(s.get("views") or 0),
            watch_seconds=float(s.get("avg_view_duration_s") or 0),
            avg_view_pct=float(s.get("avg_view_pct") or 0),
            likes=float(s.get("likes") or 0), comments=float(s.get("comments") or 0),
            meta=r,
        )
        if v.age_days(asof) >= min_age_days:
            videos.append(v)
    return OfflineLoad(videos, asof, too_new, absent)


# --------------------------------------------- age-matched reads (snapshot series)

# The first weekly snapshot after publication. Shorts distribution is largely
# decided in the first days, and this is the age with the most coverage.
AGE_MATCH_TARGET_DAYS = 7
# Half the weekly cadence, so no video has two candidate snapshots and none is
# counted twice.
AGE_MATCH_TOLERANCE_DAYS = 3.5


@dataclass
class AgeMatchedLoad:
    """Uploads as they looked at a common age, with what that could not cover."""
    videos: list
    anchor: datetime.datetime = None
    target_age: float = AGE_MATCH_TARGET_DAYS
    not_yet: list = field(default_factory=list)      # too young to have reached it
    no_coverage: list = field(default_factory=list)  # old, but no snapshot at that age

    def caveats(self):
        if not self.videos:
            return ["no weekly snapshot covers any upload at that age — nothing to report"]
        out = [f"every median below is measured at ~{self.target_age:.0f} days old, not "
               f"today; that is what makes releases from different months comparable"]
        if self.not_yet:
            out.append(f"{len(self.not_yet)} upload(s) have not reached "
                       f"{self.target_age:.0f} days yet — excluded as unmeasured, NOT "
                       f"counted as zero-view")
        if self.no_coverage:
            out.append(f"{len(self.no_coverage)} older upload(s) have no snapshot at that "
                       f"age (they predate the weekly series) — excluded")
        out.append("privacy is not recorded in the snapshots, so an owner-privatised "
                   "upload reads as zero-view; medians are unaffected (zeros are excluded "
                   "from them) but the zero count may overstate suppression")
        return out


def load_videos_at_age(target_age_days=AGE_MATCH_TARGET_DAYS,
                       tolerance_days=AGE_MATCH_TOLERANCE_DAYS):
    """Every logged upload as it looked at ~`target_age_days` old.

    Rule 2 says cohorts must be age-matched, and a release can never satisfy it
    against a snapshot of today: it applies to every upload after it and none
    before, so its two cohorts differ in age *by construction* and `compare`
    correctly refuses them. That is why `/shift` §5's auto-revert guardrail has
    never once produced a verdict — see issue #16.

    The weekly snapshot series is the way out. Each one records every channel
    video's metrics on that date, so a July upload has a row from when it was a
    week old and so does a September one. Reading both at the same age makes
    the eras genuinely comparable, on **watch-seconds as well as views** —
    which is the whole of what the rule claims, not the half an age-trend
    regression on views could have covered.

    `published` on the returned videos is **synthetic**: set so each video's age
    at `anchor` equals the age it was measured at, which is what lets every
    existing rule (`ages_comparable`, `summarize`, `compare`) apply unchanged.
    The real publish time is on `true_published`; nothing should read
    `published` as a date.

    Uploads with no snapshot inside the window are excluded and counted, never
    scored zero — the same rule `load_videos_offline` had to learn.
    """
    if not (config.ANALYTICS_SNAPSHOTS.exists() and config.UPLOAD_LOG.exists()):
        return AgeMatchedLoad([])
    by_video = {}
    with open(config.ANALYTICS_SNAPSHOTS, newline="") as f:
        for r in csv.DictReader(f):
            if r.get("snapshot_date") and r.get("video_id"):
                by_video.setdefault(r["video_id"], []).append(r)
    if not by_video:
        return AgeMatchedLoad([])

    latest = max(r["snapshot_date"] for rows in by_video.values() for r in rows)
    anchor = datetime.datetime.fromisoformat(latest).replace(tzinfo=datetime.timezone.utc)

    with open(config.UPLOAD_LOG) as f:
        rows = [r for r in csv.DictReader(f) if r.get("video_id")]

    videos, not_yet, no_coverage = [], [], []
    for row in rows:
        published = _parse_ts(row["timestamp_utc"])
        best = None
        for s in by_video.get(row["video_id"], []):
            when = datetime.datetime.fromisoformat(s["snapshot_date"]).replace(
                tzinfo=datetime.timezone.utc)
            age = (when - published).total_seconds() / 86400
            if abs(age - target_age_days) > tolerance_days:
                continue
            if best is None or abs(age - target_age_days) < abs(best[0] - target_age_days):
                best = (age, s)
        if best is None:
            reached = (anchor - published).total_seconds() / 86400
            (not_yet if reached < target_age_days - tolerance_days
             else no_coverage).append(row["video_id"])
            continue
        age, s = best
        meta = _with_derived_dimensions(row)
        videos.append(Video(
            video_id=row["video_id"],
            published=anchor - datetime.timedelta(days=age),
            true_published=published,
            views=float(s.get("views") or 0),
            watch_seconds=float(s.get("avg_view_duration_s") or 0),
            avg_view_pct=float(s.get("avg_view_pct") or 0),
            likes=float(s.get("likes") or 0),
            comments=float(s.get("comments") or 0),
            meta=meta,
        ))
    return AgeMatchedLoad(videos, anchor, target_age_days, not_yet, no_coverage)


# ---------------------------------------------------------------- zero-view analysis

ZERO_NEIGHBOURS = 4          # uploads either side used to judge "was the channel alive?"
COLD_SPELL_MEDIAN = 5        # neighbour median at/below this = channel-wide dead patch
ZERO_MIN_AGE_DAYS = 3        # below this, 0 views means "new", not "suppressed"


def classify_zero_views(channel_videos, now=None):
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

    3. **A video too young to have views is not suppressed.** Its neighbours are
       all older, so a fresh upload always looks isolated — the same
       false-positive the digest's zero-view alert was fixed for on 2026-08-23,
       which was never carried across to here. Anything under
       ZERO_MIN_AGE_DAYS is bucketed as `too_new` instead.

    `channel_videos` = [{id, published, views, privacy, title}] sorted or not.
    Returns {"non_public": [...], "cold_spell": [...], "isolated": [...],
    "too_new": [...]} — only `isolated` are genuine suppression candidates.
    """
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cutoff = (now - datetime.timedelta(days=ZERO_MIN_AGE_DAYS)).isoformat()
    vids = sorted(channel_videos, key=lambda v: v["published"])
    public = [v for v in vids if v.get("privacy") == "public"]
    by_id = {v["id"]: i for i, v in enumerate(public)}

    out = {"non_public": [], "cold_spell": [], "isolated": [], "too_new": []}
    for v in vids:
        if int(v["views"]) != 0:
            continue
        if v.get("privacy") != "public":
            out["non_public"].append(v)
            continue
        if v["published"] >= cutoff:
            out["too_new"].append(v)
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
