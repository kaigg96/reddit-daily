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

## 2026-10-13 (23:17) — Bet 1's final version plays; your label on #74 is now the only step

    Worked (% of the shift): product 25 · data 20 · reliability 20 · gm 15 · engineering 10 · security 10

**Summary:** The exact version of bet 1 that would ship was rendered tonight and plays, with all of the host's lines on screen; its four frames are on #74, so judging it takes a glance from a phone. Nothing reached viewers yet; your label ships it.

### Toward revenue
- **Bet 1, our best answer to YouTube's reused-content rule, is one label from shipping.** Tonight's sample is the final build, brought up to date with this afternoon's library fixes: it played (29 seconds), showed all three of the host's lines plus the vote, with the capitals fixed, and our own words were 44% of what the viewer gets. #74 now shows its four frames inline.
- **Four uploads a day, bet 2's lever, came closer:** the plan no longer reads as if it waits for a separate release, and its last missing piece is built (below), so it can switch on the day its read allows.

### Done
- **Product:** the sample above, and the frames on #74. Two checks a sample cannot make: the first live upload of bet 1 adds four columns to our upload record, so I replayed that on a copy (old rows intact, new row right); and bet 1's pre-committed read runs as written today, so tooling will not hold it up when its 20 uploads are in. Also made plain in the plan that four uploads a day waits only for the Groq backup, which ships inside bet 1, not for a separate release; the old wording could have cost bet 2 about two and a half weeks.
- **Data:** two pre-commitments made before any data, so later reads cannot be bent: the title tests (style B and the capitalised word) will also be read on the share of plays YouTube actually counts, since their extra views could be swipe-aways that don't count toward the bar. Today's read is too thin to say (9 against 14 uploads). Also checked whether buried uploads (5 views or fewer at a week, 13% of them) share a topic, title style or version: none does beyond chance. **Fixed a fault in the reporting tool's count of the views YouTube's bar counts:** it read every video's lifetime total as one week's gain, so it showed about 21,400 such views per 90 days; the one week actually measured supports about 9,600, in line with the plan's 11,000 to 13,000. No tracker had quoted the wrong figure, but the next read of bet 2 in those views would have (reviewed, its two risks fixed, merged).
- **Reliability:** every upload landed, including this evening's; the record of the last upload is intact; Gemini failed on 1 of the last 20 uploads. GitHub's late starts have never made two video runs collide (none in 99 runs since August; the closest were 3.5 hours apart), which matters once we post four a day.
- **Reliability, for bet 2 (four uploads a day):** built its last missing piece, on a branch behind bet 1. Each upload now records the slot it was scheduled for, and the weekly report counts it under that day and times its delay from that slot, so a run GitHub starts after midnight no longer reads as a missed day. Two fresh reviews found no bugs and two risks, both fixed: an upload started by hand would have recorded a guessed slot that looked like a scheduled one, and one hand-edited value could have stopped the weekly report. It merges after bet 1, before four a day is switched on; a sample cannot exercise it, since test renders never write the upload record. The safety screen's weekly audit is clean: one post skipped since September.
- **Engineering:** three tests failed whenever a dry run's setting was left on in the shell, which reads like a regression; fixed on the same branch, without loosening the guard that keeps tests from uploading or spending (reviewed).
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.37 this month, forecast $0.88 of $3); tonight's sample logs hold no keys.
- **General management:** your replies since 20 September fall on 15 of 24 days, with gaps of up to three days. So #74's wait is still within your normal rhythm, and the rule that fires tomorrow morning should check that before changing how asks reach you. Fixed the tracker checker, which flagged a closed issue as open for the third time in three weeks (reviewed, merged).
- **Dropped after ranking:** varying the video's template (waits for bet 1's read, as planned); a subscriber-rate metric (views, not subscribers, are what stands between us and the smaller tier); the 60-second safety stop in the upload code (never fired, and it would touch bet 1's branch). Fixing against improving: mostly improving (bet 1 made shippable, four a day's last piece), plus one fix and measurement.

### Blocked
- **For you, in order:** #74 (bet 1: a glance at four frames, then a label); #50 (four commands; it unblocks #65); #75 (comments, one label); #59 (account checks). Adding two or three music tracks also answers the template risk.

### Next
- On #74's label, merge bet 1's branch as the next version in one step (its sample names its current commit), then update the trackers.
- Tomorrow's 08:17 release check reads the same build; a PASS there is expected.
- Once bet 1 is live, merge the slot-recording branch (it sits on top of bet 1; tested and reviewed twice) before four a day is switched on.
- If #74 is still open at 10:49 tomorrow, read the rhythm note in the decision log before re-asking.

### Better?
- **Than last shift:** Slightly. Bet 1 went from "needs a final sample" to "needs only your label", and the title tests will now be read on the views that count. Nothing reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds and bet 1 is still unshipped, though it is now fully built and sampled.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-13 (18:19) — YouTube doubles its bar for new channels from February; the process audit finds your queue is still the limit

    Worked (% of the shift): gm 40 · monetization 15 · product 10 · reliability 10 · market 5 · strategy 5 · engineering 5 · data 5 · security 5

**Summary:** YouTube announced in August that from 1 February 2027 a new channel needs 20 million qualifying Shorts views in 90 days to earn ad revenue, double today's bar. Its smaller tier (500 subscribers, 3 million views, unlocking fan funding and Shopping) is unchanged and is now our nearest route. The process audit came due and found the owner's queue is still what holds bet 1 back.

### Toward revenue
- **Nothing shipped to viewers.** Bet 1 still waits on your label (#74), and its sample cannot run before 22:43 tonight.
- **Bet 1's ask is now a glance:** until now, judging it meant downloading a zip from GitHub, unzipping it and playing a silent video, which is hard on a phone. #74 now shows four frames of the sample inline, in the email too: the host's three lines and the closing vote.
- **The target moved:** the plan now records the February change and the smaller tier, about 250 times our current qualifying views, against roughly 800 times for today's full bar. No direction changes on this alone; it goes to the monthly review on 5 November.

### Done
- **Reliability:** every upload since Friday landed; the record of the last upload is intact; tonight's evening run had not started at 18:30, which is normal given GitHub's delays. Two libraries that decide which posts, comments and host lines ship were unpinned, so each run took whatever was published that morning. They are now pinned at today's versions, with a check that fails if any library is ever left unpinned (fixing; reviewed, live).
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.37 this month, forecast $0.88 of $3). New this shift: the logs of every job that holds our keys are public, so I scanned the last 17 for leaked credentials, including the short-lived tokens GitHub does not hide. None found.
- **Monetization and market:** read YouTube's own pages and its 10 August announcement (above). The template risk is also audible: all of the last 30 uploads use the same music track, so the music task on your list now answers a confirmed monetization risk.
- **General management (the audit, 13 shifts since 9 October):** re-reviewed all eleven live decisions, each with a date. Findings: label-only asks used to close within a day and #74 has now waited over two; the rule that a shift cannot read the video job's logs is false (three shifts did it), and its fix waits on #50 because shifts cannot edit their own rules; independent reviews caught real defects in 11 of 13 shifts, while sample videos only prove a video plays; 7 of 13 shifts ended early. New from the tool's docs: a stop guard can no longer loop a shift, so "don't stop before the handover is saved" can become a rule enforced in code, proposed after #50. Bet 1's read and four uploads a day would overlap, so four a day now waits for bet 1's read if bet 1 is still being measured.
- **Also checked:** the ban on shock phrases in titles is holding (none in 6 titles since it began, against 3 in 18 before); GitHub's start delay keeps rising (typical 4.4 hours in early September, 6.5 this week), which the uploads handle but the weekly report will misread at four a day.
- **Dropped after ranking:** whether upload time matters (already answered: it doesn't); a fix for false "missed day" warnings at four a day (it needs each run's slot logged, after bet 1); building the stop guard or the rule fixes ahead of #50 (they would sit unused); the safety-screen gap, the setup line's display time and the image-library upgrade (each needs a sample or your label first). Handed over about 35 minutes early because nothing else cleared the bar. Fixing against improving: mostly fixing and measurement; improving: bet 1's ask made answerable.

### Blocked
- **For you, in order:** #74 (bet 1: watch tonight's sample, then label); #50 (four commands; it unblocks #65 and the rule fixes above); #75 (comments, one label); #59 (account checks). Adding two or three music tracks now also answers a monetization risk.

### Next
- After 22:43, request the sample of bet 1's branch. It also carries the Groq backup; my recommendation is to let it ride, because it only answers when Gemini fails (about 1 upload in 10) and without it those uploads would ship with no host at all. Bet 1's read can count those uploads separately with the existing report.
- When tonight's sample lands, put its frames on #74 the same way (the image lives on its own branch; keep that branch while #74 is open).
- If #74 is still open at 10:49 tomorrow, the rule about how long your asks wait has fired: the next shift should re-think how bet 1 reaches you rather than ask again.

### Better?
- **Than last shift:** Slightly. Nothing reached viewers, but the company's target is now the real one, bet 1's one remaining step can be taken from a phone, and a silent risk to every live run is gone.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds and bet 1 is still unshipped, though median views at 7 days rose from 64 to 91.
- **Than ~100 shifts ago:** Too early to say.
