"""R8 (PRD §4): alone against paired uploads, matched within each month."""
import datetime

from src import insights

UTC = datetime.timezone.utc


def _v(vid, when, views, watch=10.0, privacy="public"):
    return {"id": vid, "published": when, "views": views, "watch_s": watch, "privacy": privacy}


def test_labels_count_neighbours_within_the_window_either_side():
    vids = [
        _v("a", "2025-05-01T06:00:00Z", 1),
        _v("b", "2025-05-01T18:00:00Z", 1),   # 12h after a, 30h before c
        _v("c", "2025-05-03T00:00:00Z", 1),   # alone: b is 30h back
        _v("d", "2025-05-05T00:00:00Z", 1),
        _v("e", "2025-05-05T06:00:00Z", 1, privacy="private"),  # still a neighbour
        _v("f", "2025-05-05T12:00:00Z", 1),
    ]
    labels = insights.spacing_labels(vids)
    assert labels["a"] == labels["b"] == "paired"
    assert labels["c"] == "alone"
    assert labels["d"] == labels["e"] == labels["f"] == "crowded"   # two within 18h each


def _month(month, alone_views, paired_views):
    """Alone uploads three days apart; paired uploads in 12-hour pairs after them."""
    out, day = [], 1
    for i, views in enumerate(alone_views):
        out.append(_v(f"{month}a{i}", f"{month}-{day:02d}T06:00:00Z", views))
        day += 3
    for i in range(0, len(paired_views), 2):
        out.append(_v(f"{month}p{i}", f"{month}-{day:02d}T06:00:00Z", paired_views[i]))
        out.append(_v(f"{month}q{i}", f"{month}-{day:02d}T18:00:00Z", paired_views[i + 1]))
        day += 2
    return out


ASOF = datetime.datetime(2026, 11, 2, tzinfo=UTC)


def test_a_large_alone_lead_reads_as_dilution():
    vids = []
    for m in ("2025-05", "2025-06", "2025-07", "2025-08", "2025-09"):
        vids += _month(m, [200, 210, 190, 205, 195, 200], [100, 105, 95, 100, 98, 102])
    r = insights.spacing_read(vids, ASOF, shuffles=300)
    assert r.alone == 30 and r.months == 5
    assert 1.9 < r.ratio < 2.1
    assert r.verdict.startswith("alone leads")


def test_equal_views_read_within_the_gap():
    vids = []
    for m in ("2025-05", "2025-06", "2025-07", "2025-08", "2025-09"):
        vids += _month(m, [90, 110, 100, 95, 105, 100], [100, 92, 108, 97, 103, 100])
    r = insights.spacing_read(vids, ASOF, shuffles=300)
    assert r.verdict.startswith("within the gap")


def test_too_few_alone_uploads_is_insufficient_and_reads_nothing():
    vids = _month("2025-05", [500, 500], [1, 1, 1, 1])
    r = insights.spacing_read(vids, ASOF)
    assert r.alone == 2 and r.ratio is None and r.verdict == "insufficient data"


def test_young_private_and_early_uploads_are_left_out():
    vids = (_month("2026-10", [500] * 6, [1] * 6)              # under 60 days at the snapshot
            + _month("2025-02", [500] * 6, [1] * 6)             # before 2025-04-01
            + [_v("x", "2025-06-01T06:00:00Z", 500, privacy="private")])
    r = insights.spacing_read(vids, ASOF)
    assert r.alone == 0 and r.verdict == "insufficient data"
