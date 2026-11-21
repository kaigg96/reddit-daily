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

**The reserve** (`CLAUDE.md` §2) is 97% of the 5-hour window, always (the
owner, 2026-11-21: "use it all, always"; the 3% is a margin to hand over), and 90%
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
recent shifts, which includes whatever the owner did meanwhile. Whether a shift
fits under a reserve uses the same change per hour run, since shifts end early.
The units allowance applies as well: a shift runs only if both pass, because
its ceiling is a repository variable a shift cannot raise.

    allowance / cost >= 1.5  behind pace: a full shift, and catch-up slots run
                     >= 0.75 on pace: a full shift
                     >= 0.4  ahead: a short one
                     below   well ahead: a scheduled slot is skipped

A host that can add runs cheaply (cloud tasks; on Actions each one spends
minutes) asks `pace --kind catch-up`: exit 0 means the week is behind pace.

Known limits (2026-11-21; the quota-pacing read in analysis/experiments.csv
judges whether they matter): pacing shares the headroom as if shifts alone will
spend it, so early in the week shifts run ahead of the owner (the 90% reserve
bounds that); a CI shift cannot take a reading mid-run, so its minutes are set
at the start; the measured reserve is held by tests/test_quota.py, not by a
guardrails.yml grep. A new host (cloud tasks) owes the same two readings:
a stream with a rate_limit_event for `gate`, and the end stream for
`shift_budget.py record`.

    quota.py gate <probe-stream> <ledger> <units-ceiling> [--kind K] [--start F] [--github-output F]
    quota.py pace [<stream>] [--kind K]   # the decision as JSON; exit 0 if it runs
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

RESERVE_5H = 97.0        # owner 2026-11-21: "use it all, always"; 3% to hand over
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
        # Epoch seconds only: a value in milliseconds would read as a reset
        # thousands of years away (and crash a date conversion).
        if (isinstance(u, (int, float)) and isinstance(r, (int, float))
                and 0 <= u <= 5 and 1e9 < r < 1e10):
            out[name] = {"used_percentage": round(u * 100, 1), "resets_at": int(r)}
    return out or None


def readings(messages):
    return [r for r in (from_event(m) for m in messages) if r]


def latest(found):
    """The newest figure for each window across readings; None if none. An
    event can carry one window only, and the older figure beats none."""
    out = {}
    for r in found or ():
        out.update({k: v for k, v in r.items() if k in WINDOWS})
    return out or None


def first_last(path):
    """(first, latest) reading in a stream file; (None, None) if it has none."""
    try:
        found = readings(load_messages(path))
    except (OSError, ValueError):
        return None, None
    return (found[0], latest(found)) if found else (None, None)


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
    """{window: (points a shift uses, points per hour run, samples)}: medians
    of measured shifts. Pacing compares the first with the allowance; whether a
    shift fits under a reserve uses the second, because shifts end early (29-46
    of 60 minutes, 11-19 to 11-21) and a per-shift figure read as an hour's
    would let a full hour cross the reserve."""
    out = {}
    for name, col in (("seven_day", "weekly_used"), ("five_hour", "five_hour_used")):
        shift, hour = [], []
        for r in rows:
            v, mins = _float(r.get(col)), _float(r.get("duration_min"))
            if v is None or v < 0:
                continue
            shift.append(v)
            if mins and mins >= 5:
                hour.append(v * 60 / mins)
        shift, hour = shift[-RECENT:], hour[-RECENT:]
        per_shift = max(statistics.median(shift), 0.5) if len(shift) >= MIN_SAMPLES else PRIOR[name]
        per_hour = max(statistics.median(hour), 0.5) if len(hour) >= MIN_SAMPLES else max(per_shift, PRIOR[name])
        out[name] = (per_shift, per_hour, len(shift))
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
    if five is None or seven is None:
        return None     # a missing window is unknown, not empty: the caller falls back
    resets = (reading.get("seven_day") or {}).get("resets_at") or 0
    if resets <= now:
        resets = next_reset(now)
    late = resets - now <= LATE_HOURS * 3600
    ceiling = weekly_ceiling(now, resets)
    cost = shift_cost(list(rows))
    c7, r7, r5 = cost["seven_day"][0], cost["seven_day"][1], cost["five_hour"][1]
    head = f"5h {five:.0f}%, weekly {seven:.0f}%"

    def out(verdict, minutes, why, pace=""):
        return {"verdict": verdict, "run": verdict != "STOP", "minutes": int(minutes),
                "reason": f"{head} — {why}", "pace": pace, "ceiling": ceiling,
                "late": late, "five_hour": five, "seven_day": seven}

    if seven >= ceiling:
        return out("STOP", 0, f"at the weekly reserve ({ceiling:.0f}%)")
    if five >= RESERVE_5H:
        return out("STOP", 0, f"at the 5-hour reserve ({RESERVE_5H:.0f}%)")

    # Minutes that fit under each reserve at SAFETY times a shift's hourly rate.
    fit7 = 60 * (ceiling - seven) / (r7 * SAFETY)
    fit5 = 60 * (RESERVE_5H - five) / (r5 * SAFETY)
    resets5 = (reading.get("five_hour") or {}).get("resets_at") or 0
    left5 = (resets5 - now) / 60
    if 0 < left5 < SHIFT_MINUTES and five + r5 * SAFETY * left5 / 60 <= RESERVE_5H:
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
    measured = (f"~{c7:.1f} points a shift, measured over {cost['seven_day'][2]}"
                if cost["seven_day"][2] >= MIN_SAMPLES else f"~{c7:.0f} assumed until {MIN_SAMPLES} are measured")
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
    """shift.yml's weekly breaker. Exit 0 runs the shift, 1 skips it.

    Two checks, and a shift runs only if both pass: the measured reserve and
    pace (decide), and the units allowance (shift_budget.check), whose ceiling
    is a repository variable a shift cannot raise. Without a reading, or if
    reading it fails in any way, the allowance alone decides, as before."""
    sys.path.insert(0, HERE)
    import shift_budget
    units_ok = shift_budget.check(ledger, float(units_ceiling)) == 0
    try:
        _, reading = first_last(stream)
        result = decide(reading, now=now, rows=_rows(ledger), kind=kind) if reading else None
    except Exception as e:                      # never let a bug here stop every shift
        print(f"Could not use the usage reading ({type(e).__name__}).")
        reading = result = None
    if result is None:
        print("No usable usage reading: the weekly units allowance alone decides.")
        if kind == "catch-up":
            print("A catch-up run goes ahead only when a reading shows the week behind pace: skipped.")
            return _emit(github_output, {"minutes": 0}, 1)
        return _emit(github_output, {"minutes": SHIFT_MINUTES if units_ok else 0},
                     0 if units_ok else 1)

    run = result["run"] and units_ok
    if result["run"] and not units_ok:
        print(f"::warning::The units allowance binds before the measured reserve "
              f"({result['reason']}). `quota.py report` gives units per weekly point; "
              f"the owner can raise SHIFT_WEEKLY_QUOTA_BUDGET to let pacing fill the week.")
    print(f"{result['verdict'] if run else 'STOP'}: {result['reason']}")
    if result["pace"]:
        print(f"pace: {result['pace']}")
    result = dict(result, run=run, minutes=result["minutes"] if run else 0, kind=kind)
    try:
        save_snapshot(reading, snapshot, source="shift start", extra={"decision": result})
        if start:
            save_snapshot(reading, start, source="shift start")
    except OSError as e:
        print(f"could not save the reading ({type(e).__name__}); the shift still runs on this decision")
    return _emit(github_output, {"minutes": result["minutes"]}, 0 if run else 1)


def pace_command(stream=None, kind="scheduled", ledger=LEDGER):
    """The decision as JSON, from a stream file or else a fresh local reading
    or snapshot; exit 0 if a run of this kind should go ahead."""
    reading = first_last(stream)[1] if stream else probe()
    if reading is None and not stream:
        try:
            reading = json.load(open(SNAPSHOT))
        except (OSError, ValueError):
            reading = None
    result = decide(reading, rows=_rows(ledger), kind=kind) if reading else None
    print(json.dumps(result if result else {"run": None, "reason": "no usage reading"}))
    return 0 if result and result["run"] else 1


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
        ends = [v for v in (_float(r.get("weekly_end")) if _float(r.get("weekly_end")) is not None
                            else _float(r.get("weekly_start")) for r in rows) if v is not None]
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
    pc = sub.add_parser("pace")
    pc.add_argument("stream", nargs="?")
    pc.add_argument("--kind", default="scheduled", choices=["scheduled", "catch-up", "dispatch"])
    sub.add_parser("probe")
    rp = sub.add_parser("report")
    rp.add_argument("ledger", nargs="?", default=LEDGER)
    a = ap.parse_args(argv)
    if a.cmd == "gate":
        return gate(a.stream, a.ledger, a.units_ceiling, a.kind, a.start, a.github_output)
    if a.cmd == "pace":
        return pace_command(a.stream, a.kind)
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
