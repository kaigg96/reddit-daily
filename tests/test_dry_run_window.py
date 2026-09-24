"""dry-run.yml refuses an automated render that would spend Gemini requests
the morning upload still needs. Runs the step's exact shell with a fake clock."""
import os
import shutil
import stat
import subprocess

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKE_DATE = """#!/bin/bash
case "$*" in
  "-u +%H") echo "$FAKE_HOUR" ;;
  "-u +%Y-%m-%d") echo "$FAKE_DAY" ;;
  *) /bin/date "$@" ;;
esac
"""


def refusal(tmp_path, hour, uploads, event="push"):
    step = next(s for s in yaml.safe_load(open(os.path.join(ROOT, ".github/workflows/dry-run.yml")))
                ["jobs"]["render"]["steps"] if s.get("name") == "What to render")
    work, fake = tmp_path / "work", tmp_path / "bin"
    (work / "scripts").mkdir(parents=True)
    (work / ".dry-run-requests").mkdir()
    fake.mkdir()
    shutil.copy(os.path.join(ROOT, "scripts", "dry_run.py"), work / "scripts")
    (work / ".dry-run-requests" / "v7.md").write_text("branch: feature/v7\nrequested_at: x\n")
    (work / "upload_log.csv").write_text("timestamp_utc,video_id\n" + "".join(f"{u},id\n" for u in uploads))
    (fake / "date").write_text(FAKE_DATE)
    (fake / "date").chmod(stat.S_IRWXU)
    out = tmp_path / "out"
    subprocess.run(["bash", "-e", "-c", step["run"]], cwd=work, capture_output=True, text=True,
                   env=dict(os.environ, PATH=f"{fake}:{os.environ['PATH']}", EVENT=event,
                            GITHUB_OUTPUT=str(out), FAKE_HOUR=hour, FAKE_DAY="2026-09-24",
                            GH_TOKEN="x", INPUT_BRANCH="feature/v7"))
    return dict(line.split("=", 1) for line in out.read_text().splitlines() if "=" in line)


def test_before_the_reset_it_waits_for_the_morning_upload(tmp_path):
    out = refusal(tmp_path, "04", ["2026-09-23T17:13:57+00:00"])
    assert out["go"] == "false" and "morning upload has not landed" in out["why"]


@pytest.mark.parametrize("hour, uploads, event", [
    ("05", ["2026-09-24T04:51:00+00:00"], "push"),       # upload landed: budget no longer contested
    ("09", ["2026-09-23T17:13:57+00:00"], "push"),       # after the reset
    ("04", ["2026-09-23T17:13:57+00:00"], "workflow_dispatch"),   # the owner's own call
])
def test_otherwise_the_clock_does_not_stop_it(tmp_path, hour, uploads, event):
    out = refusal(tmp_path, hour, uploads, event)
    # It got past the clock and stopped only at the next check (no origin here).
    assert "is not on origin" in out.get("why", "")
