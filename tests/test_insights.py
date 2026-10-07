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


def test_buried_uploads_counted_including_zero_views():
    """The retired clip (PRD §0 #11) had a normal median but half its uploads
    barely shown; the count is what exposes that."""
    videos = cohort(6, 7, "ok", views=100) + cohort(3, 7, "low", views=4) + [
        v("edge", 7, views=insights.BURIED_VIEWS), v("zero", 7, views=0)]
    c = insights.summarize(videos, "clip", Metric.VIEWS, NOW)
    assert c.buried_count == 5
    assert c.median == 100.0         # the median alone looks normal


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



# ------------------------------- the auto-revert check (issue #16, /shift §5)
#
# The guardrail that substitutes for owner review of every merge says a release
# that degraded watch-seconds or views gets reverted. It never once produced a
# verdict: a release applies to every upload after it and none before, so its
# cohorts differ in age *by construction* and `compare` correctly refuses them.
# Reading each upload at the same age, from the weekly snapshot series, is what
# makes the comparison possible at all. These pin that.

def _write_series(tmp_path, monkeypatch, uploads, snapshots):
    """uploads: [(video_id, published, format_version)]
    snapshots: [(date, video_id, views, watch)]"""
    from src import config
    log = tmp_path / "upload_log.csv"
    with open(log, "w", newline="") as f:
        f.write("timestamp_utc,video_id,post_title,video_title,bg_clip,format_version\n")
        for vid, published, fv in uploads:
            f.write(f"{published.isoformat()},{vid},q,t,pexels_1.mp4,{fv}\n")
    snap = tmp_path / "analytics_snapshots.csv"
    with open(snap, "w", newline="") as f:
        f.write("snapshot_date,video_id,published_at,views,likes,comments,shares,"
                "est_minutes_watched,avg_view_duration_s,avg_view_pct\n")
        for date, vid, views, watch in snapshots:
            f.write(f"{date},{vid},,{views},0,0,0,0,{watch},50\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", log)
    monkeypatch.setattr(config, "ANALYTICS_SNAPSHOTS", snap)


def _era(prefix, start_day, n, fv, views, watch, snapshot_gap=7):
    """n uploads from 2026-07-`start_day`, each with a snapshot `snapshot_gap`
    days later — i.e. every one of them measured at the same age."""
    uploads, snaps = [], []
    for i in range(n):
        published = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc) \
            + datetime.timedelta(days=start_day + i)
        uploads.append((f"{prefix}{i}", published, fv))
        snaps.append(((published + datetime.timedelta(days=snapshot_gap)).date().isoformat(),
                      f"{prefix}{i}", views, watch))
    return uploads, snaps


def _two_eras(tmp_path, monkeypatch, new_views=200, new_watch=10.0,
              old_views=200, old_watch=10.0, n=10):
    old_u, old_s = _era("old", 0, n, "v4", old_views, old_watch)
    new_u, new_s = _era("new", 60, n, "v5", new_views, new_watch)
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)


def _verdict(version="v5", key="format_version"):
    load = insights.load_videos_at_age()
    a, b, unset, later = insights.release_cohorts(load.videos, key, version)
    comparisons = [insights.compare(a, b, "release", "before", load.anchor, m)
                   for m in (Metric.WATCH, Metric.VIEWS)]
    return insights.release_verdict(comparisons), comparisons


def test_a_release_becomes_age_matched_when_read_at_a_common_age(tmp_path, monkeypatch):
    """The whole point. Two eras two months apart are un-comparable today, and
    perfectly comparable at seven days old."""
    _two_eras(tmp_path, monkeypatch)
    verdict, comparisons = _verdict()
    assert all(c.age_matched for c in comparisons)
    assert verdict == "KEEP — watch_seconds did not degrade beyond the channel's own drift"


def test_a_release_below_its_committed_size_gets_no_verdict(tmp_path, monkeypatch):
    """v7 commits to 20 uploads; at 8 aged the module's floor is met, and it
    would have answered on 8 (2026-09-29)."""
    _two_eras(tmp_path, monkeypatch, n=10)
    _, comparisons = _verdict()
    assert insights.release_verdict(comparisons, min_uploads=20) == (
        "NO VERDICT — 10 measurable release uploads, the rule commits to 20; bake longer")
    assert insights.release_verdict(comparisons, min_uploads=10).startswith("KEEP")


def test_a_release_that_degraded_watch_seconds_is_reverted(tmp_path, monkeypatch):
    _two_eras(tmp_path, monkeypatch, new_watch=6.0, old_watch=10.0)
    verdict, _ = _verdict()
    assert verdict == "REVERT — watch_seconds degraded beyond the channel's own drift"


def test_an_interleaved_field_is_age_matched_when_read_at_a_common_age(tmp_path, monkeypatch):
    """`report.py --at-age 7 --compare topic=…`. One snapshot of today read the
    recent-heavy dark-morbid cohort 11d old against 17d for the rest, and
    compare refused it; read at a common age the same uploads compare."""
    x_u, x_s = _era("x", 0, 10, "x", 200, 14.0)
    y_u, y_s = _era("y", 20, 10, "y", 200, 11.0)
    _write_series(tmp_path, monkeypatch, x_u + y_u, x_s + y_s)
    load = insights.load_videos_at_age()
    a, b, unset = insights.split_cohorts(load.videos, "format_version", "x")
    c = insights.compare(a, b, "x", "not x", load.anchor, Metric.WATCH)
    assert (len(a), len(b), unset) == (10, 10, 0)
    assert c.age_matched


def test_upload_slot_is_derived_from_the_log_timestamp():
    """Research row R3. The runs drift within a slot, so noon is the split."""
    slot = lambda ts: insights._with_derived_dimensions({"timestamp_utc": ts})["slot"]
    assert slot("2026-09-24T05:03:08+00:00") == "morning"
    assert slot("2026-09-24T01:40:00+00:00") == "morning"
    assert slot("2026-09-24T17:20:09+00:00") == "evening"
    assert slot("2026-09-24T12:05:00+00:00") == "evening"
    assert slot("") == ""


def test_question_length_splits_at_the_logged_median():
    """Research row R2: do shorter questions hold viewers longer under v7?"""
    length = lambda q: insights._with_derived_dimensions({"post_title": q})["question_length"]
    assert length("x" * 63) == "short"
    assert length("x" * 64) == "long"
    assert length("") == ""


def test_question_person_marks_questions_that_address_the_viewer():
    """Does a narrated opening that says "you" hold viewers longer?"""
    person = lambda q: insights._with_derived_dimensions({"post_title": q})["question_person"]
    assert person("What's something you can't prove?") == "you"
    assert person("What's your best one-liner?") == "you"
    assert person("You're a billionaire. Now what?") == "you"
    assert person("Which famous person died in the dumbest way?") == "other"
    assert person("What happened to young people's hobbies?") == "other"
    assert person("") == ""


def test_title_source_marks_uploads_that_shipped_the_raw_question():
    """Research row R2: does a failed title cost watch-seconds?"""
    source = lambda q, t: insights._with_derived_dimensions(
        {"post_title": q, "video_title": t})["title_source"]
    assert source("What is it?", " What is it? ") == "raw"
    assert source("What is it?", "You Won't Believe It!") == "generated"
    assert source("What is it?", "") == ""


def test_title_length_splits_at_the_generated_median():
    """Is title length, not title source, behind raw titles' views gap?"""
    length = lambda t: insights._with_derived_dimensions({"video_title": t})["title_length"]
    assert length("x" * 41) == "short"
    assert length(" " + "x" * 42) == "long"
    assert length("") == ""


def test_within_keeps_one_group_so_a_comparison_can_be_read_inside_it():
    """Research row R2: question length within similar-length videos."""
    rows = [{"post_title": "q", "duration_s": d} for d in ("18.0", "20.0", "24.5", "")]
    videos = [insights.Video(video_id=str(i), published=None, views=0, watch_seconds=0,
                             avg_view_pct=0, likes=0, comments=0,
                             meta=insights._with_derived_dimensions(r))
              for i, r in enumerate(rows)]
    assert [v.video_id for v in insights.within(videos, "video_length=short")] == ["0", "1"]
    assert [v.video_id for v in insights.within(videos, "video_length=long")] == ["2"]


def test_a_release_that_shifts_video_length_says_so():
    """R2: the b-roll switch moved median length 19.3s -> 20.4s, and longer
    videos hold more watch-seconds, so the verdict line must carry it."""
    mk = lambda d: insights.Video(video_id="v", published=None, views=0, watch_seconds=0,
                                  avg_view_pct=0, likes=0, comments=0, meta={"duration_s": d})
    assert "SHIFTED" in insights.render_duration([mk("20.4")], [mk("19.3")])
    assert "SHIFTED" not in insights.render_duration([mk("20.4")], [mk("20.3")])
    assert "not measurable" in insights.render_duration([mk("")], [mk("20.3")])


def _write_series_with_length(tmp_path, monkeypatch, eras):
    """eras: [(prefix, start_day, fv, [(duration_s, watch), ...])], each upload
    snapshotted at 7 days old."""
    from src import config
    log, snap = tmp_path / "upload_log.csv", tmp_path / "analytics_snapshots.csv"
    with open(log, "w", newline="") as lf, open(snap, "w", newline="") as sf:
        lf.write("timestamp_utc,video_id,post_title,video_title,bg_clip,format_version,duration_s\n")
        sf.write("snapshot_date,video_id,published_at,views,likes,comments,shares,"
                 "est_minutes_watched,avg_view_duration_s,avg_view_pct\n")
        for prefix, start_day, fv, uploads in eras:
            for i, (dur, watch) in enumerate(uploads):
                published = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc) \
                    + datetime.timedelta(days=start_day + i)
                lf.write(f"{published.isoformat()},{prefix}{i},q,t,pexels_1.mp4,{fv},{dur}\n")
                seen = (published + datetime.timedelta(days=7)).date().isoformat()
                sf.write(f"{seen},{prefix}{i},,200,0,0,0,0,{watch},50\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", log)
    monkeypatch.setattr(config, "ANALYTICS_SNAPSHOTS", snap)


def test_a_length_shifted_release_is_credited_only_within_each_length_half(tmp_path, monkeypatch):
    """v7 (2026-10-07): its posts ran 3s longer and it read +25%, +8% within
    long videos. Longer videos hold more seconds, so a release made only of
    longer videos looks better overall while matching the era in each half."""
    old = [("15.0", 9.0)] * 10 + [("25.0", 12.0)] * 10
    new = [("15.0", 9.0)] * 2 + [("25.0", 12.0)] * 18
    _write_series_with_length(tmp_path, monkeypatch,
                              [("old", 0, "v4", old), ("new", 60, "v5", new)])
    read = insights.release_read("v5")
    assert read.comparisons[0].delta > 0.1          # the headline credits length
    out = insights.render_within_length(read)
    assert "attribution only, never a trigger" in out
    assert "insufficient data" in out               # short half: 2 uploads
    assert "long vs before, long -> no material difference" in out


def test_no_within_length_read_when_length_held(tmp_path, monkeypatch):
    same = [("15.0", 9.0)] * 10 + [("25.0", 12.0)] * 10
    _write_series_with_length(tmp_path, monkeypatch,
                              [("old", 0, "v4", same), ("new", 60, "v5", same)])
    assert insights.render_within_length(insights.release_read("v5")) == ""


def test_a_release_that_shifts_length_must_also_hold_total_watch_time():
    """The owner on #39: longer videos gain watch-seconds and lose views, so a
    release that only lengthens them would read "keep" on watch-seconds alone."""
    from types import SimpleNamespace as NS
    mk = lambda d: insights.Video(video_id="v", published=None, meta={"duration_s": d})
    assert insights.release_triggers([mk("20.4")], [mk("20.3")]) == (Metric.WATCH,)
    triggers = insights.release_triggers([mk("22.0")], [mk("20.0")])
    assert triggers == (Metric.WATCH, Metric.TOTAL)

    side = NS(sufficient=True)
    cmp = lambda m, d: NS(metric=m, delta=d, a=side, b=side, age_matched=True)
    comparisons = [cmp(Metric.WATCH, 0.20), cmp(Metric.VIEWS, -0.30), cmp(Metric.TOTAL, -0.15)]
    floors = {Metric.WATCH: 0.1, Metric.VIEWS: 0.5, Metric.TOTAL: 0.1}
    assert insights.release_verdict(comparisons, floors).startswith("KEEP")
    assert insights.release_verdict(comparisons, floors, triggers) == (
        "REVERT — total_watch_s degraded beyond the channel's own drift")
    assert insights.release_verdict(comparisons[:2], floors, triggers) == (
        "NO VERDICT — total_watch_s was not compared")


def test_an_early_read_is_never_correlated_with_itself(tmp_path, monkeypatch):
    """R3. One snapshot at age 5 matches both 3 and 7 days within tolerance;
    pairing it with itself would report a perfect correlation."""
    base = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc)
    uploads, snaps = [], []
    for i in range(6):
        published = base + datetime.timedelta(days=i * 10)
        uploads.append((f"v{i}", published, "v6"))
        for age, watch in ((2, 5.0 + i), (9, 10.0 + i)):   # two snapshots, same order
            snaps.append(((published + datetime.timedelta(days=age)).date().isoformat(),
                          f"v{i}", 100, watch))
    uploads.append(("same", base + datetime.timedelta(days=70), "v6"))
    snaps.append(((base + datetime.timedelta(days=75)).date().isoformat(), "same", 100, 9.0))
    _write_series(tmp_path, monkeypatch, uploads, snaps)
    n, rho = insights.early_read_stability(3, 7)
    assert n == 6 and rho == pytest.approx(1.0)


def test_total_watch_is_views_times_watch_seconds():
    """R2: longer videos hold more seconds but may draw fewer views."""
    v = Video(video_id="v", published=None, views=120, watch_seconds=11.0)
    assert v.get(Metric.TOTAL) == 1320.0


def test_views_alone_never_trigger_a_revert(tmp_path, monkeypatch):
    """The owner on #18: "the rule now triggers on watch-seconds only, with
    views reported but never firing it". Until 2026-09-24 this tool still
    applied the old either-metric rule and printed REVERT for the b-roll
    library on views alone, which would have done the same to v7."""
    _two_eras(tmp_path, monkeypatch, new_views=100, old_views=200)
    verdict, _ = _verdict()
    assert verdict == "KEEP — watch_seconds did not degrade beyond the channel's own drift"


def test_a_verdict_needs_the_trigger_metric_compared():
    assert insights.release_verdict([]).startswith("NO VERDICT")


def test_a_release_too_young_to_judge_says_so_instead_of_nothing(tmp_path, monkeypatch):
    """Four releases shipped under a guardrail that returned nothing at all,
    which read like approval. A refusal has to be loud."""
    _two_eras(tmp_path, monkeypatch, n=4)
    verdict, _ = _verdict()
    assert verdict.startswith("NO VERDICT")
    assert "bake longer" in verdict


def test_uploads_not_yet_old_enough_are_unmeasured_never_zero(tmp_path, monkeypatch):
    """Same trap as the offline loader: the ~14 uploads too young to have
    reached the age must not be scored zero, which would invent suppression."""
    old_u, old_s = _era("old", 0, 10, "v4", 200, 10.0)
    new_u, new_s = _era("new", 60, 10, "v5", 200, 10.0)
    baby = (datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc)
            + datetime.timedelta(days=80))
    _write_series(tmp_path, monkeypatch, old_u + new_u + [("baby", baby, "v5")],
                  old_s + new_s)

    load = insights.load_videos_at_age()

    assert load.not_yet == ["baby"]
    assert "baby" not in {v.video_id for v in load.videos}
    assert any("NOT counted as zero-view" in c for c in load.caveats())


def test_uploads_predating_the_snapshot_series_are_excluded_not_zero(tmp_path, monkeypatch):
    old_u, old_s = _era("old", 0, 10, "v4", 200, 10.0)
    new_u, new_s = _era("new", 60, 10, "v5", 200, 10.0)
    ancient = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
    _write_series(tmp_path, monkeypatch, old_u + new_u + [("ancient", ancient, "v1")],
                  old_s + new_s)

    load = insights.load_videos_at_age()

    assert load.no_coverage == ["ancient"]
    assert any("predate the weekly series" in c for c in load.caveats())


def test_the_baseline_is_what_the_release_replaced_not_its_successors(tmp_path, monkeypatch):
    """`split_cohorts` would fold a later version into the baseline, quietly
    changing the question from "was this worse than what it replaced?" to
    something no rule asks."""
    old_u, old_s = _era("old", 0, 10, "v4", 200, 10.0)
    mid_u, mid_s = _era("mid", 60, 10, "v5", 200, 10.0)
    new_u, new_s = _era("new", 120, 10, "v6", 20, 1.0)   # a disaster, after v5
    _write_series(tmp_path, monkeypatch, old_u + mid_u + new_u, old_s + mid_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, later = insights.release_cohorts(load.videos, "format_version", "v5")

    assert later == 10
    assert {x.meta["format_version"] for x in b} == {"v4"}
    assert insights.release_verdict(
        [insights.compare(a, b, "r", "p", load.anchor, m)
         for m in (Metric.WATCH, Metric.VIEWS)]).startswith("KEEP")


def test_only_one_snapshot_per_upload_is_used(tmp_path, monkeypatch):
    """A video has ten weekly rows and must contribute exactly one, or it skews
    its own cohort's median. The window is half the weekly cadence, so only one
    row can ever fall inside it — and if the cadence ever changed, the row
    nearest the target age wins rather than the first one seen."""
    published = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc)
    _write_series(
        tmp_path, monkeypatch, [("a", published, "v5")],
        snapshots=[("2026-07-05", "a", 100, 9.0),    # age 4 — inside
                   ("2026-07-08", "a", 400, 11.0),   # age 7 — inside and nearer
                   ("2026-07-12", "a", 900, 12.0),   # age 11 — outside
                   ("2026-07-19", "a", 1600, 13.0)])

    load = insights.load_videos_at_age()

    assert [x.video_id for x in load.videos] == ["a"]
    assert load.videos[0].views == 400


def test_synthetic_publish_dates_never_leak_as_real_ones(tmp_path, monkeypatch):
    """`published` is rewritten so the existing age rules work unchanged. Any
    code that needs the real date must reach for `true_published`."""
    _two_eras(tmp_path, monkeypatch)
    load = insights.load_videos_at_age()
    assert all(x.true_published is not None for x in load.videos)
    assert all(abs(x.age_days(load.anchor) - insights.AGE_MATCH_TARGET_DAYS) <= 3.5
               for x in load.videos)


def test_no_snapshot_series_reports_rather_than_crashes(tmp_path, monkeypatch):
    from src import config
    monkeypatch.setattr(config, "ANALYTICS_SNAPSHOTS", tmp_path / "missing.csv")
    monkeypatch.setattr(config, "UPLOAD_LOG", tmp_path / "missing_log.csv")

    load = insights.load_videos_at_age()

    assert load.videos == [] and load.anchor is None
    assert insights.release_verdict([]) == "NO VERDICT — nothing to compare"


# --- the detection limit: age-matching does not remove the calendar confound -

def _noisy_era(prefix, start_day, n, fv, view_cycle, watch=10.0):
    """An era whose views swing between blocks with nothing changing."""
    uploads, snaps = [], []
    for i in range(n):
        published = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc) \
            + datetime.timedelta(days=start_day + i)
        uploads.append((f"{prefix}{i}", published, fv))
        snaps.append(((published + datetime.timedelta(days=7)).date().isoformat(),
                      f"{prefix}{i}", view_cycle[(i // 8) % len(view_cycle)], watch))
    return uploads, snaps


def test_a_drop_inside_the_channels_own_drift_is_not_a_revert(tmp_path, monkeypatch):
    """Run against live data, the first version of this check ordered reverting
    both `v5` and the b-roll library on views drops of 50% and 39% — while
    median day-7 views moved 82 -> 228 -> 114 -> 62 by half-month with the
    format unchanged for most of it. A guardrail that fires on the weather
    reverts good work."""
    old_u, old_s = _noisy_era("old", 0, 32, "v4", [400, 100, 400, 100])
    new_u, new_s = _era("new", 60, 16, "v5", 200, 10.0)   # mid-range, no real change
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")
    comparisons = [insights.compare(a, b, "r", "p", load.anchor, m)
                   for m in (Metric.WATCH, Metric.VIEWS)]
    floors = {m: insights.drift_floor(b, m) for m in (Metric.WATCH, Metric.VIEWS)}

    assert floors[Metric.VIEWS] > 0.5          # the era swings 4x on its own
    assert insights.release_verdict(comparisons, floors).startswith("KEEP")


def test_a_drop_larger_than_the_drift_still_reverts(tmp_path, monkeypatch):
    """The floor must not defang the rule: a degradation bigger than the
    channel's own movement is exactly what it exists to catch."""
    old_u, old_s = _noisy_era("old", 0, 32, "v4", [220, 200, 220, 200])
    new_u, new_s = _era("new", 60, 16, "v5", 210, 5.0)   # watch-seconds halved
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")
    comparisons = [insights.compare(a, b, "r", "p", load.anchor, m)
                   for m in (Metric.WATCH, Metric.VIEWS)]
    floors = {m: insights.drift_floor(b, m) for m in (Metric.WATCH, Metric.VIEWS)}

    assert floors[Metric.WATCH] < 0.2
    assert insights.release_verdict(comparisons, floors) == (
        "REVERT — watch_seconds degraded beyond the channel's own drift")


def test_a_views_drop_beyond_its_limit_is_printed_but_does_not_fire(tmp_path, monkeypatch):
    """Reported, never a trigger: the drop must still be on screen."""
    old_u, old_s = _noisy_era("old", 0, 32, "v4", [220, 200, 220, 200])
    new_u, new_s = _era("new", 60, 16, "v5", 40, 10.0)   # views collapse, watch holds
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")
    metrics = (Metric.WATCH, Metric.VIEWS)
    comparisons = [insights.compare(a, b, "r", "p", load.anchor, m) for m in metrics]
    floors = {m: insights.drift_floor(b, m) for m in metrics}
    out = insights.render_release(comparisons, floors)

    assert insights.release_verdict(comparisons, floors).startswith("KEEP")
    assert "NOT A TRIGGER: views" in out and "#18" in out


def test_the_drift_floor_is_measured_before_the_change_not_on_it(tmp_path, monkeypatch):
    """Measuring it on the release's own uploads would let a volatile release
    excuse its own regression."""
    old_u, old_s = _era("old", 0, 24, "v4", 200, 10.0)                 # steady
    new_u, new_s = _noisy_era("new", 60, 24, "v5", [20, 900, 20, 900])  # wild
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")

    assert insights.drift_floor(b, Metric.VIEWS) == 0      # the steady era
    assert insights.drift_floor(a, Metric.VIEWS) > 1       # would have hidden anything


def test_drift_floor_is_unmeasurable_rather_than_zero_on_thin_history():
    """None means "cannot tell"; 0 would mean "this channel never moves" and
    would wave every drop through as significant."""
    assert insights.drift_floor([], Metric.VIEWS) is None
    assert insights.drift_floor(
        [v(f"a{i}", 10, views=100) for i in range(9)], Metric.VIEWS) is None


def test_alternation_floor_sees_a_day_parity_gap_and_ignores_a_calendar_trend():
    """The design it measures: halves split by alternate days share the
    calendar. A steady trend moves both halves together, so it reads as no
    noise; a gap between odd and even days is exactly what it reports."""
    # Two uploads a day for 16 days. Even age offsets get 12s, odd get 10s.
    parity = [v(f"p{d}{k}", 30 - d, watch=12.0 if d % 2 else 10.0)
              for d in range(16) for k in range(2)]
    assert 0.16 < insights.alternation_floor(parity, Metric.WATCH) <= 0.2   # 2s on 10 or 12
    trend = [v(f"t{d}{k}", 30 - d, watch=10.0 + d) for d in range(16) for k in range(2)]
    assert insights.alternation_floor(trend, Metric.WATCH) < insights.drift_floor(trend, Metric.WATCH)
    assert insights.alternation_floor(parity[:15], Metric.WATCH) is None


def test_the_detection_limit_is_printed_with_every_release_answer(tmp_path, monkeypatch):
    """A verdict without its detection limit invites reading "KEEP" as "proven
    safe" — on views, this channel cannot prove anything under ~50%."""
    _two_eras(tmp_path, monkeypatch)
    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")
    comparisons = [insights.compare(a, b, "r", "p", load.anchor, m)
                   for m in (Metric.WATCH, Metric.VIEWS)]
    out = insights.render_release(comparisons, {m: insights.drift_floor(b, m)
                                                for m in (Metric.WATCH, Metric.VIEWS)})
    assert out.count("detection limit") == 2
    assert "/shift §5" in out


def test_metrics_pointing_opposite_ways_are_called_out_not_flattened(tmp_path, monkeypatch):
    """The b-roll library, live: watch-seconds +22% (limit 11%) and views -39%
    (limit 38%). The verdict follows watch-seconds (#18) and reads KEEP, but
    the views drop has to stay on screen or the one-line verdict misleads."""
    old_u, old_s = _era("old", 0, 24, "v4", 200, 6.0)
    new_u, new_s = _era("new", 60, 24, "v5", 100, 12.0)   # views halved, watch doubled
    _write_series(tmp_path, monkeypatch, old_u + new_u, old_s + new_s)

    load = insights.load_videos_at_age()
    a, b, _, _ = insights.release_cohorts(load.videos, "format_version", "v5")
    metrics = (Metric.WATCH, Metric.VIEWS)
    comparisons = [insights.compare(a, b, "r", "p", load.anchor, m) for m in metrics]
    out = insights.render_release(comparisons, {m: insights.drift_floor(b, m)
                                                for m in metrics})

    assert "CONFLICT" in out and "NOT A TRIGGER: views" in out
    assert "KEEP" in out and "REVERT" not in out


# ------------------------------------------------------------ trajectory

def _snap(vid, published_day, snapshot_day, value):
    base = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc)
    return {"video_id": vid,
            "published": base + datetime.timedelta(days=published_day),
            "snapshot": base + datetime.timedelta(days=snapshot_day),
            "value": value}


def test_trajectory_reads_every_upload_at_the_same_age():
    """The point of the measure: months become comparable.

    A July upload read at 7 days must sit alongside a September one read at 7
    days, not at 60. Without that, every trend is really an age trend.
    """
    # All six inside one ISO week — 2026-07-01 is a Wednesday, so spreading
    # them over six days would straddle the boundary and split the bucket.
    rows = []
    for i in range(6):
        rows.append(_snap(f"a{i}", 0, 7, 10.0 + i * 0))     # read at 7d
        rows.append(_snap(f"a{i}", 0, 60, 40.0))            # and much later
    series = insights.trajectory(rows)
    assert len(series) == 1
    _, n, med = series[0]
    assert n == 6
    assert med == 10.0          # the 7-day reading, not the 60-day one


def test_trajectory_skips_periods_too_thin_to_report():
    """Two uploads is not a week's worth; reporting it invites noise-chasing."""
    rows = [_snap("a", 0, 7, 10.0), _snap("b", 1, 8, 30.0)]
    assert insights.trajectory(rows) == []


def test_flat_is_detected_against_the_channels_own_drift():
    """The actionable verdict. A 1s wobble inside normal weather is NOT
    progress, and calling it progress is how a flatlining channel looks fine.
    """
    series = [(f"w{i}", 10, v) for i, v in enumerate([10.0, 11.0, 10.0, 11.0, 10.0, 11.0])]
    verdict, why = insights.trajectory_verdict(series, floor=2.0)
    assert verdict == "flat", why


def test_real_movement_is_not_dismissed_as_drift():
    series = [(f"w{i}", 10, v) for i, v in enumerate([8.0, 8.0, 8.0, 14.0, 14.0, 14.0])]
    verdict, _ = insights.trajectory_verdict(series, floor=2.0)
    assert verdict == "rising"


def test_a_decline_is_reported_as_falling():
    series = [(f"w{i}", 10, v) for i, v in enumerate([14.0, 14.0, 14.0, 8.0, 8.0, 8.0])]
    verdict, _ = insights.trajectory_verdict(series, floor=2.0)
    assert verdict == "falling"


def test_too_little_history_says_unknown_rather_than_guessing():
    series = [(f"w{i}", 10, 10.0) for i in range(3)]
    verdict, _ = insights.trajectory_verdict(series, floor=1.0)
    assert verdict == "unknown"


def _week_of_uploads(start_day, snapshot_day, views, vid="v"):
    """One upload a day for a week, all read by one snapshot."""
    return [_snap(f"{vid}{i}", start_day + i, snapshot_day, v)
            for i, v in enumerate(views)]


def test_weekly_totals_sum_every_upload_including_zero_views():
    """Bet 2 is a total: a zero-view upload is still part of the week, and a
    median would hide both a lost upload and an added one."""
    # 2026-07-06 is a Monday (day 5); a snapshot on day 16 reads the week's
    # uploads at 5-11 days old, all within 4 of 7.
    rows = _week_of_uploads(5, 16, [10, 0, 20, 30, 40, 50, 60])
    rows += _week_of_uploads(5, 24, [99] * 7)          # later readings ignored
    series = insights.weekly_totals(rows)
    assert series == [("2026-W28", 7, 210)]


def test_weekly_totals_leave_out_a_week_still_filling_in():
    """A week whose Sunday upload is too young to read would report low."""
    rows = _week_of_uploads(5, 13, [10] * 7)    # Sunday's upload is 2 days old
    assert insights.weekly_totals(rows) == []


def test_weekly_totals_leave_out_a_week_the_snapshots_never_read():
    """Uploads from before the first snapshot appear only at 30+ days old;
    the week is known but unread, so it is left out rather than summed low."""
    rows = _week_of_uploads(5, 45, [10] * 7)
    rows += [_snap("late", 11, 18, 5)]           # its Sunday upload, read at 7 days
    assert insights.weekly_totals(rows) == []


def test_views_concentration_reads_each_upload_once_at_the_same_age():
    """The top tenth's share of the views, zeros included, from the 7-day
    reading only: a later lifetime count would credit the oldest uploads."""
    rows = _week_of_uploads(5, 16, [0, 10, 10, 10, 10, 10, 10], vid="a")
    rows += _week_of_uploads(12, 23, [10, 10, 900], vid="b")
    rows += _week_of_uploads(5, 60, [5000] * 7, vid="a")    # long after 7 days
    n, total, top_n, top_total, biggest = insights.views_concentration(rows)
    assert (n, total, top_n, top_total, biggest) == (10, 980, 1, 900, 900)


def test_views_concentration_refuses_a_thin_cohort():
    rows = _week_of_uploads(5, 16, [10] * 7)
    assert insights.views_concentration(rows) is None


def test_hit_rates_count_the_top_tenth_per_group_against_the_rest():
    """R5: a hit is a top-10% upload by views; each group is tested against
    every other upload, and zero-view uploads count in n but never hit."""
    pub = datetime.datetime(2026, 9, 1, tzinfo=datetime.timezone.utc)
    vids = [insights.Video(f"b{i}", pub, views=1000 + i, meta={"title_style": "B"})
            for i in range(2)]
    vids += [insights.Video(f"a{i}", pub, views=10, meta={"title_style": "A"})
             for i in range(17)]
    vids += [insights.Video("z", pub, views=0, meta={"title_style": "A"})]
    rows, cut = insights.hit_rates(vids, "title_style")
    assert cut == 2
    assert [(label, n, hits) for label, n, hits, _ in rows] == [("B", 2, 2), ("A", 18, 0)]
    assert rows[0][3] == rows[1][3] < 0.01


def test_views_gained_counts_the_back_catalogue_and_new_uploads():
    """The Partner Program's bar counts every view in the window, so an old
    video's growth counts, and a video new since the last snapshot counts in
    full. A dip in a lifetime count (YouTube revises them) subtracts nothing."""
    rows = [_snap("old", 0, 10, 100), _snap("dip", 0, 10, 50),
            _snap("old", 0, 17, 130), _snap("dip", 0, 17, 45),
            _snap("new", 12, 17, 20)]
    gained = insights.views_gained(rows)
    assert [(g, d) for _, g, d in gained] == [(50, 7)]


def test_totals_change_compares_the_last_four_weeks_with_the_four_before():
    series = [(f"w{i}", 14, t) for i, t in enumerate([100] * 4 + [250] * 4)]
    prior, recent, ratio = insights.totals_change(series)
    assert (prior, recent, ratio) == (400, 1000, 2.5)
    assert insights.totals_change(series[:7]) is None


# ------------------------------------------------------------- scorecard

def test_longer_videos_are_not_called_success():
    """The owner's exact objection, and the project's own scar.

    Watch-seconds up while the share watched falls and duration rises is
    "we made videos longer", not "we made them better". A single-metric
    verdict calls it success; this must not.
    """
    then = {"watch_seconds": 10.0, "avg_view_pct": 55.0, "views": 120.0,
            "zero_rate": 3.0, "duration_s": 19.0}
    now = {"watch_seconds": 12.0, "avg_view_pct": 45.0, "views": 118.0,
           "zero_rate": 3.0, "duration_s": 26.0}
    verdict, rows, notes = insights.scorecard(then, now)
    assert verdict == "MIXED", verdict
    assert any("artefact" in n for n in notes)
    pct = next(r for r in rows if r["metric"] == "avg_view_pct")
    assert pct["read"] == "BREACHED"


def test_a_rising_zero_rate_breaches_and_a_falling_one_does_not():
    """zero_rate is suppression: up is worse. The check once read every
    guardrail as lower-is-worse, so a 2.4 -> 5.6 rise passed as "ok"."""
    then = {"watch_seconds": 12.0, "avg_view_pct": 61.5, "zero_rate": 2.4}
    now = {"watch_seconds": 12.5, "avg_view_pct": 56.8, "zero_rate": 5.6}
    verdict, rows, _ = insights.scorecard(then, now)
    assert next(r for r in rows if r["metric"] == "zero_rate")["read"] == "BREACHED"
    assert verdict == "MIXED"
    verdict, rows, _ = insights.scorecard(now, {**now, "zero_rate": 1.0})
    assert next(r for r in rows if r["metric"] == "zero_rate")["read"] == "ok"


def test_a_genuine_improvement_still_reads_as_better():
    """The guard must not make every result mixed."""
    then = {"watch_seconds": 10.0, "avg_view_pct": 50.0, "views": 120.0, "zero_rate": 3.0}
    now = {"watch_seconds": 12.0, "avg_view_pct": 52.0, "views": 130.0, "zero_rate": 2.0}
    verdict, _, _ = insights.scorecard(then, now)
    assert verdict == "BETTER"


def test_a_guardrail_breach_alone_is_worse_not_flat():
    then = {"watch_seconds": 10.0, "avg_view_pct": 55.0, "views": 120.0, "zero_rate": 1.0}
    now = {"watch_seconds": 10.0, "avg_view_pct": 40.0, "views": 118.0, "zero_rate": 1.0}
    verdict, _, _ = insights.scorecard(then, now)
    assert verdict == "WORSE"


def test_movement_inside_the_margin_does_not_breach():
    """Guardrails have margins so ordinary weather doesn't block everything."""
    then = {"watch_seconds": 10.0, "avg_view_pct": 50.0, "views": 120.0, "zero_rate": 2.0}
    now = {"watch_seconds": 11.0, "avg_view_pct": 47.0, "views": 100.0, "zero_rate": 3.0}
    verdict, _, _ = insights.scorecard(then, now)
    assert verdict == "BETTER"


def test_diagnostics_explain_but_never_vote():
    """A diagnostic moving wildly must not change the verdict by itself."""
    base = {"watch_seconds": 10.0, "avg_view_pct": 50.0, "views": 120.0, "zero_rate": 2.0}
    calm = insights.scorecard(base, dict(base, watch_seconds=11.0))[0]
    noisy = insights.scorecard(dict(base, duration_s=15.0),
                               dict(base, watch_seconds=11.0, duration_s=40.0))[0]
    assert calm == noisy == "BETTER"


def test_the_power_caveat_is_always_stated():
    """A small-cohort channel must never be handed a confident verdict."""
    _, _, notes = insights.scorecard({"watch_seconds": 10.0}, {"watch_seconds": 11.0})
    assert any("weather" in n for n in notes)


def test_views_does_not_block_on_ordinary_weather():
    """Views swings 2.8x on this channel with the format unchanged.

    The first real scorecard run breached on a 2x drop that is well inside
    that, which is a false positive of exactly the kind `drift_floor` exists
    to prevent. Views is diagnostic unless a caller supplies a measured floor.
    """
    then = {"watch_seconds": 11.0, "avg_view_pct": 59.0, "views": 136.0, "zero_rate": 2.4}
    now = {"watch_seconds": 12.0, "avg_view_pct": 59.0, "views": 67.5, "zero_rate": 2.4}
    verdict, rows, _ = insights.scorecard(then, now)
    assert verdict == "BETTER", verdict
    views_row = next(r for r in rows if r["metric"] == "views")
    assert views_row["kind"] == "diagnostic"


def test_a_measured_floor_promotes_views_to_a_guardrail():
    """Once we can measure its ordinary swing, it can block again."""
    then = {"watch_seconds": 11.0, "views": 136.0}
    now = {"watch_seconds": 12.0, "views": 67.5}
    verdict, rows, _ = insights.scorecard(then, now, guardrails={"views": 20.0})
    assert verdict == "MIXED"
    assert next(r for r in rows if r["metric"] == "views")["read"] == "BREACHED"


def test_a_big_diagnostic_move_is_never_silent():
    """It must not vote, and it must not be hidden.

    The first real run reported BETTER while views and engagement had both
    roughly halved. Not blocking on that is correct; saying nothing is not.
    """
    then = {"watch_seconds": 11.0, "views": 136.0, "likes_per_100": 1.1}
    now = {"watch_seconds": 12.0, "views": 67.5, "likes_per_100": 0.5}
    verdict, _, notes = insights.scorecard(then, now)
    assert verdict == "BETTER"
    assert any("views" in n and "watch if they repeat" in n for n in notes)


def test_replay_share_counts_only_over_100_pct_among_videos_with_enough_views():
    videos = [
        v("a", 10, views=50, pct=120.0),   # replaying
        v("b", 10, views=50, pct=100.0),   # watched once, exactly: not a replay
        v("c", 10, views=50, pct=60.0),
        v("d", 10, views=5, pct=300.0),    # one rewatcher on a thin video: excluded
    ]
    assert insights.replay_share(videos) == (1, 3)


def test_slate_agreement_reads_the_selected_posts_label():
    """On 2026-09-29 the slate and the screen agreed on 2 of 6 selected posts,
    found by hand; R4.4's firing rate is counted on slate labels."""
    rows = [
        {"topic": "nostalgia", "candidate_rank": "1", "slate_topics": "nostalgia|other"},
        {"topic": "other", "candidate_rank": "2", "slate_topics": "humor-absurd|nostalgia"},
        {"topic": "other", "candidate_rank": "1", "slate_topics": "!SlateFailed"},
        {"topic": "other", "candidate_rank": "1", "slate_topics": ""},
        {"topic": "other", "candidate_rank": "1", "slate_topics": "?|other"},
        {"topic": "other", "candidate_rank": "3", "slate_topics": "other"},
    ]
    assert insights.slate_agreement(rows) == (1, 2, [("other", "nostalgia")])



def test_report_refuses_an_age_read_inside_the_reporting_lag():
    """At 3-4 days a third of uploads still read zero from Analytics lag, so a
    median there is over whichever videos happened to be reported first."""
    import subprocess
    import sys
    r = subprocess.run([sys.executable, "scripts/report.py", "--offline", "--at-age", "3",
                        "--compare", "topic=dark-morbid"], capture_output=True, text=True)
    assert r.returncode != 0 and "under 5 days" in r.stderr


def test_era_imbalance_flags_a_field_that_clusters_in_one_release():
    """Voice read +50% on views pooled on 2026-09-28 only because Stephen had
    read most of the high-view `v4` era; within it the lead was 6%."""
    stephen = cohort(37, 7, "s", format_version="v4") + cohort(30, 7, "s5", format_version="v5")
    danielle = cohort(20, 7, "d", format_version="v4") + cohort(43, 7, "d5", format_version="v5")
    gaps = insights.era_imbalance(stephen, danielle)
    assert {era for era, _, _ in gaps} == {"v4", "v5"}


def test_era_imbalance_is_quiet_when_the_mix_is_even():
    b_style = cohort(19, 7, "b", format_version="v4") + cohort(23, 7, "b5", format_version="v5")
    rest = cohort(38, 7, "r", format_version="v4") + cohort(49, 7, "r5", format_version="v5")
    assert insights.era_imbalance(b_style, rest) == []


def test_implied_engaged_is_minutes_over_views_times_watch_seconds():
    """R2: est_minutes x 60 / (views x watch-seconds) — 0.18 pre-v2, ~0.4 after."""
    x = Video("a", NOW, views=100, watch_seconds=12.0, est_minutes=4.0)
    assert x.implied_engaged == pytest.approx(0.2)
    assert Video("b", NOW).implied_engaged == 0.0          # no views: no share


def test_buried_rate_p_matches_fishers_exact_test():
    """Fisher's tea-tasting table [[3,1],[1,3]] is p=0.4857 two-sided."""
    assert insights.buried_rate_p(3, 4, 1, 4) == pytest.approx(0.4857, abs=1e-4)
    assert insights.buried_rate_p(3, 4, 1, 4) == insights.buried_rate_p(1, 4, 3, 4)


def test_buried_rate_p_is_one_when_nothing_can_differ():
    assert insights.buried_rate_p(0, 10, 0, 12) == 1.0
    assert insights.buried_rate_p(2, 2, 3, 3) == 1.0
    assert insights.buried_rate_p(0, 0, 1, 5) == 1.0


def test_buried_rate_p_pooled_tests_within_strata_only():
    # One stratum with no difference contributes nothing; the gap is in the other.
    gap = insights.buried_rate_p_pooled([(8, 27, 2, 26)])
    assert insights.buried_rate_p_pooled([(8, 27, 2, 26), (0, 10, 0, 10)]) == gap
    assert insights.buried_rate_p_pooled([(3, 22, 0, 37), (8, 27, 2, 26)]) < gap
    # Opposite gaps in two strata cancel rather than add.
    assert insights.buried_rate_p_pooled([(5, 20, 0, 20), (0, 20, 5, 20)]) == 1.0
    assert insights.buried_rate_p_pooled([]) == 1.0


def test_buried_strata_pairs_only_shared_values():
    def v(fmt, views):
        return Video("x", datetime.datetime(2026, 9, 1), views=views,
                     meta={"format_version": fmt})
    a = [v("v4", 0), v("v4", 50), v("v5", 3), v("v6", 1)]
    b = [v("v4", 90), v("v5", 80), v("v5", 2)]
    assert insights.buried_strata(a, b) == [(1, 2, 0, 1), (1, 1, 1, 2)]


def test_buried_vs_rest_tests_each_group_against_the_others_pooled():
    """#11's rule: a clip whose uploads are buried far more often than every
    other clip's, within the same format, ranks first with a small p."""
    def v(views, fmt="v5"):
        return Video("x", datetime.datetime(2026, 9, 1), views=views,
                     meta={"format_version": fmt})
    groups = {"bad.mp4": [v(1)] * 8 + [v(90)] * 8,
              "ok1.mp4": [v(1)] + [v(90)] * 29,     # the real retirement: 8/16 vs 3/62
              "ok2.mp4": [v(2)] * 2 + [v(90)] * 30,
              "thin.mp4": [v(90)] * 3,
              "(unset)": [v(0)] * 20}
    rows = insights.buried_vs_rest(groups)
    assert [r[0] for r in rows][0] == "bad.mp4"
    assert {r[0] for r in rows} == {"bad.mp4", "ok1.mp4", "ok2.mp4"}  # thin and unset skipped
    label, hits, n, p = rows[0]
    assert (hits, n) == (8, 16) and p < 0.05 / len(rows)
    assert rows[-1][3] > 0.05
    # A second bad group is not hidden by the first one raising "the rest".
    groups["bad2.mp4"] = [v(1)] * 5 + [v(90)] * 11      # p=0.17 with bad.mp4 in its rest
    flagged = [r[0] for r in insights.buried_vs_rest(groups) if r[3] < 0.05 / 4]
    assert flagged == ["bad.mp4", "bad2.mp4"]
    # A gap that is only an era mix is not one: same rates within each format.
    era = {"a": [v(1, "v4")] * 10 + [v(90, "v5")] * 6,
           "b": [v(1, "v4")] * 2 + [v(90, "v5")] * 14}
    assert insights.buried_rate_p(10, 16, 2, 16) < 0.05   # pooled naively, it would flag
    assert all(p > 0.05 for *_, p in insights.buried_vs_rest(era))


def test_clip_use_counts_each_broll_clip_in_log_order():
    rows = [{"timestamp_utc": f"2026-09-{d:02d}T05:00:00+00:00", "bg_clip": c}
            for d, c in [(5, "a.mp4"), (1, "a.mp4"), (2, "procedural:7"),
                         (3, "a.mp4"), (4, "a.mp4"), (6, "b.mp4"), (7, "")]]
    out = {r["timestamp_utc"][8:10]: r["clip_use"] for r in insights.with_clip_use(rows)}
    assert insights.CLIP_EARLY_USES == 4
    assert out == {"01": "early", "03": "early", "04": "early", "05": "early",
                   "06": "early", "02": "", "07": ""}
    late = insights.with_clip_use(rows + [{"timestamp_utc": "2026-09-08", "bg_clip": "a.mp4"}])
    assert late[-1]["clip_use"] == "late"


def test_engaged_check_reads_the_minutes_column_against_engaged_views():
    from src import insights as _ins
    # 100 views, 40 engaged, 10 s per engaged view -> 400 s = 6.667 minutes
    match = {"views": "100", "avg_view_duration_s": "10", "engaged_views": "40",
             "est_minutes_watched": str(400 / 60)}
    off = dict(match, engaged_views="80")      # implied 0.4 vs actual 0.8
    blank = dict(match, engaged_views="")
    small = dict(match, views="5")
    n, med, within = _ins.engaged_check([match, match, off, blank, small])
    assert n == 3
    assert abs(med - 1.0) < 1e-9
    assert abs(within - 2 / 3) < 1e-9
    assert _ins.engaged_check([blank]) == (0, None, None)


def test_engaged_share_sums_both_counts_and_refuses_a_thin_cohort():
    import datetime as _dt
    from src import insights as _ins
    old = {"views": "100", "engaged_views": "50", "published_at": "2026-06-01T12:00:00Z"}
    new = dict(old, views="300", engaged_views="60", published_at="2026-09-01T12:00:00Z")
    blank = dict(new, engaged_views="")
    rows = [old] * 10 + [new] * 20 + [blank] * 5
    n, views, engaged, share = _ins.engaged_share(rows)
    assert (n, views, engaged) == (30, 7000, 1700)
    assert abs(share - 1700 / 7000) < 1e-9     # summed, not a mean of ratios
    since = _dt.datetime(2026, 7, 1, tzinfo=_dt.timezone.utc)
    assert _ins.engaged_share(rows, since)[1:] == (6000, 1200, 0.2)
    assert _ins.engaged_share([new] * 19) == (19, 5700, 1140, None)


def test_engaged_share_metric_skips_videos_read_before_the_column_existed():
    import datetime as _dt
    from src import insights as _ins
    t = _dt.datetime(2026, 10, 1, tzinfo=_dt.timezone.utc)
    vids = [_ins.Video("a", t, views=100, engaged_views=30),
            _ins.Video("b", t, views=100, engaged_views=50),
            _ins.Video("c", t, views=100),                   # pre-2026-10-05 snapshot
            _ins.Video("d", t, views=0, engaged_views=0)]    # zero-view, still counted
    c = _ins.summarize(vids, "all", _ins.Metric.ENGAGED_SHARE, t)
    assert (c.n, c.zero_view_count) == (2, 1)
    assert abs(c.median - 0.4) < 1e-9
    assert _ins.summarize(vids, "all", _ins.Metric.VIEWS, t).n == 3


def test_snapshot_rows_skip_a_blank_engaged_count_rather_than_read_zero(tmp_path):
    import importlib.util, pathlib, sys
    root = pathlib.Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("report", root / "scripts" / "report.py")
    report = importlib.util.module_from_spec(spec)
    sys.modules["report"] = report
    spec.loader.exec_module(report)
    csv_path = tmp_path / "snap.csv"
    csv_path.write_text(
        "snapshot_date,video_id,published_at,views,engaged_views\n"
        "2026-09-28,a,2026-09-21T12:00:00Z,100,\n"      # before the column
        "2026-10-05,a,2026-09-21T12:00:00Z,120,40\n"
        "2026-10-05,b,2026-09-29T12:00:00Z,0,0\n"       # a real zero stays
        "2026-10-05,c,2026-09-30T12:00:00Z,0,\n")       # API blank on zero views
    engaged = report._snapshot_metric_rows("engaged_views", path=str(csv_path))
    assert [(r["video_id"], r["value"]) for r in engaged] == [
        ("a", 40.0), ("b", 0.0), ("c", 0.0)]
    views = report._snapshot_metric_rows("views", path=str(csv_path))
    assert len(views) == 4


def test_engaged_per_100_needs_every_viewed_row_to_carry_the_count():
    from src import insights as _ins
    full = [{"views": "100", "engaged_views": "30"}, {"views": "50", "engaged_views": "30"},
            {"views": "0", "engaged_views": ""}]            # zero-view rows come back blank
    assert abs(_ins.engaged_per_100(full) - 40.0) < 1e-9
    assert _ins.engaged_per_100(full + [{"views": "10", "engaged_views": ""}]) is None
    assert _ins.engaged_per_100([{"views": "0", "engaged_views": ""}]) is None
    then, now = {"watch_seconds": 12, "engaged_per_100": 30.0}, {"watch_seconds": 12}
    _, rows, _ = _ins.scorecard(then, now)
    assert "engaged_per_100" not in [r["metric"] for r in rows]   # one side unread: no row


def test_latest_releases_are_newest_first_by_upload_order():
    rows = [{"format_version": v} for v in ("v4", "v5", "v5", "v6", "", "v7", "v7")]
    assert insights.latest_releases(rows) == ["v7", "v6"]
    assert insights.latest_releases([]) == []


def test_the_digest_line_reads_each_release_at_its_committed_size(tmp_path, monkeypatch):
    """The Monday digest carries the auto-revert verdict, and a release that
    committed to more uploads than the floor is not answered early."""
    import csv as _csv
    from src import config
    _two_eras(tmp_path, monkeypatch, n=10)
    rows = list(_csv.DictReader(open(config.UPLOAD_LOG)))
    line = insights.release_digest_line(rows)
    assert "`v5`: KEEP" in line and "`v4`:" in line
    monkeypatch.setitem(insights.RELEASE_MIN_UPLOADS, "v5", 20)
    assert "`v5`: NO VERDICT — 10 measurable release uploads, the rule commits to 20" in (
        insights.release_digest_line(rows))


def test_slate_firing_counts_a_weak_top_with_a_strong_candidate_in_the_top_three():
    rows = [{"slate_topics": "money-work|other|nostalgia|x"},       # fires
            {"slate_topics": "money-work|other|other|nostalgia"},   # strong at 4th: no
            {"slate_topics": "nostalgia|money-work|dark-morbid"},   # top is strong: no
            {"slate_topics": "?|nostalgia"},                        # unlabelled top: no
            {"slate_topics": "!timeout"}, {"slate_topics": ""}]     # not read
    assert insights.slate_firing(rows) == (1, 4)


def test_a_zero_view_upload_stays_zero_view_under_the_engaged_metrics():
    """The API leaves engaged views blank on zero-view rows; dropping those
    moved the zero and buried counts with --metric (review, 2026-10-06)."""
    import datetime as _dt
    from src import insights as _ins
    t = _dt.datetime(2026, 10, 1, tzinfo=_dt.timezone.utc)
    vids = [_ins.Video("a", t, views=100, engaged_views=30),
            _ins.Video("z", t, views=0)]                     # blank engaged, zero views
    for metric in (_ins.Metric.ENGAGED_SHARE, _ins.Metric.ENGAGED_VIEWS, _ins.Metric.VIEWS):
        c = _ins.summarize(vids, "all", metric, t)
        assert (c.n, c.zero_view_count, c.buried_count) == (1, 1, 1)
