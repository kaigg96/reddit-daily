#!/usr/bin/env python3
"""The friction log: what made each finished item hard, and whether fixing it
worked (DECISIONS.md D15).

Built to the spec below (PLAN.md C17). START stays unset until the commit
that lands this on `main` sets it; until then `evaluate` and `gaps` report
nothing to read, and `context_budget.py --health` raises nothing.

Shifts wrote "Friction:" notes in the work log from 09-25 to 10-07, about 18
distinct ones, several recurring. From 10-08 there were none. The work log is
the owner's email, with no slot for them, a word budget, and its oldest
entries deleted, so a recurrence could never be counted. This gives the notes
a home that lasts, a weekly reader, and a rule that says whether it works.

Every finished item logs one row as it finishes, not at the end of the shift:
a merge, an answered question, an escalation, a candidate dropped, an attempt
abandoned.

    venv/bin/python scripts/friction.py add --function engineering \\
        --task "..." --outcome done --category allowance \\
        --hardest "..." --helped "..." --minutes 15 [--fixes G3] [--group G1]
    venv/bin/python scripts/friction.py add --function data --task "..." \\
        --outcome done --category none        # nothing notable: a real answer
    venv/bin/python scripts/friction.py groups     # open groups, to tag a repeat
    venv/bin/python scripts/friction.py report     # weekly review: ungrouped rows,
                                                   # groups by leverage
    venv/bin/python scripts/friction.py evaluate   # D15's rule, then its checks
    venv/bin/python scripts/friction.py gaps       # shifts since START with no row

FILES

.github/friction.csv, append-only, one row per item:
    id            F1, F2, ... (the next after the file's highest, so two
                  branches appending both write it: renumber on merge)
    timestamp_utc when `add` ran
    run_id        GITHUB_RUN_ID, else "local"; "backfill" for the seed rows
    function      an ORG.md short name (strategy, gm, market, audience,
                  distribution, monetization, product, editorial, engineering,
                  reliability, data, finance, legal, security)
    task          one line
    outcome       done | partial | abandoned
    fixes         the group this item fixed, else blank
    category      see below
    hardest       one concrete line; blank only for "none"
    helped        one line; a moonshot is allowed
    minutes_lost  an integer, or "blocked"; blank only on backfill rows
    group         blank until sorted (the writer may tag an obvious repeat)

.github/friction-groups.csv, one row per group, written by the weekly review:
    group, title, status (open | queued | fixed | wontfix | parked),
    item (the queue id or commit that answers it), opened,
    resolved (the date its fix shipped; recurrence is counted after it), note

CATEGORIES
    docs       missing or misleading documentation
    access     no visibility or access: logs, YouTube data, a web page
    allowance  an external allowance: Gemini, a render slot, the clock
    owner      waiting on the owner
    tool       a tool's bug or false alarm
    rules      rules in conflict, or a rule that did not fit
    rederived  re-derived something already recorded
    mistake    my own mistake
    none       nothing notable

WHAT THE BUILD MUST KEEP
- `add` refuses an unknown function, category or outcome, and a non-"none"
  row without hardest, helped and minutes.
- START, the day this lands, is a constant here. Rows before it (the
  2026-10-27 backfill) are never in an evaluation.
- D15's thresholds are constants here, and a test checks that D15 states the
  same numbers, so the rule and the code cannot drift apart.
- `evaluate` prints D15's decision rule verbatim from DECISIONS.md before any
  number, then each check (a)-(h) with its value, threshold and pass / fail /
  not yet, then the verdict (keep, change, stop, not yet). Check (c) is
  judgement: print 10 random non-"none" rows for the reviewer. Check (g)
  counts rows with `fixes` set against all rows in the window.
- `gaps` matches rows to shifts by time: a shift in .github/shift-usage.csv
  logged if a row falls inside [end - duration - 5 min, end + 5 min].
- `context_budget.py --health` calls `gaps`. Three silent shifts in a row
  queue `process-friction-silent` to the owner; it is not SHIFT_OWNED,
  because a silent stop is exactly what happened to the work-log notes.
- Leverage, for `report`, per group: rows x median minutes ("blocked" counts
  as 60) x distinct functions. A fixed group with a row after `resolved` is
  flagged RECURRED.
- Tests in tests/test_friction.py, like the other scripts'.
"""
import argparse
import csv
import datetime as dt
import os
import random
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from context_budget import FUNCTIONS, LEDGER  # noqa: E402

LOG = os.path.join(ROOT, ".github", "friction.csv")
GROUPS = os.path.join(ROOT, ".github", "friction-groups.csv")
DECISIONS = os.path.join(ROOT, "DECISIONS.md")

FIELDS = ["id", "timestamp_utc", "run_id", "function", "task", "outcome",
          "fixes", "category", "hardest", "helped", "minutes_lost", "group"]
GROUP_FIELDS = ["group", "title", "status", "item", "opened", "resolved", "note"]
OUTCOMES = ["done", "partial", "abandoned"]
CATEGORIES = ["docs", "access", "allowance", "owner", "tool", "rules",
              "rederived", "mistake", "none"]
STATUSES = ["open", "queued", "fixed", "wontfix", "parked"]

# The moment this landed on main, as a full UTC timestamp, e.g.
# "2026-10-29T09:30:00+00:00". The landing commit sets it; every row before
# it, the 2026-10-27 seed included, stays out of every evaluation.
START = None

# D15's thresholds. test_friction checks D15 states each of these, so a
# changed number has to change in both places (D15: only for the next read).
LOG_SHARE = 0.80          # (a) share of shifts that log a row
SILENT_RUN = 3            # (a) silent shifts in a row that escalate
NONE_SHARE = (0.05, 0.80)  # (b) "none" rows, as a share of all rows
SAMPLE = 10               # (c) rows printed for the reviewer to judge
UNGROUPED_DAYS = 7        # (d) oldest a row may sit ungrouped
RESULTS_DAYS = 28         # (e)-(f) and "not yet": the monthly read's age
FIXED_GROUPS = 2          # (e) groups fixed by a shipped change
RECUR_BEFORE = 3          # (f) rows a group had before its fix
RECUR_AFTER = 1           # (f) rows it may log after
RECUR_DAYS = 14           # (f) and "not yet": the window after a fix
FIX_SHARE = 1 / 3         # (g) rows that fix a group, as a share of all rows
PROCESS_MINUTES = 20      # (h) a week's processing

BLOCKED_MINUTES = 60      # "blocked", for leverage
GAP_SLACK = dt.timedelta(minutes=5)

_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
_FRACTIONS = {1 / 2: "half", 1 / 3: "a third", 1 / 4: "a quarter"}


def stated():
    """The phrases D15 must contain for its numbers to match these constants."""
    return [
        f"(a) {LOG_SHARE:.0%}+ of shifts log a row",
        f"{_WORDS.get(SILENT_RUN, SILENT_RUN)} silent shifts in a row escalate",
        f'"none" is {round(NONE_SHARE[0] * 100)}–{NONE_SHARE[1]:.0%} of rows',
        f"of {SAMPLE} random rows",
        f"no row older than {UNGROUPED_DAYS} days ungrouped",
        f"{RESULTS_DAYS}+ days after START",
        f"(e) {FIXED_GROUPS}+ groups fixed",
        f"{RECUR_BEFORE}+ rows before its fix logs at most {RECUR_AFTER} row "
        f"in the {RECUR_DAYS} days after",
        f"at most {_FRACTIONS.get(FIX_SHARE, FIX_SHARE)} of the window's rows",
        f"about {PROCESS_MINUTES} minutes at most",
        f"**Not yet** under {RESULTS_DAYS} days, or with no fix {RECUR_DAYS} "
        "days old",
    ]


def rule_text(path=None):
    """D15's decision rule, verbatim from DECISIONS.md."""
    text = open(path or DECISIONS, encoding="utf-8").read()
    m = re.search(r"^## D15 .*?(\*\*Decision rule\*\*.*?)\n\n\*\*", text,
                  re.S | re.M)
    return m.group(1).strip() if m else ""


def drift(path=None):
    """Phrases in stated() that D15 no longer contains."""
    rule = " ".join(rule_text(path).split())
    return [p for p in stated() if p not in rule]


def _ts(s):
    try:
        t = dt.datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _start():
    """START as a datetime. A bare date would read as midnight and let that
    day's rows in, the 2026-10-27 seed among them, so it is refused."""
    if not START:
        return None
    if "T" not in START:
        raise ValueError(f"friction.py START {START!r} needs a time, in UTC")
    return _ts(START)


def _now(now=None):
    return now or dt.datetime.now(dt.timezone.utc)


def load(path=None):
    try:
        with open(path or LOG, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def load_groups(path=None):
    try:
        with open(path or GROUPS, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def window(rows):
    """Rows the rule reads: from START on, never the backfill."""
    start = _start()
    if not start:
        return []
    return [r for r in rows if r.get("run_id") != "backfill"
            and (_ts(r.get("timestamp_utc")) or start - GAP_SLACK) >= start]


def _minutes(value):
    if value == "blocked":
        return BLOCKED_MINUTES
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- add

def add(function, task, outcome, category, hardest="", helped="", minutes="",
        fixes="", group="", path=None, groups_path=None, now=None):
    """Append one row; refuse what D15's rule could not read. Returns the row."""
    errors = []
    if function not in FUNCTIONS:
        errors.append(f"--function {function!r} is not an ORG.md short name "
                      f"({', '.join(FUNCTIONS)})")
    if outcome not in OUTCOMES:
        errors.append(f"--outcome {outcome!r} is not one of {', '.join(OUTCOMES)}")
    if category not in CATEGORIES:
        errors.append(f"--category {category!r} is not one of {', '.join(CATEGORIES)}")
    minutes = str(minutes).strip()
    if category != "none":
        for name, value in (("--hardest", hardest), ("--helped", helped),
                            ("--minutes", minutes)):
            if not str(value).strip():
                errors.append(f"{name} is required unless --category none")
    elif not minutes:
        minutes = "0"
    if minutes and minutes != "blocked" and not re.fullmatch(r"\d+", minutes):
        errors.append(f"--minutes {minutes!r} must be a whole number or 'blocked'")
    known = {g["group"] for g in load_groups(groups_path)}
    for name, value in (("--fixes", fixes), ("--group", group)):
        if value and value not in known:
            errors.append(f"{name} {value!r} is not a group in friction-groups.csv "
                          "(friction.py groups lists them)")
    fields = {"task": task, "hardest": hardest, "helped": helped}
    for name, value in fields.items():
        if "\n" in str(value) or "\r" in str(value):
            errors.append(f"--{name} must be one line")
    if not str(task).strip():
        errors.append("--task is required")
    if errors:
        raise ValueError("\n".join(errors))

    rows = load(path)
    ids = [int(r["id"][1:]) for r in rows if re.fullmatch(r"F\d+", r.get("id", ""))]
    row = {
        "id": f"F{max(ids, default=0) + 1}",
        "timestamp_utc": _now(now).isoformat(timespec="seconds"),
        "run_id": os.environ.get("GITHUB_RUN_ID") or "local",
        "function": function, "task": task.strip(), "outcome": outcome,
        "fixes": fixes, "category": category, "hardest": hardest.strip(),
        "helped": helped.strip(), "minutes_lost": minutes, "group": group,
    }
    target = path or LOG
    new = not os.path.exists(target) or os.path.getsize(target) == 0
    if not new:
        with open(target, "rb") as f:
            f.seek(-1, os.SEEK_END)
            ends_clean = f.read(1) == b"\n"
    with open(target, "a", newline="", encoding="utf-8") as f:
        if not new and not ends_clean:
            f.write("\n")
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow(row)
    return row


# ---------------------------------------------------------------- gaps

def shifts(path=None):
    """Completed shifts since START, oldest first: (end, minutes, run_id)."""
    start = _start()
    if not start:
        return []
    try:
        with open(path or LEDGER, newline="", encoding="utf-8") as f:
            ledger = list(csv.DictReader(f))
    except OSError:
        return []
    out = []
    for r in ledger:
        if r.get("is_error") == "1":
            continue            # a failed run is a different problem
        end = _ts(r.get("timestamp_utc"))
        try:
            minutes = float(r["duration_min"])
        except (KeyError, ValueError, TypeError):   # a cut-off row
            continue
        if end and end >= start:
            out.append((end, minutes, r.get("run_id", "")))
    return sorted(out)


def gaps(rows=None, ledger=None):
    """Each shift since START and whether a row was logged during it: a row
    whose run_id is the shift's, or whose time falls inside
    [end - duration - 5 min, end + 5 min]."""
    rows = load() if rows is None else rows
    stamped = [(_ts(r.get("timestamp_utc")), r.get("run_id"))
               for r in rows if r.get("run_id") != "backfill"]
    out = []
    for end, minutes, run_id in shifts(ledger):
        lo = end - dt.timedelta(minutes=minutes) - GAP_SLACK
        hi = end + GAP_SLACK
        logged = any(rid == run_id or (t and lo <= t <= hi) for t, rid in stamped)
        out.append({"end": end, "minutes": minutes, "run_id": run_id,
                    "logged": logged})
    return out


def silent_run(rows=None, ledger=None):
    """How many of the most recent shifts, in a row, logged nothing."""
    n = 0
    for s in reversed(gaps(rows, ledger)):
        if s["logged"]:
            break
        n += 1
    return n


# ---------------------------------------------------------------- report

def leverage(group, rows):
    """(rows, median minutes, functions, leverage, minutes known?)."""
    mine = [r for r in rows if r.get("group") == group]
    known = [m for m in (_minutes(r.get("minutes_lost")) for r in mine) if m is not None]
    med = statistics.median(known) if known else 1
    funcs = len({r.get("function") for r in mine})
    return len(mine), med, funcs, len(mine) * med * funcs, bool(known)


def recurred(g, rows):
    """Rows logged in a fixed group after the day its fix shipped."""
    resolved = _date(g.get("resolved"))
    if g.get("status") != "fixed" or not resolved:
        return []
    return [r for r in rows if r.get("group") == g["group"]
            and _ts(r.get("timestamp_utc"))
            and _ts(r["timestamp_utc"]).date() > resolved]


def report(rows=None, groups=None, now=None):
    rows = load() if rows is None else rows
    groups = load_groups() if groups is None else groups
    now = _now(now)
    ungrouped = [r for r in rows if not r.get("group") and r.get("category") != "none"]
    print(f"UNGROUPED ({len(ungrouped)}) — give each a group, new or existing")
    for r in ungrouped:
        t = _ts(r.get("timestamp_utc"))
        age = f"{(now - t).days}d" if t else "?"
        print(f"  {r.get('id') or '?':>4} {age:>4} {r.get('function') or '?':<12} "
              f"{r.get('category') or '?':<9} {r.get('hardest') or ''}")
    nones = sum(1 for r in rows if not r.get("group") and r.get("category") == "none")
    if nones:
        print(f"  (+{nones} 'none' rows, which need no group)")

    print("\nGROUPS by leverage (rows x median minutes x functions; "
          "'blocked' = 60)")
    live = [g for g in groups if g.get("status") not in ("fixed", "wontfix")]
    scored = sorted(((leverage(g["group"], rows), g) for g in live),
                    key=lambda x: -x[0][3])
    for (n, med, funcs, lev, known), g in scored:
        med_s = f"{med:g}" if known else "?"
        print(f"  {g['group']:>4} {lev:>6g}  {n} rows x {med_s} min x {funcs} fn  "
              f"[{g.get('status')}{' ' + g['item'] if g.get('item') else ''}] "
              f"{g.get('title')}")
    back = [(g, recurred(g, rows)) for g in groups if g.get("status") == "fixed"]
    again = [(g, rs) for g, rs in back if rs]
    if again:
        print("\nRECURRED — fixed, then logged again")
        for g, rs in again:
            print(f"  {g['group']:>4} fixed {g['resolved']}, {len(rs)} row(s) since "
                  f"({', '.join(r['id'] for r in rs)}): {g.get('title')}")
    held = [g for g, rs in back if not rs]
    if held:
        print(f"\nFIXED and holding: {', '.join(g['group'] for g in held)}")
    return {"ungrouped": ungrouped, "ranked": scored, "recurred": again}


def list_groups(rows=None, groups=None):
    rows = load() if rows is None else rows
    groups = load_groups() if groups is None else groups
    order = {s: i for i, s in enumerate(["open", "queued", "parked", "fixed", "wontfix"])}
    for g in sorted(groups, key=lambda g: order.get(g.get("status"), 9)):
        n = sum(1 for r in rows if r.get("group") == g["group"])
        print(f"  {g['group']:>4} {g.get('status', ''):<8} {n:>2} rows  {g.get('title')}")


# ---------------------------------------------------------------- evaluate

def checks(rows=None, groups=None, ledger=None, now=None):
    """D15's checks (a)-(h): list of (id, label, value, threshold, verdict),
    verdict one of pass / fail / not yet / judge."""
    rows = load() if rows is None else rows
    groups = load_groups() if groups is None else groups
    now = _now(now)
    start = _start()
    win = window(rows)
    out = []

    g = gaps(rows, ledger)
    if g:
        share = sum(s["logged"] for s in g) / len(g)
        run = silent_run(rows, ledger)
        ok = share >= LOG_SHARE and run < SILENT_RUN
        out.append(("a", "shifts that logged a row",
                    f"{share:.0%} of {len(g)}; {run} silent in a row now",
                    f">= {LOG_SHARE:.0%}; < {SILENT_RUN} in a row",
                    "pass" if ok else "fail"))
    else:
        out.append(("a", "shifts that logged a row", "no shift since START",
                    f">= {LOG_SHARE:.0%}", "not yet"))

    if win:
        none = sum(r.get("category") == "none" for r in win) / len(win)
        lo, hi = NONE_SHARE
        out.append(("b", '"none" rows', f"{none:.0%} of {len(win)}",
                    f"{lo:.0%}-{hi:.0%}", "pass" if lo <= none <= hi else "fail"))
    else:
        out.append(("b", '"none" rows', "no rows", "", "not yet"))

    out.append(("c", "rows naming a specific doc, tool, rule or allowance",
                f"{min(SAMPLE, sum(r.get('category') != 'none' for r in win))} "
                "rows printed below", "most", "judge"))

    stale = [r for r in win if not r.get("group") and r.get("category") != "none"
             and now - _ts(r["timestamp_utc"]) > dt.timedelta(days=UNGROUPED_DAYS)]
    out.append(("d", f"rows ungrouped after {UNGROUPED_DAYS} days",
                f"{len(stale)}" + (f" ({', '.join(r['id'] for r in stale)})" if stale else ""),
                "0", ("pass" if not stale else "fail") if win else "not yet"))

    age = (now - start).days if start else 0
    fixed = [x for x in groups if x.get("status") == "fixed" and x.get("item")
             and _date(x.get("resolved")) and start
             and _date(x["resolved"]) >= start.date()]
    due = age >= RESULTS_DAYS
    out.append(("e", "groups fixed by a shipped change", f"{len(fixed)}",
                f">= {FIXED_GROUPS}",
                ("pass" if len(fixed) >= FIXED_GROUPS else "fail") if due else "not yet"))

    old = [x for x in fixed
           if (now.date() - _date(x["resolved"])).days >= RECUR_DAYS]
    held = []
    for x in old:
        resolved = _date(x["resolved"])
        mine = [(r, _ts(r["timestamp_utc"]).date()) for r in win
                if r.get("group") == x["group"]]
        before = sum(d <= resolved for _, d in mine)
        after = sum(resolved < d <= resolved + dt.timedelta(days=RECUR_DAYS)
                    for _, d in mine)
        if before >= RECUR_BEFORE:
            held.append((x["group"], before, after))
    good = [h for h in held if h[2] <= RECUR_AFTER]
    value = ", ".join(f"{gid}: {b} before, {a} after" for gid, b, a in held) or \
        f"no fixed group with {RECUR_BEFORE}+ rows is {RECUR_DAYS} days old"
    out.append(("f", "a fix that held", value,
                f">= 1 group with {RECUR_BEFORE}+ before, <= {RECUR_AFTER} after",
                ("pass" if good else "fail") if due and old else "not yet"))

    if win:
        share = sum(bool(r.get("fixes")) for r in win) / len(win)
        out.append(("g", "rows that fix a group", f"{share:.0%} of {len(win)}",
                    f"<= {FIX_SHARE:.0%}", "pass" if share <= FIX_SHARE else "fail"))
    else:
        out.append(("g", "rows that fix a group", "no rows", "", "not yet"))

    out.append(("h", "a week's processing", "the reviewer states it",
                f"about {PROCESS_MINUTES} min", "judge"))
    return out


def verdict(results, rows=None, groups=None, now=None):
    """D15's verdict from the checks: keep, change or not yet. Stop is named
    inside change's reason, because it turns on the last monthly read, which
    D15 records and these rows do not."""
    by = {c[0]: c[4] for c in results}
    start = _start()
    if not start:
        return "not yet", "START is not set: friction.py has not landed on main"
    failed = [k for k, v in by.items() if v == "fail"]
    if by["e"] == "not yet" or by["f"] == "not yet":
        why = (f"under {RESULTS_DAYS} days since START, or no fix "
               f"{RECUR_DAYS} days old")
        if failed:
            # D15 reads collection daily and processing weekly: a failure
            # there is acted on now, before the monthly verdict.
            why += ("; failing now: " + ", ".join(f"({k})" for k in failed)
                    + ", for the weekly review to act on")
        return "not yet", why
    if not failed:
        return "keep", ("every measured check passes; confirm (c) and (h) "
                        "by judgement before recording it")
    parts = []
    if any(k in failed for k in "abc"):
        parts.append("(a)-(c) failed: change how rows are written")
    elif any(k in failed for k in "def"):
        parts.append("(d)-(f) failed with (a)-(c) passing: change how rows "
                     "are processed")
    if "g" in failed:
        parts.append("guardrail (g) tripped: friction work is capped at one "
                     "item a shift until the next read")
    why = "; ".join(parts)
    if any(k in failed for k in "ef"):
        # Stop needs the last monthly read's record, which lives in D15.
        why += ("; if (e)-(f) also failed at the last monthly read after a "
                "change, the verdict is stop")
    return "change", why + " (a process change: CLAUDE.md §4)"


def evaluate(rows=None, groups=None, ledger=None, now=None, seed=None,
             decisions=None):
    rows = load() if rows is None else rows
    groups = load_groups() if groups is None else groups
    print("D15's decision rule, verbatim (DECISIONS.md):\n")
    print(rule_text(decisions) or "  (D15's rule was not found in DECISIONS.md)")
    print()
    missing = drift(decisions)
    if missing:
        print("WARNING: D15 no longer states these thresholds the code uses:")
        for p in missing:
            print(f"  - {p}")
        print()
    start = _start()
    print(f"START: {START or 'not set (friction.py has not landed)'}")
    results = checks(rows, groups, ledger, now)
    for cid, label, value, threshold, v in results:
        print(f"  ({cid}) {v.upper():<8} {label}: {value}"
              + (f"  [threshold {threshold}]" if threshold else ""))
    win = [r for r in window(rows) if r.get("category") != "none"]
    if win:
        pick = random.Random(seed).sample(win, min(SAMPLE, len(win)))
        print(f"\n(c) {len(pick)} random rows: does most name a specific doc, "
              "tool, rule or allowance?")
        for r in pick:
            print(f"  {r.get('id') or '?':>4} {r.get('category') or '?':<9} "
                  f"{r.get('hardest') or ''}")
    if any(c[0] == "g" and c[4] == "fail" for c in results):
        print("\nGUARDRAIL tripped: friction work is capped at one item a shift "
              "until the next read.")
    v, why = verdict(results, rows, groups, now)
    print(f"\nVERDICT: {v.upper()} — {why}")
    return v, results


def print_gaps():
    g = gaps()
    if not _start():
        print("START is not set: friction.py has not landed, so no shift is counted.")
        return g
    for s in g:
        print(f"  {s['end']:%Y-%m-%d %H:%M}  {s['minutes']:>5.1f} min  "
              f"{'logged' if s['logged'] else 'SILENT'}  {s['run_id']}")
    if g:
        share = sum(s["logged"] for s in g) / len(g)
        print(f"\n{share:.0%} of {len(g)} shifts logged a row "
              f"(D15 (a): {LOG_SHARE:.0%}+); {silent_run()} silent in a row now "
              f"({SILENT_RUN} escalate).")
    else:
        print("No completed shift since START.")
    return g


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="log one finished item")
    a.add_argument("--function", required=True)
    a.add_argument("--task", required=True)
    a.add_argument("--outcome", required=True)
    a.add_argument("--category", required=True)
    a.add_argument("--hardest", default="")
    a.add_argument("--helped", default="")
    a.add_argument("--minutes", default="")
    a.add_argument("--fixes", default="")
    a.add_argument("--group", default="")
    sub.add_parser("groups", help="groups, to tag a repeat")
    sub.add_parser("report", help="weekly review: ungrouped rows, groups by leverage")
    e = sub.add_parser("evaluate", help="D15's rule, then its checks")
    e.add_argument("--seed", type=int, default=None)
    sub.add_parser("gaps", help="shifts since START with no row")
    args = ap.parse_args(argv)

    if args.cmd == "add":
        try:
            row = add(args.function, args.task, args.outcome, args.category,
                      args.hardest, args.helped, args.minutes, args.fixes,
                      args.group)
        except ValueError as err:
            sys.exit(f"friction.py add: refused\n{err}")
        print(f"logged {row['id']}")
    elif args.cmd == "groups":
        list_groups()
    elif args.cmd == "report":
        report()
    elif args.cmd == "evaluate":
        evaluate(seed=args.seed)
    elif args.cmd == "gaps":
        print_gaps()


if __name__ == "__main__":
    main()
