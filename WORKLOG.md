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

## 2026-09-23 — the next experiment is built; one permission that exists only on paper stops it shipping

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→5 · security 5→10 · pm 25→25 · research 10→10 · feature 30→30 · close 10→10

**Summary:** The top experiment is built, tested and waiting: each video opening
on the question itself instead of on our channel name and a label. It cannot
go live yet because the final check needs a sample video, and a shift turns out
never to have had the access to request one. The fix is ready for you to apply.

### Feature work
- **Built the new opening.** From the first frame, the top of the screen now
  shows the whole question where it used to show "AskReddit Shorts / Today's
  top question". The channel name stays in its small mark near the bottom of
  every frame. I compared old and new frames side by side before committing.
- **Caught a flaw in my own first version.** Long questions were being cut
  short at the top of the screen, and one sample opened on "...slowly started
  becoming unwa…". That was harmless when the question only appeared after
  the viewer had heard it. As the opening it hides the point, and it would
  have affected about one video in seven. Fixed; the longest question we
  accept fits on two lines.
- **Added the first automatic check on how a video is put together.** Until
  now a mistake there would first show up as a failed live upload.

### Project management
- **Why it can't ship yet.** The rules require a real sample video before
  anything visual goes live. The shift's settings do grant permission to
  request one, but that permission is swapped out before the session starts,
  so it has never worked. Raised with you, with the two small edits that fix
  it, including a safeguard that stops a shift ever publishing by accident.
- **Timing, whatever you decide:** the new opening should not go live before
  about 25 September. The current format needs a few more uploads before its
  own check can give a verdict.
- **Your decisions:** closed the two about running shifts on the newer model.
  Both are live, and this shift ran on it. The third (making a failed release
  check explain itself) is approved, but a shift is refused permission to make
  that edit, so it needs applying by hand; I've said so on the issue.
- **Process note:** the rules say "propose on a branch" and "dry-run before
  merging", and a shift can do neither for anything touching automated jobs or
  the video. Three of the last four shifts hit this same access wall.

### Maintenance
- Every upload since the last shift landed. The daily release check
  **passed** for the first time, on live code. That matches yesterday's manual
  re-run: the earlier failures were the check, not the release. I recommended
  you close that alert.
- Subtitle uploads fail about one time in four (7 of 31), fewer than the half
  first feared. Still not worth chasing.

### Security
- No credentials committed, nothing secret-shaped in the files, job
  permissions unchanged.
- **New finding:** the image library and the web-request library we use have
  published security fixes we don't have, and our Python version stops getting
  support on 4 October. Real risk is low, because neither library ever handles
  anything from outside. Upgrading can change how videos look, though, so it
  needs its own tested release. Logged.

### Research
- **A better way to measure the new opening.** YouTube now counts a Short as
  viewed the moment it starts, and separately reports how many plays got past
  the first few seconds. That second figure measures the opening directly, and
  we don't collect it. Added to the plan as a test to run beside the agreed
  rule, never as a replacement for it.
- YouTube's August change to how views are counted affected long videos only;
  Shorts have counted this way since 2025. So it doesn't explain our view
  counts swinging.

### Blocked
- The new opening: waiting on your approval of the sample-video fix.
- Making a failed release check explain itself: approved, needs applying by you.

### Next
- If the fix lands: request the sample video, confirm it plays and that the
  safeguard is working, then put the new opening live (not before ~25 Sept).
- If it hasn't: collecting the engaged-plays figure is the best use of the
  wait, so the old format has a baseline before the new one ships.

### Better?
- **Than last shift:** yes. The top experiment went from a line in the plan to
  built and tested, and "ask for a sample video" turned out to be impossible
  as written. Now we know exactly why, and the fix is ready.
- **Than ~10 shifts ago:** unclear. This is the first change to what viewers
  see since mid-September. But nothing new has reached viewers in that time,
  and several recent shifts ended blocked on access rather than on the work.
- **Than ~100 shifts ago:** too early to say.

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

