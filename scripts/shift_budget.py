#!/usr/bin/env python3
"""The CI usage reserve: a rolling 7-day ceiling on what shifts have cost.

The owner's 80%/90% reserve cannot be enforced on a runner. Established by
experiment 2026-09-20: statusLine does not fire in headless mode, transcripts
record only the moment a limit is *hit* (`quotaLimits.status = rejected`), and
there is no plan-usage API. Remaining quota is simply not observable there.

What IS observable is consumption: the action writes `total_cost_usd`,
`num_turns` and `duration_ms` per run. So the reserve is enforced by
construction rather than measurement — shifts get a fixed weekly allowance,
and stop when they have spent it.

    shift_budget.py check <ledger> <ceiling>   -> prints spend; exit 1 if over
    shift_budget.py record <output> <ledger> <run_id> <model> <effort>

The ceiling lives in a GitHub repository variable, not in the repo, so a shift
cannot raise its own allowance by editing a file.
"""
import csv
import datetime
import json
import os
import sys


def _recent(ledger, days=7):
    if not os.path.exists(ledger):
        return 0.0
    cut = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    total = 0.0
    with open(ledger) as f:
        for row in csv.DictReader(f):
            try:
                when = datetime.datetime.fromisoformat(row["timestamp_utc"])
                if when >= cut:
                    total += float(row["cost_usd"] or 0)
            except (ValueError, KeyError, TypeError):
                continue  # a malformed row must not unblock the budget
    return total


def check(ledger, ceiling):
    spent = _recent(ledger)
    print(f"shifts have cost ${spent:.2f} in the last 7 days (ceiling ${ceiling:.2f})")
    if spent >= ceiling:
        print("OVER — skipping this shift to protect the owner's own quota.")
        return 1
    print(f"${ceiling - spent:.2f} of allowance left")
    return 0


def record(output, ledger, run_id, model, effort):
    """Append what the run actually cost. Best-effort: never fail the job."""
    try:
        text = open(output).read()
        # The action writes either one object or a stream of them; the last
        # object carries the result.
        try:
            data = json.loads(text)
        except ValueError:
            data = [json.loads(l) for l in text.splitlines()
                    if l.strip().startswith("{")][-1]
    except Exception as e:
        print(f"no usable execution output ({type(e).__name__}) — nothing recorded")
        return 0

    new = not os.path.exists(ledger)
    with open(ledger, "a", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["timestamp_utc", "run_id", "model", "effort",
                        "turns", "duration_min", "cost_usd", "is_error"])
        row = [datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
               run_id, model, effort, data.get("num_turns", ""),
               f'{data.get("duration_ms", 0) / 60000:.1f}',
               f'{data.get("total_cost_usd", 0):.4f}',
               int(bool(data.get("is_error")))]
        w.writerow(row)
    print("recorded:", row)
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        sys.exit(check(sys.argv[2], float(sys.argv[3])))
    if cmd == "record":
        sys.exit(record(*sys.argv[2:7]))
    sys.exit(__doc__)
