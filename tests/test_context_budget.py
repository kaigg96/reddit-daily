"""The time-by-function reader /audit uses. It reads the new "Worked" line and
the old planned-vs-actual one, so the history stays whole across the change."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import context_budget  # noqa: E402

WORKLOG = """# Work log

```
## 2026-09-21 — one line on what actually mattered

    Allocation (planned→actual %): rounds 10→8 · feature 30→40 · close 10→10
```

---

## 2026-10-06 (09:30) — a shift after the change

    Worked (% of the shift): reliability 10 · product 60 · gm 30

## 2026-09-29 (17:52) — a real shift

    Allocation (planned→actual %): rounds 10→10 · security 5→0 · feature 0→0 · close 10→10
"""


def test_the_header_template_is_not_read_as_the_newest_shift():
    """Until 2026-09-29 the template's feature 30→40 was read as the newest row."""
    entries = context_budget.allocation_entries(WORKLOG)
    assert [label[:18] for label, _ in entries] == ["2026-10-06 (09:30)", "2026-09-29 (17:52)"]


def test_both_formats_record_the_share_actually_worked():
    new, old = (row for _, row in context_budget.allocation_entries(WORKLOG))
    assert new == {"reliability": 10, "product": 60, "gm": 30}
    assert old["feature"] == 0 and old["security"] == 0 and old["rounds"] == 10


def test_every_function_in_org_md_is_known():
    """The short names a WORKLOG entry may use are ORG.md's fourteen functions."""
    import re
    org = open(os.path.join(os.path.dirname(__file__), "..", "ORG.md")).read()
    assert len(re.findall(r"^#### ", org, re.M)) == len(context_budget.FUNCTIONS) == 14


def _entry(stamp, headline, worked):
    return f"\n## {stamp} — {headline}\n\n    Worked (% of the shift): {worked}\n"


def test_a_restamped_shift_is_counted_once():
    """10-24's shift was stamped 09:05, then 08:50 with the same headline; the
    10-25 audit found --allocation counting it twice."""
    current = "# Work log\n" + _entry("2026-10-25 (08:25)", "newest", "product 100")
    newer = current + _entry("2026-10-24 (08:50)", "Rewording made it worse", "gm 100")
    older = current + _entry("2026-10-24 (09:05)", "Rewording made it worse", "gm 100") \
        + _entry("2026-10-23 (22:55)", "a different shift", "data 100")
    labels = [label[:18] for label, _ in context_budget.merge_versions([current, newer, older])]
    assert labels == ["2026-10-25 (08:25)", "2026-10-24 (08:50)", "2026-10-23 (22:55)"]


def test_two_shifts_on_one_day_stay_two():
    current = "# Work log\n" + _entry("2026-10-25 (08:25)", "newest", "product 100")
    old = current + _entry("2026-10-24 (22:30)", "evening", "gm 100") \
        + _entry("2026-10-24 (15:30)", "afternoon", "gm 100")
    assert len(context_budget.merge_versions([current, old])) == 3


def test_a_restamp_that_also_rewords_is_counted_once_by_its_summary():
    """10-18 08:45 became 08:50 with a reworded headline; the summary stayed."""
    def entry(stamp, headline, summary):
        return _entry(stamp, headline, "gm 100") + f"\n**Summary:** {summary}\n"
    current = "# Work log\n" + _entry("2026-10-19 (09:50)", "newest", "product 100")
    newer = current + entry("2026-10-18 (08:50)", "Bet 1 still waits, reworded", "Nothing reached viewers.")
    older = current + entry("2026-10-18 (08:45)", "Bet 1 still waits", "Nothing reached viewers.") \
        + entry("2026-10-18 (14:35)", "another shift", "Something else happened.")
    labels = [label[:18] for label, _ in context_budget.merge_versions([current, newer, older])]
    assert labels == ["2026-10-19 (09:50)", "2026-10-18 (14:35)", "2026-10-18 (08:50)"]
