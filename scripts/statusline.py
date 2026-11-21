#!/usr/bin/env python3
"""Status line that also persists Claude usage limits for `/shift` to read.

Claude Code hands a statusLine command a JSON blob on stdin, and for claude.ai
Pro/Max accounts that blob carries the real server-side rate limits:
`rate_limits.five_hour` and `.seven_day`, each with `used_percentage` and a
`resets_at` epoch. That is the only supported way to see remaining plan usage —
it is not in `~/.claude.json`, there is no CLI flag, and `/usage` is
interactive. Transcripts under `~/.claude/projects/` can reconstruct *consumed*
tokens but never the limit, so they can't answer "how much is left".

So this script does two jobs: render a status line, and drop the numbers into
SNAPSHOT where a later session can pick them up. It re-runs on every assistant
message, so the snapshot tracks the session closely.

Robustness matters more than features here: Claude Code runs this constantly,
and a crash or a hang shows up as a broken status bar. Everything is wrapped,
stdlib only, no repo dependencies — it must keep working from any directory.

Install (already done if `statusLine` in ~/.claude/settings.json points here):

    "statusLine": {"type": "command",
                   "command": "/abs/path/to/scripts/statusline.py",
                   "refreshInterval": 60}
"""
import json
import os
import sys
import tempfile
import time

SNAPSHOT = os.path.expanduser("~/.claude/usage-snapshot.json")

# The reserve and the pacing that reads these numbers live in quota.py, which
# is also stdlib-only; only `--budget` imports it, so the status bar never
# depends on it.
FRESH = 300   # seconds: older than this, --budget takes a new reading (busy sessions move 5h fast)


def _num(value):
    return value if isinstance(value, (int, float)) else None


def _window(raw):
    """Normalise one rate-limit window; None if absent or malformed.

    Windows disappear independently — Claude Code drops one once its resets_at
    passes, and none are present before the session's first API response.
    """
    if not isinstance(raw, dict):
        return None
    used, resets = _num(raw.get("used_percentage")), _num(raw.get("resets_at"))
    if used is None and resets is None:
        return None
    return {"used_percentage": used, "resets_at": resets}


def save_snapshot(payload):
    """Persist the usage numbers. Atomic, so a reader never sees a half file."""
    limits = payload.get("rate_limits") or {}
    ctx = payload.get("context_window") or {}
    snap = {
        "captured_at": int(time.time()),
        "session_id": payload.get("session_id"),
        "model": (payload.get("model") or {}).get("display_name"),
        "cwd": payload.get("cwd") or (payload.get("workspace") or {}).get("current_dir"),
        "five_hour": _window(limits.get("five_hour")),
        "seven_day": _window(limits.get("seven_day")),
        "spend_limit": _window(limits.get("spend_limit")),
        "context_used_percentage": _num(ctx.get("used_percentage")),
        "session_cost_usd": _num((payload.get("cost") or {}).get("total_cost_usd")),
    }
    # Keep the last good reading rather than overwriting it with nulls: the
    # windows are absent early in a session, and a stale-but-real number beats
    # no number for a /shift that is deciding how much to take on.
    if not any(snap[k] for k in ("five_hour", "seven_day", "spend_limit")):
        try:
            with open(SNAPSHOT) as f:
                prev = json.load(f)
            if any(prev.get(k) for k in ("five_hour", "seven_day", "spend_limit")):
                return
        except Exception:
            pass

    d = os.path.dirname(SNAPSHOT) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".usage-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(snap, f, indent=2)
        os.replace(tmp, SNAPSHOT)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _pct(window):
    if not window or window.get("used_percentage") is None:
        return "--"
    return f"{window['used_percentage']:.0f}%"


def _resets_in(window):
    if not window or not window.get("resets_at"):
        return ""
    secs = window["resets_at"] - time.time()
    if secs <= 0:
        return ""
    h, m = int(secs // 3600), int((secs % 3600) // 60)
    return f"{h}h{m:02d}m" if h else f"{m}m"


def render(payload):
    model = (payload.get("model") or {}).get("display_name") or "claude"
    ws = payload.get("workspace") or {}
    where = os.path.basename(ws.get("current_dir") or payload.get("cwd") or "") or "~"
    limits = payload.get("rate_limits") or {}
    five, seven = _window(limits.get("five_hour")), _window(limits.get("seven_day"))
    ctx = _num((payload.get("context_window") or {}).get("used_percentage"))

    bits = [model, where]
    if ctx is not None:
        bits.append(f"ctx {ctx:.0f}%")
    if five:
        left = _resets_in(five)
        bits.append(f"5h {_pct(five)}" + (f" (resets {left})" if left else ""))
    if seven:
        bits.append(f"7d {_pct(seven)}")
    return "  |  ".join(bits)


def budget_verdict(snap, now=None, rows=None):
    """How much work this shift may take on. Returns (verdict, reason, pace).

    STOP    — at or past a reserve; close the loop and end
    WRAP    — finish or park what's open, hand over; start nothing new
    BOUNDED — one small task, then hand over
    GO      — full shift, including a feature through dry run and merge
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import quota
    rows = quota._rows(quota.LEDGER) if rows is None else rows
    decided = quota.decide(snap, now=now, rows=rows, kind="dispatch") if snap else None
    if decided is None:
        # No reading at all. In CI that means the gate's probe failed and the
        # units allowance already gated this shift: returning BOUNDED there
        # capped it twice (the first CI shift stopped after 9.5 minutes).
        if os.environ.get("GITHUB_ACTIONS") == "true":
            return "GO", ("running in CI without a reading — the units allowance "
                          "gated this shift"), ""
        return "BOUNDED", "no usage reading — assuming mid-budget", ""
    return decided["verdict"], decided["reason"], decided["pace"]


def print_budget():
    """`statusline.py --budget` — what a shift reads before choosing work.

    Uses the snapshot when it is fresh. Otherwise, locally, it takes a reading
    (quota.py probe): the VSCode extension never runs a status line."""
    try:
        with open(SNAPSHOT) as f:
            snap = json.load(f)
    except Exception:
        snap = None
    age = time.time() - (snap or {}).get("captured_at", 0)
    if age > FRESH and os.environ.get("GITHUB_ACTIONS") != "true":
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import quota
            reading = quota.probe()
            if reading:
                snap = quota.save_snapshot(reading, SNAPSHOT, source="probe")
        except Exception:
            pass
    decision = (snap or {}).get("decision")
    if decision and os.environ.get("GITHUB_ACTIONS") == "true":
        # In CI the gate decided this shift from this same reading: say what it
        # decided rather than deciding again from older numbers.
        verdict, reason, pace = decision["verdict"], decision["reason"], decision.get("pace")
    else:
        verdict, reason, pace = budget_verdict(snap)
    print(f"{verdict}: {reason}")
    if pace:
        print(f"pace: {pace}")
    if decision and decision.get("minutes") and os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"this shift was given {decision['minutes']} minutes at its start")
    if snap and snap.get("captured_at"):
        age = int(time.time() - snap["captured_at"])
        print(f"reading age: {age // 60}m ({snap.get('source') or 'status line'}"
              f"{'' if age < FRESH else '; stale — trust resets_at, not the %'})")
    print("reserves: 5h stops at 80%; weekly at 90%, or 98% in the last 12h before "
          "the Friday 18:00 UTC reset — the rest is the owner's to use")
    return 0


def main():
    if "--budget" in sys.argv:
        sys.exit(print_budget())
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("")  # never leave the bar looking crashed
        return
    try:
        save_snapshot(payload)
    except Exception:
        pass  # persisting is best-effort; the status line still renders
    try:
        print(render(payload))
    except Exception:
        print("")


if __name__ == "__main__":
    main()
