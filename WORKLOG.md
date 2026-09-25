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

## 2026-09-24 (afternoon) — the new opening's sample video passed; this morning's upload went out without its generated title

    Allocation (planned→actual %): rounds 10→15 · maintenance 20→20 · security 5→5 · pm 15→10 · research 0→0 · feature 40→35 · close 10→15

**Summary:** The new opening passed its sample video and goes live after tonight's upload, as agreed. This morning's upload shipped with the plain Reddit question as its title, the second time in this format. The likely cause is the shared daily AI allowance running out, and the fix for that is now due.

### Feature work
- **The new opening's sample video passed** (right size, sound throughout, no silent gaps). I first updated the opening with everything live since it was built, so the sample tests exactly what ships. The agreed rule waits for the 10th upload in the current format (~17:00 tonight), past this shift's 30-minute limit, so tomorrow's shift puts it live.

### Maintenance
- **This morning's upload lost its generated title, search keywords and closing question.** It shipped with the Reddit question as the title instead. That is 2 of the 9 uploads in the current format, and both were morning runs. The morning run is the last one before the daily AI allowance resets, so it is the one that goes short when other jobs have spent it. The record logs *that* the title failed, not *why*, so I built a change that records why. It waits for its own sample run.
- Every scheduled upload landed, and the saved record of the last post is intact.

### Security
- Standing check clean: no credentials committed, and the secret files are still excluded.

### Project management
- **Your approval for sample videos is done and closed.** It worked end to end on the first try: requested at 14:17, rendered and judged by 14:20.

### Research
- Nothing this shift. The shift has a 30-minute limit, and shipping the new opening came first.

### Blocked
- Nothing is blocked on you.

### Next
- Put the new opening live, as long as tonight's upload landed and the branch hasn't changed since the sample. Then update the plan. Its result can be read after 20 uploads, no earlier than about 5 October.
- Sample-run and ship the change that records why the title step fails. Then, if the allowance is confirmed, make the other jobs check the day's spend first.

### Better?
- **Than last shift:** yes, a little. The new opening moved from "waiting to ask for a sample" to passed and ready to go live. The morning title failure is now counted, not just noticed.
- **Than ~10 shifts ago:** unclear. The release process is much sturdier, but nothing new has reached viewers yet and the channel is still flat.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-24 — the new opening is queued for its sample video, a wrong "revert" verdict is fixed, and the next experiment no longer waits on the AI allowance

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→10 · security 5→5 · pm 25→25 · research 10→10 · feature 25→30 · close 10→10

**Summary:** The new opening is ready for its sample video, which is requested as soon as the morning upload has landed, so the two don't compete for the day's AI allowance. The release check had been ignoring your 22 September decision to judge on watch time only, and would have undone good work on view-count noise. That is fixed, and the next experiment is built to run on a free allowance of its own.

### Feature work
- **The new opening can finally get its sample video.** Your change last night gave shifts a way to ask for one. The request waits for this morning's upload, so it doesn't use AI requests that upload still needs. It can go live after tonight's upload, the 10th in the current format, if the sample passes.
- **Built the first step of the next experiment**: choosing between the day's
  top few questions by topic. Every video now records the topic of every
  question it could have used, not just the one it picked. That tells us how
  often a topic-based choice would differ from Reddit's own order, which sets
  how long the experiment must run. The choice itself is unchanged. It uses a
  second AI model, so it doesn't draw on the daily allowance the uploads
  share, and it costs nothing (your answer on the allowance: free routes only).
  It needs its own sample video before it goes live.

### Maintenance
- **Caught a break before it reached you.** Last night's changes added tests
  that need a library nothing installs, so the test suite could not start.
  This morning's release check runs those tests. It would have failed, and
  would have kept showing yesterday's "pass" while doing so. Fixed and live.
- Every upload since the last shift landed. The saved record of the last post
  is intact.

### Security
- No credentials committed; the secret files are still excluded.
- **New finding, logged rather than fixed:** the two automatic jobs that try
  out unfinished work (the sample video and the release check) run it next to
  a key that can change the live branch. Changes made with that key skip the
  guard that protects the rules. Nothing suggests it has been used. The fix is
  a restructure I can't test from here, so I'm deliberately not asking you to
  approve it from your phone while you're away. It's written up for after.

### Project management
- **The release check was applying the old rule.** You decided on 22 September
  that only watch time can trigger an undo, with views shown but never
  deciding. The check's code was never changed. It still said "undo the
  background videos" on views alone, while watch time on them was up 22%. And
  it would have said the same about the new opening on a bad week for views.
  Fixed. The background videos now read "keep".
- **Your decisions:** everything you approved yesterday is live, and I closed
  those requests. You approved "run the tests on every change" within minutes
  of my asking; it applied itself, so approving from your phone works end to
  end.
- Brought the tech-debt list back under its cap by closing items your changes
  had already fixed.

### Research
- **YouTube reports "engaged views" per video**: plays that got past the first
  moment. That is the most direct measure of what the new opening changes. We
  collect it every week from Monday. It sits beside the agreed rule and never
  replaces it.

### Blocked
- Nothing is blocked on you. The new opening waits only on its sample video and on tonight's upload.

### Next
- Read the sample-video verdict. If it passes and names the branch's current commit, put the new opening live (merge commit, so the verdict's commit is the one that ships), then update the plan.
- Ask for the topic-logging step's own sample video (one render per 12 hours).
- Check that the 08:17 release check now explains its verdict (your change #21). If it passes, close the stale release-failure alert.

### Better?
- **Than last shift:** yes. The new opening went from "no way to get a sample
  video" to queued for one. And a verdict that would have undone good work on
  noise now follows the rule you set.
- **Than ~10 shifts ago:** yes, on evidence. Approvals now apply from your
  phone within minutes (one did today). Tests run on every change. The
  release check follows the rule you set. None of this was true ten shifts
  ago. The channel itself is still flat, and nothing new has reached viewers
  since mid-September, so the outcome hasn't moved yet.
- **Than ~100 shifts ago:** too early to say.

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
