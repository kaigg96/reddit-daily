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


def test_every_blind_field_names_a_ledger_row():
    # A renamed row, or an unread one whose due date does not parse, would
    # silently unblind its field.
    rows = {r["id"]: r for r in insights.load_experiments()}
    for test in set(insights.BLIND_FIELDS.values()):
        assert test in rows
        assert rows[test]["read"].strip() or insights._ledger_date(rows[test]["due"])
