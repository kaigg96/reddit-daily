#!/usr/bin/env python3
"""How much work in the trackers can actually be done right now.

A shift ended when its lanes looked empty, and a lane never looked empty while
it held blocked items. On 2026-09-24 and 09-25 two shifts ended with most of
their time unspent while the queue was full of changes waiting on a sample
video. Supply is work whose next step can be taken now; this counts it.

    venv/bin/python scripts/backlog_status.py           # ready work vs the floor
    venv/bin/python scripts/backlog_status.py --count   # just the number

Two trackers feed one queue: PRD §0 (the channel product) and PLAN.md §3 (every
other function of the company, ORG.md). Every row of a table with a Status
column, in either, carries one of:
    ready             the next step can be taken now, and is worth taking
    blocked: <what>   the next step waits on something outside this shift
    baking            live; waiting for its decision rule's data
    parked            deferred behind a stated gate
    done              shipped, answered, or dropped
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRD = os.path.join(ROOT, "PRD.md")
PLAN = os.path.join(ROOT, "PLAN.md")
FLOOR = 3
STATUSES = ("ready", "blocked", "baking", "parked", "done")


def section0(text):
    m = re.search(r"^## 0\..*?(?=^## 1\.)", text, re.S | re.M)
    return m.group(0) if m else ""


def queue_section(text):
    """PLAN.md §3, the company's work queue."""
    m = re.search(r"^## 3\..*?(?=^## 4\.|\Z)", text, re.S | re.M)
    return m.group(0) if m else ""


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def items(text, section=section0):
    """(status, detail, name) for each row of each table with a Status column."""
    out, header = [], None
    for line in section(text).splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = _cells(line)
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if not line.replace("|", "").replace("-", "").replace(":", "").strip():
            continue                                          # the |---| row
        if "status" not in header:
            continue
        raw = cells[header.index("status")].strip("`* ")
        name_at = next((i for i, h in enumerate(header) if h in ("item", "question")), None)
        name = re.sub(r"[*~`]", "", cells[name_at]) if name_at is not None else ""
        out.append((raw.split(":")[0].strip().lower(), raw, name.split(" — ")[0][:90]))
    return out


def malformed(text, section=section0):
    """Lines that start a table but are not followed by its |---| row. A row
    separated from its table by a blank line reads as a one-line table of its
    own: invisible to the count, and rendered as a stray line of pipes. That
    happened to a §0 row on 2026-09-25."""
    lines, bad = section(text).splitlines(), []
    for i, line in enumerate(lines):
        starts = line.startswith("|") and (i == 0 or not lines[i - 1].startswith("|"))
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if starts and not (nxt.startswith("|") and set(nxt.replace("|", "").strip()) <= set("-: ")):
            bad.append(line[:80])
    return bad


def ready(text, section=section0):
    return [name for status, _, name in items(text, section) if status == "ready"]


def _read(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def sources():
    """(label, text, section) for each tracker that feeds the queue."""
    return [("product", _read(PRD), section0), ("company", _read(PLAN), queue_section)]


def ready_all():
    """Ready work across both trackers -- the one queue a shift ranks."""
    return [f"[{label}] {name}" for label, text, section in sources()
            for name in ready(text, section)]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    found = ready_all()
    if "--count" in argv:
        print(len(found))
        return 0
    counts = {s: 0 for s in STATUSES}
    for label, text, section in sources():
        for status, _, _ in items(text, section):
            counts[status] = counts.get(status, 0) + 1
        for line in malformed(text, section):
            print(f"WARNING: a {label} row cut off from its table is not counted: {line}")
    print("  ".join(f"{s}: {n}" for s, n in counts.items()))
    print(f"\nREADY {len(found)} (floor {FLOOR})")
    for name in found:
        print(f"  - {name}")
    if len(found) < FLOOR:
        print("\nBelow the floor: generating and ranking more ready work comes "
              "first (/backlog §1-2). Research questions tested against existing "
              "data are always available, and the risk register (PLAN.md §4) "
              "names what no function is yet answering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
