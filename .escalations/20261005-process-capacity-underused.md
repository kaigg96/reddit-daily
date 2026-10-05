---
title: Shifts are ending with most of their time unspent
key: process-capacity-underused
labels: needs-owner
raised_at: 2026-10-05T22:24:29+00:00
---

The last 3 shifts ran 16, 16, 21 of their 60 minutes (30%, threshold 60%), from the usage ledger. Ready work in the tracker now: 2 (floor 5).

Ending early is right only when nothing is ready and generating more found nothing above the bar. Below the floor, replenishing was the shift's first job and was skipped; at or above it, shifts are stopping with work available.

## Context from the shift that raised it (22:12 UTC)

This shift is using its full hour. The ready count is 2 because this shift finished or blocked three items (the format candidates, pricing the revenue routes, and the other platforms' terms, which now wait on your browser read), not because work was skipped. It generated new candidates and ranked them, and is working the top two.

Two of the three short shifts were today's reviews, which ended once the review was done. The review skill says a review is not a reason to hand over early, so the likely fix is that shifts are not reading that line, not a missing rule.

## Recommendation

Read why each of the last three shifts stopped (WORKLOG) and fix that reason, not the symptom.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*