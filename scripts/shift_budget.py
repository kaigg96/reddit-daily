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

**This is a runaway breaker, not a budget.** The owner's real weekly quota is
the percentage in their Claude console, which includes their own interactive
sessions and which CI cannot see. Measured 2026-09-21: two shifts totalled
15.45 units while the console read 38% used -- almost all of that 38% was
interactive work, so shifts are a small slice. The allowance therefore only
needs to be low enough to catch a shift looping, not to manage their week.

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


# The owner's Claude quota resets on a fixed weekly boundary -- Friday 11:00
# Pacific, which is 18:00 UTC -- not on a rolling window. A rolling 7-day sum
# let spending from BEFORE the reset block shifts after it. Overridable for
# when the plan or timezone changes.
RESET_WEEKDAY = int(os.environ.get("QUOTA_RESET_WEEKDAY", 4))   # Mon=0 … Fri=4
RESET_HOUR_UTC = int(os.environ.get("QUOTA_RESET_HOUR_UTC", 18))


def window_start(now=None):
    """The most recent quota reset at or before `now`."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    candidate = now.replace(hour=RESET_HOUR_UTC, minute=0, second=0, microsecond=0)
    # Walk back to the reset weekday, then back another week if that lands ahead.
    candidate -= datetime.timedelta(days=(candidate.weekday() - RESET_WEEKDAY) % 7)
    if candidate > now:
        candidate -= datetime.timedelta(days=7)
    return candidate


def _recent(ledger, now=None):
    if not os.path.exists(ledger):
        return 0.0
    cut = window_start(now)
    total = 0.0
    with open(ledger) as f:
        for row in csv.DictReader(f):
            try:
                when = datetime.datetime.fromisoformat(row["timestamp_utc"])
                if when >= cut:
                    total += float(row["quota_units"] or 0)
            except (ValueError, KeyError, TypeError):
                continue  # a malformed row must not unblock the budget
    return total


UNDERSPEND_SHARE = 0.35   # below this share of the ceiling, capacity is idle


def check(ledger, ceiling):
    spent = _recent(ledger)
    print(f"shifts used {spent:.2f} quota units since the "
          f"{window_start():%a %d %b %H:%M} UTC reset (allowance "
          f"{ceiling:.2f}). Units are an API-list-price equivalent, not money.")
    if spent >= ceiling:
        print("OVER — skipping this shift to protect the owner's own quota.")
        return 1

    # The mirror risk, and the one the owner actually expects to hit: the whole
    # point of this workflow is that unused capacity is wasted. A ceiling that
    # is never approached means shifts are too small or too rare, which is a
    # tuning signal rather than a fault -- so it warns and proceeds.
    runs = _count(ledger)
    if runs >= 5 and spent < ceiling * UNDERSPEND_SHARE:
        print(f"::warning::Only {spent:.2f} of {ceiling:.2f} quota units used across {runs} "
              f"shifts this week. Capacity is going unused — consider raising the "
              f"cadence, the turn cap, or the effort level.")

    print(f"{ceiling - spent:.2f} quota units of allowance left")
    return 0


def _count(ledger, now=None):
    if not os.path.exists(ledger):
        return 0
    cut = window_start(now)
    n = 0
    with open(ledger) as f:
        for row in csv.DictReader(f):
            try:
                if datetime.datetime.fromisoformat(row["timestamp_utc"]) >= cut:
                    n += 1
            except (ValueError, KeyError, TypeError):
                continue
    return n


def record(output, ledger, run_id, model, effort):
    """Append what the run actually cost. Best-effort: never fail the job."""
    try:
        text = open(output).read()
        # The action writes a JSON array, a single object, or a stream of
        # objects depending on version. Observed in CI 2026-09-20: an array,
        # which the earlier code parsed happily and then called .get() on.
        try:
            data = json.loads(text)
        except ValueError:
            data = [json.loads(l) for l in text.splitlines()
                    if l.strip().startswith("{")]
        if isinstance(data, list):
            results = [d for d in data if isinstance(d, dict)
                       and ("total_cost_usd" in d or d.get("type") == "result")]
            data = results[-1] if results else {}
        if not isinstance(data, dict) or "total_cost_usd" not in data:
            # Recording a zero row would silently understate the budget, which
            # is worse than recording nothing at all.
            print("execution output carried no usage figures — nothing recorded")
            return 0
    except Exception as e:
        print(f"no usable execution output ({type(e).__name__}) — nothing recorded")
        return 0

    new = not os.path.exists(ledger)
    with open(ledger, "a", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["timestamp_utc", "run_id", "model", "effort",
                        "turns", "duration_min", "quota_units", "is_error"])
        row = [datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
               run_id, model, effort, data.get("num_turns", ""),
               f'{data.get("duration_ms", 0) / 60000:.1f}',
               f'{data.get("total_cost_usd", 0):.4f}',
               int(bool(data.get("is_error")))]
        w.writerow(row)
    print("recorded:", row)
    return 0


def actions_minutes(repo, token, days=30):
    """Minutes of GitHub Actions this repo has used recently.

    The free allowance on a private repo is 2000/month. Exhausting it does not
    produce a bill -- it STOPS Actions, which means the video pipeline stops
    publishing. That is a far worse outcome than a shift being skipped, so
    shifts yield to the pipeline rather than competing with it.
    """
    import urllib.request
    now = datetime.datetime.now(datetime.timezone.utc)
    cut = now - datetime.timedelta(days=days)
    total, page = 0.0, 1
    while page <= 5:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}",
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json"})
        try:
            data = json.load(urllib.request.urlopen(req))
        except Exception as e:
            print(f"could not read Actions usage ({type(e).__name__}) — not blocking")
            return None
        runs = data.get("workflow_runs") or []
        if not runs:
            break
        for r in runs:
            try:
                st = datetime.datetime.fromisoformat(r["run_started_at"].replace("Z", "+00:00"))
                if st < cut:
                    continue
                en = datetime.datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00"))
                mins = (en - st).total_seconds() / 60
                if 0 <= mins <= 180:      # ignore absurd values from stuck runs
                    total += mins
            except Exception:
                continue
        page += 1
    return total


def check_actions(repo, token, allowance, reserve_share):
    used = actions_minutes(repo, token)
    if used is None:
        return 0                      # unreadable must not block the shift
    ceiling = allowance * reserve_share
    print(f"Actions used ~{used:.0f} of {allowance:.0f} min this month "
          f"(shifts stop at {ceiling:.0f}, leaving the rest for the video pipeline)")
    if used >= ceiling:
        print("OVER — skipping this shift so the channel keeps publishing.")
        return 1
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        sys.exit(check(sys.argv[2], float(sys.argv[3])))
    if cmd == "record":
        sys.exit(record(*sys.argv[2:7]))
    if cmd == "actions":
        # repo, token, allowance, reserve_share
        sys.exit(check_actions(sys.argv[2], sys.argv[3],
                               float(sys.argv[4]), float(sys.argv[5])))
    sys.exit(__doc__)
