---
name: shift
description: Run an autonomous work shift on the reddit-digest channel — triage, pick the highest-value lane, do the work, ship it, and leave the next shift a clean handover. Use when a session starts with no specific task and should simply make the best use of available time. Covers maintenance, security, project management, research and feature work.
---

# Run a shift

A session with no task allocates its time across every workstream —
maintenance, security, project management, research, feature work — does the
work, ships it, and hands over, without the owner in the loop.

**Point, don't duplicate.** Status is `PRD.md` §0, code health `TECH_DEBT.md`,
conventions `CLAUDE.md`. Never keep a second copy of status here.

---

## 1. Orient (always, ~5 minutes)

Run the **`/pickup`** steps first. Do not re-derive state from `git log`.

Then read `WORKLOG.md` (repo root) — the last few shifts and what each one
queued for the next.

## 2. Plan the shift

```sh
venv/bin/python scripts/statusline.py --budget   # GO / BOUNDED / WRAP / STOP
```

**The owner keeps a reserve.** Work stops at 80% of the 5-hour window and 90%
of the weekly one — the rest is theirs; never plan around using it.

**`GO`** — take on real work: a feature through dry run and merge, or a deep
task like `/audit`. Fill the shift with what is genuinely worth doing; do not
default to something small. **`BOUNDED`** — one bounded task, finished.
**`WRAP`** — finish or park what's open. **`STOP`** — close the loop and end.

Then **allocate across every lane**, writing the plan into the `WORKLOG.md`
entry before starting. Two slices are fixed: **rounds ~10%** and **closing the
loop ~10%**. The remaining ~80% is split by how much genuinely valuable work
each lane actually has — not by a fixed percentage.

**Slices are ceilings, not quotas.** A lane finishes its valuable work and
stops rather than padding out its allocation — padding ships.

**But slack goes to PM and research, it does not end the shift.** Those two
always have work — a backlog to populate, constraints to question, decision
rules to check, and how channels like this grow. A thin maintenance or feature
day makes a PM-and-research shift, not a short one. Ending early is for when
even those have nothing above the value bar (§7), which should be rare.

Allocating honestly:

- **A lane with no actionable work gets 0%, and that is a finding**, not a
  failure. Say so in `WORKLOG.md`.
- **An empty feature lane is a project-management problem.** Give that time to
  PM to populate the backlog rather than inventing features to build.
- **Research has no ceiling**, but its output is governed by the value bar: a
  hypothesis with a proposed test, recorded in `WORKLOG.md`, no new documents.
  That bar is what stops it becoming busywork — not a percentage.
- **Starvation floor:** a lane at ~0% for **5 consecutive shifts** takes
  priority if it has queued work (check `WORKLOG.md`). A lane that keeps losing
  is the failure mode of every priority scheme.

## 3. Preemption — when one thing takes the whole shift

Not lanes competing for a slice — the shift's purpose that day. Check before
allocating:

1. **Incident.** Did both uploads land (`upload_log.csv` tail)? Did the last
   workflow run succeed? Is `prev_post.txt` intact? A missed or duplicated
   upload preempts everything.
2. **Ship what's built.** Read `.github/last-release-validation.md` on `main`;
   CI writes the verdict there, so you never need quota to find out. PASS means
   merge. Unshipped work is inventory, not progress.
3. **A closing window.** Work blocked on an external budget available *now*.

## 4. The lanes

**Maintenance** — is the pipeline healthy, are the logs sane, is anything
silently failing? *Fail-soft without telemetry looks identical to working.*
Instrument a silent fallback before fixing it.

**Security** — a standing check: secrets never committed and still ignored,
dependency advisories, workflow permissions, OAuth scope. Fix what is clearly
wrong; log the rest.

**Project management** — the lane that notices things. Standing jobs:

- **Has a decision rule come due?** Each experiment in `PRD.md` §0 carries one.
  Count uploads since the release and *act* — method in `/backlog` §4, which
  exists because this is the job the project has got wrong most often. An
  unevaluated experiment is worse than an unrun one: it looks like evidence.
- **Is the tracker true?** `scripts/check_docs.py` checks the checkable claims;
  judgement covers the rest (`/backlog` §5). Stale claims mislead worse than
  missing ones.
- **Is the next thing we'd build the highest-leverage thing?** If the feature
  lane is empty, filling the backlog is this lane's job (§2) — `/backlog` §1–2,
  because generating and ranking work has failure modes intuition walks into.
- **Is a constraint costing more than it buys?** `PRD.md` §5 marks each 🔒 or
  🔄. Three workarounds for one 🔄, or one blocking planned work, means it is due
  — `/backlog` §3. **Absorbing a recurring cost gracefully is how it becomes
  permanent.**
- **Record decisions** in `DECISIONS.md` with their assumptions — that is what
  makes them revisitable.
- **Do what the owner has already decided.** `scripts/escalations.py approved`
  lists what they have labelled — **work items, not questions**. Do them, then
  `escalations.py close <n> "…"`. Leaving one open keeps notifying them.
- **Chase closure:** `TECH_DEBT.md` at its cap, branches unmerged. Things must
  close, not accumulate.
- **`/audit`** is this lane's periodic deep task (§8).


**The workflow itself is always in scope here, not only at audit time.** Agentic
systems improve what they build and never question how they build it. If
something was awkward *this shift* — a rule that didn't fit, a step that added
nothing, state you had to re-derive, a gate you worked around — that is a
finding. Record it in `WORKLOG.md` even without acting: one shift's friction is
invisible alone, and `/audit` needs the pattern. Process changes are proposals
(§5), never self-applied.

**Research** — how do channels like this grow, and what transfers? Always has
capacity, so it is the fallback when nothing else clears the bar. Three rules:

- **Filter through our own findings.** Generic Shorts advice is the genre that
  produced two conclusions our own data later killed. Output a **hypothesis
  with a proposed test**, never a practice to adopt.
- **Do not pivot on new information.** A finding joins the bottom of `PRD.md`
  §0's backlog and waits. Direction changes need data from our own channel.
- **Discard aggressively.** Research that changes no decision is a sentence in
  `WORKLOG.md`, not a document. **Never create new files for it.**

**Feature work** — the experiment backlog in `PRD.md` §0, in its stated order,
under its pre-committed decision rules.

## 5. Authorization (owner, 2026-09-19)

**You may merge to `main` yourself, including live-path changes.** The gates
that replace owner review are in `CLAUDE.md` §3; clear them, then update
`WORKLOG.md` and `PRD.md` §0.

**Some things need the owner — escalate, don't decide, don't block.** Raise it
with `scripts/escalate.py --title … --key … --recommend …`, commit, and push;
it becomes an issue that emails them. The same `--key` comments rather than
duplicating. **Always include a recommendation** — one without it just moves
the work.

The list is in `CLAUDE.md` §4 — one rule, one home. In short: guardrails,
spending, production data, publishing.

**Auto-revert** (revised by the owner, issue #18). Check a release with
`scripts/report.py --release <version>`, which reads every upload at the same
age from the weekly snapshot — a flag-day change can never be age-matched with
`--compare`. **Revert on watch-seconds only.** Views are reported but never
trigger: measured on this channel they swing 27–50% at fixed age with nothing
changed, so a views trigger fires on noise. Shipping without review only works
if something watches the result; that watching is the PM lane's first job.

## 6. External budgets (these are not Claude usage)

Limits are in `CLAUDE.md` §1. Shift-specific:

- **Gemini:** at most 8 requests, only after the 07:00 UTC reset, never within
  an hour of a scheduled run — exhausting it cost a real upload its title.
- **Polly:** at most one dry run per shift.
- **Never run `scripts/weekly_analytics.py`** to check something: it appends
  real rows. If you do, revert the file before committing.

## 7. The value bar — what NOT to do

"Always be working" manufactures tasks, and churn on a live system is worse
than idleness. Forbidden:

- **Refactoring without a named benefit.** "Cleaner" is not one. It must
  unblock a change, remove a rule that could drift, or make untestable logic
  testable. Work `TECH_DEBT.md`'s tiers; don't invent work.
- **Re-planning what was just planned.** `PRD.md` §0's backlog order stands
  until *data* moves it, not until a shift has a new opinion.
- **Rewriting accurate docs.** Correct stale claims; leave the rest.
- **New trackers or documents.** Use the ones that exist.
- **Widening scope mid-shift.** Finish, then pick the next thing.

If a lane has nothing above that bar, say so and move on — the time goes to PM
and research (§2), not back to the clock. Stopping early is the last resort,
not the default: it means even planning, prioritising and research had nothing
worth doing, which should be rare. When it happens, say the queue is empty and
why.

## 8. Leave the context no bigger than you found it

```sh
venv/bin/python scripts/context_budget.py --check
```

Add `--health` once a day: it detects process dysfunction — capacity
consistently unused, a lane starved — and **queues the escalation itself**.

Checks both words in the loaded docs and **open items in the append-only ones**
(`WORKLOG.md`, `DECISIONS.md`, `TECH_DEBT.md`) — those cost nothing per session,
so nobody notices them growing. If you added, you are expected to have closed
something. The test for any line: **would removing this cause a mistake?**
When something is over budget the fix is almost never a bigger budget — delete
it, move detail to where it is read on demand, or convert an advisory rule into
a hook or a test.

**`/audit` is a PM task that comes due, not a separate cadence.** It reads a
*series* — the last ten entries, escalations, what got reverted — so it needs
about ten shifts of evidence. Run it when `WORKLOG.md` shows none in the last
ten; PM's slice grows that shift to fit, which is §2 working, not an exception.

## 9. End the shift rather than extend it

Cost climbs with session length, not with how much you read at the start
(orientation is ~1%). When the work is done, **hand over and end** — the
`WORKLOG.md` entry is what makes the next shift cheap. Ending early because
the work is done is right; ending early with work outstanding is not.

## 10. Close the loop

Before the shift ends — and early enough that it still happens if usage runs
out mid-task:

1. Commit work in progress on a branch; never leave `main` half-finished.
2. Update `PRD.md` §0 if anything shipped; `TECH_DEBT.md` for findings you did
   not fix.
3. Prepend a `WORKLOG.md` entry **following the template in that file's
   header**. It is emailed to the owner verbatim as the shift report and is the
   only thing they see, so write it for a manager, not an engineer: plain
   language, no filenames, no jargon. Technical detail belongs in the commit
   message and `TECH_DEBT.md`, where the next shift will look for it.
4. State plainly what you did and what you would do next.
