"""Measured quota: the reading, the owner's reserve, and pacing to the reset.

The reserve is the owner's protection for their own use of Claude, and these
tests are what CI holds it to (guardrails.yml runs them on every push)."""
import csv
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import quota  # noqa: E402
import shift_budget  # noqa: E402
import statusline  # noqa: E402

UTC = datetime.timezone.utc
RESET = datetime.datetime(2026, 11, 27, 18, tzinfo=UTC).timestamp()   # a Friday
H = 3600


def event(five, seven, five_resets=None, seven_resets=RESET):
    """Exactly the shape Claude Code 2.1.278 emitted on 2026-11-21."""
    return {"type": "rate_limit_event", "rate_limit_info": {
        "status": "allowed", "rateLimitType": "five_hour", "overageStatus": "rejected",
        "unifiedWindows": {
            "five_hour": {"utilization": five, "resetsAt": five_resets or RESET - 100 * H},
            "seven_day": {"utilization": seven, "resetsAt": seven_resets}}},
        "uuid": "x", "session_id": "y"}


def reading(five, seven, now, five_resets_in=4 * H, seven_resets=RESET):
    return quota.from_event(event(five / 100, seven / 100, now + five_resets_in, seven_resets))


def measured(n, weekly=4.0, five=20.0, minutes=60):
    return [{"weekly_used": str(weekly), "five_hour_used": str(five),
             "duration_min": str(minutes)} for _ in range(n)]


def test_the_owners_reserve_is_as_set():
    """97% 5h always (owner, 2026-11-21: "use it all, always"); 90% weekly; the
    last 12h before the reset open the weekly reserve (owner, 2026-11-20) up to
    98, short of the hard limit."""
    assert (quota.RESERVE_5H, quota.RESERVE_7D) == (97.0, 90.0)
    assert (quota.LATE_HOURS, quota.LATE_CEILING_7D) == (12, 98.0)


def test_reads_the_event_and_nothing_else():
    r = quota.from_event(event(0.66, 0.09))
    assert r["five_hour"]["used_percentage"] == 66.0
    assert r["seven_day"] == {"used_percentage": 9.0, "resets_at": int(RESET)}
    assert quota.from_event({"type": "assistant"}) is None
    assert quota.from_event({"type": "rate_limit_event", "rate_limit_info": {}}) is None
    bad = event("lots", 0.1)
    assert "five_hour" not in quota.from_event(bad)


def test_first_and_last_from_an_array_or_lines(tmp_path):
    msgs = [{"type": "system"}, event(0.1, 0.2), {"type": "assistant"}, event(0.3, 0.25),
            {"type": "result", "total_cost_usd": 1}]
    arr = tmp_path / "a.json"
    arr.write_text(json.dumps(msgs, indent=2))
    lines = tmp_path / "b.jsonl"
    lines.write_text("\n".join(json.dumps(m) for m in msgs) + "\nnot json\n")
    for path in (arr, lines):
        first, last = quota.first_last(str(path))
        assert first["five_hour"]["used_percentage"] == 10.0
        assert last["seven_day"]["used_percentage"] == 25.0
    assert quota.first_last(str(tmp_path / "missing")) == (None, None)


def test_weekly_reserve_stops_a_shift_until_the_late_window():
    now = RESET - 2 * 86400
    d = quota.decide(reading(10, 90, now), now=now, rows=measured(5))
    assert d["verdict"] == "STOP" and not d["run"]
    late = RESET - 10 * H
    d = quota.decide(reading(10, 91, late), now=late, rows=measured(5))
    assert d["run"], d            # the owner's late-week rule
    d = quota.decide(reading(10, 98, late), now=late, rows=measured(5))
    assert d["verdict"] == "STOP"


def test_a_shift_starts_only_if_it_fits_under_the_ceiling():
    """4 points a shift at 1.25x is 5: from 88%, only 24 minutes fit under 90."""
    now = RESET - 3 * 86400
    d = quota.decide(reading(10, 88, now), now=now, rows=measured(5), kind="dispatch")
    assert d["run"] and d["minutes"] == 20 and d["verdict"] == "WRAP"
    assert "fit under the weekly reserve" in d["reason"]
    d = quota.decide(reading(10, 89, now), now=now, rows=measured(5), kind="dispatch")
    assert d["verdict"] == "STOP"     # 12 minutes would fit: not worth starting


def test_the_five_hour_ceiling_always_holds():
    now = RESET - 3 * 86400
    assert quota.decide(reading(97, 10, now), now=now, rows=measured(5))["verdict"] == "STOP"
    late = RESET - 2 * H
    assert quota.decide(reading(97, 50, late), now=late, rows=measured(5))["verdict"] == "STOP"
    d = quota.decide(reading(87, 10, now), now=now, rows=measured(5))
    assert d["verdict"] == "WRAP" and d["minutes"] == 20     # 10 points at 25/h


def test_a_five_hour_reset_mid_shift_frees_the_window():
    """Review, 2026-11-21: started where a full hour would NOT fit, so only the
    reset branch can give 60; and only if the window absorbs the minutes left."""
    now = RESET - 3 * 86400
    d = quota.decide(reading(90, 10, now, five_resets_in=15 * 60), now=now, rows=measured(5))
    assert d["verdict"] == "GO" and d["minutes"] == 60
    d = quota.decide(reading(95, 10, now, five_resets_in=5 * 60), now=now, rows=measured(5))
    assert d["verdict"] == "STOP"


def test_a_local_session_near_the_ceiling_gets_one_short_step():
    """Owner, 2026-11-21: "use it all, always". A dispatch reads again after
    each step, so a few minutes still fit where a scheduled shift stops."""
    now = RESET - 3 * 86400
    local = quota.decide(reading(93, 10, now), now=now, rows=measured(5), kind="dispatch")
    assert local["verdict"] == "WRAP" and local["minutes"] == 5, local
    assert quota.decide(reading(93, 10, now), now=now, rows=measured(5))["verdict"] == "STOP"
    assert quota.decide(reading(96.5, 10, now), now=now, rows=measured(5),
                        kind="dispatch")["verdict"] == "STOP"


def test_an_unmeasured_five_hour_rate_starts_ci_with_a_wider_margin():
    """Review, 2026-11-21: a CI shift cannot read mid-run, so until its 5-hour
    rate is measured the start gate assumes 1.75x the guess, not 1.25x."""
    now = RESET - 3 * 86400
    unmeasured = [{"weekly_used": "4.0", "duration_min": "60"} for _ in range(5)]
    assert quota.decide(reading(72, 10, now), now=now, rows=measured(5))["minutes"] == 60
    d = quota.decide(reading(72, 10, now), now=now, rows=unmeasured)
    assert d["minutes"] < 60 and 72 + 20 * 1.75 * d["minutes"] / 60 <= quota.RESERVE_5H, d


def test_pacing_behind_on_and_ahead():
    now = RESET - 6 * 86400
    behind = quota.decide(reading(5, 5, now), now=now, rows=measured(5, weekly=2.0))
    assert behind["verdict"] == "GO" and "behind pace" in behind["reason"]
    on = quota.decide(reading(5, 5, now), now=now, rows=measured(5, weekly=4.5))
    assert on["verdict"] == "GO" and "on pace" in on["reason"]
    ahead = quota.decide(reading(5, 60, now), now=now, rows=measured(5, weekly=4.0))
    assert ahead["verdict"] == "BOUNDED" and ahead["minutes"] == 30
    skip = quota.decide(reading(5, 80, now), now=now, rows=measured(5, weekly=4.0))
    assert skip["verdict"] == "STOP" and "well ahead" in skip["reason"]


def test_catch_up_runs_only_behind_pace_and_dispatch_is_never_skipped_for_pace():
    now = RESET - 6 * 86400
    behind = quota.decide(reading(5, 5, now), now=now, rows=measured(5, 2.0), kind="catch-up")
    assert behind["run"] and "Gemini" in behind["reason"]
    on = quota.decide(reading(5, 5, now), now=now, rows=measured(5, 4.5), kind="catch-up")
    assert not on["run"]
    owner = quota.decide(reading(5, 80, now), now=now, rows=measured(5, 4.0), kind="dispatch")
    assert owner["run"] and owner["verdict"] == "BOUNDED"


def test_the_late_window_paces_toward_the_late_ceiling():
    """At 90% with 10h left, a scheduled shift may still spend the reserve."""
    late = RESET - 10 * H
    d = quota.decide(reading(10, 90, late), now=late, rows=measured(5, 3.0))
    assert d["run"] and d["late"] and "late-week reserve is open" in d["pace"]


def test_measured_shifts_replace_the_prior():
    prior = quota.PRIOR["seven_day"]
    assert quota.shift_cost(measured(2, 9.0))["seven_day"] == (prior, prior, 2)
    assert quota.shift_cost(measured(3, 9.0))["seven_day"] == (9.0, 9.0, 3)
    rows = measured(3, 9.0) + [{"weekly_used": ""}, {"weekly_used": "-3"}]
    assert quota.shift_cost(rows)["seven_day"] == (9.0, 9.0, 3)     # blanks and resets ignored
    assert quota.shift_cost(measured(3, 9.0, minutes=30))["seven_day"] == (9.0, 18.0, 3)


def test_a_full_hour_is_judged_at_the_hourly_rate_of_shifts_that_ended_early():
    """Review, 2026-11-21: 10 five-hour points in 30-minute shifts is 20 an
    hour, so from 77% a full hour would reach the 97% ceiling."""
    now = RESET - 5 * 86400
    d = quota.decide(reading(77, 10, now), now=now, rows=measured(5, 2.0, 10.0, minutes=30))
    assert d["minutes"] < 60 and d["verdict"] in ("BOUNDED", "WRAP"), d
    assert 77 + 20 * d["minutes"] / 60 <= quota.RESERVE_5H


def test_a_missing_window_is_unknown_not_empty():
    now = RESET - 5 * 86400
    only_five = {"five_hour": reading(10, 10, now)["five_hour"]}
    assert quota.decide(only_five, now=now, rows=measured(5)) is None
    merged = quota.latest([reading(10, 40, now), only_five])
    assert merged["seven_day"]["used_percentage"] == 40.0     # the older figure beats none


def test_a_reset_in_milliseconds_is_rejected():
    assert quota.from_event(event(0.1, 0.2, seven_resets=RESET * 1000)).get("seven_day") is None


def test_the_units_allowance_still_binds_with_a_reading(tmp_path, capsys):
    """Its ceiling is a repository variable, the one bound a shift cannot raise."""
    now = RESET - 5 * 86400
    stream = tmp_path / "probe.json"
    stream.write_text(json.dumps(event(0.1, 0.1, now + 3 * H)))
    ledger = tmp_path / "usage.csv"
    ledger.write_text("timestamp_utc,run_id,model,effort,turns,duration_min,quota_units,is_error\n"
                      f"{datetime.datetime.now(UTC).isoformat()},1,m,e,1,1,150,0\n")
    out = tmp_path / "out"
    assert quota.gate(str(stream), str(ledger), 120, github_output=str(out),
                      snapshot=str(tmp_path / "s.json"), now=now) == 1
    printed = capsys.readouterr().out
    assert "binds before the measured reserve" in printed and "minutes=0" in out.read_text()


def test_any_failure_reading_falls_back_to_the_units_allowance(tmp_path, monkeypatch):
    stream = tmp_path / "probe.json"
    stream.write_text(json.dumps(event(0.1, 0.1)))
    def broken(*a, **k):
        raise ValueError("a bug")
    monkeypatch.setattr(quota, "decide", broken)
    assert quota.gate(str(stream), str(tmp_path / "none.csv"), 100,
                      snapshot=str(tmp_path / "s.json")) == 0
    assert quota.gate(str(stream), str(tmp_path / "none.csv"), 100, kind="catch-up",
                      snapshot=str(tmp_path / "s.json")) == 1


def test_the_ledger_columns_survive_a_broken_quota_module():
    assert shift_budget.QUOTA_COLUMNS == quota.COLUMNS


def test_pace_answers_a_host_that_can_add_runs(tmp_path, capsys):
    stream = tmp_path / "s.json"
    stream.write_text(json.dumps(event(0.05, 0.05, seven_resets=quota.next_reset(datetime.datetime.now(UTC).timestamp()))))
    code = quota.pace_command(str(stream), kind="catch-up", ledger=str(tmp_path / "none.csv"))
    decided = json.loads(capsys.readouterr().out)
    assert code == (0 if decided["run"] else 1) and "reason" in decided


def test_use_across_a_reset_is_not_a_measurement():
    a = {"seven_day": {"used_percentage": 80.0, "resets_at": 1}}
    b = {"seven_day": {"used_percentage": 3.0, "resets_at": 2}}
    assert quota.used(a, b, "seven_day") is None
    c = {"seven_day": {"used_percentage": 84.5, "resets_at": 1}}
    assert quota.used(a, c, "seven_day") == 4.5


def test_shifts_per_day_is_observed_not_assumed():
    now = RESET - 3 * 86400
    stamp = lambda h: datetime.datetime.fromtimestamp(now - h * H, UTC).isoformat()
    two_a_day = [{"timestamp_utc": stamp(h), "slot": ""} for h in range(0, 168, 12)]
    assert quota.shifts_per_day(two_a_day, now) == 2.0
    catch_ups = [{"timestamp_utc": stamp(h), "slot": "catch-up"} for h in range(0, 168, 12)]
    assert quota.shifts_per_day(catch_ups, now) == quota.SLOTS_PER_DAY


def test_gate_without_a_reading_falls_back_to_the_units_allowance(tmp_path, capsys):
    stream = tmp_path / "probe.json"
    stream.write_text("")
    ledger = tmp_path / "usage.csv"
    ledger.write_text("timestamp_utc,run_id,model,effort,turns,duration_min,quota_units,is_error\n"
                      f"{datetime.datetime.now(UTC).isoformat()},1,m,e,1,1,150,0\n")
    out = tmp_path / "out"
    assert quota.gate(str(stream), str(ledger), 120, github_output=str(out),
                      snapshot=str(tmp_path / "snap.json")) == 1
    assert "units allowance alone decides" in capsys.readouterr().out
    assert quota.gate(str(stream), str(ledger), 200, github_output=str(out),
                      snapshot=str(tmp_path / "snap.json")) == 0
    assert quota.gate(str(stream), str(ledger), 200, kind="catch-up",
                      snapshot=str(tmp_path / "snap.json")) == 1


def test_gate_with_a_reading_saves_it_for_the_shift(tmp_path):
    now = RESET - 5 * 86400
    stream = tmp_path / "probe.json"
    stream.write_text(json.dumps(event(0.2, 0.3, now + 3 * H)) + "\n")
    snap, start, out = tmp_path / "snap.json", tmp_path / "start.json", tmp_path / "out"
    assert quota.gate(str(stream), str(tmp_path / "none.csv"), 1, start=str(start),
                      github_output=str(out), snapshot=str(snap), now=now) == 0
    saved = json.loads(snap.read_text())
    assert saved["seven_day"]["used_percentage"] == 30.0 and saved["decision"]["run"]
    assert json.loads(start.read_text())["five_hour"]["used_percentage"] == 20.0
    assert "minutes=60" in out.read_text()


def test_record_carries_start_and_end_and_widens_an_old_ledger(tmp_path, capsys):
    ledger = tmp_path / "usage.csv"
    ledger.write_text("timestamp_utc,run_id,model,effort,turns,duration_min,quota_units,is_error\n"
                      "2026-11-20T01:51:33+00:00,9,m,e,119,35.1,8.2702,0\n")
    start = tmp_path / "start.json"
    five_at, week_at = int(RESET - 100 * H), int(RESET)
    start.write_text(json.dumps({"five_hour": {"used_percentage": 10.0, "resets_at": five_at},
                                 "seven_day": {"used_percentage": 20.0, "resets_at": week_at}}))
    output = tmp_path / "out.json"
    output.write_text(json.dumps([
        {"type": "system"},
        event(0.12, 0.2, five_at, week_at),
        event(0.31, 0.235, five_at, week_at),
        {"type": "result", "num_turns": 3, "duration_ms": 60000, "total_cost_usd": 2.5,
         "is_error": False}]))
    assert shift_budget.record(str(output), str(ledger), "10", "m", "e",
                               str(start), "scheduled", "60") == 0
    rows = list(csv.DictReader(open(ledger)))
    assert rows[0]["run_id"] == "9" and rows[0]["weekly_used"] == ""
    new = rows[1]
    assert (new["five_hour_start"], new["five_hour_end"]) == ("10.0", "31.0")
    assert (new["weekly_start"], new["weekly_end"], new["weekly_used"]) == ("20.0", "23.5", "3.5")
    assert new["five_hour_used"] == "21.0" and new["weekly_resets_at"] == str(week_at)
    assert new["slot"] == "scheduled" and new["minutes"] == "60"
    # The units breaker still reads the widened ledger.
    assert shift_budget._recent(str(ledger)) >= 0


def test_record_survives_a_broken_reading(tmp_path, monkeypatch):
    def broken(*a):
        raise KeyError("x")
    monkeypatch.setattr(shift_budget, "_quota_columns", broken)
    output = tmp_path / "out.json"
    output.write_text(json.dumps([{"type": "result", "num_turns": 1, "duration_ms": 1,
                                   "total_cost_usd": 0.5, "is_error": False}]))
    ledger = tmp_path / "usage.csv"
    assert shift_budget.record(str(output), str(ledger), "1", "m", "e", "", "scheduled", "60") == 0
    assert list(csv.DictReader(open(ledger)))[0]["quota_units"] == "0.5000"


def test_record_without_readings_still_records_cost(tmp_path):
    output = tmp_path / "out.json"
    output.write_text(json.dumps([{"type": "result", "num_turns": 1, "duration_ms": 1,
                                   "total_cost_usd": 0.5, "is_error": False}]))
    ledger = tmp_path / "usage.csv"
    assert shift_budget.record(str(output), str(ledger), "1", "m", "e") == 0
    row = list(csv.DictReader(open(ledger)))[0]
    assert row["quota_units"] == "0.5000" and row["weekly_start"] == ""


def test_budget_in_ci_without_a_reading_is_not_capped_twice(monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert statusline.budget_verdict(None, rows=[])[0] == "GO"
    monkeypatch.delenv("GITHUB_ACTIONS")
    assert statusline.budget_verdict(None, rows=[])[0] == "BOUNDED"


def test_budget_reads_a_statusline_snapshot():
    now = RESET - 5 * 86400
    snap = {"five_hour": {"used_percentage": 97.0, "resets_at": now + H},
            "seven_day": {"used_percentage": 20.0, "resets_at": RESET}}
    assert statusline.budget_verdict(snap, now=now, rows=[])[0] == "STOP"
