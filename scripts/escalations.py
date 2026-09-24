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


def show(want_approved):
    rows = [(i, l) for i, l in _issues() if ("approved" in l) == want_approved]
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
