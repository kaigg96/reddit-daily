# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

---

## 2026-09-19 — maintenance + project management

**Standing audit (first one).** Context footprint measured and capped:
`scripts/context_budget.py` tracks what every session pays for, split into
always-loaded (`CLAUDE.md`) and read-at-startup. Now **75% of budget** —
`CLAUDE.md` pruned 1,173 → 540 words (54%) with all 19 binding rules intact;
what went was evidence and explanation, which lives in PRD §5 and is read on
demand. The check then caught the shift skill going over as the audit section
was added, which forced removing a duplicated "needs the owner" list — one
rule, one home. Adopted from Anthropic's best-practices doc: the
*"would removing this cause a mistake?"* test, CLAUDE.md as broadly-applicable
rules only with specifics in skills, and hooks/tests over advisory prose.
Deliberately not adopted yet: `/doctor` for automated cuts (untried here),
subagents for research isolation (worth trying next audit).

**Shipped:** nothing to `main` yet (authorization to self-merge arrived at the
end of this session). Seven branches assembled and green on
`integration/preview`, 83 tests.

**Found — two live bugs, both silent:**
- Gemini's default "thinking" pushed title generation past its 30s timeout:
  546 reasoning tokens for an 8-token title, 33.1s. **~25% of uploads for two
  weeks shipped the raw Reddit question as their title** (0% in W29–32 → 29%
  W37 → 25% W38). Disabled thinking: 0.6s.
- `insights.load_videos` dropped every 0-view upload, because the Analytics API
  returns no row for them. That hid **both surviving confirmed-suppression
  cases** from `report.py` — the entire evidence base for R4.6's skip
  categories. Zero-view count 1 → 4.

**Also:** Polly cost rules recorded (`CLAUDE.md`, new) and enforced in code;
title/keywords/CTA merged into one Gemini request (4–7 → 2–5 per run);
Pass 3 code-health findings proposed; two stale docs corrected.

**Measured, and it reframes things:** the Gemini free-tier cap is **20
requests/day**, not the few hundred assumed. Production spends 4–10.

**Was blocked on Gemini quota — now handled by CI.** Both gates run in
`validate-release.yml` at **08:17 UTC daily** (after the 07:00 reset, before the
~16:45 production run), against `integration/preview`, skipping itself when that
branch isn't ahead of `main`. Nobody needs to be awake for it.

1. `scripts/replay_screen.py` — `named_wrongdoing` (open since 2026-09-09) *and*
   whether the screen's verdicts survive thinking being disabled.
2. One `llm.get_metadata` call — the merged prompt is unvalidated.

**How the next shift picks this up:** read
`.github/last-release-validation.md` on `main` — CI commits the verdict there
precisely because a cold session has no GitHub token and can't read Actions
results. ✅ PASS → merge `integration/preview` to `main`. ❌ FAIL → an issue was
already opened; read it before touching the branch.

**Shipped to `main` this session:** the escalation path (`scripts/escalate.py` +
`escalations.yml`, verified end-to-end — the owner confirmed the email arrived),
the usage statusline, and the CI release gates.

**Queued next:**
- Merge `integration/preview` once CI says PASS (36 commits: v6 screen, Gemini
  fixes, analytics fix, metadata consolidation, shift workflow).
- Pass 3 Tier 1: extract and test the R1.7 duration guard; reconcile the two
  `age_adjusted_residuals` implementations (they disagree by 14% on slope).
- The release still has **no automated video check** — CI validates prompts and
  tests, not that a playable MP4 came out. `run-reddit-video.yml` already has a
  `dry_run` input; chaining it into the gate is the missing piece.

**Self-inflicted:** this session exhausted the day's Gemini quota, so the
~04:50 UTC upload on 2026-09-20 will ship with a raw title and backstop
screening. The rule in the shift skill (§5) exists because of this.
