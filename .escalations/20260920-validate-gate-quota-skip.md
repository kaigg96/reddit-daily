---
title: Approve wiring the release gate's (already tested) skip, so it stops eating a third of the Gemini cap daily
key: validate-gate-quota-skip
labels: needs-owner,guardrail
raised_at: 2026-09-20T21:12:15+00:00
---

## What happened

`validate-release.yml`'s "don't re-validate a commit that already passed"
branch **can never fire**. Recording a verdict commits to `main`, so the next
morning `HEAD` is always at least one commit past the sha just recorded, and
the sha-equality check compares those two and re-runs. `a4fb38c` is the proof:
it names `c6ee5f7` and sits directly on top of it.

Cost: **6 of the day's 20 Gemini requests, every day, forever**, to re-learn
the same answer. That quota is shared with live uploads, and the ~05:00
publish is last in the 07:00-to-07:00 window, so it is the one that starves.
The 2026-09-20 05:01 upload shipped the raw Reddit question as its YouTube
title (`title_ok=0 keywords_ok=0 cta_ok=0`).

## Why this is yours

`.github/workflows/**` is a protected path, and the reason given in
`protect-process.yml` applies exactly: *"a shift able to edit it could disable
its own supervision."* This change reduces how often the gate that supervises
shifts runs, so it is a shift adjusting its own supervision — even though the
direction is "spend less and test more." I am not treating "it's an
improvement" as self-authorising.

Separately, **I could not have proposed it on a branch even if I wanted to.**
The push was rejected: *"refusing to allow a GitHub App to create or update
workflow `.github/workflows/validate-release.yml` without `workflows`
permission."* So the documented route in `.escalations/README.md` — "propose
freely on a branch, get approval, then merge" — is not actually available to a
CI shift for workflow files. The diff is inline below instead. Worth deciding
whether to grant the `workflows` permission, or to document the diff-in-issue
route as the real one.

## What has already landed (`4cfc1c4`, no approval needed)

`validate_release.should_validate` + 12 tests, and the PRD/TECH_DEBT
corrections. The function is **inert** until the workflow calls it, so `main`
behaves exactly as it does today until you approve the diff below.

## The change being proposed

- Skip the **Gemini gates** when nothing under `src`, `scripts`, `tests` or
  `requirements.txt` has changed since the last PASS — those are the only
  things that can alter the verdict.
- **Expire a PASS after 7 days** regardless, because `gemini-2.5-flash` can
  change behaviour under a pinned name with no commit of ours. Weekly drift
  detection at 6 requests/week instead of 42.
- **Run the unit tests unconditionally.** They are free, and this workflow is
  the only pytest run anywhere in CI — leaving them behind the skip would have
  traded a quota bug for a coverage gap. This is strictly more testing than
  today.
- Record in the verdict file that a verdict naming an older commit is not
  automatically stale, with the command to check. Two shifts in a row lost
  time to that question.

What it does **not** change: the gate still runs on every commit that touches
gated code, still fails loudly, still escalates, still records a verdict, and
a FAIL is still always retried.

## Residual risk I am not fixing

Nothing enforces the Gemini **total**. Production takes up to 10/day, the
gate allows itself 8, a shift allows itself 8 — 26 against a cap of 20, with
no shared ledger. This change makes starvation much less likely but cannot
rule it out. Logged in `TECH_DEBT.md`.

## The diff

````diff
diff --git a/.github/workflows/validate-release.yml b/.github/workflows/validate-release.yml
index d38a733..47b7e4c 100644
--- a/.github/workflows/validate-release.yml
+++ b/.github/workflows/validate-release.yml
@@ -6,8 +6,12 @@ name: Validate release gates
 # CI has the same secrets and no such constraint.
 #
 # Runs shortly after the reset and well before the ~16:45 UTC production run,
-# so a failed validation never starves a real upload. Skips itself entirely
-# when there is nothing to validate, because a pointless run still spends quota.
+# so a failed validation never starves a real upload. The Gemini gates skip
+# themselves when nothing they exercise has changed, because a pointless run
+# still spends quota the next upload needs -- the decision lives in
+# validate_release.should_validate, under test, since the sha comparison that
+# used to live here could never fire once a verdict commit landed on main.
+# The unit tests are free and run unconditionally.
 
 on:
   schedule:
@@ -37,61 +41,41 @@ jobs:
         with:
           fetch-depth: 0   # need main and the target ref to compare them
 
-      - name: Is there anything to validate?
-        id: check
+      - name: Resolve the ref under test
         run: |
           if ! git rev-parse --verify "origin/$TARGET" >/dev/null 2>&1; then
-            echo "branch $TARGET does not exist — nothing to validate"
-            echo "proceed=false" >> "$GITHUB_OUTPUT"; exit 0
-          fi
-          ahead=$(git rev-list --count "origin/main..origin/$TARGET")
-          echo "$TARGET is $ahead commits ahead of main"
-          # Nothing pending means nothing to gate, and a run would spend Gemini
-          # quota that production needs.
-          if [ "$ahead" -eq 0 ]; then
+            echo "branch $TARGET does not exist — gating main instead"
+            TARGET=main
+          elif [ "$(git rev-list --count "origin/main..origin/$TARGET")" -eq 0 ]; then
             # Nothing pending means the branch has merged. The gates must keep
             # running against what is LIVE -- otherwise merging silently
             # retires the only check on the prompts and the R4.6 screen.
-            echo "$TARGET is merged; validating main instead"
+            echo "$TARGET is merged; gating main instead"
             TARGET=main
-            echo "TARGET=main" >> "$GITHUB_ENV"
-          fi
-
-          # Don't re-validate a commit that already passed. A branch waiting to
-          # be merged would otherwise burn 6 of the day's 20 Gemini requests
-          # every morning to re-learn the same answer. A previous FAIL does get
-          # retried, because the commonest cause is an exhausted quota rather
-          # than bad output.
-          VERDICT=.github/last-release-validation.md
-          target_sha=$(git rev-parse --short "origin/$TARGET")
-          if [ -f "$VERDICT" ]; then
-            prev_sha=$(grep '^- \*\*Commit:\*\*' "$VERDICT" | grep -o '`[^`]*`' | tr -d '`' | head -1)
-            if [ "$prev_sha" = "$target_sha" ] && grep -q 'PASS' "$VERDICT"; then
-              echo "$target_sha already validated and passed — skipping to save quota"
-              echo "proceed=false" >> "$GITHUB_OUTPUT"; exit 0
-            fi
           fi
-          echo "proceed=true" >> "$GITHUB_OUTPUT"
+          echo "TARGET=$TARGET" >> "$GITHUB_ENV"
 
-      - name: Check out the branch under test
-        if: steps.check.outputs.proceed == 'true'
+      - name: Check out the ref under test
         run: git checkout "origin/$TARGET"
 
       - uses: actions/setup-python@v5
-        if: steps.check.outputs.proceed == 'true'
         with:
           python-version: '3.10'
           cache: pip
 
       - name: Install
-        if: steps.check.outputs.proceed == 'true'
-        run: pip install -r requirements.txt
-
-      - name: Unit tests
-        if: steps.check.outputs.proceed == 'true'
         run: |
+          pip install -r requirements.txt
           pip install -r requirements-dev.txt
-          python -m pytest tests/ -q
+
+      # Free, and the only pytest run anywhere in CI -- so it runs every day,
+      # including the quiet ones where the Gemini gates below are skipped.
+      - name: Unit tests
+        run: python -m pytest tests/ -q
+
+      - name: Do the Gemini gates need to run?
+        id: check
+        run: python scripts/validate_release.py --should-run --target "origin/$TARGET"
 
       - name: Gemini gates
         id: gates
@@ -118,6 +102,15 @@ jobs:
             echo "- **When:** $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
             echo "- **Verdict:** $([ "$RESULT" = "success" ] && echo '✅ PASS — safe to merge' || echo '❌ FAIL — do not merge')"
             echo
+            echo "A verdict naming an older commit is **not** automatically stale:"
+            echo "the gates re-run only when \`src\`, \`scripts\`, \`tests\` or"
+            echo "\`requirements.txt\` change, because nothing else can alter their"
+            echo "result and a pointless run costs 6 of the day's 20 Gemini requests."
+            echo "To check by hand:"
+            echo
+            echo '```sh'
+            echo "git diff --stat <commit-above> origin/main -- src scripts tests requirements.txt"
+            echo '```'
             echo "[Full output](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})"
           } > .github/last-release-validation.md
````

## Recommendation

Approve. It spends less quota, keeps the gate on every code change, adds a weekly drift re-check, and makes the unit tests run more often than they do today.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*