"""The pre-push gate refuses a push that would publish a secret, a private
identifier or a personal commit address, and only such a push.

Every value these tests plant is built at run time, so this file never holds
what the gate (or CI's gitleaks scan) looks for."""
import io
import json
import os
import re
import stat
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import prepush_check as gate  # noqa: E402
from scripts import shift_trace  # noqa: E402

NOREPLY = "1+tester@users.noreply.github.com"
PERSON = "jo.smith" + "@" + "mail.co"
ACCOUNT = "4" * 12
HELD = "s3cr3t-" + "value-0123456789"


@pytest.fixture(autouse=True)
def _hermetic_git(tmp_path, monkeypatch):
    """No global or system git config: this machine's identity, hooks and
    signing settings must not leak into, or break, the repos made here."""
    cfg = tmp_path / "gitconfig"
    cfg.write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(cfg))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for var in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL", "GIT_DIR", "GIT_WORK_TREE"):
        monkeypatch.delenv(var, raising=False)


def _git(cwd, *args, env=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True, env={**os.environ, **(env or {})}).stdout


def _commit(work, path, text, message="change", author=NOREPLY, committer=NOREPLY):
    full = work / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(text)
    _git(work, "add", path)
    _git(work, "commit", "-q", "-m", message,
         env={"GIT_AUTHOR_EMAIL": author, "GIT_COMMITTER_EMAIL": committer})
    return _git(work, "rev-parse", "HEAD").strip()


@pytest.fixture
def work(tmp_path):
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", str(remote))
    w = tmp_path / "work"
    _git(tmp_path, "init", "-q", "-b", "main", str(w))
    _git(w, "config", "user.name", "tester")
    _git(w, "config", "user.email", NOREPLY)
    _git(w, "remote", "add", "origin", str(remote))
    _commit(w, "README.md", "hello\n", "base")
    _git(w, "push", "-q", "origin", "main")
    return w


def _problems(work, values=None, shapes=True):
    return gate.check([["origin/main..HEAD"]], {} if values is None else values,
                      cwd=str(work), shapes=shapes)


def _rules(problems):
    return sorted(p.rule for p in problems)


def test_a_clean_push_passes(work):
    _commit(work, "src/a.py", "x = 1\n# mail noreply@github.com or git@github.com\n")
    assert _problems(work, {HELD: ".env GEMINI_API_KEY"}) == []


@pytest.mark.parametrize("author, committer, rule", [
    (PERSON, NOREPLY, "author is not a noreply address"),
    (NOREPLY, PERSON, "committer is not a noreply address"),
], ids=["author", "committer"])
def test_a_personal_commit_address_is_refused(work, author, committer, rule):
    _commit(work, "a.txt", "fine\n", author=author, committer=committer)
    assert _rules(_problems(work)) == [rule]


def test_a_held_value_is_refused_in_a_diff_and_never_printed(work, capsys):
    _commit(work, "src/config.py", f"KEY = '{HELD}'\n")
    problems = _problems(work, {HELD: ".env GEMINI_API_KEY"})
    assert [(p.where, p.rule) for p in problems] == [("src/config.py:1", ".env GEMINI_API_KEY")]
    gate.report(problems, out=sys.stdout)
    out = capsys.readouterr().out
    assert "GEMINI_API_KEY" in out and HELD not in out


def test_a_held_value_is_refused_in_a_commit_message(work):
    _commit(work, "a.txt", "fine\n", message=f"debug: token was {HELD}")
    assert [(p.where, p.rule) for p in _problems(work, {HELD: "environment variable GH_TOKEN"})] == [
        ("commit message", "environment variable GH_TOKEN")]


def test_a_value_added_then_removed_before_the_push_is_still_refused(work):
    # The net diff is clean, but history publishes the commit that added it.
    _commit(work, "a.txt", f"{HELD}\n")
    _commit(work, "a.txt", "gone\n")
    assert _rules(_problems(work, {HELD: ".env X"})) == [".env X"]


def test_values_compare_case_insensitively(work):
    _commit(work, "a.txt", HELD.upper() + "\n")
    assert _rules(_problems(work, {HELD: ".env X"})) == [".env X"]


def test_a_private_address_is_refused_but_noreply_and_example_ones_pass(work):
    fine = ["a" + "@" + "example.com", "b" + "@" + "x.example.org", "c" + "@" + "host.invalid",
            "no-reply" + "@" + "corp.com", NOREPLY]
    _commit(work, "docs.md", "\n".join(fine) + "\n")
    assert _problems(work) == []
    _commit(work, "docs.md", "\n".join(fine) + f"\nwrite to {PERSON}\n")
    assert [(p.where, p.rule) for p in _problems(work)] == [("docs.md:6", "private-email")]


def test_a_decorator_on_a_quoted_diff_line_is_not_an_address(work):
    _commit(work, "notes.md", "+" + "@" + "pytest.mark.parametrize\n")
    assert _problems(work) == []


@pytest.mark.parametrize("line", [
    "arn:aws:iam::" + ACCOUNT + ":user/reader",
    "account id: " + ACCOUNT,
    '{"Account": "' + ACCOUNT + '"}',
], ids=["arn", "named", "json"])
def test_an_aws_account_id_is_refused(work, line):
    _commit(work, "t.py", line + "\n")
    assert _rules(_problems(work)) == ["aws-account-id"]


def test_aws_placeholder_ids_pass(work):
    _commit(work, "t.py", "arn:aws:iam::" + "123456789012" + ":user/x\naccount id: " + "0" * 12 + "\n")
    assert _problems(work) == []


def test_a_credential_shape_is_refused_except_in_the_redactor_fixtures(work):
    key = "AK" + "IA" + "Q" * 16
    _commit(work, "tests/test_shift_trace.py", f"FIXTURE = '{key}'\n")
    assert _problems(work) == []
    _commit(work, "src/aws.py", f"KEY = '{key}'\n")
    assert [(p.where, p.rule) for p in _problems(work)] == [("src/aws.py:1", "credential shape")]
    # gitleaks, when it runs, does the shape check instead.
    assert _problems(work, shapes=False) == []


def test_only_what_the_push_adds_is_checked(work):
    _commit(work, "old.md", f"{PERSON}\nline two\n")
    _git(work, "push", "-q", "origin", "main")     # already public: not this push's doing
    _commit(work, "old.md", f"{PERSON}\nline 2\n")
    assert _problems(work) == []


def test_hook_input_becomes_one_range_per_pushed_ref(work):
    base = _git(work, "rev-parse", "HEAD").strip()
    _git(work, "checkout", "-q", "-b", "topic")
    new = _commit(work, "b.txt", "b\n")
    zero = "0" * 40
    lines = [f"refs/heads/topic {new} refs/heads/topic {zero}",       # a new branch
             f"refs/heads/main {new} refs/heads/main {base}",         # an update
             f"(delete) {zero} refs/heads/gone {base}",               # a deletion
             "garbage"]
    ranges = gate.ranges_from_hook(lines, "origin", cwd=str(work))
    assert ranges == [[new, "--not", "--remotes=origin"], [f"{base}..{new}"]]
    # A remote given as a URL (no remote name): every remote ref counts as public.
    assert gate.ranges_from_hook(lines[:1], "https://example.invalid/r.git", cwd=str(work)) == [
        [new, "--not", "--remotes"]]
    shas = [c[0] for r in ranges for c in gate.commits(r, cwd=str(work))]
    assert shas == [new, new]          # the base commit is already public


def test_held_values_come_from_every_place_a_secret_lives(tmp_path):
    top = tmp_path / "checkout"
    top.mkdir()
    (top / ".env").write_text(f"# comment\nexport GEMINI_API_KEY=\"{HELD}\"\nSHORT=abc\n")
    (top / "client_secret.json").write_text(json.dumps(
        {"installed": {"client_id": "id-" + "1" * 20, "client_secret": "cs-" + "2" * 20,
                       "redirect_uris": ["http://localhost"]}}))
    home = tmp_path / "home"
    (home / ".aws").mkdir(parents=True)
    (home / ".aws" / "credentials").write_text(
        f"[{'9' * 12}_admin]\naws_access_key_id = {'K' * 20}\naws_secret_access_key = {'s' * 40}\n")
    common = tmp_path / "gitdir"
    (common / "info").mkdir(parents=True)
    (common / "info" / "private-values").write_text("# the owner\nSurname-Here\n\n")
    env = {"GROQ_API_KEY": "g" * 30, "MY_SERVICE_TOKEN": "t" * 30, "PATH": "/usr/bin:/bin:/x/y/z",
           "GIT_ASKPASS": "/some/askpass/helper"}
    vals = gate.held_values(env=env, home=str(home), tops=[str(top)], common=str(common),
                            global_email=PERSON)
    labels = set(vals.values())
    assert {".env GEMINI_API_KEY", "client_secret.json client_id", "client_secret.json client_secret",
            "~/.aws/credentials aws_access_key_id", "~/.aws/credentials aws_secret_access_key",
            "an AWS account ID named in ~/.aws/credentials", "line 2 of .git/info/private-values",
            "environment variable GROQ_API_KEY", "environment variable MY_SERVICE_TOKEN",
            "your global git user.email"} == labels
    assert HELD in vals and "abc" not in vals and "/usr/bin:/bin:/x/y/z" not in vals
    # A noreply global address is not private; a personal one is (above).
    assert NOREPLY not in gate.held_values(env={}, home=str(tmp_path), global_email=NOREPLY)


@pytest.mark.parametrize("command", [
    "git push --no-verify",
    "git push origin topic --no-verify",
    "cd x && git -c core.hooksPath=/dev/null push",
    "git config core.hooksPath /dev/null",
    "git config --global core.hooksPath ~/elsewhere",
    "git config --unset core.hooksPath",
    "git config --local --unset-all core.hooksPath",
    "GIT_CONFIG_PARAMETERS=\"'core.hooksPath=/tmp'\" git push",
])
def test_the_guard_refuses_switching_the_gate_off(command):
    assert gate.refusal(command)


@pytest.mark.parametrize("command", [
    "git push",
    "git push -u origin security/pre-push-gate",
    "git config core.hooksPath",
    "git config --get core.hooksPath",
    "grep -rn core.hooksPath scripts/",
    "cat .git/config | grep core.hooksPath",
    "git commit -m 'explain why --no-verify is refused'",
    "python3 scripts/prepush_check.py install --check",
])
def test_the_guard_lets_everything_else_through(command):
    assert gate.refusal(command) is None


def test_the_guard_speaks_claude_codes_hook_protocol(monkeypatch, capsys):
    call = {"tool_name": "Bash", "tool_input": {"command": "git push --no-verify"}}
    assert gate.guard(io.StringIO(json.dumps(call))) == 2         # 2 blocks the call
    assert "--no-verify" in capsys.readouterr().err
    assert gate.guard(io.StringIO(json.dumps({**call, "tool_input": {"command": "ls"}}))) == 0
    assert gate.guard(io.StringIO(json.dumps({"tool_name": "Read", "tool_input": {}}))) == 0
    assert gate.guard(io.StringIO("not json")) == 0


def test_install_points_git_at_the_hooks_and_check_reports_it(work, capsys):
    assert gate.install(check_only=True, cwd=str(work)) == 1
    assert gate.install(cwd=str(work)) == 0
    assert _git(work, "config", "core.hooksPath").strip() == ".githooks"
    assert gate.install(check_only=True, cwd=str(work)) == 0
    assert "installed" in capsys.readouterr().out


def test_a_real_git_push_runs_the_gate(work):
    # The shim finds the script beside itself, so point git at this checkout's.
    _git(work, "config", "core.hooksPath", os.path.join(ROOT, ".githooks"))
    _commit(work, "ok.txt", "fine\n")
    _git(work, "push", "-q", "origin", "main")
    _commit(work, "bad.txt", f"reach me at {PERSON}\n")
    r = subprocess.run(["git", "push", "-q", "origin", "main"], cwd=work, capture_output=True, text=True)
    assert r.returncode != 0
    assert "private-email" in r.stderr and PERSON not in r.stderr
    remote_head = _git(work, "ls-remote", "origin", "main").split()[0]
    assert remote_head != _git(work, "rev-parse", "HEAD").strip()


def test_the_hook_files_are_wired():
    shim = os.path.join(ROOT, ".githooks", "pre-push")
    assert os.stat(shim).st_mode & stat.S_IXUSR, "git ignores a hook that is not executable"
    with open(os.path.join(ROOT, ".claude", "settings.json")) as f:
        hooks = json.load(f)["hooks"]
    commands = [h["command"] for e in hooks["SessionStart"] for h in e["hooks"]]
    assert any(c.endswith("prepush_check.py\" install") for c in commands)
    guards = [h["command"] for e in hooks["PreToolUse"] if e.get("matcher") == "Bash" for h in e["hooks"]]
    assert any(c.endswith("prepush_check.py\" guard") for c in guards)


def _toml_rule(rules, rule_id):
    return next(r for r in rules if r["id"] == rule_id)


def test_the_rules_match_ci_s_gitleaks_config():
    """One rule set: CI applies .github/workflows/gitleaks.toml, the gate and the
    trace redactor apply shift_trace's copy. Python 3.10 has no tomllib, so this
    runs in CI (3.12) and skips locally."""
    tomllib = pytest.importorskip("tomllib")
    path = os.path.join(ROOT, gate.GITLEAKS_CONFIG)
    if not os.path.exists(path):
        pytest.skip("gitleaks.toml has not landed yet")
    with open(path, "rb") as f:
        rules = tomllib.load(f)["rules"]
    email = _toml_rule(rules, "private-email")
    assert email["regex"] == shift_trace.PRIVATE_EMAIL
    assert {x for a in email["allowlists"] for x in a["regexes"]} == set(shift_trace.NOT_A_PERSON)
    account = _toml_rule(rules, "aws-account-id")
    assert account["regex"] == shift_trace.AWS_ACCOUNT_ID
    assert {x for a in account["allowlists"] for x in a["regexes"]} == set(shift_trace.PLACEHOLDER_ACCOUNTS)


def test_the_gate_never_flags_its_own_source():
    for path in ("scripts/prepush_check.py", "scripts/shift_trace.py", "tests/test_prepush_check.py",
                 ".githooks/pre-push", ".claude/settings.json"):
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            text = f.read()
        assert gate._rules(text, {}, shapes=True) == [], path
