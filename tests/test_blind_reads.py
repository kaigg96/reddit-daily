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


def _log(arm_sizes, day="2026-11-10"):
    rows = [{"timestamp_utc": "2026-10-14T07:00:00+00:00", "title_caps": "1"}]  # before 10-15
    for arm, n in arm_sizes.items():
        rows += [{"timestamp_utc": f"{day}T07:00:00+00:00", "title_caps": arm}] * n
    return rows + [{"timestamp_utc": f"{day}T19:00:00+00:00", "title_caps": ""}] * 5


def test_past_due_stays_blind_while_an_arm_is_under_its_floor():
    log = _log({"0": 32, "1": 29})
    assert insights.blind_arms(["title_caps", "title_hype"], LEDGER, D(2026, 11, 23), log) == [
        ("title_caps", "#14", 29, 30), ("title_hype", "#14", 29, 30)]
    with pytest.raises(SystemExit) as e:
        report.refuse_blind(_args(compare="title_caps=1"), LEDGER, D(2026, 11, 23), log)
    assert "the smaller holds 29" in str(e.value) and "--unblind" in str(e.value)


def test_floor_counts_only_what_a_7_day_read_sees():
    # Uploads from the last 7 days are not yet 7 days old, so they do not count.
    log = _log({"0": 30, "1": 25}) + _log({"1": 5}, day="2026-11-17")
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log) == [
        ("title_caps", "#14", 25, 30)]
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 24), log) == []


def test_floor_met_read_row_or_before_due_leaves_it_to_blind_reads():
    log = _log({"0": 30, "1": 30})
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 23), log) == []
    report.refuse_blind(_args(by="title_caps"), LEDGER, D(2026, 11, 23), log)  # open
    read = [{"id": "#14", "due": "2026-11-23", "read": "2026-11-23"}]
    assert insights.blind_arms(["title_caps"], read, D(2026, 11, 23), _log({"0": 3})) == []
    assert insights.blind_arms(["title_caps"], LEDGER, D(2026, 11, 6), _log({"0": 3})) == []
    assert insights.blind_arms(["voice"], LEDGER, D(2026, 11, 23), _log({"0": 3})) == []


def test_unblind_reads_under_the_floor_and_says_so(capsys):
    report.refuse_blind(_args(by="title_caps", unblind="owner asked"), LEDGER,
                        D(2026, 11, 23), _log({"0": 32}))
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
