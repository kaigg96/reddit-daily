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


def _strip_fences(raw):
    """Drop fenced code blocks.

    The file's header shows the entry template inside a fence, and that example
    contains a '## <date>' line. Without this, the report happily renders the
    template as if it were the latest shift.
    """
    out, fenced = [], False
    for line in raw.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return "\n".join(out)


def latest_entry(worklog):
    """The newest '## <date>' block — what this shift wrote."""
    try:
        raw = _strip_fences(open(worklog, encoding="utf-8").read())
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


def sections(text):
    """The `### Workstream` blocks a shift wrote, in the order it wrote them."""
    out, current, buf = [], None, []
    for line in (text or "").splitlines():
        if line.startswith("### "):
            if current:
                out.append((current, "\n".join(buf).strip()))
            current, buf = line[4:].strip(), []
        elif current is not None:
            buf.append(line)
    if current:
        out.append((current, "\n".join(buf).strip()))
    return out


def summary_line(text):
    m = re.search(r"\*\*Summary:\*\*\s*(.+?)(?=\n\n|\n###|$)", text or "", re.S)
    return " ".join(m.group(1).split()) if m else ""


def build(worklog, ledger, since_sha, run_url=""):
    date, body = latest_entry(worklog)
    if not date:
        return "No handover was written, so there is nothing to report."

    out = [f"## {date}", ""]

    # 1. The overview, first and short — this is what gets read on a phone.
    summary = summary_line(body)
    if summary:
        out += [summary, ""]

    # 2. Where the time went.
    alloc = allocation(body)
    if alloc:
        out += ["| Workstream | Planned | Actual |", "|---|---|---|"]
        for lane in LANES:
            if lane in alloc:
                planned, actual = alloc[lane]
                out.append(f"| {LANE_NAMES[lane]} | {planned}% | {actual}% |")
        out.append("")

    # 3. One heading per workstream, bullets underneath. Same shape every time,
    #    so it can be skimmed without reading.
    blocks = sections(body)
    if blocks:
        for heading, content in blocks:
            out += [f"### {heading}", ""]
            lines = [l for l in content.splitlines() if l.strip()]
            if not any(l.lstrip().startswith(("-", "*")) for l in lines):
                lines = [f"- {' '.join(' '.join(lines).split())}"] if lines else []
            out += lines + [""]
    else:
        # A shift that ignored the template still gets reported, rather than
        # the owner silently receiving less than they asked for.
        narrative = re.sub(r"\s*Allocation \(planned→actual %\):.+", "", body)
        narrative = re.sub(r"\*\*Summary:\*\*.+?(?=\n\n|$)", "", narrative, flags=re.S)
        out += ["### Details", "", narrative.strip(),
                "", "*(This shift did not follow the report template.)*", ""]

    cost = last_cost(ledger)
    if cost:
        out.append(f"*{cost.get('turns','?')} steps · "
                   f"{cost.get('duration_min','?')} min · "
                   f"{cost.get('quota_units','?')} quota units*")
    if run_url:
        out.append(f"*[Full log]({run_url})*")
    return "\n".join(out)


if __name__ == "__main__":
    print(build(*sys.argv[1:5]))
