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

## 2026-11-10 (03:00) — Weekly review: the rise in videos nobody is shown is still unexplained; the backup question source for after Reddit starts building now, not on 14 December

    Worked (% of the shift): data 35 · strategy 20 · gm 15 · reliability 10 · security 5 · editorial 5 · legal 5 · audience 5

**Summary:** The weekly review found watch time flat and about one video in seven still getting no views, for reasons we cannot find; bet 1 still waits on you. Because you have been away three weeks, I started building our own-questions source now, so uploads can continue after Reddit's cutoff with one label from you.

### Toward revenue
- **Nothing directly.** Watch time is flat at 11–12 seconds. One thing protects bet 1's result: when it ships, it will be judged against the videos made just before it, including the ones on the new AI model. Without this it would have been judged against the channel's whole history, which earlier analysis showed could let a worse version pass. I settled this before any bet 1 video exists, so the choice cannot be bent to fit its result.
- **Keeping the channel alive after January.** Our own questions are the one source whose earnings Reddit's terms do not forbid. The build is half done and switched off.

### Done
- **Data (weekly review):**
  - **Videos nobody is shown:** still about 1 in 7 recently, against 1 in 40 before. The rule set on 2 November said to check whether one of our two subreddits causes it. It does not: the difference is within chance. No background clip stands out either. So it goes to the December monthly, as the rule says.
  - **Feed views:** 2,829 this week after 3,823. For ten weeks a high week was always followed by a low one, and this time it was not. The test of whether those swings are real viewers or a quirk of how the data arrives reads next Monday, so nothing is concluded yet. Subscribers went from 23 to 26.
  - **Viewer comments:** none at all in the week, across the last 20 videos.
  - **The safety screen** skipped 3 posts this week. All three were right to skip (speculation about a named person, a prompt inviting sexual punchlines, too few safe comments), so it stays as it is.
  - **The new AI model:** three uploads so far, and none hit the daily limit. One title was refused by our shock-phrase filter and shipped the Reddit question instead. The old model had 2 such refusals in 30. The rule set on 8 November counts them at the new model's 20th upload.
- **Data (built, live):** bet 1's comparison, above. A fresh review found no bugs, and it changes how no other test is read. It is reporting only, so viewers see nothing.
- **Reliability (checked):** all 15 uploads since last Monday landed. Three went out with the Reddit question as their title: two old-model failures and the one refusal. Scheduled jobs still start hours late (last night's evening upload went up at 22:34), and the upload code handles that correctly.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, and the money controls are intact ($0.23 this month, forecast $0.74 of $3). Library warnings are unchanged (Pillow and oauthlib, already listed).
- **Editorial (checked):** I read everything the new model has published so far: titles, closing lines and top comments. Nothing was wrong. All three closing lines end by asking viewers to comment, against 3 of the old model's last 8. Too few to call; it is counted again at the 20th upload, since YouTube's spam rules name sameness.
- **Legal (checked):** Reddit was reported to be updating its terms on 10 November. Its two terms pages and its registration page are unchanged as of 02:30 UTC. That is still 9 November in the US, so the next shift looks again.
- **Data (rule, before any data):** the rise in videos nobody is shown began on 15 October, the same day the capitals-in-titles test started. When that test is read on about 23 November, it will also say whether one of its two versions accounts for the rise. Nothing about it was read today, and the extra figure cannot change the test's verdict.
- **Strategy (date moved):** uploads stop on 12 January unless our Reddit app is registered (#82). The backup plan was to start building our own questions on 14 December, which left four weeks for your label. That assumed your slowest label so far, 4 days. It has now been 21 days since you last replied, so the build starts now instead. Reddit's free access ends in March even if we register, so the work is needed either way. It costs nothing, ships switched off, and turning it on is still one label from you. #90 now says so (editing it sent no email).
- **Strategy (started, not live):** I began that build on a separate copy of the code. It writes our own question and three takes, runs them through the same safety screen as Reddit posts, refuses any question we have already shipped, labels each answer a take, and credits no one. It is off unless switched on, so uploads are untouched. A fresh review found nothing that touches today's uploads. I fixed four of its points on the new path the same day; one that matters is left: the step that writes titles still assumes a Reddit post, so a title could present our takes as real people's answers. That, then one sample video, come before it merges, still switched off.
- **General management (ranking):** nothing was ready after the review. A fresh helper proposed eight ideas; two survived (the model's text and Reddit's terms), and I added the third. A second helper ranked the three the same way forwards and backwards. A second round, aimed at the functions not yet touched, found only the date change above. Dropped: re-planning bet 2 (a shift updates #80 on 20 November), closing asks (all four checked are still accurate), income outside YouTube (answered on 2 November), whether late-running uploads get fewer views (too few late ones, and they all fall in recent weeks); counting comments YouTube holds back (weekly counts already swing from 0 to 7); re-reading YouTube's money rules (read 3 November); a library upgrade (no risk to us). The friction log had nothing unsorted.
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1), #82, #89, #90, #91, #92, #93, #88, #65, #80, #59. Your last comment was on 20 October. Bet 2's window opens 30 November and needs bet 1 first.

### Next
- **Today after 08:00 UTC, an hour clear of an upload:** stage 1 of the host-line test, under its rule. Today's release check will skip (checked), because this shift touched nothing it tests.
- **The own-questions source** is the only ready item and is half built: fix the title step its review flagged, request one sample video of it, then merge it switched off. Leave the bet 1 test version untouched on the day of a host-line stage.
- **11 November:** look at Reddit's terms again (their reported update may land late on the 10th, US time).
- **16 November:** the weekly review, including the test of whether weekly view swings are real.

### Better?
- **Than last shift:** slightly. Bet 1's test can no longer be judged against the wrong baseline, and the source after Reddit is half built rather than a date. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat, bet 1 hasn't shipped, and more videos get no views.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-09 (12:15) — Shift helpers now see every recorded finding before proposing work, the biggest source of repeated work; uploads will record the new AI's unpublished daily limit the first time they hit it

    Worked (% of the shift): gm 55 · reliability 35 · security 5 · data 5

**Summary:** I fixed the most common reason shifts redo work: the helpers that propose work now see every finding we have recorded. Uploads also now record the new AI's daily limit the first time they hit it. Neither change reaches viewers, and the weekly review moves to tonight because Monday's figures had not arrived.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds. Shifts should waste less time, and bet 2's four-a-day plan will no longer rest on a daily limit nobody has seen once an upload hits it. Bet 1 still waits on your label on #77, and tomorrow's host-line test is its next step.

### Done
- **General management (fixed):** the friction log had 44 rows nobody had sorted, and the oldest would have broken its 7-day rule tomorrow. All are now grouped, in about 8 minutes (the log's rule allows about 20 a week). One group stands far above the rest: "recorded answers are hard to find, so work gets redone", 19 rows across 5 functions. Its main cause was that the helpers proposing work saw only recent drops and finished work, never the findings, so they kept re-proposing questions a finding had already answered. They now see all 56 finding headlines. A fresh review found no bugs, and it is live. It is the friction log's first fix, and its verdict on 7 December needs two that have held for 14 days.
- **Reliability (built, live):** the "20 AI requests a day" that every plan budgets on was read off the old model in September. Google no longer publishes the new model's figure, so four a day (bet 2's route) and each shift's budget rest on a number nobody has seen. Now, the first time an upload hits the new model's daily limit, its log records the limit. Logging only, so viewers see no change; a fresh review found no bugs.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas; only the daily-limit log line above survived. A second helper, aimed at the functions this shift had not touched, found nothing above the bar. It was the first to use the new findings list, which settled three of its ideas in seconds. Dropped: a rule for how bet 1's read treats the new model's version (tonight's review decides it); pre-building the replacement source (dated 14 December); more background music (it would disturb two running tests); redrafting the viewer replies (nothing posts without your label on #89). Checked and changing nothing: Google's AI terms still let it learn from what we send (last changed 23 March), and YouTube's election rules end with the vote, so our election-week skip rightly lapses on 10 November. With nothing else above the bar, I waited for Monday's figures until 12:11 and handed over at 12:15, 16 minutes early.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.21 this month, forecast $0.75 of $3).
- **Reliability (checked):** all 15 uploads since last Monday landed. Both made with the new model got AI-written titles, with no limit refusals. GitHub is starting our scheduled jobs four to eight hours late; this shift, at 11:31, was today's first.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. Your last comment was on 20 October.

### Next
- **Tonight:** the weekly review, once Monday's figures land. This shift already did its upload, security and friction-sorting steps. Left: the zero-view re-read routed on 2 November (it runs from the saved figures), the figures' other reads, viewer comments, traffic sources, and how bet 1's read treats the new model's version.
- **10 November, after 08:00 UTC, an hour clear of an upload,** if the release check is idle that day: stage 1 of the host-line test, under its rule. Leave bet 1's release untouched until then: any change to it makes that day's check run and spend the allowance again.

### Better?
- **Than last shift:** slightly: shifts should now redo less work, and the friction log's verdict stays on track. Nothing reached viewers.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
