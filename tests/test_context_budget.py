"""The allocation reader behind the starvation floor."""

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

## 2026-09-29 (17:52) — a real shift

    Allocation (planned→actual %): rounds 10→10 · security 5→0 · feature 0→0 · close 10→10
"""


def test_the_header_template_is_not_read_as_the_newest_shift():
    """Until 2026-09-29 the template's feature 30→40 was the newest row, so
    the feature lane could never be flagged starved."""
    entries = context_budget.allocation_entries(WORKLOG)
    assert [label for label, _ in entries] == ["2026-09-29 (17:52) — a real "]
    assert entries[0][1]["feature"] == (0, 0)


def test_security_is_a_lane():
    assert "security" in context_budget.LANES
