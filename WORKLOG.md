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

## 2026-09-20 — maintenance (incident-led)

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→65 · pm 15→20 · research 15→0 · feature 35→0 · close 10→5

Preempted by two faults, so feature and research got nothing — correct under
the triage rules, not starvation.

**FAULT 1 — the screen lost its judgment, and it was live.** The 08:17 CI gate
failed against `main`: with thinking disabled the R4.6 screen **passed** a
`sexual_suggestive` question backed by one of only two confirmed zeroed
uploads. Disabling thinking everywhere (2026-09-19) fixed title latency and
silently broke the one genuine judgment task. Fixed: the screen gets 512
reasoning tokens, everything else stays at zero. Verified live —
`skip_post/sexual_suggestive` in 5.4s. A test pins it. **The gate is the only
reason this surfaced before it cost an upload.**

**FAULT 2 — the first scheduled shift did nothing, and reported success.**
`claude-code-action` grants a prompt no shell or file access without
`--allowedTools`, and `/shift` has no `allowed-tools` frontmatter. Fixed in the
workflow. The generalisable half: **a shift that leaves no trace is
indistinguishable from one that never ran**, and every health signal built so
far reads `WORKLOG.md`, which a silent shift never writes — so they would have
reported "ok" forever. The workflow now fails when a shift produces no
handover. Logged in `TECH_DEBT.md`.

**The new telemetry proved itself immediately.** `2026-09-20T05:01` shows
`title_ok=0 keywords_ok=0 cta_ok=0` with `screen_source=gemini` — that run
fired before the 07:00 reset on the budget the previous session exhausted, so
the screen call landed and the metadata call hit the wall. Previously invisible.
`16:15` came back all-`1` with a good merged-prompt title. The R2.2 fix also
holds in production: the failed run logged a blank `title_style`, the good one
logged `C`.

**Queued next:**
1. **Verify the shift workflow actually works** — needs a manual *Actions → Run
   a shift → Run workflow*, or tomorrow's 09:17. It has never completed a real
   shift. Until it does, treat scheduled autonomy as unproven.
2. The 08:17 gate should now pass; confirm in `.github/last-release-validation.md`.
3. Pass 3 Tier 1 (`TECH_DEBT.md`): extract and test the R1.7 duration guard;
   reconcile the two `age_adjusted_residuals` implementations (14% apart).
4. No automated video check — CI gates prompts and tests, not that a playable
   MP4 came out.

**Both faults were mine, both were caught by the checks rather than by looking,
and both were invisible in their own success output.** That is the pattern to
watch for: green is not evidence.

## 2026-09-19 — first session (pre-dates the allocation model)

    Allocation (planned→actual %): rounds 0→0 · maintenance 0→30 · pm 0→50 · research 0→5 · feature 0→5 · close 0→10

Unplanned — this session built the workflow rather than running it.

**✅ MERGED to `main`.** `v6` live: the R4.6 screen retiering, the Gemini
thinking fix (ended ~25% of uploads shipping the raw Reddit question as their
title), the analytics fix that was hiding every zero-view upload including both
confirmed-suppression cases, metadata consolidation (4–7 → 2–5 Gemini requests
against a 20/day cap), and the `/shift` + `/audit` workflow. Approval chain
verified end-to-end: issue #11 labelled `approved`, merged with
`Approved-In: #11`, `protect-process.yml` checked the label and let it stand.

**⚠️ The Gemini gates have NOT run** — quota was exhausted. `validate-release.yml`
runs them at **08:17 UTC** against `main` and escalates on failure. **Read
`.github/last-release-validation.md` before trusting the screen or the merged
metadata prompt.** A FAIL means revert, not debug-in-production.

**Queued next:**
1. Check the 08:17 UTC validation verdict.
2. **Give the agent GitHub access** (`gh` CLI, or a fine-grained token scoped to
   this repo). Without it a session cannot read issues, Actions results, or the
   owner's replies — this session had to ask for an issue number by hand.
   Anthropic's best-practices doc recommends `gh` explicitly.
3. **`escalations.yml` discards the issue number it creates.** Nothing records
   key→number, so a later session cannot reference an escalation it raised.
   Append a ledger when filing.
4. Pass 3 Tier 1 (`TECH_DEBT.md`): extract and test the R1.7 duration guard;
   reconcile the two `age_adjusted_residuals` implementations (14% apart).
5. No automated video check — CI gates prompts and tests, not that a playable
   MP4 came out. `run-reddit-video.yml` already takes a `dry_run` input.
6. **Nothing schedules shifts.** Cloud routines were permission-denied; shifts
   are manual (`/shift`) until that is granted.

**Every threshold in the workflow is an unvalidated guess** — caps, waste and
starvation windows, turn counts, allocation shape. No shift has run. Treat the
first few as the experiment and report friction (`DECISIONS.md` D4, D5).
