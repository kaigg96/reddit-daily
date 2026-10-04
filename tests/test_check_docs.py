"""The tracker's checkable claims (scripts/check_docs.py). A false positive
here is not harmless: the fix a shift reaches for is deleting the citation."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import check_docs as c


def test_a_closed_issue_described_as_pending_is_caught():
    assert c.describes_as_open("Patch queued, awaiting #33's label.", 33)


def test_an_unrelated_open_elsewhere_on_a_long_row_is_not():
    row = ("| 1 | baking | **Open on the hook, not the format label** — "
           + "detail " * 30 + "Views never trigger (#18). |")
    assert not c.describes_as_open(row, 18)


def test_a_longer_number_is_not_the_cited_issue():
    assert not c.describes_as_open("#180 is still open", 18)


def test_only_the_newest_worklog_entry_is_read_as_current():
    log = ("# Work log\n\n```\n## 2026-09-21 — template\n```\n\n---\n\n"
           "## 2026-10-04 (07:37) — newest\n\n- Blocked on #45.\n\n"
           "## 2026-10-02 (15:52) — older\n\n- Waiting on your edit (issue #44).\n")
    entry = c.latest_worklog_entry(log)
    assert entry.startswith("## 2026-10-04") and "#45" in entry
    assert "#44" not in entry and "template" not in entry
