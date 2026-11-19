# Lessons

Rules a shift or an agent follows because something outside it showed the
need: a bounced ticket, a failed check, a review finding, a revert, a number.
Never an agent's opinion of its own work (D16's brief, PLAN C19). Seeded
2026-11-15 from the friction log's groups (`.github/friction-groups.csv`,
rows in `.github/friction.csv`); from E2 T7 on, `scripts/epics.py brief`
puts into each brief exactly the lessons whose `Applies` matches the
ticket's role and `Touches`, and `--check` refuses a lesson with no evidence.
At most **30**. The weekly review retires a lesson with no new evidence in
eight weeks and turns a friction group with three or more new rows into one.

Each lesson: the rule in one sentence; `Evidence:` ids; `Applies:` a role
(orchestrator, implementer, generator, filter, any) and optionally paths in
backticks, `;` between clauses; `Retire when:`. A clause with paths reaches
briefs whose `Touches` match one.

## L1 · A fresh-context review before every merge, with its findings fixed or recorded
Evidence: G19 (20 rows; 7 more by 11-16); D2's re-review of 11-05 ("Fresh reviews caught ~19 defects since 10-28; four dry runs and eight release checks caught none.")
Applies: orchestrator (acceptance)
Retire when: a month of reviews finds nothing that would have shipped

## L2 · Rehearse the merge onto today's `main` and run the full suite on the merged tree before pushing
Evidence: G22 (16 rows); G11 (F240, F255, F324) supports its second half, run the suite before pushing (`main`'s tests broke for minutes after pushes made without a run)
Applies: orchestrator; implementer, `src/**`
Retire when: a month without a post-merge break

## L3 · Read `backlog_status.py --dropped` before proposing or researching
Evidence: G2 (26 rows; F157, F168, F201: answered findings re-proposed; reopened 11-16, F265, F309, F311)
Applies: generator; filter
Retire when: ten generation rounds re-propose nothing answered

## L4 · A message to the owner is re-checked against today's facts at the moment it is sent
Evidence: G16 (16 rows: an ask's facts drifted after it was raised, or went out unchecked; #82's three corrections)
Applies: orchestrator (notices and asks)
Retire when: ten notices go out needing no correction

## L5 · Plan work that needs a render or Gemini around the allowance: free `SAMPLE=1` first, and an hour clear of an upload
Evidence: G1 (14 rows); F345 (a merge-ready tree waited a night for its check)
Applies: orchestrator (scheduling); implementer, `src/video.py`, `src/llm.py`, `src/run.py`
Retire when: `dry_run.py next` and the check's own scheduling make the window invisible (G1 closed)

## L6 · When a site refuses the fetch tool, use curl with a browser user agent or an archived copy
Evidence: G17 (9 rows)
Applies: any (research)
Retire when: the fetch tool stops being refused (G17 closed)

## L7 · Run a library on a sample before relying on how its code reads
Evidence: G18 (6 rows)
Applies: implementer
Retire when: G18 gains no row in eight weeks

## L8 · Every agent of a round goes in one message, foreground, each in its own worktree
Evidence: F346; E2 T3 (run 43749661055: three agents returned together in 11 minutes against 19 summed); `foreground_in_ci.py` refuses background agents
Applies: orchestrator (dispatch)
Retire when: CI allows background agents and the shift tool can wait on them

## L9 · A tracker over its budget is closed or trimmed before the push, never after
Evidence: G15 (7 rows); F324 (a `pytest | tail -1` inside an `&&` chain hid a failing test, so a merge pushed `main` with a malformed PLAN status)
Applies: orchestrator (records); any, `PLAN.md`, `PRD.md`, `WORKLOG.md`
Retire when: the check fails the push itself

## L10 · A handover entry goes after the template fence and the separator, newest first
Evidence: F347 (an entry inside the template block hid from the latest-entry reader and the stale-issue check)
Applies: any, `WORKLOG.md`
Retire when: a check refuses an entry inside the fence

## L11 · A text-rule change replays over every shipped line before it merges
Implementers use `scripts/replay_text.py <base> HEAD` (no model, no network); `scripts/replay_screen.py` spends Gemini per case, so it is an orchestrator-only step run an hour clear of an upload.
Evidence: G26 (4 rows; the own-title cases)
Applies: implementer, `src/screen.py`, `src/llm.py`, `src/ownquestions.py`
Retire when: the replay runs in CI on those paths

## L12 · A review is run from its checklist file, each step ticked, not from memory
Evidence: G27 (a review step skipped when worked from memory; seeded below the three-row bar)
Applies: orchestrator (reviews, acceptance)
Retire when: G27 gains no row in eight weeks

## L13 · Copy a result from the tool's output, never retype or truncate it
Evidence: G28 (hand-copied or truncated output misstated a result; seeded below the three-row bar)
Applies: any (reports, evidence lines)
Retire when: G28 gains no row in eight weeks

## L14 · Run a doc's claim about a tool or limit once before a plan rests on it
Evidence: G30 (F250, F283, F291, F351)
Applies: any
Retire when: G30 gains no row in eight weeks

## L15 · Edit one CSV or tracker row as a one-line replacement; read the diff stat
Evidence: G32 (F299, F304, F327)
Applies: any, `analysis/*.csv`, `.github/*.csv`, `TECH_DEBT.md`
Retire when: G32 gains no row in eight weeks

## L16 · Before pre-committing a rule, run its exact read once
Evidence: G33 (F247, F306, F320, F321)
Applies: any (ledger and `PRD.md` §0 rules)
Retire when: G33 gains no row in eight weeks
