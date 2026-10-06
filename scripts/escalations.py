#!/usr/bin/env python3
"""See and close the owner's decisions, so they stop being involved.

An escalation asks the owner something. Once they label it `approved` they are
done with it -- but nothing picked the decision back up, so four settled
questions sat open at once and every one of them kept notifying them. An
approved escalation is a **work item**, not a question.

    escalations.py open              # anything still awaiting a decision
    escalations.py approved          # decided — do these, then close them
    escalations.py close <n> "what was done"

Needs GH_TOKEN (locally, from .env) or GITHUB_TOKEN (in CI).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "kaigg96/reddit-daily")


def _token():
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    sys.exit("no GH_TOKEN or GITHUB_TOKEN — cannot reach GitHub")


def _api(path, data=None, method=None):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        data=json.dumps(data).encode() if data else None,
        method=method or ("POST" if data else "GET"),
        headers={"Authorization": f"Bearer {_token()}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r) if r.status != 204 else None


def _issues():
    out = []
    for i in _api(f"/repos/{REPO}/issues?state=open&per_page=100"):
        if "pull_request" in i:
            continue
        labels = {l["name"] for l in i["labels"]}
        if "needs-owner" in labels:
            out.append((i, labels))
    return out


def _owner_replies(issue):
    """What the owner wrote on an escalation. The owner answers in comments --
    on 2026-09-24 one reply read "not approved to spend real money on this,
    other solutions acceptable" -- and this script used to print titles only,
    so a shift could act on the label and never see the condition attached."""
    if not issue.get("comments"):
        return []
    return [c["body"].strip() for c in
            _api(f"/repos/{REPO}/issues/{issue['number']}/comments")
            if c.get("author_association") == "OWNER" and c["body"].strip()]


def _recommendation(issue):
    """What the owner approved when they labelled it. An approval with no
    reply printed as a bare title, so the shift had to open the issue to learn
    what it was asked to do (#43, 2026-10-01)."""
    m = re.search(r"^## Recommendation\s*$(.*?)(?=^---|^## |\Z)",
                  issue.get("body") or "", re.S | re.M)
    return " ".join(m.group(1).split()) if m else ""


APPLY_MARKER = "<!-- apply-patch -->"      # escalate.py --patch
RESULT_MARKER = "<!-- apply-result -->"    # apply-approved.yml's report


def _not_applied(issue):
    """Why an approved patch is not on main, or None if it landed or has none.

    On 2026-10-05 the owner approved #53, and the job that applies it was
    cancelled in a GitHub outage before it ran a step. The issue still read
    as approved, the label is all this listing showed, and nothing on main
    had changed, so the approval was silently lost. The job reports on the
    issue whatever it does; no report means it never ran."""
    if APPLY_MARKER not in (issue.get("body") or ""):
        return None
    results = [c["body"] for c in
               (_api(f"/repos/{REPO}/issues/{issue['number']}/comments")
                if issue.get("comments") else [])
               if c.get("body", "").startswith(RESULT_MARKER)]
    if not results:
        return ("the apply job never reported, so it did not run. Only the "
                "owner's label starts it: ask them to re-run it or re-label")
    last = " ".join(results[-1][len(RESULT_MARKER):].split())
    return None if last.startswith("**Applied**") else last


def _approved_by_owner(issue):
    """Only the owner's own label is a decision. A shift's token can add
    labels -- it closes and comments with the same permission -- and the guard
    applies this same rule before accepting an `Approved-In:`."""
    owner = REPO.split("/")[0]
    marks = [e for e in _api(f"/repos/{REPO}/issues/{issue['number']}/events?per_page=100")
             if e.get("event") == "labeled"
             and (e.get("label") or {}).get("name", "").strip().lower() == "approved"]
    return bool(marks) and (marks[-1].get("actor") or {}).get("login") == owner


def show(want_approved):
    rows = [(i, l) for i, l in _issues() if ("approved" in l) == want_approved]
    if want_approved:
        forged = [(i, l) for i, l in rows if not _approved_by_owner(i)]
        rows = [r for r in rows if r not in forged]
        if forged:
            print("LABELLED APPROVED, BUT NOT BY THE OWNER — not a decision; do not act:")
            for i, _ in forged:
                print(f"  #{i['number']}  {i['title']}")
    if not rows:
        print("approved and waiting to be done: none" if want_approved
              else "awaiting the owner: none")
        return 0
    print("DECIDED — do these, then close them. The owner's replies are part of "
          "the decision and bind what you do:" if want_approved
          else "AWAITING THE OWNER — do not act on these. Replies are shown so "
          "you do not re-ask what they have answered; a reply is not approval:")
    for i, _ in rows:
        print(f"  #{i['number']}  {i['title']}")
        if want_approved and _recommendation(i):
            print("      approved: " + _recommendation(i))
        unapplied = want_approved and _not_applied(i)
        if unapplied:
            print("      NOT APPLIED: " + unapplied)
        for reply in _owner_replies(i):
            print("      owner: " + reply.replace("\n", "\n             "))
    return 0


def close(number, message):
    """Close only with a note saying what was done — a bare close loses why."""
    _api(f"/repos/{REPO}/issues/{number}/comments", {"body": message})
    _api(f"/repos/{REPO}/issues/{number}", {"state": "closed"}, method="PATCH")
    print(f"closed #{number}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if cmd == "approved":
            sys.exit(show(True))
        if cmd == "open":
            sys.exit(show(False))
        if cmd == "close" and len(sys.argv) >= 4:
            sys.exit(close(int(sys.argv[2]), " ".join(sys.argv[3:])))
    except urllib.error.HTTPError as e:
        sys.exit(f"GitHub said {e.code}: {e.reason}")
    sys.exit(__doc__)
