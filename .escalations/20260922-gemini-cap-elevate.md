---
title: The Gemini cap is now blocking the top-ranked experiment — elevate it?
key: gemini-cap-elevate
labels: needs-owner,guardrail
raised_at: 2026-09-22T14:19:47+00:00
---

## Why this is being raised now

The rule for challenging a 🔄 constraint (PRD §5 no. 3) is that it has either
forced three or more workarounds, or begun blocking planned work. **Both are
now true**, so this is due — and noticing that is my job, while elevating it
is yours.

**Workarounds it has forced**, each sensible alone:

1. Three metadata prompts merged into one (2026-09-19).
2. Per-consumer request caps — production 10, release gate 8, a shift 8 — which
   sum past 20 with no shared ledger.
3. A skip so the release gate stops re-validating the same commit daily (#14).
4. The R4.6 screen never retries a 429, because one 429 means the whole day.
5. A cap on how many candidates may be screened per run.
6. Work timed around the 07:00 UTC reset.

**And it is now blocking planned work.** R4.4, the top item in the experiment
backlog, is priced out in the tracker's own words: a per-candidate scan "does
not fit the Gemini cap". It has been reduced to a telemetry prerequisite
instead of being run. That is the clearest possible signal — the constraint is
no longer just costing effort, it is choosing what we do.

**And it has cost real uploads.** The ~05:00 run is last in the daily window:
it shipped a raw Reddit question as its title on 2026-09-20 with the budget
gone. Until today the release gate was also spending 6 requests every morning
to re-learn the same stuck FAIL.

This matters more this week than last, because the channel now reads **FLAT** —
median watch-seconds 11.0 → 12.0 over six periods, inside its own drift. The
response to flat is to change what we ship, and the top-ranked candidate for
doing that is the thing this constraint is blocking.

## Three concrete routes, with costs

| | What it is | Cost | Risk |
|---|---|---|---|
| **A** | Move production's metadata call to a second model name. Our own 429 body names the quota `GenerateRequestsPerDayPerProjectPerModel` — **per model**, so a different model has its own 20/day. | **$0** | Titles/keywords/CTA come from a different model, so it is a format change needing a decision rule. Fully reversible. |
| **B** | A second Google Cloud project, i.e. a second free key for the same model. | **$0**, one new secret | No quality change at all. I do not know whether Google's terms permit running one workload across two projects' free tiers — **please check before choosing this**; I am not comfortable recommending it as if I did. |
| **C** | Pay-as-you-go on the current model. | A real invoice, but at 10–16 short requests a day it should be well under a dollar a month — worth confirming against current pricing. | Makes Gemini a **second billed service**, which PRD §5 no. 1 (🔄 $0 budget) forbids without you. |

**A is the one I would do**, because it costs nothing, needs no new secret, and
raises headroom where it is actually spent — production's own calls — while
leaving the full 20/day of the current model for the R4.6 screen, which is the
one genuine judgment task and the one I would least like to degrade. It needs
a pre-committed decision rule like any format change, and I would write one
before shipping it.

**C is the honest long-term answer** if you would rather not touch what
production calls: it removes the constraint instead of doubling it. But it
crosses the $0 line, so it is yours to decide.

If you would rather absorb the cap for now, say so and I will stop raising it —
but then R4.4 should be marked blocked in the tracker rather than sitting at
the top of the backlog looking actionable.

## Recommendation

Elevate it. Cheapest route first: move production's metadata call to a second model name, which has its own separate 20/day bucket and costs nothing. If you would rather not change what production calls, the paid tier is pennies a month at our volume — but that is a new billed service, which is your call, not mine.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*