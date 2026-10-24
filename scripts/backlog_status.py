#!/usr/bin/env python3
"""How much work in the trackers can actually be done right now.

A shift ended when its lanes looked empty, and a lane never looked empty while
it held blocked items. On 2026-09-24 and 09-25 two shifts ended with most of
their time unspent while the queue was full of changes waiting on a sample
video. Supply is work whose next step can be taken now; this counts it.

    venv/bin/python scripts/backlog_status.py           # ready work vs the floor
    venv/bin/python scripts/backlog_status.py --count   # just the number
    venv/bin/python scripts/backlog_status.py --dropped # what recent shifts dropped

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
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRD = os.path.join(ROOT, "PRD.md")
PLAN = os.path.join(ROOT, "PLAN.md")
WORKLOG = os.path.join(ROOT, "WORKLOG.md")
# 3 until 2026-10-05, when shifts grew from 25 to 60 minutes (D11).
FLOOR = 5
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
    if "--dropped" in argv:
        for heading, bullet in recently_dropped():
            print(f"{heading[:70]}\n  {bullet}\n")   # cut, a drop is re-proposed
        print("DONE in the last ten shifts (each bullet's opening), so "
              "finished work is not proposed again:\n")
        for heading, bullets in recently_dropped(extract=done_in):
            print(heading[:110])
            print("".join(f"  - {b}\n" for b in bullets.split(" | ")))
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
              "names what no function is yet answering. What the last ten "
              "shifts already dropped, and why, and what they did: --dropped.")
    for line in short_shifts():
        print(line)
    return 0


_ENTRY = re.compile(r"^## (\d{4}-\d{2}-\d{2}.*)$")
# A short bold label ("**Dropped:**", "**Ranked and dropped**"), anywhere in a
# bullet: since 10-20 a shift lists its drops inside its General management
# bullet, and a match only at the opening showed the generator nothing newer
# (found 10-24). Short, so a bold headline that says "dropped" is not one.
_DROPPED = re.compile(r"(?<!\S)\*\*(?:\w+\s+){0,3}dropped(?:\s+\w+){0,2}:?\*\*", re.I)


def _dropped_part(bullet):
    """The dropped list a bullet holds, from its label on, or None."""
    m = _DROPPED.search(bullet)
    return bullet[m.start():].replace("**", "").strip() if m else None


def dropped_in(text):
    """(entry heading, [dropped bullets]) for each WORKLOG entry that has any."""
    out, heading, bullets, bullet = [], None, [], None
    for line in text.splitlines() + ["## 0000-00-00 end"]:
        if bullet is not None and line.startswith("  ") and line.strip():
            bullet += " " + line.strip()        # the bullet wrapped onto more lines
            continue
        part = bullet and _dropped_part(bullet)
        if part:
            bullets.append(part)
        bullet = None                           # any other line ends it
        m = _ENTRY.match(line)
        if m:
            if heading and bullets:
                out.append((heading, bullets))
            heading, bullets = m.group(1).strip(), []
        elif heading and line.startswith("- "):
            bullet = line
    return out


_SECTION = re.compile(r"^### (.+?)\s*$")
_DONE_SECTIONS = {"Toward revenue", "Done"}


def done_in(text):
    """(entry heading, [first sentence of each bullet]) under each entry's
    "Toward revenue" and "Done", dropped lists left out. The 10-21 audit: a
    generator re-proposed bet 2's start date, answered on 10-17 and 10-19, and
    a ranker put it first, because only drops were listed."""
    out, heading, bullets, section, inside, fenced = [], None, [], None, False, False
    for line in text.splitlines() + ["## 0000-00-00 end"]:
        if line.lstrip().startswith("```"):
            fenced = not fenced                 # the header's template is no shift
            continue
        if fenced:
            continue
        m, sec = _ENTRY.match(line), _SECTION.match(line)
        if m:
            if heading and bullets:
                out.append((heading, bullets))
            heading, bullets, section, inside = m.group(1).strip(), [], None, False
        elif sec:
            section, inside = sec.group(1), False
        elif (heading and section in _DONE_SECTIONS and line.startswith("- ")
              and not _DROPPED.match(line, 2)):          # one that opens on its label
            bullets.append(line[2:].replace("**", "").strip())
            inside = True
        elif inside and line.startswith("  ") and line.strip():
            bullets[-1] += " " + line.strip()
        else:
            inside = False
    return [(h, [_clip(b, 240) for b in bs]) for h, bs in out]


def _clip(text, width):
    """The first `width` characters, cut at a word. A bullet's first sentence
    is often only its headline ("What a late label costs is now written
    down."), and the fact is in the next one."""
    return text if len(text) <= width else text[:width].rsplit(" ", 1)[0] + " …"


def _heading_parts(heading):
    """(date, time or "", headline) of an entry heading."""
    m = re.match(r"(\S+)\s*(?:\((\d\d:\d\d)\))?\s*(?:—\s*)?(.*)", heading)
    return m.group(1), m.group(2) or "", m.group(3).strip()


def _worklog_versions(commits):
    """WORKLOG.md as it stands, then as each of its last `commits` commits left
    it, newest first. Nothing when git is unavailable."""
    yield _read(WORKLOG)
    try:
        shas = subprocess.run(
            ["git", "log", f"-{commits}", "--format=%H", "--", "WORKLOG.md"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return
    for sha in shas:
        r = subprocess.run(["git", "show", f"{sha}:WORKLOG.md"], cwd=ROOT,
                           capture_output=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            yield r.stdout


def recently_dropped(limit=10, commits=200, versions=None, extract=None):
    """What the last `limit` shifts considered and dropped, newest first.

    WORKLOG.md's word budget keeps about two entries, so a shift could not see
    what the shift before last had dropped, and re-proposed it: the 10-17
    audit found four candidates dropped twice (retention curves, likes, the
    length check's fail-soft, a subscriber test). Git keeps every entry; each
    is read from the newest version that has it. A shift that re-stamps its
    heading (08:24, then 08:28) or rewords its headline is still one entry:
    a heading repeating an earlier one's date and time, or date and headline,
    is the same shift. `extract=done_in` lists what they did instead."""
    out, keys = [], set()
    for text in (versions if versions is not None else _worklog_versions(commits)):
        for heading, bullets in (extract or dropped_in)(text):
            date, time, headline = _heading_parts(heading)
            mine = {(date, "h", headline)} | ({(date, "t", time)} if time else set())
            seen = bool(mine & keys)
            keys |= mine      # even when skipped, so a chain of edits links up
            if not seen:
                out.append((heading, " | ".join(bullets)))
    return sorted(out, key=lambda e: _heading_parts(e[0])[:2], reverse=True)[:limit]


def waiting_on_owner():
    """Blocked rows whose block names the owner, across both trackers."""
    return [f"[{label}] {name[:50]}: {raw.split(':', 1)[-1].strip()[:80]}"
            for label, text, section in sources()
            for status, raw, name in items(text, section)
            if status == "blocked" and "owner" in raw.lower()]


def short_shifts():
    """What to print when recent shifts ran short. The cause, found on
    2026-10-11 for #67: the queue is empty because its rows wait on the owner,
    and an ask that needs the owner's hands or a session waits for days, while
    one they answer with a label closes within a day (12 of 12, audit
    2026-10-09; bet 1 was approved the day it was split out of the planning
    session). Every row cleared of hands-work is one less reason to stop."""
    if __package__:
        from . import context_budget
    else:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import context_budget
    short = context_budget.capacity_shortfall()
    if not short:
        return []
    minutes, used = short
    owner = waiting_on_owner()
    out = [f"\nSHIFTS ARE ENDING EARLY: the last {len(minutes)} ran "
           f"{', '.join(f'{m:.0f}' for m in minutes)} of their "
           f"{context_budget.SHIFT_MINUTES} minutes ({used:.0%}). This is the "
           "shift's to fix, never the owner's (#67)."]
    if owner:
        out.append(f"{len(owner)} rows wait on the owner. Asks they answer with "
                   "a label close within a day; asks needing their hands or a "
                   "session wait. Before generating, do every part of these a "
                   "shift can, so what is left for the owner is one label:")
        out += [f"  - {o}" for o in owner]
    return out


if __name__ == "__main__":
    sys.exit(main())
