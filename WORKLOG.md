# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PLAN.md](PLAN.md) (the company), [PRD.md](PRD.md) §0 (the product) and
[TECH_DEBT.md](TECH_DEBT.md) (code health).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it within its word budget (`scripts/context_budget.py`) by deleting the
oldest entries; git history keeps them, and the audit reads them there.

**Entries are emailed to the owner verbatim as the shift report.** Write for a
manager, not an engineer: plain language, no filenames, no jargon. Technical
detail belongs in the commit message and `TECH_DEBT.md`, which is where the
next shift looks. Follow this template exactly — the report is generated from
its structure:

```
## 2026-10-06 — one line on what actually mattered

    Worked (% of the shift): reliability 10 · product 30 · engineering 30 · strategy 20 · gm 10

**Summary:** Two sentences. What moved, and whether it brought the company
closer to revenue. No detail — this is the part read on a phone.

### Toward revenue
- What this shift did that moves the company toward revenue, or "nothing
  directly, because …". Say it plainly either way.

### Done
- **Engineering:** one bullet per thing done, in plain words, led by its
  function. Say whether it fixed something or was a bet, when that isn't obvious.

### Blocked
- What is stuck, and what it is waiting on.

### Next
- What the following shift should pick up.

### Better?
- **Than last shift:** is the company closer to revenue — yes/no/unclear, and the specific thing.
- **Than ~10 shifts ago:** same, naming evidence rather than impression.
- **Than ~100 shifts ago:** same, or "too early to say".
```

**`Worked`** uses the short names of the functions in `ORG.md` (strategy, gm,
market, audience, distribution, monetization, product, editorial, engineering,
reliability, data, finance, legal, security), and it must total 100%. Since
2026-10-05 a shift works one ranked queue, so there is no planned column and no
heading per function: a function the shift did not touch is simply absent.
Reviews (`/review`) use the same shape, and the monthly one adds the sections
its skill lists. Read the series with
`venv/bin/python scripts/context_budget.py --allocation`.

**On the "Better?" section.** Numbers lag and no single one judges the
company, so a subjective read is part of the record — but a shift grading its
own work is exactly the bias the research warns about. Two rules make it worth
having: answer **comparatively** against a named horizon rather than rating out
of ten, and **name the evidence**, not the feeling. "Unclear" is a real answer
and more useful than a confident guess.

---

## 2026-11-19 (12:20) — The replacement show is switched on: its first video goes up tomorrow evening, and the checks that will judge it now work

    Worked (% of the shift): strategy 30 · gm 20 · reliability 15 · legal 15 · data 10 · engineering 10

**Summary:** The takes show, which keeps uploads going after Reddit ends for us on 12 January, passed its one test video and is live: from tomorrow evening the channel uploads one Reddit video and one takes video a day. Three smaller fixes make sure it is judged on what viewers did, and not on a copyright block or a scheduling delay.

### Toward revenue
- **Directly, on the biggest risk.** Uploads no longer depend on Reddit alone. The first takes video goes up on the evening of 20 November, and about 35 will be a week old by the 4 January read that decides whether takes takes every slot.
- The fixes below protect that read. A takes video blocked by a copyright claim would have counted as nobody watching it. And a late upload run would have shown up as a missed day.

### Done
- **Strategy (shipped):** the test video passed (21 seconds, sound, one of the new music tracks, nothing of Reddit's in the text). Merged, with all 1,482 tests passing. Today's two Reddit uploads are unchanged, and takes starts with the next evening slot of 20 November.
- **Legal (a fix to the plan):** our plan was to check each new music track's first takes video for a copyright claim. It turned out no shift could actually make that check, since shifts have no YouTube access and YouTube's pages block our machines. The Monday analytics job, which does have access, now records whether YouTube rejected or region-blocked each recent video. The first read is on 23 November. Reviewed fresh; nothing blocking.
- **Reliability (shipped, promised since October):** the upload log now records which scheduled slot each run belonged to. GitHub starts our runs 5 to 9 hours late, and the Monday report was reading a late run as a missed day. Reviewed fresh; nothing blocking.
- **Data (a fix):** takes is exempt from the automatic undo rule until its 4 January read. That exemption now ends by itself at the 5 January cutover, so no future shift has to remember to remove it.
- **General management (a fix to the method):** the project board was telling every shift to start a costly new round of project proposals, even though two projects are already running (our limit) and a third is planned and waiting. It now says to wait. I proposed six items, a fresh reviewer ranked them in both orders, and I did the top four. I also deleted 123 old branches whose work was already merged or superseded, and merged a second one promised for after the current release (the Monday report's count for bet 1 now reads only the videos its verdict reads, as set in October); 20 unmerged remain.
- **Reliability and security (checked):** this morning's upload landed (07:44). Money controls are intact ($0.49 this month, forecast $0.78 of $3). No secrets committed, no workflow change. AI use: one test video (a few Google requests); no paid voice.
- Balance: one bet shipped (the takes show), four fixes.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **21 November, first:** check the first takes upload (logged as takes, nothing of Reddit's in the title, description or tags), then mark the takes task done.
- **Then:** a new task, written tonight. Nothing in the code yet hands every slot to takes on 5 January, so without a shift that day, half the uploads would fail from 12 January. The task makes it a date in the code. It can be handed to a helper agent as the first task of the trial of that way of working.
- **23 November:** the weekly review. Read the new claim columns for each music track's first takes video, and drop any track that was rejected or blocked. Count how often takes runs fell back from Google's AI, since two takes runs share one day's allowance on 20–21 November; already 3 of the last 5 uploads did, so each show's rate gets named beside the 4 January read. Bet 2's capitals test also reads that day, and takes videos cannot leak into it, because its 30-a-side sample closed on 16 November.
- The queue holds one ready item, well under its minimum of five, so the next shift should generate more work. Dropped today: a test against takes videos mentioning Reddit (one already exists); counting Google requests per takes run (the weekly review does it); a tidy-up of the takes run's startup message (cosmetic, recorded).

### Better?
- **Than last shift:** yes. The replacement show is live, not one test video away, and the checks that will judge it now work.
- **Than ~10 shifts ago:** yes. Around 15 November the takes show was built but switched off, with no rule to judge it. Now it uploads daily under a rule set in advance. But watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-19 (01:13) — The switch that starts the replacement show is built, reviewed and one test video from going live; the review caught two faults that would have spoiled its judging

    Worked (% of the shift): engineering 35 · strategy 25 · data 15 · product 10 · legal 5 · gm 10

**Summary:** The change that starts the takes show uploading daily is now ready on its own branch, with a matching test-video branch, so tomorrow's one daytime test video settles it and it can go live the same day. A fresh review of it as a live change found two faults that would have muddied the 4 January decision; both are fixed.

### Toward revenue
- **Directly, on the biggest risk.** Reddit ends for us on 12 January; the takes show is what keeps uploads going after it. Before tonight, going live needed two test videos and four separate merges. Now it needs one test video and one merge, which a single daytime shift can do.
- The two faults fixed would each have weakened the 4 January judgement: about 1 takes video in 9 would have used the Reddit show's music, against how the rule describes the two shows, and the Monday report would have told a shift to switch takes off in mid-December, under a different rule, before its own read.

### Done
- **Engineering (a fix):** our tests could use the real Google allowance that the uploads share, if any part of the code was left untested. They no longer can. Live on the main line.
- **Engineering (prep):** nine tests that check the old single-show behaviour are pinned to it, and a new test checks that the Reddit cut-off still stops a run cleanly once the two shows alternate. With the switch on, everything passes (1,479 tests).
- **Strategy (prep):** the switch-on itself is on a branch, with a twin that forces the test video to show the takes show. A free local test video of the switched-on code played (26 seconds, new music track).
- **Product (two fixes from the review):** takes now uses only its four new tracks, and the Monday report leaves takes to its own rule. A third check: the 4 January read command gives a real comparison rather than a refusal once there are enough videos, now held by a test.
- **Legal (a question answered):** can a shift tell if a new track gets a copyright claim? Partly. A claim that blocks or rejects a video shows up in what we can read. A claim that only takes the ad money or tracks the video reaches only your email. Our rule is now to check each track's first takes video two days after it goes up. No ask for you: a money-only claim costs nothing while we earn nothing.
- **Engineering (tidy, same branch):** the music notes and a test still described the old rotation; corrected. A second fresh review of everything added after the first: nothing blocking.
- **General management:** the queue was below its minimum. I proposed eight items, and a fresh reviewer ranked them in both orders. The top three were done tonight (above).
- **Reliability and security (checked):** last night's upload landed (20:46); money controls intact ($0.47 this month, forecast $0.77 of $3). No secret committed, no workflow change. AI use: no Google requests (the test video ran with no keys present), no paid voice.
- Balance: two fixes (the tests' Google access, the review's two faults), the rest preparation for a bet that is already decided.

### Blocked
- The test video needs a daytime shift: after Google's reset (08:00 UTC in winter), an hour clear of an upload, one per shift.
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **First, by day:** request the test video of the switch-on twin branch. On a pass, merge the switch-on branch: that merges the slot switching, the music and the switch together, and the takes show starts with the next upload. Then mark the epic's tasks and the product tracker done, and check each new track's first takes video for a claim two days after it uploads.
- Keep Google requests low on days with two takes runs in a row (recorded with the code-health notes).
- The 23 November weekly review.
- Dropped tonight: whether video length explains the falling watch time (it changes no pending decision, as the Reddit show is ending); two play-along fixes (that show cannot run before February); re-pricing other revenue routes (the next quarter's project covers it); measuring how bland the takes questions are (needs Google requests, so a daytime job, and the takes rule is already set).

### Better?
- **Than last shift:** yes: the replacement show is one test video from live, not two videos and four merges, and two faults in how it would be judged are gone.
- **Than ~10 shifts ago:** yes, narrowly: the replacement exists, has a rule written before it starts, and is days from uploading; but watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.
