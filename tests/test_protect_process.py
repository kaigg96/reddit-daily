"""The process guard (.github/workflows/protect-process.yml), tested by running
its exact script text -- pulled out of the workflow file -- against real git
histories. It is the only thing between a shift and its own rules, and until
2026-09-24 it inspected just the last commit of each push."""
import json
import os
import shutil
import subprocess

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "protect-process.yml")

pytestmark = pytest.mark.skipif(not shutil.which("node") or not shutil.which("git"),
                                reason="needs node and git")

HARNESS = r"""
const fs = require('fs');
const [script, approvals, payload] = process.argv.slice(2).map(p => fs.readFileSync(p, 'utf8'));
const labels = JSON.parse(approvals), push = JSON.parse(payload), out = { warnings: [] };
const core = { setOutput: (k, v) => { out[k] = v; }, warning: m => out.warnings.push(m), info: () => {} };
// approvals: {issue: [labels]} (labelled by the owner, 'o') or {issue: {labels, by}}
const entry = n => Array.isArray(labels[n]) ? { labels: labels[n], by: 'o' } : labels[n];
const github = {
  rest: { issues: {
    get: async ({ issue_number }) => {
      if (!(issue_number in labels)) throw new Error('Not Found');
      return { data: { labels: entry(issue_number).labels.map(name => ({ name })) } };
    },
    listEvents: async ({ issue_number }) => ({ data: entry(issue_number).labels.map(name =>
      ({ event: 'labeled', label: { name }, actor: { login: entry(issue_number).by } })) }),
  } },
  paginate: async (fn, params) => (await fn(params)).data,
};
const context = { sha: push.after, payload: { before: push.before }, repo: { owner: 'o', repo: 'r' } };
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
new AsyncFunction('github', 'context', 'core', 'require', 'process', script)(
  github, context, core, require, process).then(() => console.log(JSON.stringify(out)));
"""


def steps():
    wf = yaml.safe_load(open(WORKFLOW))
    return {s.get("name"): s for s in wf["jobs"]["check"]["steps"]}


@pytest.fixture
def env(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    return dict(os.environ, HOME=str(home), GIT_CONFIG_GLOBAL=str(home / ".gitconfig"),
                GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                GIT_COMMITTER_EMAIL="t@t", RUNNER_TEMP=str(tmp_path))


@pytest.fixture
def repo(tmp_path, env):
    r = tmp_path / "repo"
    r.mkdir()
    run(r, env, "init", "-q", "-b", "main")
    write(r, "README.md", "hi\n")
    write(r, "CLAUDE.md", "rules v1\n")
    write(r, ".claude/skills/shift/SKILL.md", "skill v1\n")
    commit(r, env, "base")
    return r


def run(repo, env, *args):
    return subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def write(repo, path, text):
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def commit(repo, env, msg):
    run(repo, env, "add", "-A")
    run(repo, env, "commit", "-q", "-m", msg)
    return run(repo, env, "rev-parse", "HEAD")


def guard(repo, env, tmp_path, before, approvals=None):
    for name, text in (("script.js", steps()["Was this approved?"]["with"]["script"]),
                       ("approvals.json", json.dumps(approvals or {})),
                       ("payload.json", json.dumps({"before": before,
                                                    "after": run(repo, env, "rev-parse", "HEAD")})),
                       ("harness.js", HARNESS)):
        (tmp_path / name).write_text(text)
    out = subprocess.run(["node", str(tmp_path / "harness.js"), str(tmp_path / "script.js"),
                          str(tmp_path / "approvals.json"), str(tmp_path / "payload.json")],
                         cwd=repo, env=env, check=True, capture_output=True, text=True).stdout
    return json.loads(out)


APPROVED = {5: ["needs-owner", "approved"]}


def test_an_approved_change_passes(repo, env, tmp_path):
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2\n")
    commit(repo, env, "Change the skill\n\nApproved-In: #5")
    assert guard(repo, env, tmp_path, before, APPROVED)["ok"] == "true"


@pytest.mark.parametrize("message, approvals, why", [
    ("Change the skill", APPROVED, "no `Approved-In: #N` trailer"),
    ("Change the skill\n\nApproved-In: #5", {5: ["needs-owner"]}, "not labelled `approved`"),
    ("Change the skill\n\nApproved-In: #9", APPROVED, "#9 could not be read"),
])
def test_an_unapproved_change_is_caught(repo, env, tmp_path, message, approvals, why):
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2\n")
    commit(repo, env, message)
    out = guard(repo, env, tmp_path, before, approvals)
    assert out["ok"] == "false" and why in out["why"]


def test_the_label_check_forgives_case_and_spaces(repo, env, tmp_path):
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, "CLAUDE.md", "rules v2\n")
    commit(repo, env, "Rules\n\nApproved-In: #5")
    assert guard(repo, env, tmp_path, before, {5: [" Approved "]})["ok"] == "true"


def test_a_protected_edit_behind_a_later_commit_is_caught(repo, env, tmp_path):
    """The gap found 2026-09-24: the old guard diffed HEAD~1..HEAD only."""
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2 -- unapproved\n")
    commit(repo, env, "Quietly change the skill")
    write(repo, "README.md", "hi again\n")
    commit(repo, env, "Unrelated tip")
    assert run(repo, env, "diff", "--name-only", "HEAD~1", "HEAD") == "README.md"  # all the old guard saw
    out = guard(repo, env, tmp_path, before, APPROVED)
    assert out["ok"] == "false" and ".claude/skills/shift/SKILL.md" in out["files"]


def test_approved_work_merged_with_a_merge_commit_passes(repo, env, tmp_path):
    """The false revert recorded 2026-09-23: a merge commit's message has no trailer."""
    before = run(repo, env, "rev-parse", "HEAD")
    run(repo, env, "checkout", "-q", "-b", "feature")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2\n")
    commit(repo, env, "Change the skill\n\nApproved-In: #5")
    run(repo, env, "checkout", "-q", "main")
    write(repo, "README.md", "main moved on\n")
    commit(repo, env, "Meanwhile on main")
    run(repo, env, "merge", "-q", "--no-ff", "feature", "-m", "Merge pull request #30 from feature")
    assert guard(repo, env, tmp_path, before, APPROVED)["ok"] == "true"


def test_a_protected_edit_hidden_inside_a_merge_is_caught(repo, env, tmp_path):
    before = run(repo, env, "rev-parse", "HEAD")
    run(repo, env, "checkout", "-q", "-b", "feature")
    write(repo, "README.md", "feature work\n")
    commit(repo, env, "Harmless feature")
    run(repo, env, "checkout", "-q", "main")
    write(repo, "notes.txt", "x\n")
    commit(repo, env, "Meanwhile on main")
    run(repo, env, "merge", "-q", "--no-ff", "--no-commit", "feature")
    write(repo, "CLAUDE.md", "rules rewritten during the merge\n")
    commit(repo, env, "Merge feature")
    out = guard(repo, env, tmp_path, before, APPROVED)
    assert out["ok"] == "false" and "CLAUDE.md" in out["files"]


def test_unprotected_changes_pass(repo, env, tmp_path):
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, "README.md", "docs\n")
    commit(repo, env, "Docs")
    assert guard(repo, env, tmp_path, before)["ok"] == "true"


def test_an_unknown_push_base_still_checks_the_tip(repo, env, tmp_path):
    write(repo, "CLAUDE.md", "rules v2\n")
    commit(repo, env, "Unapproved rules")
    out = guard(repo, env, tmp_path, "1" * 40, APPROVED)
    assert out["ok"] == "false" and out["warnings"]


def test_the_revert_restores_edits_removes_additions_and_keeps_the_rest(repo, env, tmp_path):
    """Runs the revert step's own shell against a real origin. The old revert
    could not remove a file the push added, and interpolated file names into
    the shell -- a name is chosen by whoever made the commit."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], env=env, check=True)
    run(repo, env, "remote", "add", "origin", str(origin))
    run(repo, env, "push", "-q", "-u", "origin", "main")
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2 -- unapproved\n")
    evil = ".claude/skills/x$(touch PWNED)/SKILL.md"
    write(repo, evil, "an added skill\n")
    write(repo, "README.md", "legitimate docs change\n")
    commit(repo, env, "Mixed push")
    run(repo, env, "push", "-q", "origin", "main")

    out = guard(repo, env, tmp_path, before, APPROVED)
    assert out["ok"] == "false"
    revert = steps()["Revert the unapproved change"]["run"]
    subprocess.run(["bash", "-e", "-c", revert], cwd=repo, check=True, capture_output=True,
                   env=dict(env, BASE=out["base"]))

    assert (repo / ".claude/skills/shift/SKILL.md").read_text() == "skill v1\n"
    assert not (repo / evil).exists()
    assert (repo / "README.md").read_text() == "legitimate docs change\n"
    assert not (repo / "PWNED").exists() and not (tmp_path / "PWNED").exists()
    assert run(repo, env, "rev-parse", "HEAD") == run(origin, env, "rev-parse", "main")


def test_only_the_owners_label_is_an_approval(repo, env, tmp_path):
    """A shift's token can add labels; an `approved` it added is not a decision."""
    before = run(repo, env, "rev-parse", "HEAD")
    write(repo, ".claude/skills/shift/SKILL.md", "skill v2\n")
    commit(repo, env, "Self-approved\n\nApproved-In: #5")
    out = guard(repo, env, tmp_path, before,
                {5: {"labels": ["needs-owner", "approved"], "by": "claude[bot]"}})
    assert out["ok"] == "false" and "by claude[bot], not o" in out["why"]
