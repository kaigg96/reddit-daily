# E8 · A merge to the live branch that cannot land broken
Status: proposed
Function: Engineering (with Reliability)
Deadline: none; most useful before E1's switch-on merges (by 2027-01-05)
Measure: new rows in friction groups G22 ("Merge mechanics show their breakage only after landing", 17) and G11 ("Tests not rerun after the last edit before a merge", 4), and fix commits landing within an hour of a merge to `main`
Rule: it worked if G22 and G11 together gain at most one row in the four weeks after every merge goes through the command, against 21 rows since the log began on 10-27.

## Why now

`main` is live: it uploads twice a day (CLAUDE.md §3). `friction.py groups`:
G22 has 17 rows, the second most of any open group, and G11 has 4 more.
Recent rows: F271 (a test passed or failed depending on whether the merge
was committed), F336 (a new test broke bet 1's clean merge), and F357 (two
branches on one module broke three tests, caught only by the full suite on
the merged tree). The fix that row names, "run the suite on the merged tree
before", is advice, and CLAUDE.md's opening says advice "has been ignored in
practice". E1's cutover means several branches merging onto one module
before 12 January.

## The decision

`scripts/merge.py <branch>` does the steps in order and refuses on any
failure. It merges onto the latest `main` in a temporary worktree, runs the
full test suite on that merged tree, then the docs check and the attribution
check from `guardrails.yml`. It refuses if any file changed after the last
test run. Only then does it push. Rejected: a git hook, which each fresh
checkout would have to install and which can be skipped silently. Also
rejected: required checks on GitHub, which are the owner's repository
setting and would need their login.

## Scorecard number it moves

None on the channel directly. It protects uploads landed against uploads
scheduled (Reliability's measure in ORG.md), which a broken `main` stops.

## Riskiest assumption and its cheapest test

That most G22 breakages would have shown up in a run on the merged tree,
rather than only in the live workflow. The cheapest test: sort the 21 rows
into "a merged-tree run catches it" and "only production shows it". Half a
shift, no API. **Run already? No.** The rows each name a lesson, and none
sorts them.

## First slice that ships alone

`scripts/merge.py` with the merged-tree test run and the refusal on later
edits, with tests using a throwaway repository. One shift.

## Cost in shifts

About two: the sort and the command (1), adding the docs and attribution
checks, making it the documented merge path, and the four-week read (1).

## Out of scope

Workflow files (an `escalate.py --patch` if a step needs one). Branch
protection. Speeding up the test suite.

## Assumptions

1. The full suite runs in a few minutes on a shift's runner, so running it
   every merge is affordable inside a 70-minute shift.
2. The checks in `guardrails.yml` can be run locally without the secrets
   that workflow holds.
