---
name: shift
description: Run an autonomous work shift on the reddit-digest channel — triage, pick the highest-value lane, do the work, ship it, and leave the next shift a clean handover. Use when a session starts with no specific task and should simply make the best use of available time. Covers maintenance, security, project management, research and feature work.
---

# Run a shift

A session that starts without a task still does the most valuable thing
available, ships it, and hands over cleanly — without the owner in the loop.
Five lanes: maintenance, security, project management, research, feature work.
Be whichever is worth most right now; don't tour all five.

**Point, don't duplicate.** Status lives in `PRD.md` §0, code health in
`TECH_DEBT.md`, conventions in `CLAUDE.md`. This skill and `WORKLOG.md` record
what happened and what's next — never a second copy of status.

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
of the weekly one — the rest is theirs; never plan around using it. `WRAP`
means finish or park what's open; `STOP` means close the loop and end.

Then **allocate across every lane**, writing the plan into the `WORKLOG.md`
entry before starting. Two slices are fixed: **rounds ~10%** and **closing the
loop ~10%**. The remaining ~80% is split by how much genuinely valuable work
each lane actually has — not by a fixed percentage.

**Slices are ceilings, not quotas.** A lane finishes its valuable work and
stops; it does not fill its allocation. Unused budget is **not** redistributed
— if every lane finishes early, the shift ends early. That is the whole
defence against padding, and padding ships.

Allocating honestly:

- **A lane with no actionable work gets 0%, and that is a finding**, not a
  failure. Say so in `WORKLOG.md`.
- **An empty feature lane is a project-management problem.** Give that time to
  PM to populate the backlog rather than inventing features to build.
- **Research absorbs genuine slack** — it always has capacity — but cap it at
  ~25%, or it becomes the place effort goes to look busy.
- **Starvation floor:** any lane at ~0% for **5 consecutive shifts** takes
  priority in this one if it has any queued work. Check the `Lane:` lines in
  `WORKLOG.md`. A lane that keeps losing is the failure mode of every
  priority scheme, including the one this replaced (see `DECISIONS.md` D1).

## 3. Preemption — when one thing takes the whole shift

These are not lanes competing for a slice; they are the shift's purpose that
day. Check in order, before allocating:

1. **Incident.** Did both scheduled uploads land (`upload_log.csv` tail)? Did
   the last workflow run succeed? Is `prev_post.txt` intact? A missed or
   duplicated upload preempts everything.
2. **Ship what's built.** Read `.github/last-release-validation.md` on `main` —
   CI runs the Gemini gates at 08:17 UTC and commits the verdict, so you never
   need quota to find out. PASS means merge. Unshipped work is inventory, not
   progress: a branch once sat 8 days while six stacked behind it.
3. **A closing window.** Work blocked on an external budget that is available
   *now* — these windows close.

## 4. The lanes

**Maintenance** — is the pipeline healthy, are the logs sane, is anything
silently failing? *Fail-soft without telemetry is indistinguishable from
working* — that has bitten three times. Instrument a silent fallback before
fixing it.

**Security** — a standing check: secrets never committed (`git log --all --
.env client_secret.json token.json` empty, `.gitignore` covering them),
dependency advisories, Actions workflow permissions, OAuth scope. Fix what is
clearly wrong; log the rest.

**Project management** — is the tracker true? Is the next thing we'd build
actually the highest-leverage thing? Are decision rules still pre-committed and
honest? Is documentation accurate (stale claims mislead worse than missing
ones)?

**The workflow itself is always in scope here, not only at audit time.** Agentic
systems improve what they build and never question how they build it. If
something about this process was awkward *this shift* — a rule that didn't fit,
a step that added nothing, state you had to re-derive, a gate you worked around
— that is a finding. Record it in `WORKLOG.md` even when you don't act on it;
the next `/audit` needs the pattern, and one shift's friction is invisible on
its own. Changes to the process are proposals (§5), not self-applied edits.

**Research** — how do channels like this actually grow, and what transfers?
This lane always has capacity, so it is the fallback when nothing else clears
the bar. Three rules keep it useful:

- **Filter through this channel's own findings.** Generic Shorts advice is
  precisely the genre that produced R1.8/R1.9 and the b-roll retention claim,
  both of which the data later killed. Output a **hypothesis with a proposed
  test**, never a practice to adopt.
- **Do not pivot on new information.** A finding goes to the bottom of the
  experiment backlog in `PRD.md` §0 and waits its turn, unless it contradicts
  something we currently *believe* — in which case the finding is that our
  evidence is weak, not that we should change direction today. Direction changes
  need data from our own channel.
- **Discard aggressively.** Research that does not change a decision should be
  a sentence in the `WORKLOG.md` entry, not a new document. **Do not create
  new files in `analysis/` or new top-level docs for research output.** A
  scatter of unread reports is a maintenance cost with no upside; if it is
  worth keeping, it belongs in §0's backlog or §4's Findings.

**Feature work** — the experiment backlog in `PRD.md` §0, in its stated order,
under its pre-committed decision rules.

## 5. Authorization (owner, 2026-09-19)

**You may merge to `main` yourself, including live-path changes — prompts,
content selection, the upload path.** The owner-review gate and the
"don't build until told" rule are superseded. Ship it.

**Gates that replace the owner's review** (also `CLAUDE.md` §3): tests green;
a `DRY_RUN=1` run producing a playable MP4 for anything touching the video or
its metadata; `FORMAT_VERSION` bumped when the video changes; one variable per
release. Then update `WORKLOG.md`, and `PRD.md` §0 if anything shipped.

**Still requires the owner — escalate, don't decide.** Queue an issue and move
on to other work; do not block the shift waiting for an answer:

```sh
venv/bin/python scripts/escalate.py --title "..." --key ... --recommend "..." <<'EOF'
...why this is the owner's call...
EOF
```

Commit and push it — `.github/workflows/escalations.yml` files it as a GitHub
issue, which emails the owner. Re-raising the same `--key` comments on the open
issue rather than duplicating. Always include a recommendation; an escalation
without one just moves the work. Details in `.escalations/README.md`.

The list is in `CLAUDE.md` §4 — one rule, one home. In short: guardrails,
spending, production data, publishing.

**Auto-revert.** A shift that finds the previous autonomous release degraded
median watch-seconds or views against an age-matched baseline (`scripts/report.py
--compare`) reverts it and records why. Shipping without review only works if
something is watching the result.

## 6. External budgets (these are not Claude usage)

Limits are in `CLAUDE.md` §1. Shift-specific rules:

- **Gemini:** at most 8 requests for verification, only after the 07:00 UTC
  reset, never in the hour before a scheduled run. Exhausting it degrades a
  real upload — that happened on 2026-09-19 and cost a video its title.
- **Polly:** at most one dry run per shift.
- **Don't run `scripts/weekly_analytics.py`** to check something — it appends
  real rows. If you do, revert the file before committing.

## 7. The value bar — what NOT to do

"Always be working" creates pressure to manufacture tasks, and this project is
a live system that uploads twice a day. Churn on it is worse than idleness.
Specifically forbidden:

- **Refactoring without a named benefit.** "Cleaner" is not one. It must
  unblock a change, remove a rule that could drift, or make untestable logic
  testable. Work `TECH_DEBT.md`'s tiers; don't invent work.
- **Re-planning what was just planned.** `PRD.md` §0's backlog order stands
  until *data* moves it, not until a shift has a new opinion.
- **Rewriting docs that are already accurate.** Correct stale claims; leave
  correct ones alone.
- **New trackers, new documents, new analysis files.** Use the four that exist:
  `PRD.md`, `TECH_DEBT.md`, `WORKLOG.md`, `CLAUDE.md`.
- **Widening scope mid-shift.** Finish the thing, then pick the next thing.

If a lane has nothing above that bar, say so and move on. If *no* lane does, do
research — it always has capacity, and thinking and planning are real work.
Only if that is thin too, **stop and say the queue is empty.** A shift that
ships one real thing and says "nothing else cleared the bar" is a good shift.

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

**Every ~10th shift** (or when `WORKLOG.md` shows none in the last ten), run
**`/audit`** for the deep pass over the process itself.

## 9. End the shift rather than extend it

Every turn re-reads everything before it, so cost climbs with session length
while **orientation is only ~1% of it** — don't optimise the reading, optimise
the length. **One lane, ~100 turns, then hand over and end.** A good
`WORKLOG.md` entry isn't overhead; it's what makes a cheap restart possible
instead of an expensive continuation. Evidence and the measurement:
`scripts/context_budget.py --session`.

## 10. Close the loop

Before the shift ends — and early enough that it still happens if usage runs
out mid-task:

1. Commit work in progress on a branch; never leave `main` half-finished.
2. Update `PRD.md` §0 if anything shipped; `TECH_DEBT.md` for findings you did
   not fix.
3. Prepend a `WORKLOG.md` entry: the allocation line, then **one line per lane
   saying what it produced** — including "nothing, because …", which is a real
   answer. Then what's queued next, and anything blocked *and on what*. This
   entry is emailed to the owner as the shift report, so it is the only thing
   they see; write it for someone who has not looked at the repo.
4. State plainly what you did and what you would do next.
