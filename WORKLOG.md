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

## 2026-09-22 — the check that guards every release has never once passed, and nobody could see why

    Allocation (planned→actual %): rounds 10→10 · maintenance 40→35 · security 5→5 · pm 25→40 · research 10→0 · feature 0→0 · close 10→10

**Summary:** The automatic check that decides whether new work is safe to put
live has failed every day since it was built, and today I could show that the
thing it was failing is healthy. One cause is fixed and live; seeing the rest
needs a one-line change you have to approve.

### Maintenance
- **The release check has never passed.** Three runs, three refusals to ship.
  I ran both halves of it by hand today against the live code: both pass. The
  code was fine, the check was wrong about it, and meanwhile nothing could be
  shipped.
- **Fixed one cause.** We get a fixed number of free AI requests a day, shared
  with the two live uploads. When they ran out, the check could not tell "I
  could not check this" apart from "this is broken" — so it declared the
  release unsafe and emailed you. It now tells those apart, and once it knows
  the service is not answering it stops rather than spending five more requests
  proving it again.
- **That failure was quietly expensive.** A failed check is retried every
  morning by design, so a permanently stuck one spent nearly a third of the
  day's shared AI allowance daily to re-learn the same non-answer. The
  early-morning upload is last in that queue and lost its title to exactly this
  two days ago.
- **What I still cannot see** is whether that was the whole story: the reason
  exists only in a log this kind of session is not permitted to read. Third
  shift running to hit that wall. One line fixes it; it is with you.

### Security
- Standing checks clean: no credentials have ever been committed, they remain
  ignored, nothing secret-shaped is in the tracked files, and every automated
  job's permissions are still scoped to what it does.

### Project management
- **The channel is flat** — viewing time has sat inside its own noise for six
  periods. The rule for that is explicit: process work does not count as a
  response, we have to change what we publish. Candidates generated and ranked;
  the winner is now first in the plan.
- **Titles matter less than we assumed.** Our three competing title styles
  separate nothing across 119 videos — the first properly powered "no effect"
  this channel has produced. And only about 1 view in 70 arrives through search:
  96.6% come from the feed, where the opening second decides whether someone
  stays. **So the new top experiment changes that opening second**, which today
  is spent on our channel name and a label reading "today's top question"
  rather than on the question itself. No AI requests, no new narration, and a
  rollback rule agreed in advance.
- **The AI allowance is now choosing our work, not just costing effort** — it
  is what blocks the experiment previously ranked first. Raised with you, with
  three costed ways out, one of them free.
- **Applied your decision** on how a release is judged to that experiment,
  which was still written against a measure that cannot be measured here. That
  closes the previous shift's open item.
- Two process notes, because they cost time: the rules tell me to propose a
  change like this on a branch for you to review, and I cannot — my access
  refuses to create or change automated jobs at all, so the patch has to be
  pasted into the issue. And this same fix was queued once before as "add it to
  the approval already waiting" — it died silently when you closed that one.

### Research
- Nothing this shift. The release-check failure and the flat-channel response
  took the time, and neither left a question outside reading would settle.

### Feature work
- Nothing built. The check that guards shipping was itself broken, so fixing it
  was what stood between us and shipping anything at all.

### Blocked
- The one-line approval, without which a failed release check stays unreadable.
- Your call on the AI allowance; until then the previously-top experiment can
  be prepared but not run.

### Next
- Build the opening-second change and dry-run it — that needs a render this
  kind of session cannot do directly and must ask the video job to produce.
- Check tomorrow's release check. If it passes, the three-day failure was the
  allowance running out, and it closes.

### Better?
- **Than last shift:** yes. Last shift knew the check was failing and could not
  find out why; this one proved the code healthy, removed one cause, and
  stopped the daily waste the failure was causing.
- **Than ~10 shifts ago:** yes, narrowly. Ten shifts ago a release could not be
  measured at all; now it can, and that same tooling is what shows the channel
  is flat — worse news, honestly arrived at. The uncomfortable pattern is how
  many of those shifts went on the machinery rather than on what we publish.
- **Than ~100 shifts ago:** too early to say.

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

## 2026-09-20 (afternoon) — maintenance (stale-then-real gate failure)

    Allocation (planned→actual %): rounds 10→5 · maintenance 15→70 · pm 15→15 · research 10→0 · feature 40→0 · close 10→10

The recorded FAIL was stale, but re-checking found a real, different fault:
with reasoning restored, the R4.6 screen still missed a paraphrase of the
identical `sexual_suggestive` shape while catching the literal in-prompt
example. **One example doesn't generalize a category.** Fixed in `89bc245`,
pinned by a test; full finding in `TECH_DEBT.md`.

**A fix verified once, live, is a sample of one.**
