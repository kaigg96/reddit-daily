#!/usr/bin/env python3
"""Did the uploads land? Fails, so that GitHub emails the owner, when not.

GitHub emails a scheduled workflow's failures to whoever last edited its
`schedule` lines, and since 2026-10-11 that is a bot for the upload job
(TECH_DEBT, #86). Shifts check the upload log, but none runs once the weekly
allowance is spent. The shift workflow's own schedule is the owner's, and it
runs three times a day whatever the allowance, so a step there that fails on a
missed upload reaches them however the upload job's schedule was last edited.

Two checks:
- fewer than MIN_UPLOADS uploads in the last WINDOW_HOURS: catches any missed
  slot, a run that never started or was cancelled included. Replayed over the
  129 scheduled shift starts from 09-20 to 11-13 it raises no false alarm, and
  flags the one real miss (10-05's evening) at both shifts after it; the
  closest call was 26.7 hours (11-02), and 26 hours would have raised one
  false alarm (10-12, a 15-hour gap);
- a scheduled upload run that failed in the last day: the same day's news,
  where the count can wait for the next morning.

    upload_watch.py <upload_log.csv> [<repo> <token>]

Without a token only the first check runs. A failed read of the run list is
reported and never fails the step: a false alarm every shift would be ignored.
"""
import csv
import datetime
import json
import sys

WINDOW_HOURS = 28
MIN_UPLOADS = 2   # at two a day; at four it still catches three misses in a row
FAILED = {"failure", "timed_out", "startup_failure"}
WORKFLOW = "run-reddit-video.yml"


def _ts(text):
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))


def upload_times(log_path):
    """Every upload's time; a row that does not parse is skipped, not fatal,
    since a crash here would read as a missed upload."""
    stamps = []
    with open(log_path, newline="") as f:
        for r in csv.DictReader(f):
            try:
                stamps.append(_ts(r["timestamp_utc"]))
            except (KeyError, TypeError, ValueError, AttributeError):
                continue
    return stamps


def problems(stamps, runs, now):
    """Plain-language problems; [] when the uploads look fine. `runs` is the
    workflow's run list from the API, or None when it could not be read."""
    found = []
    recent = [t for t in stamps if now - datetime.timedelta(hours=WINDOW_HOURS) < t <= now]
    if len(recent) < MIN_UPLOADS:
        last = f"the last was {max(stamps):%Y-%m-%d %H:%M} UTC" if stamps else "the log has none"
        found.append(f"{len(recent)} upload(s) in the last {WINDOW_HOURS} hours, "
                     f"where {MIN_UPLOADS} are expected ({last})")
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
    found = problems(upload_times(argv[1]), runs, datetime.datetime.now(datetime.timezone.utc))
    for p in found:
        print(f"::error::Upload check: {p}")
    if not found:
        print("uploads ok")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
