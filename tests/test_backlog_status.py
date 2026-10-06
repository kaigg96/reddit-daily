"""Ready work is the supply a shift can act on now (scripts/backlog_status.py).
A lane full of blocked items looked non-empty, so nothing generated more work
and two shifts ended with most of their time unspent (2026-09-24, 09-25)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import backlog_status as b

TRACKER = """## 0. Delivery plan

#### Next keepers

| Item | Status | Req | Decision rule |
|---|---|---|---|
| **Free samples** — reuse narration | ready | — | done when a sample costs nothing |
| ~~Old screen~~ | done | R4.6 | shipped |

#### Experiment backlog

| # | Status | Item | Req | Decision rule (pre-committed) |
|---|---|---|---|---|
| 1 | baking | **New opening** | — | judge after 20 uploads |
| 2 | blocked: sample video | Ranker | R4.4 | keep if … a | b | c |
| 3 | parked: needs volume | Upload time | R4.5 | later |

#### Research questions

| # | Status | Question | Test |
|---|---|---|---|
| 1 | ready | Do question titles hold viewers longer? | report.py --by title_style |

| Item | Req | Decision rule |
|---|---|---|
| a table without a Status column is not counted | — | — |

## 1. Next section
| 9 | ready | outside §0 is not counted | — |
"""


def test_only_ready_work_counts_as_supply():
    assert b.ready(TRACKER) == ["Free samples", "Do question titles hold viewers longer?"]


def test_every_row_is_classified_and_blocked_work_keeps_its_reason():
    got = {name: (status, raw) for status, raw, name in b.items(TRACKER)}
    assert got["Ranker"] == ("blocked", "blocked: sample video")
    assert got["New opening"][0] == "baking" and got["Upload time"][0] == "parked"
    assert len(got) == 6        # a pipe inside a cell does not add a row


def test_the_real_tracker_is_well_formed():
    """Runs on every push: a row without a known status -- or a row cut off
    from its table, as happened once -- fails here, not in a shift's count."""
    text = open(b.PRD).read()
    rows = b.items(text)
    assert rows, "no §0 table with a Status column"
    bad = [(status, name) for status, _, name in rows if status not in b.STATUSES]
    assert not bad, f"unknown statuses: {bad}"
    section = b.section0(text)
    assert "#### Research questions" in section and "| # | Status | Question | Test |" in section
    assert not b.malformed(text), f"rows cut off from their table: {b.malformed(text)}"


def test_a_row_cut_off_from_its_table_is_caught():
    broken = TRACKER.replace("| shipped |\n\n#### Experiment", "| shipped |\n\n#### Experiment")
    broken = broken.replace("| ~~Old screen~~", "\n| ~~Old screen~~")
    assert b.malformed(broken) == ["| ~~Old screen~~ | done | R4.6 | shipped |"]
    assert b.malformed(TRACKER) == []


def test_answered_research_questions_leave_the_tracker():
    """The research table is a queue, not an archive: §0 is read every shift, so
    an answered row that stays is context every shift pays for, forever."""
    text = open(b.PRD).read()
    section = b.section0(text)
    table = section.split("#### Research questions", 1)[1].split("####", 1)[0]
    rows = [line for line in table.splitlines() if line.startswith("|")][2:]
    lingering = [r[:70] for r in rows
                 if b._cells(r)[1].strip("` ").split(":")[0].lower() not in ("ready", "blocked")]
    assert not lingering, f"answered research rows still in §0: {lingering}"


def test_the_company_queue_is_well_formed_and_counted():
    """PLAN.md §3 feeds the same queue as PRD §0, under the same statuses."""
    text = open(b.PLAN).read()
    rows = b.items(text, b.queue_section)
    assert rows, "no PLAN.md §3 table with a Status column"
    bad = [(status, name) for status, _, name in rows if status not in b.STATUSES]
    assert not bad, f"unknown statuses: {bad}"
    assert not b.malformed(text, b.queue_section)
    assert all(name.startswith(("[product] ", "[company] ")) for name in b.ready_all())
