---
name: shift
description: Run an autonomous work shift on the reddit-digest channel — triage, pick the highest-value lane, do the work, ship it, and leave the next shift a clean handover. Use when a session starts with no specific task and should simply make the best use of available time. Covers maintenance, security, project management, research and feature work.
---

# Run a shift

The owner has finite Claude usage and little time to direct it. This skill
exists so that any session which starts without a task still does the most
valuable thing available, ships it, and hands over cleanly — **without needing
the owner in the loop.**

Think of it as running a small company: the channel needs maintenance,
security, project management, research and feature work. Your job this shift is
to be whichever of those is worth the most right now, not to touch all five.

**Core rule: point, don't duplicate.** Status lives in `PRD.md` §0, code health
in `TECH_DEBT.md`, conventions in `CLAUDE.md`. This skill and `WORKLOG.md`
record *what happened and what's next* — never a second copy of status. That
drift has already happened once here.

---

## 1. Orient (always, ~5 minutes)

Run the **`/pickup`** steps first. Do not re-derive state from `git log`.

Then read `WORKLOG.md` (repo root) — the last few shifts and what each one
queued for the next.

## 2. Triage before choosing a lane

In order. The first one that fires wins the shift.

1. **Incident.** Is production broken? Check: did both scheduled uploads land
   (`upload_log.csv` tail), did the last workflow run succeed, is
   `prev_post.txt` intact? A missed or duplicated upload preempts everything.
2. **Time-windowed work.** Anything blocked on an external budget that is
   *now* available — most often Gemini quota after its 07:00 UTC reset. These
   windows close; take them when they are open.
3. **Ship what's already built.** If branches are queued and their gates pass,
   **merging beats building more.** Unshipped work is inventory, not progress:
   on 2026-09-19 a branch had sat 8 days while six more were stacked behind it.
   Clearing the queue is a real lane, not overhead.
4. Otherwise, **rotate** through the lanes below, skipping any with nothing
   above the value bar. Prefer the lane least recently worked (see `WORKLOG.md`).

## 3. The lanes

**Maintenance** — the system and the channel. Is the pipeline healthy, are the
logs sane, is anything silently failing? The recurring lesson here is that
*fail-soft without telemetry is indistinguishable from working* — three
separate times (`caption_ok`, `screen_source`, `title_ok`). When you find a
silent fallback, instrument it before you fix it.

**Security** — cheap, bounded, worth a standing check: secrets never committed
(`git log --all -- .env client_secret.json token.json` must be empty and
`.gitignore` must cover them), dependency advisories, GitHub Actions workflow
permissions, OAuth token scope no broader than needed. Fix what is clearly
wrong; log the rest.

**Project management** — is the tracker true? Is the next thing we'd build
actually the highest-leverage thing? Are decision rules still pre-committed and
honest? Is documentation accurate (stale claims mislead worse than missing
ones)? **This lane owns this skill too** — if the shift process is wrong,
fixing it is the work.

**Research** — how do channels like this actually grow, and what transfers?
This lane always has capacity, so it is the fallback when nothing else clears
the bar. **Filter everything through this channel's own findings.** Generic
Shorts advice is precisely the genre that produced R1.8/R1.9 and the b-roll
retention claim, both of which the data later killed. Output hypotheses with a
proposed test, never "best practices" to adopt.

**Feature work** — the experiment backlog in `PRD.md` §0, in its stated order,
under its pre-committed decision rules.

## 4. Authorization (owner, 2026-09-19)

**You may merge to `main` yourself, including changes to the live upload path,
prompts and content selection.** The former rollout gate (owner reviews a
dry-run sample before merge) and the "don't build until the owner says go" rule
are **superseded for routine work**. Ship it.

**Every merge must clear these gates — they replace the owner's review:**
- Full test suite green (`venv/bin/python -m pytest tests/`).
- For anything touching the rendered video or its metadata: a `DRY_RUN=1` run
  that produces a playable MP4, with the printed metadata sane.
- `FORMAT_VERSION` bumped if the video or its metadata changes, so the cohort
  stays separable. **One variable per release.**
- `WORKLOG.md` updated, and `PRD.md` §0 updated if anything shipped.

**Still requires the owner — do not do these autonomously:**
- Weakening a safety or cost control: the Polly budget, the `DRY_RUN` guard,
  secrets handling, or the R4.6 screen's skip categories. Autonomy was granted
  over channel work, not over the protections that bound it.
- Anything that spends money beyond the existing ~$0.90/month Polly line.
- Deleting or rewriting production data (`upload_log.csv`, `prev_post.txt`,
  `analysis/*`), including backfills of historical rows.
- Publishing anything outside the channel's normal upload.

**Auto-revert.** A shift that finds the previous autonomous release degraded
median watch-seconds or views against an age-matched baseline (`scripts/report.py
--compare`) reverts it and records why. Shipping without review only works if
something is watching the result.

## 5. External budgets (these are not Claude usage)

- **Gemini: 20 requests/day, shared with production.** Production spends 4–10.
  Budget **at most 8** for verification, only after the 07:00 UTC reset, and
  never in the hour before a scheduled run. Exhausting it degrades real uploads
  — this happened on 2026-09-19 and cost the next morning's upload its title.
- **Polly costs real money.** At most one dry run per shift. Never bulk; see
  `CLAUDE.md` §1.
- **Don't run `scripts/weekly_analytics.py`** to check something — it appends
  real rows. If you do, revert the file before committing.

## 6. Stopping is allowed

If a lane has nothing above the value bar, say so and move on. If *no* lane
does, do research — and if that is thin too, **stop and say the queue is
empty.** Idle beats manufactured work on a system that uploads twice a day.
A shift that ships one real thing and says "nothing else was worth doing" is a
good shift.

## 7. Close the loop

Before the shift ends — and early enough that it still happens if usage runs
out mid-task:

1. Commit work in progress on a branch; never leave `main` half-finished.
2. Update `PRD.md` §0 if anything shipped; `TECH_DEBT.md` for findings you did
   not fix.
3. Prepend a `WORKLOG.md` entry: date, lane, what happened, what's queued next,
   and anything blocked *and on what*.
4. State plainly what you did and what you would do next.
