---
title: Approve the company redesign: one queue, reviews, money checked every shift
key: company-redesign
labels: needs-owner
raised_at: 2026-10-05T17:58:16+00:00
---

## What this is

The redesign we worked out together on 5 October, on branch `org/responsibility-map`. It touches protected files (`CLAUDE.md`, the skills, three workflows, and the new `ORG.md`), so it needs your label to land.

## What changes

- **The company, not the channel.** Fourteen functions (`ORG.md`), each saying what it answers for and who decides: the shift alone, a proposal to you, or you only.
- **One ranked queue instead of time slices.** Shifts rank the product's work and the rest of the company's work together, on what moves the company toward revenue. The company's queue, risks and goal live in a new `PLAN.md`.
- **Reviews on a schedule.** A weekly review after Monday's data, a monthly business review written for you, and a quarterly packet of up to three bets for you to set. A due review becomes that day's shift. This adds no extra runs.
- **Money checked every shift.** A script reads your AWS controls with the read-only key, refuses to run as anything else, and escalates if anything drifts. A guardrail stops anyone raising its thresholds.
- **The shift report** leads with what moved the company toward revenue, and shows time by function.
- **`ORG.md` becomes protected**, like `CLAUDE.md`.

All 309 tests pass. The context budget is within limits, and every guardrail check passes locally.

## What you'll see first

The first shift after this lands runs the monthly review. That is your first business review. The weekly review and the quarterly packet follow on the next two shifts.

## Recommendation

Approve. Label this issue approved and the change lands as one commit naming it.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*