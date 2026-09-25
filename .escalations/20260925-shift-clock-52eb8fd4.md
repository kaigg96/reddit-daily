---
title: Approve: give shifts a clock, so they stop ending early
key: shift-clock-52eb8fd4
labels: needs-owner
raised_at: 2026-09-25T01:47:20+00:00
---

## What happened

This afternoon's shift stopped after **8 of its 30 minutes** and did no
research, saying "the shift has a 30-minute limit". It was nowhere near it.
A shift cannot see a clock: it knows it will be cut off at 30 minutes, and a
shift cut off mid-handover loses its work, so it guessed and played safe. The
two shifts before it used 18 and 24 minutes, so this is judgement under
uncertainty rather than a habit — but it is the uncertainty to remove.

## The change

- **Each shift is told the exact time it must hand over by**, and to check the
  time rather than guess. Stopping with more than 8 minutes to spare means every
  area is done, research and planning included.
- **The per-shift step limit goes from 200 to 400.** A shift that uses its full
  time takes about 180 steps, close enough to 200 that a busy one would be cut
  off and fail. The clock, not a step count, should end a shift.

## What it costs

Shifts will use more of their time: roughly 5–9 quota units each instead of
2–9. That is well inside the weekly limit, and you will not be using your
quota much while you are away.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/shift.yml b/.github/workflows/shift.yml
index ead9a11..af3049c 100644
--- a/.github/workflows/shift.yml
+++ b/.github/workflows/shift.yml
@@ -109,7 +109,13 @@ jobs:
 
       - name: Remember where this shift started
         if: steps.auth.outputs.ready == 'true' && steps.budget.outputs.proceed == 'true' && steps.minutes.outputs.proceed == 'true'
-        run: echo "START_SHA=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
+        run: |
+          echo "START_SHA=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
+          # The job is killed at 30 minutes and the agent has no clock of its
+          # own, so it guessed: on 2026-09-24 one stopped at 8 minutes, skipping
+          # research "because of the 30-minute limit". Its deadline now goes in
+          # the prompt. 25 leaves room for the handover and the steps after it.
+          echo "SHIFT_DEADLINE=$(date -u -d '+25 minutes' +%H:%M)" >> "$GITHUB_ENV"
 
       - uses: actions/setup-python@v5
         if: steps.auth.outputs.ready == 'true' && steps.budget.outputs.proceed == 'true' && steps.minutes.outputs.proceed == 'true'
@@ -133,7 +139,10 @@ jobs:
         if: steps.auth.outputs.ready == 'true' && steps.budget.outputs.proceed == 'true' && steps.minutes.outputs.proceed == 'true'
         with:
           claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
-          prompt: ${{ inputs.prompt || '/shift' }}
+          prompt: |
+            ${{ inputs.prompt || '/shift' }}
+
+            Your clock: hand over by ${{ env.SHIFT_DEADLINE }} UTC. The job is killed at 30 minutes, taking an unfinished handover with it, so check `date -u +%H:%M` rather than guessing how much time is left. Ending with more than 8 minutes to spare means every lane is done, research and project management included: spare time goes to them, it does not end the shift.
           # Without --allowedTools the action runs with NO shell or file
           # access, so the first scheduled shift "succeeded" having done
           # literally nothing. Blast radius is bounded elsewhere: this job has
@@ -154,7 +163,7 @@ jobs:
           claude_args: >-
             --model ${{ inputs.model || 'claude-opus-5-5' }}
             --effort ${{ inputs.effort || 'ultracode' }}
-            --max-turns 200
+            --max-turns 400
             --allowedTools "Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,TodoWrite,Task,Agent"
         env:
           GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
`````
patch-sha256: 52eb8fd42ccbfb54b05a6f1d4ab29095598adbea267cae770cf80f2d621c59c2

## Recommendation

Approve — it applies itself; shifts then use the time they have instead of guessing.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*