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
