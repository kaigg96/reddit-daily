"""Collect how long each uploaded video's answers were, from the live runs' logs.

The upload log records the post but not the answers read. Each live run's
Actions log prints them (`  comment N: …`) and the video it uploaded
(`Upload complete! Video ID: …`), so this reads those logs and writes word
counts only — never the answers' text, which is Reddit's — to
`analysis/answer_lengths.csv`, for `report.py --first-answer` (PRD §4).
Answers are printed before the duration guard can drop the last, so `words_2`
and `words_3` may count an answer the video left out; `words_1` never is (review).

    venv/bin/python scripts/answer_lengths.py

Read-only against GitHub (`gh run view --log`); logs expire after ~90 days,
so rows already in the file are kept and only new uploads are added.
"""
import concurrent.futures
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "answer_lengths.csv"
FIELDS = ["video_id", "run_id", "words_1", "words_2", "words_3"]
COMMENT = re.compile(r"Z\s+comment ([123]): (.*)$")
UPLOADED = re.compile(r"Upload complete! Video ID: ([\w-]{11})")


def parse_log(text):
    """(video_id, {n: words}) from one run's log, or None when it uploaded
    nothing (an off slot, a dry run, a failure)."""
    video, words = None, {}
    for line in text.splitlines():
        m = COMMENT.search(line)
        if m and int(m.group(1)) not in words:
            words[int(m.group(1))] = len(m.group(2).split())
        m = UPLOADED.search(line)
        if m:
            video = m.group(1)
    return (video, words) if video and 1 in words else None


def _log(run_id):
    out = subprocess.run(["gh", "run", "view", str(run_id), "--log"],
                         capture_output=True, text=True)
    return run_id, out.stdout if out.returncode == 0 else ""


def main():
    rows = {}
    if OUT.exists():
        rows = {r["video_id"]: r for r in csv.DictReader(OUT.open())}
    runs = json.loads(subprocess.run(
        ["gh", "run", "list", "--workflow", "run-reddit-video.yml", "--limit", "400",
         "--status", "success", "--json", "databaseId"],
        capture_output=True, text=True, check=True).stdout)
    seen = {r["run_id"] for r in rows.values()}
    todo = [r["databaseId"] for r in runs if str(r["databaseId"]) not in seen]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for run_id, text in pool.map(_log, todo):
            parsed = parse_log(text)
            if parsed:
                video, words = parsed
                rows[video] = {"video_id": video, "run_id": run_id,
                               **{f"words_{n}": words.get(n, "") for n in (1, 2, 3)}}
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: int(r["run_id"])))
    print(f"{len(rows)} uploads with answer lengths ({len(todo)} logs read) -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
