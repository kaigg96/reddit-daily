"""The shift trace: the one account of a shift that stopped without a handover
(run 39338110057, 2026-10-19), since the action hides its output and a shift
cannot read Actions logs. It is committed to a public repo, so redaction is
tested as hard as the trace."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import shift_report, shift_trace


def _assistant(*blocks):
    return {"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}}


def _tool(i, name, **args):
    return {"type": "tool_use", "id": f"t{i}", "name": name, "input": args}


def _result(i, text, error=False):
    return {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": f"t{i}", "content": text, "is_error": error}]}}


# The shape of the action's execution output: system, the turns, then a result.
RUN = [
    {"type": "system", "subtype": "init", "model": "claude-opus-5-5"},
    _assistant({"type": "text", "text": "Orienting."},
               _tool(1, "Bash", command="venv/bin/python scripts/statusline.py --budget",
                     description="Check the budget")),
    _result(1, "GO  running in CI"),
    _assistant(_tool(2, "Read", file_path="/repo/PRD.md")),
    _result(2, [{"type": "text", "text": "File does not exist.\nmore"}], error=True),
    _assistant({"type": "text", "text": "Nothing is ready; every item waits on the owner.\nEnding."}),
    {"type": "result", "subtype": "success", "is_error": False, "duration_ms": 134889,
     "num_turns": 32, "total_cost_usd": 1.6, "result": "Nothing is ready; every item waits on the owner.\nEnding."},
]


def test_the_trace_says_how_it_ended_what_it_ran_and_what_failed():
    text = shift_trace.render(*shift_trace.trace(RUN), run_id="39338110057", env={})
    assert text.startswith("## Shift trace — run 39338110057")
    assert "**Ended:** success, is_error false, 32 turns, 2.2 min. **Tool calls:** 2, 1 failed." in text
    assert "> Nothing is ready; every item waits on the owner.\n> Ending." in text
    assert "1. Bash: venv/bin/python scripts/statusline.py --budget" in text
    assert "2. ✗ Read: /repo/PRD.md — File does not exist." in text


def test_a_run_cut_off_before_its_result_says_so():
    ending, final, calls, _ = shift_trace.trace(RUN[:-1])
    assert "did not finish" in ending
    assert final.startswith("Nothing is ready")     # its last words, from the turns
    assert len(calls) == 2


def test_a_long_shift_keeps_its_last_calls_numbered_as_they_ran():
    run = [_assistant(_tool(i, "Bash", command=f"step {i}")) for i in range(1, 101)]
    text = shift_trace.render(*shift_trace.trace(run), env={})
    assert "### Tool calls (last 80 of 100)" in text
    assert "21. Bash: step 21" in text and "20. Bash" not in text


def test_secret_values_and_token_shapes_are_redacted():
    env = {"GEMINI_API_KEY": "plainvalue-no-shape-123"}
    run = [_assistant(_tool(1, "Bash", command="curl -H 'k: plainvalue-no-shape-123' https://x-access-token:ghs_abcdefghijklmnopqrstuvwxyz0123@github.com"),
                      _tool(2, "Bash", command="curl -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload'"),
                      _tool(3, "Bash", command="echo AIzaSyFAKEFAKEFAKEFAKEFAKEFAKEFAKE1 AKIAABCDEFGHIJKLMNOP gsk_abcdefghijklmnopqrstuv")),
           _result(3, "denied for github_pat_11ABCDEFG0123456789_abcdefghij", error=True),
           {"type": "result", "subtype": "success", "result": "token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345 and sk-ant-oat01-secretsecret"}]
    text = shift_trace.render(*shift_trace.trace(run), env=env)
    for leaked in ("plainvalue", "ghs_abc", "eyJhbGci", "AIzaSy", "AKIAAB", "gsk_abc",
                   "github_pat_11", "ghp_ABC", "sk-ant-oat01"):
        assert leaked not in text, leaked


def test_more_token_shapes_and_aws_account_ids_are_redacted():
    env = {"AWS_READONLY_SECRET_ACCESS_KEY": "wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY\n"}
    run = [_assistant(_tool(1, "Bash", command="curl -H 'authorization: bearer abcdefghijklmnopqrstu'"),
                      _tool(2, "Bash", command="echo eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyZXBvOm8vciJ9.c2lnbmF0dXJl"),
                      _tool(3, "Bash", command="aws sts get-caller-identity")),
           _result(1, "AUTHORIZATION: basic eC1hY2Nlc3MtdG9rZW46Z2hzX3h4eA==", error=True),
           _result(3, "User arn:aws:iam::123456789012:user/claude-readonly is denied; key wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY", error=True)]
    text = shift_trace.render(*shift_trace.trace(run), env=env)
    for leaked in ("abcdefghijklmnop", "eyJhbGci", "eC1hY2Nl", "123456789012", "wJalrXUtn"):
        assert leaked not in text, leaked
    assert "arn:aws:iam::***:user/claude-readonly" in text


def test_helper_agents_are_counted_not_listed_and_never_speak_last():
    run = [_assistant({"type": "text", "text": "Starting the review."}, _tool(1, "Agent", description="Rank candidates")),
           {**_assistant({"type": "text", "text": "Helper: here are eight candidates."},
                         _tool(2, "Bash", command="grep -r x")), "parent_tool_use_id": "t1"},
           {**_result(2, "Exit code 2\ngrep: x: No such file", error=True), "parent_tool_use_id": "t1"},
           {"type": "result", "subtype": "error_max_turns", "is_error": True, "num_turns": 900,
            "duration_ms": 60000, "errors": ["Reached maximum number of turns (900)"],
            "permission_denials": [{"tool_name": "WebFetch"}]}]
    ending, final, calls, helper = shift_trace.trace(run)
    assert final == "Starting the review."              # the shift's own words, not the helper's
    assert [c[0] for c in calls] == ["Agent"] and helper == (1, 1)
    assert "error_max_turns" in ending and "Reached maximum number of turns (900)" in ending
    assert "1 permission denial(s): WebFetch" in ending
    text = shift_trace.render(ending, final, calls, helper, env={})
    assert "Helper agents made 1 more, 1 failed." in text and "grep -r x" not in text


def test_a_failed_command_shows_its_message_not_only_its_exit_code():
    run = [_assistant(_tool(1, "Bash", command="venv/bin/python -m pytest")),
           _result(1, "Exit code 1\n\nImportError: cannot import name 'x'", error=True)]
    text = shift_trace.render(*shift_trace.trace(run), env={})
    assert "✗ Bash: venv/bin/python -m pytest — Exit code 1: ImportError: cannot import name 'x'" in text


def test_a_dotted_github_token_is_redacted_whole():
    # The shape of the workflow token the agent holds (2026-10-28): segments of
    # 5, 36, 243, 21 and 64 characters after `ghs_`, joined by dots and underscores.
    parts = ["Ab3dE", "B" * 36, "C" * 243, "D" * 21, "E" * 64]
    token = "ghs_" + parts[0] + "." + parts[1] + "." + parts[2] + "_" + parts[3] + "." + parts[4]
    run = [_assistant(_tool(1, "Bash", command="echo " + token[:100])),
           {"type": "result", "subtype": "success", "result": "it printed " + token + "."}]
    text = shift_trace.render(*shift_trace.trace(run), env={})
    assert "ghs_" not in text
    for part in parts:
        assert part[:5] not in text, part[:5]


def test_a_token_cut_by_the_line_limit_leaves_no_prefix():
    token = "ghp_" + "A" * 36
    run = [_assistant(_tool(1, "Bash", command="x" * 125 + " " + token))]
    text = shift_trace.render(*shift_trace.trace(run), env={})
    assert "ghp_" not in text and "AAAA" not in text


def test_every_output_format_the_action_has_written_loads(tmp_path):
    for name, raw in (("array", json.dumps(RUN)), ("object", json.dumps(RUN[-1])),
                      ("stream", "\n".join(json.dumps(m) for m in RUN))):
        p = tmp_path / f"{name}.json"
        p.write_text(raw)
        assert shift_trace.load(str(p))[-1]["type"] == "result", name


def test_a_missing_or_unreadable_output_still_writes_a_trace_and_never_fails_the_job(tmp_path, capsys):
    out = tmp_path / "trace.md"
    assert shift_trace.main([str(tmp_path / "missing.json"), "--write", str(out), "--run-id", "7"]) == 0
    assert out.read_text().startswith("## Shift trace — run 7")
    assert "no execution output: the agent did not finish" in out.read_text()   # killed or cancelled
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert shift_trace.main([str(bad), "--write", str(out)]) == 0
    assert "could not be read" in out.read_text()


def test_the_summary_stops_before_the_tool_list_and_ignores_another_runs_trace(tmp_path):
    p = tmp_path / "trace.md"
    p.write_text(shift_trace.render(*shift_trace.trace(RUN), run_id="5", env={}))
    head = shift_trace.summary(str(p), "5")
    assert "**Ended:** success" in head and "Tool calls (" not in head and "statusline" not in head
    assert shift_trace.summary(str(p), "6") == ""
    assert shift_trace.summary(str(tmp_path / "none.md"), "5") == ""


# --- the emailed report -----------------------------------------------------

def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / ".github").mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "WORKLOG.md").write_text("# Work log\n\n## 2026-10-19 (18:25) — an earlier shift\n\n**Summary:** Old news.\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "earlier handover")
    return repo, _git(repo, "rev-parse", "HEAD")


def test_a_shift_without_a_handover_is_reported_as_one_not_as_the_last(tmp_path, monkeypatch):
    repo, start = _repo(tmp_path)
    (repo / shift_trace.TRACE).write_text(shift_trace.render(*shift_trace.trace(RUN), run_id="9", env={}))
    monkeypatch.chdir(repo)
    monkeypatch.setenv("GITHUB_RUN_ID", "9")
    body = shift_report.build("WORKLOG.md", str(tmp_path / "no-ledger.csv"), start, "https://run")
    assert body.startswith("## This shift wrote no handover")
    assert "Old news" not in body and "an earlier shift" not in body
    assert "> Nothing is ready; every item waits on the owner." in body
    assert "statusline" not in body                  # the tool list stays in the file
    assert body.rstrip().endswith("*[Full log](https://run)*")


def test_without_a_trace_for_this_run_it_says_so(tmp_path, monkeypatch):
    repo, start = _repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.setenv("GITHUB_RUN_ID", "9")
    assert "No trace was recorded for this run." in shift_report.build("WORKLOG.md", "x.csv", start)


def test_a_shift_that_handed_over_is_reported_from_its_entry(tmp_path, monkeypatch):
    repo, start = _repo(tmp_path)
    worklog = repo / "WORKLOG.md"
    worklog.write_text(worklog.read_text().replace(
        "# Work log\n", "# Work log\n\n## 2026-10-20 (09:00) — this shift\n\n**Summary:** New news.\n"))
    _git(repo, "commit", "-qam", "handover")
    monkeypatch.chdir(repo)
    body = shift_report.build("WORKLOG.md", "x.csv", start)
    assert body.startswith("## 2026-10-20 (09:00) — this shift") and "New news." in body
    # Written but not yet committed counts too, as in the workflow's check.
    _, start = _repo(tmp_path / "b")
    monkeypatch.chdir(tmp_path / "b" / "repo")
    (tmp_path / "b" / "repo" / "WORKLOG.md").write_text("# Work log\n\n## 2026-10-20 — uncommitted\n")
    assert shift_report.build("WORKLOG.md", "x.csv", start).startswith("## 2026-10-20 — uncommitted")


def test_no_start_sha_reports_the_entry_as_before(tmp_path, monkeypatch):
    repo, _ = _repo(tmp_path)
    monkeypatch.chdir(repo)
    assert shift_report.build("WORKLOG.md", "x.csv", "").startswith("## 2026-10-19 (18:25)")
