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
