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
        # A live row stays ungrouped until the weekly review sorts it; the
        # seed rows were all sorted when they were written.
        blank = set() if r["run_id"] == "backfill" else {""}
        assert r["outcome"] in fr.OUTCOMES and r["group"] in known | blank
        assert r["fixes"] in known | {""}
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


def test_three_silent_shifts_are_the_shifts_to_fix(tmp_path, monkeypatch, started):
    """Until D16 (2026-11-14) this reached the owner; now nothing does."""
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
    assert calls == []


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


# ---------------------------------------------------------------- requests
# D15, amended 2026-11-20: a retro a shift, one vote citing its own row.

REQ_START = "2026-11-01T10:00:00+00:00"


@pytest.fixture
def reqs(tmp_path, monkeypatch):
    """Files for the requests, the shift's own run id, REQ_START set."""
    monkeypatch.setenv("GITHUB_RUN_ID", "100")
    monkeypatch.setattr(fr, "REQ_START", REQ_START)
    log = tmp_path / "f.csv"
    with open(log, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fr.FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows([row(1, t(2), run_id="100", minutes="10", group="G1"),
                     row(2, t(2), run_id="100", category="none", minutes="0"),
                     row(3, t(2), run_id="99", minutes="10"),
                     row(4, t(2), run_id="100", minutes="blocked")])
    return {"path": str(tmp_path / "v.csv"), "requests_path": str(tmp_path / "r.csv"),
            "rows_path": str(log),
            "groups_path": groups_file(tmp_path, (("G1", "open", "", ""),
                                                  ("G2", "open", "", "")))}


def cast(files, now=None, **kw):
    args = dict(row="F1", saved="5", why="it would have")
    args.update(kw)
    return fr.vote(**args, now=now or t(2, 13), **files)


def test_d15_states_every_requests_threshold():
    assert fr.rule_text(label="Requests rule").startswith("**Requests rule**")
    assert fr.drift_requests() == []


def test_a_changed_requests_threshold_is_caught(monkeypatch):
    monkeypatch.setattr(fr, "BAR_VOTES", 4)
    assert any("four votes" in p for p in fr.drift_requests())


def test_a_vote_that_is_not_evidence_is_refused(reqs):
    for kw in ({"row": "F3"},                   # another shift's row
               {"row": "F2"},                   # a "none" row lost nothing
               {"row": "F9"},                   # no such row
               {"saved": "11"},                 # more than the row lost
               {"saved": "0"}, {"saved": "ten"},
               {"why": ""}, {"why": "two\nlines"},
               {"row": ""},
               {"request": "R1"},               # two choices, with new
               {"new": ""}):                    # no choice
        with pytest.raises(ValueError):
            cast(reqs, **{"new": "a thing", **kw})
    assert fr.load_votes(reqs["path"]) == []
    assert fr.load_requests(reqs["requests_path"]) == []


def test_a_blocked_row_backs_up_to_an_hour(reqs):
    v, r = cast(reqs, new="a thing", row="F4", saved="60")
    assert v["saved"] == "60" and r["request"] == "R1"


def test_one_retro_a_shift_and_one_vote_a_row(reqs, monkeypatch):
    v, r = cast(reqs, new="Compute the render slot")
    assert (v["id"], v["request"], r["group"]) == ("V1", "R1", "G1")  # the row's group
    with pytest.raises(ValueError, match="already held its retro"):
        cast(reqs, request="R1", row="F4")
    monkeypatch.setenv("GITHUB_RUN_ID", "101")
    with pytest.raises(ValueError, match="already backs V1"):
        cast(reqs, request="R1")


def test_an_abstention_is_a_retro_with_its_reason(reqs):
    v, r = fr.vote(none=True, why="nothing a change would have saved",
                   now=t(2, 13), **reqs)
    assert r is None and v["request"] == "none" and v["row"] == ""
    with pytest.raises(ValueError):
        fr.vote(none=True, row="F1", why="x", now=t(2, 13), **reqs)


def test_a_duplicate_request_in_a_group_is_refused_unless_distinct(reqs, monkeypatch):
    cast(reqs, new="Compute the render slot")
    monkeypatch.setenv("GITHUB_RUN_ID", "101")
    reqs_rows = reqs["rows_path"]
    fr._append(reqs_rows, fr.FIELDS, row(5, t(3), run_id="101", group="G1"))
    with pytest.raises(ValueError, match="G1 already has an open request: R1"):
        cast(reqs, new="Render twice a shift", row="F5", now=t(3, 13))
    v, r = cast(reqs, new="Render twice a shift", row="F5", distinct=True,
                now=t(3, 13))
    assert r["request"] == "R2"


def test_local_sessions_cite_recent_local_rows(reqs, monkeypatch):
    monkeypatch.delenv("GITHUB_RUN_ID")
    fr._append(reqs["rows_path"], fr.FIELDS, row(5, t(3, 9), run_id="local"))
    with pytest.raises(ValueError, match="not logged by this shift"):
        cast(reqs, new="x", row="F5", now=t(4, 9))      # 24 hours old
    v, _ = cast(reqs, new="x", row="F5", now=t(3, 12))
    assert v["run_id"] == "local"


def votes_for(spec):
    """spec: [(request, run_id, saved, day)] -> vote rows."""
    return [{"id": f"V{i}", "timestamp_utc": t(day).isoformat(), "run_id": rid,
             "request": req, "row": f"F{i}", "saved": str(s), "why": "w"}
            for i, (req, rid, s, day) in enumerate(spec, 1)]


def request(rid, status="open", item="", group="", resolved=""):
    return {"request": rid, "title": f"title {rid}", "group": group,
            "status": status, "item": item, "opened": "2026-11-01",
            "resolved": resolved, "note": ""}


def test_merged_votes_count_and_the_bar_needs_different_shifts():
    reqs = [request("R1"), request("R2", "merged", "R1"), request("R3")]
    votes = votes_for([("R1", "1", 5, 2), ("R2", "2", 4, 3), ("R3", "3", 20, 3),
                       ("R1", "local", 2, 4), ("R1", "local", 1, 5)])
    t_ = fr.tally(reqs, votes)
    assert "R2" not in t_ and t_["R1"]["saved"] == 12 and t_["R1"]["shifts"] == 4
    assert t_["R1"]["bar"] == t(4)                    # the third shift's vote
    assert [x["req"]["request"] for x in fr.ranked(reqs, votes)] == ["R3", "R1"]
    assert [x["req"]["request"] for x in fr.due(reqs, votes)] == ["R1"]


def test_shipping_a_request_marks_its_group_fixed_for_d15(reqs, started):
    rp, gp = reqs["requests_path"], reqs["groups_path"]
    cast(reqs, new="Compute the render slot")
    r, g = fr.mark("R1", "queued", "C21", requests_path=rp, groups_path=gp, now=t(3))
    assert r["status"] == "queued" and (g["status"], g["item"]) == ("queued", "C21")
    r, g = fr.mark("R1", "shipped", "abc123", requests_path=rp, groups_path=gp, now=t(4))
    assert (g["status"], g["resolved"], g["item"]) == ("fixed", "2026-11-04", "abc123")
    groups = fr.load_groups(gp)
    e = {c[0]: c for c in fr.checks(rows=[], groups=groups, ledger=None, now=t(4))}["e"]
    assert e[2] == "1"                                  # D15 (e) counts it
    with pytest.raises(ValueError):
        fr.mark("R1", "shipped", "again", requests_path=rp, groups_path=gp)


def test_the_queue_cap_and_the_marks_that_need_a_value(tmp_path):
    rp, gp = str(tmp_path / "r.csv"), groups_file(tmp_path)
    fr._write_all(rp, fr.REQUEST_FIELDS, [request("R1", "queued", "C1"),
                                          request("R2", "queued", "C2"),
                                          request("R3"), request("R4", "merged", "R3")])
    with pytest.raises(ValueError, match="2 requests are queued"):
        fr.mark("R3", "queued", "C3", requests_path=rp, groups_path=gp)
    for status, value in (("declined", ""), ("merged", "R3"), ("merged", "R4"),
                          ("merged", "R9")):
        with pytest.raises(ValueError):
            fr.mark("R3", status, value, requests_path=rp, groups_path=gp)
    with pytest.raises(ValueError, match="R4 is merged"):
        fr.mark("R4", "declined", "x", requests_path=rp, groups_path=gp)
    r, _ = fr.mark("R3", "declined", "loses to bet 1", requests_path=rp,
                   groups_path=gp, now=t(5))
    assert (r["status"], r["note"], r["resolved"]) == ("declined", "loses to bet 1",
                                                       "2026-11-05")


def test_a_vote_for_a_closed_request_is_refused(reqs):
    fr._write_all(reqs["requests_path"], fr.REQUEST_FIELDS,
                  [request("R1", "shipped", "abc", resolved="2026-11-01"),
                   request("R2", "declined"), request("R3", "merged", "R2")])
    for rid in ("R1", "R2", "R3", "R9"):
        with pytest.raises(ValueError):
            cast(reqs, request=rid)


def test_the_requests_rule_reads_not_yet_then_fails_what_it_should(tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "REQ_START", REQ_START)
    shifts = [(t(d, 12), 30, str(d), 0) for d in range(2, 12)]
    led = ledger(tmp_path, shifts)
    votes = votes_for([("R1", str(d), 5, d) for d in (2, 3, 4)]
                      + [("none", str(d), "", d) for d in (5, 6)])
    for v in votes:
        v["timestamp_utc"] = t(int(v["run_id"]), 11, 50).isoformat()
    reqs = [request("R1")]
    early = {c[0]: c[4] for c in fr.request_checks(votes, reqs, led, now=t(12))}
    assert early == {"r1": "fail", "r2": "pass", "r3": "not yet", "r4": "not yet",
                     "r5": "pass"}                      # 5 of 10 shifts held one
    v, why = fr.request_verdict(list(fr.request_checks(votes, reqs, led, now=t(12))),
                                now=t(12))
    assert v == "not yet" and "failing now: (r1)" in why
    late = fr.request_checks(votes, reqs, led, now=t(30))
    by = {c[0]: c[4] for c in late}
    assert by["r3"] == "fail" and by["r4"] == "fail" and by["r5"] == "fail"
    v, why = fr.request_verdict(late, now=t(30))
    assert v == "change" and "verdict is stop" in why


def test_evaluate_requests_quotes_its_rule_before_any_number(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(fr, "REQ_START", REQ_START)
    fr.evaluate_requests(votes=[], reqs=[], ledger=ledger(tmp_path, []), now=t(3))
    out = capsys.readouterr().out
    assert fr.rule_text(label="Requests rule") in out
    assert (out.index("**Requests rule**") < out.index("\nREQ_START: ")
            < out.index("\n  (r1) "))


def test_the_retro_shows_the_shifts_rows_and_says_when_it_is_held(reqs, capsys):
    rows = fr.load(reqs["rows_path"])
    assert fr.retro(rows=rows, reqs=[], votes=[], now=t(2, 13)) is None
    out = capsys.readouterr().out
    assert "3 rows, 2 to cite" in out and "F3" not in out and "vote --none" in out
    held = votes_for([("R1", "100", 5, 2)])
    assert fr.retro(rows=rows, reqs=[request("R1")], votes=held, now=t(2, 13))
    assert "Retro held: V1" in capsys.readouterr().out


def test_the_request_files_parse_and_use_only_known_values():
    reqs, votes = fr.load_requests(), fr.load_votes()
    with open(fr.REQUESTS) as f:
        assert f.readline().strip().split(",") == fr.REQUEST_FIELDS
    with open(fr.VOTES) as f:
        assert f.readline().strip().split(",") == fr.VOTE_FIELDS
    ids = {r["request"] for r in reqs}
    assert all(r["status"] in fr.REQUEST_STATUSES for r in reqs)
    assert all(v["request"] in ids | {"none"} for v in votes)


def test_backlog_status_hands_requests_past_the_bar_to_the_ranking(monkeypatch, capsys):
    from scripts import backlog_status as bs
    monkeypatch.setattr(fr, "load_requests", lambda path=None: [request("R1", group="G2")])
    monkeypatch.setattr(fr, "load_votes", lambda path=None: votes_for(
        [("R1", str(d), 5, d) for d in (2, 3, 4)]))
    lines = bs.friction_requests()
    assert lines and "R1" in lines[1] and "15 min" in lines[1]
