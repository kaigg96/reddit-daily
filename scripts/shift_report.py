#!/usr/bin/env python3
"""Build the per-shift summary the owner reads by email.

The owner does not watch the repo work; they need to know what moved without
opening it. So every shift posts a short report, broken down by workstream, as
a comment on one long-lived GitHub issue -- one email per shift, one thread,
and no clutter in the issue tracker, which is reserved for decisions that need
them.

Source of truth is the shift's own WORKLOG.md entry, so the report cannot
drift from the handover: if a shift did not write an entry it has nothing to
report, which the workflow already treats as a failure.

    shift_report.py <worklog> <ledger> <since_sha> [run_url]
"""
import csv
import os
import re
import subprocess
import sys

LANES = ["rounds", "maintenance", "pm", "research", "feature", "close"]
LANE_NAMES = {
    "rounds": "Routine checks", "maintenance": "Maintenance",
    "pm": "Project management", "research": "Research",
    "feature": "Feature work", "close": "Wrap-up",
}


def latest_entry(worklog):
    """The newest '## <date>' block — what this shift wrote."""
    try:
        raw = open(worklog, encoding="utf-8").read()
    except OSError:
        return None, None
    blocks = raw.split("\n## ")
    if len(blocks) < 2:
        return None, None
    block = blocks[1]
    return block.split("\n")[0].strip(), "\n".join(block.split("\n")[1:]).strip()


def allocation(text):
    m = re.search(r"Allocation \(planned→actual %\):(.+)", text or "")
    if not m:
        return {}
    out = {}
    for part in m.group(1).split("·"):
        hit = re.match(r"\s*([a-z]+)\s*(\d+)\s*→\s*(\d+)", part.strip())
        if hit:
            out[hit.group(1)] = (int(hit.group(2)), int(hit.group(3)))
    return out


def changes(since_sha):
    """What actually landed — the claim checked against the diff."""
    try:
        files = subprocess.run(["git", "diff", "--stat", f"{since_sha}..HEAD"],
                               capture_output=True, text=True).stdout.strip()
        commits = subprocess.run(
            ["git", "log", f"{since_sha}..HEAD", "--format=- %s", "--no-merges"],
            capture_output=True, text=True).stdout.strip()
        return commits, files.split("\n")[-1] if files else "no file changes"
    except Exception:
        return "", "could not read the diff"


def last_cost(ledger):
    try:
        rows = list(csv.DictReader(open(ledger)))
        return rows[-1] if rows else None
    except Exception:
        return None


def build(worklog, ledger, since_sha, run_url=""):
    date, body = latest_entry(worklog)
    if not date:
        return "No WORKLOG entry — nothing to report."

    alloc = allocation(body)
    commits, stat = changes(since_sha)
    cost = last_cost(ledger)

    out = [f"## Shift — {date}", ""]

    if alloc:
        out += ["**Where the time went**", "",
                "| Workstream | Planned | Actual |", "|---|---|---|"]
        for lane in LANES:
            if lane in alloc:
                p, a = alloc[lane]
                note = " — nothing worth doing" if a == 0 else ""
                out.append(f"| {LANE_NAMES[lane]} | {p}% | {a}%{note} |")
        out.append("")

    # Strip the allocation line; it is already rendered as the table above.
    narrative = re.sub(r"\s*Allocation \(planned→actual %\):.+", "", body).strip()
    if narrative:
        out += ["**What happened**", "", narrative, ""]

    if commits:
        out += ["**Shipped**", "", commits, "", f"`{stat}`", ""]
    else:
        out += ["**Shipped** — nothing landed this shift.", ""]

    if cost:
        out.append(f"*{cost.get('model','?')} at {cost.get('effort','?')} · "
                   f"{cost.get('turns','?')} turns · {cost.get('duration_min','?')} min · "
                   f"${cost.get('cost_usd','?')}*")
    if run_url:
        out.append(f"*[Full run]({run_url})*")
    return "\n".join(out)


if __name__ == "__main__":
    print(build(*sys.argv[1:5]))
