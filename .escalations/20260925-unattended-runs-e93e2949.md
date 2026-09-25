---
title: Approve: stop shifts ending at milestones (Opus 5.5 guidance)
key: unattended-runs-e93e2949
labels: needs-owner
raised_at: 2026-09-25T02:59:49+00:00
---

You approved this in conversation on 2026-09-25, after we read Anthropic's new
guide to prompting Opus 5.5. This issue is the formal approval.

## What it fixes

Anthropic's guide says Opus 5.5 sometimes stops to report on long unattended
runs, for example when a milestone is done. It ends its turn with a summary
instead of carrying on. Our shifts run unattended, so a turn like that ends the
whole shift. Both short shifts stopped right after a milestone: the new
opening's sample video passing, then the new opening going live.

The guide also says the model "usually finishes well before" any time budget
it is given. The deadline added two days ago may have been nudging shifts to
wrap up early.

## The change

- Each shift gets a standing instruction, adapted from Anthropic's recommended
  text, naming the stops you don't want. Status notes go alongside the next
  action, not instead of it. The stops you do want are kept: the handover,
  anything that needs you, and anything deliberately protected. Checks before
  risky actions are untouched.
- The deadline is reworded as time to use, not a target to beat.

Checked before proposing: the exact Claude Code version the shifts run accepts
the instruction file and follows it.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/shift-standing-instruction.md b/.github/workflows/shift-standing-instruction.md
new file mode 100644
index 0000000..52c97ed
--- /dev/null
+++ b/.github/workflows/shift-standing-instruction.md
@@ -0,0 +1,5 @@
+A standing instruction from the owner, the person you are working for. It is about how your turns end.
+
+You are running unattended: nobody reads your messages while you work. A message with no tool call in it ends your turn, and here that ends the whole shift: the work stops, and nobody is asked to continue. The owner has seen shifts end in four ways while work they asked for was still owed, and does not want any of them. One: a long summary of what was done that closes by announcing the next step and has no tool call, so the next thing never starts. Two: an offer to carry on with something unless the owner would prefer otherwise, which stops to wait for an answer that will not come. Three: a list of decisions for the owner when, by your own account, none of them blocks the rest of the work. Four: deciding that this is a good place to report, because the turn has been long or a milestone is done, such as a sample video passing or a change going live. Status notes are welcome, and so are your recommendations on open decisions, but put them in the same message as your next tool call and carry on with whatever does not depend on the owner's answer. If you notice yourself inviting the owner to redirect you or offering to wait, delete it and do the next thing.
+
+The stops the owner does want: the handover, once your WORKLOG entry is committed and pushed near your hand-over time; earlier only when nothing is ready and generating more work found nothing above the bar; and when nothing at all can move without the owner, or the thing blocking you is deliberately protected from you. Anything that needs the owner goes in an escalation while you carry on with the rest. This does not override the need for confirmation on risky or destructive actions, or any rule in CLAUDE.md.
diff --git a/.github/workflows/shift.yml b/.github/workflows/shift.yml
index af3049c..66c7b24 100644
--- a/.github/workflows/shift.yml
+++ b/.github/workflows/shift.yml
@@ -142,7 +142,7 @@ jobs:
           prompt: |
             ${{ inputs.prompt || '/shift' }}
 
-            Your clock: hand over by ${{ env.SHIFT_DEADLINE }} UTC. The job is killed at 30 minutes, taking an unfinished handover with it, so check `date -u +%H:%M` rather than guessing how much time is left. Ending with more than 8 minutes to spare means every lane is done, research and project management included: spare time goes to them, it does not end the shift.
+            Your working time runs until ${{ env.SHIFT_DEADLINE }} UTC. Use it: keep taking the next piece of ready work until about then, then commit and push your handover. The job is cut off at 30 minutes, taking an unpushed handover with it, so check `date -u +%H:%M` rather than guessing. Finishing early is not a goal: stopping with more than 8 minutes left means nothing is ready and generating more found nothing above the bar.
           # Without --allowedTools the action runs with NO shell or file
           # access, so the first scheduled shift "succeeded" having done
           # literally nothing. Blast radius is bounded elsewhere: this job has
@@ -155,6 +155,14 @@ jobs:
           # Scheduled runs get the defaults below; a dispatch can override both.
           # The first shift silently ran Sonnet because nothing set this.
           #
+          # The standing instruction is Anthropic's guidance for unattended runs
+          # on Opus 5.5 (prompting-claude-opus-5-5, "Unattended agentic runs"):
+          # the model sometimes ends a turn with a report at a milestone, and a
+          # headless run treats that as the end of the shift -- two shifts on
+          # 2026-09-24/25 stopped at 8 and 7 of 25 minutes right after one. The
+          # clock above says the time is to be used, because a model given a
+          # time budget "usually finishes well before it".
+          #
           # ultracode = xhigh plus dynamic-workflow orchestration. The owner's
           # call, and deliberate: a smaller amount of thorough, correct work
           # beats a larger amount of sloppy work. It spends quota faster, which
@@ -164,6 +172,7 @@ jobs:
             --model ${{ inputs.model || 'claude-opus-5-5' }}
             --effort ${{ inputs.effort || 'ultracode' }}
             --max-turns 400
+            --append-system-prompt-file ${{ github.workspace }}/.github/workflows/shift-standing-instruction.md
             --allowedTools "Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,TodoWrite,Task,Agent"
         env:
           GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
`````
patch-sha256: e93e29498b7642e729d8ff2c9c68650cf3c4748627f34a2eabb1335fbae60e59

## Recommendation

Approve — you've agreed it in conversation; it applies itself.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*