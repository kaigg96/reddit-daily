---
title: Shifts are ending with most of their time unspent
key: process-capacity-underused
labels: needs-owner
raised_at: 2026-09-26T13:51:00+00:00
---

The last 3 shifts ran 19, 15, 7 of their 25 minutes (54%, threshold 60%), from the usage ledger. Ready work in the tracker now: 0 (floor 3).

Ending early is right only when nothing is ready and generating more found nothing above the bar. Below the floor, replenishing was the project-management lane's first job and was skipped; at or above it, shifts are stopping with work available.

## Recommendation

Read why each of the last three shifts stopped (WORKLOG) and fix that reason, not the symptom.

## What the 2026-09-26 shift found

Ready work reaches zero for a structural reason, not because shifts skip replenishing it:

- **Every build item waits on one bake.** Items 3 and 7 are blocked only by "one experiment at a time", so nothing can be built until the opening-seconds read (~4 October).
- **Research questions drain faster than data arrives.** New performance data lands once a week; the last two shifts answered about a dozen questions, and this shift found the rest already answered, too thin, or needing the 28 September snapshot.

**Recommendation:** let one alternating-days experiment run beside a whole-video change. The title-style test already ran that way alongside three releases and still gave a clean answer. That roughly doubles how many changes can be tested, without touching any safety or cost control. Queued for the next shift to rank in a separate pass; no rule changed yet.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*