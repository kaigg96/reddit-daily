# E2 · Work in epics: a generator, a filter, an orchestrator, many implementers
Status: approved
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

1. A CI shift can run implementers side by side (T3). If not, they run one
   after another and the model still holds; only the speed changes.
2. The usage allowance covers it: implementers multiply a shift's cost, and
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
Status: ready
Needs: none
Touches: scripts/epics.py (new), tests/test_epics.py (new), .github/shift-usage.csv (read only)
Context: `epics/README.md` defines the format. Model the script on `scripts/backlog_status.py`, which reads the status tables in PLAN.md and PRD.md.
Accept:
- [ ] `venv/bin/python scripts/epics.py` prints every epic with its tickets grouped by status
- [ ] `scripts/epics.py --next` prints the single next action by the order in README ("Four roles")
- [ ] `scripts/epics.py --check` exits 1, naming the file and line, for: a missing header line, an unknown status, a `Needs` naming a ticket that does not exist, a `done` ticket with an empty `Evidence`, a `doing` ticket older than 12 hours, more than two `active` epics
- [ ] a test runs `--check` on the committed `epics/` and passes; each failure above has its own test
- [ ] the three baseline numbers under "How we will know" are written into this file with the commands that produced them
Evidence:

### T2 · The four roles have written methods
Status: todo
Needs: T1
Touches: process/epics.md (new), process/shift.md, process/backlog.md, scripts/context_budget.py, scripts/backlog_status.py
Context: this file's "The decision" is the outline. Read the two Anthropic articles named in assumption 3 first-hand and adopt only what fits; cite what you adopt.
Accept:
- [ ] `process/epics.md` gives each role a procedure a cold shift can follow, in 1,200 words or fewer, and has a budget in `context_budget.py`
- [ ] `process/shift.md` §3 sends a shift to `epics.py --next` before the ranked queue
- [ ] `backlog_status.py` counts `ready` tickets of `active` epics as ready work, with a test
- [ ] the fresh-context review required by `CLAUDE.md` §3 found no contradiction with `CLAUDE.md` §4 or `ORG.md` §2
Evidence:

### T3 · We know whether implementers can run side by side in CI
Status: todo
Needs: T1
Touches: this file; process/epics.md if it exists
Context: a spike, one shift at most. Shifts run with `Agent` allowed and background agents refused (`.github/workflows/foreground_in_ci.py`); foreground agents sent in one message run together. Try two implementers on two trivial tickets, each isolated on its own branch or worktree.
Accept:
- [ ] this file records the run id, whether both ran at once, whether each stayed in its own tree, and the shift's quota units against a normal shift's
- [ ] assumption 1 and 2 above are each marked true or false with that evidence
- [ ] the dispatch method chosen (side by side, or one after another) is written where T4 will read it
Evidence: early, ahead of T1 (11-15, run 43749661055, E1's T3 and T6 plus a read-only challenger, three foreground agents in one message): **assumption 1 true:** they returned together after ~11 minutes (19:01 to 19:12), the longest one's own 651 s, against 1,160 s summed; each implementer worked in its own worktree (`isolation: worktree`) and pushed its own branch, and neither diff touched the other's files. **Assumption 2 unmeasured:** this run's row in `.github/shift-usage.csv` lands after the shift; compare it with the three before it (8.2–11.1 units). Dispatch method, for T4: side by side, all agents in one message, since a background agent is refused and a lone foreground one blocks the orchestrator.

### T4 · An implementer's brief is built from its ticket alone
Status: todo
Needs: T2, T3
Touches: scripts/epics.py, tests/test_epics.py, process/epics.md
Context: the brief is the implementer's whole world, so it is generated, not written by hand: ticket text, `Touches`, the gates that apply, the matching lessons (T7 adds them), and the report format.
Accept:
- [ ] `scripts/epics.py brief E2 T4` prints a complete brief and nothing from any other ticket or epic, with a test
- [ ] the brief ends with the report format: branch, what changed, each `Accept` line with the command run and its output, what could not be done
- [ ] one real ticket was implemented from a generated brief and its report followed the format
Evidence:

### T5 · Acceptance re-runs the criteria and leaves evidence
Status: todo
Needs: T4
Touches: process/epics.md, scripts/epics.py, tests/test_epics.py
Context: README "Four roles" step 1. An implementer's report is a claim; the orchestrator's re-run is the evidence.
Accept:
- [ ] `process/epics.md` states the procedure, the bounce rule (twice, then rewrite the ticket) and that the `CLAUDE.md` §3 gates run once per mergeable slice
- [ ] `scripts/epics.py accept E<n> T<n> --evidence "…"` sets `done` and writes `Evidence`; `bounce … --why "…"` returns it to `ready` and appends the reason; both tested
- [ ] each bounce also adds a line to the friction log (`scripts/friction.py add`)
Evidence:

### T6 · Epics are proposed and cut before they are planned
Status: todo
Needs: T2
Touches: process/backlog.md, process/epics.md, epics/ (new proposed files)
Context: "The decision", Generator and Filter. The filter must be a fresh agent. Expect it to cut most of what is proposed.
Accept:
- [ ] one full round is recorded: at least four proposed epics, the filter's verdict and reason on each, at least one cut
- [ ] cut epics appear in `backlog_status.py --dropped`, so the next round does not propose them again
- [ ] no more than two epics are `active` afterwards (`epics.py --check`)
Evidence:

### T7 · Lessons come from evidence and reach the agent that needs them
Status: todo
Needs: T5
Touches: process/lessons.md (new), scripts/epics.py, tests/test_epics.py, process/review.md
Context: PLAN C19 and D16's brief. A lesson is never an agent's opinion of its own work. Seed the file from evidence that already exists: the friction log's groups (`.github/friction-groups.csv`) and review findings recorded in TECH_DEBT.md.
Accept:
- [ ] each lesson has: the rule in one sentence, `Evidence:` (a commit, run id, issue or friction id), `Applies:` (a role, and optionally paths), `Retire when:`
- [ ] `epics.py --check` fails a lesson with no evidence, and the file holds at most 30
- [ ] `epics.py brief` includes exactly the lessons whose `Applies` matches the ticket's role and `Touches`, with a test
- [ ] the weekly review (`process/review.md`) gains one step: a friction group with three or more entries becomes a lesson or a ticket, and a lesson with no new evidence in eight weeks is retired
- [ ] at least five lessons are seeded, each with real evidence
Evidence:

### T8 · E1's remaining tickets run through this workflow
Status: todo
Needs: T5
Touches: epics/E1-the-show-after-reddit.md
Context: the pilot. E1 does not wait for it: any E1 ticket due before this is ready is done the old way, by a shift directly.
Accept:
- [ ] at least four E1 tickets went from `ready` to `done` by dispatch and acceptance, with `Evidence` on each
- [ ] this file records, per ticket: accepted first time or bounced, and the shift's quota units
Evidence:

### T9 · The read
Status: todo
Needs: T8
Touches: this file, DECISIONS.md, PLAN.md
Context: "How we will know". Quote the rule before any number.
Accept:
- [ ] four weeks after T8 started, the three measures are set beside their baselines and the rule is applied as written: keep, change or stop
- [ ] the verdict and what changes are recorded in `DECISIONS.md`, and PLAN C19 and C20 are closed or re-scoped
Evidence:
