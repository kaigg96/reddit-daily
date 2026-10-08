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

# Pinned, not derived from FIELDS: a derived OLD drifts with every new column
# and stops testing the header the file actually has. OLD matches the
# 10-value rows below; LIVE is the header on disk on 2026-10-08, which the next
# weekly run extends by two columns at once (subs_gained, privacy_status).
OLD = ["snapshot_date", "video_id", "published_at", "views", "likes", "comments",
       "shares", "est_minutes_watched", "avg_view_duration_s", "avg_view_pct"]
LIVE = OLD + ["engaged_views"]


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
    assert row["views"] == "7"
    assert all(row[c] is None for c in wa.FIELDS[len(OLD):])


class _FakeAnalytics:
    """Stands in for the Analytics client; refuses engagedViews if told to."""

    def __init__(self, refuse_engaged, only_beside_all=False):
        self.refuse_engaged = refuse_engaged
        self.only_beside_all = only_beside_all
        self.calls = []

    def reports(self):
        return self

    def query(self, **kw):
        self.calls.append(kw["metrics"])
        self._metrics = kw["metrics"].split(",")
        self._ids = kw["filters"].removeprefix("video==").split(",")
        return self

    def execute(self):
        if (self.refuse_engaged and wa.ENGAGED_METRIC in self._metrics
                and not (self.only_beside_all and len(self._metrics) == 2)):
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
    assert "; alone: RuntimeError" in stats["a"][wa.ENGAGED_METRIC]
    assert wa.METRICS in ya.calls


def test_engaged_views_refused_beside_every_metric_are_asked_for_alone():
    ya = _FakeAnalytics(refuse_engaged=True, only_beside_all=True)
    stats = wa.fetch_stats_with_engaged(ya, ["a", "b"], "2026-09-28")
    assert stats["a"][wa.ENGAGED_METRIC] == 3 and stats["a"]["views"] == 9
    assert ya.calls[-1] == f"views,{wa.ENGAGED_METRIC}"


class _FakeYT:
    """channels().list(...).execute() -> one channel's statistics."""

    def __init__(self, stats):
        self.stats = stats

    def channels(self):
        return self

    def list(self, **kwargs):
        assert kwargs == {"mine": True, "part": "statistics"}
        return self

    def execute(self):
        return {"items": [{"statistics": self.stats}]}


def test_channel_snapshot_appends_one_row_under_one_header(tmp_path):
    p = tmp_path / "channel.csv"
    yt = _FakeYT({"subscriberCount": "142", "hiddenSubscriberCount": False,
                  "viewCount": "91000", "videoCount": "180"})
    wa.snapshot_channel(yt, "2026-10-12", p)
    wa.snapshot_channel(yt, "2026-10-19", p)
    lines = p.read_text().splitlines()
    assert lines == [",".join(wa.CHANNEL_FIELDS),
                     "2026-10-12,142,0,91000,180",
                     "2026-10-19,142,0,91000,180"]


def test_hidden_subscriber_count_is_flagged_not_guessed(tmp_path):
    p = tmp_path / "channel.csv"
    wa.snapshot_channel(_FakeYT({"hiddenSubscriberCount": True, "viewCount": "1"}), "2026-10-12", p)
    assert p.read_text().splitlines()[1] == "2026-10-12,,1,1,"


class _FakeComments:
    def __init__(self, items):
        self.items = items

    def commentThreads(self):
        return self

    def list(self, **kwargs):
        return self

    def execute(self):
        return {"items": self.items}


def _thread(cid, when, text):
    return {"snippet": {"topLevelComment": {"id": cid, "snippet": {
        "publishedAt": when, "likeCount": 2, "textDisplay": text, "authorDisplayName": "x"}}}}


def test_comments_keep_last_week_only_on_one_line_without_author(tmp_path):
    p = tmp_path / "comments.csv"
    yt = _FakeComments([_thread("new", "2026-10-10T01:00:00Z", "great\nvideo"),
                        _thread("old", "2026-09-01T01:00:00Z", "stale")])
    assert wa.snapshot_comments(yt, "2026-10-12", ["v1"], p) == 1
    lines = p.read_text().splitlines()
    assert lines == [",".join(wa.COMMENTS_FIELDS),
                     "2026-10-12,v1,new,2026-10-10T01:00:00Z,2,great video"]


class _FakeSubsAnalytics(_FakeAnalytics):
    """Serves subscribersGained (as 2) unless told to refuse it."""

    def __init__(self, refuse_subs):
        super().__init__(refuse_engaged=False)
        self.refuse_subs = refuse_subs

    def execute(self):
        if self.refuse_subs and wa.SUBS_METRIC in self._metrics:
            raise RuntimeError("HttpError 400: Unknown identifier (subscribersGained)")
        resp = super().execute()
        if wa.SUBS_METRIC in self._metrics:
            i = self._metrics.index(wa.SUBS_METRIC) + 1
            for row in resp["rows"]:
                row[i] = 2
        return resp


def test_subscribers_gained_are_added_per_upload():
    """Subscribers are half the Partner Program's bar; C11's channel count
    cannot say which uploads earn them (2026-10-07)."""
    ya = _FakeSubsAnalytics(refuse_subs=False)
    stats = wa.fetch_stats_with_engaged(ya, ["a", "b"], "2026-10-12")
    wa.add_subscribers_gained(ya, stats, ["a", "b"], "2026-10-12")
    assert stats["a"][wa.SUBS_METRIC] == 2 and stats["a"]["views"] == 9
    assert ya.calls[-1] == f"views,{wa.SUBS_METRIC}"


def test_a_refused_subscribers_query_costs_the_column_not_the_snapshot():
    ya = _FakeSubsAnalytics(refuse_subs=True)
    stats = wa.fetch_stats_with_engaged(ya, ["a", "b"], "2026-10-12")
    wa.add_subscribers_gained(ya, stats, ["a", "b"], "2026-10-12")
    assert stats["a"]["views"] == 9 and stats["a"][wa.ENGAGED_METRIC] == 3
    assert stats["b"][wa.SUBS_METRIC].startswith("refused: RuntimeError: HttpError 400")


# ------------------------------------------- privacy_status (2026-10-08)

def test_privacy_rides_on_the_listing_call_it_already_makes(monkeypatch):
    """No extra request: the uploads listing is asked for `status` too."""
    asked = []

    def listing(yt, part):
        asked.append(part)
        return [{"contentDetails": {"videoId": "a", "videoPublishedAt": "2026-10-01T06:00:00Z"},
                 "status": {"privacyStatus": "private"}},
                {"contentDetails": {"videoId": "b"}}]

    monkeypatch.setattr(wa.analytics, "list_uploaded_videos", listing)
    assert wa.all_uploads(object()) == [("a", "2026-10-01T06:00:00Z", "private"), ("b", "", "")]
    assert asked == ["contentDetails,status"]


def test_the_live_header_extends_by_two_columns_in_one_run(tmp_path):
    """The weekly job has not run since subs_gained was added, so its next run
    appends subs_gained and privacy_status together, to an LF header."""
    p = tmp_path / "snap.csv"
    body = b"2026-10-05,b,2026-09-01T06:00:00Z,7,0,0,0,1,12,60,3\r\n"
    p.write_bytes(",".join(LIVE).encode() + b"\n" + body)
    wa.ensure_header(p, wa.FIELDS)
    assert p.read_bytes() == ",".join(wa.FIELDS).encode() + b"\n" + body
    assert wa.FIELDS[len(LIVE):] == ["subs_gained", "privacy_status"]
