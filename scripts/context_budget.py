#!/usr/bin/env python3
"""Measure the context every session pays for, and fail when it grows.

Agentic setups bloat. Each session adds a doc, a rule, a tracker, and none of
it is ever removed, until CLAUDE.md is long enough that Claude starts ignoring
the instructions that matter. Anthropic's own guidance is explicit about this:
"Bloated CLAUDE.md files cause Claude to ignore your actual instructions" and
"for each line, ask: would removing this cause Claude to make mistakes?"

Good intentions don't survive that pressure, so this makes the cost visible and
gives it a ceiling — the same reason the Polly budget lives in code rather than
in a paragraph.

    venv/bin/python scripts/context_budget.py          # report
    venv/bin/python scripts/context_budget.py --check  # exit 1 if CLAUDE.md is over

Only the ALWAYS tier fails a build. Everything else is reported and left to
judgement, because a project that grows legitimately needs more words, and a
cap that blocks is a cap agents route around. That mattered most for the
corpus counts: when exceeding TECH_DEBT's cap broke CI, the cheapest way to
stay green was to not record the finding -- a control producing dishonesty
rather than hygiene, which is the failure CLAUDE.md section 4 warns about.

Two tiers, because they cost differently:

  ALWAYS   loaded into every single session, whatever the task. The expensive
           tier: every word here is paid for even when irrelevant.
  ORIENT   read during /pickup or /shift startup. Cheaper, but still per-shift.

Reference material that is read only when a task needs it is NOT counted —
that is what skills and PRD §6 are for, and moving detail there is usually the
right fix when a budget is breached.
"""
import argparse
import csv
import glob
import subprocess
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Budgets are deliberately tight, and this one is the only hard limit: bloat
# here has a specific documented effect -- Claude starts ignoring the file, which
# has already happened on this project. Raising it is a decision to spend more of
# every future session on the same words, so it needs a reason beyond "it grew".
ALWAYS = {"CLAUDE.md": 1200}
ORIENT = {
    "README.md#Picking this up": 400,
    # 1800 -> 1950 on 2026-09-25: every backlog row gained a Status and the
    # section a research-questions queue -- what the ready-work count reads
    # (D11). The tracker became machine-readable, not longer for its own sake.
    "PRD.md#0.": 1950,
    # Raised from 900 on 2026-09-20: it contradicted the 10-entry retention
    # cap in CORPUS below. Entries run ~200 words, so ten of them plus the
    # template header can never fit in 900 — one of the two controls had to
    # move, and the audit needs ten entries of evidence to read.
    # 2400 -> 2600 on 2026-09-21: the entry template gained a "Better?"
    # section at three horizons, which every entry now carries. The retention
    # cap is ten entries and the audit needs all ten, so the budget moved
    # rather than the retention -- the same trade as the 900 -> 2400 raise.
    "WORKLOG.md": 2600,
    # Raised 1800 -> 1900 on 2026-09-21, using the escape hatch below for the
    # first time and deliberately. 1800 was a first guess made when the skill
    # covered four lanes and one budget. It now covers six workstreams, four
    # separate resource budgets, escalation, owner reporting and close-out --
    # scope the project actually gained, not prose that crept in. Six trims in
    # one day had reached the point where each one removed real guidance, and
    # grinding further was itself the waste the budget exists to prevent.
    # 1900 -> 1950 on 2026-09-24: shifts gained a way to get a render at all
    # (dry runs by request, #27). The old line said "at most one dry run" and
    # never how -- shifts inferred a route from a comment in shift.yml that had
    # never worked. Four lines of mechanism, not prose creep.
    # 1950 -> 2050 on 2026-09-24, before the owner's ten days away: shifts
    # gained a way to propose the one change they cannot push (workflow files,
    # applied on the owner's label) and to see why an upload failed. Two
    # mechanisms that remove the owner from the loop, not prose creep.
    # 2050 -> 2100 on 2026-09-25: the ready-work floor (D11) replaced "an empty
    # lane is PM's problem", which never fired while blocked items filled it.
    ".claude/skills/shift/SKILL.md": 2100,
    ".claude/skills/pickup/SKILL.md": 700,
}


def words(text):
    return len(text.split())


def section(path, heading):
    """Words in one '## ' section — PRD §0 is read every shift, §6 is not."""
    try:
        raw = open(os.path.join(ROOT, path), encoding="utf-8").read()
    except OSError:
        return None
    lines = raw.split("\n")
    start = next((i for i, l in enumerate(lines)
                  if l.startswith("#") and heading.lower() in l.lower()), None)
    if start is None:
        return None
    depth = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("#")
                and (len(lines[i]) - len(lines[i].lstrip("#"))) <= depth), len(lines))
    return words("\n".join(lines[start:end]))


def measure(spec):
    out = []
    for name, budget in spec.items():
        if "#" in name:
            path, heading = name.split("#", 1)
            n = section(path, heading)
        else:
            path = name
            try:
                n = words(open(os.path.join(ROOT, path), encoding="utf-8").read())
            except OSError:
                n = None
        out.append((name, n, budget))
    return out


def report(rows, label):
    over = []
    print(f"\n{label}")
    for name, n, budget in rows:
        if n is None:
            print(f"  {'?':>6}          {name}  (missing)")
            continue
        flag = "OVER" if n > budget else "ok"
        bar = "#" * min(int(n / budget * 20), 30)
        print(f"  {n:>6}/{budget:<5} {flag:4} {bar:<22} {name}")
        if n > budget:
            over.append((name, n, budget))
    return over


# Anthropic price ratios vs input tokens — cache reads are cheap per token but
# dominate a long session because every turn re-reads everything before it.
# Calibrated for Claude Opus 5.5 ($4/$20 per MTok), which shifts run: its cache
# reads are 5% of base input, where every earlier model charged 10%. The
# output/cache-write ratios are unchanged from Opus 5.
WEIGHTS = {"input": 1.0, "cw1h": 2.0, "cw5m": 1.25, "cread": 0.05, "output": 5.0}


def _turns(path):
    for line in open(path, errors="ignore"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message")
        if not isinstance(m, dict) or not m.get("usage"):
            continue
        u, cc = m["usage"], (m["usage"].get("cache_creation") or {})
        yield {
            "input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0),
            "cread": u.get("cache_read_input_tokens", 0),
            "cw1h": cc.get("ephemeral_1h_input_tokens", 0),
            "cw5m": cc.get("ephemeral_5m_input_tokens", 0),
        }


def session_cost():
    """What the most recent session actually spent, and on what.

    Measured 2026-09-19 over a 526-turn session: orientation was 1.1% of cost,
    generated output 17%, and re-reading accumulated context 73%. Reading
    context to decide what to do is therefore NOT worth optimising; session
    length is, because every turn re-reads everything before it and cost grows
    roughly with the square of the turn count.
    """
    files = glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True)
    if not files:
        print("no transcripts found")
        return
    latest = max(files, key=os.path.getmtime)
    turns = list(_turns(latest))
    if not turns:
        print("no usage data in the latest transcript")
        return

    def w(t):
        return sum(t[k] * WEIGHTS[k] for k in WEIGHTS)

    total = sum(w(t) for t in turns)
    first10 = sum(w(t) for t in turns[:10])
    out = sum(t["output"] for t in turns) * WEIGHTS["output"]
    reread = sum(t["cread"] for t in turns) * WEIGHTS["cread"]
    ctx = [t["cread"] + t["cw1h"] + t["cw5m"] for t in turns]

    print(f"\nLATEST SESSION  ({len(turns)} turns, {os.path.basename(latest)[:8]})")
    print(f"  weighted cost          {total:>12,.0f} input-equivalent tokens")
    print(f"  orientation (first 10) {first10:>12,.0f}  {first10 / total * 100:>5.1f}%")
    print(f"  output generated       {out:>12,.0f}  {out / total * 100:>5.1f}%")
    print(f"  re-reading context     {reread:>12,.0f}  {reread / total * 100:>5.1f}%")
    print(f"  context/turn           {ctx[0]:>12,} -> {ctx[-1]:,}")
    if len(turns) > 150:
        print(f"\n  ⚠️ {len(turns)} turns. Cost per turn grows with everything before it;"
              f"\n     ending and handing over beats continuing. ~100 turns is the"
              f"\n     point where splitting stops paying (5 x 105 ≈ 44% of 1 x 526).")


# Files that are read on demand cost nothing per session, but they still rot:
# stale, superseded and contradictory content accumulates where nobody looks.
# The failure mode is too many OPEN THINGS, not too many words, so these are
# counted as items. Past a cap the signal is "this list needs closing, not
# extending" -- but it is advisory. Blocking on it would make silence cheaper
# than recording a finding, which is worse than a long list.
CORPUS = {
    "WORKLOG.md": (r"^## \d{4}-", 10, "shift entries", "delete the oldest; git keeps them"),
    "DECISIONS.md": (r"^## D\d+ ", 15, "decisions",
                     "compress superseded ones to a line; graduate stable ones into the rules"),
    "TECH_DEBT.md": (r"^- \*\*", 25, "open items",
                     "fix, promote to PRD §0's backlog, or delete with reasoning"),
}


def corpus_health():
    """Count open items in the append-only docs. Growth here is invisible to
    the word budgets because these files are read on demand, not every session.
    """
    print("\nCORPUS (read on demand — counted as open items, not words)")
    over = []
    for path, (pattern, cap, noun, fix) in CORPUS.items():
        try:
            raw = open(os.path.join(ROOT, path), encoding="utf-8").read()
        except OSError:
            continue
        n = len(re.findall(pattern, raw, re.M))
        flag = "OVER" if n > cap else "ok"
        bar = "#" * min(int(n / cap * 20), 30)
        print(f"  {n:>6}/{cap:<5} {flag:4} {bar:<22} {path}  ({noun})")
        if n > cap:
            over.append((path, n, cap, fix))
    for path, n, cap, fix in over:
        print(f"\n  {path}: {n} {'items'} exceeds {cap} — {fix}")
    if not over:
        print("  (things are closing, not just accumulating)")
    return over


LANES = ["rounds", "maintenance", "security", "pm", "research", "feature", "close"]
STARVED_AFTER = 5   # consecutive shifts at ~0% before a lane takes priority


def allocation_entries(raw):
    """(heading, {lane: (planned, actual)}) per WORKLOG entry, newest first.

    Fenced blocks are dropped first: the header's template is itself an entry
    with an allocation line, and until 2026-09-29 it was read as the newest
    shift, so no lane it gave time to could ever be flagged starved."""
    raw = re.sub(r"^```.*?^```", "", raw, flags=re.S | re.M)
    entries = []
    for block in raw.split("\n## ")[1:]:
        m = re.search(r"Allocation \(planned→actual %\):(.+)", block)
        if not m:
            continue
        row = {}
        for part in m.group(1).split("·"):
            hit = re.match(r"\s*([a-z]+)\s*(\d+)\s*→\s*(\d+)", part.strip())
            if hit:
                row[hit.group(1)] = (int(hit.group(2)), int(hit.group(3)))
        entries.append((block.split("\n")[0].strip()[:28], row))
    return entries


def worklog_history(commits=40):
    """allocation_entries over WORKLOG.md now and in its recent commits, one
    per heading, newest first. The log's word budget keeps ~4 entries, fewer
    than STARVED_AFTER, so the current file alone could never trip the floor;
    dropped entries are still in git history (shift.yml checks out in full)."""
    texts = []
    try:
        texts.append(open(os.path.join(ROOT, "WORKLOG.md"), encoding="utf-8").read())
    except OSError:
        pass
    try:
        shas = subprocess.run(["git", "log", f"-n{commits}", "--format=%H", "--", "WORKLOG.md"],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
        for sha in shas:
            texts.append(subprocess.run(["git", "show", f"{sha}:WORKLOG.md"], cwd=ROOT,
                                        capture_output=True, text=True).stdout)
    except (OSError, subprocess.CalledProcessError):
        pass                                    # no git: the current file is all there is
    # Keyed on the date and time: a shift may reword its headline or even its
    # time, so only entries older than the current file's oldest were dropped.
    seen, oldest = {}, None
    for i, text in enumerate(texts):            # current file first, so its edits win
        for label, row in allocation_entries(text):
            key = re.match(r"[\d-]+(?: \(\d\d:\d\d\))?", label).group(0)
            if i == 0 or oldest is None or key < oldest:
                seen.setdefault(key, (label, row))
        if i == 0 and seen:
            oldest = min(seen)
    return [seen[k] for k in sorted(seen, reverse=True)]


def allocation_history():
    """Planned vs actual per lane, from WORKLOG.md's allocation lines.

    Two questions this answers that prose cannot: is a lane being starved, and
    are slices being *finished* or merely *filled*? Consistently landing under
    plan is not a problem — slices are ceilings — but landing under plan on
    every lane, every shift, means we are not finding valuable work, which is a
    process finding rather than a good shift.
    """
    entries = worklog_history()
    if not entries:
        print("\nno allocation lines in WORKLOG.md yet")
        return

    print(f"\nALLOCATION, last {len(entries)} shift(s)   (planned→actual %)")
    header = "  " + "shift".ljust(30) + "".join(l[:7].ljust(9) for l in LANES)
    print(header)
    for label, row in entries:
        cells = "".join((f"{row[l][0]}→{row[l][1]}" if l in row else "-").ljust(9)
                        for l in LANES)
        print(f"  {label.ljust(30)}{cells}")

    print()
    for lane in LANES:
        zeros = 0
        for _, row in entries:                       # newest first
            if row.get(lane, (0, 0))[1] > 0:
                break
            zeros += 1
        if zeros >= STARVED_AFTER:
            print(f"  ⚠️ {lane}: {zeros} consecutive shifts at 0% — "
                  f"takes priority next shift if it has queued work")
    under = [l for l in LANES
             if all(row.get(l, (0, 0))[1] < row.get(l, (1, 0))[0] for _, row in entries)]
    if len(entries) >= 3 and len(under) >= len(LANES) - 1:
        print("  ⚠️ every lane landed under plan on every recorded shift — "
              "we are not finding valuable work. Process finding, not a good shift.")


# Process-health thresholds. Guesses, like the caps — see DECISIONS.md D4.
WASTE_SHIFTS = 3      # consecutive shifts using far less than their time
WASTE_RATIO = 0.6     # ...where minutes actually run are below this share
SHIFT_MINUTES = 25    # the hand-over deadline shift.yml gives a shift (killed at 30)
LEDGER = os.path.join(ROOT, ".github", "shift-usage.csv")


def shift_minutes(path=None):
    """Minutes each completed shift ran, most recent first -- from the usage
    ledger the workflow writes, which a shift cannot inflate. The old check
    compared planned with reported *percentages*, and a shift reports
    percentages of whatever time it used, so an 8-minute shift read as
    "planned 100%, used 100%" and two short shifts went unflagged."""
    try:
        rows = list(csv.DictReader(open(path or LEDGER)))
    except OSError:
        return []
    out = []
    for r in reversed(rows):
        if r.get("is_error") == "1":
            continue            # a failed run is a different problem
        try:
            out.append(float(r["duration_min"]))
        except (KeyError, ValueError):
            continue
    return out
STARVED_SHIFTS = 5    # consecutive shifts a lane sat at 0%


def _allocation_rows():
    return [row for _, row in worklog_history()
            if any(p for p, _ in row.values())]     # skip unplanned/outlier shifts


def health(raise_issues=False):
    """Detect process dysfunction and escalate it.

    The escalation path was built for "I need permission", not for "something
    is systematically wrong" — so the workflow could measure its own failure
    and have no route to report it. These checks close that: a threshold trip
    queues a GitHub issue, which emails the owner.
    """
    rows = _allocation_rows()
    problems = []

    minutes = shift_minutes()[:WASTE_SHIFTS]
    if len(minutes) == WASTE_SHIFTS:
        used = sum(minutes) / (WASTE_SHIFTS * SHIFT_MINUTES)
        if used < WASTE_RATIO:
            sys.path.insert(0, os.path.join(ROOT, "scripts"))
            import backlog_status
            ready = len(backlog_status.ready(open(backlog_status.PRD).read()))
            problems.append((
                "process-capacity-underused",
                "Shifts are ending with most of their time unspent",
                f"The last {WASTE_SHIFTS} shifts ran "
                f"{', '.join(f'{m:.0f}' for m in minutes)} of their {SHIFT_MINUTES} "
                f"minutes ({used:.0%}, threshold {WASTE_RATIO:.0%}), from the usage "
                f"ledger. Ready work in the tracker now: {ready} "
                f"(floor {backlog_status.FLOOR}).\n\n"
                "Ending early is right only when nothing is ready and generating "
                "more found nothing above the bar. Below the floor, replenishing "
                "was the project-management lane's first job and was skipped; at "
                "or above it, shifts are stopping with work available.",
                "Read why each of the last three shifts stopped (WORKLOG) and fix "
                "that reason, not the symptom."))

    for lane in LANES:
        zeros = 0
        for r in rows:
            if r.get(lane, (0, 0))[1] > 0:
                break
            zeros += 1
        if zeros >= STARVED_SHIFTS:
            problems.append((
                f"process-lane-starved-{lane}",
                f"The {lane} lane has had no time for {zeros} shifts",
                f"`{lane}` has been allocated ~0% for {zeros} consecutive "
                f"shifts.\n\nThe starvation floor should have promoted it. "
                "Either it is not firing, or the lane genuinely has no work — "
                "and if it has none for this long, it may not be a lane.",
                "Check whether the lane has queued work. If it never does, "
                "propose removing it rather than leaving a slice that is "
                "always zero."))

    if not problems:
        print("\nPROCESS HEALTH: ok"
              + ("" if rows else "  (no planned shifts recorded yet)"))
        return []

    print("\nPROCESS HEALTH: %d problem(s)" % len(problems))
    for key, title, body, rec in problems:
        print(f"  - {title}")
        if raise_issues:
            r = subprocess.run(
                [sys.executable, os.path.join(ROOT, "scripts", "escalate.py"),
                 "--title", title, "--key", key, "--recommend", rec],
                input=body, text=True, capture_output=True)
            print("    " + (r.stdout.strip() or r.stderr.strip()))
        else:
            print(f"    (run with --health to queue an issue; key={key})")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if anything is over budget")
    ap.add_argument("--session", action="store_true",
                    help="also report what the latest session actually spent")
    ap.add_argument("--allocation", action="store_true",
                    help="planned vs actual per lane, from WORKLOG.md")
    ap.add_argument("--health", action="store_true",
                    help="detect process dysfunction and queue escalations for it")
    args = ap.parse_args()

    always = measure(ALWAYS)
    orient = measure(ORIENT)
    blocking = report(always, "ALWAYS LOADED (every session, whatever the task)")
    advisory = report(orient, "READ AT STARTUP (every shift)")
    corpus_over = corpus_health()

    total = sum(n for _, n, _ in always + orient if n)
    cap = sum(b for _, _, b in always + orient)
    print(f"\n  TOTAL {total} words against a {cap} budget "
          f"({total / cap * 100:.0f}%)")

    if args.session:
        session_cost()
    if args.allocation:
        allocation_history()
    if args.health:
        health(raise_issues=True)

    advisory += [(p, n, c) for p, n, c, _ in corpus_over]

    if blocking or advisory:
        if blocking:
            print("\nOver budget — BLOCKING (always-loaded context):")
            for name, n, budget in blocking:
                print(f"  - {name}: {n} words, {n - budget} over")
        if advisory:
            print("\nOver budget — advisory, does not fail the build:")
            for name, n, budget in advisory:
                print(f"  - {name}: {n}, {n - budget} over")
        print("\nOptions, in rough order of preference:")
        print("  1. Delete it. 'Would removing this cause a mistake?' If no, cut it.")
        print("  2. Move detail to where it is read on demand — a skill, or PRD §6.")
        print("  3. Convert an advisory rule into a hook or a test, which is")
        print("     enforcement rather than words (CLAUDE.md is advisory).")
        print("  4. Raise the budget — legitimate when the project actually grew,")
        print("     which it has twice. Say why in the commit, as those did.")
    else:
        print("\nAll within budget.")
    return 1 if (blocking and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
