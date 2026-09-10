---
name: pickup
description: Start a session on the reddit-digest YouTube Shorts project. Orients from the delivery plan, reports where things stand, applies the standing conventions, and closes the loop so the next session inherits accurate state. Use at the beginning of any new session, with or without a specific task.
---

# Pick up work on reddit-digest

This project is worked on in short, separate sessions. This skill exists so each
one starts from the same place and leaves the tracker accurate for the next.

**Core rule: point, don't duplicate.** The living truth lives in the repo docs,
never in this file. Restating status or conventions here is how memory and
`PRD.md` drifted into contradicting each other once already. If something below
looks stale, the doc wins — fix the doc, not just this skill.

## 1. Orient — always, before anything else

Read, in this order:

1. **`README.md` → "Picking this up"** — reading order and the standing conventions.
2. **`PRD.md` §0 "Delivery plan"** — the single tracker: shipped, next keepers,
   experiment backlog with pre-committed decision rules, open owner tasks.

Then read further **only as the task requires** — `PRD.md` §4 (Findings) for
anything touching metrics or experiments, §6 for a specific requirement's spec,
`TECH_DEBT.md` for code-health work.

Do not reconstruct state from `git log`, the code, or an old conversation. If
§0 and the code disagree, say so — that's a finding, not something to silently
work around.

## 2. Report before building

Open with a few lines: what's shipped, what §0 says is next, and your
recommendation — including disagreeing with §0 if the data supports it.

Then **stop**, unless the invocation both named a task and told you to build.
Starting a phase or feature without an explicit go-ahead is a standing rule the
owner set after it happened.

## 3. Conventions

Follow the **"Standing conventions"** list in `README.md` as binding. It is
deliberately not copied here so the two can't drift.

## 4. Task lanes

- **Feature work** — branch first (`main` runs live twice daily). Dry-run the
  pipeline (`DRY_RUN=1 venv/bin/python -m src.run`) and show a sample before
  merging. Bump `FORMAT_VERSION` only for changes that alter the video itself;
  measurement-only work ships without a bump.
- **Code health** — follow the `TECH_DEBT.md` ritual: find the highest-leverage
  non-functional improvements, fix what's approved, defer the rest *with
  reasoning*.
- **Performance question** — `venv/bin/python scripts/report.py` only. If it
  refuses a comparison (thin cohort, ages not matched), that refusal is the
  answer. Needing a new capability means adding it to `src/insights.py` with a
  test, not writing analysis inline.
- **Incident / "the run failed"** — establish blast radius before fixing:
  which uploads, and is live state (`prev_post.txt`, `upload_log.csv`) intact?
  A lost `prev_post.txt` risks a duplicate upload on the next scheduled run.

## 5. Close the loop

Work isn't done until the next session can trust the tracker:

- **Update `PRD.md` §0** whenever anything ships, and propagate the result to
  any requirement that was waiting on it — a measurement often settles a
  deferred decision elsewhere in §6.
- **Record findings you don't fix** in `TECH_DEBT.md` → "Open items (logged
  between passes)". A diagnosis left in a commit message is invisible.
- **Tests pass**: `venv/bin/python -m pytest tests/`.
- **Don't commit verification side effects.** `scripts/weekly_analytics.py`
  appends real rows to `analysis/`. If you ran it to check something, revert
  that file before committing.
