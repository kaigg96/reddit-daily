"""The report email is the owner's one window into the channel while they are
away, so the step that sends it is run here with its exact script text. A
thrown error in it would stop the emails silently."""
import json
import os
import shutil
import subprocess

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="needs node")

HARNESS = r"""
const fs = require('fs');
const [script, fx] = process.argv.slice(2).map(p => fs.readFileSync(p, 'utf8'));
const f = JSON.parse(fx); const out = {};
const github = {
  rest: { issues: {
    listForRepo: async () => ({ data: f.open }),
    listComments: async ({ issue_number }) => ({ data: f.comments[issue_number] || [] }),
    create: async () => ({ data: { number: 15 } }),
    createComment: async ({ body }) => { out.body = body; },
  } },
  paginate: async (fn, params) => (await fn(params)).data,
};
const context = { serverUrl: 'https://github.com', runId: 1, repo: { owner: 'o', repo: 'r' } };
const core = { info: () => {} };
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
new AsyncFunction('github', 'context', 'core', 'require', 'process', script)(
  github, context, core, require, process).then(() => console.log(JSON.stringify(out)));
"""


def email(tmp_path, open_issues, comments=None):
    wf = yaml.safe_load(open(os.path.join(ROOT, ".github", "workflows", "shift.yml")))
    step = next(s for s in wf["jobs"]["shift"]["steps"]
                if s.get("name") == "Email the owner what this shift did")
    thread = {"number": 15, "body": "<!-- shift-reports -->", "labels": [{"name": "shift-report"}],
              "comments": 0, "title": "Shift reports", "html_url": "u15"}
    for name, text in (("script.js", step["with"]["script"]), ("harness.js", HARNESS),
                       ("fx.json", json.dumps({"open": [thread] + open_issues,
                                               "comments": comments or {}}))):
        (tmp_path / name).write_text(text)
    out = subprocess.run(["node", str(tmp_path / "harness.js"), str(tmp_path / "script.js"),
                          str(tmp_path / "fx.json")], cwd=ROOT, check=True, capture_output=True,
                         text=True, env=dict(os.environ, START_SHA="HEAD")).stdout
    return json.loads(out)["body"]


def esc(n, title, labels, comments=0):
    return {"number": n, "title": title, "labels": [{"name": l} for l in labels],
            "comments": comments, "html_url": f"u{n}", "body": ""}


def test_it_leads_with_what_needs_the_owner(tmp_path):
    body = email(tmp_path, [esc(22, "Gemini cap?", ["needs-owner"], comments=1),
                            esc(31, "Pre-trip", ["needs-owner"]),
                            esc(27, "Dry runs", ["needs-owner", "approved"])],
                 {22: [{"author_association": "OWNER", "body": "no money"}]})
    head = body.split("---")[0]
    assert head.startswith("**Waiting on you (2):**")
    assert "#22" in head and "you replied" in head
    assert "#31" in head and "#27" not in head          # approved is not waiting


def test_it_says_plainly_when_nothing_is_waiting(tmp_path):
    body = email(tmp_path, [esc(27, "Dry runs", ["needs-owner", "approved"])])
    assert body.startswith("**Nothing is waiting on you.**")
