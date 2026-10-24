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


_OLD = """## 2026-10-16 (22:36) — older shift

### Done
- **Considered and dropped:** likes per view (a median of 0).
- **Security:** clean.

## 2026-10-14 (09:40) — oldest shift

- **Ranked and dropped** (eight candidates): retention curves, which need
  a workflow change.
"""

_NEW = """# Work log

## 2026-10-17 (14:13) — newest shift

- **Engineering:** a fix, which dropped nothing.
- **Considered and dropped:** a spelling guard (1 in 50).

## 2026-10-16 (22:36) — older shift

- **Considered and dropped:** likes per view, edited later.
"""


def test_dropped_candidates_are_read_per_entry_and_wrapped_lines_joined():
    got = dict(b.dropped_in(_OLD))
    assert got["2026-10-16 (22:36) — older shift"] == [
        "Considered and dropped: likes per view (a median of 0)."]
    assert got["2026-10-14 (09:40) — oldest shift"] == [
        "Ranked and dropped (eight candidates): retention curves, which need "
        "a workflow change."]


def test_a_bullet_that_only_mentions_dropping_is_not_a_dropped_list():
    assert "2026-10-17 (14:13) — newest shift" in dict(b.dropped_in(_NEW))
    assert dict(b.dropped_in(_NEW))["2026-10-17 (14:13) — newest shift"] == [
        "Considered and dropped: a spelling guard (1 in 50)."]


def test_entries_pruned_from_the_worklog_are_still_listed_newest_first():
    got = b.recently_dropped(versions=[_NEW, _OLD])
    assert [h for h, _ in got] == ["2026-10-17 (14:13) — newest shift",
                                   "2026-10-16 (22:36) — older shift",
                                   "2026-10-14 (09:40) — oldest shift"]
    # The newest version of an entry wins over the one it was edited from.
    assert got[1][1] == "Considered and dropped: likes per view, edited later."
    assert len(b.recently_dropped(limit=2, versions=[_NEW, _OLD])) == 2


def test_a_shift_that_restamped_or_reworded_its_heading_is_one_entry():
    restamped = _OLD.replace("(22:36) — older shift", "(22:31) — older shift")
    reworded = _OLD.replace("(22:36) — older shift", "(22:36) — older, reworded")
    got = b.recently_dropped(versions=[_NEW, restamped, reworded])
    assert [h for h, _ in got] == ["2026-10-17 (14:13) — newest shift",
                                   "2026-10-16 (22:36) — older shift",
                                   "2026-10-14 (09:40) — oldest shift"]


def test_indented_lines_of_a_later_bullet_stay_out_of_the_dropped_one():
    text = ("## 2026-10-17 (08:00) — X\n"
            "- **Considered and dropped:** a.\n"
            "- **Security:** clean, and\n"
            "  more security text.\n"
            "### Next\n"
            "  indented note\n")
    assert b.dropped_in(text) == [("2026-10-17 (08:00) — X", ["Considered and dropped: a."])]


def test_drops_listed_inside_a_bullet_are_read_from_their_label_on():
    """Since 10-20 drops sit inside the General management bullet, which the
    opening match missed, so nothing newer than 10-20 was listed (10-24)."""
    text = ("## 2026-10-24 (15:30) — X\n\n### Done\n"
            "- **General management:** nothing was ready. Two survived. **Dropped:** draft\n"
            "  answers (the form's questions were never recorded); affiliate links.\n"
            "- **Product:** the filter dropped nothing new. **Also:** x.\n"
            "- **The vote no longer gets dropped for running long.** A fix.\n"
            "- **Dropped after ranking** (eight): likes.\n"
            "- **Data:** read it. **Considered and dropped:** a subscriber rate.\n")
    assert b.dropped_in(text) == [("2026-10-24 (15:30) — X", [
        "Dropped: draft answers (the form's questions were never recorded); affiliate links.",
        "Dropped after ranking (eight): likes.",
        "Considered and dropped: a subscriber rate."])]
    done = b.done_in(text)[0][1]       # a headline saying "dropped" is done work
    assert any(d.startswith("The vote no longer") for d in done)
    assert not any(d.startswith("Dropped after") for d in done)


def test_a_chain_of_edits_to_time_and_headline_is_still_one_shift():
    def v(time, headline):
        return f"## 2026-10-17 ({time}) — {headline}\n- **Considered and dropped:** a.\n"
    got = b.recently_dropped(versions=[v("08:28", "Y"), v("08:28", "X"), v("08:24", "X")])
    assert [h for h, _ in got] == ["2026-10-17 (08:28) — Y"]


def test_the_real_history_reads_without_error_even_in_a_shallow_clone():
    got = b.recently_dropped(limit=3)
    assert len(got) <= 3 and all(bullet for _, bullet in got)


def test_done_work_is_listed_too_so_it_is_not_proposed_again():
    text = ("## 2026-10-19 (09:45) — X\n\n### Toward revenue\n"
            "- **Bet 2's date.** It needs #77 labelled by about 1 November. More\n"
            "  detail here.\n\n### Done\n"
            "- **Strategy:** volume priced. It caps near 6.\n"
            "- **Considered and dropped:** likes.\n\n### Next\n- Read Sunday's figures.\n")
    opening = "Bet 2's date. It needs #77 labelled by about 1 November. More detail here."
    assert b.done_in(text) == [("2026-10-19 (09:45) — X", [
        opening, "Strategy: volume priced. It caps near 6."])]
    got = b.recently_dropped(versions=[text], extract=b.done_in)
    assert got == [("2026-10-19 (09:45) — X", opening + " | Strategy: volume priced. It caps near 6.")]
    assert b._clip("a" * 10 + " bbbb", 12) == "a" * 10 + " …"
    assert b.recently_dropped(versions=[text]) == [
        ("2026-10-19 (09:45) — X", "Considered and dropped: likes.")]


def test_the_worklog_template_in_a_fence_is_not_a_done_entry():
    text = ("```\n## 2026-10-06 — one line\n### Done\n- **Engineering:** x.\n```\n"
            "## 2026-10-21 (16:50) — real\n### Done\n- **Data:** y.\n")
    assert b.done_in(text) == [("2026-10-21 (16:50) — real", ["Data: y."])]
