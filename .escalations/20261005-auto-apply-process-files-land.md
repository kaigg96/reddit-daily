---
title: Land the auto-apply extension you approved in #45 (one patch, yours to apply)
key: auto-apply-process-files-land
labels: needs-owner,process
raised_at: 2026-10-05T18:29:43+00:00
---

## What happened

You approved #45: let approved changes to the skill files and `CLAUDE.md` land automatically, under the same checks as workflow changes. The change is built and tested. It touches `apply-approved.yml`, which only you land, so here it is as one patch. The three files must land together, because the escalation tool and the workflow have to accept exactly the same files. Without the workflow line, the new tests fail; with it, all 312 pass.

What it does:
- `scripts/escalate.py --patch` now accepts `.claude/skills/**` and `CLAUDE.md` as well as workflow files. It still never accepts `protect-process.yml` or `apply-approved.yml`.
- `apply-approved.yml` applies the same set. Every other check is unchanged: your label, the unedited issue, the sha256 fingerprint, and the allow-list checked on what git actually stages.
- Tests: an approved skill change and an approved `CLAUDE.md` change each land with `Approved-In: #N`. The two enforcing workflows and ordinary code are still refused.

`ORG.md` is guarded the same way but was not in #45's scope, so it is left out. Say so if you want it included.

To land it, from a clean checkout of `main`:

```sh
git apply auto-apply-process-files.patch   # the diff below, saved to a file
venv/bin/python -m pytest tests/test_apply_approved.py -q
git commit -am "Auto-apply approved skill and CLAUDE.md changes" -m "Approved-In: #45"
git push
```

```diff
diff --git a/.github/workflows/apply-approved.yml b/.github/workflows/apply-approved.yml
index 9710eee..da7c20a 100644
--- a/.github/workflows/apply-approved.yml
+++ b/.github/workflows/apply-approved.yml
@@ -9,8 +9,8 @@ name: Apply an approved workflow change
 #
 # It refuses unless: the owner applied the label; the issue was never edited
 # after it was raised, so the change is the one they read; the change matches
-# its recorded fingerprint; and it touches workflow files only -- never this
-# file or protect-process.yml. The machinery that checks approvals is never
+# its recorded fingerprint; and it touches workflow files, skills and CLAUDE.md
+# only (#45) -- never this file or protect-process.yml. The machinery that checks approvals is never
 # changed by the machinery it checks. protect-process.yml then re-checks
 # everything this pushes, because a push with this token triggers it.
 
@@ -96,11 +96,13 @@ jobs:
               return;
             }
 
-            // Workflow files only, never the two that enforce approvals. Checked
-            // on what git actually stages, not on how the patch describes itself.
+            // Workflow files, skills and CLAUDE.md only (#45), never the two that
+            // enforce approvals. Checked on what git actually stages, not on how
+            // the patch describes itself.
             const enforcers = ['.github/workflows/protect-process.yml',
                                '.github/workflows/apply-approved.yml'];
-            const allowed = p => p.startsWith('.github/workflows/') && !enforcers.includes(p);
+            const allowed = p => (p.startsWith('.github/workflows/') || p.startsWith('.claude/skills/')
+                                  || p === 'CLAUDE.md') && !enforcers.includes(p);
             fs.writeFileSync(`${tmp}/approved.patch`, patch);
             try { git(`apply --check ${tmp}/approved.patch`); }
             catch (e) {
@@ -114,7 +116,8 @@ jobs:
             const outside = staged.filter(p => !allowed(p));
             if (!staged.length || outside.length) {
               git('reset -q --hard');
-              await say('**Not applied:** auto-apply only changes workflow files, and never ' +
+              await say('**Not applied:** auto-apply only changes workflow files, skills and ' +
+                        'CLAUDE.md, and never ' +
                         'the two that enforce approvals. This touches ' +
                         (outside.map(p => `\`${p}\``).join(', ') || 'nothing') +
                         ', so it needs landing by hand.');
diff --git a/scripts/escalate.py b/scripts/escalate.py
index 012c83c..16450ce 100755
--- a/scripts/escalate.py
+++ b/scripts/escalate.py
@@ -37,7 +37,8 @@ import sys
 ROOT = pathlib.Path(__file__).resolve().parents[1]
 QUEUE = ROOT / ".escalations"
 
-# A shift cannot push workflow files. With --patch it attaches the exact change
+# A shift cannot push workflow files, and process files (skills, CLAUDE.md) land
+# only with the owner's approval (#45). With --patch it attaches the exact change
 # instead, and .github/workflows/apply-approved.yml applies it once the owner
 # labels the issue `approved`. These must match that workflow exactly.
 PATCH_MARKER = "<!-- apply-patch -->"
@@ -45,6 +46,11 @@ ENFORCERS = (".github/workflows/protect-process.yml", ".github/workflows/apply-a
 MAX_PATCH = 30000
 
 
+def patchable(path):
+    return (path.startswith((".github/workflows/", ".claude/skills/")) or path == "CLAUDE.md") \
+        and path not in ENFORCERS
+
+
 def validate_patch(text, repo=ROOT):
     """(inner text, sha256) of a patch auto-apply will accept, or exit saying why."""
     inner = text.rstrip("\n")
@@ -56,10 +62,10 @@ def validate_patch(text, repo=ROOT):
     paths = {p for pair in paths for p in pair}
     if not paths:
         sys.exit("escalate: not a git patch -- make it with `git diff -- .github/workflows/`")
-    bad = sorted(p for p in paths if not p.startswith(".github/workflows/") or p in ENFORCERS)
+    bad = sorted(p for p in paths if not patchable(p))
     if bad:
-        sys.exit("escalate: --patch is for workflow files only, and never "
-                 f"{' or '.join(ENFORCERS)}; this touches {', '.join(bad)}")
+        sys.exit("escalate: --patch is for workflow files, skills and CLAUDE.md only, and "
+                 f"never {' or '.join(ENFORCERS)}; this touches {', '.join(bad)}")
     # Against the index, so a shift that still has the edit in its working tree
     # is not told the change "already exists".
     check = subprocess.run(["git", "apply", "--check", "--cached", "-"], input=inner + "\n",
@@ -89,8 +95,8 @@ def main():
                     help="Comma-separated (default: needs-owner)")
     ap.add_argument("--recommend", help="Your recommendation — always give one")
     ap.add_argument("--body-file", help="Read body from a file instead of stdin")
-    ap.add_argument("--patch", help="A workflow change to apply once the owner "
-                                    "approves (git diff output; workflow files only)")
+    ap.add_argument("--patch", help="A change to apply once the owner approves (git diff "
+                                    "output; workflow files, skills and CLAUDE.md only)")
     args = ap.parse_args()
     patch = validate_patch(pathlib.Path(args.patch).read_text()) if args.patch else None
 
diff --git a/tests/test_apply_approved.py b/tests/test_apply_approved.py
index 96ebb2e..17da91c 100644
--- a/tests/test_apply_approved.py
+++ b/tests/test_apply_approved.py
@@ -64,6 +64,8 @@ def repo(tmp_path, env):
     git(r, env, "init", "-q", "-b", "main")
     for path, text in ((".github/workflows/demo.yml", "name: Demo\non: push\n"),
                        (".github/workflows/protect-process.yml", "name: Guard\n"),
+                       (".claude/skills/demo/SKILL.md", "# Demo\n"),
+                       ("CLAUDE.md", "# Rules\n"),
                        ("src/app.py", "print('hi')\n")):
         (r / path).parent.mkdir(parents=True, exist_ok=True)
         (r / path).write_text(text)
@@ -123,6 +125,15 @@ def test_the_approved_change_lands_exactly_and_the_issue_closes(repo, env, tmp_p
     assert "Approved-In: #44" in message and message.startswith("tidy the demo")
 
 
+@pytest.mark.parametrize("path", [".claude/skills/demo/SKILL.md", "CLAUDE.md"])
+def test_approved_process_file_changes_land_too(repo, env, tmp_path, path):
+    """#45: an approved skill or CLAUDE.md change no longer waits on a hand edit."""
+    inner, sha = escalate.validate_patch(diff_of(repo, env, path, "# Changed\n"), repo=repo)
+    out = apply(repo, env, tmp_path, issue_body(inner, sha))
+    assert out["closed"] and "**Applied**" in out["comments"][-1]
+    assert "Approved-In: #44" in git(repo, env, "log", "-1", "--format=%B")
+
+
 def test_an_edited_issue_is_refused(repo, env, tmp_path):
     inner, sha = escalate.validate_patch(
         diff_of(repo, env, ".github/workflows/demo.yml", "name: Demo 2\non: push\n"), repo=repo)
@@ -164,7 +175,8 @@ def test_without_the_token_it_says_so(repo, env, tmp_path):
     assert not out["closed"] and "not set up" in out["comments"][-1]
 
 
-@pytest.mark.parametrize("path", ["src/app.py", ".github/workflows/apply-approved.yml"])
+@pytest.mark.parametrize("path", ["src/app.py", ".github/workflows/apply-approved.yml",
+                                  ".github/workflows/protect-process.yml"])
 def test_escalate_refuses_what_auto_apply_would(repo, env, path):
     patch = diff_of(repo, env, path, "changed\n")
     with pytest.raises(SystemExit):
```

## Recommendation

Apply the patch below as it stands. It is tested, and nothing else changes until a later shift raises a skill or CLAUDE.md change for your approval.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*