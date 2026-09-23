---
title: Approve: run shifts on Claude Opus 5.5
key: opus-5-5-model-bump
labels: needs-owner
raised_at: 2026-09-23T02:50:37+00:00
---

Anthropic released Claude Opus 5.5 on 2026-09-22 and Opus 5 moved to legacy
status. Shifts should run on the current model, but `.github/workflows/shift.yml`
is a protected path, so the change needs your approval before it can land.

## What the change does

Branch: `chore/opus-5-5`

- `shift.yml` — the shift model becomes `claude-opus-5-5` (default, and the
  fallback in both the `claude_args` and the usage-recording step). `claude-opus-5`
  stays in the manual-dispatch options list; it is legacy but available until at
  least 2027-07-24.
- `scripts/context_budget.py` — the session cost weights are recalibrated. Opus 5.5
  charges 5% of base input for a cache read where every earlier model charged 10%,
  and cache reads dominate a long agent session, so the old ratio would have
  overstated the cost of exactly what a shift does most. Output and cache-write
  ratios are unchanged; $4/$20 has the same shape as $5/$25.

The model ID was verified against Anthropic's model documentation rather than
inferred. A wrong ID fails the scheduled shift unattended, and shifts are the only
thing currently managing the channel.

## Verification

- `shift.yml` parses; dispatch input default and options confirmed
- 135 tests pass
- context budget check green

## One thing to decide separately

`shift_budget.py` reads `total_cost_usd` from the action rather than hardcoding
prices, so the weekly quota ledger follows the model automatically — no change
needed there. But Opus 5.5 is 20% cheaper per token, so the same real work now
reports roughly 20% fewer quota units, which makes the weekly runaway breaker
about 20% looser than when the ceiling was set.

Holding the same line would mean `SHIFT_WEEKLY_QUOTA_BUDGET` moving from 120 to
roughly 96. Recommend leaving it: that ledger is explicitly a runaway breaker
rather than a budget, and its own docstring records that the dollar-to-quota
mapping is already poor (15.45 units read as 38% used on the console). Flagging it
because it is a real loosening of a control, not because it needs action.

## What approving means

Label this issue `approved`. The change then re-lands with an `Approved-In: #N`
trailer citing this issue, which is what `protect-process.yml` checks. Without it,
the change is reverted automatically on push to main.

## Recommendation

Approve — Opus 5 is legacy as of today and the ID is verified. The only judgement call is the quota-ledger caveat, which needs no action.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*