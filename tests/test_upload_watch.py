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


def ago(*hours):
    return [NOW - datetime.timedelta(hours=h) for h in hours]


def test_a_normal_day_is_quiet():
    stamps = ago(1, 16, 27)   # the longest good gap since September was 15.1 hours
    runs = [run("success", 2), run("success", 14), run(None, 0)]   # one still running
    assert upload_watch.problems(stamps, runs, NOW) == []


def test_a_missed_slot_is_reported_though_its_run_never_failed():
    # an evening run that never started: the morning upload landed, the one before is 30 hours old
    found = upload_watch.problems(ago(13, 30), [], NOW)
    assert found == ["1 upload(s) in the last 28 hours, where 2 are expected (the last was 2026-11-04 06:30 UTC)"]
    assert upload_watch.problems([], None, NOW) == [
        "0 upload(s) in the last 28 hours, where 2 are expected (the log has none)"]


def test_one_failed_run_is_reported_the_same_day():
    found = upload_watch.problems(ago(1, 16), [run("failure", 12)], NOW)
    assert found == ["a scheduled upload run failure: https://github.com/x/y/actions/runs/1"]


def test_old_or_manual_failures_and_an_unreadable_run_list_are_not_alarms():
    stamps = ago(3, 15)
    assert upload_watch.problems(stamps, [run("failure", 25), run("failure", 1, "workflow_dispatch")], NOW) == []
    assert upload_watch.problems(stamps, None, NOW) == []


def test_the_log_is_read_and_the_exit_code_fails_the_step(tmp_path, capsys, monkeypatch):
    log = tmp_path / "upload_log.csv"
    log.write_text("timestamp_utc,video_id\n2026-11-01T06:29:39+00:00,a\nnot a time,c\n"
                   "2026-10-31T17:19:11+00:00,b\n")
    assert max(upload_watch.upload_times(str(log))) == datetime.datetime(2026, 11, 1, 6, 29, 39, tzinfo=UTC)

    class Clock(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW

    monkeypatch.setattr(upload_watch.datetime, "datetime", Clock)
    assert upload_watch.main(["upload_watch.py", str(log)]) == 1
    assert "::error::Upload check: 0 upload(s) in the last 28 hours" in capsys.readouterr().out
