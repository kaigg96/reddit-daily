"""report.py refuses to cut by a blind test's field before its read (the
11-05 peek at #14), unless --unblind gives a reason."""
import argparse
import datetime
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import report
from src import insights

D = datetime.date
LEDGER = [
    {"id": "#14", "due": "2026-11-23", "read": ""},
    {"id": "R7-voice-watch", "due": "2026-11-23", "read": "2026-11-20"},
]


def _args(by=None, compare=None, within=None, unblind=None, release=None,
          release_key="format_version"):
    return argparse.Namespace(by=by, compare=compare, within=within, unblind=unblind,
                              release=release, release_key=release_key)


def test_unread_row_before_its_due_date_is_blind():
    assert insights.blind_reads(["title_caps", "title_caps"], LEDGER, D(2026, 11, 6)) == [
        ("title_caps", "#14", D(2026, 11, 23))]


def test_due_date_read_row_and_unmapped_field_are_open():
    assert insights.blind_reads(["title_caps"], LEDGER, D(2026, 11, 23)) == []
    assert insights.blind_reads(["voice"], LEDGER, D(2026, 11, 6)) == []  # read early
    assert insights.blind_reads(["subreddit", "topic"], LEDGER, D(2026, 11, 6)) == []
    assert insights.blind_reads(["title_caps"], [{"id": "#14", "due": "", "read": ""}],
                                D(2026, 11, 6)) == []


@pytest.mark.parametrize("kw", [{"by": "title_caps"}, {"compare": "title_caps=1"},
                                {"within": "title_caps!=0"}, {"by": "title_hype"},
                                {"release": "1", "release_key": "title_caps"}])
def test_report_refuses_every_way_of_cutting_by_it(kw):
    with pytest.raises(SystemExit) as e:
        report.refuse_blind(_args(**kw), LEDGER, D(2026, 11, 6))
    assert "#14" in str(e.value) and "2026-11-23" in str(e.value) and "--unblind" in str(e.value)


def test_unblind_reads_and_says_so(capsys):
    report.refuse_blind(_args(by="title_caps", unblind="owner asked"), LEDGER, D(2026, 11, 6))
    assert "UNBLINDED #14 before 2026-11-23: owner asked" in capsys.readouterr().out
    report.refuse_blind(_args(by="subreddit"), LEDGER, D(2026, 11, 6))  # open: no exit
    report.refuse_blind(_args(release="v8"), LEDGER, D(2026, 11, 6))  # format_version


WEEKS = ("2026-10-19", "2026-10-26", "2026-11-02", "2026-11-09", "2026-11-16", "2026-11-23")
_ids = iter(range(10 ** 6))


def _log(arm_sizes, when="2026-11-10T07:00:00+00:00"):
    rows = [{"video_id": f"v{next(_ids)}", "timestamp_utc": "2026-10-14T07:00:00+00:00",
             "title_caps": "1"}]                                          # before 10-15
    for arm, n in arm_sizes.items():
        rows += [{"video_id": f"v{next(_ids)}", "timestamp_utc": when, "title_caps": arm}
                 for _ in range(n)]
    return rows + [{"video_id": f"v{next(_ids)}", "timestamp_utc": when, "title_caps": ""}
                   for _ in range(5)]                                     # fell back: unassigned


def _snaps(log, weeks=WEEKS):
    """The weekly series writes a row for every upload on each snapshot date."""
    when = [datetime.datetime.fromisoformat(w).replace(tzinfo=datetime.timezone.utc)
            for w in weeks]
    return {r["video_id"]: when for r in log}


def test_past_due_stays_blind_while_an_arm_is_under_its_floor():
    log = _log({"0": 32, "1": 29})
    assert insights.blind_arms(["title_caps", "title_hype"], LEDGER, D(2026, 11, 23), log,
                               _snaps(log)) == [("title_caps", "#14", 29, 30),
                                                ("title_hype", "#14", 29, 30)]
    with pytest.raises(SystemExit) as e:
        report.refuse_blind(_args(compare="title_caps=1"), LEDGER, D(2026, 11, 23), log,
                            _snaps(log))
    assert "the smaller holds 29" in str(e.value) and "--unblind" in str(e.value)


def test_floor_counts_the_cohort_an_at_age_read_takes():
    # An --at-age 7 read takes an upload 3.5 days old or more on a snapshot:
    # 11-19 07:00 is in 11-23's read, 11-19 19:00 is not (both in the short arm).
    late = _log({"1": 9}, when="2026-11-19T19:00:00+00:00")
    log = _log({"0": 30, "1": 28}) + late
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == [
        ("title_caps", "#14", 28, 30)]
    log += _log({"1": 2}, when="2026-11-19T07:00:00+00:00")
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == []
    # Before 11-23's snapshot lands, the newest is 11-16's, which reads to 11-12 12:00.
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log,
                               _snaps(log, WEEKS[:-1])) == [("title_caps", "#14", 28, 30)]


def test_floor_counts_from_the_coins_first_day():
    # Two real uploads went up on 10-15; _log's 10-14 row (arm 1) never counts.
    log = _log({"0": 30, "1": 29})
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == [
        ("title_caps", "#14", 29, 30)]
    log += _log({"1": 1}, when="2026-10-15T07:00:00+00:00")
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == []


def test_a_missed_snapshot_leaves_its_week_out_of_the_count():
    log = _log({"0": 30, "1": 30})          # 11-10: measured at 11-16 (5.7 days) only
    missed = tuple(w for w in WEEKS if w != "2026-11-16")
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == []
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log,
                               _snaps(log, missed)) == [("title_caps", "#14", 0, 30)]
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, {}) == [
        ("title_caps", "#14", 0, 30)]       # no series at all: nothing can be read


def test_floor_met_read_row_or_before_due_leaves_it_to_blind_reads():
    log = _log({"0": 30, "1": 30})
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log, _snaps(log)) == []
    report.refuse_blind(_args(by="title_caps"), LEDGER, D(2026, 11, 23), log, _snaps(log))
    read = [{"id": "#14", "due": "2026-11-23", "read": "2026-11-23"}]
    few = _log({"0": 3})
    assert insights.blind_arms(["title_caps"], read, D(2026, 11, 23), few, _snaps(few)) == []
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 6), few, _snaps(few)) == []
    assert insights.blind_arms(["voice"], LEDGER, D(2026, 11, 23), few, _snaps(few)) == []


def test_unblind_reads_under_the_floor_and_says_so(capsys):
    log = _log({"0": 32})
    report.refuse_blind(_args(by="title_caps", unblind="owner asked"), LEDGER,
                        D(2026, 11, 23), log, _snaps(log))
    assert "UNBLINDED #14 under its floor (0 of 30 per arm): owner asked" in capsys.readouterr().out


def test_every_floor_names_a_blind_test():
    assert set(insights.BLIND_FLOORS) <= set(insights.BLIND_FIELDS.values())


def test_every_blind_field_names_a_ledger_row():
    # A renamed row, or an unread one whose due date does not parse, would
    # silently unblind its field.
    rows = {r["id"]: r for r in insights.load_experiments()}
    for test in set(insights.BLIND_FIELDS.values()):
        assert test in rows
        assert rows[test]["read"].strip() or insights._ledger_date(rows[test]["due"])
