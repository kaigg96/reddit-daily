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
import functools
import json
import math
import re
import statistics
from dataclasses import dataclass, field

from . import config

# A comparison needs at least this many videos per side to report a number.
MIN_COHORT = 8
# Below this relative change, two cohorts are "the same".
MATERIAL = 0.05
# At or below this many views an upload was barely shown at all — the
# retired-clip signal (PRD §0 #11), which a median of the rest cannot see.
BURIED_VIEWS = 5
CLIP_EARLY_USES = 4   # R4: retired clip #11 was buried only after its 4th use
# Two cohorts whose share of one release differs by more than this compare
# eras as much as the field (`era_imbalance`).
ERA_MIX_TOLERANCE = 0.15
# Analytics lags, and by more than the ~1-2 days once assumed: in the weekly
# snapshots (2026-09-27), `report.py --at-age 3` read 35% of uploads as
# zero-view, `--at-age 4` 20%, and 5 through 7 a steady 4-6%. Below this, a
# zero mostly means "not reported yet", and medians skip those videos.
MIN_AGE_DAYS = 5


class Metric:
    WATCH = "watch_seconds"      # primary — cannot be gamed by trimming
    VIEWS = "views"
    PCT = "avg_view_pct"         # diagnostic only; valid at fixed duration
    LIKES = "likes"
    COMMENTS = "comments"
    TOTAL = "total_watch_s"      # views x watch-seconds: does length trade one for the other?
    ENGAGED = "implied_engaged"  # NOT the engaged share: refuted 2026-10-05 (engaged_check)
    ENGAGED_SHARE = "engaged_share"  # engagedViews / views: the share the Partner Program counts
    ENGAGED_VIEWS = "engaged_views"  # the count the Partner Program's 10M bar is in (PLAN §1)
    WATCH_FINE = "watch_seconds_fine"  # diagnostic: watch-seconds to a fraction; rules stay on WATCH
    # Share of views still watching at 10..100% of the video (weekly snapshot
    # from 2026-10-19, uploads under 30 days old; above 1 means replays).
    # Diagnostics for where viewers leave (PRD §0, "Retention points"), never a trigger.
    RETENTION = ("watch_ratio_10", "watch_ratio_25", "watch_ratio_50",
                 "watch_ratio_75", "watch_ratio_100")


@dataclass
class Video:
    video_id: str
    published: datetime.datetime
    views: float = 0.0
    watch_seconds: float = 0.0
    avg_view_pct: float = 0.0
    likes: float = 0.0
    comments: float = 0.0
    est_minutes: float = 0.0
    engaged_views: float = None   # None where the snapshot predates the column (2026-10-05)
    subs_gained: float = None     # None where the snapshot predates the column (2026-10-12)
    # Metric.RETENTION: None where not collected (before 2026-10-19, past 30
    # days old, or a refused week), so cohorts skip them rather than read 0.
    watch_ratio_10: float = None
    watch_ratio_25: float = None
    watch_ratio_50: float = None
    watch_ratio_75: float = None
    watch_ratio_100: float = None
    meta: dict = field(default_factory=dict)   # upload_log row (format_version, topic, ...)
    # Set only by load_videos_at_age, where `published` is deliberately
    # synthetic so that every age rule applies unchanged. See that docstring.
    true_published: datetime.datetime = None

    @property
    def total_watch_s(self):
        return self.views * self.watch_seconds

    @property
    def implied_engaged(self):
        """est_minutes x 60 / (views x watch-seconds): ~0.18 before v2 and ~0.4
        after. Hypothesis (R2): watch-seconds is per engaged view, so this is
        engagedViews / views. Refuted 2026-10-05: `engaged_check` reads it 26% high."""
        denom = self.views * self.watch_seconds
        return self.est_minutes * 60 / denom if denom else 0.0

    @property
    def engaged_share(self):
        """engagedViews / views, the share of play starts the Partner Program
        counts (PLAN §1). None when unreported, so cohorts skip it, not zero it."""
        if self.engaged_views is None:
            return None
        return self.engaged_views / self.views if self.views else 0.0

    @property
    def watch_seconds_fine(self):
        """Percentage viewed x the upload's length: watch-seconds to a fraction.
        YouTube reports whole seconds, so medians move in half-second steps and
        a 4% change hides under the channel's ~1s drift. On 2026-10-12 it fell
        within a second of the whole figure on all 162 logged uploads, and the
        lengths YouTube implies sit ~0.3s from ours. None without a length."""
        duration = _optional_float(self.meta.get("duration_s"))
        if not duration:
            return None
        return self.avg_view_pct / 100 * duration

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
    buried_count: int = 0   # views <= BURIED_VIEWS, zero-view included

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
        d = decimals(self.metric)
        lines = [f"{self.metric}: {self.a.label} vs {self.b.label} -> {self.verdict}"]
        for c in (self.a, self.b):
            flag = "" if c.sufficient else f"  (below MIN_COHORT={MIN_COHORT})"
            zeros = f", {c.zero_view_count} zero-view excluded" if c.zero_view_count else ""
            lines.append(f"    {c.label:24} n={c.n:<4} median={c.median:<8.{d}f} "
                         f"med_age={c.median_age:.0f}d{zeros}{flag}")
        if not self.age_matched:
            lines.append("    WARNING: cohort ages differ enough to confound this comparison.")
        return "\n".join(lines)


# ---------------------------------------------------------------- pure logic


def decimals(metric):
    """Places to print: a share lives between 0 and 1, where .1f hides 0.33 vs 0.38."""
    return 2 if metric == Metric.ENGAGED_SHARE or metric in Metric.RETENTION else 1


def median(values):
    return statistics.median(values) if values else float("nan")


def reported(videos, metric):
    """The videos a cohort counts on `metric`.

    A metric the snapshot never reported (engaged views before 2026-10-05)
    leaves the cohort, but only for a video with views: the API leaves
    engaged views blank on zero-view rows, and those are still zero-view.
    Every check beside a median reads this set too, or it judges uploads the
    median never saw: on 2026-10-14 a 7-day engaged-share read of `v7`
    uploads warned of a `v4` mix."""
    return [v for v in videos if not v.views or v.get(metric) is not None]


def summarize(videos, label, metric, now):
    """Cohort summary. Zero-view videos are counted, not averaged in (rule 4)."""
    videos = reported(videos, metric)
    live = [v for v in videos if v.views > 0]
    zeros = len(videos) - len(live)
    return Cohort(
        label=label,
        n=len(live),
        median=median([v.get(metric) for v in live]),
        zero_view_count=zeros,
        median_age=median([v.age_days(now) for v in live]) if live else float("nan"),
        buried_count=sum(1 for v in videos if v.views <= BURIED_VIEWS),
    )


def buried_rate_p(hit_a, n_a, hit_b, n_b):
    """Two-sided Fisher exact p that two cohorts are buried (<= BURIED_VIEWS)
    at the same rate. Medians exclude zero-view videos, so a cohort YouTube
    distributes less can tie on watch-seconds and differ only here (R3)."""
    k, n = hit_a + hit_b, n_a + n_b
    if not (n_a and n_b and 0 < k < n):
        return 1.0

    def pmf(x):
        return math.comb(n_a, x) * math.comb(n_b, k - x) / math.comb(n, k)

    observed = pmf(hit_a)
    tables = range(max(0, k - n_b), min(k, n_a) + 1)
    return min(1.0, sum(p for p in map(pmf, tables) if p <= observed * (1 + 1e-9)))


def is_buried(v):
    return v.views <= BURIED_VIEWS


def buried_strata(videos_a, videos_b, key="format_version", hit=is_buried):
    """(hit_a, n_a, hit_b, n_b) for each value of `key` both cohorts share.
    `hit` defaults to buried; `top_share_hits` gives the other tail."""
    def value(v):
        return str(v.meta.get(key, "")).strip()

    out = []
    for val in sorted({value(v) for v in videos_a} & {value(v) for v in videos_b}):
        a = [v for v in videos_a if value(v) == val]
        b = [v for v in videos_b if value(v) == val]
        out.append((sum(map(hit, a)), len(a), sum(map(hit, b)), len(b)))
    return out


def top_share_hits(videos, top=0.10, key="format_version"):
    """A predicate for `buried_strata`: is this upload in the top `top` share
    of views **within its own release**? Ranked channel-wide, July's v4 (median
    160 views at 7 days, twice later releases) would hold most of the hits, and
    any field that merely leans toward v4 would pass for a hit-maker. Ties at
    the cut count as hits."""
    by_era = {}
    for v in videos:
        by_era.setdefault(str(v.meta.get(key, "")).strip(), []).append(v.views)
    cut = {}
    for era, views in by_era.items():
        views = sorted(views, reverse=True)
        cut[era] = views[max(0, math.ceil(len(views) * top) - 1)]
    return lambda v: v.views >= cut[str(v.meta.get(key, "")).strip()]


def buried_rate_p_pooled(strata):
    """Mantel-Haenszel p (continuity-corrected) that two cohorts are buried at
    the same rate, pooling strata such as formats without comparing across
    them. Per-format reads are thin (~10 per voice per format), so R3 needs
    the pooled one to reach a verdict."""
    diff = var = 0.0
    for hit_a, n_a, hit_b, n_b in strata:
        n, k = n_a + n_b, hit_a + hit_b
        if n < 2 or k in (0, n):
            continue
        diff += hit_a - n_a * k / n
        var += n_a * n_b * k * (n - k) / (n * n * (n - 1))
    if not var:
        return 1.0
    stat = max(0.0, abs(diff) - 0.5) ** 2 / var
    return math.erfc(math.sqrt(stat / 2))


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
    videos_a, videos_b = reported(videos_a, metric), reported(videos_b, metric)
    for v in videos_a + videos_b:
        v.age_days_cached = v.age_days(now)
    return Comparison(
        metric=metric,
        a=summarize(videos_a, label_a, metric, now),
        b=summarize(videos_b, label_b, metric, now),
        # Ages are matched over the uploads in the medians, as `summarize` reports them.
        age_matched=ages_comparable([v for v in videos_a if v.views > 0],
                                    [v for v in videos_b if v.views > 0]),
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


def era_imbalance(videos_a, videos_b, key="format_version", tolerance=ERA_MIX_TOLERANCE):
    """Eras whose share differs between two cohorts by more than `tolerance`.

    Views moved several-fold between releases, so a field that is not spread
    evenly across them compares eras, not the field. On 2026-09-28 voice read
    +50% on views pooled, but Stephen had read 37 of 57 `v4` uploads, the
    high-view era; within `v4` his lead was 6%. Returns [(era, share_a,
    share_b)], largest gap first; empty when the mix is even."""
    def shares(vs):
        out = {}
        for v in vs:
            era = str(v.meta.get(key, "")).strip() or "(unset)"
            out[era] = out.get(era, 0) + 1
        return {k: n / len(vs) for k, n in out.items()} if vs else {}
    sa, sb = shares(videos_a), shares(videos_b)
    gaps = [(era, sa.get(era, 0.0), sb.get(era, 0.0)) for era in set(sa) | set(sb)]
    gaps = [g for g in gaps if abs(g[1] - g[2]) > tolerance]
    return sorted(gaps, key=lambda g: -abs(g[1] - g[2]))


def _parse_spec(spec):
    key, _, value = spec.partition("=")
    negate = key.endswith("!")
    return key.rstrip("!").strip(), value.strip(), negate


def matches(meta, spec):
    """Does an upload_log row match "key=value", or "key!=value"? A row with
    the field unset matches neither: it predates the field, so counting it as
    "not X" would mix history in (the trap `split_cohorts` names)."""
    key, value, negate = _parse_spec(spec)
    got = str(meta.get(key, "")).strip()
    return bool(got) and (got == value) != negate


# A derived field's possible values, so a filter can name one no upload has
# yet: `title_writer!=groq` is meant to be in the title tests' reads before
# Groq writes any title (#10, #14), and must not be refused as a typo.
_DERIVED_VALUES = {"title_writer": {"reddit", "gemini", "groq"}}


def _require_value(metas, spec):
    """Refuse a filter whose value no upload has. "!=" with a typo would
    otherwise keep every upload and print as if it had filtered."""
    key, value, _ = _parse_spec(spec)
    if value in _DERIVED_VALUES.get(key, ()):
        return
    if not any(str(m.get(key, "")).strip() == value for m in metas):
        raise ValueError(f"no logged upload has {key}={value}: check the spelling")


def within(videos, spec):
    """Keep only videos whose upload_log field equals a value ("key=value"),
    or all but one value ("key!=value"). An empty result is an answer here
    (a release may hold no short videos), so a typo is caught where the user
    types it: `ids_within`, which report.py runs on every --within first.

    Lets one comparison be read inside another's halves, e.g. question length
    within similar-length videos, so a mechanical cause can be ruled out."""
    return [v for v in videos if matches(v.meta, spec)]


def since(videos, day):
    """Uploads published on or after `day`. A test that started mid-history
    reads only the weeks it ran: `--compare subreddit=NoStupidQuestions`
    across all history set NoStupidQuestions' first weeks against AskReddit's
    since July, when watch-seconds ran 8-9s against today's 12-13s (PRD §0 #3)."""
    return [v for v in videos if (v.true_published or v.published).date() >= day]


def ids_within(spec, log_rows=None):
    """Video ids of the logged uploads matching `spec`, for the readers that
    work on snapshot rows (the trajectory), which carry no upload_log fields.
    An unlogged video (the back catalogue) matches nothing, so a filtered
    trajectory covers logged uploads only. Raises ValueError for a value no
    logged upload has: with "!=", a typo would otherwise keep everything."""
    rows = _read_upload_log() if log_rows is None else log_rows
    metas = [_with_derived_dimensions(r) for r in rows]
    _require_value(metas, spec)
    return {m["video_id"] for m in metas if matches(m, spec)}


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


# As many as a release needs for its own verdict (RELEASE_MIN_UPLOADS): `v6`,
# with 10 at 7 days, is too thin to stand alone, so `v7` still reads its pool.
PREDECESSOR_MIN_UPLOADS = 20


def predecessor(before, key, min_uploads=None):
    """The release a new one replaced, and its uploads, from `release_cohorts`'
    preceding side; (None, before) when it is too thin to stand alone.

    Pooling every earlier release answers "worse than the channel's history?",
    not "worse than what it replaced?": `v7` read +20% over its pool (12.0 vs
    10.0 s), so `v8` judged against v2-v7 could fall ~17% below `v7` and still
    clear a 13% limit (2026-10-18, before any `v8` upload). The drift floor
    still reads the whole history, which a single release is too short for."""
    if not before:
        return None, before
    latest = max(before, key=lambda v: v.true_published or v.published)
    value = str(latest.meta.get(key, "")).strip()
    if not value:
        return None, before
    own = [v for v in before if str(v.meta.get(key, "")).strip() == value]
    need = PREDECESSOR_MIN_UPLOADS if min_uploads is None else min_uploads
    return (value, own) if len(own) >= need else (None, before)


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


def alternation_floor(videos, metric, block=MIN_COHORT):
    """`drift_floor`'s counterpart for a test that alternates by day.

    A release is judged against the batch before it, so it carries the
    calendar's swing. A change switched on and off on alternate days is
    judged against uploads from the same weeks. This measures that design's
    noise with nothing switched: take `2 * block` consecutive uploads, split
    them by the parity of their publish day, and record how far apart the two
    halves' medians sit. Returns the median of that across the history, or
    None without enough of it. Compare with `drift_floor` at the same
    `block`: the gap is what alternating would buy (PLAN C9, 2026-10-05).
    """
    live = sorted([v for v in videos if v.views > 0],
                  key=lambda v: v.true_published or v.published)
    size = block * 2
    deltas = []
    for i in range(0, len(live) - size + 1, size):
        chunk = live[i:i + size]
        day = lambda v: (v.true_published or v.published).toordinal() % 2
        on = [v.get(metric) for v in chunk if day(v)]
        off = [v.get(metric) for v in chunk if not day(v)]
        if len(on) < block // 2 or len(off) < block // 2:
            continue
        mx, my = median(off), median(on)
        if mx:
            deltas.append(abs(my - mx) / mx)
    return median(deltas) if deltas else None


# The uploads `report.py --compare` prices chance from: about six weeks at two
# a day. Noise grew from July to late August (`coin_floor`), and a read is
# judged against the weeks it sits in, not the channel's whole history.
CHANCE_SPAN = 90


def coin_windows(videos, metric, arm, other=None, span=None, min_views=1):
    """The upload windows `coin_floor` splits: every `arm + other` consecutive
    uploads with a value (`other` defaults to `arm`), anchored at the newest
    so the latest weeks count, each overlapping the next by half. `span`
    keeps only the newest that many uploads (never fewer than one window)."""
    size = arm + (arm if other is None else other)
    live = sorted([v for v in videos if v.views >= max(1, min_views)
                   and v.get(metric) is not None],
                  key=lambda v: v.true_published or v.published)
    if span:
        live = live[-max(span, size):]
    starts = range(len(live) - size, -1, -max(1, size // 2))
    return [[v.get(metric) for v in live[i:i + size]] for i in starts]


def coin_floor(videos, metric, arm, quantile=0.9, splits=200, seed=0, other=None,
               span=None, min_views=1):
    """The gap a coin-flip test (PRD §0 #14) reads with nothing switched.

    Each run's arm is random, so the arms share the calendar and the noise is
    a random split of the same weeks' uploads. Split each of `coin_windows` at
    random `splits` times and return the `quantile` of how far the two
    halves' medians sit apart, relative to the second arm's as
    `Comparison.delta` is. Two-sided: one arm leads by more than it roughly
    half that often. The 90th percentile, not the median, because a rule set
    at the median gap fires on chance about one read in four, one-sided.
    `other` sizes the second arm when the two differ: title style B runs
    two uploads to the rest's one (PRD §0 #10), and the smaller arm is what
    sets the noise. `span` reads only the newest uploads: at 15 a side the gap
    was 11-12% in July's windows and 33-36% from late August (2026-10-10
    review), so all history understates the noise a read meets today.
    `min_views` leaves out uploads with fewer plays, whose average is noisy
    (PRD §0 R4). None without one full window.
    """
    import random
    rng, deltas = random.Random(seed), []
    for values in coin_windows(videos, metric, arm, other, span, min_views):
        for _ in range(splits):
            rng.shuffle(values)
            mx, my = median(values[:arm]), median(values[arm:])
            if my:
                deltas.append(abs(mx - my) / my)
    if not deltas:
        return None
    deltas.sort()
    return deltas[min(len(deltas) - 1, int(quantile * len(deltas)))]


# What may fire a revert. The owner settled it on #18 (2026-09-22): "the rule
# now triggers on watch-seconds only, with views reported but never firing it".
# Views at a fixed age move 27-52% between batches with nothing changed, five
# times watch-seconds' 6-15%, so a views trigger fires on noise. Views are
# still compared and printed, with their own detection limit.
REVERT_TRIGGER = (Metric.WATCH,)


def release_triggers(release, before, threshold=1.0):
    """What may fire a revert for this release.

    Watch-seconds rises with length alone while views fall, so total watch time
    stays flat: a release that only lengthens videos would read "keep". The
    owner on #39 (2026-09-25): when median length shifts by `threshold` or more,
    total watch time must not drop either. Tightens that one case only."""
    a, b = median_duration(release), median_duration(before)
    if a is not None and b is not None and abs(a - b) >= threshold:
        return REVERT_TRIGGER + (Metric.TOTAL,)
    return REVERT_TRIGGER


def release_verdict(comparisons, floors=None, triggers=REVERT_TRIGGER, min_uploads=MIN_COHORT):
    """Fold `/shift` §5: a release that degraded **watch-seconds** is reverted,
    unless the drop is no bigger than the channel's own drift. Other metrics
    are reported beside it and never fire, except total watch time when the
    release shifted video length (`release_triggers`).

    Everything short of a clean, separable answer is an explicit "no verdict",
    never silence. The guardrail spent four releases returning nothing at all
    and reading, to anyone glancing at it, like approval.

    `min_uploads` is the experiment's own pre-committed size (PRD §0: v7
    commits to 20). MIN_COHORT is only this module's floor, so without it a
    read taken as soon as 8 uploads were a week old would answer anyway.
    """
    if not comparisons:
        return "NO VERDICT — nothing to compare"
    missing = [t for t in triggers if not any(c.metric == t for c in comparisons)]
    if missing:
        return f"NO VERDICT — {' / '.join(missing)} was not compared"
    for c in comparisons:
        if not (c.a.sufficient and c.b.sufficient):
            return (f"NO VERDICT — under {MIN_COHORT} measurable uploads on one side; "
                    f"bake longer")
        if min_uploads > MIN_COHORT and c.a.n + c.a.zero_view_count < min_uploads:
            return (f"NO VERDICT — {c.a.n + c.a.zero_view_count} measurable release "
                    f"uploads, the rule commits to {min_uploads}; bake longer")
        if not c.age_matched:
            return "NO VERDICT — cohorts are not age-matched"
    floors = floors or {}
    worse = []
    for c in comparisons:
        floor = floors.get(c.metric)
        if (c.metric in triggers
                and c.delta is not None and c.delta < 0 and abs(c.delta) >= MATERIAL
                and (floor is None or abs(c.delta) > floor)):
            worse.append(c.metric)
    if worse:
        return f"REVERT — {' and '.join(worse)} degraded beyond the channel's own drift"
    return (f"KEEP — {' / '.join(triggers)} did not degrade beyond the "
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


OWN_WORDS_DONE = 0.50  # bet 1's done-when (#70): our own words, every upload


def render_own_words(log_rows, version, key="format_version"):
    """Bet 1's done-when beside its release verdict (#70): how many of the
    release's uploads had our own words at OWN_WORDS_DONE or more of the
    narration. Read from the log, at any age: it is a property of what
    shipped, not of how it performed, so it never waits on snapshots. A
    fallback logs 0.00 and counts as a miss. Counts every upload of the release,
    whatever --within narrowed above it. Empty when nothing logs a share."""
    vals = []
    for r in log_rows:
        if r.get(key) != version:
            continue
        try:
            v = float((r.get("own_words_share") or "").strip())
        except ValueError:  # blank (before the column) or malformed: not read
            continue
        if v == v:  # not NaN
            vals.append(v)
    vals.sort()
    if not vals:
        return ""
    met = sum(1 for v in vals if v >= OWN_WORDS_DONE)
    line = (f"own words (bet 1's done-when, >= {OWN_WORDS_DONE:.2f} on every upload): "
            f"{met} of {len(vals)} uploads, median {statistics.median(vals):.2f}")
    fell_back = sum(1 for v in vals if v == 0)
    if fell_back:
        line += f", {fell_back} fell back to a plain reading"
    return line + (" -- DONE" if met == len(vals) else " -- NOT YET")


def render_within_length(read, threshold=1.0):
    """When a release shifted length, its watch-seconds within each length half.

    Attribution, never a trigger: a gain that is only longer videos is not the
    release's to claim. `v7`'s posts ran 3s longer for reasons outside its code
    and read +25%, but +8% within long videos (PRD §0 #1, pre-committed
    2026-10-07 before its read). The verdict stands as the owner set it (#18,
    #39). Empty when length did not shift."""
    a, b = median_duration(read.release), median_duration(read.before)
    if a is None or b is None or abs(a - b) < threshold:
        return ""
    label = read.comparisons[0].a.label if read.comparisons else "release"
    lines = ["WITHIN LENGTH — the gain the release may claim; attribution only, never a trigger"]
    for half in ("short", "long"):
        spec = f"video_length={half}"
        lines.append(compare(within(read.release, spec), within(read.before, spec),
                             f"{label}, {half}", f"before, {half}",
                             read.load.anchor, Metric.WATCH).render())
    return "\n".join(lines)


# Plays below which an upload leaves the robustness read: its average is
# YouTube's whole-second figure over a handful of viewers, often 0.0 on 1-6
# plays (TECH_DEBT). The floor #3 and #10 read with (`--min-views 10`).
RELEASE_MIN_VIEWS = 10


def binomial_two_sided(k, n, p):
    """P(a result at least as unlikely as k of n, at rate p). Exact; computed
    in logs, since math.comb(n, i) overflows a float past ~1,000 events."""
    if n == 0 or not 0 < p < 1:
        return 1.0
    logs = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
            + i * math.log(p) + (n - i) * math.log1p(-p) for i in range(n + 1)]
    cut = logs[k] + 1e-9
    return min(1.0, sum(math.exp(x) for x in logs if x <= cut))


def render_vote_diagnostics(read, min_uploads=MIN_COHORT):
    """Comments and subscribers gained per 100 views, each side pooled.

    Bet 1's vote is for these (PRD R3.2, pre-committed 2026-10-07), but both
    are almost always zero per upload (median 0 in every release, 2026-10-14),
    so a median reads 0 vs 0. Pooled, the test conditions on the total: given
    k events on both sides, the release's share is binomial in its share of
    the views. Never a trigger. That test treats events as independent, so
    the count of uploads carrying any is printed beside it: one busy thread
    is not an effect. Subscriber gains are read only over uploads whose
    snapshot carries them (from 2026-10-12), so their baseline is the late
    weeks of the era before, not all of it; a side with fewer than
    MIN_COHORT such uploads reads "insufficient data". Empty until the
    release reaches its pre-committed size, as `render_without_near_zero`."""
    if not read.comparisons:
        return ""
    head = read.comparisons[0]
    if head.a.n + head.a.zero_view_count < min_uploads:
        return ""
    lines = []
    for label, get in (("comments", lambda v: v.comments),
                       ("subscribers gained", lambda v: v.subs_gained)):
        sides = [[v for v in side if get(v) is not None and v.views > 0]
                 for side in (read.release, read.before)]
        if min(len(side) for side in sides) < MIN_COHORT:
            lines.append(f"  {label}: insufficient data ({len(sides[0])} vs "
                         f"{len(sides[1])} uploads log it, under {MIN_COHORT})")
            continue
        views = [sum(v.views for v in side) for side in sides]
        k = [int(round(sum(get(v) for v in side))) for side in sides]
        any_ = [sum(1 for v in side if get(v) > 0) for side in sides]
        p = binomial_two_sided(k[0], k[0] + k[1], views[0] / (views[0] + views[1]))
        lines.append(f"  {label}: {100 * k[0] / views[0]:.2f} vs {100 * k[1] / views[1]:.2f} "
                     f"per 100 views ({k[0]} over {views[0]:,.0f} on {any_[0]} of "
                     f"{len(sides[0])} uploads, vs {k[1]} over {views[1]:,.0f} on "
                     f"{any_[1]} of {len(sides[1])}), p={p:.2g}"
                     + ("" if p < 0.05 else ": chance-sized"))
    return "VOTE DIAGNOSTICS, pooled (never a trigger):\n" + "\n".join(lines)


def render_without_near_zero(read, min_uploads=MIN_COHORT, min_views=RELEASE_MIN_VIEWS):
    """The release's watch-seconds without uploads under `min_views` plays.

    Robustness, never a trigger: `v7` read +20% on every upload and +9%
    without them (2026-10-12), the retired clip's buried uploads sitting in
    the before-cohort. The verdict stands as the owner set it (#18). Empty
    when no upload on either side is under the floor, and until the release
    reaches its pre-committed size, so it cannot show a result the rule has
    not yet allowed (`release_verdict` counts the same way)."""
    if not read.comparisons:
        return ""
    head = read.comparisons[0]
    if head.a.n + head.a.zero_view_count < min_uploads:
        return ""
    # Zero-view uploads already sit outside the verdict's medians; count only
    # the ones this line removes.
    few = [sum(1 for v in side if 0 < v.views < min_views)
           for side in (read.release, read.before)]
    if not any(few):
        return ""
    a = [v for v in read.release if v.views >= min_views]
    b = [v for v in read.before if v.views >= min_views]
    return (f"WITHOUT UPLOADS UNDER {min_views} VIEWS ({few[0]} release and {few[1]} "
            "before left out) — robustness only, never a trigger\n"
            + compare(a, b, head.a.label, head.b.label, read.load.anchor,
                      Metric.WATCH).render())


# Each release's pre-committed size (PRD §0); one not listed is read at
# MIN_COHORT. An automatic read without it answers at 8 and pre-empts a rule
# that committed to more (#1: `v7` commits to 20; #15: bet 1's `v8`, 20).
RELEASE_MIN_UPLOADS = {"v7": 20, "v8": 20}


@dataclass
class ReleaseRead:
    load: object
    release: list
    before: list
    unset: int
    later: int
    triggers: tuple
    comparisons: list
    floors: dict


def release_read(version, key="format_version", target_age=None, within_spec=None):
    """The auto-revert check's inputs (`report.py --release`, the Monday
    digest), computed in one place so the two cannot drift. Every upload read
    at a common age; the drift floor comes from the era BEFORE the change, so
    a volatile release cannot excuse itself. None when no upload has a reading
    at the age."""
    target_age = AGE_MATCH_TARGET_DAYS if target_age is None else target_age
    load = load_videos_at_age(target_age)
    if not load.videos:
        return None
    # `within_spec` reads the release inside one group, both sides alike, e.g.
    # bet 1 within subreddit=AskReddit while subreddit rotation runs (PRD §0 #7).
    videos = within(load.videos, within_spec) if within_spec else load.videos
    a, history, unset, later = release_cohorts(videos, key, version)
    prior, b = predecessor(history, key)
    triggers = release_triggers(a, b)
    metrics = (Metric.WATCH, Metric.VIEWS) + tuple(
        t for t in triggers if t not in (Metric.WATCH, Metric.VIEWS))
    label = f"{key}={prior}" if prior else f"before {version}"
    comparisons = [compare(a, b, f"{key}={version}", label, load.anchor, m)
                   for m in metrics]
    floors = {m: drift_floor(history, m) for m in metrics}
    return ReleaseRead(load, a, b, unset, later, triggers, comparisons, floors)


def latest_releases(log_rows, key="format_version", n=2):
    """The last `n` releases in upload order, newest first. The previous one
    matters: `v6`'s read came due after `v7` shipped and sat unrecorded until a
    shift stumbled on it (2026-10-06)."""
    order = []
    for r in log_rows:
        v = r.get(key)
        if v:
            if v in order:
                order.remove(v)
            order.append(v)
    return order[::-1][:n]


def release_digest_line(log_rows, target_age=None):
    """One line for the Monday digest, so a due verdict reaches the owner
    whether or not a shift remembers to run the check (TECH_DEBT)."""
    target_age = AGE_MATCH_TARGET_DAYS if target_age is None else target_age
    parts = []
    for version in latest_releases(log_rows):
        read = release_read(version, target_age=target_age)
        if read is None:
            verdict = f"NO VERDICT — no upload has a snapshot at ~{target_age:g} days old"
        else:
            verdict = release_verdict(read.comparisons, read.floors, read.triggers,
                                      RELEASE_MIN_UPLOADS.get(version, MIN_COHORT))
        parts.append(f"`{version}`: {verdict}")
    return (f"**Release checks** (auto-revert, every upload read at ~{target_age:g} days) — "
            + (" · ".join(parts) if parts else "no release logged"))


def render_release(comparisons, floors, triggers=REVERT_TRIGGER, min_uploads=MIN_COHORT):
    """The release answer in full: every metric, each with the size of change
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
    quiet = {m: d for m, d in moved.items() if m not in triggers and d < 0}
    if quiet:
        also = ", ".join(f"{m} {d:+.0%}" for m, d in quiet.items())
        out.append(f"    NOT A TRIGGER: {also}, beyond its detection limit. Reported only; "
                   f"a revert fires on {' / '.join(triggers)} alone (owner, #18, #39).")
    if any(d > 0 for d in moved.values()) and any(d < 0 for d in moved.values()):
        better = ", ".join(f"{m} {d:+.0%}" for m, d in moved.items() if d > 0)
        worse = ", ".join(f"{m} {d:+.0%}" for m, d in moved.items() if d < 0)
        out.append(f"    CONFLICT: {better} but {worse}. The verdict follows "
                   f"{' / '.join(triggers)}.")
    out.append("")
    out.append(f"{release_verdict(comparisons, floors, triggers, min_uploads)}   (/shift §5 auto-revert rule)")
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
    buckets = {}
    for value, pub in _read_at_age(snapshot_rows, at_age, tolerance):
        buckets.setdefault(pub.strftime("%G-W%V"), []).append(value)
    return [(period, len(v), median(v))
            for period, v in sorted(buckets.items())
            if len(v) >= TRAJECTORY_MIN_N]


def _read_at_age(snapshot_rows, at_age, tolerance, keep_zero=False):
    """[(value, published)] — each video's reading nearest `at_age` days old."""
    best = {}
    for row in snapshot_rows:
        pub, snap = row.get("published"), row.get("snapshot")
        value = row.get("value")
        if not pub or not snap or value is None or value < 0:
            continue
        if not value and not keep_zero:
            continue
        age = (snap - pub).days
        if abs(age - at_age) > tolerance:
            continue
        key = row.get("video_id")
        prev = best.get(key)
        if prev is None or abs(age - at_age) < abs(prev[0] - at_age):
            best[key] = (age, value, pub)
    return [(value, pub) for _, value, pub in best.values()]


def weekly_totals(snapshot_rows, at_age=TRAJECTORY_AT_AGE, tolerance=4, known_rows=None):
    """Total views per publish-week, every upload read at the same age.

    Bet 2 (PLAN §2) is judged on total weekly views, because the Partner
    Program's bar is a total: more uploads count, and so does a lost one.
    A median would hide both. Zero-view uploads count, since they are part
    of the total.

    A sum is only honest over a week whose every upload was read, so a week
    is reported only when each of its uploads that any snapshot knows of has
    a reading at the age, and its Sunday upload is old enough to have one.
    That leaves out the newest weeks, still filling in, and the weeks before
    the snapshots began or across a missed one, rather than reporting them
    low. Returns [(period, n, total)] oldest first.

    `known_rows` says which uploads exist when `snapshot_rows` may leave some
    out: an upload with views but no engaged reading is skipped there, and
    judged from those rows alone its week would sum low (2026-10-13).
    """
    stamps = [r["snapshot"] for r in snapshot_rows if r.get("snapshot")]
    if not stamps:
        return []
    newest = (max(stamps) - datetime.timedelta(days=at_age - tolerance)).date()
    week = lambda pub: pub.strftime("%G-W%V")
    known = {}
    for r in list(snapshot_rows) + list(known_rows or ()):
        if r.get("published") and r.get("video_id"):
            known.setdefault(week(r["published"]), set()).add(r["video_id"])
    read = {}
    for value, pub in _read_at_age(snapshot_rows, at_age, tolerance, keep_zero=True):
        read.setdefault(week(pub), []).append((value, pub))
    out = []
    for period, values in sorted(read.items()):
        pub = values[0][1]
        sunday = (pub - datetime.timedelta(days=pub.weekday() - 6)).date()
        if len(values) < len(known.get(period, ())) or sunday > newest:
            continue
        out.append((period, len(values), sum(v for v, _ in values)))
    return out


def views_gained(snapshot_rows):
    """[(snapshot date, views gained since the previous snapshot, days)].

    The Partner Program counts Shorts views over 90 days, the back
    catalogue's included, while `weekly_totals` counts only new uploads'
    first week. This is the channel-wide figure the bar is read against, in
    play starts: the bar counts only their engaged share (`engaged_share`):
    the rise in the summed views of every video between consecutive
    snapshots. A video first seen in a snapshot counts in full, since it
    was published after the one before.
    """
    out = []
    for prev, cur, before, after, _ in _measured_pairs(snapshot_rows):
        gained = sum(max(v - before.get(vid, 0), 0) for vid, v in after.items())
        out.append((cur, gained, (cur - prev).days))
    return out


def _measured_pairs(snapshot_rows):
    """Consecutive snapshots as (prev, cur, before, after, published), leaving
    out a snapshot holding under half the videos published by its date: it
    did not measure this column. A column added later is absent before it
    began, except on zero-view rows, read as zero: engaged views began
    2026-10-05, so 09-28 held only zero-view videos and every video's
    lifetime engaged count read as gained in one week (19,027 of 19,771;
    10-13). Within a kept pair, a video missing from the earlier snapshot
    though published before it was unmeasured, not new: the callers count
    only videos in `before` or published since."""
    by_snap, published = {}, {}
    for r in snapshot_rows:
        if r.get("snapshot") and r.get("video_id") and r.get("value") is not None:
            by_snap.setdefault(r["snapshot"], {})[r["video_id"]] = r["value"]
            if r.get("published"):
                published[r["video_id"]] = r["published"]
    out_by = lambda d: sum(1 for p in published.values() if p <= d)
    dates = sorted(d for d in by_snap if len(by_snap[d]) * 2 >= out_by(d))
    for prev, cur in zip(dates, dates[1:]):
        before = by_snap[prev]
        after = {vid: v for vid, v in by_snap[cur].items()
                 if vid in before or published.get(vid) is None or published[vid] > prev}
        yield prev, cur, before, after, published


def views_gained_by_age(snapshot_rows, old_days=60):
    """[(snapshot date, old gained, recent gained, days)]: `views_gained`
    split by each video's age at the earlier snapshot. A drop in new uploads'
    views that the back catalogue shares at the same moment is the channel's
    distribution, not anything about the new uploads (the September 2026 drop
    held across every field we log, PRD §4)."""
    out = []
    for prev, cur, before, after, published in _measured_pairs(snapshot_rows):
        old = recent = 0
        for vid, v in after.items():
            gained = max(v - before.get(vid, 0), 0)
            pub = published.get(vid)
            if pub is not None and (prev - pub).days >= old_days:
                old += gained
            else:
                recent += gained
        out.append((cur, old, recent, (cur - prev).days))
    return out


def views_concentration(snapshot_rows, at_age=TRAJECTORY_AT_AGE, tolerance=4, top=0.10):
    """How much of the views the best uploads earn, each read at the same age.

    The Partner Program's bar is a total, and a total over a lottery is set by
    its few winners: if a tenth of uploads earn most of the views, the views
    half of the bar is a hit-rate problem, and a change that moves the median
    upload is the smaller lever (PRD §0 R4). Zero-view uploads count, since
    they are part of the total. Returns (n, total, top_n, top_total, biggest),
    or None below a cohort's worth of reads.
    """
    values = sorted((v for v, _ in _read_at_age(snapshot_rows, at_age, tolerance,
                                                 keep_zero=True)), reverse=True)
    if len(values) < MIN_COHORT:
        return None
    top_n = max(1, round(len(values) * top))
    return len(values), sum(values), top_n, sum(values[:top_n]), values[0]


def hit_rates(videos, key, top=0.10):
    """([(group, n, hits, p)], cut): how often each value of `key` makes the
    top `top` share of `videos` by views, highest rate first, with Fisher's
    two-sided p against every other upload (PRD §0 R5). Zero-view uploads
    count in n; they can never be hits."""
    cut = max(1, round(len(videos) * top))
    hits = {id(v) for v in sorted(videos, key=lambda v: v.views, reverse=True)[:cut]}
    rows = []
    for label, vids in split_by(videos, key).items():
        h = sum(id(v) in hits for v in vids)
        rows.append((label, len(vids), h,
                     buried_rate_p(h, len(vids), cut - h, len(videos) - len(vids))))
    rows.sort(key=lambda r: (r[2] / r[1], r[1]), reverse=True)
    return rows, cut


def buried_vs_rest(groups, min_n=MIN_COHORT, hit=is_buried, pooled=True):
    """[(label, hits, n, p)]: each group's buried rate (<= BURIED_VIEWS)
    against every other group pooled, Mantel-Haenszel within formats so an
    era mix cannot pass for an effect (#11's clip read uneven across releases).
    Groups under `min_n` and "(unset)" are skipped; `p` is uncorrected, so a
    reader of k rows compares it with 0.05 / k (PRD §0 #11). A group that
    clears that bar is left out of every other group's "rest" on a second
    pass: the retired clip's 9 buried of 18 would otherwise raise the baseline
    and hide a second bad clip behind it. `hit` swaps the tail tested, e.g.
    `top_share_hits` for which groups make the hits.

    `pooled=False` is for groups that *are* the formats: a release shares no
    format with the rest, so pooling within formats returns 1.0 for every
    release whatever its rate. Plain Fisher then, with the calendar inside the
    comparison, and unlike `--release` later releases sit in each one's rest
    (2026-10-10). Pooled, any group sharing no format with its rest reads 1.0
    too: untestable, not null (no logged field does, 2026-10-10)."""
    def tests(exclude):
        rows = []
        for label, vids in groups.items():
            if label == "(unset)" or len(vids) < min_n:
                continue
            rest = [v for other, vs in groups.items()
                    if other not in (label, "(unset)") and other not in exclude for v in vs]
            if not rest:
                continue
            hits = sum(map(hit, vids))
            p = (buried_rate_p_pooled(buried_strata(vids, rest, hit=hit)) if pooled
                 else buried_rate_p(hits, len(vids), sum(map(hit, rest)), len(rest)))
            rows.append((label, hits, len(vids), p))
        return sorted(rows, key=lambda r: r[3])

    first = tests(exclude=())
    flagged = {label for label, _, _, p in first if p < 0.05 / len(first)}
    return tests(exclude=flagged) if flagged else first


def totals_change(series, weeks=4):
    """(prior total, recent total, ratio) over the last `weeks` against the
    `weeks` before, or None without enough complete weeks to compare."""
    if len(series) < weeks * 2:
        return None
    recent = sum(t for _, _, t in series[-weeks:])
    prior = sum(t for _, _, t in series[-weeks * 2:-weeks])
    return prior, recent, (recent / prior if prior else None)


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
# Guardrails where a rise is the bad direction. Without this a rising zero
# rate could never breach, and a falling one would (found 2026-10-06).
HIGHER_IS_WORSE = {"zero_rate"}
DIAGNOSTICS = ("views", "duration_s", "likes_per_100", "comments_per_100",
               "engaged_per_100")


def engaged_per_100(snapshot_rows):
    """Engaged views per 100 play starts over a period: the share the Partner
    Program counts (PLAN §1). None unless every row with views carries the
    count, so a period read before the column (2026-10-05) shows nothing
    rather than a share of whichever rows happened to have it. The API leaves
    it blank on zero-view rows (all 41 blanks on 2026-10-05), which is no gap."""
    views = engaged = 0.0
    for r in snapshot_rows:
        v = float(r.get("views") or 0)
        if not v:
            continue
        e = _optional_float(r.get("engaged_views"))
        if e is None:
            return None
        views, engaged = views + v, engaged + e
    return 100.0 * engaged / views if views else None


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
            worse_by = change if metric in HIGHER_IS_WORSE else -change
            if worse_by > margins[metric]:
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


def slate_agreement(rows):
    """(agreeing, labelled, disagreements) over upload_log rows: how often the
    slate's label for the selected post (`slate[candidate_rank - 1]`) matches
    the screen's `topic`. R4.4's firing rate is counted on slate labels, so
    read this first — disagreement means the two classifiers bucket the same
    post differently. `disagreements` is a list of (screen, slate) pairs.
    Rows with no slate, a failed call ("!…") or an unlabelled entry are skipped,
    and so are rows the screen's fallback answered: that is the slate's own
    model, so the two would agree with themselves."""
    agree, pairs = 0, []
    for r in rows:
        if (r.get("screen_source") or "").strip() == "gemini_fallback":
            continue
        slate = (r.get("slate_topics") or "").strip()
        topic = (r.get("topic") or "").strip()
        rank = (r.get("candidate_rank") or "").strip()
        if not slate or slate.startswith("!") or not topic or not rank.isdigit():
            continue
        labels = slate.split("|")
        k = int(rank)
        if not 1 <= k <= len(labels) or labels[k - 1] in ("", "?"):
            continue
        if labels[k - 1] == topic:
            agree += 1
        else:
            pairs.append((topic, labels[k - 1]))
    return agree, agree + len(pairs), pairs


# R4.4's tiers, measured on current-format content (PRD §4, R4.3 re-run,
# 2026-09-11: Spearman +0.79 against the pre-overhaul ordering).
STRONG_TOPICS = ("nostalgia", "humor-absurd", "dark-morbid")
WEAK_TOPICS = ("life-advice", "money-work", "fame-celebrity")
SLATE_FIRING_MIN_RUNS = 20   # PRD §0 #2 / §6 Step 0.5: "after >=20 uploads"


def slate_firing(rows, depth=3):
    """(fired, read) over upload_log rows: R4.4's pre-committed firing-rate
    read. A run fires when the slate's rank-1 candidate is weak-tier and a
    strong-tier one sits within the top `depth`. Slates are read as logged:
    every eligible candidate in Reddit rank order. Rows with no slate or a
    failed call ("!...") are not read; an unlabelled entry ("?") never fires."""
    fired = read = 0
    for r in rows:
        slate = (r.get("slate_topics") or "").strip()
        if not slate or slate.startswith("!"):
            continue
        labels = slate.split("|")
        read += 1
        if labels[0] in WEAK_TOPICS and any(t in STRONG_TOPICS for t in labels[1:depth]):
            fired += 1
    return fired, read


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


def _optional_float(value):
    """A number, or None where the column was not collected: blank, or the
    reason a refused metric leaves in its place (weekly_analytics writes
    "refused: ..." so a shift can read why). Raising here would take every
    age-matched read down with one refused week."""
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _parse_ts(value):
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _read_upload_log():
    with open(config.UPLOAD_LOG) as f:
        return with_clip_use([r for r in csv.DictReader(f) if r.get("video_id")])


def with_clip_use(rows):
    """Add `clip_use`: "early" for a b-roll clip's first CLIP_EARLY_USES
    uploads, "late" after (R4). It counts across the whole log, so it cannot
    live in _with_derived_dimensions, which sees one row. The threshold came
    from retired clip #11 itself, so read R4 on the other clips."""
    seen = {}
    for r in sorted(rows, key=lambda r: r.get("timestamp_utc") or ""):
        bg = (r.get("bg_clip") or "").strip()
        if not bg or bg.startswith("procedural"):
            r["clip_use"] = ""
            continue
        seen[bg] = seen.get(bg, 0) + 1
        r["clip_use"] = "early" if seen[bg] <= CLIP_EARLY_USES else "late"
    return rows


# title_hype: shock phrases and capitalised emphasis ("The SHOCKING Truth",
# "Who's YOUR Hero?"); capitals that are real acronyms don't count.
_HYPE_WORD = re.compile(
    r"shock|won.?t believe|never guess|insane|exposed|jaw.?drop|mind.?blow", re.I)
_ACRONYMS = config.TITLE_ACRONYMS


# Topic labels for uploads from before the screen logged one (82 rows, mostly
# `v4`): the channel-wide labelling pass (scripts/analyze_channel.py) keeps
# them here, keyed by the Reddit question. Where both exist they agree on 29 of
# 30 uploads (2026-10-16). Read as `topic_any`, never into `topic`, so reads
# pre-committed on `topic` (R1, PRD §0 #2) keep their population.
_TOPICS_CACHE = config.ROOT / "analysis" / "topics_cache.json"


@functools.lru_cache(maxsize=1)
def _cached_topics():
    try:
        return json.loads(_TOPICS_CACHE.read_text())
    except (OSError, ValueError):
        return {}


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
    # Do buried uploads come in calendar runs? Then a clip, voice or release
    # that was on air at the time takes the blame for a channel-wide spell
    # (R3's 09-06..09-19 cluster). `--by publish_week --metric views`.
    r["publish_week"] = "" if not ts else _parse_ts(ts).strftime("%G-W%V")
    # 63 characters is the logged median (2026-09-25), so the halves are even.
    q = (r.get("post_title") or "").strip()
    r["question_length"] = "" if not q else "short" if len(q) <= 63 else "long"
    # The logged topic, else the labelling pass's (see _TOPICS_CACHE).
    r["topic_any"] = (r.get("topic") or "").strip() or (_cached_topics().get(q, "") if q else "")
    # The question is the narrated opening: does addressing the viewer hold
    # them? 90 of 154 logged questions say "you" (2026-10-03).
    r["question_person"] = "" if not q else (
        "you" if re.search(r"\byou(?:r|rs|'re|'ve|'d|'ll)?\b", q, re.I) else "other")
    # A failed title call ships the Reddit question verbatim. title_ok only
    # exists from 2026-09-19; comparing the two titles covers the older rows.
    # Where it is logged it decides: a generated echo of a lower-case question
    # can now be sentence-cased into an exact match (llm.sentence_case, 10-14).
    # The two agreed on all 48 rows that log it.
    t = (r.get("video_title") or "").strip()
    ok = (r.get("title_ok") or "").strip()
    r["title_source"] = ("" if not (q and t) else "raw" if ok == "0" else
                         "generated" if ok == "1" else "raw" if t == q else "generated")
    # Who wrote the title, so the title tests (#10, #14) can set Groq's apart
    # once v8 logs `meta_source` (#13). `meta_source!=groq` would drop every
    # older row, since an unset field matches neither side; before the column
    # no production call reached Groq (GROQ_FALLBACK was never on in `main`),
    # so an older generated title is Gemini's.
    src = (r.get("meta_source") or "").strip()
    r["title_writer"] = ("" if not r["title_source"] else
                         "reddit" if r["title_source"] == "raw" else
                         "groq" if src.startswith("groq") else "gemini")
    # Raw titles run ~64 characters, generated ~41 (the generated median,
    # 2026-10-04): is length, not source, behind raw titles' views gap?
    r["title_length"] = "" if not t else "short" if len(t) <= 41 else "long"
    # YouTube's monetization review reads titles, and since July 2026 refuses
    # content "designed to shock or surprise viewers for the sole purpose of
    # getting views". Do our capitals-and-shock titles earn the views that
    # would justify them? Generated titles only: a raw one is Reddit's wording.
    r["title_hype"] = "" if not t or r["title_source"] == "raw" else (
        "hype" if _HYPE_WORD.search(t) or any(
            w not in _ACRONYMS for w in re.findall(r"\b[A-Z]{2,}\b", t)) else "plain")
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
    rows = _read_upload_log()

    ya = analytics.youtube_analytics_client()
    stats, ids = {}, [r["video_id"] for r in rows]
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        resp = ya.reports().query(
            ids="channel==MINE", startDate="2024-01-01",
            endDate=now.date().isoformat(),
            metrics="views,averageViewDuration,averageViewPercentage,likes,comments,estimatedMinutesWatched",
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
            est_minutes=float(s.get("estimatedMinutesWatched", 0)),
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


def _snapshot_privacy(rows):
    """{video_id: (privacy, lifetime views)} from the newest snapshot that
    recorded privacy; {} before `privacy_status` began (2026-10-12). A blank
    cell in that snapshot reads "unknown"."""
    dated = [r["snapshot_date"] for r in rows if r.get("privacy_status")]
    if not dated:
        return {}
    latest = max(dated)
    return {r["video_id"]: (r.get("privacy_status") or "unknown", float(r.get("views") or 0))
            for r in rows if r["snapshot_date"] == latest}


def _privatised_zero(video_id, views, privacy):
    """The rule load_videos applies with live privacy: drop an upload whose
    reading is zero only if it is not public and has no views to date (or is
    gone from the newest snapshot). One that earned views and was made private
    later keeps its reading, zero at 7 days or not."""
    if views != 0 or not privacy:
        return False
    status, lifetime = privacy.get(video_id, ("unknown", 0.0))
    return status != "public" and lifetime == 0


def _privacy_caveat(non_public, privacy_known):
    if not privacy_known:
        return ("privacy is not recorded in the snapshots read, so an owner-privatised "
                "upload reads as zero-view; medians are unaffected (zeros are excluded "
                "from them) but the zero count may overstate suppression")
    return (f"{len(non_public)} zero-view upload(s) are non-public (owner-privatised) "
            f"and excluded, not counted as zero-view")


@dataclass
class OfflineLoad:
    """What the snapshot could and could not measure — returned together so a
    caller cannot report the numbers without the caveats."""
    videos: list
    asof: datetime.datetime = None
    too_new: list = field(default_factory=list)   # published after the snapshot
    absent: list = field(default_factory=list)    # older, yet missing from it
    non_public: list = field(default_factory=list)  # zero-view and privatised: excluded
    privacy_known: bool = False                     # a snapshot recorded privacy

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
        out.append(_privacy_caveat(self.non_public, self.privacy_known))
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

    Privacy: from 2026-10-12 the snapshot records it, and a zero-view upload
    that is non-public is excluded, as `load_videos` does. Before that, such an
    upload reads as zero-view. Bounded, not silent: see `OfflineLoad.caveats()`.
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
    privacy = _snapshot_privacy(snapshot_rows)

    rows = _read_upload_log()

    videos, too_new, absent, non_public = [], [], [], []
    for r in rows:
        published = _parse_ts(r["timestamp_utc"])
        s = stats.get(r["video_id"])
        if s is None:
            (too_new if published > asof else absent).append(r["video_id"])
            continue
        if (published <= asof - datetime.timedelta(days=min_age_days)
                and _privatised_zero(r["video_id"], float(s.get("views") or 0), privacy)):
            non_public.append(r["video_id"])
            continue
        r = _with_derived_dimensions(r)
        v = Video(
            video_id=r["video_id"], published=published,
            views=float(s.get("views") or 0),
            watch_seconds=float(s.get("avg_view_duration_s") or 0),
            est_minutes=float(s.get("est_minutes_watched") or 0),
            engaged_views=_optional_float(s.get("engaged_views")),
            avg_view_pct=float(s.get("avg_view_pct") or 0),
            likes=float(s.get("likes") or 0), comments=float(s.get("comments") or 0),
            meta=r,
            **{m: _optional_float(s.get(m)) for m in Metric.RETENTION},
        )
        if v.age_days(asof) >= min_age_days:
            videos.append(v)
    return OfflineLoad(videos, asof, too_new, absent, non_public, bool(privacy))


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
    non_public: list = field(default_factory=list)   # zero-view and privatised: excluded
    privacy_known: bool = False                      # a snapshot recorded privacy

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
        out.append(_privacy_caveat(self.non_public, self.privacy_known))
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
    privacy = _snapshot_privacy([r for rows in by_video.values() for r in rows])

    rows = _read_upload_log()

    videos, not_yet, no_coverage, non_public = [], [], [], []
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
        if _privatised_zero(row["video_id"], float(s.get("views") or 0), privacy):
            non_public.append(row["video_id"])
            continue
        meta = _with_derived_dimensions(row)
        videos.append(Video(
            video_id=row["video_id"],
            published=anchor - datetime.timedelta(days=age),
            true_published=published,
            views=float(s.get("views") or 0),
            watch_seconds=float(s.get("avg_view_duration_s") or 0),
            est_minutes=float(s.get("est_minutes_watched") or 0),
            engaged_views=_optional_float(s.get("engaged_views")),
            avg_view_pct=float(s.get("avg_view_pct") or 0),
            likes=float(s.get("likes") or 0),
            comments=float(s.get("comments") or 0),
            subs_gained=_optional_float(s.get("subs_gained")),
            meta=meta,
            **{m: _optional_float(s.get(m)) for m in Metric.RETENTION},
        ))
    return AgeMatchedLoad(videos, anchor, target_age_days, not_yet, no_coverage,
                          non_public, bool(privacy))


# ---------------------------------------------------------------- zero-view analysis

ZERO_NEIGHBOURS = 4          # uploads either side used to judge "was the channel alive?"
COLD_SPELL_MEDIAN = 5        # neighbour median at/below this = channel-wide dead patch
ZERO_MIN_AGE_DAYS = MIN_AGE_DAYS  # below this, 0 views means "new", not "suppressed"


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


def load_channel_videos_offline():
    """load_channel_videos read from the newest weekly snapshot, for a shift
    with no YouTube access. Returns (videos, asof); videos is None when that
    snapshot predates `privacy_status` (added 2026-10-08), because
    calling a privatised video buried is the wrong conclusion
    classify_zero_views exists to prevent. A row with the column blank reads
    as non-public: excluded, the safe direction. Views are Analytics lifetime
    views at the snapshot (1-2 days' lag), so judge ages at `asof`."""
    if not config.ANALYTICS_SNAPSHOTS.exists():
        return None, None
    with open(config.ANALYTICS_SNAPSHOTS, newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("snapshot_date")]
    if not rows:
        return None, None
    latest = max(r["snapshot_date"] for r in rows)
    asof = datetime.datetime.fromisoformat(latest).replace(tzinfo=datetime.timezone.utc)
    rows = [r for r in rows if r["snapshot_date"] == latest]
    if not any(r.get("privacy_status") for r in rows):
        return None, asof
    titles = ({r["video_id"]: r.get("video_title", "") for r in _read_upload_log()}
              if config.UPLOAD_LOG.exists() else {})
    return [{
        "id": r["video_id"],
        "published": r["published_at"],
        "title": titles.get(r["video_id"], ""),
        "views": int(float(r["views"] or 0)),
        "privacy": r.get("privacy_status") or "unknown",
    } for r in rows], asof


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


def engaged_check(snapshot_rows, min_views=20, tolerance=0.10):
    """PRD §0 R2: does est_minutes x 60 / (views x avg_view_duration_s) equal
    engaged_views / views? Read on rows where the API returned both.

    Returns (n, median implied/actual ratio, share of rows within `tolerance`
    of 1), or (0, None, None). A median near 1 with most rows inside the band
    means the minutes column encodes engaged views, so history can be read.
    """
    ratios = []
    for r in snapshot_rows:
        try:
            views = float(r["views"])
            dur = float(r["avg_view_duration_s"])
            engaged = float(r["engaged_views"])
            minutes = float(r["est_minutes_watched"])
        except (KeyError, TypeError, ValueError):
            continue
        if views < min_views or dur <= 0 or engaged <= 0:
            continue
        implied = minutes * 60 / (views * dur)
        ratios.append(implied / (engaged / views))
    if not ratios:
        return 0, None, None
    within = sum(1 for x in ratios if abs(x - 1) <= tolerance) / len(ratios)
    return len(ratios), statistics.median(ratios), within


ENGAGED_SHARE_MIN_VIDEOS = 20


def engaged_share(snapshot_rows, published_since=None):
    """What share of our views does the Partner Program count? Since
    2025-03-31 `views` counts every play start, while the bar's "qualified
    Shorts views" are the older, stricter engaged count (PLAN §1). Summed over
    rows carrying both, optionally only videos published on or after
    `published_since` (an aware datetime).

    Returns (n videos, views, engaged views, share), or (n, views, engaged,
    None) under ENGAGED_SHARE_MIN_VIDEOS — too few to restate a gap with.
    """
    n, views, engaged = _summed(snapshot_rows, "engaged_views", published_since)
    if n < ENGAGED_SHARE_MIN_VIDEOS or not views:
        return n, views, engaged, None
    return n, views, engaged, engaged / views


def subscriber_rate(snapshot_rows, published_since=None):
    """Subscribers gained per 1,000 views, summed like `engaged_share`. A
    follower bar (TikTok's 10k, the Partner Program's 1,000) is a distance in
    views only through this rate, so a route priced on views alone hides its
    other half (PLAN §1, 2026-10-17).

    Returns (n videos, views, subscribers gained, per 1,000), the last None
    under ENGAGED_SHARE_MIN_VIDEOS."""
    n, views, subs = _summed(snapshot_rows, "subs_gained", published_since)
    if n < ENGAGED_SHARE_MIN_VIDEOS or not views:
        return n, views, subs, None
    return n, views, subs, subs / views * 1000


def poisson_interval(k, conf=0.95):
    """Exact (Garwood) interval for a Poisson count `k`: the range of true
    means that could have produced it. Subscriber gains are counts in the
    tens, so a rate built on them needs its range printed beside it; 11 gains
    reads anywhere from ~5 to ~20 (2026-10-17). It treats views as fixed and
    gains as independent; one video bringing a burst would make it too narrow
    (today the 23 gains sit one to a video, one video with two)."""
    assert 0 < conf < 1, conf
    alpha = (1 - conf) / 2

    def cdf(n, lam):        # P(X <= n), summed in logs so large lam is safe
        if n < 0:
            return 0.0
        return sum(math.exp(i * math.log(lam) - lam - math.lgamma(i + 1))
                   for i in range(n + 1)) if lam > 0 else 1.0

    def solve(f, target, hi):   # f falls as lam rises
        lo = 0.0
        for _ in range(100):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) > target else (lo, mid)
        return (lo + hi) / 2

    top = k + 10 * math.sqrt(k + 1) + 10
    lower = 0.0 if k == 0 else solve(lambda lam: cdf(k - 1, lam), 1 - alpha, top)
    upper = solve(lambda lam: cdf(k, lam), alpha, top)
    return lower, upper


def _summed(snapshot_rows, column, published_since):
    """(n, views, column total) over rows reporting both, optionally only
    videos published on or after `published_since`."""
    n, views, total = 0, 0, 0
    for r in snapshot_rows:
        try:
            v, x = int(float(r["views"])), int(float(r[column]))
        except (KeyError, TypeError, ValueError):
            continue        # blank: the API did not report it
        if published_since and (not r.get("published_at")
                                or _parse_ts(r["published_at"]) < published_since):
            continue
        n, views, total = n + 1, views + v, total + x
    return n, views, total
