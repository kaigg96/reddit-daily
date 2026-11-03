---
title: Two shifts a day instead of three, so the weekly allowance stops leaving days with no shift?
key: shift-schedule-vs-allowance-8f8c895d
labels: needs-owner
raised_at: 2026-11-03T11:10:45+00:00
---

## What is happening

Shifts stop when the week's usage allowance is spent. You set it at 200 units, and a shift cannot raise it. A shift now costs about 12–16 units, so the allowance pays for 13–16 shifts a week. Three a day is 21. So the allowance runs out midweek, and every shift after that is skipped until Friday's 18:00 reset.

This has happened **three weeks running**: 5 shifts skipped on 15–16 October, 3 on 22–23 October, and 6 from 28 to 30 October. The last gap ran about 53 hours (28 October 17:46 to 30 October 22:58) with nothing checking the uploads or the money controls. The skips are recorded nowhere except the run list. This week's 8 shifts have spent 101 of the 200.

## The proposal

Two shifts a day instead of three: 11:17 and 19:17 UTC, dropping 03:17. At this week's 12.6 units a shift, 14 a week spend about 176 of the 200. **It is not a guarantee:** at last week's 15.2 a shift, 14 would spend about 213, so the last half-day before Friday could still go dark. Shifts' cost per shift is theirs to bring down. The patch below changes only the schedule line and its comments. It edits a `cron:` line; approved patches are applied with your token, so this job's failure emails very likely still go to you (#86).

One thing to know: GitHub has been starting our scheduled runs 2 to 8 hours late. The "03:17" shift has actually started between about 07:45 and 11:05 (this one began at 10:52), and the "11:17" one between 14:30 and 17:30. If you'd rather keep the morning start, reply "drop 19:17" and I'll change the patch.

## Cost and reversibility

No spending: shifts bill nothing per use, and this uses less of your reserve, not more. Total shift time per week stays about the same, spread evenly instead of stopping midweek. To revert, restore the one line.

## The alternative

Raise the allowance to about 300 to keep three a day. That uses more of the Claude reserve you keep for yourself, so it is your call. I don't recommend it while the channel earns nothing.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/shift.yml b/.github/workflows/shift.yml
index a12b536..fe60228 100644
--- a/.github/workflows/shift.yml
+++ b/.github/workflows/shift.yml
@@ -12,7 +12,7 @@ name: Run a shift
 
 on:
   schedule:
-    # Three a day, about an hour each, since the repo went public (2026-10-05).
+    # Two a day (11-03 monthly; three from 2026-10-05), about an hour each.
     # Standard runners cost no minutes there. Fewer, longer shifts beat more,
     # shorter ones up to a point: each shift pays ~5 minutes to orient, and a
     # sample video takes 5-10 minutes to come back, so a 25-minute shift kept
@@ -20,7 +20,9 @@ on:
     # context costs more than another hand-over would. 11:17 follows the 07:00
     # Gemini reset, the morning upload and the 08:17 validation; 19:17 follows
     # the evening upload. The concurrency group below queues any that overlap.
-    - cron: '17 3,11,19 * * *'
+    # Three a day spent the weekly allowance (~12.6-15 units a shift against
+    # 200) by midweek and left the channel without a shift until Friday.
+    - cron: '17 11,19 * * *'
   workflow_dispatch:
     inputs:
       prompt:
`````
patch-sha256: 8f8c895d6b9aa3c6ddf9b55285d5449ac2be54a62233b84d56aa4108d9c43e77

## Recommendation

Approve: two a day nearly always fits the allowance you set, so the channel stops going unwatched for a day or two each week. Raising the allowance instead would use more of your Claude reserve.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*