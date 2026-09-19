# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

---

## 2026-09-19 — maintenance + project management

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

**Blocked — needs Gemini quota, run after 07:00 UTC:**
1. `scripts/replay_screen.py` — validates `named_wrongdoing` (open since
   2026-09-09) *and* whether the screen's verdicts survive thinking being
   disabled. **Gates the whole preview branch.**
2. One `llm.get_metadata` call — the merged prompt is unvalidated; merging
   three focused prompts into one multi-task prompt can degrade each task.

**Queued next:**
- Run both validations, then ship `integration/preview`.
- Pass 3 Tier 1: extract and test the R1.7 duration guard; reconcile the two
  `age_adjusted_residuals` implementations (they disagree by 14% on slope).
- Decide the shift trigger: scheduled cloud routines need a permission grant
  *and* a way to reach the secrets — GitHub Actions `dry_run` is the likely
  verification substrate.

**Self-inflicted:** this session exhausted the day's Gemini quota, so the
~04:50 UTC upload on 2026-09-20 will ship with a raw title and backstop
screening. The rule in the shift skill (§5) exists because of this.
