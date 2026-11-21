#!/usr/bin/env python3
"""Measured Claude quota: readings, the owner's reserve, and pacing shifts to
the weekly reset.

**The reading.** Claude Code reports the plan's real usage in its stream-json
output, once at the first response and again whenever the rounded figure moves:

    {"type": "rate_limit_event", "rate_limit_info": {"unifiedWindows": {
        "five_hour": {"utilization": 0.66, "resetsAt": 1795239600},
        "seven_day": {"utilization": 0.09, "resetsAt": 1795802400}}}}

Utilization is a fraction of the whole plan, so it includes the owner's own
sessions; it can pass 1. It replaces the "quota units" proxy in
`.github/shift-usage.csv` wherever a reading exists (the owner, 2026-11-20:
units are poorly calibrated). Never call `/api/oauth/usage` (403 for setup
tokens) or `/v1/messages` with the subscription token: Anthropic's terms bar
using it outside Claude Code. A reading comes from one of three places:

- a shift's start: shift.yml runs one minimal `claude -p` probe on the smallest
  model (~600 input tokens, 3 s) *before checkout*, so no file a shift could
  have edited runs while the subscription token is in the environment. `gate`
  below reads the stream it left;
- a shift's end: the last event in the action's execution output, which keeps
  every SDK message (`shift_budget.py record`);
- a local session: `statusline.py`'s snapshot when its status line runs, else
  `probe` (the VSCode extension never runs a status line).

**The reserve** (`CLAUDE.md` §2) is 80% of the 5-hour window, always, and 90%
of the weekly one, except in the last 12 hours before the Friday 18:00 UTC
reset, when the weekly reserve is the shifts' to use too, because it expires
unused (the owner, 2026-11-20). Late in the week the ceiling is 98, not 100: a
shift that reaches the hard limit dies without handing over (11-15). A shift
starts only if its expected use fits under the ceiling in force.

**Pacing.** The goal is to land near that ceiling at the reset, because quota
left unused there is lost. Each shift gets an allowance: the headroom left to
the ceiling, shared over the scheduled shifts expected before the reset (and,
before the late window, the headroom to 90 over the shifts before it). That is
compared with what a shift measurably uses: the median start-to-end change of
recent shifts, which includes whatever the owner did meanwhile.

    allowance / cost >= 1.5  behind pace: a full shift, and catch-up slots run
                     >= 0.75 on pace: a full shift
                     >= 0.4  ahead: a short one
                     below   well ahead: a scheduled slot is skipped

Known limits (2026-11-21; the quota-pacing read in analysis/experiments.csv
judges whether they matter): pacing shares the headroom as if shifts alone will
spend it, so early in the week shifts run ahead of the owner (the 90% reserve
bounds that); a CI shift cannot take a reading mid-run, so its minutes are set
at the start; the measured reserve is held by tests/test_quota.py, not by a
guardrails.yml grep. A new host (cloud tasks) owes the same two readings:
a stream with a rate_limit_event for `gate`, and the end stream for
`shift_budget.py record`.

    quota.py gate <probe-stream> <ledger> <units-ceiling> [--kind K] [--start F] [--github-output F]
    quota.py probe              # take a reading now (local only) and save the snapshot
    quota.py report [<ledger>]  # per-week landing and per-shift use: the scheduled read
"""
import argparse
import csv
import datetime
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(os.path.dirname(HERE), ".github", "shift-usage.csv")
SNAPSHOT = os.path.expanduser("~/.claude/usage-snapshot.json")

RESERVE_5H = 80.0        # the owner's live sessions keep the rest, always
RESERVE_7D = 90.0
LATE_HOURS = 12          # the owner, 2026-11-20: the last ~12h before the reset
LATE_CEILING_7D = 98.0   # not 100: a shift that hits the hard limit cannot hand over
SAFETY = 1.25            # a shift starts only if 1.25x its usual use still fits

# Until three shifts have been measured. Guesses, replaced by the median of
# measured shifts as soon as there are MIN_SAMPLES of them.
PRIOR = {"seven_day": 4.0, "five_hour": 20.0}
MIN_SAMPLES = 3
RECENT = 10              # shifts in the median

SHIFT_MINUTES = 60       # the full shift shift.yml gives (the job is killed at 70)
SHORT_MINUTES = 30
MIN_MINUTES = 20         # below this a shift only orients and hands over
SLOTS_PER_DAY = 3        # shift.yml's scheduled slots; the observed rate wins
BEHIND, ON_PACE, AHEAD = 1.5, 0.75, 0.4

WINDOWS = ("five_hour", "seven_day")
COLUMNS = ["slot", "minutes", "five_hour_start", "five_hour_end", "weekly_start",
           "weekly_end", "five_hour_used", "weekly_used", "weekly_resets_at"]


# --- readings ---------------------------------------------------------------

def load_messages(path):
    """Every message in a stream-json file: a JSON array, one object or lines."""
    text = open(path, encoding="utf-8").read()
    try:
        data = json.loads(text)
    except ValueError:
        data = []
        for line in text.splitlines():
            try:
                data.append(json.loads(line))
            except ValueError:
                continue
    if isinstance(data, dict):
        data = [data]
    return [m for m in data if isinstance(m, dict)] if isinstance(data, list) else []


def from_event(message):
    """One rate_limit_event as a reading, in the snapshot's shape; else None."""
    if not isinstance(message, dict) or message.get("type") != "rate_limit_event":
        return None
    windows = ((message.get("rate_limit_info") or {}).get("unifiedWindows")) or {}
    out = {}
    for name in WINDOWS:
        w = windows.get(name)
        if not isinstance(w, dict):
            continue
        u, r = w.get("utilization"), w.get("resetsAt")
        if isinstance(u, (int, float)) and isinstance(r, (int, float)) and 0 <= u <= 5:
            out[name] = {"used_percentage": round(u * 100, 1), "resets_at": int(r)}
    return out or None


def readings(messages):
    return [r for r in (from_event(m) for m in messages) if r]


def first_last(path):
    """(first, last) reading in a stream file; (None, None) if it has none."""
    try:
        found = readings(load_messages(path))
    except (OSError, ValueError):
        return None, None
    return (found[0], found[-1]) if found else (None, None)


def live(window, now):
    """Percent used, 0.0 once the window has reset, None if there is none."""
    if not window or window.get("used_percentage") is None:
        return None
    if window.get("resets_at") and window["resets_at"] <= now:
        return 0.0
    return float(window["used_percentage"])


def save_snapshot(reading, path=SNAPSHOT, source="probe", extra=None):
    """Write a reading where `statusline.py --budget` looks. Atomic."""
    snap = {"captured_at": int(time.time()), "source": source,
            "five_hour": reading.get("five_hour"), "seven_day": reading.get("seven_day")}
    snap.update(extra or {})
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".usage-", suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(snap, f, indent=2)
    os.replace(tmp, path)
    return snap


def probe(timeout=90):
    """Take a reading now, locally, through Claude Code itself. Never in CI:
    there the token is out of a shift's reach, and the gate took the reading."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return None
    with tempfile.TemporaryDirectory(prefix="quota-probe-") as where:
        try:
            done = subprocess.run(
                ["claude", "-p", "Reply with OK.", "--model", "haiku", "--tools", "",
                 "--system-prompt", "Reply with OK.", "--max-turns", "1",
                 "--output-format", "stream-json", "--verbose",
                 "--no-session-persistence", "--strict-mcp-config"],
                cwd=where, stdin=subprocess.DEVNULL, capture_output=True,
                text=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired):
            return None
    found = [r for r in (from_event(_json(l)) for l in done.stdout.splitlines()) if r]
    return found[-1] if found else None


def _json(line):
    try:
        return json.loads(line)
    except ValueError:
        return None


# --- what shifts use ----------------------------------------------------------

def used(start, end, name):
    """Points a window moved between two readings; None across a reset."""
    a, b = (start or {}).get(name), (end or {}).get(name)
    if not a or not b or a.get("resets_at") != b.get("resets_at"):
        return None
    return round(b["used_percentage"] - a["used_percentage"], 1)


def _rows(ledger):
    try:
        with open(ledger, newline="") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def _float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def shift_cost(rows):
    """{window: (median points a shift uses, samples)}, from measured shifts."""
    out = {}
    for name, col in (("seven_day", "weekly_used"), ("five_hour", "five_hour_used")):
        seen = [v for v in (_float(r.get(col)) for r in rows) if v is not None and v >= 0]
        seen = seen[-RECENT:]
        if len(seen) >= MIN_SAMPLES:
            out[name] = (max(statistics.median(seen), 0.5), len(seen))
        else:
            out[name] = (PRIOR[name], len(seen))
    return out


def shifts_per_day(rows, now):
    """Scheduled shifts a day, as observed over the last week. Since 11-16
    only two of shift.yml's three slots have run, so the cron overstates it."""
    cut = now - 7 * 86400
    n = 0
    for r in rows:
        try:
            when = datetime.datetime.fromisoformat(r["timestamp_utc"]).timestamp()
        except (KeyError, TypeError, ValueError):
            continue
        if when >= cut and (r.get("slot") or "scheduled") == "scheduled":
            n += 1
    return n / 7 if n >= 3 else SLOTS_PER_DAY


def next_reset(now):
    """The Friday 18:00 UTC reset after `now`, when no reading says otherwise."""
    t = datetime.datetime.fromtimestamp(now, datetime.timezone.utc)
    r = t.replace(hour=18, minute=0, second=0, microsecond=0)
    r += datetime.timedelta(days=(4 - r.weekday()) % 7)
    if r <= t:
        r += datetime.timedelta(days=7)
    return r.timestamp()


def weekly_ceiling(now, resets_at):
    return LATE_CEILING_7D if resets_at - now <= LATE_HOURS * 3600 else RESERVE_7D


# --- the decision ------------------------------------------------------------

def decide(reading, now=None, rows=(), kind="scheduled"):
    """How much this shift may take on, from a reading. kind is `scheduled`,
    `catch-up` (runs only when behind pace) or `dispatch` (an owner's run, or a
    local session: pacing can shorten it, never skip it).

    Returns {verdict, run, minutes, reason, pace}. verdict is GO, BOUNDED, WRAP
    or STOP, as process/shift.md reads them."""
    now = now or time.time()
    reading = reading or {}
    five = live(reading.get("five_hour"), now)
    seven = live(reading.get("seven_day"), now)
    if five is None and seven is None:
        return None
    five, seven = five or 0.0, seven or 0.0
    resets = (reading.get("seven_day") or {}).get("resets_at") or 0
    if resets <= now:
        resets = next_reset(now)
    late = resets - now <= LATE_HOURS * 3600
    ceiling = weekly_ceiling(now, resets)
    cost = shift_cost(list(rows))
    c7, c5 = cost["seven_day"][0], cost["five_hour"][0]
    head = f"5h {five:.0f}%, weekly {seven:.0f}%"

    def out(verdict, minutes, why, pace=""):
        return {"verdict": verdict, "run": verdict != "STOP", "minutes": int(minutes),
                "reason": f"{head} — {why}", "pace": pace, "ceiling": ceiling,
                "late": late, "five_hour": five, "seven_day": seven}

    if seven >= ceiling:
        return out("STOP", 0, f"at the weekly reserve ({ceiling:.0f}%)")
    if five >= RESERVE_5H:
        return out("STOP", 0, f"at the 5-hour reserve ({RESERVE_5H:.0f}%)")

    # Minutes that fit under each reserve at SAFETY times a shift's usual rate.
    fit7 = SHIFT_MINUTES * (ceiling - seven) / (c7 * SAFETY)
    fit5 = SHIFT_MINUTES * (RESERVE_5H - five) / (c5 * SAFETY)
    resets5 = (reading.get("five_hour") or {}).get("resets_at") or 0
    left5 = (resets5 - now) / 60
    if 0 < left5 < SHIFT_MINUTES and five + c5 * SAFETY * left5 / SHIFT_MINUTES <= RESERVE_5H:
        fit5 = SHIFT_MINUTES     # the 5-hour window resets mid-shift, in time

    # Pace: the headroom per scheduled shift left before the reset.
    hours = (resets - now) / 3600
    per_day = shifts_per_day(rows, now)
    n = max(1.0, per_day * hours / 24)
    allowance = (LATE_CEILING_7D - seven) / n
    if not late:
        allowance = min(allowance, (RESERVE_7D - seven) / max(1.0, per_day * (hours - LATE_HOURS) / 24))
    ratio = allowance / c7
    when = datetime.datetime.fromtimestamp(resets, datetime.timezone.utc).strftime("%a %d %b %H:%M")
    measured = (f"~{c7:.1f} points a shift, measured over {cost['seven_day'][1]}"
                if cost["seven_day"][1] >= MIN_SAMPLES else f"~{c7:.0f} assumed until {MIN_SAMPLES} are measured")
    pace = (f"{allowance:.1f} weekly points per shift left for ~{n:.0f} shifts to the {when} UTC "
            f"reset ({measured})" + ("; the late-week reserve is open" if late else ""))

    if ratio >= BEHIND:
        verdict, minutes, why = "GO", SHIFT_MINUTES, "behind pace: use the full time; larger ready items and parallel helpers are worth it"
    elif ratio >= ON_PACE:
        if kind == "catch-up":
            return out("STOP", 0, "on pace, so this catch-up slot is not needed", pace)
        verdict, minutes, why = "GO", SHIFT_MINUTES, "on pace"
    elif ratio >= AHEAD or kind == "dispatch":
        if kind == "catch-up":
            return out("STOP", 0, "ahead of pace, so this catch-up slot is not needed", pace)
        verdict, minutes, why = "BOUNDED", SHORT_MINUTES, "ahead of pace: one bounded task"
    else:
        return out("STOP", 0, "well ahead of pace: this slot is skipped so the week lasts", pace)
    if kind == "catch-up":
        why = ("catch-up shift, " + why + "; prefer work that spends no Gemini or Polly")

    fit = min(fit7, fit5)
    if fit < minutes:
        if fit < MIN_MINUTES:
            limit = "weekly" if fit7 <= fit5 else "5-hour"
            return out("STOP", 0, f"a shift would cross the {limit} reserve", pace)
        minutes = int(fit // 5 * 5)
        verdict = "WRAP" if minutes < SHORT_MINUTES else "BOUNDED"
        why = f"{minutes} minutes fit under the {'weekly' if fit7 <= fit5 else '5-hour'} reserve"
    return out(verdict, minutes, why, pace)


# --- commands ------------------------------------------------------------------

def gate(stream, ledger, units_ceiling, kind="scheduled", start=None,
         github_output=None, snapshot=SNAPSHOT, now=None):
    """shift.yml's weekly breaker. Exit 0 runs the shift, 1 skips it. Without a
    reading it falls back to the units allowance, as before 2026-11-21."""
    _, reading = first_last(stream)
    rows = _rows(ledger)
    result = decide(reading, now=now, rows=rows, kind=kind) if reading else None
    outputs = {}
    if result is None:
        print("No usage reading from the probe — falling back to the weekly units allowance.")
        if kind == "catch-up":
            print("A catch-up slot runs only when a reading shows the week behind pace: skipped.")
            return _emit(github_output, {"minutes": 0}, 1)
        sys.path.insert(0, HERE)
        import shift_budget
        code = shift_budget.check(ledger, float(units_ceiling))
        return _emit(github_output, {"minutes": SHIFT_MINUTES}, code)

    print(f"{result['verdict']}: {result['reason']}")
    if result["pace"]:
        print(f"pace: {result['pace']}")
    outputs["minutes"] = result["minutes"]
    try:
        save_snapshot(reading, snapshot, source="shift start", extra={"decision": result})
        if start:
            save_snapshot(reading, start, source="shift start")
    except OSError as e:
        print(f"could not save the reading ({type(e).__name__}); the shift still runs on this decision")
    return _emit(github_output, outputs, 0 if result["run"] else 1)


def _emit(path, outputs, code):
    if path:
        with open(path, "a") as f:
            for k, v in outputs.items():
                f.write(f"{k}={v}\n")
    return code


def report(ledger=LEDGER):
    """Each weekly window: shifts measured, their median use, and where the
    week landed (the last reading before its reset). The scheduled read in
    analysis/experiments.csv (quota-pacing) is judged on this."""
    weeks = {}
    for r in _rows(ledger):
        key = r.get("weekly_resets_at")
        if not key:
            continue
        weeks.setdefault(key, []).append(r)
    if not weeks:
        print("No measured shifts yet: readings start with the first shift after shift.yml's probe lands.")
        return 0
    print("week resetting (UTC)  shifts  measured  median weekly/5h per shift  last reading  units/point")
    for key in sorted(weeks):
        rows = weeks[key]
        w = [v for v in (_float(r.get("weekly_used")) for r in rows) if v is not None]
        f = [v for v in (_float(r.get("five_hour_used")) for r in rows) if v is not None]
        ends = [v for v in (_float(r.get("weekly_end")) or _float(r.get("weekly_start")) for r in rows) if v is not None]
        units = sum(_float(r.get("quota_units")) or 0 for r in rows)
        per_point = f"{units / sum(w):.1f}" if sum(w) > 0 else "-"
        when = datetime.datetime.fromtimestamp(int(float(key)), datetime.timezone.utc).strftime("%a %d %b %H:%M")
        print(f"{when:<21} {len(rows):>6}  {len(w):>8}  "
              f"{(statistics.median(w) if w else float('nan')):>9.1f} / {(statistics.median(f) if f else float('nan')):<5.1f}"
              f"            {(ends[-1] if ends else float('nan')):>5.0f}%  {per_point:>11}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gate")
    g.add_argument("stream")
    g.add_argument("ledger")
    g.add_argument("units_ceiling", type=float)
    g.add_argument("--kind", default="scheduled", choices=["scheduled", "catch-up", "dispatch"])
    g.add_argument("--start")
    g.add_argument("--github-output")
    sub.add_parser("probe")
    rp = sub.add_parser("report")
    rp.add_argument("ledger", nargs="?", default=LEDGER)
    a = ap.parse_args(argv)
    if a.cmd == "gate":
        return gate(a.stream, a.ledger, a.units_ceiling, a.kind, a.start, a.github_output)
    if a.cmd == "probe":
        reading = probe()
        if not reading:
            print("no reading: is `claude` installed and signed in? (never in CI)")
            return 1
        save_snapshot(reading, source="probe")
        print(json.dumps(reading))
        return 0
    return report(a.ledger)


if __name__ == "__main__":
    sys.exit(main())
