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
    held = table(weekly="2026-11-02", monthly="2026-10-31", prep="2026-10-03", planning="2026-10-04")
    assert "monthly" not in names(held, "2026-10-31", "2026-10-26")
    assert "monthly" in names(held, "2026-11-02", "2026-11-02")


def test_monthly_waits_for_the_months_first_weekly_review():
    # 2026-11-01 is a Sunday: the packet would read figures October's last
    # weekly already reviewed, a day before Monday's snapshot.
    before = table(weekly="2026-10-26", monthly="2026-10-05", prep="2026-10-05", planning="2026-10-10")
    assert names(before, "2026-11-01", "2026-10-26") == []
    assert names(before, "2026-11-02", "2026-11-02") == ["weekly"]
    after = table(weekly="2026-11-02", monthly="2026-10-05", prep="2026-10-05", planning="2026-10-10")
    assert names(after, "2026-11-02", "2026-11-02") == ["monthly"]


def test_monthly_comes_due_without_a_weekly_from_the_10th():
    # A broken snapshot job must not hide the monthly, or its overdue alarm.
    stuck = table(weekly="2026-10-26", monthly="2026-10-05", prep="2026-10-05", planning="2026-10-10")
    assert "monthly" not in names(stuck, "2026-11-09", "2026-10-26")
    assert "monthly" in names(stuck, "2026-11-10", "2026-10-26")
    late = dict(c.overdue(c.last_held(stuck), D("2026-11-20"), D("2026-10-26")))
    assert late == {"monthly": 46}


def test_quarterly_planning_waits_on_the_owner_after_prep():
    held = table(weekly="2026-10-06", monthly="2026-10-02", prep="2026-10-04")
    assert names(held, "2026-10-08", "2026-10-05") == ["quarterly planning"]
    done = table(weekly="2026-10-06", monthly="2026-10-02", prep="2026-10-04", planning="2026-10-07")
    assert names(done, "2026-10-08", "2026-10-05") == []
    assert names(done, "2027-01-02", "2026-10-05") == ["monthly"]   # the quarter's monthly first
    monthly_done = table(weekly="2026-10-06", monthly="2027-01-02", prep="2026-10-04", planning="2026-10-07")
    assert names(monthly_done, "2027-01-02", "2026-10-05") == ["quarterly prep"]


def test_only_long_overdue_reviews_are_a_process_failure():
    held = c.last_held(table(weekly="2026-09-01", monthly="2026-09-02", prep="2026-08-01"))
    late = dict(c.overdue(held, D("2026-10-05"), D("2026-10-05")))
    assert late == {"weekly": 34}          # monthly 33 days is not yet overdue


def test_the_real_plan_parses():
    held = c.last_held(open(c.PLAN).read())
    assert set(held) == {"weekly", "monthly", "quarterly prep", "quarterly planning"}


def test_a_late_weekly_on_old_figures_does_not_open_the_monthly():
    # The 10-26 snapshot reviewed late, on 11-01: the row says November, the figures October.
    late = table(weekly="2026-11-01", monthly="2026-10-05", prep="2026-10-05", planning="2026-10-10")
    assert names(late, "2026-11-01", "2026-10-26") == []


def test_an_overdue_monthly_stays_due_across_the_month_boundary():
    # November's was skipped: December must not wait for its first weekly.
    skipped = table(weekly="2026-11-30", monthly="2026-10-05", prep="2026-10-05", planning="2026-10-10")
    for day in ("2026-11-30", "2026-12-01", "2026-12-06"):
        assert "monthly" in names(skipped, day, "2026-11-30")
    late = dict(c.overdue(c.last_held(skipped), D("2026-12-01"), D("2026-11-30")))
    assert late == {"monthly": 57}


def test_quarterly_prep_follows_the_quarters_first_monthly_and_stays_due():
    december = table(weekly="2026-12-28", monthly="2026-12-07", prep="2026-10-05", planning="2026-10-10")
    assert names(december, "2027-01-01", "2026-12-28") == []          # January's monthly first
    january = table(weekly="2027-01-04", monthly="2027-01-04", prep="2026-10-05", planning="2026-10-10")
    assert names(january, "2027-01-04", "2027-01-04") == ["quarterly prep"]
    # Left undone past January, prep must not vanish while February waits for its monthly.
    for day in ("2027-02-01", "2027-02-09"):
        assert "quarterly prep" in names(january, day, "2027-01-25")
    assert dict(c.overdue(c.last_held(january), D("2027-02-01"), D("2027-01-25")))["quarterly prep"] == 119
