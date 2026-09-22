# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

**Entries are emailed to the owner verbatim as the shift report.** Write for a
manager, not an engineer: plain language, no filenames, no jargon. Technical
detail belongs in the commit message and `TECH_DEBT.md`, which is where the
next shift looks. Follow this template exactly — the report is generated from
its structure:

```
## 2026-09-21 — one line on what actually mattered

    Allocation (planned→actual %): rounds 10→8 · maintenance 15→25 · security 10→5 · pm 15→12 · research 10→0 · feature 30→40 · close 10→10

**Summary:** Two sentences. What the shift achieved, and why it matters to the
channel. No detail — this is the part read on a phone.

### Maintenance
- One bullet per thing done, in plain words.

### Security
- Nothing this shift — the standing checks were clean.

### Project management
- Nothing this shift — no decisions came due.

### Research
- Nothing this shift, because maintenance took the time.

### Blocked
- What is stuck, and what it is waiting on.

### Next
- What the following shift should pick up.

### Better?
- **Than last shift:** yes/no/unclear, and the specific thing that is better.
- **Than ~10 shifts ago:** same, naming evidence rather than impression.
- **Than ~100 shifts ago:** same, or "too early to say".
```

**On the "Better?" section.** Numbers lag and no single one judges this channel
(`report.py --scorecard`), so a subjective read is part of the record — but a
shift grading its own work is exactly the bias the research warns about. Two
rules make it worth having: answer **comparatively** against a named horizon
rather than rating out of ten, and **name the evidence**, not the feeling.
"Unclear" is a real answer and more useful than a confident guess.

**Every workstream gets a heading, including ones that did nothing** — with a
one-line "nothing this shift, because …". Silence and inactivity must not look
alike, and the report flags a missing reason rather than hiding it. Routine
checks and wrap-up are overhead and need no section. **The planned and actual
columns must each total 100%**; the report shows the sum and flags it if not.
Read the allocation series with
`venv/bin/python scripts/context_budget.py --allocation`.

---

## 2026-09-21 (evening) — the safety net behind unattended releases now works, and it says views can't be trusted

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→10 · security 5→5 · pm 15→15 · research 20→10 · feature 30→40 · close 10→10

**Summary:** The rule that is supposed to catch a bad release and roll it back
has never once been able to give an answer; it can now, using performance data
we already keep. Building it turned up something bigger: the channel's view
counts swing so much on their own that most of what we measure them for cannot
actually be measured.

### Feature work
- **The release safety net works.** Every upload can now be compared with
  older ones *at the same age* — a video from July read at a week old against
  one from September read at a week old — which is what the rule always
  required and never had. It covers both of the measures the rule names, not
  just one, and needs no account access, so an unattended session can run it.
- **Its first run would have thrown away the last two things we shipped** —
  roll back both the current video format and the background-video library, on
  view drops of 50% and 39%. But the channel's view counts move 27–52% between
  consecutive batches of uploads *with nothing changed at all*, and both
  "drops" are the same few weeks of ordinary weather. The tool now measures
  that background movement, will not call something a regression unless it is
  bigger, and prints that limit beside every answer — so nobody reads a clean
  result as proof a change worked.
- Verdicts as of today: current format **keep**; background library **roll
  back, but see below**; newest release **no answer yet**, and it becomes
  answerable around 5 October.

### Project management
- **A decision that is yours.** The rule rolls back a release if watch time
  *or* views got worse, and for the background library those two disagree:
  time watched is up 22%, comfortably beyond the noise, while views are down
  39% against a noise limit of 38%. So the rule says roll back a change that
  improved the measure the plan calls primary — and doing that would discard
  clips you chose. **Raised with you**; not acted on, and the tool shows the
  disagreement rather than hiding it.
- **The same problem waits in the next experiment**, which is pre-committed to
  "keep only if watch time and views both hold or improve". Views cannot meet
  that standard here at two uploads a day. Flagged in the plan rather than
  rewritten, because it is the same decision as above.

### Maintenance
- The daily check on the live code has now failed two mornings running, and I
  could not find out why: the failure detail only exists in a log an unattended
  session is not allowed to read, and re-running the check would have taken
  more of the shared daily AI allowance than was left after today's uploads.
  Nothing suggests a live problem — this morning's upload generated everything
  correctly — but it is unresolved and you already have an open issue about it.
- The morning upload landed. **The evening one was still due when this shift
  ended and is unconfirmed** — the next shift should check it first.
- **The fix is a line in a file I am not permitted to change**, so I added it
  to the approval you already have waiting rather than raising a third request.
  Once approved, every future failure explains itself for free.

### Security
- Standing checks clean: no credentials have ever been committed, they remain
  ignored, and every automated workflow's permissions are scoped.

### Research
- Outside sources put 50–500 views in the first two days as normal for a
  channel our size. We sit inside that, which independently supports the
  finding above: the swing is the platform's per-video lottery, not something
  wrong with us. They also claim ranking now follows watch time; **our own
  numbers point the other way**, so it is filed as a question, not a fact.
  Nothing adopted.

### Blocked
- The roll-back rule's disagreement between the two measures needs your call.
- The release-check failures stay undiagnosed until either the approval lands
  or a shift has spare daily allowance.

### Next
- If the owner settles the measures question, apply it in one place for both
  the roll-back rule and the ranking experiment.
- Otherwise: the slate measurement the ranking experiment needs, under the
  cheaper design already priced.

## 2026-09-21 — the channel can now be measured without the keys to it

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→5 · security 5→5 · pm 15→25 · research 5→0 · feature 45→45 · close 10→10

**Summary:** Automated work sessions could not answer a single question about
how the channel is performing, because the performance tool needed YouTube
credentials that those sessions are deliberately denied. They can now, using
the weekly performance data we already keep. The first thing it found is that
the rule meant to catch a bad release has never been able to run.

### Feature work
- Performance reporting now has an offline mode that reads the weekly
  performance data already stored in the project, so an unattended session can
  check how the channel is doing without any account access. Three
  easy-to-get-wrong rules are built in and locked down by tests — most
  importantly that the fortnight of videos published since the last weekly data
  pull are reported as *not yet measured* rather than as zero views, which
  would have invented two weeks of fake disasters.
- It states what it cannot see on every run rather than quietly guessing, and
  refuses outright to answer the one question the stored data genuinely cannot
  settle.

### Project management
- **The safety net behind unattended releases has never worked.** The rule says
  a release that hurts performance is automatically rolled back, judged against
  videos of a similar age. But a release applies to everything published after
  it and nothing before, so there is never a similar-aged group to compare
  against, and the check correctly refuses to answer — every time, for every
  release we have shipped, and for the background-video library too. Nothing
  was ever rolled back because nothing could ever produce a verdict. The right
  measurement already exists in the project and simply has no way to be run.
  **Raised with you as an issue**, since the rule is yours; the tool it needs is
  ordinary work and is queued next.
- **A blocker that had already been cleared cost the last session its feature
  time.** The next planned experiment was recorded as waiting on an analysis
  that had in fact been completed ten days earlier — the plan said so in one
  place and the detailed spec still said "do not start" in another. Corrected.
- **That experiment has a cost nobody had priced.** Picking a better question
  than Reddit's top-ranked one means asking our AI service about several
  candidates instead of one, and the free daily allowance is already tight
  enough that it starved a live upload last week. Scanning ten candidates would
  consume the entire day's allowance by itself. Recorded a cheaper design —
  one combined request per run — that both fits the allowance and produces the
  missing measurement the experiment needs before it can be judged.

### Maintenance
- Both scheduled uploads landed, and today's ran with every element generated
  correctly — the title problem from last week has not recurred.

### Security
- Standing checks clean: no credentials have ever been committed, they remain
  ignored, and every automated workflow's permissions are scoped.

### Research
- Nothing this shift. Project management turned up more than expected and the
  time went there; this is the third consecutive shift at zero, and the process
  flags a lane at five.

### Blocked
- The release-rollback rule needs your decision before the check can be pointed
  at something that works.
- Still waiting on the earlier request about the daily allowance the release
  gate consumes.

### Next
- Build the release check the rule needs, so a release can finally be judged.
- Then the slate measurement for the next experiment, under the cheaper design.

## 2026-09-20 (evening) — maintenance + PM (a guardrail that cost quota daily)

    Allocation (planned→actual %): rounds 10→10 · maintenance 45→45 · security 10→5 · pm 15→20 · research 10→0 · feature 10→10 · close 10→10

No preemption: both uploads landed, `prev_post.txt` intact, nothing waiting to
ship, recorded FAIL stale by 16 commits.

**The release gate could never skip itself, and the early upload paid.**
`validate-release.yml`'s "don't re-validate a commit that already passed"
branch cannot fire: recording a verdict *commits to `main`*, so next morning
HEAD is always past the sha just recorded. `a4fb38c` names `c6ee5f7` and sits
directly on top of it. Cost: **6 of the day's 20 Gemini requests, every day,
forever** — shared with live uploads, and the ~05:00 publish is *last* in the
07:00→07:00 window, so it starves first. That is why the 05:01 upload shipped
the raw Reddit question as its title (`title_ok=0`).

Fix compares the code the gates exercise, expires a PASS after 7 days (the
model drifts with no commit of ours), and runs the unit tests unconditionally
— free, and **the only pytest anywhere in CI**. Logic moved from bash into a
tested function; the version it replaces failed silently and nothing could
have noticed.

**Half of it is not mine to ship.** `should_validate` + 12 tests landed
(`4cfc1c4`), inert. The wiring is **issue #14**: `.github/workflows/**` is
protected precisely because a shift editing it "could disable its own
supervision", and this reduces how often that supervision runs.

**Two process findings.** (1) A shift cannot propose a workflow change on a
branch either — the push is rejected for lack of `workflows` permission, so
`.escalations/README.md`'s "propose freely on a branch" is not the real route
for these; diff inlined in #14. (2) `report.py` dies on
`KeyError: 'YOUTUBE_REFRESH_TOKEN'` — shifts are rightly denied YouTube
secrets, so **a scheduled shift can answer no performance question at all.**

**PM.** Three TECH_DEBT items described already-shipped work (merged
`get_metadata`, the `*_ok` columns, `title_style` blanking). PRD §4 still said
8–14 requests/day, contradicting §2's corrected 4–10. Fixed; items 25 → 24.

**Feature (10%) ended in a blocker, not code.** R4.4 is gated on re-running
the topic analysis, which needs `report.py` — see finding (2). The fix is an
offline read-only loader in `insights.py`; not rushed at shift end, because
`load_videos` encodes two rules a naive snapshot reader breaks silently.
Details in `TECH_DEBT.md`.

**Research 0%** — nothing above the bar once the gate bug surfaced; 2
consecutive shifts at 0, floor is 5. **Security clean** — secrets never
committed and still ignored, permissions scoped.

**Queued next:** (1) the offline analytics loader, unblocking R4.4 and every
future PM lane; (2) #14 needs the owner before the quota fix does anything;
(3) tomorrow's 08:17 gate is the authoritative verdict on the screen fix — it
*will* run, since `src/screen.py` and `scripts/` changed; (4)
`replay_screen.py`'s FLIRT case is still a memorization check.

**Spent no Gemini, no Polly** — today's window was already drawn down.

## 2026-09-20 (afternoon) — maintenance (stale-then-real gate failure)

    Allocation (planned→actual %): rounds 10→5 · maintenance 15→70 · pm 15→15 · research 10→0 · feature 40→0 · close 10→10

The recorded FAIL was stale, but re-checking found a real, different fault:
with reasoning restored, the R4.6 screen still missed a paraphrase of the
identical `sexual_suggestive` shape while catching the literal in-prompt
example. **One example doesn't generalize a category.** Fixed in `89bc245`,
pinned by a test; full finding in `TECH_DEBT.md`.

**A fix verified once, live, is a sample of one.**

## 2026-09-20 — maintenance (incident-led)

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→65 · pm 15→20 · research 15→0 · feature 35→0 · close 10→5

**FAULT 1 — the screen lost its judgment, live.** Disabling Gemini thinking
everywhere (2026-09-19) fixed title latency and silently broke the one genuine
judgment task. 512 reasoning tokens restored, pinned by a test. **The CI gate
is the only reason this surfaced before it cost an upload.**

**FAULT 2 — the first scheduled shift did nothing and reported success.**
`claude-code-action` grants no shell access without `--allowedTools`. Fixed.
**A shift that leaves no trace is indistinguishable from one that never ran**,
and every health signal reads `WORKLOG.md`.

**Both faults were caught by the checks, not by looking. Green is not
evidence.**
