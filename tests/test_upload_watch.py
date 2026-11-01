"""The upload check the shift workflow runs whatever the allowance (#86)."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import upload_watch

UTC = datetime.timezone.utc
NOW = datetime.datetime(2026, 11, 4, 19, 30, tzinfo=UTC)


def run(conclusion, hours_ago, event="schedule"):
    created = (NOW - datetime.timedelta(hours=hours_ago)).isoformat().replace("+00:00", "Z")
    return {"event": event, "conclusion": conclusion, "created_at": created,
            "html_url": "https://github.com/x/y/actions/runs/1"}


def test_a_normal_day_is_quiet():
    last = NOW - datetime.timedelta(hours=15)   # the longest good gap since September
    runs = [run("success", 2), run("success", 14), run(None, 0)]   # one still running
    assert upload_watch.problems(last, runs, NOW) == []


def test_a_day_without_an_upload_is_reported():
    found = upload_watch.problems(NOW - datetime.timedelta(hours=21), [], NOW)
    assert found == ["no upload for 21 hours (the last was 2026-11-03 22:30 UTC)"]


def test_one_failed_slot_is_reported_though_the_next_upload_landed():
    found = upload_watch.problems(NOW - datetime.timedelta(hours=1), [run("failure", 12)], NOW)
    assert found == ["a scheduled upload run failure: https://github.com/x/y/actions/runs/1"]


def test_old_or_manual_failures_and_an_unreadable_run_list_are_not_alarms():
    last = NOW - datetime.timedelta(hours=3)
    assert upload_watch.problems(last, [run("failure", 25), run("failure", 1, "workflow_dispatch")], NOW) == []
    assert upload_watch.problems(last, None, NOW) == []


def test_the_log_is_read_and_the_exit_code_fails_the_step(tmp_path, capsys, monkeypatch):
    log = tmp_path / "upload_log.csv"
    log.write_text("timestamp_utc,video_id\n2026-11-01T06:29:39+00:00,a\n2026-10-31T17:19:11+00:00,b\n")
    assert upload_watch.last_upload(str(log)) == datetime.datetime(2026, 11, 1, 6, 29, 39, tzinfo=UTC)

    class Clock(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW

    monkeypatch.setattr(upload_watch.datetime, "datetime", Clock)
    assert upload_watch.main(["upload_watch.py", str(log)]) == 1
    assert "::error::Upload check: no upload for 85 hours" in capsys.readouterr().out
