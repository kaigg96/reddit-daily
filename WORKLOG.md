# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

**Every entry starts with an allocation line**, in exactly this shape, so the
next shift can compute starvation floors and `/audit` can see whether slices
are being finished or filled:

    Allocation (planned→actual %): rounds 10→8 · maintenance 15→25 · pm 15→12 · research 10→0 · feature 40→35 · close 10→10

`0` actual is fine and often correct — say why in the entry. Read it with
`venv/bin/python scripts/context_budget.py --allocation`.

---

## 2026-09-19 — first session (pre-dates the allocation model)

    Allocation (planned→actual %): rounds 0→0 · maintenance 0→35 · pm 0→45 · research 0→5 · feature 0→5 · close 0→10

Unplanned — this session built the workflow rather than running it. The zeros
in `planned` mark it as the outlier, not a starvation signal.

**Shipped to `main`:** escalation path (verified end-to-end — owner confirmed
the email), usage statusline, CI release gates.

**On `integration/preview`, 83 tests green, awaiting CI:** v6 screen retiering,
the Gemini thinking fix, the zero-view analytics fix, metadata consolidation,
and the shift/audit workflow.

**Two live bugs found, both silent** (detail in PRD §4 Findings): Gemini's
default thinking blew the 30s timeout, so **~25% of uploads for two weeks
shipped the raw Reddit question as their title**; and `load_videos` dropped
every 0-view upload, hiding **both confirmed-suppression cases** from
`report.py`. Also measured: the Gemini free tier is **20 requests/day**, not
the few hundred assumed.

**Queued next:**
1. CI validates `preview` at 08:17 UTC → read `.github/last-release-validation.md`
   on `main`. PASS means merge; FAIL means an issue is already open.
2. Pass 3 Tier 1 (`TECH_DEBT.md`): extract and test the R1.7 duration guard;
   reconcile the two `age_adjusted_residuals` implementations (14% apart).
3. No automated video check yet — CI gates prompts and tests, not that a
   playable MP4 came out. `run-reddit-video.yml` takes a `dry_run` input.

**Process friction noted:** the shift skill needed four rounds of word-shaving
before the real fix (splitting `/audit` out) became obvious; and `DECISIONS.md`
D1 records a decision whose assumption expired in two hours unnoticed.
