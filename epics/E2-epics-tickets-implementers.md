# E2 · Work in epics: a generator, a filter, an orchestrator, many implementers
Status: active
Function: General management, Engineering
Deadline: none; its pilot is E1, which has one (2027-01-12)
Measure: format releases reaching viewers (one in the 31 days to 2026-11-14, a model swap Google forced)
Rule: set below under "How we will know", before any ticket starts

## Why now

In the month to 2026-11-14 the shifts made about 1,200 commits, and the only
format release was a model swap Google forced. Waiting on the owner was half of it (D16 removes that). The
other half is the size of the work: the idea helper proposes what one
70-minute shift can finish, and each shift starts cold, so nothing larger than
a shift is ever planned, and a shift spends its best attention re-deriving
context instead of building. The owner has had success elsewhere with the
model below and asked for it here (D16, PLAN C20), planned and built by shifts.

## The decision

**Roles are modes of a shift and agents inside it, not new scheduled jobs.**
The board in `epics/` says which role the next shift plays (`README.md`).

- **Generator.** Proposes epics, not tasks. Each names the scorecard number it
  moves, its riskiest assumption, the first slice that could ship alone, and
  its cost in shifts. `process/backlog.md` §1 is its method, lifted a level.
- **Filter.** A fresh agent that did not write the proposals, with the right
  to cut. It asks: does it move a number we can read at our volume, does it
  spend money (then no), is its first slice shippable in a shift or two, what
  is the cheapest test of its riskiest assumption. It keeps the opposite-order
  ranking the backlog already uses. Most proposals should die here.
- **Orchestrator.** Plans an approved epic into tickets with acceptance
  criteria, dispatches them, and judges what comes back against those
  criteria by re-running them. It never writes the change itself.
- **Implementer.** One ticket, one branch, nothing else in context. It
  reports each acceptance line with the command it ran and what it printed.

**State is files** (`README.md` says why), read and checked by one script.

**Lessons are part of acceptance (PLAN C19).** Every bounce, failed check,
review finding and revert is evidence from outside the agent that did the
work. The orchestrator turns it into a lesson in `process/lessons.md`: the
rule, its evidence, which role it applies to, and when to retire it. A
ticket's brief carries only the lessons that match its role and files, so
lessons reach the agent that needs them without bloating everyone's context.

**Rejected:** separate scheduled jobs per role (more workflow files, which
only the owner can land, and idle runs); GitHub issues as tickets (emails the
owner on every move); one long-lived orchestrator session (a shift's machine
is fresh every run).

## Out of scope

Changing the merge gates (`CLAUDE.md` §3), the experiment rules (D9, #18) or
the reviews' calendar. Small fixes still go straight through a shift: a
one-line bug does not need a ticket.

## How we will know (set 2026-11-15, D15's pattern)

T1 records the baseline before the pilot: format releases reaching viewers,
quota units per merged change, shifts that ended early for lack of ready work.
Read four weeks after T8 starts:

- **Keep** if at least one epic slice shipped through it, 60% or more of
  tickets were accepted first time, and units per accepted ticket are no more
  than 1.5 times the baseline units per merged change.
- **Change** if tickets bounce more than that (the scoping is the fault, fix
  the orchestrator's method) or cost more than that (fewer implementers at once).
- **Stop** if nothing shipped through it in four weeks, or it delayed E1.

The 60% and 1.5 are guesses, like D4's caps; the read should say so if they
turn out to measure the wrong thing.

## Assumptions to check

1. **True (T3, 11-15).** A CI shift can run implementers side by side (T3). If not, they run one
   after another and the model still holds; only the speed changes.
2. **True per shift, false at three shifts a day (T3, 11-16).** The usage allowance covers it: implementers multiply a shift's cost, and
   three shifts a day already exceed the 200-unit weekly cap the owner has
   been asked to raise. T3 measures the cost of two at once before more are tried.
3. Anthropic's published accounts of this pattern still read as recalled here
   ("Building effective agents": orchestrator-workers and evaluator-optimizer;
   "How we built our multi-agent research system": a worker needs an
   objective, an output format and clear boundaries, and should write results
   to files instead of passing them back through the lead). T2 reads them
   first-hand before quoting them.

## Tickets

### T1 · The board can be read and checked by one command
Status: done
Needs: none
Touches: scripts/epics.py (new), tests/test_epics.py (new), .github/shift-usage.csv (read only)
Context: `epics/README.md` defines the format. Model the script on `scripts/backlog_status.py`, which reads the status tables in PLAN.md and PRD.md.
Accept:
- [x] `venv/bin/python scripts/epics.py` prints every epic with its tickets grouped by status
- [x] `scripts/epics.py --next` prints the single next action by the order in README ("Four roles")
- [x] `scripts/epics.py --check` exits 1, naming the file and line, for: a missing header line, an unknown status, a `Needs` naming a ticket that does not exist, a `done` ticket with an empty `Evidence`, a `doing` ticket older than 12 hours, more than two `active` epics
- [x] a test runs `--check` on the committed `epics/` and passes; each failure above has its own test
- [x] the three baseline numbers under "How we will know" are written into this file with the commands that produced them
Evidence: 11-16, merged `783d015`. Re-run by the orchestrator on the branch: the listing, `--next` -> "ACCEPT E1 T2 …", `--check` -> "3 epics, 25 tickets: clean", exit 0; `pytest tests/test_epics.py` -> 21 passed; full suite on the merged tree 1,104 passed. Two fresh reviews: the committed-board test hung on the clock and CI's depth-1 clone, and `Needs: none (note)` read as a dependency; both fixed before merge. Baselines (31 days to 11-14): **format releases reaching viewers 1** (`v7s`, first upload 11-08; first timestamp per `format_version` in `upload_log.csv`); **7.7 quota units per merge** (902.6 units over 72 runs in `.github/shift-usage.csv`, 2026-10-14 to 11-13, / 117 first-parent merges on `main` by `git log --merges --first-parent`, less one sync; a proxy, since most changes land as direct commits); **16 of 72 shifts ended early for lack of ready work** (under 36 of 60 minutes and a handover saying nothing was ready, matched ±75 min across `WORKLOG.md`'s history; a heuristic, the weakest of the three).

### T2 · The four roles have written methods
Status: done
Needs: T1
Touches: process/epics.md (new), process/shift.md, process/backlog.md, scripts/context_budget.py, scripts/backlog_status.py
Context: this file's "The decision" is the outline. Read the two Anthropic articles named in assumption 3 first-hand and adopt only what fits; cite what you adopt.
Accept:
- [x] `process/epics.md` gives each role a procedure a cold shift can follow, in 1,200 words or fewer, and has a budget in `context_budget.py`
- [x] `process/shift.md` §3 sends a shift to `epics.py --next` before the ranked queue
- [x] `backlog_status.py` counts `ready` tickets of `active` epics as ready work, with a test
- [x] the fresh-context review required by `CLAUDE.md` §3 found no contradiction with `CLAUDE.md` §4 or `ORG.md` §2
Evidence: 11-15: `process/epics.md` (1,037 words, budget 1,200 in `context_budget.py`); the dispatch method is T3's (one message, foreground, worktrees). Not yet reviewed fresh; the first orchestrating shift reviews it with T1's wiring. 11-16, merged `783d015`: a fresh review found one contradiction with `CLAUDE.md` §4 (a ticket needing a paid key "ends in one ask") and five more blocking gaps (accept-first against "dispatch first", dispatch ignoring `active` and `Needs`, briefs silent on the Gemini and render allowances, L11 naming a tool that spends Gemini, gates weaker than §3); all applied, with L1, L2, L9, L12 and L13's evidence corrected. A second fresh review of the result found no contradiction.

### T3 · We know whether implementers can run side by side in CI
Status: done
Needs: T1
Touches: this file; process/epics.md if it exists
Context: a spike, one shift at most. Shifts run with `Agent` allowed and background agents refused (`.github/workflows/foreground_in_ci.py`); foreground agents sent in one message run together. Try two implementers on two trivial tickets, each isolated on its own branch or worktree.
Accept:
- [x] this file records the run id, whether both ran at once, whether each stayed in its own tree, and the shift's quota units against a normal shift's
- [x] assumption 1 and 2 above are each marked true or false with that evidence
- [x] the dispatch method chosen (side by side, or one after another) is written where T4 will read it
Evidence: early, ahead of T1 (11-15, run 43749661055, E1's T3 and T6 plus a read-only challenger, three foreground agents in one message): **assumption 1 true:** they returned together after ~11 minutes (19:01 to 19:12), the longest one's own 651 s, against 1,160 s summed; each implementer worked in its own worktree (`isolation: worktree`) and pushed its own branch, and neither diff touched the other's files. **Assumption 2 unmeasured:** this run's row in `.github/shift-usage.csv` lands after the shift; compare it with the three before it (8.2–11.1 units). Dispatch method, for T4: side by side, all agents in one message, since a background agent is refused and a lone foreground one blocks the orchestrator.
11-16: run 43749661055's row reads 10.48 units over 47.7 minutes, inside the 8.2–11.5 of the shifts before it, so either a round costs little or `shift-usage.csv` does not count subagents' tokens; which one is the line left (compare this shift's row, run 43856314698, seven rounds, when it lands). Dispatch method written in `process/epics.md` (merged 11-16). 11-16 (21:00 shift): run 43856314698, seven rounds, reads **14.19 units** over 44.4 min and 100 turns, above the 8.2–11.5 of the ten shifts before it (11-13 to 11-15, no rounds), at 0.14 a turn against their 0.07–0.10. Cost rose with rounds while turns did not, so `quota_units` (the action's `total_cost_usd`) counts subagents. **Assumption 2:** a heavy round shift costs about 1.4× the band's median, which fits inside one shift's share; but three shifts a day at ~10 units already run past the 200-unit weekly cap, so routine rounds every shift do not fit until the owner's raise lands (PLAN, the allowance variable). Rounds stay at what a ticket needs, as `process/epics.md` says.

### T4 · An implementer's brief is built from its ticket alone
Status: done
Needs: T2, T3
Touches: scripts/epics.py, tests/test_epics.py, process/epics.md
Context: the brief is the implementer's whole world, so it is generated, not written by hand: ticket text, `Touches`, the gates that apply, the matching lessons (T7 adds them), and the report format.
Accept:
- [x] `scripts/epics.py brief E2 T4` prints a complete brief and nothing from any other ticket or epic, with a test
- [x] the brief ends with the report format: branch, what changed, each `Accept` line with the command run and its output, what could not be done
- [x] one real ticket was implemented from a generated brief and its report followed the format
Evidence: 11-18 (01:37 shift), implementer from a hand-written brief on `e2-t4-brief` (`74547e6`). Re-run by the orchestrator: `epics.py brief E2 T4` exit 0, 54 lines, T4's own heading, Needs, Touches, Context and Accept, no Status or Evidence, nothing of the epic's prose or a sibling (grep for T3, T5, "Why now", "The decision": 0); it ends with the report block, one line per Accept; `brief E2 T99` exit 2. Fresh review: nothing blocking, 27 tickets checked for leaks; its two should-fixes fixed (`lessons_for` matched "any" only as the first clause, so L9 reached no brief; a fixture-board test read the live lessons file) in `851ec19`. Merged, 1,440 pass. Left as nits: the quote regex would cut a gates sentence at an "e.g. "; `brief` must be the first argument; E1 T7's and E6 T2's Context say "above", which a brief no longer shows; the brief prints Accept lines already ticked.
Accepted 2026-11-18: Line 3: E2 T5 was dispatched from `epics.py brief E2 T5` (the generated text verbatim, plus four dispatch notes) and its report followed the format, every Accept line with its command and output; T4 done.

### T5 · Acceptance re-runs the criteria and leaves evidence
Status: done
Needs: T4
Touches: process/epics.md, scripts/epics.py, tests/test_epics.py
Context: README "Four roles" step 1. An implementer's report is a claim; the orchestrator's re-run is the evidence.
Accept:
- [x] `process/epics.md` states the procedure, the bounce rule (twice, then rewrite the ticket) and that the `CLAUDE.md` §3 gates run once per mergeable slice
- [x] `scripts/epics.py accept E<n> T<n> --evidence "…"` sets `done` and writes `Evidence`; `bounce … --why "…"` returns it to `ready` and appends the reason; both tested
- [x] each bounce also adds a line to the friction log (`scripts/friction.py add`)
Evidence: Accepted 2026-11-18: 11-18 (01:37 shift), implementer from a generated brief on `e2-t5-accept` (`907ff71`). Re-run: `pytest tests/test_epics.py` 30 passed; `bounce E2 T5` on a copy of the board changed only its Status and Evidence lines and wrote one friction row to the given log. Line 1: the Accepts paragraph already held it, one sentence added (1,194 of 1,200 words). Fresh review: not blocking; its two should-fixes fixed: a second bounce set `ready`, which `--next` would dispatch, now `todo`; a bounce dropped the old status (branch, commit), now kept as (was: …). Nits left: the friction row is written before the epic file, so a failed write leaves a row; the count includes bounces from before a rewrite. Merged `8661f9f`, 1,444 pass. This acceptance is the command's first use.

### T6 · Epics are proposed and cut before they are planned
Status: done
Needs: T2
Touches: process/backlog.md, process/epics.md, epics/ (new proposed files)
Context: "The decision", Generator and Filter. The filter must be a fresh agent. Expect it to cut most of what is proposed.
Accept:
- [x] one full round is recorded: at least four proposed epics, the filter's verdict and reason on each, at least one cut
- [x] cut epics appear in `backlog_status.py --dropped`, so the next round does not propose them again
- [x] no more than two epics are `active` afterwards (`epics.py --check`)
Evidence: 11-18 (01:37 shift). A generator agent (worktree, about 5 minutes) wrote five proposals on `e2-t6-proposals` (`188f67e`): E4 a play-along round past a minute, E5 where viewers leave, E6 what the hits in our genre share, E7 one command for "do we already know", E8 a merge that cannot land broken. A second fresh agent filtered them, ranking forward and reversed (both E6 > E8 > E7 > E5 > E4): **E6 approved, four cut**, each status line carrying its reason (`c02dcf7`). The filter checked the generator's claims and five did not hold (E4's "about as long as a reading": a narrated play-along episode is 16.9 s, so three are ~50 s, not past a minute; E6's "the only scan": three ran). Line 2 needed code: `--dropped` read only the work log, so `backlog_status.dropped_epics` now lists cut epics first, with a test (merged `9b44509` after a fresh review, nits only, the one that could drop a reason fixed; 1,435 pass). `venv/bin/python scripts/backlog_status.py --dropped` prints E4, E5, E7, E8 with their reasons. `epics.py --check`: 8 epics, clean, two active (E1, E2). E8's residue is already lesson L2. The round took about 15 minutes of a shift; the generator's 5 minutes is the cheap part and the filter's checking is where the value was.

### T7 · Lessons come from evidence and reach the agent that needs them
Status: done
Needs: T5
Touches: process/lessons.md (new), scripts/epics.py, tests/test_epics.py, process/review.md
Context: PLAN C19 and D16's brief. A lesson is never an agent's opinion of its own work. Seed the file from evidence that already exists: the friction log's groups (`.github/friction-groups.csv`) and review findings recorded in TECH_DEBT.md.
Accept:
- [x] each lesson has: the rule in one sentence, `Evidence:` (a commit, run id, issue or friction id), `Applies:` (a role, and optionally paths), `Retire when:`
- [x] `epics.py --check` fails a lesson with no evidence, and the file holds at most 30
- [x] `epics.py brief` includes exactly the lessons whose `Applies` matches the ticket's role and `Touches`, with a test
- [x] the weekly review (`process/review.md`) gains one step: a friction group with three or more entries becomes a lesson or a ticket, and a lesson with no new evidence in eight weeks is retired (11-15, `22816b9`)
- [x] at least five lessons are seeded, each with real evidence
Evidence: 11-15 (owner's session): 13 lessons from the friction groups with the most rows (G2, G16, G22, G19, G1, G15, G17, G18, G26, G27, G28) and the day's own rows (F346, F347), each with `Evidence:`, `Applies:`, `Retire when:`. 11-16 weekly review: L14–L16 from G30, G32, G33 (three or more rows each), same four fields; evidence counts refreshed on L1–L6.
Accepted 2026-11-18: 11-18 (01:37 shift), implementer from a brief on `e2-t7-lessons` (`dbbc9a3`). Re-run: `epics.py --check` clean on 16 lessons; `pytest tests/test_epics.py` 34 passed (fixture tests for no Evidence, a 31st lesson, five Touches sets); `brief E6 T1` (Touches PRD.md §4) lists L6, L7, L9, L13, L14, L16 and no `src/` lesson. The branch put process/lessons.md 29 words over its budget; trimmed. Fresh review: a Touches item with a note ("src/ (by merge of …)") missed its directory's lessons, and a prefix match let `PLAN.md.bak` match; fixed in `652103f` (an item matches on its first word), with a test. Left: L16's backticked `PRD.md` is a topic, now read as a path filter. Merged `4f18702`, 1,449 pass.

### T8 · E1's remaining tickets run through this workflow
Status: todo: 2 of 4 (T12, T13); T14 ready
Needs: T5
Touches: epics/E1-the-show-after-reddit.md
Context: the pilot. E1 does not wait for it: any E1 ticket due before this is ready is done the old way, by a shift directly.
Accept:
- [ ] at least four E1 tickets went from `ready` to `done` by dispatch and acceptance, with `Evidence` on each
- [ ] this file records, per ticket: accepted first time or bounced, and the shift's quota units
Evidence: 1 of 4 so far. **E1 T12** (11-20, 01:16 shift, run 44652295279): dispatched before T5 was done, its code being inert until 01-05; **accepted first time**; implementer ~6 min, 28 tool calls; the shift's quota units are run 44652295279's row in `shift-usage.csv`. The brief was enough to start cold; the one gap was the worktree having no `venv/` (the orchestrator named the interpreter). **E1 T13** (11-21, 00:47 shift, run 44846129038): **bounced once, accepted on the second round** by the same agent: round 1 shipped 32 of 40 because rule 4's rewording bar, written for Reddit titles, read every price hook as a rewording of the last; the orchestrator changed that rule, and round 2 shipped 52 (~6 + ~2 min, 27 tool calls). The brief went in as a `$(cat …)` that was not expanded; the implementer read the file itself (F401; `process/epics.md` now says to paste it).

### T9 · The read
Status: todo
Needs: T8
Touches: this file, DECISIONS.md, PLAN.md
Context: "How we will know". Quote the rule before any number.
Accept:
- [ ] four weeks after T8 started, the three measures are set beside their baselines and the rule is applied as written: keep, change or stop
- [ ] the verdict and what changes are recorded in `DECISIONS.md`, and PLAN C19 and C20 are closed or re-scoped
Evidence:
