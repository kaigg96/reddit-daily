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
    # Nor this machine's ~/.aws: a hook a test runs reads HOME.
    (tmp_path / "home").mkdir()
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    for var in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL", "GIT_DIR", "GIT_WORK_TREE"):
        monkeypatch.delenv(var, raising=False)


def _git(cwd, *args, env=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True, env={**os.environ, **(env or {})}).stdout


def _commit(work, path, text, message="change", author=NOREPLY, committer=NOREPLY, name="tester"):
    full = work / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_bytes(text) if isinstance(text, bytes) else full.write_text(text)
    _git(work, "add", path)
    _git(work, "commit", "-q", "-m", message,
         env={"GIT_AUTHOR_EMAIL": author, "GIT_COMMITTER_EMAIL": committer, "GIT_AUTHOR_NAME": name})
    return _git(work, "rev-parse", "HEAD").strip()


def _push(work, *args):
    return subprocess.run(["git", "push", "-q", *args], cwd=work, capture_output=True, text=True)


def _gate_on(work):
    # The shim finds the script beside itself, so point git at this checkout's.
    _git(work, "config", "core.hooksPath", os.path.join(ROOT, ".githooks"))


def _public(work, branch):
    """Push without the gate: history that was public before it existed."""
    _git(work, "-c", "core.hooksPath=/dev/null", "push", "-q", "origin", branch)


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
    assert ranges == [[new, "--not", "--remotes=origin"], [new, "--not", base, "--remotes=origin"]]
    # A remote given as a URL is the configured remote with that URL; an
    # unknown one falls back to every remote's refs.
    url = _git(work, "remote", "get-url", "origin").strip()
    assert gate.ranges_from_hook(lines[:1], url, cwd=str(work)) == [[new, "--not", "--remotes=origin"]]
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
    (home / ".aws" / "config").write_text(
        f"[profile reader]\nrole_arn = arn:aws:iam::{'7' * 12}:role/r\nsso_account_id = {'8' * 12}\n")
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
            "an AWS account ID in ~/.aws/credentials", "an AWS account ID in ~/.aws/config",
            "line 2 of .git/info/private-values",
            "environment variable GROQ_API_KEY", "environment variable MY_SERVICE_TOKEN",
            "your global git user.email"} == labels
    assert HELD in vals and "abc" not in vals and "/usr/bin:/bin:/x/y/z" not in vals
    assert "7" * 12 in vals and "8" * 12 in vals
    # A noreply global address is not private; a personal one is (above).
    assert NOREPLY not in gate.held_values(env={}, home=str(tmp_path), global_email=NOREPLY)


def test_a_name_carrying_a_held_value_is_refused(work):
    _commit(work, "a.txt", "fine\n", name="Jo " + HELD)
    assert [(p.where, p.rule) for p in _problems(work, {HELD: "line 1 of .git/info/private-values"})] == [
        ("commit metadata", "author name: line 1 of .git/info/private-values")]


def test_a_credential_in_a_message_is_refused_even_when_gitleaks_runs(work):
    # gitleaks reads patches, never messages, so the shapes check them always.
    _commit(work, "a.txt", "fine\n", message="debug " + "AK" + "IA" + "Q" * 16)
    assert [(p.where, p.rule) for p in _problems(work, shapes=False)] == [
        ("commit message", "credential shape")]


def test_a_flagged_path_is_refused_and_never_printed(work, capsys):
    _commit(work, f"notes-{PERSON}.md", f"write to {PERSON}\n")
    problems = _problems(work)
    assert [(p.where, p.rule) for p in problems] == [
        ("a file path", "private-email"), (gate.WITHHELD, "private-email")]
    gate.report(problems, out=sys.stdout)
    assert PERSON not in capsys.readouterr().out


def test_a_content_line_shaped_like_a_diff_header_is_content(work):
    # "++ b/x" shows in the patch as "+++ b/x": the hunk's counts say it is content.
    _commit(work, "a.md", f"++ b/elsewhere\n{PERSON}\n")
    assert [(p.where, p.rule) for p in _problems(work)] == [("a.md:2", "private-email")]


def test_a_binary_file_is_read_whole_for_held_values_and_credentials(work):
    key = "AK" + "IA" + "Q" * 16
    _commit(work, "Q and A.bin", b"\x00\x01\x02 " + HELD.encode() + b" \x00\xff")
    _commit(work, 'say "hi".bin', b"\x00 " + key.encode() + b" \x00")
    assert sorted((p.where, p.rule) for p in _problems(work, {HELD: ".env X"})) == [
        ("Q and A.bin (binary)", ".env X"), ('say "hi".bin (binary)', "credential shape")]


def test_a_binary_file_is_not_held_to_the_address_patterns(work):
    # Compressed media matches them by chance (a committed mp3 does), and a
    # refusal nothing can clear is worse than the owner's own values alone.
    _commit(work, "music.bin", b"\x00\x01 " + PERSON.encode() + b" account id: " + ACCOUNT.encode() + b"\x00")
    assert _problems(work) == []


def test_utf16_text_which_git_calls_binary_is_read(work):
    _commit(work, "notes.txt", f"key {HELD}\n".encode("utf-16"))
    assert [(p.where, p.rule) for p in _problems(work, {HELD: ".env X"})] == [("notes.txt (binary)", ".env X")]


@pytest.mark.parametrize("text", [
    "progress 10%\rdone {held}\n",
    "a\x0c{held}\n",
    "a\x1e{held}\n",
    "x\r+y\n{held}\n",
], ids=["carriage-return", "form-feed", "record-separator", "cr-then-plus"])
def test_a_line_break_python_knows_and_git_does_not_hides_nothing(work, text):
    _commit(work, "trace.md", text.format(held=HELD))
    assert _rules(_problems(work, {HELD: ".env X"})) == [".env X"]


def test_this_machines_diff_config_cannot_hide_added_lines(work):
    """Each of these once hid something from the parser: merged hunks with
    context, no a/ b/ prefixes, a textconv driver, a hidden root commit."""
    _commit(work, "long.txt", "".join(f"line {i}\n" for i in range(20)))
    _git(work, "push", "-q", "origin", "main")
    for key, value in (("diff.interHunkContext", "5"), ("diff.noprefix", "true"),
                       ("diff.rev.textconv", "rev"), ("log.showRoot", "false")):
        _git(work, "config", key, value)
    (work / ".gitattributes").write_text("*.dat diff=rev\n")
    (work / "long.txt").write_text("".join(f"line {i}{' changed' if i in (2, 6) else ''}\n" for i in range(20)))
    (work / "x.dat").write_text(f"{HELD}\n")
    (work / "zz.bin").write_bytes(b"\x00" + HELD.encode())
    (work / f"empty-{HELD}").write_text("")
    _git(work, "add", "-A")
    _git(work, "commit", "-q", "-m", "change", env={"GIT_AUTHOR_EMAIL": NOREPLY, "GIT_COMMITTER_EMAIL": NOREPLY})
    where = sorted({p.where for p in _problems(work, {HELD: ".env X"})})
    assert where == sorted(["a file path", "x.dat:1", "zz.bin (binary)"])
    # A root commit, with log.showRoot off.
    root = work.parent / "root"
    _git(work.parent, "init", "-q", "-b", "main", str(root))
    _git(root, "config", "user.name", "tester")
    _git(root, "config", "log.showRoot", "false")
    _commit(root, "a.txt", f"{HELD}\n")
    assert _rules(gate.check([["HEAD"]], {HELD: ".env X"}, cwd=str(root))) == [".env X"]


def test_a_merge_gets_the_credential_shapes_even_when_gitleaks_runs(work):
    # gitleaks reads no merge diffs, so what a merge adds is the gate's.
    _git(work, "checkout", "-q", "-b", "side")
    _commit(work, "side.txt", "side\n")
    _git(work, "checkout", "-q", "main")
    _git(work, "merge", "-q", "--no-ff", "--no-commit", "side")
    (work / "evil.py").write_text("KEY = '" + "AK" + "IA" + "Q" * 16 + "'\n")
    _git(work, "add", "evil.py")
    _git(work, "commit", "-q", "--no-edit")
    assert [(p.where, p.rule) for p in _problems(work, shapes=False)] == [("evil.py:1", "credential shape")]


def test_an_octopus_merge_is_refused(work):
    # git shows nothing for one, so what it adds cannot be checked.
    for b in ("b1", "b2"):
        _git(work, "checkout", "-q", "-b", b, "main")
        _commit(work, f"{b}.txt", f"{b}\n")
    _git(work, "checkout", "-q", "main")
    _git(work, "merge", "-q", "--no-ff", "--no-edit", "b1", "b2")
    assert [p.rule for p in _problems(work)] == [
        "an octopus merge, which git cannot show what it adds: merge one branch at a time"]


def test_a_name_with_a_space_is_reported_once_and_plainly(work):
    _commit(work, "my notes.txt", f"{PERSON}\n")
    assert [(p.where, p.rule) for p in _problems(work)] == [("my notes.txt:1", "private-email")]


def test_an_old_git_is_refused_plainly(work, monkeypatch, capsys):
    monkeypatch.setattr(gate, "_git_version", lambda cwd=None: (2, 35))
    assert gate.run([["HEAD"]], cwd=str(work), values={}) == 1
    assert "needs git 2.36" in capsys.readouterr().err


def test_an_annotated_tag_is_checked(work):
    zero = "0" * 40
    _git(work, "tag", "-a", "v1", "-m", f"release, ask {PERSON}", env={"GIT_COMMITTER_EMAIL": PERSON})
    tag = _git(work, "rev-parse", "v1").strip()
    lines = [f"refs/tags/v1 {tag} refs/tags/v1 {zero}"]
    assert gate.pushed_tags(lines, cwd=str(work)) == [tag]
    assert _rules(gate.check_tags([tag], {}, cwd=str(work))) == [
        "private-email", "tagger is not a noreply address"]
    _git(work, "tag", "-a", "v2", "-m", "release", env={"GIT_COMMITTER_EMAIL": NOREPLY})
    assert gate.check_tags([_git(work, "rev-parse", "v2").strip()], {}, cwd=str(work)) == []
    # The commit it points at is public already: only the tag object is new.
    assert [c.sha for r in gate.ranges_from_hook(lines, "origin", cwd=str(work))
            for c in gate.commits(r, cwd=str(work))] == []


def test_a_pushed_ref_name_is_checked():
    sha, zero = "1" * 40, "0" * 40
    assert gate.check_refs([f"refs/heads/x {sha} refs/heads/{PERSON} {zero}"], {}) == [
        gate.Problem("-", "a pushed ref's name", "private-email")]
    assert gate.check_refs([f"refs/heads/x {sha} refs/heads/topic {zero}"], {}) == []


def test_rebasing_or_merging_main_into_a_pushed_branch_rechecks_nothing_public(work):
    """main carries history from before the gate (personal addresses among it).
    A branch rebased onto it, or merged with it, publishes only its own commits."""
    _gate_on(work)
    _git(work, "checkout", "-q", "-b", "topic")
    _commit(work, "t.txt", "t\n")
    assert _push(work, "-u", "origin", "topic").returncode == 0
    _git(work, "checkout", "-q", "main")
    _commit(work, "contact.md", f"{PERSON}\n", author=PERSON)
    _public(work, "main")
    _git(work, "checkout", "-q", "topic")
    _git(work, "rebase", "-q", "main")
    r = _push(work, "--force", "origin", "topic")
    assert r.returncode == 0, r.stderr
    _git(work, "checkout", "-q", "main")
    _commit(work, "contact2.md", f"{PERSON}\n", author=PERSON)
    _public(work, "main")
    _git(work, "checkout", "-q", "topic")
    _git(work, "merge", "-q", "--no-ff", "--no-edit", "main")
    r = _push(work, "origin", "topic")
    assert r.returncode == 0, r.stderr
    # What a merge adds of its own is still its own.
    _git(work, "checkout", "-q", "main")
    _commit(work, "c3.md", "three\n")
    _public(work, "main")
    _git(work, "checkout", "-q", "topic")
    _git(work, "merge", "-q", "--no-ff", "--no-commit", "main")
    (work / "evil.md").write_text(f"{PERSON}\n")
    _git(work, "add", "evil.md")
    _git(work, "commit", "-q", "--no-edit")
    r = _push(work, "origin", "topic")
    assert r.returncode != 0 and "evil.md:1  private-email" in r.stderr and PERSON not in r.stderr


@pytest.mark.parametrize("command", [
    "git push --no-verify",
    "git push origin topic --no-verify",
    "git push --no-veri",
    "cd x && git -c core.hooksPath=/dev/null push",
    "git -c 'core.hooksPath=/dev/null' push",
    'git -c "core.hookspath=" push',
    "git --config-env=core.hooksPath=HOOKS push",
    "git -C sub push --no-verify",
    "env git push --no-verify",
    "env -u FOO git push --no-verify",
    "command git push --no-verify",
    "/usr/bin/git push --no-verify",
    "sh -c 'git push --no-verify'",
    "echo start $(git push --no-verify)",
    "cd x\ngit push --no-verify",
    "git config core.hooksPath /dev/null",
    "git config --global core.hooksPath ~/elsewhere",
    "git config --unset core.hooksPath",
    "git config --local --unset-all core.hooksPath",
    "git config set core.hooksPath /x",
    "git config unset core.hooksPath",
    "GIT_CONFIG_PARAMETERS=\"'core.hooksPath=/tmp'\" git push",
    "export GIT_CONFIG_PARAMETERS=\"'core.hooksPath=/tmp'\"",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/x git push",
    # Shell keywords and wrappers in front of the command.
    "if git push --no-verify; then echo ok; fi",
    "if ! git push --no-verify; then exit 1; fi",
    "for i in 1 2 3; do git push --no-verify && break; done",
    "until git push --no-verify; do sleep 1; done",
    "{ git push --no-verify; }",
    "! git push --no-verify",
    "case x in a) git push --no-verify;; esac",
    "timeout 120 git push --no-verify",
    "stdbuf -oL git push --no-verify",
    "echo main | xargs git push --no-verify origin",
    "bash -lc 'git push --no-verify'",
    "sh -ec 'git push --no-verify'",
    # A substitution runs, in double quotes too.
    'out="$(git push --no-verify 2>&1)"',
    'echo "`git push --no-verify`"',
    # Quoting a heredoc or $'…' must not swallow a real command after it.
    "cat <<'END-NOTES'\nnotes\nEND-NOTES\ngit push --no-verify",
    "git commit -m \"$(cat <<'EOF'\nsay \"hi\nEOF\n)\" && git push --no-verify",
    "echo $'it\\'s' && git push --no-verify",
])
def test_the_guard_refuses_switching_the_gate_off(command):
    assert gate.refusal(command)


@pytest.mark.parametrize("command", [
    "git push",
    "git push -u origin security/pre-push-gate",
    "git push -n",
    "git config core.hooksPath",
    "git config --get core.hooksPath",
    "git config core.hooksPath .githooks",
    "grep -rn core.hooksPath scripts/",
    "cat .git/config | grep core.hooksPath",
    "git commit -m 'explain why --no-verify is refused'",
    'git commit -m "Pre-push gate: refuse git push --no-verify"',
    'git commit --no-verify -m "push it"',
    'gh pr create --body "never git push --no-verify"',
    "echo 'git push --no-verify'",
    "git push  # never with --no-verify",
    "cat >> WORKLOG.md <<'EOF'\nNever git push --no-verify.\ngit config core.hooksPath /dev/null\nEOF\ngit status",
    "git commit -q -F - <<EOF\nwhy git push --no-verify is refused\nEOF",
    "git commit -m \"$(cat <<'EOF'\nGate: git push --no-verify is refused\nEOF\n)\"",
    "python3 scripts/prepush_check.py install --check",
    "cat <<'END-NOTES'\ngit push --no-verify\nEND-NOTES",
    "cat <<\\EOF\ngit push --no-verify\nEOF",
    "cat <<-EOF\n\tgit push --no-verify\n\tEOF\ngit status",
    "git commit -m \"$(cat <<'EOF'\nsay \"hi; git push --no-verify\nEOF\n)\"",
    "echo $((1 + 2)) && git push",
    "python3 -c \"print('git push --no-verify')\"",
    "for f in a b; do echo \"$f\"; done",
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
    # Malformed input is not a command: never an exception (Claude Code would
    # run the call anyway, having learnt nothing).
    assert gate.guard(io.StringIO("[1]")) == 0
    assert gate.guard(io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": {"command": 5}}))) == 0
    assert gate.guard(io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": "x"}))) == 0


def test_the_guard_never_raises_or_hangs_on_shell_like_noise():
    import random
    import time
    rng = random.Random(7)
    alphabet = ["git", " push", " --no-verify", "'", '"', "`", "$(", "$'", ")", "(", "\\", "\n", ";",
                "&&", "|", "<<", "EOF", "<<-", "#", " ", "x", "\t", "{", "}", "$((", "-c", "bash"]
    start = time.time()
    for _ in range(3000):
        gate.refusal("".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40))))
    gate.refusal("$(" * 5000)
    gate.refusal("`" * 5000)
    assert time.time() - start < 20


def test_install_points_git_at_the_hooks_and_check_needs_the_hook_itself(work, capsys):
    assert gate.install(check_only=True, cwd=str(work)) == 1
    assert gate.install(cwd=str(work)) == 0
    assert _git(work, "config", "core.hooksPath").strip() == ".githooks"
    # The setting is shared by every worktree; one whose branch predates the
    # gate has no hook to run, so the check must not call it installed.
    assert gate.install(check_only=True, cwd=str(work)) == 1
    assert "no executable .githooks/pre-push" in capsys.readouterr().out
    hook = work / ".githooks" / "pre-push"
    hook.parent.mkdir()
    hook.write_text("#!/bin/sh\n")
    hook.chmod(0o755)
    assert gate.install(check_only=True, cwd=str(work)) == 0
    assert "installed" in capsys.readouterr().out


def test_a_real_git_push_runs_the_gate(work):
    _gate_on(work)
    _commit(work, "ok.txt", "fine\n")
    assert _push(work, "origin", "main").returncode == 0
    _commit(work, "bad.txt", f"reach me at {PERSON}\n")
    r = _push(work, "origin", "main")
    assert r.returncode != 0
    assert "private-email" in r.stderr and PERSON not in r.stderr
    remote_head = _git(work, "ls-remote", "origin", "main").split()[0]
    assert remote_head != _git(work, "rev-parse", "HEAD").strip()


def _hook_commands(event, matcher=None):
    with open(os.path.join(ROOT, ".claude", "settings.json")) as f:
        entries = json.load(f)["hooks"][event]
    return [h["command"] for e in entries if matcher is None or e.get("matcher") == matcher
            for h in e["hooks"]]


def test_the_hook_files_are_wired(tmp_path):
    shim = os.path.join(ROOT, ".githooks", "pre-push")
    assert os.stat(shim).st_mode & stat.S_IXUSR, "git ignores a hook that is not executable"
    [install] = [c for c in _hook_commands("SessionStart") if "prepush_check.py" in c]
    [guard] = [c for c in _hook_commands("PreToolUse", "Bash") if "prepush_check.py" in c]
    assert install.endswith('"$f" install') and guard.endswith('"$f" guard')
    refused = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git push --no-verify"}})

    def run(project):
        return subprocess.run(["sh", "-c", guard], input=refused, text=True, capture_output=True,
                              env={**os.environ, "CLAUDE_PROJECT_DIR": project}).returncode
    assert run(ROOT) == 2
    # A checkout of a branch from before the gate has no script. Exit 2 would
    # block every Bash call, `git checkout main` included: it must stand aside.
    assert run(str(tmp_path)) == 0


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
