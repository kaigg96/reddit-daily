"""The weekly snapshot gains engaged_views without risking the series it extends.

analysis/analytics_snapshots.csv is the measurement backbone every release
verdict reads, and it has ~7,500 rows with mixed line endings. Adding a column
must touch only its header, and a refusal of the new metric must cost the
column, never the snapshot.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import weekly_analytics as wa  # noqa: E402

OLD = wa.FIELDS[:-1]


def test_header_is_extended_and_every_other_byte_is_kept(tmp_path):
    p = tmp_path / "snap.csv"
    body = b"2026-07-21,a,2026-07-01,5,0,0,0,1,10,50\r\n2026-09-21,b,2026-09-01,7,0,0,0,1,12,60\n"
    p.write_bytes(",".join(OLD).encode() + b"\n" + body)
    wa.ensure_header(p, wa.FIELDS)
    head, rest = p.read_bytes().split(b"\n", 1)
    assert head.decode().split(",") == wa.FIELDS
    assert rest == body  # mixed CRLF/LF rows untouched


def test_crlf_header_keeps_its_line_ending(tmp_path):
    p = tmp_path / "snap.csv"
    p.write_bytes(",".join(OLD).encode() + b"\r\nrow\r\n")
    wa.ensure_header(p, wa.FIELDS)
    assert p.read_bytes() == ",".join(wa.FIELDS).encode() + b"\r\nrow\r\n"


def test_current_header_is_left_alone(tmp_path):
    p = tmp_path / "snap.csv"
    original = ",".join(wa.FIELDS).encode() + b"\nrow\n"
    p.write_bytes(original)
    wa.ensure_header(p, wa.FIELDS)
    assert p.read_bytes() == original


def test_a_header_that_is_not_a_prefix_is_refused(tmp_path):
    p = tmp_path / "snap.csv"
    p.write_bytes(b"snapshot_date,views,video_id\nrow\n")
    with pytest.raises(SystemExit):
        wa.ensure_header(p, wa.FIELDS)
    assert p.read_bytes() == b"snapshot_date,views,video_id\nrow\n"


def test_old_rows_read_back_blank_for_the_new_column(tmp_path):
    import csv
    p = tmp_path / "snap.csv"
    p.write_bytes(",".join(OLD).encode() + b"\n2026-09-21,b,2026-09-01,7,0,0,0,1,12,60\n")
    wa.ensure_header(p, wa.FIELDS)
    (row,) = csv.DictReader(open(p, newline=""))
    assert row["views"] == "7" and row["engaged_views"] is None


class _FakeAnalytics:
    """Stands in for the Analytics client; refuses engagedViews if told to."""

    def __init__(self, refuse_engaged):
        self.refuse_engaged = refuse_engaged
        self.calls = []

    def reports(self):
        return self

    def query(self, **kw):
        self.calls.append(kw["metrics"])
        self._metrics = kw["metrics"].split(",")
        self._ids = kw["filters"].removeprefix("video==").split(",")
        return self

    def execute(self):
        if self.refuse_engaged and wa.ENGAGED_METRIC in self._metrics:
            raise RuntimeError("HttpError 400: Unknown identifier (engagedViews)")
        headers = [{"name": "video"}] + [{"name": m} for m in self._metrics]
        rows = [[v] + [3 if m == wa.ENGAGED_METRIC else 9 for m in self._metrics]
                for v in self._ids]
        return {"columnHeaders": headers, "rows": rows}


def test_engaged_views_are_collected_when_served():
    ya = _FakeAnalytics(refuse_engaged=False)
    stats = wa.fetch_stats_with_engaged(ya, ["a", "b"], "2026-09-28")
    assert stats["a"][wa.ENGAGED_METRIC] == 3 and stats["a"]["views"] == 9
    assert len(ya.calls) == 1


def test_a_refused_metric_costs_the_column_not_the_snapshot():
    ya = _FakeAnalytics(refuse_engaged=True)
    stats = wa.fetch_stats_with_engaged(ya, ["a", "b"], "2026-09-28")
    assert set(stats) == {"a", "b"} and stats["a"]["views"] == 9
    assert stats["a"][wa.ENGAGED_METRIC].startswith("refused: RuntimeError: HttpError 400")
    assert ya.calls[-1] == wa.METRICS
