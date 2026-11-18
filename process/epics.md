# Working in epics: the four roles' methods

The board is `epics/` (its README gives the format and the order of play);
this file is how each role does its job. Written 2026-11-15 (E2 T2) from the
first day's evidence: three agents dispatched in one message ran side by side
in CI, each in its own worktree (E2 T3), and a lone agent blocks the shift
that sent it (F346). Change this on evidence, as any process text (D16).

## Which role, now

Read the board (`scripts/epics.py --next` once E2 T1 lands; until then the
files). After `process/shift.md` §2 items 1–5 (incident, ship what's built, a
due review, owner decisions, a closing window), the order never changes:
**accept** what is in `review`, **dispatch** `ready` tickets of an `active`
epic whose `Needs` are all `done`, **plan** what is `approved` and
unticketed, **generate and filter** only when nothing else is open. Finishing beats starting; a shift
that leaves work in `review` for the next one has chosen the slowest path.

The clock: a shift has 70 minutes and an agent round takes 10–15. Accept tickets
carried over in `review` first, then dispatch; accept this round's reports
last. Never leave a ticket
`doing` at hand-over: return it to `ready` with what was learned.

## The orchestrator

**Plans.** An `approved` epic becomes tickets a stranger could start cold:
one change each, named by its result, with `Touches` (the files it may
change), `Context` (everything needed, nothing else: the design is quoted or
linked, not implied) and `Accept` lines that someone else can check by
running or reading something in a few minutes. `Needs` is the dependency
graph; the first slice should be shippable alone. A ticket whose `Accept`
cannot be checked in minutes is two tickets.

**Dispatches.** Every agent of a round goes in **one message**, foreground,
with `isolation: worktree`, one ticket each, on its own branch named
`e<n>-t<n>-<slug>`. Background agents are refused in CI and a lone foreground
agent blocks the shift, so batching is the only way the orchestrator's time
is not spent waiting. Each brief is generated from the ticket by
`scripts/epics.py brief E<n> T<n>` (E2 T4), never written by hand: the ticket's
text, its `Touches`, the gates in `CLAUDE.md` §3 that apply, the lessons
whose `Applies` matches (`process/lessons.md`), the report format below, and
its allotment: by default no Gemini calls and no render requests, only free
`SAMPLE=1` renders and `scripts/replay_text.py`. The orchestrator spends the
shift's Gemini requests and its one render. Nothing else: not the board, not the epic, not another ticket. Three at once
is proven; more is measured before it is relied on (`shift-usage.csv`).

**While they run** the orchestrator does only read-only work, such as
reading the board; it plans the next round before dispatching. It never edits
a file an implementer's `Touches` names.

**Accepts.** A report is a claim. For each `Accept` line the orchestrator
re-runs the command or reads the thing itself, on the implementer's branch,
and records what it saw in `Evidence` (commit, command, result). Then the
gates once per mergeable slice, as `CLAUDE.md` §3 puts them: "Merge once the
gates pass: tests green, a fresh-context agent's review of the diff with its
findings fixed or recorded, a dry run producing a playable MP4 for anything
touching the video, `FORMAT_VERSION` bumped if the video changed, one
variable per release." A dry run's PASS must name the branch's current
commit. A ticket
that fails goes back to `ready` with the reason as a line under `Evidence`
and a row in the friction log; one that fails **twice** was written wrong,
and the orchestrator rewrites it before anyone tries again. Bounces are the
lessons file's main source (`process/lessons.md`).

**Records.** Status changes are made the moment they are true, in the epic
file, in the commit that makes them true. At dispatch the orchestrator sets
`doing: <run id>, <UTC time from date -u>`, and `review` when the report
lands; a note may follow any status after a colon. The handover names each ticket
moved and its state.

## The implementer

One ticket, one branch, one sitting. Read the brief and nothing else; if the
brief is not enough to start, say so in the report rather than guessing. Make
the change, run the tests the brief names, and report in this shape:

```
Branch: e1-t7-play-along (commit abc1234)
Changed: src/playalong.py (new), tests/test_playalong.py (new)
Accept:
- [x] "a test fails if the revealed value differs": venv/bin/python -m pytest tests/test_playalong.py -q -> 6 passed; the test test_reveal_matches_record fails when the value is altered (tried)
- [ ] "one narrated dry run is playable": not done, needs a dry run, which only the orchestrator requests
Could not do: ...
Learned: anything the next person on this file should know (one line each)
```

Never merge, never edit the board, never touch a file outside `Touches`
without saying so. Stop when every `Accept` line is met or a blocker is
found; a blocker reported in ten minutes is worth more than an hour's
workaround.

## The generator

Proposes **epics**, not tasks: work larger than a shift, each with the
scorecard number it moves (`report.py --scorecard`, `--routes`), its
riskiest assumption and the cheapest test of it, the first slice that could
ship alone, and its cost in shifts. It draws from evidence, as
`process/backlog.md` §1 says for candidates: the trajectory, the failures,
the findings (`PRD.md` §4), the risk register (`PLAN.md` §4), the friction
groups with the most rows, and `backlog_status.py --dropped` so the answered
are not re-proposed (G2, 19 rows). It writes each proposal as an epic file
with `Status: proposed` and no tickets.

## The filter

A **fresh agent** that did not write the proposals, with the right to cut,
given the proposals and the same evidence. For each: does it move a number
we can read at our volume (the chance gaps `report.py` prints)? does it
spend (then no, without appeal)? is its first slice shippable in a shift or
two? what is the cheapest test of its riskiest assumption, and has that test
already been run (`--dropped`, §4)? It ranks the survivors twice, in
opposite orders (`process/backlog.md` §2's bias method), and only an epic
that ranks well both ways is `approved`. It should cut most of what it sees;
a round that approves everything has not filtered. Cut epics get
`Status: dropped: <why>` and stay on the board a month, so the generator
sees them.

## Limits

At most **two** epics `active`. No ticket spends money or asks the owner for
a decision (`CLAUDE.md` §4). A render goes through `scripts/dry_run.py
request <branch>` (silent narration on a branch); a narration change is the
owner's run by hand; a workflow change goes through `scripts/escalate.py
--patch`; a paid key is never asked for, it is recorded in `PLAN.md`. A
one-way door (a channel rename) has `scripts/escalate.py --notice-days 7` in
its `Accept` and is not merged before the notice date. The usage
allowance is the owner's: a round of three agents costs about what a shift
does, so a shift dispatches at most two rounds, and the cost per accepted
ticket is read against E2's rule at its review.
