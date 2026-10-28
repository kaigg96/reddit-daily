"""The upload log after a live upload: a failure loses the row, never the
record of the post, and never the log itself (src/log.py)."""
import csv

import pytest

from src import log


def test_a_failing_append_does_not_raise_and_says_so(monkeypatch, capsys):
    def broken(*a, **k):
        raise OSError("disk")
    monkeypatch.setattr(log, "_append", broken)
    log.append_upload_log({"video_id": "abc"})
    assert "::error::Upload abc not logged: OSError" in capsys.readouterr().out


def test_a_migration_that_fails_part_way_leaves_the_old_log_whole(monkeypatch, tmp_path):
    path = tmp_path / "upload_log.csv"
    path.write_text("timestamp_utc,video_id\n2026-10-01,a\n2026-10-02,b\n")
    before = path.read_text()
    real = csv.DictWriter.writerow
    calls = []

    def fail_on_second(self, row):
        calls.append(row)
        if len(calls) == 2:
            raise OSError("disk full")
        return real(self, row)
    monkeypatch.setattr(csv.DictWriter, "writerow", fail_on_second)
    with pytest.raises(OSError):
        log._migrate_header(path, ["timestamp_utc", "video_id", "new_column"])
    assert path.read_text() == before


def test_a_migration_still_rewrites_the_header(tmp_path):
    path = tmp_path / "upload_log.csv"
    path.write_text("timestamp_utc,video_id\n2026-10-01,a\n")
    log._migrate_header(path, ["timestamp_utc", "video_id", "new_column"])
    assert path.read_text().splitlines() == ["timestamp_utc,video_id,new_column", "2026-10-01,a,"]
    assert not (tmp_path / "upload_log.csv.tmp").exists()
