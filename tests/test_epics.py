"""The epic board is read and checked by one command (scripts/epics.py, E2 T1).
Each fault --check names has its own synthetic board here, and the committed
board in epics/ must pass."""
import datetime as dt
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import epics as ep

DAY = dt.date(2026, 11, 16)
NOON = dt.datetime(2026, 11, 16, 12, 0, tzinfo=dt.timezone.utc)

HEAD = """# E{n} · Epic {n}
Status: {status}
Function: Engineering
Deadline: none
Measure: something
Rule: keep if it works

## Tickets
"""

TICKET = """
### T{n} · Ticket {n}
Status: {status}
Needs: {needs}
Touches: scripts/
Context: enough to start cold
Accept:
- [ ] a line someone can check
Evidence: {evidence}
"""


def epic(n=1, status="active", tickets=()):
    return HEAD.format(n=n, status=status) + "".join(
        TICKET.format(**{"needs": "none", "evidence": "", "status": "todo", **t})
        for t in tickets)


def write(tmp_path, files):
    for name, text in files.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    return str(tmp_path)


def run_check(tmp_path, files, now=NOON):
    epics = ep.board(write(tmp_path, files))
    errors, _ = ep.check(epics, now=now, date_of=lambda _p: DAY)
    return errors


CLEAN = {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "done", "evidence": "abc123, 5 pass"},
                                     {"n": 2, "status": "ready", "needs": "T1"},
                                     {"n": 3, "status": "doing: 123, 11:00", "needs": "T1"}]),
         "E2-b.md": epic(2, "proposed (challenged 11-15)",
                         tickets=[{"n": 1, "status": "todo", "needs": "E1 T2"}])}


def test_clean_board_passes(tmp_path):
    assert run_check(tmp_path, CLEAN) == []


def test_main_check_exits_zero_on_clean_and_one_on_a_fault(tmp_path, capsys):
    d = write(tmp_path, CLEAN)
    assert ep.main(["--check", "--dir", d, "--now", "2026-11-16 12:00"],
                   date_of=lambda _p: DAY) == 0
    (tmp_path / "E3-c.md").write_text(epic(3, "wobbly"), encoding="utf-8")
    assert ep.main(["--check", "--dir", d, "--now", "2026-11-16 12:00"],
                   date_of=lambda _p: DAY) == 1
    assert "E3-c.md:2: unknown epic status `wobbly`" in capsys.readouterr().out


def test_missing_header_line_is_named_with_file_and_line(tmp_path):
    text = epic(1).replace("Measure: something\n", "")
    errors = run_check(tmp_path, {"E1-a.md": text})
    assert len(errors) == 1 and errors[0].endswith("E1-a.md:5: missing header line `Measure:`")


def test_missing_title_line(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1).replace("# E1 · Epic 1", "# Epic one")})
    assert any(e.endswith("E1-a.md:1: first line is not `# E<n> · name`") for e in errors)


def test_ticket_missing_a_field(tmp_path):
    text = epic(1, tickets=[{"n": 1}]).replace("Touches: scripts/\n", "")
    errors = run_check(tmp_path, {"E1-a.md": text})
    assert errors == [f"{tmp_path}/E1-a.md:10: T1 is missing `Touches:`"]


def test_unknown_ticket_status(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "started"}])})
    assert len(errors) == 1 and "E1-a.md:11: T1 has unknown status `started`" in errors[0]


def test_unknown_epic_status(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1, "underway")})
    assert len(errors) == 1 and "E1-a.md:2: unknown epic status `underway`" in errors[0]


def test_needs_a_ticket_that_does_not_exist_in_the_same_epic(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1, tickets=[{"n": 1, "needs": "T1, T7"}])})
    assert len(errors) == 1 and "E1-a.md:12: T1 needs T7, which does not exist" in errors[0]


def test_needs_a_ticket_that_does_not_exist_across_epics(tmp_path):
    files = {"E1-a.md": epic(1, tickets=[{"n": 1}]),
             "E2-b.md": epic(2, tickets=[{"n": 1, "needs": "E1 T1, E1 T4, E9 T1"}])}
    errors = run_check(tmp_path, files)
    assert len(errors) == 2
    assert "E2-b.md:12: T1 needs E1 T4, which does not exist" in errors[0]
    assert "E2-b.md:12: T1 needs E9 T1, which does not exist" in errors[1]


def test_done_with_empty_evidence(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "done"}])})
    assert len(errors) == 1 and "E1-a.md:17: T1 is done with an empty `Evidence:`" in errors[0]


def test_evidence_on_following_lines_counts(tmp_path):
    text = epic(1, tickets=[{"n": 1, "status": "done"}]) + "commit abc, 12 pass\n"
    assert run_check(tmp_path, {"E1-a.md": text}) == []


def test_doing_older_than_twelve_hours(tmp_path):
    files = {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "doing: 4385, 23:30 (note)"}])}
    late = dt.datetime(2026, 11, 17, 11, 29, tzinfo=dt.timezone.utc)
    assert run_check(tmp_path, files, now=late) == []                  # 11 h 59 m
    later = dt.datetime(2026, 11, 17, 11, 31, tzinfo=dt.timezone.utc)
    errors = run_check(tmp_path, files, now=later)
    assert len(errors) == 1 and "E1-a.md:11: T1 has been doing for 12 hours" in errors[0]


def test_doing_with_a_full_date_ignores_the_file_date(tmp_path):
    files = {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "doing: 4385, 2026-11-15 11:00"}])}
    errors = run_check(tmp_path, files)                                 # 25 h before NOON
    assert len(errors) == 1 and "since 2026-11-15 11:00 UTC" in errors[0]


def test_doing_with_no_time(tmp_path):
    errors = run_check(tmp_path, {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "doing: 4385"}])})
    assert len(errors) == 1 and "T1 is doing with no UTC time" in errors[0]


def test_more_than_two_active_epics(tmp_path):
    files = {f"E{n}-x.md": epic(n) for n in (1, 2, 3)}
    errors = run_check(tmp_path, files)
    assert len(errors) == 3 and all(":2: 3 epics are active, at most 2" in e for e in errors)
    files["E3-x.md"] = epic(3, "approved")
    assert run_check(tmp_path, files) == []


def test_status_keyword_ignores_what_follows():
    assert ep.keyword("ready: `process/lessons.md` seeded") == "ready"
    assert ep.keyword("review: `product/e1-t2-music` (`e1f8b5d`)") == "review"
    assert ep.keyword("proposed (challenged and amended)") == "proposed"
    assert ep.keyword("doing: 43856314698, 11:36 (note)") == "doing"
    assert ep.keyword("dropped") == "dropped"


def test_listing_groups_tickets_by_status(tmp_path, capsys):
    d = write(tmp_path, CLEAN)
    assert ep.main(["--dir", d]) == 0
    out = capsys.readouterr().out
    assert "E1 · Epic 1  [active]" in out and "E2 · Epic 2  [proposed]" in out
    assert out.index("  ready (1)\n    T2 · Ticket 2") < out.index("  done (1)\n    T1 · Ticket 1")
    assert "  doing (1)\n    T3 · Ticket 3" in out


def _next(tmp_path, files):
    return ep.next_action(ep.board(write(tmp_path, files)))


def test_next_follows_the_four_roles_in_order(tmp_path):
    files = {"E1-a.md": epic(1, tickets=[{"n": 1, "status": "done", "evidence": "x"},
                                         {"n": 2, "status": "ready", "needs": "T1"},
                                         {"n": 3, "status": "ready", "needs": "T4"},
                                         {"n": 4, "status": "todo"}]),
             "E2-b.md": epic(2, "approved"),
             "E3-c.md": epic(3, "proposed", tickets=[{"n": 1, "status": "review: branch x"}])}
    assert _next(tmp_path, files).startswith("ACCEPT E3 T1 · Ticket 1")
    files["E3-c.md"] = epic(3, "proposed", tickets=[{"n": 1, "status": "ready"}])
    # a ready ticket whose Needs is not done, or of an epic not active, is not dispatched
    assert _next(tmp_path, files).startswith("DISPATCH E1 T2 · Ticket 2")
    assert "1 ready in active epics" in _next(tmp_path, files)
    files["E1-a.md"] = epic(1, tickets=[{"n": 1, "status": "todo"}])
    assert _next(tmp_path, files).startswith("PLAN E2 · Epic 2")
    files["E2-b.md"] = epic(2, "done")
    assert _next(tmp_path, files).startswith("GENERATE AND FILTER")


def test_file_date_reads_an_untracked_file_by_its_mtime(tmp_path):
    path = tmp_path / "E1-a.md"
    path.write_text("x", encoding="utf-8")
    os.utime(path, (1_700_000_000, 1_700_000_000))                      # 2023-11-14
    assert ep.file_date(str(path)) == dt.date(2023, 11, 14)


def test_committed_board_passes(capsys):
    """The board as committed, checked for form. A `doing` ticket's age depends
    on the clock and on clone depth (CI checks out one commit, so every file
    dates from HEAD); staleness has its own tests above, so here every
    `doing` time is read as not yet begun."""
    future = lambda path: dt.date(2100, 1, 1)
    assert ep.main(["--check", "--now", "2000-01-01 00:00"], date_of=future) == 0, \
        capsys.readouterr().out
    assert ep.main([]) == 0 and ep.main(["--next"]) == 0


BRIEF_BOARD = {
    "E1-a.md": HEAD.format(n=1, status="active").replace(
        "## Tickets", "Prose only the epic has: zebra crossing.\n\n## Tickets") + """
### T1 · Make the widget wobble
Status: ready: orchestrator's note, marmalade
Needs: none
Touches: src/widget.py, tests/test_widget.py
Context: the widget is still
Accept:
- [ ] `pytest tests/test_widget.py` passes
- [ ] the wobble is visible in a frame,
  wrapped onto a second line
Evidence: grapefruit, from an earlier bounce
and a second evidence line, kumquat

### T2 · Paint the sibling shed
Status: todo
Needs: T1
Touches: src/shed.py
Context: the shed is grey
Accept:
- [ ] the shed is teal
Evidence:
""",
    "E2-b.md": epic(2, tickets=[{"n": 1}]).replace("Ticket 1", "Polish the other epic's lantern"),
}


def test_brief_is_its_ticket_alone(tmp_path, capsys):
    d = write(tmp_path, BRIEF_BOARD)
    assert ep.main(["brief", "E1", "T1", "--dir", d]) == 0
    out = capsys.readouterr().out
    assert "### T1 · Make the widget wobble" in out
    assert "Touches: src/widget.py, tests/test_widget.py" in out
    assert "- [ ] `pytest tests/test_widget.py` passes" in out
    assert "  wrapped onto a second line" in out
    assert "branch named `e1-t1-<slug>`" in out
    for foreign in ("zebra", "Epic 1", "shed", "teal", "lantern", "Epic 2",     # sibling, epic
                    "marmalade", "grapefruit", "kumquat"):                    # Status, Evidence
        assert foreign not in out, foreign
    assert '"Merge once the gates pass: tests green,' in out and "SAMPLE=1" in out
    assert "## Lessons that apply to you" in out     # which ones: the fixture test below


def test_lessons_match_a_clause_opening_with_the_role_or_any(tmp_path):
    """Read from a fixture, not the live file, which every round edits."""
    path = tmp_path / "lessons.md"
    path.write_text("## L1 · Orchestrator only\nApplies: orchestrator (acceptance)\n\n"
                    "## L2 · Implementer second\nApplies: orchestrator; implementer, `src/**`\n\n"
                    "## L3 · Any on files\nApplies: orchestrator (records); any, `PLAN.md`\n\n"
                    "## L4 · Any first\nApplies: any (research)\n\n"
                    "## L5 · Mentions the word only\nApplies: generator (not the implementer)\n",
                    encoding="utf-8")
    assert ep.lessons_for("implementer", str(path)) == [
        "L2 · Implementer second", "L3 · Any on files", "L4 · Any first"]


def test_brief_ends_with_the_report_format(tmp_path, capsys):
    assert ep.main(["brief", "E1", "T1", "--dir", write(tmp_path, BRIEF_BOARD)]) == 0
    out = capsys.readouterr().out.rstrip()
    block = out[out.rindex("```", 0, len(out) - 3):].splitlines()
    assert out.endswith("Learned: anything the next person on this file should know "
                        "(one line each)\n```")
    assert block[1] == "Branch: e1-t1-<slug> (commit abc1234)"
    assert ('- [ ] "the wobble is visible in a frame, wrapped onto a second line": '
            "<command run> -> <its output, copied>") in block
    # the same fields, in the same order, as process/epics.md's "The implementer"
    doc = open(os.path.join(ep.ROOT, "process", "epics.md"), encoding="utf-8").read()
    doc = doc.split("## The implementer", 1)[1].split("```")[1]
    def labels(lines):
        return [l.split(":")[0] for l in lines if l.strip() and not l.startswith(("-", "`"))]
    assert labels(block) == labels(doc.splitlines()) == \
        ["Branch", "Changed", "Accept", "Could not do", "Learned"]


def test_brief_of_an_unknown_ticket_exits_non_zero(tmp_path, capsys):
    d = write(tmp_path, BRIEF_BOARD)
    for args in (["E1", "T9"], ["E9", "T1"], ["E1"]):
        assert ep.main(["brief", *args, "--dir", d]) != 0
        err = capsys.readouterr()
        assert err.out == "" and len(err.err.strip().splitlines()) == 1, args


def test_brief_of_a_committed_ticket(capsys):
    """The sentences the brief quotes from CLAUDE.md and process/epics.md are
    still there to quote."""
    assert ep.main(["brief", "E2", "T4"]) == 0
    assert capsys.readouterr().out.startswith("# Brief: E2 T4 · ")


def test_needs_none_with_a_note_names_no_ticket():
    assert ep.needs_refs("none (E1 T7 for the play-along form)") == []
    assert ep.needs_refs("T1, E1 T3") == [("", "1"), ("1", "3")]
