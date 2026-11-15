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
(orchestrator, implementer, generator, filter, any) and optionally paths;
`Retire when:`.

## L1 · A fresh-context review before every merge, with its findings fixed or recorded
Evidence: G19 (13 rows); D2's re-reviews 10-28 to 11-12 ("fresh reviews caught ~19 defects since 10-28; gates caught none")
Applies: orchestrator (acceptance)
Retire when: a month of reviews finds nothing that would have shipped

## L2 · Rehearse the merge onto today's `main` and run the full suite on the merged tree before pushing
Evidence: G22 (13 rows); F240, F255 (`main`'s tests broke for minutes after pushes without a run on the merged tree)
Applies: orchestrator; implementer, `src/**`
Retire when: a month without a post-merge break

## L3 · Read `backlog_status.py --dropped` before proposing or researching
Evidence: G2 (19 rows; F157, F168, F201: answered findings re-proposed)
Applies: generator; filter
Retire when: ten generation rounds re-propose nothing answered

## L4 · A message to the owner is re-checked against today's facts at the moment it is sent
Evidence: G16 (14 rows: an ask's facts drifted after it was raised, or went out unchecked; #82's three corrections)
Applies: orchestrator (notices and asks)
Retire when: ten notices go out needing no correction

## L5 · Plan work that needs a render or Gemini around the allowance: free `SAMPLE=1` first, and an hour clear of an upload
Evidence: G1 (10 rows); F345 (a merge-ready tree waited a night for its check)
Applies: orchestrator (scheduling); implementer, `src/video.py`, `src/llm.py`, `src/run.py`
Retire when: `dry_run.py next` and the check's own scheduling make the window invisible (G1 closed)

## L6 · When a site refuses the fetch tool, use curl with a browser user agent or an archived copy
Evidence: G17 (7 rows)
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
Evidence: G15 (7 rows); 11-15: PLAN pushed 28 words over by the owner's session because a grep masked the check's exit code
Applies: orchestrator (records); any, `PLAN.md`, `PRD.md`, `WORKLOG.md`
Retire when: the check fails the push itself

## L10 · A handover entry goes after the template fence and the separator, newest first
Evidence: F347 (an entry inside the template block hid from the latest-entry reader and the stale-issue check)
Applies: any, `WORKLOG.md`
Retire when: a check refuses an entry inside the fence

## L11 · A text-rule change replays over every shipped line before it merges
Evidence: G26 (4 rows; `scripts/replay_screen.py`, the own-title cases)
Applies: implementer, `src/screen.py`, `src/llm.py`, `src/ownquestions.py`
Retire when: the replay runs in CI on those paths

## L12 · A review is run from its checklist file, each step ticked, not from memory
Evidence: G27 (a review step skipped when worked from memory)
Applies: orchestrator (reviews, acceptance)
Retire when: G27 gains no row in eight weeks

## L13 · Copy a result from the tool's output, never retype or truncate it
Evidence: G28 (hand-copied or truncated output misstated a result)
Applies: any (reports, evidence lines)
Retire when: G28 gains no row in eight weeks
