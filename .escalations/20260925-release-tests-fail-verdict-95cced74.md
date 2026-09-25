---
title: Record a FAIL when the release check's unit tests fail, instead of keeping yesterday's PASS
key: release-tests-fail-verdict-95cced74
labels: needs-owner
raised_at: 2026-09-25T01:59:14+00:00
---

**What:** when the daily release check's unit tests fail, the job stops before it records a verdict. The file shifts read therefore keeps showing the previous run's PASS, so a shift could merge on a stale "safe to merge". This is the open tech-debt item "A release check whose unit tests fail leaves the previous PASS in place".

**The change (patch attached, one workflow file):** the test step continues on failure. A failure is then recorded as ❌ FAIL, with the reason "Unit tests failed, so the Gemini gates were not run", and it goes through the existing failure escalation. The Gemini gates are skipped when tests fail, so broken code spends no quota. This tightens a gate and loosens nothing.

**Not tested in Actions**, because a shift cannot run workflows. The YAML parses, and the change reuses the step-outcome pattern the gates step already relies on.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/validate-release.yml b/.github/workflows/validate-release.yml
index e0ac3dc..ea2e958 100644
--- a/.github/workflows/validate-release.yml
+++ b/.github/workflows/validate-release.yml
@@ -82,7 +82,9 @@ jobs:
         run: pip install -r requirements.txt
 
       - name: Unit tests
+        id: tests
         if: steps.check.outputs.proceed == 'true'
+        continue-on-error: true    # a failure must replace yesterday's PASS, not leave it
         run: |
           pip install -r requirements-dev.txt
           python -m pytest tests/ -q
@@ -95,6 +97,12 @@ jobs:
           GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
         run: |
           set +e
+          if [ "${{ steps.tests.outcome }}" != "success" ]; then
+            # Failing tests are a FAIL; don't spend Gemini quota gating broken code.
+            echo "Unit tests failed, so the Gemini gates were not run." > .github/last-release-detail.md
+            echo "code=1" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
           python scripts/validate_release.py
           echo "code=$?" >> "$GITHUB_OUTPUT"
 
`````
patch-sha256: 95cced743cb472ad055e253dc2a7ec327dd3a58b6ad7a1f403383c83161b16b5

## Recommendation

Approve: it closes a way for a stale PASS to authorise a merge, spends no extra quota, and loosens nothing.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*