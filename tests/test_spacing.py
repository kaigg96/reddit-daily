"""R8 (PRD §4): uploads beside a missed slot against the regular rhythm,
matched within each month."""
import datetime

from src import insights

UTC = datetime.timezone.utc
ASOF = datetime.datetime(2026, 11, 2, tzinfo=UTC)


def _v(vid, when, views, watch=10.0, privacy="public"):
    stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(when, datetime.datetime) else when
    return {"id": vid, "published": stamp, "views": views, "watch_s": watch, "privacy": privacy}


def _stream(start, slots, missed, views, sparse_views=None):
    """The real rhythm: an upload every 12 hours, except the `missed` slots.
    Uploads beside a missed slot get `sparse_views` when given."""
    t0 = datetime.datetime.fromisoformat(start).replace(tzinfo=UTC)
    out, kept = [], [i for i in range(slots) if i not in missed]
    for i in kept:
        # a stream's first and last uploads have a neighbour on one side only
        beside = (i - 1) in missed or (i + 1) in missed or i in (kept[0], kept[-1])
        n = sparse_views if (beside and sparse_views is not None) else views
        out.append(_v(f"{start}-{i}", t0 + datetime.timedelta(hours=12 * i), n(i) if callable(n) else n))
    return out


def test_the_twice_a_day_rhythm_is_regular_and_a_missed_slot_makes_its_neighbours_sparse():
    vids = _stream("2025-05-01T06:00:00", 10, missed={5}, views=1)
    labels = insights.spacing_labels(vids)
    assert labels["2025-05-01T06:00:00-4"] == labels["2025-05-01T06:00:00-6"] == "sparse"
    assert labels["2025-05-01T06:00:00-2"] == "regular"
    assert labels["2025-05-01T06:00:00-0"] == "sparse"     # the stream's edge has one side


def test_exactly_the_window_away_is_not_near_and_privatised_uploads_still_count():
    vids = [_v("a", "2025-05-01T00:00:00Z", 1),
            _v("b", "2025-05-01T18:00:00Z", 1),                       # 18h: not near a
            _v("c", "2025-05-01T12:00:00Z", 1, privacy="private"),    # near both
            _v("d", "2025-05-01T13:00:00Z", 1)]
    labels = insights.spacing_labels(vids)
    assert labels["a"] == "regular"          # c (12h) and d (13h); b is exactly 18h
    assert labels["c"] == "dense"            # a, b and d


def _months(sparse_views, regular_views, months=("2025-05", "2025-06", "2025-07",
                                                 "2025-08", "2025-09")):
    vids = []
    for m in months:
        # 40 slots (20 days), three isolated missed slots: 6 sparse, plus the 2 edges
        vids += _stream(f"{m}-01T06:00:00", 40, missed={8, 20, 32},
                        views=regular_views, sparse_views=sparse_views)
    return vids


def test_a_large_sparse_lead_reads_as_dilution():
    r = insights.spacing_read(_months(lambda i: 200 + i % 5, lambda i: 100 + i % 7), ASOF,
                              shuffles=300)
    assert r.sparse == 40 and r.months == 5 and r.dense == 0
    assert 1.9 < r.ratio < 2.1 and r.watch_ratio == 1.0
    assert r.verdict.startswith("sparse leads")


def test_a_large_regular_lead_is_recorded_only():
    r = insights.spacing_read(_months(lambda i: 50 + i % 5, lambda i: 100 + i % 7), ASOF,
                              shuffles=300)
    assert r.verdict.startswith("regular leads")


def test_equal_views_read_within_the_gap():
    r = insights.spacing_read(_months(100, 100), ASOF, shuffles=300)
    assert r.verdict.startswith("within the gap")


def test_under_25_sparse_uploads_is_insufficient_and_reads_nothing():
    three = _months(500, 1, months=("2025-05", "2025-06", "2025-07"))
    r = insights.spacing_read(three, ASOF)
    assert r.sparse == 24 and r.ratio is None and r.verdict == "insufficient data"
    four = _months(500, 1, months=("2025-05", "2025-06", "2025-07", "2025-08"))
    assert insights.spacing_read(four, ASOF, shuffles=50).ratio == 500


def test_young_private_early_and_one_sparse_months_are_left_out():
    vids = (_stream("2026-10-01T06:00:00", 40, missed={8, 20, 32}, views=5)   # under 60 days
            + _stream("2025-02-01T06:00:00", 40, missed={8, 20, 32}, views=5)  # before 2025-04
            + _stream("2025-06-25T06:00:00", 40, missed=set(), views=5)       # one sparse a month
            + [_v("x", "2025-08-01T06:00:00Z", 500, privacy="private")])
    r = insights.spacing_read(vids, ASOF)
    assert r.months == 0 and r.sparse == 0 and r.verdict == "insufficient data"


def test_report_refuses_options_spacing_would_ignore():
    import subprocess
    import sys
    for extra in (["--within", "subreddit=AskReddit"], ["--metric", "views"], ["--at-age", "7"]):
        out = subprocess.run([sys.executable, "scripts/report.py", "--spacing", *extra],
                             capture_output=True, text=True,
                             cwd=insights.config.ROOT)
        assert out.returncode != 0 and "--spacing takes no other option" in out.stderr, extra
