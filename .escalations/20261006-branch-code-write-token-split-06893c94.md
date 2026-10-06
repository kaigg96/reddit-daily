---
title: Close the route by which unmerged code could change the live code (security, one patch)
key: branch-code-write-token-split-06893c94
labels: needs-owner,security
raised_at: 2026-10-06T11:04:45+00:00
---

## What this is

Two automated jobs run code from unmerged branches: the sample-video render and the daily release check. That code runs in the same job as a token that can change the live code. Pushes made with that token skip the guard that protects the process rules. Nothing suggests it has been misused. It was found by reading the workflow on 24 September.

## The change

Each job splits in two. The part that runs branch code can only read. A second, fresh part runs only the live code, then records the result and pushes. Today's review added two hardening details:
- The recording part does not keep its push token on disk while it checks the video.
- It takes only the one expected file from the branch part's output.

## Checked

- Both changes apply cleanly to the live code.
- The workflow files parse.
- All 337 tests pass with the changes applied.

They cannot be run end to end before approval. If something is wrong, sample renders or release checks fail. Uploads are not affected: the upload workflow is untouched.

## If it misbehaves

The next shift reverts it in one commit and re-raises a fixed version.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/dry-run.yml b/.github/workflows/dry-run.yml
index c396660..77238ce 100644
--- a/.github/workflows/dry-run.yml
+++ b/.github/workflows/dry-run.yml
@@ -22,8 +22,12 @@ on:
         description: 'Branch to render (a manual run skips the 12-hour limit)'
         required: true
 
+# The job that runs the branch's code gets no write access: a token that can
+# push, left beside unmerged code, could change main without starting the
+# guard workflows (TECH_DEBT, 2026-09-24). Only `record`, on a fresh runner
+# running main's code alone, can push.
 permissions:
-  contents: write   # record the verdict, clear the queue
+  contents: read
   actions: read     # render history, which the 12-hour limit reads
 
 concurrency:
@@ -34,7 +38,15 @@ jobs:
   render:
     runs-on: ubuntu-latest
     timeout-minutes: 25
+    outputs:
+      branch: ${{ steps.req.outputs.branch }}
+      go: ${{ steps.req.outputs.go }}
+      why: ${{ steps.req.outputs.why }}
+      code: ${{ steps.render.outputs.code }}
+      commit: ${{ steps.render.outputs.commit }}
     steps:
+      # Read-only token, so persisting it is harmless, and the queue check's
+      # git ls-remote needs it on a private repository.
       - uses: actions/checkout@v4
 
       - name: What to render
@@ -174,15 +186,81 @@ jobs:
           if-no-files-found: ignore
           retention-days: 14
 
+  # A fresh runner: nothing the branch's code did can reach this job's files.
+  # It re-checks the sample from main's code and redacts the log again, since
+  # the render job's copies of both ran beside the branch.
+  record:
+    needs: render
+    if: always()
+    runs-on: ubuntu-latest
+    timeout-minutes: 5
+    permissions:
+      contents: write   # record the verdict, clear the queue
+    steps:
+      # The playability check below parses a video that branch code made, so
+      # no write token sits in .git/config while it runs; the push step alone
+      # gets it.
+      - uses: actions/checkout@v4
+        with:
+          persist-credentials: false
+
+      - name: Fetch the sample and the log
+        if: needs.render.outputs.go == 'true'
+        uses: actions/download-artifact@v4
+        with:
+          name: dry-run-render
+          path: ${{ runner.temp }}/sample
+        continue-on-error: true
+
+      - name: Strip secrets from the log, from main's side
+        if: needs.render.outputs.go == 'true'
+        env:
+          S1: ${{ secrets.REDDIT_CLIENT_ID }}
+          S2: ${{ secrets.REDDIT_CLIENT_SECRET }}
+          S3: ${{ secrets.AWS_POLLY_ACCESS_KEY }}
+          S4: ${{ secrets.AWS_POLLY_SECRET_ACCESS_KEY }}
+          S5: ${{ secrets.GEMINI_API_KEY }}
+        run: |
+          python3 - "$RUNNER_TEMP/sample/render.log" "$RUNNER_TEMP/render.log" <<'PY'
+          import os, sys
+          src, dst = sys.argv[1], sys.argv[2]
+          text = open(src, errors="replace").read() if os.path.exists(src) else ""
+          for k in ("S1", "S2", "S3", "S4", "S5"):
+              v = os.environ.get(k, "")
+              if len(v) >= 6:
+                  text = text.replace(v, "***")
+          open(dst, "w").write(text)
+          PY
+
+      # The check needs moviepy and imageio-ffmpeg: main's pins, not the branch's.
+      - uses: actions/setup-python@v5
+        if: needs.render.outputs.go == 'true'
+        with:
+          python-version: '3.10'
+          cache: pip
+
+      - name: Install main's dependencies
+        if: needs.render.outputs.go == 'true'
+        run: pip install -r requirements.txt
+
+      - name: Is it a playable video?
+        if: needs.render.outputs.go == 'true'
+        run: |
+          python3 scripts/dry_run.py check "$RUNNER_TEMP/sample/final_askreddit_video.mp4" \
+            > "$RUNNER_TEMP/check.txt" 2>&1 || true
+          cat "$RUNNER_TEMP/check.txt"
+
       - name: Record the verdict where a shift can read it
         if: always()
         env:
-          BRANCH: ${{ steps.req.outputs.branch }}
-          GO: ${{ steps.req.outputs.go }}
-          WHY: ${{ steps.req.outputs.why }}
-          CODE: ${{ steps.render.outputs.code }}
-          COMMIT: ${{ steps.render.outputs.commit }}
+          BRANCH: ${{ needs.render.outputs.branch }}
+          GO: ${{ needs.render.outputs.go }}
+          WHY: ${{ needs.render.outputs.why }}
+          CODE: ${{ needs.render.outputs.code }}
+          COMMIT: ${{ needs.render.outputs.commit }}
           RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
+          GH_TOKEN: ${{ github.token }}
+          REPO: ${{ github.repository }}
         run: |
           if [ "$GO" = "true" ]; then
             python3 scripts/dry_run.py record --branch "$BRANCH" --commit "$COMMIT" \
@@ -197,6 +275,7 @@ jobs:
           git config --global user.email "github-actions[bot]@users.noreply.github.com"
           git add -A .github/last-dry-run.md .dry-run-requests
           git commit -m "Record dry-run verdict" || echo "unchanged"
+          git remote set-url origin "https://x-access-token:${GH_TOKEN}@github.com/${REPO}"
           for attempt in 1 2 3; do
             git pull --rebase origin main && git push && exit 0
             echo "push attempt $attempt failed; retrying"; sleep 5
diff --git a/.github/workflows/validate-release.yml b/.github/workflows/validate-release.yml
index ea2e958..f0081a7 100644
--- a/.github/workflows/validate-release.yml
+++ b/.github/workflows/validate-release.yml
@@ -19,9 +19,10 @@ on:
         required: false
         default: 'integration/preview'
 
+# The job that runs the branch's code cannot push (TECH_DEBT, 2026-09-24);
+# only `record`, on a fresh runner running main's code, writes.
 permissions:
-  contents: write
-  issues: write
+  contents: read
 
 concurrency:
   group: validate-release
@@ -32,6 +33,11 @@ jobs:
     runs-on: ubuntu-latest
     env:
       TARGET: ${{ inputs.ref || 'integration/preview' }}
+    outputs:
+      proceed: ${{ steps.check.outputs.proceed }}
+      target: ${{ steps.out.outputs.target }}
+      commit: ${{ steps.out.outputs.commit }}
+      code: ${{ steps.gates.outputs.code }}
     steps:
       - uses: actions/checkout@v4
         with:
@@ -106,13 +112,67 @@ jobs:
           python scripts/validate_release.py
           echo "code=$?" >> "$GITHUB_OUTPUT"
 
+      # Artifacts are readable by anyone who can read the repo, so the key is
+      # stripped before upload, not only before the commit.
+      - name: Hand the result to the record job
+        id: out
+        if: always() && steps.check.outputs.proceed == 'true'
+        env:
+          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}   # only to strip it
+        run: |
+          echo "target=$TARGET" >> "$GITHUB_OUTPUT"
+          echo "commit=$(git rev-parse --short "origin/$TARGET")" >> "$GITHUB_OUTPUT"
+          mkdir -p "$RUNNER_TEMP/detail"
+          if [ -f .github/last-release-detail.md ]; then
+            python3 -c 'import os, sys; k = os.environ.get("GEMINI_API_KEY", ""); t = open(sys.argv[1]).read(); sys.stdout.write(t.replace(k, "***") if len(k) >= 6 else t)' \
+              .github/last-release-detail.md > "$RUNNER_TEMP/detail/last-release-detail.md"
+          fi
+
+      - name: Keep the detail
+        if: always() && steps.check.outputs.proceed == 'true'
+        uses: actions/upload-artifact@v4
+        with:
+          name: release-detail
+          path: ${{ runner.temp }}/detail
+          if-no-files-found: ignore
+          retention-days: 3
+
+  # A fresh runner on main: nothing the branch's code did reaches this job.
+  # Not always(): tests and gates are continue-on-error, so a failed validate
+  # job is an infrastructure fault. Recording it would write a false FAIL with
+  # no escalation; skipping keeps the old verdict and shows a failed run, as
+  # the single job did.
+  record:
+    needs: validate
+    if: needs.validate.result == 'success' && needs.validate.outputs.proceed == 'true'
+    runs-on: ubuntu-latest
+    permissions:
+      contents: write
+      issues: write
+    env:
+      TARGET: ${{ needs.validate.outputs.target }}
+    steps:
+      - uses: actions/checkout@v4
+
+      # Branch code chose this artifact's files. Unpacked into .github they
+      # could overwrite tracked files, so take the one expected file only.
+      - name: Fetch the detail
+        uses: actions/download-artifact@v4
+        with:
+          name: release-detail
+          path: ${{ runner.temp }}/detail-in
+        continue-on-error: true
+
+      - name: Take only the detail file
+        run: |
+          mkdir -p .github
+          f="$RUNNER_TEMP/detail-in/last-release-detail.md"
+          if [ -f "$f" ] && [ ! -L "$f" ]; then cp "$f" .github/last-release-detail.md; fi
+
       - name: Record the verdict where a cold session can read it
-        if: steps.check.outputs.proceed == 'true'
         env:
           GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}   # only to strip it, below
         run: |
-          RESULT="${{ steps.gates.outcome }}"
-          git checkout main
           mkdir -p .github
           {
             echo "# Last release validation"
@@ -121,9 +181,9 @@ jobs:
             echo "needing live Gemini quota to find out whether the gates pass."
             echo
             echo "- **Branch:** \`$TARGET\`"
-            echo "- **Commit:** \`$(git rev-parse --short "origin/$TARGET")\`"
+            echo "- **Commit:** \`${{ needs.validate.outputs.commit }}\`"
             echo "- **When:** $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
-            case "${{ steps.gates.outputs.code }}" in
+            case "${{ needs.validate.outputs.code }}" in
               0) V='✅ PASS — safe to merge' ;;
               2) V='⚠️ INCONCLUSIVE — gates could not be exercised; not a failure' ;;
               *) V='❌ FAIL — do not merge' ;;
@@ -159,7 +219,7 @@ jobs:
       # recorded and left for the next scheduled run -- it means the gates
       # could not be exercised, not that the release is bad.
       - name: Escalate a failure to the owner
-        if: steps.check.outputs.proceed == 'true' && steps.gates.outputs.code == '1'
+        if: needs.validate.outputs.code == '1'
         uses: actions/github-script@v7
         with:
           script: |
@@ -199,5 +259,5 @@ jobs:
             }
 
       - name: Fail the run if the gates failed
-        if: steps.check.outputs.proceed == 'true' && steps.gates.outputs.code == '1'
+        if: needs.validate.outputs.code == '1'
         run: exit 1
`````
patch-sha256: 06893c940fae3e13da32a376a8cd559e7d9fa4ed4ea77d98325f88398456881f

## Recommendation

Approve. It closes the one route by which unmerged code could change the live code unseen, and uploads are untouched.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*