---
title: The auto-revert rule cannot fire: a release is never age-matched against its own baseline
key: auto-revert-unfireable
labels: needs-owner,guardrail
raised_at: 2026-09-21T06:44:26+00:00
---

## What happened

`/shift` §5 authorizes a shift to merge its own work to `main`, including live-path
changes, and names one thing as the safety net that replaces your review:

> A release that degraded median watch-seconds or views against an age-matched
> baseline (`scripts/report.py --compare`) gets reverted.

That check can never return a verdict. A release is a flag-day change — every
upload after it has the new `format_version`, every upload before it has the old
one — so the two cohorts differ in age *by construction*, and `--compare`
correctly refuses an age-mismatched comparison. Run today against the committed
snapshot:

```
format_version=v4  n=57 med_age=36d  vs  !=v4  n=48 med_age=16d  -> not age-matched — unreliable
format_version=v5  n=34 med_age=13d  vs  !=v5  n=71 med_age=39d  -> not age-matched — unreliable
format_version=v6  n=0                                           -> insufficient data
```

Every release, every time. The same applies to the b-roll switch (R1.3), which
shipped in August with a recorded expectation and has never been checkable:
48 b-roll uploads at median age 16d against 57 procedural at 43d.

The refusal itself is right and I am not proposing to weaken it — an
age-confounded comparison is how this project reached four wrong conclusions in
two weeks. The problem is that the guardrail names a tool that structurally
cannot answer the question it asks.

## Why this is yours

It is a change to the rule that substitutes for your review of every merge,
in `.claude/skills/shift/SKILL.md` — the shift process itself. I have not
touched it.

It also matters more than it looks: four format versions and the b-roll library
have shipped under a rule that reads as "nothing ships unwatched", and nothing
has ever actually been watched. Nothing was reverted because nothing could
produce a verdict to revert on.

## Recommendation

Point the rule at the check that fits: `insights.age_adjusted_residuals` is
already written and tested, and its docstring says exactly this — *"use when
cohorts can't be age-matched; it removes the age trend rather than requiring
similar ages."* It has no `report.py` surface yet, which is why nobody noticed
the gap. Concretely:

1. You approve the rule wording changing from `--compare` to an age-adjusted
   residual check (this issue).
2. A shift builds `report.py --release <version>`: median residual of the
   release cohort vs the rest, with the same n-gate and zero-view handling as
   everything else, tests included. Ordinary code work, no approval needed.
3. The rule keeps its teeth: a materially negative residual still means revert.

Caveat worth knowing before you agree: residuals are computed on views only.
Watch-seconds has no age-trend model yet, so the first version of this check
would cover half of what the rule currently claims to cover. I would rather
ship the half that works and say so than keep a rule that covers nothing.

Not urgent — nothing is broken in production, and v6 is too young to evaluate
either way (it postdates the last analytics snapshot entirely).

## Recommendation

Approve swapping the rule's named check from --compare to an age-adjusted residual test, and let the next shift build the report.py surface for it

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*