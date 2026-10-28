#!/usr/bin/env python3
"""See and close the owner's decisions, so they stop being involved.

An escalation asks the owner something. Once they label it `approved` they are
done with it -- but nothing picked the decision back up, so four settled
questions sat open at once and every one of them kept notifying them. An
approved escalation is a **work item**, not a question.

    escalations.py open              # anything still awaiting a decision
    escalations.py approved          # decided — do these, then close them;
                                     # also lists recent refusals
    escalations.py close <n> "what was done"

Needs GH_TOKEN (locally, from .env) or GITHUB_TOKEN (in CI).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

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


def _comments(issue):
    """Every comment on an issue, oldest first. The API pages them 30 at a
    time by default, so without paging the "latest" comment was the 30th:
    #55 gathers about three re-raise notices a day."""
    out = []
    for page in range(1, (issue.get("comments") or 0) // 100 + 2):
        out += _api(f"/repos/{REPO}/issues/{issue['number']}/comments?per_page=100&page={page}") or []
    return out


def _owner_replies(issue):
    """What the owner wrote on an escalation. The owner answers in comments --
    on 2026-09-24 one reply read "not approved to spend real money on this,
    other solutions acceptable" -- and this script used to print titles only,
    so a shift could act on the label and never see the condition attached."""
    if not issue.get("comments"):
        return []
    return [c["body"].strip() for c in _comments(issue)
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
               (_comments(issue) if issue.get("comments") else [])
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


DECLINED_DAYS = 7


def _declined(days=DECLINED_DAYS, now=None):
    """Escalations the owner closed without approving, with what they said.

    A "no" is a decision too, and this script listed open issues only. On
    2026-10-08 the owner closed #62 ("Not approved to spend money on this,
    find another solution") and that morning's shift, reading only the open
    list, missed both the refusal and the request in it. Only closes carrying
    an owner reply are shown: the reply is the decision, and a bare close is
    usually a duplicate or a notice acknowledged. Only the owner's own close
    counts: a shift can close an escalation too (superseded, split), and the
    owner's question on it is not their answer."""
    now = now or datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    owner = REPO.split("/")[0]
    out = []
    for i in _api(f"/repos/{REPO}/issues?state=closed&labels=needs-owner"
                  f"&since={cutoff}&per_page=100"):
        labels = {l["name"].strip().lower() for l in i["labels"]}
        if ("pull_request" in i or "needs-owner" not in labels or "approved" in labels
                or (i.get("closed_at") or "") < cutoff):
            continue
        replies = _owner_replies(i)
        if not replies:
            continue
        closes = [e for e in _api(f"/repos/{REPO}/issues/{i['number']}/events?per_page=100")
                  if e.get("event") == "closed"]
        if closes and (closes[-1].get("actor") or {}).get("login") == owner:
            out.append((i, replies))
    return out


def _answered_in_comment(issues):
    """Open, unlabelled escalations where the owner's comment is the latest.

    The owner also answers in a comment without labelling or closing. On
    2026-10-10 they replied on #60 that asking Reddit could wait until before
    monetization, and the next shift, reading only the `approved` listing,
    reported #60 as still waiting on them. A reply that is the last word on
    an open ask is their answer until they say otherwise."""
    out = []
    for i, labels in issues:
        if "approved" in labels or not i.get("comments"):
            continue
        comments = _comments(i)
        last = comments[-1] if comments else {}
        if last.get("author_association") == "OWNER" and last.get("body", "").strip():
            out.append((i, last["body"].strip()))
    return out


OWNER_ACTS = {"labeled", "unlabeled", "closed", "reopened"}


def _owner_last_action():
    """(when, what) the owner last did on any issue, or None.

    D13 revisits when a label-only ask waits over three days, and asks first
    whether the owner is away or passing it over. Each of its re-reviews
    (10-11 to 10-28) dug that up by hand; on 10-28 the answer was that they
    had labelled #84 and #85 within hours while #77 and #80 waited.

    Only deliberate acts count. A `referenced` event names whoever's token
    pushed the commit, and the auto-apply job pushes with the owner's: an
    unattended run would read as the owner here (review, 10-28)."""
    owner = REPO.split("/")[0]
    seen = []
    for e in _api(f"/repos/{REPO}/issues/events?per_page=100") or []:
        if (e.get("event") in OWNER_ACTS and (e.get("actor") or {}).get("login") == owner
                and e.get("created_at")):
            label = (e.get("label") or {}).get("name")
            seen.append((e["created_at"], f"{e.get('event', '?')}{' ' + label if label else ''}"
                                          f" #{(e.get('issue') or {}).get('number', '?')}"))
    for c in _api(f"/repos/{REPO}/issues/comments?sort=created&direction=desc&per_page=100") or []:
        if c.get("author_association") == "OWNER" and c.get("created_at"):
            seen.append((c["created_at"], f"commented on #{(c.get('issue_url') or '?').rsplit('/', 1)[-1]}"))
    return max(seen) if seen else None


def _print_owner_last_action(now=None):
    """One line, and never the reason the listing fails: it is context."""
    try:
        last = _owner_last_action()
    except Exception as e:
        print(f"The owner's last action could not be read ({type(e).__name__}).")
        return
    if not last:
        print("The owner's last action: none in the newest issue events and comments.")
        return
    when, what = last
    now = now or datetime.now(timezone.utc)
    hours = (now - datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)) / timedelta(hours=1)
    print(f"The owner last acted {hours:.0f} hours ago ({when[:16].replace('T', ' ')} UTC: {what}). "
          "An ask waiting longer than that waited while they were here (D13).")


def show(want_approved):
    issues = _issues()
    if not want_approved:
        _print_owner_last_action()
    rows = [(i, l) for i, l in issues if ("approved" in l) == want_approved]
    if want_approved:
        answered = _answered_in_comment(issues)
        if answered:
            print("ANSWERED IN A COMMENT, NOT LABELLED: the owner's reply is the latest "
                  "word on an open ask. If it decides, record it, do what it allows and "
                  "close the issue saying what was done; if it asks, answer it. It "
                  "approves nothing it does not say:")
            for i, reply in answered:
                print(f"  #{i['number']}  {i['title']}")
                print("      owner: " + reply.replace("\n", "\n             "))
        declined = _declined()
        if declined:
            print(f"CLOSED BY THE OWNER WITHOUT APPROVAL in the last {DECLINED_DAYS} days. "
                  "Their reply says why. It approves nothing, so do not re-ask what it "
                  "refused:")
            for i, replies in declined:
                print(f"  #{i['number']}  {i['title']}  (closed {i['closed_at'][:10]})")
                for reply in replies:
                    print("      owner: " + reply.replace("\n", "\n             "))
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
