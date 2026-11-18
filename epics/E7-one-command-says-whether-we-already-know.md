# E7 · One command says whether we already know the answer
Status: proposed
Function: General management (with Data)
Deadline: none
Measure: new rows in friction group G2 ("Recorded answers are hard to find, so work gets redone"), today 26, the most of any open group
Rule: it worked if G2 gains at most one row in the four weeks after the command lands, and shift traces show the generator and rankers calling it. Otherwise the search, not the habit, is the problem: say so in G2 and stop.

## Why now

`scripts/friction.py groups` (2026-11-18): G2 has 26 rows, more than any
other open group. The 11-16 weekly review reopened it after it "had come
back seven times". Its first fix, `backlog_status.py --dropped` listing
PRD §4's headlines (F227, 11-09), did not stop it. Later rows: F242 (a
closing note contradicted TECH_DEBT, read only afterwards), F265 (rankers put
two settled items first), F269 (a release's on-screen change was spread
across an issue, five comments and a branch), and F275 (a rule built and
then abandoned because PRD §4 already held the answer). Each costs minutes
and sometimes a whole item.

## The decision

`scripts/known.py <words>` searches every place an answer lives: PRD §4's
findings, `DECISIONS.md`, the experiment ledger, `TECH_DEBT.md`, the epics,
closed escalations and the work log's drops. It prints each hit's date,
headline and location, newest first. The generator, the rankers and anyone
setting a rule call it first. Rejected: another summary document, which goes
stale (G30). Also rejected: longer briefings, which the context budget
forbids and which are what G2's rows already had.

## Scorecard number it moves

None on the channel. It moves G2's row count and the minutes lost per
finished item (`friction.py report`).

## Riskiest assumption and its cheapest test

That a plain keyword search would have surfaced the answer in most G2
cases, rather than each needing judgement. The cheapest test: replay G2's
26 rows. For each, search those files for two or three words from its task
and note whether the answer appears in the top five hits. Half a shift, no
API. **Run already? No.** F227 built a listing, not a search, and no row
records a replay.

## First slice that ships alone

`scripts/known.py` over the files, with tests on two rows from the replay.
One shift.

## Cost in shifts

About two: the replay and the command (1), wiring it into the generator,
the rankers and the rule-setting step, then the four-week read (1, spread).

## Out of scope

Rewriting or moving any record. Semantic search with a model, which costs
Gemini quota. Pruning PRD §4.

## Assumptions

1. The process files the wiring touches can be edited on a branch. G8 says
   some cannot. If so, the command ships and the wiring is raised with
   `escalate.py --patch`.
2. The work log's drops stay greppable in the form `backlog_status.py
   --dropped` reads today.
