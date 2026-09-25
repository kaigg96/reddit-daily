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

## 2026-09-25 — the new opening is live; the next upload is the first to open on the question

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→10 · security 5→5 · pm 20→15 · research 15→25 · feature 25→20 · close 10→15

**Summary:** The new opening, where the video starts on the question instead of the channel name, is live. This morning's upload (around 05:00) is the first to use it. It is the first change to the videos themselves since the channel went flat six weeks ago, and it can be judged after 20 uploads, around 4 October.

### Feature work
- **Put the new opening live.** Both agreed conditions were met: last night's upload was the 10th in the old format, and the sample passed on exactly the version that shipped. All tests pass.

### Maintenance
- Every scheduled upload landed, and the saved record of the last post is intact.
- **The fix that records why titles fail is ready for its sample video**, updated to include the new opening. I did not request the sample: at this hour it would use the AI allowance this morning's upload needs, which is what cost an upload its title yesterday.

### Security
- Standing check clean: no credentials committed, and the secret files are still excluded.

### Project management
- **Channel still flat** at 11–12 seconds watched per view. The new opening is the right response: a change to what viewers see.
- Nothing is waiting on your approval, and the process health check is clean.
- **Tidying, for when convenient:** five of your own branches (the pre-trip work and four fixes from 23 September) are already fully in the live version. They can be deleted, but I've left them because they're yours.
- **Friction, noted rather than acted on:** two finished changes each wait for a sample video. Shifts get one each, and only at hours that don't compete with an upload. This shift ran at 02:00, outside those hours, so the queue didn't move.

### Research
- **Tested and dropped an idea within the shift: making the ending loop back into the opening.** Nearly all our views come from the Shorts feed, where a looping video plays again. The free check was whether any past videos were watched for longer than they last on average, which only replays can cause. Only 3 of 110 were, so we are not building it. The check stays in our reporting tool, so this can be revisited.

### Blocked
- Nothing is blocked on you.

### Next
- After 07:00, request the sample for the title-failure fix and ship it if it passes. The topic-recording change for the next experiment is next in line. Both are now up to date with the live version, so either can be requested as is.

### Better?
- **Than last shift:** yes. The new opening went from "passed, waiting" to live.
- **Than ~10 shifts ago:** yes, modestly. A tested change reached viewers without needing your review, which is what the automated release process was built for. Whether it helps is too early to say.
- **Than ~100 shifts ago:** too early to say.

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
