"""Reviews give the slower functions their turn (ORG.md §5). "Due" must come from
facts -- the newest data and the calendar -- not from a shift's sense of time."""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import cadence as c

D = dt.date.fromisoformat


def table(weekly="never", monthly="never", prep="never", planning="never"):
    return f"""## 4. Risks

| Review | Last held |
|---|---|
| fake row outside §5 | 2000-01-01 |

## 5. Reviews

| Review | Last held |
|---|---|
| Weekly | {weekly} |
| Monthly | {monthly} |
| Quarterly prep | {prep} |
| Quarterly planning | {planning} |
"""


def names(text, today, snapshot):
    return [r for r, _ in c.due(c.last_held(text), D(today), D(snapshot) if snapshot else None)]


def test_never_held_means_all_due_with_monthly_first():
    assert names(table(), "2026-10-05", "2026-10-05") == ["monthly", "weekly", "quarterly prep"]


def test_weekly_follows_the_data_not_the_calendar():
    held = table(weekly="2026-10-06", monthly="2026-10-02", prep="2026-10-03", planning="2026-10-04")
    assert names(held, "2026-10-11", "2026-10-05") == []          # no new snapshot yet
    assert names(held, "2026-10-13", "2026-10-12") == ["weekly"]  # Monday's arrived


def test_monthly_is_due_once_per_calendar_month():
    held = table(weekly="2026-10-06", monthly="2026-10-31", prep="2026-10-03", planning="2026-10-04")
    assert "monthly" not in names(held, "2026-10-31", "2026-10-05")
    assert "monthly" in names(held, "2026-11-01", "2026-10-05")


def test_quarterly_planning_waits_on_the_owner_after_prep():
    held = table(weekly="2026-10-06", monthly="2026-10-02", prep="2026-10-04")
    assert names(held, "2026-10-08", "2026-10-05") == ["quarterly planning"]
    done = table(weekly="2026-10-06", monthly="2026-10-02", prep="2026-10-04", planning="2026-10-07")
    assert names(done, "2026-10-08", "2026-10-05") == []
    assert "quarterly prep" in names(done, "2027-01-02", "2026-10-05")


def test_only_long_overdue_reviews_are_a_process_failure():
    held = c.last_held(table(weekly="2026-09-01", monthly="2026-09-02", prep="2026-08-01"))
    late = dict(c.overdue(held, D("2026-10-05"), D("2026-10-05")))
    assert late == {"weekly": 34}          # monthly 33 days is not yet overdue


def test_the_real_plan_parses():
    held = c.last_held(open(c.PLAN).read())
    assert set(held) == {"weekly", "monthly", "quarterly prep", "quarterly planning"}
