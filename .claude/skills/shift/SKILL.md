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

## 2. Check the budget — and respect the owner's reserve

```sh
venv/bin/python scripts/statusline.py --budget
```

**The owner keeps a reserve.** Autonomous work stops at **80% of the 5-hour
window** and **90% of the weekly window** — not 100%. The remainder is theirs;
never plan around using it.

Reads `~/.claude/usage-snapshot.json` and prints one of:

| Verdict | Do |
|---|---|
| `GO` | Full shift — a feature through dry run and merge is in scope |
| `BOUNDED` | One small task, finish it, hand over |
| `WRAP` | Start nothing new; finish or park what's open and hand over |
| `STOP` | Close the loop immediately: commit, update `WORKLOG.md`, end the shift |

**Never start what cannot be finished or cleanly parked.** An abandoned
half-refactor costs the next shift more than it saved. On `STOP`, stopping *is*
the work — say so and end.

## 3. Triage before choosing a lane

In order. The first one that fires wins the shift.

1. **Incident.** Is production broken? Check: did both scheduled uploads land
   (`upload_log.csv` tail), did the last workflow run succeed, is
   `prev_post.txt` intact? A missed or duplicated upload preempts everything.
2. **Time-windowed work.** Anything blocked on an external budget that is
   *now* available — most often Gemini quota after its 07:00 UTC reset. These
   windows close; take them when they are open.
3. **Ship what's already built.** Read `.github/last-release-validation.md` on
   `main` — CI runs the Gemini gates at 08:17 UTC daily and commits the verdict
   there, so you never need quota to find out. PASS means merge.
   If branches are queued and their gates pass,
   **merging beats building more.** Unshipped work is inventory, not progress:
   on 2026-09-19 a branch had sat 8 days while six more were stacked behind it.
   Clearing the queue is a real lane, not overhead.
4. Otherwise, **rotate** through the lanes below, skipping any with nothing
   above the value bar. Prefer the lane least recently worked (see `WORKLOG.md`).

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
ones)? **This lane owns this skill too** — if the shift process is wrong,
fixing it is the work, and §9 is how that stays honest.

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

**Every merge must clear these gates — they replace the owner's review:**
- Full test suite green (`venv/bin/python -m pytest tests/`).
- For anything touching the rendered video or its metadata: a `DRY_RUN=1` run
  that produces a playable MP4, with the printed metadata sane.
- `FORMAT_VERSION` bumped if the video or its metadata changes, so the cohort
  stays separable. **One variable per release.**
- `WORKLOG.md` updated, and `PRD.md` §0 updated if anything shipped.

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

- **Refactoring without a named benefit.** "Cleaner" is not a benefit. A
  refactor needs a concrete one: it unblocks a change, removes a duplicated
  rule that could drift, or makes untestable logic testable. `TECH_DEBT.md`
  tiers findings for exactly this reason — work the tiers, don't invent work.
- **Re-planning what was just planned.** Re-deriving priorities every shift
  destroys direction. `PRD.md` §0's backlog order stands until *data* moves it,
  not until a shift has a new opinion.
- **Rewriting docs that are already accurate.** Correct stale claims; leave
  correct ones alone.
- **New trackers, new documents, new analysis files.** Use the four that exist:
  `PRD.md`, `TECH_DEBT.md`, `WORKLOG.md`, `CLAUDE.md`.
- **Widening scope mid-shift.** Finish the thing, then pick the next thing.

If a lane has nothing above that bar, say so and move on. If *no* lane does, do
research — it always has capacity, and thinking and planning are real work.
Only if that is thin too, **stop and say the queue is empty.** A shift that
ships one real thing and says "nothing else cleared the bar" is a good shift.

## 8. The standing audit — every shift, briefly

Agentic setups bloat until the instructions that matter are lost among those
that don't — *"bloated CLAUDE.md files cause Claude to ignore your actual
instructions."* This project added four documents in its first autonomous
session, so the pressure is real.

**Every shift, before closing:**

```sh
venv/bin/python scripts/context_budget.py --check
```

If you added context, you are expected to have removed some. The test for any
line, from Anthropic's own guidance: **"would removing this cause a mistake?"**
If not, cut it. When something is over budget, the fix is almost never a bigger
budget — delete it, move detail to where it is read on demand (a skill, or PRD
§6), or convert an advisory rule into a hook or a test, which is enforcement
rather than words.

**Every ~10th shift, or whenever `WORKLOG.md` shows no audit in the last ten,
do the deep pass** and record it in `TECH_DEBT.md`:

1. **Prune.** Re-read `CLAUDE.md` line by line against the question above.
   `/doctor` proposes cuts for anything derivable from the codebase.
2. **Check the external guidance.** Re-read
   [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
   and the [skills](https://code.claude.com/docs/en/skills) docs. They change.
   Adopt what applies; **record what you deliberately rejected and why**, so
   the next shift doesn't re-litigate it.
3. **Audit what the process actually produced.** Read the last ten `WORKLOG.md`
   entries. Which shifts shipped something that mattered? Which produced churn?
   Is any lane always skipped — and is that correct, or is the triage order
   wrong? Are escalations landing on real decisions, or noise?
4. **Look for layering.** Rules restated in two places will drift — that has
   already happened once here, between memory and `PRD.md`. One rule, one home,
   pointers everywhere else.

Changes to this skill are a **proposal**, not a self-applied edit: escalate
them (§5). A workflow that rewrites its own rules unobserved is the failure
mode this whole section exists to prevent.

## 9. Close the loop

Before the shift ends — and early enough that it still happens if usage runs
out mid-task:

1. Commit work in progress on a branch; never leave `main` half-finished.
2. Update `PRD.md` §0 if anything shipped; `TECH_DEBT.md` for findings you did
   not fix.
3. Prepend a `WORKLOG.md` entry: date, lane, what happened, what's queued next,
   and anything blocked *and on what*.
4. State plainly what you did and what you would do next.
