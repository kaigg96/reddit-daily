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

    Allocation (planned→actual %): rounds 0→0 · maintenance 0→30 · pm 0→50 · research 0→5 · feature 0→5 · close 0→10

Unplanned — this session built the workflow rather than running it. The zeros
in `planned` mark it as the outlier, not a starvation signal.

**⛔ `integration/preview` is BLOCKED on owner approval.** It changes
`CLAUDE.md` and `.claude/skills/**`, which `protect-process.yml` guards. Issue
*"Approve the process rules built on 2026-09-19?"* is filed. When it carries
the `approved` label, land the branch with `Approved-In: #N` in the merge
commit — without it CI reverts the protected files.

**On `main`:** escalation path (verified end-to-end), usage statusline, CI
release gates, the approval request.

**On `integration/preview`, 83 tests green:** v6 screen retiering, the Gemini
thinking fix, the zero-view analytics fix, metadata consolidation, and the
whole shift/audit workflow.

**Two live bugs found, both silent** (detail in PRD §4 Findings): Gemini's
default thinking blew the 30s timeout, so **~25% of uploads for two weeks
shipped the raw Reddit question as their title**; and `load_videos` dropped
every 0-view upload, hiding **both confirmed-suppression cases** from
`report.py`. Also measured: the Gemini free tier is **20 requests/day**.

**Queued next:**
1. Get approval → merge `preview`. CI validates it at 08:17 UTC daily; read the
   verdict in `.github/last-release-validation.md` on `main`.
2. Pass 3 Tier 1 (`TECH_DEBT.md`): extract and test the R1.7 duration guard;
   reconcile the two `age_adjusted_residuals` implementations (14% apart).
3. No automated video check — CI gates prompts and tests, not that a playable
   MP4 came out. `run-reddit-video.yml` already takes a `dry_run` input.

**Every threshold in the workflow is an unvalidated guess** — caps, waste and
starvation windows, turn counts. No shift has run. First real shifts should
treat them as hypotheses and report friction (`DECISIONS.md` D4, D5).
