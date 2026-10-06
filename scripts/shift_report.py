#!/usr/bin/env python3
"""Build the per-shift summary the owner reads by email.

The owner does not watch the repo work; they need to know what moved without
opening it. So every shift posts a short report as a comment on one long-lived
GitHub issue -- one email per shift, one thread, and no clutter in the issue
tracker, which is reserved for decisions that need them.

Since 2026-10-05 a shift works one ranked queue across the company's functions
(ORG.md), not a slice per lane, so the report shows where the time went by
function and keeps the sections in the order the shift wrote them.

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

# The functions in ORG.md, in its order, by the short name a WORKLOG entry uses.
FUNCTIONS = {
    "strategy": "Strategy", "gm": "General management", "market": "Market intelligence",
    "audience": "Audience", "distribution": "Distribution", "monetization": "Monetization",
    "product": "Product", "editorial": "Editorial", "engineering": "Engineering",
    "reliability": "Reliability", "data": "Data & insights",
    "finance": "Finance", "legal": "Legal & policy", "security": "Security",
}
# The old lanes, so an entry written before 2026-10-05 still renders.
OLD_LANES = {
    "rounds": "Routine checks", "maintenance": "Maintenance", "pm": "Project management",
    "research": "Research", "feature": "Feature work", "close": "Wrap-up",
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


def worked(text):
    """{function: % of the shift} from the entry's `Worked` line.

    Falls back to the old `Allocation (planned→actual %)` line, keeping the
    actual share, so entries from before the change still report."""
    m = re.search(r"Worked \(% of the shift\):(.+)", text or "")
    if m:
        out = {}
        for part in m.group(1).split("·"):
            hit = re.match(r"\s*([a-z]+)\s*(\d+)", part.strip())
            if hit:
                out[hit.group(1)] = int(hit.group(2))
        return out
    m = re.search(r"Allocation \(planned→actual %\):(.+)", text or "")
    out = {}
    for part in (m.group(1).split("·") if m else []):
        hit = re.match(r"\s*([a-z]+)\s*(\d+)\s*→\s*(\d+)", part.strip())
        if hit:
            out[hit.group(1)] = int(hit.group(3))
    return out


def _name(key):
    return FUNCTIONS.get(key) or OLD_LANES.get(key) or key.replace("_", " ").capitalize()


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

    # 2. Where the time went, by function.
    share = worked(body)
    if share:
        out += ["| Function | Share of the shift |", "|---|---|"]
        order = [k for k in FUNCTIONS if k in share] + [k for k in share if k not in FUNCTIONS]
        out += [f"| {_name(k)} | {share[k]}% |" for k in order if share[k]]
        total = sum(share.values())
        flag = "" if total == 100 else "  ⚠️ should total 100%"
        out += [f"| **Total** | **{total}%** |{flag}", ""]

    # 3. The sections in the order the shift wrote them: "Toward revenue" first
    #    by the template, then what was done, blocked, next. A function the
    #    shift did not touch gets no heading -- with fourteen of them, a
    #    "nothing this shift" line each would bury what did happen.
    blocks = sections(body)
    if blocks:
        for heading, content in blocks:
            lines = [l for l in content.splitlines() if l.strip()]
            if not lines:
                continue
            if not any(l.lstrip().startswith(("-", "*")) for l in lines):
                lines = [f"- {' '.join(' '.join(lines).split())}"]
            out += [f"### {heading}", ""] + lines + [""]
    else:
        # A shift that ignored the template still gets reported, rather than
        # the owner silently receiving less than they asked for.
        narrative = re.sub(r"\s*(Allocation \(planned→actual %\)|Worked \(% of the shift\)):.+", "", body)
        narrative = re.sub(r"\*\*Summary:\*\*.+?(?=\n\n|$)", "", narrative, flags=re.S)
        out += ["### Details", "", narrative.strip(),
                "", "*(This shift did not follow the report template.)*", ""]

    cost = last_cost(ledger)
    if cost:
        # Minutes against the shift's budget, and the ready work it left: the
        # two numbers that show a shift stopping with work available.
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import backlog_status
        try:
            ready = f"{len(backlog_status.ready_all())}"
        except OSError:
            ready = "?"
        try:
            import datetime
            import cadence
            today = datetime.datetime.now(datetime.timezone.utc).date()
            due = [r for r, _ in cadence.due(cadence.last_held(open(cadence.PLAN).read()),
                                             today, cadence.newest_snapshot())
                   if r in cadence.ORDER]
        except Exception:
            due = []
        import context_budget
        out.append(f"*{cost.get('duration_min','?')} of {context_budget.SHIFT_MINUTES} min · "
                   f"{cost.get('turns','?')} steps · "
                   f"{cost.get('quota_units','?')} quota units · "
                   f"ready work left: {ready} (floor {backlog_status.FLOOR})"
                   + (f" · review due: {', '.join(due)}" if due else "") + "*")
    if run_url:
        out.append(f"*[Full log]({run_url})*")
    return "\n".join(out)


if __name__ == "__main__":
    print(build(*sys.argv[1:5]))
