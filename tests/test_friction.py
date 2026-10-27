"""The friction log (DECISIONS.md D15). The work log's friction notes stopped
on 10-08 and nobody noticed for three weeks, so the rule that judges this log
is pinned to its code, its seed rows stay out of every read, and a silent
stop reaches the owner."""
import csv
import datetime as dt
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import context_budget as cb

# The bare name, as context_budget.health imports it, so one module is patched.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import friction as fr  # noqa: E402

UTC = dt.timezone.utc
START = "2026-11-01T10:00:00+00:00"
LEDGER_HEADER = "timestamp_utc,run_id,model,effort,turns,duration_min,quota_units,is_error\n"


def t(day, hour=12, minute=0):
    return dt.datetime(2026, 11, day, hour, minute, tzinfo=UTC)


def row(i, when, category="tool", group="", fixes="", function="gm",
        run_id="1", minutes="5"):
    return {"id": f"F{i}", "timestamp_utc": when.isoformat(), "run_id": run_id,
            "function": function, "task": "x", "outcome": "done", "fixes": fixes,
            "category": category, "hardest": "" if category == "none" else "h",
            "helped": "", "minutes_lost": minutes, "group": group}


def groups_file(tmp_path, groups=(("G1", "open", "", ""),)):
    p = tmp_path / "groups.csv"
    with open(p, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(fr.GROUP_FIELDS)
        for gid, status, item, resolved in groups:
            w.writerow([gid, "title", status, item, "2026-10-01", resolved, ""])
    return str(p)


def ledger(tmp_path, shifts, name="usage.csv"):
    p = tmp_path / name
    p.write_text(LEDGER_HEADER + "".join(
        f"{end.isoformat()},{rid},m,e,50,{mins},1.0,{err}\n"
        for end, mins, rid, err in shifts))
    return str(p)


@pytest.fixture
def started(monkeypatch):
    monkeypatch.setattr(fr, "START", START)


# ---------------------------------------------------------------- the rule

def test_d15_states_every_threshold_the_code_uses():
    # A changed number must change in DECISIONS.md and here together.
    assert fr.rule_text().startswith("**Decision rule**")
    assert fr.drift() == []


def test_a_changed_threshold_is_caught(monkeypatch):
    monkeypatch.setattr(fr, "LOG_SHARE", 0.7)
    assert any("70%+" in p for p in fr.drift())


def test_evaluate_quotes_the_rule_before_any_number(tmp_path, capsys, started):
    fr.evaluate(rows=[row(1, t(2))], groups=[], ledger=ledger(tmp_path, []), now=t(3))
    out = capsys.readouterr().out
    assert fr.rule_text() in out
    first_check = re.search(r"\n  \(a\) [A-Z]", out).start()
    assert out.index("**Decision rule**") < out.index("\nSTART: ") < first_check


# ---------------------------------------------------------------- add

def test_add_refuses_what_the_rule_could_not_read(tmp_path):
    log, groups = str(tmp_path / "f.csv"), groups_file(tmp_path)
    for kw in ({"function": "marketing"}, {"outcome": "finished"},
               {"category": "slow"}, {"hardest": ""}, {"helped": ""},
               {"minutes": ""}, {"minutes": "ten"}, {"group": "G9"},
               {"fixes": "G9"}, {"task": "two\nlines"}):
        args = dict(function="gm", task="t", outcome="done", category="tool",
                    hardest="h", helped="p", minutes="5")
        args.update(kw)
        with pytest.raises(ValueError):
            fr.add(**args, path=log, groups_path=groups)
    assert not os.path.exists(log)


def test_none_is_a_real_answer_and_needs_nothing_else(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_RUN_ID", "777")
    log = str(tmp_path / "f.csv")
    r = fr.add("data", "Read a test", "done", "none", path=log,
               groups_path=groups_file(tmp_path), now=t(2))
    assert r["id"] == "F1" and r["minutes_lost"] == "0" and r["run_id"] == "777"
    assert fr.load(log)[0]["category"] == "none"


def test_add_appends_after_the_seed_with_the_next_id(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
    log = tmp_path / "f.csv"
    log.write_text(",".join(fr.FIELDS) + "\nF26,2026-10-27T00:00:00+00:00,local,gm,"
                   "x,done,,rules,h,p,10,G1")             # no trailing newline
    r = fr.add("engineering", 'A "quoted", task', "partial", "allowance",
               "render slot used", "a second slot", "blocked", group="G1",
               path=str(log), groups_path=groups_file(tmp_path))
    rows = fr.load(str(log))
    assert [x["id"] for x in rows] == ["F26", "F27"] and r["run_id"] == "local"
    assert rows[1]["task"] == 'A "quoted", task' and rows[1]["minutes_lost"] == "blocked"


def test_the_seed_files_parse_and_use_only_known_values():
    rows, groups = fr.load(), fr.load_groups()
    assert rows and groups
    known = {g["group"] for g in groups}
    for r in rows:
        assert list(r) == fr.FIELDS
        assert r["function"] in fr.FUNCTIONS and r["category"] in fr.CATEGORIES
        assert r["outcome"] in fr.OUTCOMES and r["group"] in known
    assert all(g["status"] in fr.STATUSES for g in groups)


# ---------------------------------------------------------------- the window

def test_nothing_is_read_before_start(monkeypatch):
    # Unset until the landing commit: no read, no alarm.
    if fr.START is None:
        assert fr.window(fr.load()) == []
        assert fr.gaps(ledger=cb.LEDGER) == []
    # Set, at any landing time, the seed stays out: every seed row is
    # "backfill", so the 10-27 one is out even if it landed that morning.
    monkeypatch.setattr(fr, "START", fr.START or "2026-10-27T09:00:00+00:00")
    seed = [r for r in fr.load() if int(r["id"][1:]) <= 26]
    assert seed and all(r["run_id"] == "backfill" for r in seed)
    assert not set(r["id"] for r in fr.window(fr.load())) & set(r["id"] for r in seed)


def test_a_bare_date_start_is_refused(monkeypatch):
    # "2026-10-27" would read as midnight and let that day's rows in.
    monkeypatch.setattr(fr, "START", "2026-10-27")
    with pytest.raises(ValueError):
        fr.window(fr.load())


def test_the_backfill_and_rows_before_start_stay_out(started):
    rows = [row(1, t(1, 9), run_id="backfill"), row(2, t(1, 9, 59), run_id="local"),
            row(3, t(1, 10)), row(4, t(3))]
    assert [r["id"] for r in fr.window(rows)] == ["F3", "F4"]


# ---------------------------------------------------------------- gaps

def test_gaps_match_rows_to_shifts_by_time_or_run(tmp_path, started):
    led = ledger(tmp_path, [
        (t(1, 9), 30, "100", 0),        # before START: not counted
        (t(2, 10), 60, "200", 0),       # row at 08:56: inside [08:55, 10:05] by the slack
        (t(3, 10), 60, "300", 0),       # row at 10:06: just outside
        (t(4, 10), 60, "400", 0),       # matched by run id
        (t(5, 10), 60, "500", 1),       # a failed run: not a shift
    ])
    rows = [row(1, t(2, 8, 56), run_id="local"), row(2, t(3, 10, 6), run_id="local"),
            row(3, t(9), run_id="400"), row(4, t(6, 10, 4), run_id="local")]
    led2 = ledger(tmp_path, [(t(6, 10), 60, "600", 0)], "usage2.csv")  # row at 10:04: after the end, by the slack
    assert [(s["run_id"], s["logged"]) for s in fr.gaps(rows, led)] == \
        [("200", True), ("300", False), ("400", True)]
    assert [s["logged"] for s in fr.gaps(rows, led2)] == [True]


def test_three_silent_shifts_reach_the_owner(tmp_path, monkeypatch, started):
    led = ledger(tmp_path, [(t(d, 10), 50, str(d), 0) for d in (2, 3, 4, 5)])
    monkeypatch.setattr(cb, "LEDGER", led)
    monkeypatch.setattr(fr, "load", lambda path=None: [row(1, t(2, 9, 30), run_id="x")])
    assert fr.silent_run(ledger=led) == 3
    calls = []

    def run(args, **kw):
        calls.append(args)
        return cb.subprocess.CompletedProcess(args, 0, "queued", "")
    monkeypatch.setattr(cb.subprocess, "run", run)
    problems = cb.health(raise_issues=True)
    assert any(p[0] == "process-friction-silent" for p in problems)
    assert "process-friction-silent" not in cb.SHIFT_OWNED
    assert any("process-friction-silent" in a for a in calls)


def test_two_silent_shifts_do_not(tmp_path, monkeypatch, started):
    led = ledger(tmp_path, [(t(d, 10), 50, str(d), 0) for d in (2, 3, 4)])
    monkeypatch.setattr(cb, "LEDGER", led)
    monkeypatch.setattr(fr, "load", lambda path=None: [row(1, t(2, 9, 30), run_id="x")])
    assert fr.silent_run(ledger=led) == 2
    assert not any(p[0] == "process-friction-silent" for p in cb.health())


# ---------------------------------------------------------------- report

def test_leverage_ranks_and_blocked_counts_as_an_hour():
    rows = [row(1, t(1), group="G1", minutes="blocked", function="engineering"),
            row(2, t(1), group="G1", minutes="10", function="gm"),
            row(3, t(1), group="G2", minutes="5"),
            row(4, t(1), group="G3", minutes="")]
    assert fr.leverage("G1", rows) == (2, 35, 2, 140, True)
    assert fr.leverage("G2", rows)[3] == 5
    assert fr.leverage("G3", rows)[4] is False      # minutes unknown: shown as "?"


def test_a_fixed_group_logged_again_is_flagged_recurred(capsys):
    groups = [{"group": "G1", "title": "slot", "status": "fixed", "item": "C9",
               "resolved": "2026-11-05", "opened": "", "note": ""},
              {"group": "G2", "title": "docs", "status": "fixed", "item": "C8",
               "resolved": "2026-11-05", "opened": "", "note": ""}]
    rows = [row(1, t(5, 23), group="G1"), row(2, t(6), group="G1"),
            row(3, t(4), group="G2"), row(4, t(7))]
    out = fr.report(rows, groups, now=t(10))
    assert [g["group"] for g, _ in out["recurred"]] == ["G1"]
    assert [r["id"] for r in out["ungrouped"]] == ["F4"]
    text = capsys.readouterr().out
    assert "RECURRED" in text and "F2" in text and "holding: G2" in text


# ---------------------------------------------------------------- evaluate

def fixed(gid, resolved, item="C9"):
    return {"group": gid, "title": "", "status": "fixed", "item": item,
            "resolved": resolved, "opened": "", "note": ""}


def verdict_of(tmp_path, rows, groups, now, shifts):
    results = fr.checks(rows, groups, ledger(tmp_path, shifts), now)
    return fr.verdict(results), {c[0]: c[4] for c in results}


def healthy(n_shifts=10):
    """Shifts that each logged a row, about a quarter of them "none"."""
    shifts, rows = [], []
    for i in range(n_shifts):
        end = t(1, 12) + dt.timedelta(days=3 * i)
        shifts.append((end, 40, str(i), 0))
        cat = "none" if i % 4 == 0 else "tool"
        rows.append(row(i, end - dt.timedelta(minutes=10), category=cat,
                        group="" if cat == "none" else "G1", run_id=str(i)))
    return shifts, rows


def test_not_yet_under_28_days(tmp_path, started):
    shifts, rows = healthy(4)
    (v, _), by = verdict_of(tmp_path, rows, [], t(20), shifts)
    assert v == "not yet" and by["a"] == "pass" and by["e"] == "not yet"


def test_not_yet_without_a_fix_14_days_old(tmp_path, started):
    shifts, rows = healthy()
    groups = [fixed("G1", "2026-11-25"), fixed("G2", "2026-11-26")]
    (v, _), by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 2, tzinfo=UTC), shifts)
    assert v == "not yet" and by["f"] == "not yet"


def test_keep_when_two_fixes_shipped_and_one_held(tmp_path, started):
    # Every shift logs; a quarter "none"; G1 had 3 rows before its 11-08 fix
    # and none after; fix rows are 2 of 17.
    shifts = [(t(1, 12) + dt.timedelta(days=d), 40, str(d), 0) for d in range(0, 30, 2)]
    rows = []
    for i, (end, _, rid, _) in enumerate(shifts):
        when = end - dt.timedelta(minutes=5)
        if i % 4 == 3:
            rows.append(row(i, when, category="none", run_id=rid))
        else:
            rows.append(row(i, when, group="G1" if end <= t(7, 23) else "G3", run_id=rid))
    rows.append(row(99, t(8), fixes="G1", category="none", run_id="x"))
    rows.append(row(98, t(9), fixes="G2", category="none", run_id="x"))
    groups = [fixed("G1", "2026-11-08"), fixed("G2", "2026-11-09")]
    (v, why), by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 3, tzinfo=UTC), shifts)
    assert by == {"a": "pass", "b": "pass", "c": "judge", "d": "pass", "e": "pass",
                  "f": "pass", "g": "pass", "h": "judge"}
    assert v == "keep" and "judgement" in why


def test_a_fix_that_did_not_hold_fails_f(tmp_path, started):
    shifts = [(t(1, 12) + dt.timedelta(days=d), 40, str(d), 0) for d in range(0, 30, 2)]
    rows = [row(i, s[0] - dt.timedelta(minutes=5), group="G1", run_id=s[2])
            for i, s in enumerate(shifts)]
    rows += [row(100 + i, s[0] - dt.timedelta(minutes=4), category="none", run_id=s[2])
             for i, s in enumerate(shifts[::3])]
    groups = [fixed("G1", "2026-11-08"), fixed("G2", "2026-11-09")]
    (v, why), by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 3, tzinfo=UTC), shifts)
    assert by["e"] == "pass" and by["f"] == "fail"
    assert v == "change" and "processed" in why and "stop" in why


def test_a_held_fix_passes_f(tmp_path, started):
    shifts = [(t(1, 12) + dt.timedelta(days=d), 40, str(d), 0) for d in range(0, 30, 2)]
    rows = [row(i, s[0] - dt.timedelta(minutes=5),
                group="G1" if s[0] <= t(7, 23) else "", run_id=s[2],
                category="tool" if s[0] <= t(7, 23) else "none")
            for i, s in enumerate(shifts)]
    rows += [row(200, t(20), fixes="G1", category="none", run_id="x")]
    groups = [fixed("G1", "2026-11-08"), fixed("G2", "2026-11-09")]
    _, by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 3, tzinfo=UTC), shifts)
    assert by["f"] == "pass"


def test_fixes_before_start_do_not_count_for_e(tmp_path, started):
    shifts, rows = healthy()
    groups = [fixed("G5", "2026-09-29", "report.py"), fixed("G7", "2026-10-01")]
    _, by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 2, tzinfo=UTC), shifts)
    assert by["e"] == "fail"


def test_too_many_none_rows_fail_b_and_point_at_writing(tmp_path, started):
    shifts, _ = healthy()
    rows = [row(i, s[0] - dt.timedelta(minutes=5), category="none", run_id=s[2])
            for i, s in enumerate(shifts)]
    groups = [fixed("G1", "2026-11-05"), fixed("G2", "2026-11-06")]
    (v, why), by = verdict_of(tmp_path, rows, groups, dt.datetime(2026, 12, 2, tzinfo=UTC), shifts)
    assert by["b"] == "fail" and v == "change" and "written" in why


def test_a_stale_ungrouped_row_fails_d(tmp_path, started):
    rows = [row(1, t(2)), row(2, t(10), category="none")]
    _, by = verdict_of(tmp_path, rows, [], t(9, 20), [])   # 7 days 8 hours
    assert by["d"] == "fail"
    _, by = verdict_of(tmp_path, rows, [], t(9, 12), [])   # exactly 7 days
    assert by["d"] == "pass"


def test_only_the_guardrail_failing_says_so(started):
    results = [(k, "", "", "", "pass") for k in "abdef"] + \
        [("c", "", "", "", "judge"), ("g", "", "", "", "fail"), ("h", "", "", "", "judge")]
    v, why = fr.verdict(results)
    assert v == "change" and "guardrail (g)" in why and "processed" not in why


def test_a_collection_failure_shows_before_the_monthly_read(started):
    results = [(k, "", "", "", "pass") for k in "bdg"] + [("a", "", "", "", "fail")] + \
        [(k, "", "", "", "not yet") for k in "ef"] + \
        [(k, "", "", "", "judge") for k in "ch"]
    v, why = fr.verdict(results)
    assert v == "not yet" and "failing now: (a)" in why


def test_a_bad_byte_in_the_log_does_not_stop_the_other_checks(tmp_path, monkeypatch, capsys, started):
    bad = tmp_path / "f.csv"
    bad.write_bytes(b"id,timestamp_utc\nF1,\xff\xfe\n")
    monkeypatch.setattr(fr, "LOG", str(bad))
    monkeypatch.setattr(cb, "LEDGER", ledger(tmp_path, [(t(2), 50, "1", 0)]))
    cb.health()
    assert "FRICTION CHECK FAILED" in capsys.readouterr().out


def test_fix_rows_over_a_third_trip_the_guardrail(tmp_path, capsys, started):
    rows = [row(1, t(2), fixes="G1", group="G1"), row(2, t(3), group="G1"),
            row(3, t(4), fixes="G1", group="G1")]
    v, results = fr.evaluate(rows=rows, groups=[], ledger=ledger(tmp_path, []),
                             now=t(5), seed=1)
    assert {c[0]: c[4] for c in results}["g"] == "fail"
    out = capsys.readouterr().out
    assert "GUARDRAIL tripped" in out and "random rows" in out


def test_unset_start_reads_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fr, "START", None)
    v, _ = fr.evaluate(rows=[row(1, t(2))], groups=[], ledger=ledger(tmp_path, []),
                       now=t(5))
    assert v == "not yet" and "has not landed" in capsys.readouterr().out
