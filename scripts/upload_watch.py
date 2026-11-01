#!/usr/bin/env python3
"""Did the uploads land? Fails, so that GitHub emails the owner, when not.

GitHub emails a scheduled workflow's failures to whoever last edited its
`schedule` lines, and since 2026-10-11 that is a bot for the upload job
(TECH_DEBT, #86). Shifts check the upload log, but none runs once the weekly
allowance is spent. The shift workflow's own schedule is the owner's, and it
runs three times a day whatever the allowance, so a step there that fails on a
missed upload reaches them however the upload job's schedule was last edited.

Two checks, because each misses what the other sees:
- the newest upload is older than STALE_HOURS: catches runs that never start;
  the longest gap between two good uploads since September was 15.1 hours;
- a scheduled upload run failed in the last day: catches a single missed slot,
  which the next slot's upload would hide from the first check.

    upload_watch.py <upload_log.csv> [<repo> <token>]

Without a token only the first check runs. A failed read of the run list is
reported and never fails the step: a false alarm every shift would be ignored.
"""
import csv
import datetime
import json
import sys

STALE_HOURS = 20
FAILED = {"failure", "timed_out", "startup_failure"}
WORKFLOW = "run-reddit-video.yml"


def _ts(text):
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))


def last_upload(log_path):
    with open(log_path, newline="") as f:
        stamps = [_ts(r["timestamp_utc"]) for r in csv.DictReader(f) if r.get("timestamp_utc")]
    return max(stamps) if stamps else None


def problems(last, runs, now):
    """Plain-language problems; [] when the uploads look fine. `runs` is the
    workflow's run list from the API, or None when it could not be read."""
    found = []
    if last is None:
        found.append("the upload log has no uploads")
    elif now - last > datetime.timedelta(hours=STALE_HOURS):
        hours = (now - last).total_seconds() / 3600
        found.append(f"no upload for {hours:.0f} hours (the last was {last:%Y-%m-%d %H:%M} UTC)")
    for r in runs or []:
        if r.get("event") != "schedule" or r.get("conclusion") not in FAILED:
            continue
        if now - _ts(r["created_at"]) <= datetime.timedelta(days=1):
            found.append(f"a scheduled upload run {r['conclusion'].replace('_', ' ')}: {r.get('html_url', '')}")
    return found


def scheduled_runs(repo, token):
    import urllib.request
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW}/runs?per_page=20",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=30)).get("workflow_runs") or []
    except Exception as e:
        print(f"::warning::could not read the upload runs ({type(e).__name__}); checked the log only")
        return None


def main(argv):
    if len(argv) not in (2, 4):
        print(__doc__)
        return 2
    runs = scheduled_runs(argv[2], argv[3]) if len(argv) == 4 else None
    found = problems(last_upload(argv[1]), runs, datetime.datetime.now(datetime.timezone.utc))
    for p in found:
        print(f"::error::Upload check: {p}")
    if not found:
        print("uploads ok")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
