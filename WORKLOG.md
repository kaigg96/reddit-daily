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

## 2026-09-20 (afternoon) — maintenance (preempted by a stale-then-real gate failure)

    Allocation (planned→actual %): rounds 10→5 · maintenance 15→70 · pm 15→15 · research 10→0 · feature 40→0 · close 10→10

Preempted by `.github/last-release-validation.md` reading FAIL against `main`
(§3 "Ship what's built"). Feature/research got nothing — correct given what
this turned into, not starvation.

**The recorded FAIL was stale, but re-checking surfaced a real, different
fault.** It validated `c6ee5f7`, the commit *before* this morning's own
reasoning-budget fix (`d59703f`) landed (`integration/preview` is 14 commits
behind `main`, not in play). Re-ran `scripts/validate_release.py` locally (6
requests, within the 8-request cap, >7h from the next scheduled run) to
confirm current `main` actually passes. **It didn't:** with reasoning already
restored, the R4.6 screen still missed a live paraphrase of the identical
`sexual_suggestive` shape ("...dangerously flirty?") while correctly catching
the literal in-prompt example ("...excellent in bed?"). One example doesn't
generalize a category.

**Fixed in `89bc245`:** added the paraphrase as a second calibration example
in `src/screen.py`'s prompt, pinned by a deterministic test needing no live
Gemini call. Also corrected this morning's code comment, which mis-attributed
the paraphrase to a confirmed zeroed upload it isn't (that upload's actual
text is the "excellent in bed" example already in the prompt). Full finding in
`TECH_DEBT.md`. Did not spend more quota re-verifying live today — commented
on issue #12 with the fix rather than closing it (no `workflow_dispatch`
permission to force a fresh CI run); tomorrow's 08:17 UTC gate is the
authoritative PASS/FAIL record.

**Also corrected PRD.md §0**, which still said `v6` was "pending owner review,
nothing merged" — it merged 2026-09-19. Folded the stale branch table into
Shipped history.

**Queued next:** confirm tomorrow's gate reads PASS against `89bc245`+ (if
still FAIL, it's a third fault); `replay_screen.py`'s FLIRT case is now a
memorization check, not generalization — swap in a fresh paraphrase before
trusting it again; shift-workflow completion still unproven; Pass 3 Tier 1
(R1.7 guard, `age_adjusted_residuals`).

**Same lesson as this morning, one level deeper: a fix verified once, live, is
a sample of one.** The 512-token fix looked solid against the one case it was
written for; a second, differently-worded case in the same category broke it
immediately.

## 2026-09-20 — maintenance (incident-led)

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→65 · pm 15→20 · research 15→0 · feature 35→0 · close 10→5

Preempted by two faults, so feature and research got nothing — correct under
the triage rules, not starvation.

**FAULT 1 — the screen lost its judgment, live.** The 08:17 CI gate failed:
with thinking disabled the R4.6 screen **passed** a `sexual_suggestive`
question backed by a confirmed zeroed upload. Disabling thinking everywhere
(2026-09-19) fixed title latency and silently broke the one genuine judgment
task. Fixed: the screen gets 512 reasoning tokens, everything else stays at
zero, pinned by a test. **The gate is the only reason this surfaced before it
cost an upload.**

**FAULT 2 — the first scheduled shift did nothing, and reported success.**
`claude-code-action` grants no shell/file access without `--allowedTools`, and
`/shift` had no `allowed-tools` frontmatter. Fixed. Generalisable half: **a
shift that leaves no trace is indistinguishable from one that never ran** —
every health signal reads `WORKLOG.md`, which a silent shift never writes. The
workflow now fails when a shift produces no handover. Logged in `TECH_DEBT.md`.

**The new telemetry proved itself immediately**: a 05:01 run shows
`title_ok=0 keywords_ok=0 cta_ok=0` — it hit a budget already exhausted before
the 07:00 reset, previously invisible. 16:15 came back all-`1` with a good
title; `title_style` was blank on the bad run, `C` on the good one.

**Queued next:** verify the shift workflow completes a real scheduled shift
(never has); Pass 3 Tier 1 R1.7/residuals; no automated video check exists.
(08:17-gate item resolved by the entry above.)

**Both faults were mine, both were caught by the checks rather than by
looking.** Green is not evidence.

## 2026-09-19 — first session (pre-dates the allocation model)

    Allocation (planned→actual %): rounds 0→0 · maintenance 0→30 · pm 0→50 · research 0→5 · feature 0→5 · close 0→10

Unplanned — built the workflow rather than running it. Merged `v6` to `main`
(details in `PRD.md` §0's Shipped history) and shipped `/shift` + `/audit`.
Most queued items resolved by later shifts: `gh` access, scheduled shifts, the
CI gate. **Still open:** `escalations.yml` discards the issue number it
creates, no key→number ledger. No automated *video* check — CI gates
prompts/tests, not a playable MP4.

**Every threshold in the workflow was an unvalidated guess** at the time —
caps, starvation windows, turn counts, allocation shape. Two shifts in, treat
them as still under test (`DECISIONS.md` D4, D5).
