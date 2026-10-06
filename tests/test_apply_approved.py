"""Approved workflow changes apply themselves (#31). A shift cannot push
workflow files, so it attaches the exact change to its escalation; the owner's
label applies it. These run the real escalate.py on the raising side and the
exact script from apply-approved.yml on the applying side, against real git."""
import json
import os
import shutil
import subprocess
import sys

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from scripts import escalate  # noqa: E402

WORKFLOW = os.path.join(ROOT, ".github", "workflows", "apply-approved.yml")
pytestmark = pytest.mark.skipif(not shutil.which("node") or not shutil.which("git"),
                                reason="needs node and git")

HARNESS = r"""
const fs = require('fs');
const [script, ctx] = process.argv.slice(2).map(p => fs.readFileSync(p, 'utf8'));
const c = JSON.parse(ctx), out = { comments: [], closed: false, failed: null };
const github = {
  rest: { issues: {
    createComment: async ({ body }) => { out.comments.push(body); },
    update: async ({ state }) => { out.closed = state === 'closed'; },
  } },
  graphql: async () => ({ repository: { issue: { lastEditedAt: c.lastEditedAt } } }),
};
const context = { repo: { owner: 'o', repo: 'r' }, payload: { issue: c.issue } };
const core = { setFailed: m => { out.failed = m; } };
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
new AsyncFunction('github', 'context', 'core', 'require', 'process', script)(
  github, context, core, require, process).then(() => console.log(JSON.stringify(out)));
"""


def job():
    return yaml.safe_load(open(WORKFLOW))["jobs"]["apply"]


@pytest.fixture
def env(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    return dict(os.environ, HOME=str(home), GIT_CONFIG_GLOBAL=str(home / ".gitconfig"),
                GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                GIT_COMMITTER_EMAIL="t@t", RUNNER_TEMP=str(tmp_path), HAS_TOKEN="true")


def git(repo, env, *args):
    return subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path, env):
    r, origin = tmp_path / "repo", tmp_path / "origin.git"
    r.mkdir()
    git(tmp_path, env, "init", "-q", "--bare", "-b", "main", str(origin))
    git(r, env, "init", "-q", "-b", "main")
    for path, text in ((".github/workflows/demo.yml", "name: Demo\non: push\n"),
                       (".github/workflows/protect-process.yml", "name: Guard\n"),
                       ("src/app.py", "print('hi')\n")):
        (r / path).parent.mkdir(parents=True, exist_ok=True)
        (r / path).write_text(text)
    git(r, env, "add", "-A")
    git(r, env, "commit", "-q", "-m", "base")
    git(r, env, "remote", "add", "origin", str(origin))
    git(r, env, "push", "-q", "-u", "origin", "main")
    return r


def diff_of(repo, env, path, text):
    """Make an edit, capture it the way a shift would, then drop the edit."""
    original = (repo / path).read_text() if (repo / path).exists() else None
    (repo / path).write_text(text)
    patch = subprocess.run(["git", "diff", "--", path], cwd=repo, env=env,
                           capture_output=True, text=True).stdout
    if original is None:
        (repo / path).unlink()
    else:
        git(repo, env, "checkout", "--", path)
    return patch


def issue_body(inner, sha):
    return "<!-- escalation-key: k -->\n\nWhy.\n\n" + "\n".join(escalate.patch_section(inner, sha))


def apply(repo, env, tmp_path, body, edited=None):
    script = job()["steps"][-1]["with"]["script"]
    ctx = {"lastEditedAt": edited,
           "issue": {"number": 44, "title": "Approve: tidy the demo", "body": body}}
    for name, text in (("script.js", script), ("ctx.json", json.dumps(ctx)),
                       ("harness.js", HARNESS)):
        (tmp_path / name).write_text(text)
    out = subprocess.run(["node", str(tmp_path / "harness.js"), str(tmp_path / "script.js"),
                          str(tmp_path / "ctx.json")], cwd=repo, env=env, check=True,
                         capture_output=True, text=True).stdout
    return json.loads(out)


def test_only_the_owners_label_starts_it():
    cond = job()["if"]
    assert "github.event.label.name == 'approved'" in cond
    assert "github.event.sender.login == github.repository_owner" in cond


def test_the_approved_change_lands_exactly_and_the_issue_closes(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo\non: [push]\n"), repo=repo)
    out = apply(repo, env, tmp_path, issue_body(inner, sha))
    assert out["closed"] and "**Applied**" in out["comments"][-1]
    shown = subprocess.run(["git", "--git-dir", str(tmp_path / "origin.git"), "show",
                            "main:.github/workflows/demo.yml"], env=env, capture_output=True,
                           text=True).stdout
    assert shown == "name: Demo\non: [push]\n"
    message = git(repo, env, "log", "-1", "--format=%B")
    assert "Approved-In: #44" in message and message.startswith("tidy the demo")


def test_an_edited_issue_is_refused(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo 2\non: push\n"), repo=repo)
    out = apply(repo, env, tmp_path, issue_body(inner, sha), edited="2026-09-25T10:00:00Z")
    assert not out["closed"] and "edited after it was raised" in out["comments"][-1]


def test_a_tampered_change_fails_its_fingerprint(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo 2\non: push\n"), repo=repo)
    out = apply(repo, env, tmp_path, issue_body(inner.replace("Demo 2", "Demo 3"), sha))
    assert not out["closed"] and "fingerprint" in out["comments"][-1]


@pytest.mark.parametrize("path", ["src/app.py", ".github/workflows/protect-process.yml"])
def test_it_never_reaches_beyond_ordinary_workflows(repo, env, tmp_path, path):
    """Even a change that slipped past escalate.py is refused on what git stages."""
    patch = diff_of(repo, env, path, "changed\n")
    inner = patch.rstrip("\n")
    sha = __import__("hashlib").sha256((inner + "\n").encode()).hexdigest()
    out = apply(repo, env, tmp_path, issue_body(inner, sha))
    assert not out["closed"] and "workflow files" in out["comments"][-1]
    assert git(repo, env, "status", "--porcelain") == ""        # nothing left staged


def test_a_stale_change_is_refused_not_forced(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo 2\non: push\n"), repo=repo)
    (repo / ".github/workflows/demo.yml").write_text("name: Moved on\non: push\n")
    git(repo, env, "commit", "-qam", "main moved on")
    out = apply(repo, env, tmp_path, issue_body(inner, sha))
    assert not out["closed"] and "no longer fits" in out["comments"][-1]


def test_without_the_token_it_says_so(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo 2\non: push\n"), repo=repo)
    out = apply(repo, dict(env, HAS_TOKEN="false"), tmp_path, issue_body(inner, sha))
    assert not out["closed"] and "not set up" in out["comments"][-1]


@pytest.mark.parametrize("path", ["src/app.py", ".github/workflows/apply-approved.yml"])
def test_escalate_refuses_what_auto_apply_would(repo, env, path):
    patch = diff_of(repo, env, path, "changed\n")
    with pytest.raises(SystemExit):
        escalate.validate_patch(patch, repo=repo)


def test_two_messages_on_one_key_queue_as_two_files(tmp_path, monkeypatch):
    """A second same-day comment must not overwrite the first, nor reuse the
    name the filer deletes once the first is filed (2026-10-06)."""
    import io
    monkeypatch.setattr(escalate, "QUEUE", tmp_path / ".escalations")
    monkeypatch.setattr(escalate, "ROOT", tmp_path)
    for body in ("first", "second"):
        monkeypatch.setattr(sys, "argv", ["escalate.py", "--title", "T", "--key", "same-key"])
        monkeypatch.setattr(sys, "stdin", io.StringIO(body))
        escalate.main()
    files = sorted((tmp_path / ".escalations").glob("*.md"))
    assert len(files) == 2
    assert ["first" in files[0].read_text(), "second" in files[1].read_text()] == [True, True]
    assert all("key: same-key" in f.read_text() for f in files)
