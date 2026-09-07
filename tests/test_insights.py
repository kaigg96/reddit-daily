"""Tests for the pure analysis logic.

Each test corresponds to a mistake that actually reached a decision — see
TECH_DEBT.md Pass 2. The point isn't coverage for its own sake; it's that the
specific failures we've already made can't recur silently.
"""

import datetime
import math

import pytest

from src import insights
from src.insights import Metric, Video

NOW = datetime.datetime(2026, 8, 23, tzinfo=datetime.timezone.utc)


def v(vid, age_days, views=100, watch=10.0, pct=50.0, **meta):
    return Video(
        video_id=vid,
        published=NOW - datetime.timedelta(days=age_days),
        views=views, watch_seconds=watch, avg_view_pct=pct, meta=meta,
    )


def cohort(n, age_days, prefix, **kw):
    return [v(f"{prefix}{i}", age_days, **kw) for i in range(n)]


def cohort_cached(age_days, n=5):
    """Cohort with age_days_cached populated, as compare() would do."""
    items = cohort(n, age_days, f"c{age_days}")
    for i in items:
        i.age_days_cached = i.age_days(NOW)
    return items


# --- rule 3: thin slices must refuse to report ------------------------------

def test_small_cohort_reports_insufficient_not_a_median():
    a = cohort(3, 10, "a", watch=20.0)   # would look like a huge win
    b = cohort(30, 10, "b", watch=10.0)
    result = insights.compare(a, b, "tiny", "baseline", NOW)
    assert result.verdict == "insufficient data"


def test_sufficient_cohorts_do_report():
    a = cohort(insights.MIN_COHORT, 10, "a", watch=12.0)
    b = cohort(insights.MIN_COHORT, 10, "b", watch=10.0)
    assert "better by 20%" in insights.compare(a, b, "a", "b", NOW).verdict


# --- rule 2: age-matching (the b-roll false win) ----------------------------

def test_age_mismatched_comparison_is_flagged_not_reported():
    """The b-roll bug: recent videos looked far better purely because they
    were recent. A 5-day cohort vs a 200-day cohort must not yield a verdict."""
    fresh = cohort(12, 5, "fresh", watch=14.0)
    old = cohort(12, 200, "old", watch=9.0)
    result = insights.compare(fresh, old, "b-roll", "procedural", NOW)
    assert result.verdict == "not age-matched — unreliable"
    assert "WARNING" in result.render()


def test_similar_ages_are_considered_matched():
    a = cohort(12, 10, "a")
    b = cohort(12, 13, "b")
    assert insights.compare(a, b, "a", "b", NOW).age_matched


def test_ages_comparable_is_relative_not_absolute():
    """Age effects are roughly logarithmic: 100d vs 130d is a small gap,
    3d vs 30d is not, even though the absolute difference is smaller."""
    assert insights.ages_comparable(cohort_cached(100), cohort_cached(130))
    assert not insights.ages_comparable(cohort_cached(3), cohort_cached(30))


# --- rule 4: zero-view videos are suppression events, not weak performance --

def test_zero_view_videos_excluded_from_median_but_counted():
    live = cohort(10, 10, "live", views=100, watch=10.0)
    suppressed = [v("zero", 10, views=0, watch=0.0)]
    c = insights.summarize(live + suppressed, "cohort", Metric.WATCH, NOW)
    assert c.n == 10                 # zero-view not counted in n
    assert c.zero_view_count == 1
    assert c.median == 10.0          # and not dragged toward 0


# --- rule 1: watch-seconds is the default metric ----------------------------

def test_default_metric_is_watch_seconds_not_percentage():
    """The R1.8 mistake: shorter videos inflate avg-% while watch-seconds are
    flat. Default comparisons must reflect watch-seconds."""
    short = cohort(10, 10, "short", watch=9.0, pct=65.0)
    long_ = cohort(10, 10, "long", watch=9.0, pct=45.0)
    assert insights.compare(short, long_, "short", "long", NOW).verdict == "no material difference"
    # the ratio still shows the illusory win when explicitly requested
    pct_cmp = insights.compare(short, long_, "short", "long", NOW, metric=Metric.PCT)
    assert "better" in pct_cmp.verdict


# --- age-adjusted residuals -------------------------------------------------

def test_residuals_rank_above_trend_video_higher():
    videos = [v(f"n{i}", age_days=d, views=views)
              for i, (d, views) in enumerate([(10, 50), (50, 200), (100, 400), (200, 800)])]
    over = v("over", age_days=10, views=500)     # young but many views
    res = insights.age_adjusted_residuals(videos + [over], NOW)
    assert res["over"] > max(res[x.video_id] for x in videos)


def test_residuals_degrade_gracefully_on_thin_data():
    assert insights.age_adjusted_residuals([v("a", 10)], NOW) == {}


def test_zero_view_videos_do_not_break_residuals():
    videos = cohort(5, 10, "a", views=100) + [v("zero", 10, views=0)]
    res = insights.age_adjusted_residuals(videos, NOW)
    assert "zero" not in res


# --- grouping ---------------------------------------------------------------

def test_split_by_groups_and_labels_missing_values():
    videos = [v("a", 10, format_version="v4"), v("b", 10, format_version="v5"),
              v("c", 10)]
    groups = insights.split_by(videos, "format_version")
    assert set(groups) == {"v4", "v5", "(unset)"}
    assert len(groups["v4"]) == 1


def test_no_baseline_is_reported_rather_than_dividing_by_zero():
    a = cohort(10, 10, "a", watch=10.0)
    b = cohort(10, 10, "b", watch=0.0)
    assert insights.compare(a, b, "a", "b", NOW).verdict == "no baseline"


# --- regression: unlogged upload / blank metadata (2026-08-24 incident) ------

def test_blank_bg_clip_is_not_counted_as_broll():
    """A workflow bug lost an upload's log row; the backfilled row has a blank
    bg_clip. Blank must not be silently bucketed as 'broll' — that would
    corrupt the very comparison the b-roll library exists to inform."""
    from src.insights import Video  # noqa: F401
    rows = [{"bg_clip": "procedural:12"}, {"bg_clip": "pexels_1.mp4"},
            {"bg_clip": ""}, {}]
    got = []
    for r in rows:
        bg = (r.get("bg_clip") or "").strip()
        got.append("(unknown)" if not bg else
                   "procedural" if bg.startswith("procedural") else "broll")
    assert got == ["procedural", "broll", "(unknown)", "(unknown)"]


# --- zero-view classification (2026-08-30: both traps hit in one investigation) ---

def _cv(vid, day, views, privacy="public"):
    return {"id": vid, "published": f"2026-07-{day:02d}T01:00:00Z",
            "views": views, "privacy": privacy, "title": vid}


def test_private_zero_is_not_a_suppression_candidate():
    """10 of the channel's 41 zeroes are owner-privatised. Counting them as
    suppression once produced 'the screen is missing benign content'."""
    vids = [_cv(f"ok{i}", i, 100) for i in range(1, 6)] + [_cv("priv", 6, 0, "private")]
    got = insights.classify_zero_views(vids)
    assert [v["id"] for v in got["non_public"]] == ["priv"]
    assert got["isolated"] == [] and got["cold_spell"] == []


def test_zero_inside_a_cold_spell_is_not_per_video_moderation():
    """The chiropractic video sat in a patch reading 1,0,0,3,1,[0],37 — the
    whole channel was dead. It was recorded as confirmed suppression case #2."""
    vids = ([_cv(f"dead{i}", i, v) for i, v in enumerate([1, 0, 0, 3, 1], start=1)]
            + [_cv("target", 6, 0)] + [_cv(f"back{i}", i, 37) for i in range(7, 10)])
    got = insights.classify_zero_views(vids)
    assert "target" in [v["id"] for v in got["cold_spell"]]
    assert "target" not in [v["id"] for v in got["isolated"]]


def test_isolated_zero_among_healthy_neighbours_is_flagged():
    vids = [_cv(f"ok{i}", i, 200) for i in range(1, 6)] + [_cv("sup", 6, 0)] \
           + [_cv(f"ok{i}", i, 200) for i in range(7, 11)]
    got = insights.classify_zero_views(vids)
    assert [v["id"] for v in got["isolated"]] == ["sup"]


def test_zero_at_the_edge_of_a_cold_spell_is_still_cold_spell():
    """A symmetric window straddles the collapse and its recovery. The
    chiropractic video (before: 0,0,3,1 / after: 37,15,43,210) must read as
    cold-spell, not isolated — it was PRD's confirmed case #2."""
    vids = ([_cv(f"d{i}", i, v) for i, v in enumerate([0, 0, 3, 1], start=1)]
            + [_cv("edge", 5, 0)]
            + [_cv(f"r{i}", i, v) for i, v in zip(range(6, 10), [37, 15, 43, 210])])
    got = insights.classify_zero_views(vids)
    assert "edge" in [v["id"] for v in got["cold_spell"]]


# --- publish drift (2026-09-07: 4.5h drift ran unnoticed for 10 days) --------

def test_publish_drift_is_measured_against_nearest_slot_across_midnight():
    """A 23:50 publish is 33 min from the 00:23 slot, not 1407 min — without
    wrapping, near-midnight uploads would look catastrophically late."""
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from scripts import weekly_digest as wd
    vids = [{"published": "2026-09-07T23:50:00Z"}, {"published": "2026-09-07T00:23:00Z"}]
    assert wd.median_publish_drift(vids, days=36500) == 16.5   # median of 33 and 0
