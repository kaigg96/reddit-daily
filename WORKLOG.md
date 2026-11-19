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
- **General management:** the queue was below its minimum. I proposed eight items, and a fresh reviewer ranked them in both orders. The top three were done tonight (above).
- **Reliability and security (checked):** last night's upload landed (20:46); money controls intact ($0.47 this month, forecast $0.77 of $3). No secret committed, no workflow change. AI use: no Google requests (the test video ran with no keys present), no paid voice.
- Balance: two fixes (the tests' Google access, the review's two faults), the rest preparation for a bet that is already decided.

### Blocked
- The test video needs a daytime shift: after Google's 07:00 reset, an hour clear of an upload, one per shift.
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

---

## 2026-11-18 (12:18) — The replacement show was waiting on a read our own plan says not to wait for; that is fixed, and it is one test video from being switched on

    Worked (% of the shift): product 35 · strategy 25 · engineering 15 · data 10 · gm 15

**Summary:** The show meant to replace Reddit could not start uploading until mid-December, because its music change was waiting on bet 1's read, against our own plan. The music now changes only on the new show, so it can start in days, and it has three more weeks of real uploads to be judged on before it takes every slot on 5 January.

### Toward revenue
- **Directly, on the company's biggest risk.** Reddit ends for us on 12 January, and the takes show is the floor that keeps uploads going. Started mid-December, too few of its videos would be a week old by 4 January for our rules to judge it, so it would have taken over unchecked. Starting ~21 November, about 35 will be.
- Left before its first upload: one test video (prepared and checked for free; it covers both the slot switching and the music), then merging the two and switching it on (its judging rule is set).

### Done
- **Strategy (a decision):** the four new free music tracks rotate on the takes show only. The Reddit videos keep today's single track, so bet 1's read is undisturbed. A fresh reviewer argued against it and found a real flaw: the shows alternate, so without a fix the new show would repeat its own track one day in four. That is fixed, and its other conditions are recorded (watch for copyright claims on each new track; name the music difference when the show is judged).
- **Product (checked):** the slot switching's test video for the Reddit show passed (32 seconds, sound, no dead air). The one for the new show is ready to request.
- **Engineering (a fix before launch):** the music change was reworked onto the current code, with three new tests. A fresh review found nothing blocking, and all 1,458 tests pass. Nothing changed on the live channel.
- **Data (a rule set in advance):** the test that decides whether the new show takes every slot on 5 January is now written down, before its first upload: it compares how long viewers watch each show over the same weeks, read once on 4 January. It can only fail on at least 20 new-show videos and a clear shortfall; otherwise it takes over as planned. Two fresh reviewers checked it.
- **General management (a fix to the method):** the project board's daily check now warns when a task waits on another that is blocked, and says why. On yesterday's board it names exactly the stall above. Reviewed and merged.
- **Product (checked):** no clip in use meets the rule for retiring clips that bury uploads.
- **Reliability and security (checked):** this morning's upload landed (07:47); money controls intact ($0.45 this month, forecast $0.75 of $3). No secret committed, no workflow change. AI use: one test video (a few Google requests); no paid voice. **A mistake:** a trial run of the tests with the new show switched on was not shielded from Google, and some requests may have gone out from the shared daily allowance; recorded, with the fix, for the switch-on.
- Balance: one bet (the decision) and its rule, two fixes (the repeat, the board's check), the rest checks.

### Blocked
- The new show's test video needs a daytime shift (after Google's 07:00 reset, clear of an upload): one per shift.
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **First, by day:** request the new show's test video. If it passes, merge the slot switching and the music, then switch the show on: its judging rule is already set.
- Before switching the new show on: shield the tests from Google and pin ten tests to the switch's off position (the trial found them; recorded with the code-health notes). The slot switching and the music merge cleanly together (1,476 tests pass).
- The 23 November weekly review: a free project slot for the genre study.

### Better?
- **Than last shift:** yes: the replacement show's start moved from mid-December to days away, with time to judge it before the cutover.
- **Than ~10 shifts ago:** unclear: the replacement exists and is nearly live, but watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.
