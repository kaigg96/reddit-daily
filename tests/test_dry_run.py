"""Dry runs by request (#27). A shift cannot render, so it queues a request and
reads a verdict; these pin the parts that decide what gets rendered and what
the verdict says."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import dry_run

GOOD = dict(size=(1080, 1920), fps=30.0, duration=18.8, has_audio=True,
            frames_ok=True, decode_errors="", silences=[(3.2, 0.34)])


def test_the_render_that_shipped_passes():
    """Measured 2026-09-24 on a real upload. PRD §9's old 20 s floor and 0.3 s
    silence rule would both have failed it."""
    assert dry_run.judge(**GOOD) == (True, [])


@pytest.mark.parametrize("change, reason", [
    (dict(size=(720, 1280)), "size 720x1280"),
    (dict(fps=24.0), "24 fps"),
    (dict(duration=4.0), "4.0 s long"),
    (dict(duration=75.0), "75.0 s long"),
    (dict(has_audio=False), "no audio track"),
    (dict(frames_ok=False), "frames could not be decoded"),
    (dict(decode_errors="Invalid NAL unit"), "decoder errors"),
    (dict(silences=[(5.0, 4.0)]), "dead air: 4.0 s at 5.0 s"),
])
def test_a_broken_render_fails_and_says_why(change, reason):
    ok, bad = dry_run.judge(**dict(GOOD, **change))
    assert not ok and any(reason in b for b in bad)


@pytest.mark.parametrize("name, ok", [
    ("feature/v7-open-on-hook", True), ("main", True), ("fix/a.b_c", True),
    ("", False), ("-rf", False), ("a..b", False), ("x; rm -rf /", False),
    ("feature/$(whoami)", False), ("a" * 101, False),
])
def test_only_plain_branch_names_are_rendered(name, ok):
    """The name reaches a checkout and a shell; anything odd is refused."""
    assert dry_run.valid_branch(name) is ok


def test_request_refuses_a_bad_name():
    with pytest.raises(SystemExit):
        dry_run.request("feature/$(whoami)")


def test_pending_takes_the_newest_valid_request(tmp_path, capsys):
    (tmp_path / "README.md").write_text("branch: not-a-request\n")
    (tmp_path / "old.md").write_text("branch: feature/old\nrequested_at: 2026-09-24T09:00:00Z\n")
    (tmp_path / "new.md").write_text("branch: feature/new\nrequested_at: 2026-09-24T10:00:00Z\n")
    (tmp_path / "evil.md").write_text("branch: x; rm -rf /\nrequested_at: 2026-09-24T11:00:00Z\n")
    dry_run.pending(str(tmp_path))
    assert capsys.readouterr().out.strip() == "feature/new"


def test_pending_with_nothing_queued_prints_nothing(tmp_path, capsys):
    dry_run.pending(str(tmp_path))
    assert capsys.readouterr().out == ""


def record(tmp_path, monkeypatch, *argv):
    monkeypatch.chdir(tmp_path)
    dry_run.main(["record", *argv])
    return (tmp_path / ".github" / "last-dry-run.md").read_text()


def test_a_pass_names_the_commit(tmp_path, monkeypatch):
    (tmp_path / "check.txt").write_text("PASS -- playable: 1080x1920, 30 fps, 18.8 s")
    out = record(tmp_path, monkeypatch, "--branch", "feature/v7", "--commit", "abc1234",
                 "--render-code", "0", "--check-file", "check.txt", "--run-url", "u")
    assert "`abc1234`" in out and "✅ PASS" in out and "rendered" in out
    assert "<details>" not in out


def test_a_pass_still_shows_calls_that_failed_soft(tmp_path, monkeypatch):
    (tmp_path / "check.txt").write_text("PASS -- playable")
    (tmp_path / "run.log").write_text("Selected post: q\n"
                                      "Slate: topic call failed with HTTPError 429 (not logged this run)\n"
                                      "Slate topics (rank order): (not collected)\nUploaded fine\n")
    out = record(tmp_path, monkeypatch, "--branch", "feature/v7", "--commit", "abc1234",
                 "--render-code", "0", "--check-file", "check.txt", "--log", "run.log",
                 "--run-url", "u")
    assert "✅ PASS" in out and "HTTPError 429" in out and "(not collected)" in out
    assert "Uploaded fine" not in out


def test_a_pass_shows_what_the_screen_picked_and_skipped(tmp_path, monkeypatch):
    """A screen replay on a new subreddit is read from here, not from Actions."""
    (tmp_path / "check.txt").write_text("PASS -- playable")
    (tmp_path / "run.log").write_text("Screen: skipping post (named_wrongdoing) — q1\n"
                                      "Selected post: q2\n  comment 1: an answer\n"
                                      "Today's top NoStupidQuestions post: q2\n")
    out = record(tmp_path, monkeypatch, "--branch", "b", "--commit", "abc1234",
                 "--render-code", "0", "--check-file", "check.txt", "--log", "run.log",
                 "--run-url", "u")
    assert "skipping post (named_wrongdoing)" in out and "Selected post: q2" in out
    assert "NoStupidQuestions" in out and "an answer" not in out


def test_a_failure_carries_the_end_of_the_log(tmp_path, monkeypatch):
    (tmp_path / "run.log").write_text("\n".join(f"line {i}" for i in range(100)))
    out = record(tmp_path, monkeypatch, "--branch", "feature/v7", "--commit", "abc1234",
                 "--render-code", "1", "--log", "run.log", "--run-url", "u")
    assert "❌ FAIL -- the pipeline exited 1" in out
    assert "line 99" in out and "line 59" not in out    # the last 40 lines only


def test_a_refusal_keeps_the_last_real_verdict(tmp_path, monkeypatch):
    (tmp_path / "check.txt").write_text("PASS -- playable")
    record(tmp_path, monkeypatch, "--branch", "feature/v7", "--commit", "abc1234",
           "--render-code", "0", "--check-file", "check.txt", "--run-url", "u")
    out = record(tmp_path, monkeypatch, "--branch", "feature/v8",
                 "--refused", "one automated render per 12 hours")
    last_render, last_request = out.split("## Last request")
    assert "`abc1234`" in last_render and "✅ PASS" in last_render
    assert "feature/v8" in last_request and "not rendered" in last_request
