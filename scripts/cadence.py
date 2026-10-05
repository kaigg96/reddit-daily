#!/usr/bin/env python3
"""Which of the company's reviews are due (ORG.md §5).

Functions on slower clocks (strategy, money, policy, market, audience) get
their turn in a review, not in a time slice of every shift. A due review is
that shift's work (`/review`). This decides "due" from facts, not from a
shift's sense of whether it has been a while:

    weekly             the newest analytics snapshot is newer than the last weekly review
    monthly            no monthly review yet this calendar month
    quarterly prep     no packet prepared yet this quarter (the agent drafts the bets)
    quarterly planning prepared, but not yet held with the owner -- never a shift's to do

PLAN.md §5 records when each was last held. A review updates its own row.

    venv/bin/python scripts/cadence.py          # what is due, most important first
    venv/bin/python scripts/cadence.py --next   # just the first due review's name
"""
import csv
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "PLAN.md")
SNAPSHOTS = os.path.join(ROOT, "analysis", "analytics_snapshots.csv")

# The order a shift takes them in when several are due. Monthly first: it is
# the one that reaches the owner, and its findings feed the quarter's packet.
ORDER = ["monthly", "weekly", "quarterly prep"]
# Overdue by this many days and the process has a problem worth escalating
# (context_budget.py --health). Generous: a review a few days late is normal.
OVERDUE_DAYS = {"weekly": 14, "monthly": 45, "quarterly prep": 100}


def last_held(text):
    """{review name (lowercase): date or None} from PLAN.md §5."""
    m = re.search(r"^## 5\..*", text, re.S | re.M)
    out = {}
    for line in (m.group(0) if m else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not line.startswith("|") or cells[0].lower() == "review":
            continue
        if set(cells[0]) <= set("-: "):
            continue
        hit = re.search(r"\d{4}-\d{2}-\d{2}", cells[1])
        out[cells[0].lower()] = datetime.date.fromisoformat(hit.group(0)) if hit else None
    return out


def newest_snapshot(path=SNAPSHOTS):
    """The latest snapshot_date in the weekly analytics file, or None."""
    try:
        with open(path, encoding="utf-8") as f:
            dates = [r["snapshot_date"] for r in csv.DictReader(f) if r.get("snapshot_date")]
    except (OSError, KeyError):
        return None
    return datetime.date.fromisoformat(max(dates)) if dates else None


def _quarter(d):
    return (d.year, (d.month - 1) // 3)


def due(held, today, snapshot):
    """[(review, why)] due today, in ORDER, plus quarterly planning if waiting."""
    out = []
    monthly = held.get("monthly")
    if monthly is None or (monthly.year, monthly.month) < (today.year, today.month):
        out.append(("monthly", f"last held {monthly or 'never'}"))
    weekly = held.get("weekly")
    if snapshot and (weekly is None or snapshot > weekly):
        out.append(("weekly", f"snapshot of {snapshot} not yet reviewed "
                              f"(last weekly {weekly or 'never'})"))
    prep = held.get("quarterly prep")
    if prep is None or _quarter(prep) < _quarter(today):
        out.append(("quarterly prep", f"no packet yet this quarter (last {prep or 'never'})"))
    plan = held.get("quarterly planning")
    if prep and _quarter(prep) == _quarter(today) and (plan is None or plan < prep):
        out.append(("quarterly planning", "packet prepared; waiting on the owner's session"))
    return out


def overdue(held, today, snapshot):
    """Reviews due for longer than OVERDUE_DAYS -- a process failure, not a delay."""
    late = []
    for review, _ in due(held, today, snapshot):
        if review not in OVERDUE_DAYS:
            continue
        last = held.get(review)
        if last is not None and (today - last).days > OVERDUE_DAYS[review]:
            late.append((review, (today - last).days))
    return late


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        text = open(PLAN, encoding="utf-8").read()
    except OSError:
        print("PLAN.md not found")
        return 1
    today = datetime.datetime.now(datetime.timezone.utc).date()
    found = due(last_held(text), today, newest_snapshot())
    shift_work = [(r, why) for r, why in found if r in ORDER]
    if "--next" in argv:
        print(shift_work[0][0] if shift_work else "")
        return 0
    if not found:
        print("No review is due.")
        return 0
    for review, why in found:
        mark = "DUE   " if review in ORDER else "OWNER "
        print(f"{mark}{review}: {why}")
    if shift_work:
        print(f"\nThis shift's work: /review {shift_work[0][0]} (one review per shift).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
