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


# --- traffic sources (R4.7) -------------------------------------------------

def test_chunked_cohort_queries_are_summed_before_shares_are_computed():
    """A video filter over >CHUNK ids comes back as several partial breakdowns.
    Treating one chunk as the whole cohort would report a share of the wrong
    denominator — the reason aggregate_traffic exists at all."""
    rows = insights.aggregate_traffic([
        ("SHORTS", 600, 30), ("YT_SEARCH", 40, 4),      # chunk 1
        ("SHORTS", 300, 15), ("YT_SEARCH", 60, 6),      # chunk 2
    ])
    by_source = {r.source: r for r in rows}
    assert by_source["SHORTS"].views == 900
    assert by_source["YT_SEARCH"].views == 100
    assert by_source["SHORTS"].minutes == 45
    assert by_source["SHORTS"].share_pct == pytest.approx(90.0)
    assert by_source["YT_SEARCH"].share_pct == pytest.approx(10.0)


def test_traffic_rows_sort_by_views_then_name_for_a_stable_committed_csv():
    rows = insights.aggregate_traffic([
        ("YT_SEARCH", 10, 1), ("SHORTS", 90, 9), ("EXT_URL", 10, 1)])
    assert [r.source for r in rows] == ["SHORTS", "EXT_URL", "YT_SEARCH"]


def test_zero_view_scope_does_not_divide_by_zero():
    """A dead week returns real source rows with 0 views; the job must still
    write them rather than crash on the share denominator."""
    rows = insights.aggregate_traffic([("SHORTS", 0, 0), ("YT_SEARCH", 0, 0)])
    assert [r.share_pct for r in rows] == [0.0, 0.0]


def test_discovery_share_counts_only_sources_the_viewer_sought_out():
    """The R4.7 decision number: search/hashtag/external, not feed placement."""
    rows = insights.aggregate_traffic([
        ("SHORTS", 900, 45), ("YT_SEARCH", 60, 6),
        ("HASHTAGS", 30, 3), ("EXT_URL", 10, 1)])
    assert insights.discovery_share(rows) == pytest.approx(10.0)


def test_traffic_mix_line_collapses_the_long_tail_into_other():
    rows = insights.aggregate_traffic([
        ("SHORTS", 940, 47), ("YT_SEARCH", 34, 3), ("YT_CHANNEL", 11, 1),
        ("EXT_URL", 8, 1), ("SUBSCRIBER", 7, 1)])
    line = insights.format_traffic_mix(rows)
    assert line == "Shorts feed 94.0% · Search 3.4% · Channel pages 1.1% · other 1.5%"


def test_traffic_mix_drops_sub_one_percent_sources_from_the_named_list():
    rows = insights.aggregate_traffic([("SHORTS", 995, 50), ("YT_SEARCH", 5, 1)])
    assert insights.format_traffic_mix(rows) == "Shorts feed 99.5% · other 0.5%"


def test_unmapped_traffic_codes_survive_as_their_raw_enum():
    """YouTube adds source types; an unknown code must show up rather than be
    silently dropped or mislabelled."""
    rows = insights.aggregate_traffic([("SOME_NEW_SURFACE", 100, 10)])
    assert rows[0].label == "SOME_NEW_SURFACE"
    assert insights.format_traffic_mix(rows) == "SOME_NEW_SURFACE 100.0%"


def test_empty_traffic_result_reports_no_data_instead_of_a_blank_line():
    assert insights.format_traffic_mix([]) == "no data"


def test_second_weekly_append_extends_the_file_without_a_repeated_header():
    """The traffic CSV is appended to weekly and committed. Guards checked:
    header written once, prior rows untouched, LF endings kept, and the
    same-day guard refusing a double-append on a rerun."""
    import sys, pathlib, tempfile
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from scripts import weekly_analytics as wa

    class StubClient:
        """Mimics the one report shape R4.7 queries."""
        def reports(self): return self
        def query(self, **kw): self.kw = kw; return self
        def execute(self):
            return {"columnHeaders": [{"name": "insightTrafficSourceType"},
                                      {"name": "views"},
                                      {"name": "estimatedMinutesWatched"}],
                    "rows": [["SHORTS", 950, 48], ["YT_SEARCH", 50, 5]]}

    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d) / "traffic_sources.csv"
        orig_out, orig_scopes = wa.TRAFFIC_OUT, wa.traffic_scopes
        wa.TRAFFIC_OUT = out
        wa.traffic_scopes = lambda today: [("channel_7d", "2026-01-01", None)]
        try:
            wa.snapshot_traffic(StubClient(), "2026-09-07")
            assert not wa.already_snapshotted(out, "2026-09-14")
            wa.snapshot_traffic(StubClient(), "2026-09-14")
        finally:
            wa.TRAFFIC_OUT, wa.traffic_scopes = orig_out, orig_scopes

        raw = out.read_bytes()
        assert b"\r" not in raw
        lines = raw.decode().splitlines()
        assert lines[0].startswith("snapshot_date,")
        assert len(lines) == 5                       # header + 2 sources x 2 weeks
        assert lines[1] == "2026-09-07,channel_7d,SHORTS,950,48,95.00"
        assert lines[3] == "2026-09-14,channel_7d,SHORTS,950,48,95.00"
        assert wa.already_snapshotted(out, "2026-09-07")
        assert not wa.already_snapshotted(out, "2026-09-21")


# --- cohort splitting -------------------------------------------------------

def test_split_cohorts_excludes_unset_from_both_sides():
    """Fields are added to upload_log mid-history, so `!= value` used to sweep
    the entire pre-field past into the comparison cohort. `--compare
    candidate_rank=1` reported 24 vs 75 when the real contrast was 24 vs 3."""
    videos = [
        v("a", 5, candidate_rank="1"),
        v("b", 5, candidate_rank="1"),
        v("c", 5, candidate_rank="2"),
        v("old1", 40),           # logged before the field existed
        v("old2", 40),
    ]
    a, b, unset = insights.split_cohorts(videos, "candidate_rank", "1")
    assert [x.video_id for x in a] == ["a", "b"]
    assert [x.video_id for x in b] == ["c"]
    assert unset == 2


def test_split_cohorts_treats_whitespace_as_unset():
    a, b, unset = insights.split_cohorts([v("a", 5, topic="  ")], "topic", "nostalgia")
    assert (a, b, unset) == ([], [], 1)


# --- era rank correlation (analyze_channel) ---------------------------------

def _rank_correlation(*args, **kwargs):
    import importlib.util, pathlib, sys
    root = pathlib.Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "analyze_channel", root / "scripts" / "analyze_channel.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["analyze_channel"] = mod
    spec.loader.exec_module(mod)
    return mod.rank_correlation(*args, **kwargs)


def row(topic, residual, n=10):
    return {"topic": topic, "n": n, "median_residual": residual}


def test_rank_correlation_detects_a_preserved_ordering():
    a = [row("x", 0.9), row("y", 0.6), row("z", 0.3), row("w", 0.1)]
    b = [row("x", 0.5), row("y", 0.4), row("z", 0.2), row("w", -0.1)]
    rho, shared = _rank_correlation(a, b)
    assert len(shared) == 4
    assert rho == pytest.approx(1.0)


def test_rank_correlation_detects_a_reversed_ordering():
    a = [row("x", 0.9), row("y", 0.6), row("z", 0.3), row("w", 0.1)]
    b = [row("x", -0.4), row("y", -0.2), row("z", 0.3), row("w", 0.8)]
    rho, _ = _rank_correlation(a, b)
    assert rho == pytest.approx(-1.0)


def test_rank_correlation_drops_thin_buckets_and_refuses_when_too_few_remain():
    a = [row("x", 0.9), row("y", 0.6, n=1), row("z", 0.3), row("w", 0.1)]
    b = [row("x", 0.5), row("y", 0.4), row("z", 0.2), row("w", -0.1)]
    rho, shared = _rank_correlation(a, b)
    assert "y" not in shared           # thin in era a, so excluded
    assert rho is None                 # only 3 shared buckets left, under the floor
# --- zero-view age floor ----------------------------------------------------

def zv(vid, age_days, views=0, privacy="public"):
    return {"id": vid, "published": (NOW - datetime.timedelta(days=age_days)).isoformat(),
            "views": views, "privacy": privacy, "title": vid}


def test_fresh_zero_is_too_new_not_a_suppression_candidate():
    """A video hours old has no views yet and every neighbour is older, so it
    always looks isolated. The digest was fixed for this on 2026-08-23; the
    same trap sat in report.py --zeros until an upload 1.9h old was flagged."""
    vids = [zv(f"old{i}", 40 - i, views=50) for i in range(8)] + [zv("fresh", 0.08)]
    groups = insights.classify_zero_views(vids, NOW)
    assert [v["id"] for v in groups["too_new"]] == ["fresh"]
    assert groups["isolated"] == []


def test_aged_zero_among_healthy_neighbours_is_still_isolated():
    vids = [zv(f"old{i}", 40 - i, views=50) for i in range(8)] + [zv("dead", 20)]
    groups = insights.classify_zero_views(vids, NOW)
    assert [v["id"] for v in groups["isolated"]] == ["dead"]
    assert groups["too_new"] == []


# ---------------------------------------------------------- load_videos joins

class _FakeQuery:
    """Stands in for the Analytics reports().query() chain."""

    def __init__(self, rows):
        self._rows = rows

    def reports(self):
        return self

    def query(self, **kw):
        return self

    def execute(self):
        return {
            "columnHeaders": [{"name": n} for n in (
                "video", "views", "averageViewDuration",
                "averageViewPercentage", "likes", "comments")],
            "rows": self._rows,
        }


def _fake_analytics(monkeypatch, rows, privacy):
    from src import analytics
    monkeypatch.setattr(analytics, "youtube_analytics_client", lambda: _FakeQuery(rows))
    monkeypatch.setattr(analytics, "youtube_client", lambda: object())
    monkeypatch.setattr(analytics, "fetch_video_details",
                        lambda yt, ids, part=None: [
                            {"id": i, "status": {"privacyStatus": privacy.get(i, "public")}}
                            for i in ids])


def _write_log(tmp_path, monkeypatch, video_ids):
    from src import config
    path = tmp_path / "upload_log.csv"
    old = NOW - datetime.timedelta(days=30)
    with open(path, "w", newline="") as f:
        f.write("timestamp_utc,video_id,post_title,video_title,bg_clip\n")
        for vid in video_ids:
            f.write(f"{old.isoformat()},{vid},q,t,pexels_1.mp4\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", path)
    return path


def test_a_zero_view_upload_is_kept_not_silently_dropped(tmp_path, monkeypatch):
    """The Analytics API returns NO row for a 0-view video.

    The old code did `if not s: continue`, so those uploads vanished from every
    median and every zero count. On 2026-09-19 that hid both surviving
    confirmed-suppression cases (VDH3pSafyE0, _0MNAf8AzNg) — the entire evidence
    base for R4.6's skip categories — from the tool that answers "did X work?".
    """
    _write_log(tmp_path, monkeypatch, ["seen", "zeroed"])
    _fake_analytics(monkeypatch, rows=[["seen", 100, 12.0, 50.0, 1, 0]], privacy={})

    vids = insights.load_videos(now=NOW)

    assert {v.video_id for v in vids} == {"seen", "zeroed"}
    zero = next(v for v in vids if v.video_id == "zeroed")
    assert zero.views == 0
    assert zero.watch_seconds == 0


def test_a_privatised_upload_is_excluded_rather_than_counted_as_zero(tmp_path, monkeypatch):
    """Owner-privatised is not suppression — the distinction classify_zero_views
    already makes, now made here too. Counting them as zeros would invent
    suppression events."""
    _write_log(tmp_path, monkeypatch, ["seen", "hidden"])
    _fake_analytics(monkeypatch, rows=[["seen", 100, 12.0, 50.0, 1, 0]],
                    privacy={"hidden": "private"})

    vids = insights.load_videos(now=NOW)

    assert {v.video_id for v in vids} == {"seen"}


def test_dropping_zero_view_uploads_biases_medians_upward(tmp_path, monkeypatch):
    """Why this mattered beyond the zero count: the dropped rows are the worst
    performers by definition, so excluding them flatters every median."""
    _write_log(tmp_path, monkeypatch, ["a", "b", "c"])
    _fake_analytics(monkeypatch,
                    rows=[["a", 100, 10.0, 50.0, 1, 0], ["b", 100, 20.0, 50.0, 1, 0]],
                    privacy={})

    vids = insights.load_videos(now=NOW)
    watch = sorted(v.watch_seconds for v in vids)

    assert watch == [0.0, 10.0, 20.0]      # the zero is present
    assert insights.median(watch) == 10.0  # not 15.0, which is what dropping it gave


# ------------------------------------------- load_videos_offline (weekly snapshot)

def _write_offline(tmp_path, monkeypatch, uploads, snapshots):
    """uploads: [(video_id, published)] · snapshots: [(date, video_id, views, watch)]"""
    from src import config
    log = tmp_path / "upload_log.csv"
    with open(log, "w", newline="") as f:
        f.write("timestamp_utc,video_id,post_title,video_title,bg_clip\n")
        for vid, published in uploads:
            f.write(f"{published.isoformat()},{vid},q,t,pexels_1.mp4\n")
    snap = tmp_path / "analytics_snapshots.csv"
    with open(snap, "w", newline="") as f:
        f.write("snapshot_date,video_id,published_at,views,likes,comments,shares,"
                "est_minutes_watched,avg_view_duration_s,avg_view_pct\n")
        for date, vid, views, watch in snapshots:
            f.write(f"{date},{vid},,{views},0,0,0,0,{watch},50\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", log)
    monkeypatch.setattr(config, "ANALYTICS_SNAPSHOTS", snap)


def test_offline_uploads_newer_than_the_snapshot_are_unmeasured_not_zero(
        tmp_path, monkeypatch):
    """The snapshot runs weekly and the channel uploads twice a day, so ~14
    logged uploads always postdate it. Scoring them 0 would manufacture a
    fortnight of suppression events — the 2026-08-23 digest false positive,
    exactly."""
    old = NOW - datetime.timedelta(days=30)
    fresh = NOW - datetime.timedelta(days=1)          # after the snapshot below
    _write_offline(
        tmp_path, monkeypatch,
        uploads=[("measured", old), ("fresh", fresh)],
        snapshots=[("2026-08-20", "measured", 100, 12.0)],
    )

    load = insights.load_videos_offline()

    assert [v.video_id for v in load.videos] == ["measured"]
    assert load.too_new == ["fresh"]
    assert load.absent == []
    assert any("NOT counted as zero-view" in c for c in load.caveats())


def test_offline_zero_view_rows_are_kept_as_genuine_zeros(tmp_path, monkeypatch):
    """A row that IS in the snapshot with 0 views is real: weekly_analytics writes
    one row per channel video and defaults a missing Analytics row to 0. Dropping
    these would re-lose the suppression evidence load_videos was fixed to keep."""
    old = NOW - datetime.timedelta(days=30)
    _write_offline(
        tmp_path, monkeypatch,
        uploads=[("seen", old), ("zeroed", old)],
        snapshots=[("2026-08-20", "seen", 100, 12.0), ("2026-08-20", "zeroed", 0, 0.0)],
    )

    load = insights.load_videos_offline()

    assert {v.video_id for v in load.videos} == {"seen", "zeroed"}
    assert load.too_new == []


def test_offline_ages_are_measured_at_the_snapshot_not_today(tmp_path, monkeypatch):
    """The metrics froze when the snapshot ran. A video published the day before
    it had one day to earn them, however old it is now — so MIN_AGE_DAYS has to
    bite against the snapshot date, and callers must age-match against `asof`."""
    old = NOW - datetime.timedelta(days=30)
    young_at_snapshot = datetime.datetime(2026, 8, 19, tzinfo=datetime.timezone.utc)
    _write_offline(
        tmp_path, monkeypatch,
        uploads=[("measured", old), ("young", young_at_snapshot)],
        snapshots=[("2026-08-20", "measured", 100, 12.0),
                   ("2026-08-20", "young", 0, 0.0)],
    )

    load = insights.load_videos_offline()

    # "young" is 4 days old today but was 1 day old when measured -> excluded.
    assert [v.video_id for v in load.videos] == ["measured"]
    assert load.asof == datetime.datetime(2026, 8, 20, tzinfo=datetime.timezone.utc)


def test_offline_reads_the_newest_snapshot_per_video(tmp_path, monkeypatch):
    """The file is an append-only weekly series; stale rows must not win."""
    old = NOW - datetime.timedelta(days=30)
    _write_offline(
        tmp_path, monkeypatch,
        uploads=[("measured", old)],
        snapshots=[("2026-08-13", "measured", 50, 6.0),
                   ("2026-08-20", "measured", 100, 12.0)],
    )

    load = insights.load_videos_offline()

    assert load.videos[0].views == 100
    assert load.videos[0].watch_seconds == 12.0


def test_offline_flags_an_older_upload_missing_from_the_snapshot(tmp_path, monkeypatch):
    """Absent-but-old means it left the channel (deleted, or never in the uploads
    playlist) — a different thing from too-new, and worth saying out loud rather
    than folding into the benign bucket."""
    old = NOW - datetime.timedelta(days=30)
    _write_offline(
        tmp_path, monkeypatch,
        uploads=[("measured", old), ("vanished", old)],
        snapshots=[("2026-08-20", "measured", 100, 12.0)],
    )

    load = insights.load_videos_offline()

    assert load.absent == ["vanished"]
    assert load.too_new == []
    assert any(c.startswith("WARNING") for c in load.caveats())


def test_offline_always_states_the_privacy_blind_spot(tmp_path, monkeypatch):
    """The snapshot records no privacy status, so a privatised upload reads as
    zero-view here while load_videos excludes it. Bounded and stated, never
    silent — a half-right offline path is worse than none."""
    old = NOW - datetime.timedelta(days=30)
    _write_offline(tmp_path, monkeypatch, uploads=[("measured", old)],
                   snapshots=[("2026-08-20", "measured", 100, 12.0)])

    caveats = insights.load_videos_offline().caveats()

    assert any("privacy" in c for c in caveats)
    assert any("as of 2026-08-20" in c for c in caveats)


def test_offline_with_no_snapshot_file_reports_rather_than_crashes(tmp_path, monkeypatch):
    from src import config
    monkeypatch.setattr(config, "ANALYTICS_SNAPSHOTS", tmp_path / "missing.csv")
    monkeypatch.setattr(config, "UPLOAD_LOG", tmp_path / "missing_log.csv")

    load = insights.load_videos_offline()

    assert load.videos == [] and load.asof is None
    assert load.caveats() == ["no analytics snapshot on disk — nothing to report"]

