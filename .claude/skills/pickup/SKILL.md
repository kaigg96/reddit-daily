---
name: pickup
description: Start a session on the reddit-digest media company (its first product is a YouTube Shorts channel). Orients from the plans, reports where things stand, applies the standing conventions, and closes the loop so the next session inherits accurate state. Use at the beginning of any new session, with or without a specific task.
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
2. **`PRD.md` §0 "Delivery plan"** — the product's tracker: shipped, next
   keepers, experiment backlog with pre-committed decision rules, open owner tasks.
3. **`PLAN.md`** — the company's: its goal, the queue for every function
   outside the product, its risks, and when each review last ran. Who owns
   what is in `ORG.md`, read when a task needs it.

Then read further **only as the task requires** — `PRD.md` §4 (Findings) for
anything touching metrics or experiments, §6 for a specific requirement's spec,
`TECH_DEBT.md` for code-health work.

Do not reconstruct state from `git log`, the code, or an old conversation. If
§0 and the code disagree, say so — that's a finding, not something to silently
work around.

## 2. Report, then work

Open with a few lines: what's shipped, what §0 says is next, and your
recommendation — including disagreeing with §0 if the data supports it.

Then **get on with it.** ~~Stop unless told to build~~ — that rule was retired
2026-09-19; the owner would rather work proceed than wait on a go-ahead. For a
session with no specific task, use **`/shift`**, which ranks the one queue
across the company's functions and carries the authorization rules and
external budgets. What still needs the
owner is listed in `CLAUDE.md` §4, and the usage reserve in §2.

## 3. Conventions

Follow the **"Standing conventions"** list in `README.md` as binding. It is
deliberately not copied here so the two can't drift.

## 4. Kinds of task

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

- **Update `PRD.md` §0 and `PLAN.md`** whenever anything ships or a company
  item moves, and propagate the result to
  any requirement that was waiting on it — a measurement often settles a
  deferred decision elsewhere in §6.
- **Record findings you don't fix** in `TECH_DEBT.md` → "Open items (logged
  between passes)". A diagnosis left in a commit message is invisible.
- **Tests pass**: `venv/bin/python -m pytest tests/`.
- **Don't commit verification side effects.** `scripts/weekly_analytics.py`
  appends real rows to `analysis/`. If you ran it to check something, revert
  that file before committing.
