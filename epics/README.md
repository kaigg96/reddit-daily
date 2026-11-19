# Epics

Work larger than one shift lives here: one file per epic, its tickets inside
it. This is the board the owner asked for on 2026-11-14 (`DECISIONS.md` D16,
PLAN C20). The design, and the work of building it, is `E2`. Until `E2`'s first
tickets land there is no tool: read the files.

**Why files and not GitHub issues.** A shift starts on a fresh machine and
reads the repo first; a file needs no API call and no token, shows up in the
diff that changes it, and can be checked by a test. Every issue change also
emails the owner, who asked to be out of the loop.

## An epic file

`E<n>-<slug>.md`, opening with these lines, exactly:

```
# E3 · A name a viewer would understand
Status: proposed | approved | active | done | dropped: why
Function: the ORG.md function that answers for it
Deadline: a date, or none
Measure: the scorecard number it should move, or what exists when it is done
Rule: how we will know it worked, written before the first ticket starts
```

Then, in prose: **why now**, **the decision** (with the alternative rejected,
as `ORG.md`'s Decide level asks), **what is out of scope**, and the
**assumptions** a later shift should check. Then the tickets.

## A ticket

```
### T4 · One change, named by its result
Status: todo | ready | doing: <run id>, <UTC time> | review | done | blocked: why | dropped: why
Needs: T1, T3            (tickets that must be done first, or none)
Touches: the files or areas it may change
Context: everything the implementer needs, and nothing else
Accept:
- [ ] a statement someone else can check by running or reading something
Evidence: written at acceptance by the orchestrator: commit, command, result
```

A ticket is sized for one implementer in one sitting: if its `Accept` list
cannot be checked in a few minutes, it is two tickets. `ready` means every
`Needs` is `done` and the text is enough to start cold.

## Four roles, one shift at a time

A shift plays whichever role the board needs next, in this order:

1. **Accept** what is in `review`. The orchestrator re-runs each `Accept` line
   itself, records `Evidence`, and merges through the gates in `CLAUDE.md` §3.
   A ticket that fails goes back to `ready` with the reason; one that fails
   twice was written wrong, and the orchestrator rewrites it.
2. **Dispatch** `ready` tickets of an `active` epic to implementers: each one
   a fresh agent given its ticket and nothing else, on its own branch.
3. **Plan** an `approved` epic that has no tickets yet; one planned starts
   when an active slot frees, and no new round is proposed while it waits.
4. **Generate and filter**: propose epics, and have a fresh agent cut them.

At most two epics are `active`. Finishing comes before starting.

The orchestrator never implements, and an implementer never reads the board:
its whole world is one ticket. That is what keeps each context small enough
to do the work well.
