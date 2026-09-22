"""The release gate's skip decision — it guards 6 of the 20 daily Gemini
requests, and those are shared with live uploads."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.validate_release import parse_verdict, should_validate

WRITTEN = "2026-09-20T13:02:51Z"
NOW = datetime.datetime(2026, 9, 21, 8, 17, 0)   # the morning after


def verdict(commit, result, when=WRITTEN):
    """A last-release-validation.md exactly as the workflow writes one."""
    return (
        "# Last release validation\n\n"
        "Written by `validate-release.yml`. A shift reads this instead of\n"
        "needing live Gemini quota to find out whether the gates pass.\n\n"
        "- **Branch:** `main`\n"
        f"- **Commit:** `{commit}`\n"
        f"- **When:** {when}\n"
        f"- **Verdict:** {result}\n"
    )


PASS = "✅ PASS — safe to merge"
FAIL = "❌ FAIL — do not merge"

never = lambda _prev: False
always = lambda _prev: True


def decide(text, target, changed=never, now=NOW):
    return should_validate(text, target, changed, now=now)


def test_parses_the_workflows_own_format():
    commit, passed, when = parse_verdict(verdict("c6ee5f7", PASS))
    assert (commit, passed) == ("c6ee5f7", True)
    assert when == datetime.datetime(2026, 9, 20, 13, 2, 51)


def test_prose_saying_gates_pass_is_not_a_verdict():
    # The file's own header contains "whether the gates pass"; a whole-file
    # grep for PASS would read a FAIL as a pass.
    assert parse_verdict(verdict("c6ee5f7", FAIL))[1] is False


def test_the_verdict_record_commit_does_not_force_a_re_run():
    """The regression this fix exists for.

    Recording a PASS for c6ee5f7 commits to main, so the next morning HEAD is
    a4fb38c — one commit later, touching only .github/. The old sha-equality
    check compared c6ee5f7 to a4fb38c, never matched, and re-ran the gates
    every single day forever.
    """
    proceed, why = decide(verdict("c6ee5f7", PASS), "a4fb38c")
    assert proceed is False, why


def test_doc_only_commits_do_not_spend_quota():
    assert decide(verdict("c6ee5f7", PASS), "de759ee")[0] is False


def test_changed_gated_code_revalidates():
    proceed, why = decide(verdict("c6ee5f7", PASS), "89bc245", changed=always)
    assert proceed is True
    assert "changed" in why


def test_a_fail_is_always_retried():
    # Commonest cause is an exhausted quota, not bad output.
    proceed, why = decide(verdict("c6ee5f7", FAIL), "c6ee5f7")
    assert proceed is True
    assert "FAIL" in why


def test_no_verdict_file_validates():
    assert decide("", "c6ee5f7")[0] is True


def test_unchanged_head_still_skips():
    assert decide(verdict("c6ee5f7", PASS), "c6ee5f7")[0] is False


def test_unresolvable_previous_commit_validates():
    """Fail toward spending quota rather than toward shipping unvalidated."""
    def exploded(_prev):
        return True  # _git_gated_code_changed returns this when rev-parse fails

    assert decide(verdict("deadbee", PASS), "c6ee5f7", changed=exploded)[0] is True


def test_a_pass_expires_so_model_drift_is_still_caught():
    """gemini-2.5-flash can change under a pinned name with no commit of ours."""
    stale = NOW + datetime.timedelta(days=7)
    proceed, why = decide(verdict("c6ee5f7", PASS), "c6ee5f7", now=stale)
    assert proceed is True
    assert "drift" in why


def test_a_pass_still_holds_the_day_before_it_expires():
    almost = NOW + datetime.timedelta(days=6)
    assert decide(verdict("c6ee5f7", PASS), "c6ee5f7", now=almost)[0] is False


def test_an_undated_verdict_is_not_trusted():
    assert decide(verdict("c6ee5f7", PASS, when="whenever"), "c6ee5f7")[0] is True


# --- The three states of gate 1 -------------------------------------------
# `get_metadata` fails soft, so a spent quota and a degraded prompt both arrive
# as three empty fields. Calling both FAIL blocks merging a healthy release and
# pages the owner -- the mistake check_screen already refuses to make.

import scripts.validate_release as vr
from src.llm import MetadataResult


def _metadata(monkeypatch, meta):
    monkeypatch.setattr("src.llm.get_metadata", lambda *a, **k: meta)
    return vr.check_metadata()


def test_a_dead_api_is_inconclusive_not_a_failed_release(monkeypatch):
    assert _metadata(monkeypatch, MetadataResult(None, None, None, "error")) is None


def test_gemini_answering_with_junk_is_a_real_failure(monkeypatch):
    """Empty fields when the call itself succeeded means the prompt degraded."""
    assert _metadata(monkeypatch, MetadataResult(None, None, None, "gemini")) is False


def test_a_good_answer_passes(monkeypatch):
    assert _metadata(monkeypatch, MetadataResult(
        "A Rewritten Title", ["a", "b", "c"], "Comment below!", "gemini")) is True


def test_a_title_that_echoes_the_question_fails(monkeypatch):
    """"Worked" is not the same as "produced something usable"."""
    echoed = "What hobby has become too expensive for the average person?"
    assert _metadata(monkeypatch, MetadataResult(
        echoed, ["a", "b", "c"], "Comment below!", "gemini")) is False


def test_an_overlong_title_fails(monkeypatch):
    assert _metadata(monkeypatch, MetadataResult(
        "x" * 101, ["a", "b", "c"], "Comment below!", "gemini")) is False


def test_a_dead_api_does_not_spend_the_screen_replays_five_requests(monkeypatch):
    """The saving is the point: gate 2 costs five of the 20 daily requests, and
    if Gemini is not answering they can only fail the same way as gate 1's one.
    Those five come off the ~05:00 upload, which is last in the daily window."""
    monkeypatch.setenv("GEMINI_API_KEY", "set")
    monkeypatch.setattr(sys, "argv", ["validate_release.py"])
    monkeypatch.setattr(vr, "check_metadata", lambda: None)

    def never(*a, **k):
        raise AssertionError("spent the replay's five requests on a dead API")

    monkeypatch.setattr(vr, "check_screen", never)
    assert vr.main() == 2          # inconclusive, not a failed release


def test_a_reachable_gemini_still_runs_both_gates(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "set")
    monkeypatch.setattr(sys, "argv", ["validate_release.py"])
    monkeypatch.setattr(vr, "check_metadata", lambda: True)
    monkeypatch.setattr(vr, "check_screen", lambda: True)
    assert vr.main() == 0


def test_the_detail_keeps_the_end_of_a_long_transcript(tmp_path):
    """Truncation must keep the verdict, which the gates print last -- keeping
    the head would preserve the preamble and lose the answer."""
    out = tmp_path / "detail.md"
    vr.write_detail(["x" * 4000, "FAIL — do not merge"], path=str(out))
    written = out.read_text()

    assert "FAIL — do not merge" in written
    assert "truncated" in written
    assert len(written) < vr.MAX_DETAIL_CHARS + 200


def test_the_detail_survives_an_unwritable_path(capsys):
    """It is diagnostics, never a reason to fail a release."""
    vr.write_detail(["anything"], path="no/such/dir/detail.md")
    assert "could not write" in capsys.readouterr().err
