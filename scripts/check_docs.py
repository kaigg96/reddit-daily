#!/usr/bin/env python3
"""Check the tracker's checkable claims against ground truth.

"Is the tracker true?" was a judgement call, and judgement kept losing: the
live format was described as pending review for a day after it merged, the
publish times were wrong for weeks, and a shift lost its feature time to a
blocker that had been cleared ten days earlier. Stale claims mislead worse
than missing ones, because they are read with confidence.

Not everything is checkable. This does the part that is, so a shift spends its
judgement on the part that isn't.

    venv/bin/python scripts/check_docs.py          # report
    venv/bin/python scripts/check_docs.py --check  # exit 1 on a stale claim
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(path):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def check_live_format():
    """The version PRD claims is live, against the version the code ships."""
    prd = _read("PRD.md")
    code = re.search(r'FORMAT_VERSION\s*=\s*"([^"]+)"', _read("src/config.py"))
    claim = re.search(r"\*\*Live format:\*\*\s*`([^`]+)`", prd)
    if not code or not claim:
        return None, "could not read one of the two values"
    if code.group(1) != claim.group(1):
        return False, (f"PRD says live format is {claim.group(1)}, "
                       f"but src/config.py ships {code.group(1)}")
    return True, f"live format {code.group(1)} agrees with the code"


def check_merged_branches():
    """Docs describing a branch as pending when it has already merged."""
    prd = _read("PRD.md")
    stale = []
    for branch in set(re.findall(r"`((?:feature|integration|fix|chore|analysis)/[\w.\-/]+)`", prd)):
        # Merged into main, or gone entirely -> describing it as pending is stale.
        merged = _git("branch", "--merged", "main", "--list", branch)
        exists = _git("rev-parse", "--verify", "--quiet", branch)
        if merged or not exists:
            near = " ".join(
                l for l in prd.splitlines() if branch in l)[:160].lower()
            if any(w in near for w in ("pending", "awaiting", "do not start",
                                       "not yet", "blocked on")):
                stale.append(branch)
    if stale:
        return False, ("described as pending but already merged or gone: "
                       + ", ".join(sorted(stale)))
    return True, "no branch is described as pending after merging"


def check_upload_counts():
    """A cohort size quoted as current, against the log's actual size."""
    log = _read("upload_log.csv")
    actual = max(len(log.strip().splitlines()) - 1, 0)
    prd = _read("PRD.md")
    claims = [int(n) for n in re.findall(r"logged uploads?\D{0,12}n=(\d+)", prd)]
    stale = [n for n in claims if actual - n > 25]
    if stale:
        return False, (f"quotes a current cohort of {stale} while the log has "
                       f"{actual} — re-read or mark those as historical")
    return True, f"no current-cohort claim lags the log's {actual} rows"


OPEN_WORDS = ("awaiting", "waiting on", "open", "pending")
NEAR = 80   # characters either side of a citation


def describes_as_open(text, n):
    """Whether a mention of #n sits near a word calling it open. A whole line
    was too wide: a PRD §0 row is one long line, so a row citing closed #18
    and titled "Open on the hook" read as describing #18 as open (2026-09-29)."""
    for m in re.finditer(rf"#{n}\b", text):
        near = text[max(0, m.start() - NEAR):m.end() + NEAR].lower()
        if any(w in near for w in OPEN_WORDS):
            return True
    return False


def check_open_escalations():
    """A doc pointing at an issue that has since been closed."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None, "no GitHub token — skipped"
    import json
    import urllib.request
    repo = os.environ.get("GITHUB_REPOSITORY", "kaigg96/reddit-daily")
    text = _read("PRD.md") + _read("WORKLOG.md") + _read("TECH_DEBT.md")
    refs = {int(n) for n in re.findall(r"(?:issue|#)\s?#?(\d{1,4})\b", text)}
    refs = {n for n in refs if n < 500}
    stale = []
    for n in sorted(refs):
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/issues/{n}",
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json"})
        try:
            with urllib.request.urlopen(req) as r:
                issue = json.load(r)
        except Exception:
            continue
        if issue.get("state") == "closed" and describes_as_open(text, n):
            stale.append(n)
    if stale:
        return False, f"describes closed issue(s) as still open: {stale}"
    return True, f"{len(refs)} referenced issue(s), none misdescribed"


def check_decision_ids():
    """Two authors appending to DECISIONS.md will pick the same number.

    It happened on 2026-09-21: a shift added a D6 and this session added
    another, independently. A duplicate id makes every later reference
    ambiguous, and one decision was lost entirely in the same episode.
    """
    ids = re.findall(r"^## (D\d+)\b", _read("DECISIONS.md"), re.M)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        return False, f"duplicate decision id(s): {', '.join(dupes)}"
    nums = sorted(int(i[1:]) for i in ids)
    gaps = [n for n in range(1, max(nums, default=0)) if n not in nums]
    if gaps:
        return False, (f"missing decision id(s) {gaps} — a record was lost or "
                       f"mis-numbered")
    return True, f"{len(ids)} decisions, ids unique and contiguous"


CHECKS = [
    ("decision ids", check_decision_ids),
    ("live format", check_live_format),
    ("merged branches", check_merged_branches),
    ("cohort sizes", check_upload_counts),
    ("issue references", check_open_escalations),
]


def main():
    strict = "--check" in sys.argv
    bad = 0
    print("TRACKER CLAIMS")
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = None, f"check errored ({type(e).__name__})"
        mark = {True: "ok  ", False: "STALE", None: "skip"}[ok]
        print(f"  {mark}  {name}: {detail}")
        if ok is False:
            bad += 1
    print(f"\n{bad} stale claim(s)." if bad else "\nNo stale claims found.")
    print("Judgement is still needed for what this cannot check: whether §0's"
          "\npriorities are right, and whether a finding still holds.")
    return 1 if (bad and strict) else 0


if __name__ == "__main__":
    sys.exit(main())
