"""The unused-capacity alarm reads minutes from the usage ledger. It used to
compare self-reported percentages, which always add up, so two shifts that ran
8 and 7 of 25 minutes went unflagged (2026-09-24, 09-25)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import context_budget as cb

HEADER = "timestamp_utc,run_id,model,effort,turns,duration_min,quota_units,is_error\n"


def ledger(tmp_path, rows):
    p = tmp_path / "usage.csv"
    p.write_text(HEADER + "".join(f"t,{i},m,e,50,{m},1.0,{err}\n" for i, (m, err) in enumerate(rows)))
    return str(p)


def flagged(tmp_path, monkeypatch, rows):
    monkeypatch.setattr(cb, "LEDGER", ledger(tmp_path, rows))
    return [p for p in cb.health() if p[0] == "process-capacity-underused"]


def test_the_real_short_shifts_are_flagged(tmp_path, monkeypatch):
    problems = flagged(tmp_path, monkeypatch, [(24.4, 0), (8.0, 0), (6.9, 0)])
    assert problems and "ran 7, 8, 24 of their 60 minutes" in problems[0][2]
    assert "Ready work in the tracker now:" in problems[0][2]


def test_shifts_that_use_their_time_are_not(tmp_path, monkeypatch):
    assert not flagged(tmp_path, monkeypatch, [(58.0, 0), (52.0, 0), (55.0, 0)])


def test_a_failed_run_is_not_counted_as_a_short_shift(tmp_path, monkeypatch):
    # The Opus 5.5 failure recorded 0.0 minutes; it is not idleness.
    assert not flagged(tmp_path, monkeypatch, [(52.0, 0), (0.0, 1), (55.0, 0), (50.0, 0)])


def test_short_shifts_are_never_escalated_to_the_owner(tmp_path, monkeypatch):
    # The owner on #67: finding and fixing why shifts end early is the
    # shift's job, not theirs. It prints for the shift instead.
    monkeypatch.setattr(cb, "LEDGER", ledger(tmp_path, [(20.0, 0), (17.0, 0), (35.0, 0)]))
    calls = []
    monkeypatch.setattr(cb.subprocess, "run", lambda args, **kw: calls.append(args))
    assert any(p[0] == "process-capacity-underused" for p in cb.health(raise_issues=True))
    assert not any("process-capacity-underused" in a for a in calls)


def test_the_shift_is_told_what_waits_on_the_owner(tmp_path, monkeypatch):
    from scripts import backlog_status as b
    monkeypatch.setattr(cb, "LEDGER", ledger(tmp_path, [(20.0, 0), (17.0, 0), (35.0, 0)]))
    monkeypatch.setattr(b, "sources", lambda: [("company", (
        "## 3. Work queue\n\n| # | Status | Item |\n|---|---|---|\n"
        "| C1 | blocked: the owner's six checks (#59) | **Account check** |\n"
        "| C2 | blocked: the 2026-10-12 snapshot | **A read** |\n"), b.queue_section)])
    lines = "\n".join(b.short_shifts())
    assert "ran 35, 17, 20 of their 60 minutes" in lines and "#67" in lines
    assert "Account check: the owner's six checks (#59)" in lines
    assert "A read" not in lines


def test_nothing_is_printed_when_shifts_use_their_time(tmp_path, monkeypatch):
    from scripts import backlog_status as b
    monkeypatch.setattr(cb, "LEDGER", ledger(tmp_path, [(58.0, 0), (52.0, 0), (55.0, 0)]))
    assert b.short_shifts() == []
