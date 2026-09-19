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
    venv/bin/python scripts/context_budget.py --check  # exit 1 if over budget

Two tiers, because they cost differently:

  ALWAYS   loaded into every single session, whatever the task. The expensive
           tier: every word here is paid for even when irrelevant.
  ORIENT   read during /pickup or /shift startup. Cheaper, but still per-shift.

Reference material that is read only when a task needs it is NOT counted —
that is what skills and PRD §6 are for, and moving detail there is usually the
right fix when a budget is breached.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Budgets are deliberately tight. Raising one is a decision to spend more of
# every future session on the same words, so it needs a reason beyond "it grew".
ALWAYS = {"CLAUDE.md": 1200}
ORIENT = {
    "README.md#Picking this up": 400,
    "PRD.md#0.": 1800,
    "WORKLOG.md": 900,
    ".claude/skills/shift/SKILL.md": 1800,
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
WEIGHTS = {"input": 1.0, "cw1h": 2.0, "cw5m": 1.25, "cread": 0.1, "output": 5.0}


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


LANES = ["rounds", "maintenance", "pm", "research", "feature", "close"]
STARVED_AFTER = 5   # consecutive shifts at ~0% before a lane takes priority


def allocation_history():
    """Planned vs actual per lane, from WORKLOG.md's allocation lines.

    Two questions this answers that prose cannot: is a lane being starved, and
    are slices being *finished* or merely *filled*? Consistently landing under
    plan is not a problem — slices are ceilings — but landing under plan on
    every lane, every shift, means we are not finding valuable work, which is a
    process finding rather than a good shift.
    """
    try:
        raw = open(os.path.join(ROOT, "WORKLOG.md"), encoding="utf-8").read()
    except OSError:
        print("no WORKLOG.md")
        return
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if anything is over budget")
    ap.add_argument("--session", action="store_true",
                    help="also report what the latest session actually spent")
    ap.add_argument("--allocation", action="store_true",
                    help="planned vs actual per lane, from WORKLOG.md")
    args = ap.parse_args()

    always = measure(ALWAYS)
    orient = measure(ORIENT)
    over = report(always, "ALWAYS LOADED (every session, whatever the task)")
    over += report(orient, "READ AT STARTUP (every shift)")

    total = sum(n for _, n, _ in always + orient if n)
    cap = sum(b for _, _, b in always + orient)
    print(f"\n  TOTAL {total} words against a {cap} budget "
          f"({total / cap * 100:.0f}%)")

    if args.session:
        session_cost()
    if args.allocation:
        allocation_history()

    if over:
        print("\nOver budget:")
        for name, n, budget in over:
            print(f"  - {name}: {n} words, {n - budget} over")
        print("\nThe fix is almost never a bigger budget. In order of preference:")
        print("  1. Delete it. 'Would removing this cause a mistake?' If no, cut it.")
        print("  2. Move detail to where it is read on demand — a skill, or PRD §6.")
        print("  3. Convert an advisory rule into a hook or a test, which is")
        print("     enforcement rather than words (CLAUDE.md is advisory).")
        print("  4. Only then, raise the budget — and say why in the commit.")
    else:
        print("\nAll within budget.")
    return 1 if (over and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
