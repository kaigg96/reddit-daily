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
