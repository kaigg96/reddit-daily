"""Approved workflow changes apply themselves (#31). A shift cannot push
workflow files, so it attaches the exact change to its escalation; the owner's
label applies it, and since D16 (2026-11-14) so does three days of notice the
owner did not object to -- but never to the money checks, and never to a file
holding a key a shift does not hold. These run the real escalate.py on the
raising side and the exact script from apply-approved.yml on the applying side,
against real git."""
import datetime
import hashlib
import json
import os
import pathlib
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
const c = JSON.parse(ctx), out = { comments: [], closed: false, failed: null, by: {}, closedNumbers: [] };
const github = {
  rest: { issues: {
    createComment: async ({ issue_number, body }) => {
      out.comments.push(body);
      (out.by[issue_number] = out.by[issue_number] || []).push(body);
    },
    update: async ({ issue_number, state }) => {
      out.closed = state === 'closed';
      if (state === 'closed') out.closedNumbers.push(issue_number);
    },
    listForRepo: async () => ({ data: c.open || [] }),
    listComments: async ({ issue_number }) => ({ data: (c.comments || {})[issue_number] || [] }),
    listEvents: async ({ issue_number }) => ({ data: (c.events || {})[issue_number] || [] }),
    listEventsForTimeline: async ({ issue_number }) => ({ data: (c.timeline || {})[issue_number] || [] }),
  } },
  paginate: async (fn, params) => (await fn(params)).data,
  graphql: async (q, v) => ({ repository: { issue: {
    lastEditedAt: (c.editedAt || {})[v.n] || c.lastEditedAt || null } } }),
};
const context = { eventName: c.event, repo: { owner: 'o', repo: 'r' }, payload: { issue: c.issue } };
const core = { setFailed: m => { out.failed = m; }, info: () => {} };
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
                GIT_COMMITTER_EMAIL="t@t", RUNNER_TEMP=str(tmp_path), HAS_TOKEN="true",
                PYTHON=sys.executable)      # the checker needs PyYAML: this interpreter has it


# A notice-landed workflow must declare permissions (notice_check.py), so the
# demo file every notice test edits does.
def demo(name="Demo", extra=""):
    return f"name: {name}\non: push\npermissions:\n  contents: read\n{extra}"


def git(repo, env, *args):
    return subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path, env):
    r, origin = tmp_path / "repo", tmp_path / "origin.git"
    r.mkdir()
    git(tmp_path, env, "init", "-q", "--bare", "-b", "main", str(origin))
    git(r, env, "init", "-q", "-b", "main")
    checker = open(os.path.join(ROOT, ".github", "workflows", "notice_check.py")).read()
    for path, text in ((".github/workflows/demo.yml", demo()),
                       (".github/workflows/notice_check.py", checker),
                       (".github/workflows/protect-process.yml", "name: Guard\n"),
                       (".github/workflows/guardrails.yml", "name: Money checks\n"),
                       (".github/workflows/upload.yml",
                        demo("Upload", "env:\n  K: ${{ secrets.AWS_POLLY_ACCESS_KEY }}\n")),
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
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(text)
    if original is None:
        git(repo, env, "add", "-N", "--", path)      # git diff shows a new file only once it is intended
    patch = subprocess.run(["git", "diff", "--", path], cwd=repo, env=env,
                           capture_output=True, text=True).stdout
    if original is None:
        git(repo, env, "reset", "-q", "--", path)
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


def test_only_the_owners_label_or_the_clock_starts_it():
    cond = job()["if"]
    assert "github.event.label.name == 'approved'" in cond
    assert "github.event.sender.login == github.repository_owner" in cond
    # Any other label event is refused; the schedule and a dispatch are the notice path.
    assert cond.startswith("github.event_name != 'issues' ||")
    triggers = yaml.safe_load(open(WORKFLOW))[True]      # YAML reads the key `on` as True
    assert set(triggers) == {"issues", "schedule", "workflow_dispatch"}


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


def test_the_places_that_know_the_notice_rules_agree():
    """notice_check.py holds the rules; the two workflows carry only the days
    and the paths, and must match it, or an issue promises what the job refuses."""
    import re
    here = os.path.join(ROOT, ".github", "workflows")
    applying = open(os.path.join(here, "apply-approved.yml")).read()
    guard = open(os.path.join(here, "protect-process.yml")).read()
    days = lambda text: int(re.search(r"const NOTICE_DAYS = (\d+);", text).group(1))
    assert days(applying) == days(guard) == CHECK.NOTICE_DAYS == escalate.NOTICE_DAYS
    for path in CHECK.LOCKED:
        assert f"'{path}'" in applying and f"'{path}'" in guard
    for path in CHECK.MONEY_CHECKS:
        assert f"'{path}'" in applying and f"'{path}'" in guard
    assert escalate.ENFORCERS == CHECK.LOCKED and escalate.MONEY_CHECKS == CHECK.MONEY_CHECKS
    # ...and SHIFT_HOLDS is exactly what the shift job is given, no more.
    shift = open(os.path.join(here, "shift.yml")).read()
    assert set(re.findall(r"secrets\.([A-Z_]+)", shift)) == set(CHECK.SHIFT_HOLDS)


# --- Notice (D16): three days with no objection from the owner -------------------

def days_ago(n):
    return (datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(days=n)).isoformat(timespec="seconds")


def raised(repo, env, path, text, number=50, age=4, labels=("notice",)):
    """An open issue carrying a change, as the notice path lists it."""
    patch = diff_of(repo, env, path, text)
    inner = patch.rstrip("\n")
    sha = hashlib.sha256((inner + "\n").encode()).hexdigest()
    return {"number": number, "title": "Tidy the demo", "body": issue_body(inner, sha),
            "created_at": days_ago(age), "labels": [{"name": n} for n in labels]}


def notice(repo, env, tmp_path, issues, comments=None, events=None, edited=None, token="true"):
    script = job()["steps"][-1]["with"]["script"]
    ctx = {"event": "schedule", "open": issues, "comments": comments or {},
           "events": events or {}, "editedAt": edited or {}}
    for name, text in (("script.js", script), ("ctx.json", json.dumps(ctx)),
                       ("harness.js", HARNESS)):
        (tmp_path / name).write_text(text)
    out = subprocess.run(["node", str(tmp_path / "harness.js"), str(tmp_path / "script.js"),
                          str(tmp_path / "ctx.json")], cwd=repo, env=dict(env, HAS_TOKEN=token),
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def on_main(tmp_path, env, path):
    return subprocess.run(["git", "--git-dir", str(tmp_path / "origin.git"), "show", f"main:{path}"],
                          env=env, capture_output=True, text=True).stdout


DEMO = ".github/workflows/demo.yml"


def test_a_change_nobody_objected_to_lands_after_its_notice(repo, env, tmp_path):
    out = notice(repo, env, tmp_path, [raised(repo, env, DEMO, demo().replace("on: push", "on: [push]"))])
    assert out["closedNumbers"] == [50] and "**Applied**" in out["by"]["50"][-1]
    assert "3 days of notice" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, DEMO) == demo().replace("on: push", "on: [push]")
    message = git(repo, env, "log", "-1", "--format=%B")
    assert "Notice-In: #50" in message and "Approved-In" not in message


def test_a_notice_still_running_is_left_alone(repo, env, tmp_path):
    out = notice(repo, env, tmp_path, [raised(repo, env, DEMO, demo("Demo 2"), age=2)])
    assert out["comments"] == [] and out["closedNumbers"] == []
    assert on_main(tmp_path, env, DEMO) == demo()


@pytest.mark.parametrize("comments, events, labels", [
    ([{"user": {"login": "o"}, "body": "not this one"}], [], ("notice",)),
    ([], [{"event": "closed", "actor": {"login": "o"}}], ("notice",)),        # closed, then reopened by a shift
    ([], [{"event": "labeled", "label": {"name": "objection"}, "actor": {"login": "o"}}], ("notice",)),  # label since removed
    ([], [], ("notice", "Objection")),                                         # whoever put it there
])
def test_any_sign_of_the_owner_holds_a_notice(repo, env, tmp_path, comments, events, labels):
    issue = raised(repo, env, DEMO, demo("Demo 2"), labels=labels)
    out = notice(repo, env, tmp_path, [issue], comments={"50": comments}, events={"50": events})
    assert out["closedNumbers"] == [] and "**Held:**" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, DEMO) == demo()


def test_a_shifts_own_comment_does_not_hold_a_notice(repo, env, tmp_path):
    issue = raised(repo, env, DEMO, demo("Demo 2"))
    out = notice(repo, env, tmp_path, [issue],
                 comments={"50": [{"user": {"login": "claude[bot]"}, "body": "raised again"}]})
    assert out["closedNumbers"] == [50]


def test_an_issue_this_job_already_answered_is_not_answered_again(repo, env, tmp_path):
    issue = raised(repo, env, DEMO, demo("Demo 2"))
    out = notice(repo, env, tmp_path, [issue], comments={"50": [
        {"user": {"login": "github-actions[bot]"}, "body": "<!-- apply-result -->\n**Held:** ..."}]})
    assert out["comments"] == [] and out["closedNumbers"] == []


@pytest.mark.parametrize("path", [".github/workflows/guardrails.yml",
                                  ".github/workflows/protect-process.yml", "src/app.py"])
def test_a_notice_never_reaches_the_money_checks_or_the_enforcers(repo, env, tmp_path, path):
    out = notice(repo, env, tmp_path, [raised(repo, env, path, "changed\n")])
    assert out["closedNumbers"] == [] and "**Not applied by notice:**" in out["by"]["50"][-1]
    assert "`approved` label" in out["by"]["50"][-1]
    assert git(repo, env, "status", "--porcelain") == ""        # nothing left staged


def test_a_notice_cannot_remove_the_money_checks_by_renaming_them(repo, env, tmp_path):
    git(repo, env, "mv", ".github/workflows/guardrails.yml", ".github/workflows/later.yml")
    patch = git(repo, env, "diff", "--cached", "-M", "HEAD") + "\n"
    git(repo, env, "reset", "-q", "--hard")
    inner = patch.rstrip("\n")
    issue = {"number": 50, "title": "Rename a job", "created_at": days_ago(4), "labels": [{"name": "notice"}],
             "body": issue_body(inner, hashlib.sha256((inner + "\n").encode()).hexdigest())}
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "guardrails.yml" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, ".github/workflows/guardrails.yml") == "name: Money checks\n"


def test_a_notice_never_changes_a_file_that_holds_a_paid_key(repo, env, tmp_path):
    """Even an edit that leaves the key line alone: the file runs with it."""
    issue = raised(repo, env, ".github/workflows/upload.yml",
                   demo("Upload more", "env:\n  K: ${{ secrets.AWS_POLLY_ACCESS_KEY }}\n"))
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "AWS_POLLY_ACCESS_KEY" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, ".github/workflows/upload.yml").startswith("name: Upload\n")
    assert git(repo, env, "status", "--porcelain") == ""


@pytest.mark.parametrize("reach, found", [
    ("${{ secrets.AWS_POLLY_ACCESS_KEY }}", "secrets.AWS_POLLY_ACCESS_KEY"),
    ("${{ SECRETS.aws_polly_access_key }}", "secrets.aws_polly_access_key"),   # expression names ignore case
    ("${{ secrets . YOUTUBE_REFRESH_TOKEN }}", "secrets.YOUTUBE_REFRESH_TOKEN"),
    ("${{ secrets['APPLY_TOKEN'] }}", "every secret"),
    ("${{ toJSON(secrets) }}", "every secret"),
    ("${{ join(secrets.*, ' ') }}", "every secret"),
    ("${{ format('{0}', secrets, 1) }}", "every secret"),
])
def test_a_notice_cannot_hand_a_job_a_key_a_shift_does_not_hold(repo, env, tmp_path, reach, found):
    issue = raised(repo, env, DEMO, demo(extra=f"env:\n  K: {reach}\n"))
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "**Not applied by notice:**" in out["by"]["50"][-1]
    assert found in out["by"]["50"][-1]
    assert on_main(tmp_path, env, DEMO) == demo()


def test_a_notice_cannot_inherit_every_key_into_a_called_workflow(repo, env, tmp_path):
    issue = raised(repo, env, DEMO, demo(extra="jobs:\n  a:\n    uses: ./x.yml\n    secrets: inherit\n"))
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "every secret" in out["by"]["50"][-1]


def test_a_notice_may_use_the_keys_a_shift_already_holds(repo, env, tmp_path):
    text = demo(extra="env:\n  G: ${{ secrets.GEMINI_API_KEY }}\n")
    out = notice(repo, env, tmp_path, [raised(repo, env, DEMO, text)])
    assert out["closedNumbers"] == [50] and on_main(tmp_path, env, DEMO) == text


def test_the_owners_label_still_reaches_what_a_notice_cannot(repo, env, tmp_path):
    text = demo("Upload more", "env:\n  K: ${{ secrets.AWS_POLLY_ACCESS_KEY }}\n")
    issue = raised(repo, env, ".github/workflows/upload.yml", text)
    out = apply(repo, env, tmp_path, issue["body"])
    assert out["closed"] and on_main(tmp_path, env, ".github/workflows/upload.yml") == text
    assert "Approved-In: #44" in git(repo, env, "log", "-1", "--format=%B")


def test_an_edited_notice_is_refused(repo, env, tmp_path):
    issue = raised(repo, env, DEMO, demo("Demo 2"))
    out = notice(repo, env, tmp_path, [issue], edited={"50": "2026-11-14T10:00:00Z"})
    assert out["closedNumbers"] == [] and "edited after it was raised" in out["by"]["50"][-1]


def test_two_notices_land_one_after_the_other_and_a_refusal_does_not_stop_the_next(repo, env, tmp_path):
    bad = raised(repo, env, ".github/workflows/guardrails.yml", "changed\n", number=50)
    good = raised(repo, env, DEMO, demo("Demo 2"), number=51)
    out = notice(repo, env, tmp_path, [bad, good])
    assert out["closedNumbers"] == [51] and on_main(tmp_path, env, DEMO) == demo("Demo 2")
    assert on_main(tmp_path, env, ".github/workflows/guardrails.yml") == "name: Money checks\n"


def test_the_notice_path_does_nothing_without_the_token(repo, env, tmp_path):
    out = notice(repo, env, tmp_path, [raised(repo, env, DEMO, demo("Demo 2"))], token="false")
    assert out["comments"] == [] and out["closedNumbers"] == []


# --- The raising side: what escalate.py tells the owner a change will do ---------

def queue(repo, tmp_path, monkeypatch, *argv, body="Why."):
    import io
    monkeypatch.setattr(escalate, "QUEUE", tmp_path / ".escalations")
    monkeypatch.setattr(escalate, "ROOT", repo)
    monkeypatch.setattr(pathlib.Path, "relative_to", lambda self, *a: self)   # the queue sits outside this repo
    monkeypatch.setattr(sys, "argv", ["escalate.py", "--title", "T", *argv])
    monkeypatch.setattr(sys, "stdin", io.StringIO(body))
    escalate.main()
    return sorted((tmp_path / ".escalations").glob("*.md"))[-1].read_text()


def test_a_change_within_a_shifts_reach_is_raised_as_a_dated_notice(repo, env, tmp_path, monkeypatch):
    (tmp_path / "c.patch").write_text(diff_of(repo, env, DEMO, demo("Demo 2")))
    text = queue(repo, tmp_path, monkeypatch, "--patch", str(tmp_path / "c.patch"))
    assert "labels: notice" in text and "**A notice, not a question.**" in text
    assert "applies itself, exactly as shown, on or after" in text and "`objection`" in text
    assert "Nothing is needed from you unless you object" in text


@pytest.mark.parametrize("path, text, why", [
    (".github/workflows/upload.yml", demo("Upload more", "env:\n  K: ${{ secrets.AWS_POLLY_ACCESS_KEY }}\n"),
     "AWS_POLLY_ACCESS_KEY"),
    (DEMO, "name: Demo\non: push\nenv:\n  K: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}\n", "YOUTUBE_REFRESH_TOKEN"),
    (".github/workflows/guardrails.yml", "name: Fewer money checks\n", "money checks"),
])
def test_a_change_beyond_a_shifts_reach_is_raised_as_an_ask(repo, env, tmp_path, monkeypatch,
                                                           path, text, why):
    (tmp_path / "c.patch").write_text(diff_of(repo, env, path, text))
    out = queue(repo, tmp_path, monkeypatch, "--patch", str(tmp_path / "c.patch"))
    assert "labels: needs-owner" in out and "does not apply itself after notice" in out
    assert why in out and "A notice, not a question" not in out


CHECK = escalate.checker()


@pytest.mark.parametrize("text, found", [
    ("${{ secrets.AWS_POLLY_ACCESS_KEY }}", "secrets.AWS_POLLY_ACCESS_KEY"),
    ("${{ SECRETS.aws_polly_access_key }}", "secrets.aws_polly_access_key"),
    ("${{ secrets . YOUTUBE_REFRESH_TOKEN }}", "secrets.YOUTUBE_REFRESH_TOKEN"),
    ("${{ secrets['APPLY_TOKEN'] }}", "every secret"),
    ("${{ toJSON(secrets) }}", "every secret"),
    ("${{ toJSON(secrets || 0) }}", "every secret"),          # an operator after it (review, 11-15)
    ("${{ join(secrets.*, ' ') }}", "every secret"),
    ("${{ format('{0}', secrets, 1) }}", "every secret"),
    ("    secrets: inherit", "every secret"),
    ("    secrets: \"inherit\"", "every secret"),             # quoted: the old regex missed it
    ("# no upload secrets here", "every secret"),              # prose counts: a refusal is the safe answer
    ("\"${{ secr\\x65ts.AWS_POLLY_ACCESS_KEY }}\"", "escaped character"),
])
def test_the_checker_reads_every_way_a_key_can_be_spelled(text, found):
    assert any(found in r for r in CHECK.reasons(text, "x.yml", raw_only=True)), CHECK.reasons(text, "x.yml", raw_only=True)


@pytest.mark.parametrize("text", [
    "${{ secrets.GEMINI_API_KEY }} ${{ secrets.claude_code_oauth_token }}",
    "# no upload keys here",
])
def test_the_checker_allows_what_a_shift_already_holds(text):
    assert CHECK.reasons(text, "x.yml", raw_only=True) == []


@pytest.mark.parametrize("yaml_text, found", [
    ('name: x\non: push\npermissions:\n  contents: read\nenv:\n  K: "${{ secr\\x65ts.AWS_POLLY_ACCESS_KEY }}"\n',
     "secrets.AWS_POLLY_ACCESS_KEY"),                                      # resolves once parsed
    ('name: x\non: push\npermissions:\n  contents: read\njobs:\n  a:\n    uses: ./x.yml\n    "secrets": inherit\n',
     "every secret"),
    ('name: x\non: push\npermissions:\n  contents: read\njobs:\n  a:\n    uses: ./x.yml\n    secrets: \'inherit\'\n',
     "every secret"),
    ("name: x\non: push\n", "declares no permissions"),
    ("name: x\non: push\npermissions: write-all\n", "grants write-all"),
    ("name: x\non: push\npermissions:\n  actions: write\n", "grants actions: write"),
    ("name: x\non: push\npermissions:\n  pull-requests: write\n", "grants pull-requests: write"),
    ("name: x\non: push\npermissions:\n  contents: read\njobs:\n  a:\n    permissions:\n      actions: write\n",
     "job a grants actions: write"),
    ("name: x\non: push\npermissions:\n  contents: read\njobs: [\n", "could not be read as YAML"),
    ("just a string\n", "not a workflow"),
])
def test_the_checker_reads_the_parsed_workflow_too(yaml_text, found):
    assert any(found in r for r in CHECK.reasons(yaml_text, "x.yml")), CHECK.reasons(yaml_text, "x.yml")


def test_the_checker_allows_a_workflow_shaped_like_the_shifts_own():
    text = ("name: x\non: push\npermissions:\n  contents: write\n  issues: write\n  actions: read\n"
            "  id-token: write\njobs:\n  a:\n    permissions:\n      contents: read\n    env:\n"
            "      G: ${{ secrets.GEMINI_API_KEY }}\n")
    assert CHECK.reasons(text, "x.yml") == []


def test_the_checker_runs_as_a_command_and_refuses_on_any_error(tmp_path):
    out = subprocess.run([sys.executable, os.path.join(ROOT, ".github", "workflows", "notice_check.py"),
                          "--name", "x.yml"], input="name: x\non: push\n", capture_output=True, text=True)
    assert out.returncode == 1 and "declares no permissions" in out.stdout
    out = subprocess.run([sys.executable, os.path.join(ROOT, ".github", "workflows", "notice_check.py"),
                          "--name", "x.yml", str(tmp_path / "missing")], capture_output=True, text=True)
    assert out.returncode == 2 and "could not be checked" in out.stdout


def test_a_one_way_door_is_a_notice_with_a_date_and_never_under_a_week(repo, tmp_path, monkeypatch):
    text = queue(repo, tmp_path, monkeypatch, "--notice-days", "7", body="Delete the 883 old videos.")
    due = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).date().isoformat()
    assert f"<!-- notice-date: {due} -->" in text and "labels: notice" in text
    assert "**A notice, not a question.**" in text and "Delete the 883 old videos." in text
    with pytest.raises(SystemExit):
        queue(repo, tmp_path, monkeypatch, "--notice-days", "3")


def test_a_plain_ask_is_still_an_ask(repo, tmp_path, monkeypatch):
    text = queue(repo, tmp_path, monkeypatch)
    assert "labels: needs-owner" in text and "could not go on without you" in text
    assert "notice" not in text


def test_a_change_an_ask_carries_is_not_touched_by_the_notice_run(repo, env, tmp_path):
    """escalate.py labels a change that waits for the label `needs-owner`, not
    `notice`; the daily run passes it by without a comment (review, 11-15)."""
    issue = raised(repo, env, ".github/workflows/upload.yml",
                   demo("Upload more", "env:\n  K: ${{ secrets.AWS_POLLY_ACCESS_KEY }}\n"),
                   labels=("needs-owner",))
    out = notice(repo, env, tmp_path, [issue])
    assert out["comments"] == [] and out["closedNumbers"] == []


def test_a_notice_cannot_delete_a_file_that_holds_a_paid_key(repo, env, tmp_path):
    (repo / ".github/workflows/upload.yml").unlink()
    patch = git(repo, env, "diff", "--", ".github/workflows/upload.yml") + "\n"
    git(repo, env, "checkout", "--", ".github/workflows/upload.yml")
    inner = patch.rstrip("\n")
    issue = {"number": 50, "title": "Drop the upload job", "created_at": days_ago(4),
             "labels": [{"name": "notice"}],
             "body": issue_body(inner, hashlib.sha256((inner + "\n").encode()).hexdigest())}
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "AWS_POLLY_ACCESS_KEY" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, ".github/workflows/upload.yml").startswith("name: Upload\n")


@pytest.mark.parametrize("extra", [
    "  actions: write\n",                                   # dispatches the keyed jobs (review, 11-15)
    "  pull-requests: write\n",
])
def test_a_notice_cannot_widen_the_token(repo, env, tmp_path, extra):
    issue = raised(repo, env, DEMO, demo().replace("  contents: read\n", "  contents: read\n" + extra))
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "grants" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, DEMO) == demo()


def test_a_notice_cannot_add_a_workflow_with_no_permissions_block(repo, env, tmp_path):
    issue = raised(repo, env, ".github/workflows/new.yml", "name: New\non: push\njobs: {}\n")
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "declares no permissions" in out["by"]["50"][-1]
    assert on_main(tmp_path, env, ".github/workflows/new.yml") == ""


def test_a_notice_cannot_spell_a_key_with_an_escape(repo, env, tmp_path):
    issue = raised(repo, env, DEMO, demo(extra='env:\n  K: "${{ secr\\x65ts.APPLY_TOKEN }}"\n'))
    out = notice(repo, env, tmp_path, [issue])
    assert out["closedNumbers"] == [] and "APPLY_TOKEN" in out["by"]["50"][-1]


def test_a_deleted_comment_holds_a_notice_whoever_deleted_it(repo, env, tmp_path):
    """A shift's token can delete the owner's reply; it cannot delete the
    record that a comment was deleted."""
    issue = raised(repo, env, DEMO, demo("Demo 2"))
    out = notice(repo, env, tmp_path, [issue], events={"50": [{"event": "comment_deleted"}]})
    assert out["closedNumbers"] == [] and "**Held:**" in out["by"]["50"][-1]
    ctx_timeline = notice(repo, env, tmp_path, [raised(repo, env, DEMO, demo("Demo 3"))],
                          comments={}, events={})
    assert ctx_timeline["closedNumbers"] == [50]


def test_the_owners_label_applies_an_issue_a_notice_run_already_held(repo, env, tmp_path):
    inner, sha = escalate.validate_patch(
        diff_of(repo, env, DEMO, demo("Demo 2")), repo=repo)
    script = job()["steps"][-1]["with"]["script"]
    ctx = {"lastEditedAt": None, "event": "issues",
           "issue": {"number": 44, "title": "Tidy", "body": issue_body(inner, sha)},
           "comments": {"44": [{"user": {"login": "github-actions[bot]"},
                                "body": "<!-- apply-result -->\n**Held:** ..."}]}}
    for name, text in (("script.js", script), ("ctx.json", json.dumps(ctx)), ("harness.js", HARNESS)):
        (tmp_path / name).write_text(text)
    out = json.loads(subprocess.run(["node", str(tmp_path / "harness.js"), str(tmp_path / "script.js"),
                                     str(tmp_path / "ctx.json")], cwd=repo, env=env, check=True,
                                    capture_output=True, text=True).stdout)
    assert out["closed"] and on_main(tmp_path, env, DEMO) == demo("Demo 2")
