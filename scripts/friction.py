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

At the end of every shift, the retro: its rows, then its one vote.

    venv/bin/python scripts/friction.py retro      # this shift's rows, the requests
    venv/bin/python scripts/friction.py vote --request R3 --row F402 \\
        --saved 10 --why "how R3 would have saved those minutes"
    venv/bin/python scripts/friction.py vote --new "what to build or change" \\
        --row F402 --saved 10 --why "..." [--group G2] [--distinct]
    venv/bin/python scripts/friction.py vote --none --why "why nothing would have"
    venv/bin/python scripts/friction.py requests [--due]   # ranked by minutes saved
    venv/bin/python scripts/friction.py mark R3 queued C21  # | shipped <commit>
                                                   # | declined "why" | merged R2
    venv/bin/python scripts/friction.py evaluate --requests  # the requests rule

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

REQUESTS (D15, amended 2026-11-20)

Rows were logged and grouped on time, and nothing turned a group into a fix:
on 11-20 no group had ever been `queued`, and none of 31 open was fixed since
START. A group says what hurt, not what to build, and only the weekly review
could queue one. A request says what to build; the shift that just lost the
minutes is the one that votes for it.

.github/friction-requests.csv, one row per request:
    request   R1, R2, ... (renumber on merge, as F ids)
    title     one line: what to build or change
    group     the friction group it answers, else blank
    status    open | queued | shipped | declined | merged
    item      queued: the queue id; shipped: the commit or PR; merged: the
              request it joined
    opened, resolved, note

.github/friction-votes.csv, append-only, one row per retro:
    id V1, V2, ...; timestamp_utc; run_id; request (an R id, or "none" for an
    abstention); row (the F id it cites); saved (minutes); why (one line)

WHAT THE REQUESTS BUILD MUST KEEP
- One retro a shift: `vote` refuses a second from the same GITHUB_RUN_ID. A
  local session's retro cites "local" rows from the last LOCAL_HOURS.
- A vote is evidence or nothing: it cites a non-"none" row this shift logged,
  that no other vote cites, and claims at most that row's minutes lost
  ("blocked" = 60). An abstention needs only its reason.
- A new request whose group already has an open one is refused unless
  --distinct: duplicates split the votes, and the bar is never reached.
- Requests rank by minutes saved, votes of merged requests included. One is
  past the bar at BAR_VOTES votes from different shifts; `backlog_status.py`
  prints each open one past it, for /backlog §2 to rank.
- `mark ... shipped` marks the request's group fixed, so D15 (e) counts it and
  (f) and RECURRED test it. `mark ... queued` refuses past QUEUED_CAP.
- The requests rule's thresholds are constants here, checked against D15's
  text like the decision rule's; `evaluate --requests` quotes it first.
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
START = "2026-10-27T16:40:00+00:00"

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

REQUESTS = os.path.join(ROOT, ".github", "friction-requests.csv")
VOTES = os.path.join(ROOT, ".github", "friction-votes.csv")
REQUEST_FIELDS = ["request", "title", "group", "status", "item", "opened",
                  "resolved", "note"]
VOTE_FIELDS = ["id", "timestamp_utc", "run_id", "request", "row", "saved", "why"]
REQUEST_STATUSES = ["open", "queued", "shipped", "declined", "merged"]

# When the requests landed on main, a full UTC timestamp like START. The
# landing commit sets it; no vote before it is read.
REQ_START = None

# The requests rule's thresholds (D15, amended 2026-11-20). test_friction
# checks D15 states each, as for the decision rule's.
BAR_VOTES = 3             # votes, each a different shift's: past the bar
QUEUED_CAP = 2            # requests queued at once; `mark` enforces it
RETRO_SHARE = 0.80        # (r1) share of shifts that hold a retro
VOTE_SHARE = 1 / 3        # (r2) retros that vote for a request
CONVERGE_DAYS = 14        # (r3) its read's age
CONVERGED = 2             # (r3) requests past the bar
REQ_RESULTS_DAYS = 28     # (r4)-(r5) and "not yet"
SHIPPED = 1               # (r4) requests shipped
DUE_DAYS = 14             # (r5) longest past the bar, neither queued nor declined
LOCAL_HOURS = 12          # a local retro's rows: "local" ones this recent

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


def stated_requests():
    """The phrases D15's requests rule must contain, as stated() for its own."""
    return [
        f"(r1) {RETRO_SHARE:.0%}+ of shifts since REQ_START hold a retro",
        f"(r2) at least {_FRACTIONS.get(VOTE_SHARE, VOTE_SHARE)} of retros "
        "vote for a request",
        f"{CONVERGE_DAYS}+ days after REQ_START: (r3) {CONVERGED}+ requests "
        f"past the bar of {_WORDS.get(BAR_VOTES, BAR_VOTES)} votes, each a "
        "different shift's",
        f"{REQ_RESULTS_DAYS}+ days after REQ_START: (r4) {SHIPPED}+ request "
        "shipped",
        f"(r5) no request past the bar for more than {DUE_DAYS} days",
        f"at most {_WORDS.get(QUEUED_CAP, QUEUED_CAP)} requests queued at once",
        f"**Not yet** under {REQ_RESULTS_DAYS} days",
    ]


def rule_text(path=None, label="Decision rule"):
    """A rule in D15, verbatim from DECISIONS.md: its decision rule, or with
    label="Requests rule" the rule its 11-20 amendment set."""
    text = open(path or DECISIONS, encoding="utf-8").read()
    m = re.search(r"^## D15 .*?(\*\*" + re.escape(label) + r"\*\*.*?)\n\n\*\*",
                  text, re.S | re.M)
    if not m or "\n## " in m.group(0):     # found past D15's own section
        return ""
    return m.group(1).strip()


def drift(path=None, label="Decision rule", phrases=None):
    """Phrases in stated() (or `phrases`) that the D15 rule no longer contains."""
    rule = " ".join(rule_text(path, label).split())
    return [p for p in (stated() if phrases is None else phrases) if p not in rule]


def drift_requests(path=None):
    return drift(path, "Requests rule", stated_requests())


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


def _start(value=None, name="START"):
    """START (or REQ_START) as a datetime. A bare date would read as midnight
    and let that day's rows in, the 2026-10-27 seed among them, so it is
    refused."""
    value = START if name == "START" else value
    if not value:
        return None
    if "T" not in value:
        raise ValueError(f"friction.py {name} {value!r} needs a time, in UTC")
    return _ts(value)


def _req_start():
    return _start(REQ_START, "REQ_START")


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

    row = {
        "id": _next_id(load(path), "id", "F"),
        "timestamp_utc": _now(now).isoformat(timespec="seconds"),
        "run_id": os.environ.get("GITHUB_RUN_ID") or "local",
        "function": function, "task": task.strip(), "outcome": outcome,
        "fixes": fixes, "category": category, "hardest": hardest.strip(),
        "helped": helped.strip(), "minutes_lost": minutes, "group": group,
    }
    _append(path or LOG, FIELDS, row)
    return row


def _next_id(rows, key, prefix):
    """The next after the highest, so two branches appending both write it:
    renumber on merge."""
    ids = [int(r[key][len(prefix):]) for r in rows
           if re.fullmatch(prefix + r"\d+", r.get(key) or "")]
    return f"{prefix}{max(ids, default=0) + 1}"


def _append(path, fields, row):
    """Append one row, with the header if the file is new, and a newline first
    if a hand edit left the last line without one."""
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    ends_clean = True
    if not new:
        with open(path, "rb") as f:
            f.seek(-1, os.SEEK_END)
            ends_clean = f.read(1) == b"\n"
    with open(path, "a", newline="", encoding="utf-8") as f:
        if not ends_clean:
            f.write("\n")
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow(row)


def _write_all(path, fields, rows):
    """Rewrite a small table whole. Minimal quoting, "\\n" endings: a file this
    module wrote reads back and rewrites byte for byte."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- gaps

def shifts(path=None, start=None):
    """Completed shifts since START (or `start`), oldest first:
    (end, minutes, run_id)."""
    start = start or _start()
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


def gaps(rows=None, ledger=None, start=None):
    """Each shift since START (or `start`) and whether a row was logged during
    it: a row whose run_id is the shift's, or whose time falls inside
    [end - duration - 5 min, end + 5 min]. The retro's check passes votes."""
    rows = load() if rows is None else rows
    stamped = [(_ts(r.get("timestamp_utc")), r.get("run_id"))
               for r in rows if r.get("run_id") != "backfill"]
    out = []
    for end, minutes, run_id in shifts(ledger, start):
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
    print()
    print_requests(now=now)
    print("  Merge duplicates (friction.py mark R… merged R…): split votes never "
          "reach the bar.")
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


# ---------------------------------------------------------------- requests

def load_requests(path=None):
    return load(path or REQUESTS)


def load_votes(path=None):
    return load(path or VOTES)


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _run_id():
    return os.environ.get("GITHUB_RUN_ID") or "local"


def resolve(rid, reqs):
    """The request a vote for `rid` counts toward: itself, or where its merges
    lead. A loop stops where it closes."""
    by = {r.get("request"): r for r in reqs}
    seen = set()
    while rid in by and by[rid].get("status") == "merged" and rid not in seen:
        seen.add(rid)
        rid = by[rid].get("item", "")
    return rid


def _shift_key(v):
    """A shift's identity, for "each a different shift's". Local sessions
    cannot be told apart, so each local vote is its own."""
    rid = v.get("run_id") or "local"
    return f"local:{v.get('id')}" if rid == "local" else rid


def tally(reqs=None, votes=None):
    """Each request not merged away, with every vote it counts, its merged
    requests' included: {id: {"req", "votes", "saved", "shifts", "bar"}},
    "bar" the time its BAR_VOTES-th shift voted, else None."""
    reqs = load_requests() if reqs is None else reqs
    votes = load_votes() if votes is None else votes
    out = {r["request"]: {"req": r, "votes": []} for r in reqs
           if r.get("status") != "merged"}
    for v in votes:
        target = resolve(v.get("request", ""), reqs)
        if target in out:
            out[target]["votes"].append(v)
    for t in out.values():
        t["votes"].sort(key=lambda v: v.get("timestamp_utc") or "")
        t["saved"] = sum(_int(v.get("saved")) for v in t["votes"])
        seen, t["bar"] = set(), None
        for v in t["votes"]:
            seen.add(_shift_key(v))
            if len(seen) == BAR_VOTES and t["bar"] is None:
                t["bar"] = _ts(v.get("timestamp_utc"))
        t["shifts"] = len(seen)
    return out


def ranked(reqs=None, votes=None):
    """Open and queued requests, most minutes saved first."""
    t = tally(reqs, votes)
    live = [x for x in t.values() if x["req"].get("status") in ("open", "queued")]
    return sorted(live, key=lambda x: (-x["saved"], -x["shifts"],
                                       _int(x["req"]["request"][1:])))


def due(reqs=None, votes=None):
    """Open requests past the bar: /backlog §2 ranks each until it is queued
    or declined."""
    return [x for x in ranked(reqs, votes)
            if x["req"].get("status") == "open" and x["bar"]]


def shift_rows(rows=None, now=None, run_id=None):
    """This shift's friction rows: its run's, or for a local session the
    "local" rows of the last LOCAL_HOURS."""
    rows = load() if rows is None else rows
    run_id = run_id or _run_id()
    if run_id != "local":
        return [r for r in rows if r.get("run_id") == run_id]
    since = _now(now) - dt.timedelta(hours=LOCAL_HOURS)
    return [r for r in rows if r.get("run_id") == "local"
            and (_ts(r.get("timestamp_utc")) or since) > since]


def vote(request="", new="", none=False, row="", saved="", why="", group="",
         distinct=False, path=None, requests_path=None, rows_path=None,
         groups_path=None, now=None):
    """Cast this shift's one vote, or its abstention, refusing anything that
    is not evidence. Returns (the vote, the request it counts for or None)."""
    now = _now(now)
    run_id = _run_id()
    votes, reqs = load_votes(path), load_requests(requests_path)
    rows = load(rows_path)
    request, new, row, why = (str(x or "").strip() for x in (request, new, row, why))
    errors = []
    if [bool(request), bool(new), bool(none)].count(True) != 1:
        errors.append('give exactly one of --request R…, --new "what to build", --none')
    if not why:
        errors.append("--why is required: how the request would have saved the "
                      "minutes, or why no change would have")
    for name, value in (("--why", why), ("--new", new)):
        if "\n" in value or "\r" in value:
            errors.append(f"{name} must be one line")
    if run_id != "local":
        held = [v for v in votes if v.get("run_id") == run_id]
        if held:
            errors.append(f"this shift (run {run_id}) already held its retro: "
                          f"{held[0]['id']}, for {held[0]['request']}")

    target = None
    if request:
        by = {r["request"]: r for r in reqs}
        final = resolve(request, reqs)
        if request not in by:
            errors.append(f"--request {request!r} is not in friction-requests.csv "
                          "(friction.py requests lists them)")
        elif final not in by or by[final].get("status") == "merged":
            errors.append(f"{request} was merged into {final!r}, which is not an "
                          "open request")
        else:
            target = by[final]
            st = target.get("status")
            if st == "shipped":
                errors.append(f"{final} shipped ({target.get('item')}, "
                              f"{target.get('resolved')}). If it did not hold, "
                              "vote --new for what would, and say so in --why")
            elif st == "declined":
                errors.append(f"{final} was declined {target.get('resolved')}: "
                              f"{target.get('note')}. If that no longer holds, "
                              "vote --new and say what changed")

    cited = None
    if not none:
        if not row:
            errors.append("--row is required: this shift's friction row the "
                          "request would have saved")
        else:
            cited = next((r for r in rows if r.get("id") == row), None)
            if cited is None:
                errors.append(f"--row {row!r} is not in friction.csv")
            else:
                if row not in {r["id"] for r in shift_rows(rows, now, run_id)}:
                    where = (f"run {run_id}" if run_id != "local" else
                             f"a local session in the last {LOCAL_HOURS} hours")
                    errors.append(f"--row {row} was not logged by this shift "
                                  f"({where}): a vote cites friction its voter hit")
                if cited.get("category") == "none":
                    errors.append(f"--row {row} is a 'none' row: it lost nothing")
                taken = next((v for v in votes if v.get("row") == row), None)
                if taken:
                    errors.append(f"--row {row} already backs {taken['id']}")
        lost = _minutes(cited.get("minutes_lost")) if cited else None
        s = str(saved).strip()
        if not re.fullmatch(r"\d+", s) or int(s) < 1:
            errors.append(f"--saved {saved!r} must be whole minutes, 1 or more")
        elif cited is not None and (lost is None or int(s) > lost):
            errors.append(f"--saved {s} is more than {row} lost "
                          f"({cited.get('minutes_lost') or 'nothing recorded'}): "
                          "a vote claims at most its row's minutes")
    elif row or str(saved).strip():
        errors.append("--none takes no --row or --saved: it says why nothing "
                      "would have helped")

    if new:
        group = (group or (cited or {}).get("group") or "").strip()
        if group and group not in {g["group"] for g in load_groups(groups_path)}:
            errors.append(f"--group {group!r} is not a group in friction-groups.csv")
        elif group and not distinct:
            same = [r for r in reqs if r.get("group") == group
                    and r.get("status") in ("open", "queued")]
            if same:
                errors.append(
                    f"{group} already has an open request: "
                    + "; ".join(f"{r['request']} {r['title']}" for r in same)
                    + ". Vote for it with --request, or pass --distinct if "
                    "yours is a different change")
    elif group:
        errors.append("--group goes with --new: a request's group is set when "
                      "it opens")
    if errors:
        raise ValueError("\n".join(errors))

    if new:
        target = {"request": _next_id(reqs, "request", "R"), "title": new,
                  "group": group, "status": "open", "item": "",
                  "opened": now.date().isoformat(), "resolved": "", "note": ""}
        _append(requests_path or REQUESTS, REQUEST_FIELDS, target)
    v = {"id": _next_id(votes, "id", "V"),
         "timestamp_utc": now.isoformat(timespec="seconds"), "run_id": run_id,
         "request": target["request"] if target else "none",
         "row": "" if none else row, "saved": "" if none else str(int(saved)),
         "why": why}
    _append(path or VOTES, VOTE_FIELDS, v)
    return v, target


_MOVES = {"queued": ("open",), "shipped": ("open", "queued"),
          "declined": ("open", "queued"), "merged": ("open", "queued"),
          "open": ("declined", "shipped")}


def mark(rid, status, value="", requests_path=None, groups_path=None, now=None):
    """Move a request on, and its friction group with it: queued makes an open
    group queued, shipped makes it fixed (D15 (e) counts it; (f) and RECURRED
    test it), declined returns a group it had queued to open.
    Returns (the request, the group changed or None)."""
    today = _now(now).date().isoformat()
    value = str(value or "").strip()
    reqs = load_requests(requests_path)
    by = {r["request"]: r for r in reqs}
    if rid not in by:
        raise ValueError(f"{rid!r} is not a request (friction.py requests)")
    r = by[rid]
    if status not in _MOVES:
        raise ValueError(f"status {status!r} is not one of {', '.join(_MOVES)}")
    if r.get("status") not in _MOVES[status]:
        raise ValueError(f"{rid} is {r.get('status')}; only "
                         f"{' or '.join(_MOVES[status])} can become {status}")
    if status != "open" and not value:
        need = {"queued": "the queue id (PLAN C…, PRD #…, an epic ticket)",
                "shipped": "the commit or PR", "declined": "the reason",
                "merged": "the request it joins"}[status]
        raise ValueError(f"{status} needs {need}")
    if status == "queued":
        n = sum(x.get("status") == "queued" for x in reqs)
        if n >= QUEUED_CAP:
            raise ValueError(f"{n} requests are queued already, the most at once "
                             f"(D15's requests rule): ship or decline one first")
    if status == "merged":
        if value not in by or value == rid or resolve(value, reqs) == rid:
            raise ValueError(f"{value!r} is not another request to merge into")
        if by[resolve(value, reqs)].get("status") not in ("open", "queued"):
            raise ValueError(f"{value} is not open or queued: merge into a live one")

    r["status"] = status
    if status in ("queued", "shipped", "merged"):
        r["item"] = value
    if status == "declined":
        r["note"] = value
    r["resolved"] = "" if status in ("open", "queued") else today
    if status == "open" and value:
        r["note"] = value
    _write_all(requests_path or REQUESTS, REQUEST_FIELDS, reqs)

    changed = None
    groups = load_groups(groups_path)
    g = next((x for x in groups if x["group"] == r.get("group")), None)
    if g and status == "queued" and g.get("status") == "open":
        g.update(status="queued", item=value)
        changed = g
    elif g and status == "shipped" and g.get("status") not in ("fixed", "wontfix"):
        g.update(status="fixed", item=value, resolved=today)
        g["note"] = "; ".join(x for x in (g.get("note"), f"{today}: fixed by "
                                          f"{rid}, {r['title']}") if x)
        changed = g
    elif (g and status == "declined" and g.get("status") == "queued"
          and g.get("item") == r.get("item")):
        g.update(status="open", item="")
        changed = g
    if changed:
        _write_all(groups_path or GROUPS, GROUP_FIELDS, groups)
    return r, changed


def print_requests(reqs=None, votes=None, now=None, limit=None):
    reqs = load_requests() if reqs is None else reqs
    votes = load_votes() if votes is None else votes
    now = _now(now)
    live = ranked(reqs, votes)
    print(f"REQUESTS by minutes saved (past the bar: {BAR_VOTES} votes, each a "
          "different shift's)")
    if not live:
        print("  none open: a retro opens one with vote --new")
    for x in live[:limit]:
        r = x["req"]
        bar = ""
        if x["bar"]:
            bar = (f"  PAST THE BAR {(now - x['bar']).days}d"
                   + (": rank it, /backlog §2" if r["status"] == "open" else ""))
        print(f"  {r['request']:>4} {x['saved']:>4} min  {len(x['votes'])} votes  "
              f"[{r['status']}{' ' + r['item'] if r.get('item') else ''}"
              f"{' ' + r['group'] if r.get('group') else ''}]{bar}  {r['title']}")
    if limit and len(live) > limit:
        print(f"  … {len(live) - limit} more: friction.py requests")
    done = {s: sum(r.get("status") == s for r in reqs)
            for s in ("shipped", "declined", "merged")}
    if any(done.values()):
        print("  " + ", ".join(f"{n} {s}" for s, n in done.items() if n))
    return live


def retro(rows=None, reqs=None, votes=None, now=None, run_id=None):
    """The end-of-shift retrospective: this shift's rows, the requests, and
    the one command that closes it."""
    rows = load() if rows is None else rows
    votes = load_votes() if votes is None else votes
    run_id = run_id or _run_id()
    mine = shift_rows(rows, now, run_id)
    citable = [r for r in mine if r.get("category") != "none"]
    lost = sum(_minutes(r.get("minutes_lost")) or 0 for r in citable)
    who = (f"run {run_id}" if run_id != "local" else
           f"this session (local rows, last {LOCAL_HOURS} hours)")
    print(f"RETRO for {who}: {len(mine)} rows, {len(citable)} to cite, "
          f"{lost} minutes lost")
    cited = {v.get("row") for v in votes}
    for r in mine:
        print(f"  {r.get('id'):>5} {r.get('category'):<9} "
              f"{r.get('minutes_lost') or '0':>7} min {r.get('group') or '-':>4}"
              f"{' (cited)' if r.get('id') in cited else ''}  "
              f"{r.get('hardest') or r.get('task')}")
    if not mine:
        print("  no rows yet: log each finished item first (friction.py add)")
    held = [v for v in votes if run_id != "local" and v.get("run_id") == run_id]
    if held:
        v = held[0]
        print(f"\nRetro held: {v['id']}, for {v['request']}"
              + (f", citing {v['row']} ({v['saved']} min)" if v.get("row") else "")
              + f": {v['why']}")
        return held[0]
    print()
    print_requests(reqs, votes, now, limit=10)
    print("\nClose it with this shift's one vote: the row a change would have "
          "saved, and at most the minutes that row lost.")
    print("  friction.py vote --request R… --row F… --saved N --why \"how\"")
    print("  friction.py vote --new \"what to build or change\" --row F… "
          "--saved N --why \"how\"")
    print("  friction.py vote --none --why \"why no change would have helped\"")
    return None


def request_checks(votes=None, reqs=None, ledger=None, now=None):
    """The requests rule's checks (r1)-(r5): (id, label, value, threshold,
    verdict), verdict one of pass / fail / not yet."""
    votes = load_votes() if votes is None else votes
    reqs = load_requests() if reqs is None else reqs
    now = _now(now)
    start = _req_start()
    win = [v for v in votes if start
           and (_ts(v.get("timestamp_utc")) or start - GAP_SLACK) >= start]
    out = []

    g = gaps(win, ledger, start) if start else []
    if g:
        share = sum(s["logged"] for s in g) / len(g)
        out.append(("r1", "shifts that held a retro", f"{share:.0%} of {len(g)}",
                    f">= {RETRO_SHARE:.0%}",
                    "pass" if share >= RETRO_SHARE else "fail"))
    else:
        out.append(("r1", "shifts that held a retro", "no shift since REQ_START",
                    f">= {RETRO_SHARE:.0%}", "not yet"))

    if win:
        share = sum(v.get("request") != "none" for v in win) / len(win)
        out.append(("r2", "retros that voted for a request",
                    f"{share:.0%} of {len(win)}", f">= {VOTE_SHARE:.0%}",
                    "pass" if share >= VOTE_SHARE else "fail"))
    else:
        out.append(("r2", "retros that voted for a request", "no retro",
                    f">= {VOTE_SHARE:.0%}", "not yet"))

    age = (now - start).days if start else 0
    t = tally(reqs, votes)
    past = sorted(k for k, x in t.items() if x["bar"] and start and x["bar"] >= start)
    out.append(("r3", "requests past the bar", f"{len(past)}"
                + (f" ({', '.join(past)})" if past else ""), f">= {CONVERGED}",
                "pass" if len(past) >= CONVERGED else
                "fail" if age >= CONVERGE_DAYS else "not yet"))

    shipped = [r["request"] for r in reqs if r.get("status") == "shipped" and start
               and (_date(r.get("resolved")) or dt.date.min) >= start.date()]
    out.append(("r4", "requests shipped", f"{len(shipped)}"
                + (f" ({', '.join(shipped)})" if shipped else ""), f">= {SHIPPED}",
                "pass" if len(shipped) >= SHIPPED else
                "fail" if age >= REQ_RESULTS_DAYS else "not yet"))

    stale = [f"{k} {(now - x['bar']).days}d" for k, x in t.items()
             if x["req"].get("status") == "open" and x["bar"]
             and now - x["bar"] > dt.timedelta(days=DUE_DAYS)]
    out.append(("r5", f"open past the bar over {DUE_DAYS} days",
                f"{len(stale)}" + (f" ({', '.join(stale)})" if stale else ""), "0",
                "fail" if stale else "pass" if past else "not yet"))
    return out


def request_verdict(results, now=None):
    """The requests rule's verdict: keep, change or not yet; stop is named
    inside change's reason, since it turns on the last read's record."""
    start = _req_start()
    if not start:
        return "not yet", "REQ_START is not set: the requests have not landed on main"
    by = {c[0]: c[4] for c in results}
    failed = [k for k, v in by.items() if v == "fail"]
    if (_now(now) - start).days < REQ_RESULTS_DAYS or (
            not failed and any(by[k] == "not yet" for k in ("r1", "r2", "r3", "r4"))):
        why = f"under {REQ_RESULTS_DAYS} days since REQ_START, or a check unread"
        if failed:
            why += ("; failing now: " + ", ".join(f"({k})" for k in failed)
                    + ", for the weekly review to act on")
        return "not yet", why
    if not failed:
        return "keep", "every check passes"
    parts = []
    if {"r1", "r2"} & set(failed):
        parts.append("(r1)-(r2) failed: change the retro")
    if "r3" in failed:
        parts.append("(r3) failed: change how requests are named and merged")
    if {"r4", "r5"} & set(failed):
        parts.append("(r4)-(r5) failed: change how /backlog takes them")
    why = "; ".join(parts)
    if "r4" in failed:
        why += ("; if (r4) also failed at the last read after a change, the "
                "verdict is stop")
    return "change", why + " (a process change: CLAUDE.md §4)"


def evaluate_requests(votes=None, reqs=None, ledger=None, now=None,
                      decisions=None):
    votes = load_votes() if votes is None else votes
    reqs = load_requests() if reqs is None else reqs
    print("D15's requests rule, verbatim (DECISIONS.md):\n")
    print(rule_text(decisions, "Requests rule")
          or "  (the requests rule was not found in D15)")
    print()
    missing = drift_requests(decisions)
    if missing:
        print("WARNING: D15 no longer states these thresholds the code uses:")
        for p in missing:
            print(f"  - {p}")
        print()
    print(f"REQ_START: {REQ_START or 'not set (the requests have not landed)'}")
    results = request_checks(votes, reqs, ledger, now)
    for cid, label, value, threshold, v in results:
        print(f"  ({cid}) {v.upper():<8} {label}: {value}"
              + (f"  [threshold {threshold}]" if threshold else ""))
    start = _req_start()
    win = [v for v in votes if start and v.get("request") != "none"
           and (_ts(v.get("timestamp_utc")) or start) >= start]
    print(f"\nMinutes saved, claimed (reported, never decisive): "
          f"{sum(_int(v.get('saved')) for v in win)} over {len(win)} votes")
    v, why = request_verdict(results, now)
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
    e.add_argument("--requests", action="store_true",
                   help="the requests rule (D15, amended 11-20) instead")
    sub.add_parser("gaps", help="shifts since START with no row")
    sub.add_parser("retro", help="end of shift: this shift's rows, the requests")
    v = sub.add_parser("vote", help="this shift's one vote, or its abstention")
    v.add_argument("--request", default="")
    v.add_argument("--new", default="", metavar="TITLE")
    v.add_argument("--none", action="store_true")
    v.add_argument("--row", default="")
    v.add_argument("--saved", default="")
    v.add_argument("--why", default="")
    v.add_argument("--group", default="")
    v.add_argument("--distinct", action="store_true")
    q = sub.add_parser("requests", help="requests ranked by minutes saved")
    q.add_argument("--due", action="store_true", help="only those past the bar")
    m = sub.add_parser("mark", help="queue, ship, decline, merge or reopen a request")
    m.add_argument("request")
    m.add_argument("status", choices=list(_MOVES))
    m.add_argument("value", nargs="?", default="")
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
        if args.requests:
            evaluate_requests()
        else:
            evaluate(seed=args.seed)
    elif args.cmd == "gaps":
        print_gaps()
    elif args.cmd == "retro":
        retro()
    elif args.cmd == "vote":
        try:
            cast, req = vote(args.request, args.new, args.none, args.row,
                             args.saved, args.why, args.group, args.distinct)
        except ValueError as err:
            sys.exit(f"friction.py vote: refused\n{err}")
        if req is None:
            print(f"retro held: {cast['id']}, no vote")
        else:
            x = tally().get(req["request"], {})
            moved = (f" ({args.request} was merged into it)"
                     if args.request and args.request != req["request"] else "")
            print(f"retro held: {cast['id']} for {req['request']}{moved}, now "
                  f"{x.get('saved', 0)} min over {len(x.get('votes', []))} votes"
                  + (", past the bar" if x.get("bar") else ""))
    elif args.cmd == "requests":
        if args.due:
            for x in due():
                r = x["req"]
                print(f"  {r['request']} {x['saved']} min over {x['shifts']} "
                      f"shifts [{r.get('group') or '-'}] {r['title']}")
        else:
            print_requests()
    elif args.cmd == "mark":
        try:
            r, g = mark(args.request, args.status, args.value)
        except ValueError as err:
            sys.exit(f"friction.py mark: refused\n{err}")
        print(f"{r['request']} {r['status']}"
              + (f"; group {g['group']} now {g['status']}" if g else ""))


if __name__ == "__main__":
    main()
