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

## 2026-11-09 (12:25) — Shift helpers now see every recorded finding before proposing work, the biggest source of repeated work; Monday's figures had not arrived, so the weekly review falls to the evening shift

    Worked (% of the shift): gm 55 · reliability 35 · security 5 · data 5

**Summary:** I fixed the most common reason shifts redo work: the helpers that propose work now see a one-line list of every finding we have recorded. I also grouped a week of the friction log before it went stale. Monday's YouTube figures had not arrived by the end of the shift, so the weekly review moves to tonight's shift.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds. Today's work makes shifts waste less time (the fix) and keeps the friction log's 7 December verdict readable. Bet 1 still waits on your label on #77, and tomorrow's host-line test is its next step.

### Done
- **General management (fixed):** the friction log had 44 rows nobody had sorted, and the oldest would have broken its 7-day rule tomorrow. All are now grouped. One group stands far above the rest: "recorded answers are hard to find, so work gets redone", 19 rows across 5 functions. Its main cause was that the helpers proposing work saw only recent drops and finished work, never the findings, so they kept re-proposing questions a finding had already answered. They now see all 56 finding headlines. A fresh review found no bugs, and it is live. It is the friction log's first fix, and its verdict on 7 December needs two that have held for 14 days.
- **Reliability (built, live):** the "20 AI requests a day" that every plan budgets on was read off the old model in September. Google no longer publishes the new model's figure, so four a day (bet 2's route) and each shift's budget rest on a number nobody has seen. Now, the first time an upload hits the new model's daily limit, its log records the limit. Logging only, so viewers see no change; a fresh review found no bugs.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.21 this month, forecast $0.75 of $3).
- **Reliability (checked):** all 15 uploads since last Monday landed. Both made with the new model got AI-written titles, with no limit refusals. GitHub is starting our scheduled jobs four to eight hours late; this shift, at 11:31, was today's first.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. Your last comment was on 20 October.

### Next
- **Tonight:** the weekly review, once Monday's figures land. It includes the zero-view re-read routed on 2 November.
- **10 November, after 08:00 UTC, an hour clear of an upload,** if the release check is idle that day: stage 1 of the host-line test, under its rule.

### Better?
- **Than last shift:** slightly: shifts should now redo less work, and the friction log's verdict stays on track. Nothing reached viewers.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-08 (23:30) — Tomorrow's host-line test moves a day so it can't use up an upload's AI allowance; our own history shows no sign that a second daily upload takes views from the first

    Worked (% of the shift): data 30 · strategy 30 · reliability 20 · gm 15 · security 5

**Summary:** I found that tomorrow's release check and the planned host-line test would both draw on the AI allowance our uploads now use, together enough to risk the next morning's title. So the test moves to 10 November. A new test of our own history found no sign that a second daily upload takes views from the first, which supports bet 2's four-a-day plan.

### Toward revenue
- **A little evidence for bet 2's route, no revenue yet.** Watch time is flat at 12 seconds. Bet 2's route to doubling views is four uploads a day, which works only if each video keeps its views when more of ours share the feed. Our own history now says that held between one and two a day. Four a day still waits on bet 1 and your answer on #80.

### Done
- **Reliability (found, fixed in the plan):** since the switch, our daily release check runs on the same AI allowance as the uploads. Tomorrow it re-tests bet 1's release (6–8 requests), because that release changed tonight. Add the host-line test's 6 and the uploads' 4–10, and Google's day could reach 24 requests against the 20 we plan around. Its last upload, the next morning's, would then lose its AI title. So the test now waits for a day the check stays idle: 10 November at the earliest. The first week's check on the new model's daily limit now ignores days we spent from it ourselves. Otherwise our own spending would read as "the new model's allowance is too small" and send us to the model that failed every request it was sent today.
- **Data (corrected):** on #77, the comment you will read when you decide on bet 1 still gave the old model's host lines as about 21 of 27 reacting, a figure scored by eye. It now gives the blind scores, 14 of 21 against the new model's 2 of 12. Editing a comment sends no email.
- **Strategy and data (rule set before any view was read, then built):** do views per upload fall when another upload is near? Nearly every day since April 2025 had two uploads; about 45 had one. So our data can compare one a day with two, never two with four, and only a large effect would show. I wrote the rule down and published it before reading anything. It compares uploads alone against paired within the same month, so old and new eras never meet. Then I built the read with tests. A fresh review found my first wording labelled only 1 of 878 videos as alone, since uploads come 12 hours apart, so I amended the rule, still unread, to compare videos beside a missed slot with the regular rhythm. After a second review found no bugs, I ran it once: videos beside a missed slot got 1.08 times the views of the rest, inside the 17% that chance alone produces, and the same watch time. So there's no sign that a second daily upload takes views from the first. That supports four a day, though it can't rule out a smaller effect, or one at six-hour spacing.
- **General management (ranking):** nothing was ready. A fresh helper, checking against the code and data, proposed the two items above and nothing else above the bar. Both were cheap and independent, so I took both without a separate ranking pass. Dropped: a tool to plan each day's AI requests (tonight's note in the plan covers the one case that matters this week); fixing the reset hour in the sample-video gate (since the switch, renders use a separate allowance from the uploads, so the wrong hour costs nothing); redrafting the three viewer replies (they lapse on 17 November, and nothing posts without your label on #89). A last look at 23:28, after the spacing result: telling you on #80 now that four a day might double views alone. Dropped: the result doesn't touch the spam-policy risk #80 is about, and this report already tells you. Nothing else was above the bar, so I handed over at 23:30.
- **Reliability (checked):** tonight's upload, the first on the new model, landed at 18:01 with an AI-written title and no errors. The sample copy #90 links is safe on its branch.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.20 this month, forecast $0.80 of $3).

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2; its comment now carries the blind figures), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence, which still holds after the switch), #80, #59. Your last comment was on 20 October.

### Next
- **9 November:** the weekly review, and check that the morning's release check passed. **No host-line test that day.**
- **10 November, after 08:00 UTC, an hour clear of an upload,** if the release check is idle that day (the plan says how to tell): stage 1 of the host-line test, under its rule.

### Better?
- **Than last shift:** slightly: an upload's title and a sound reading of the new model's limit are protected, bet 1's issue now has the honest figure, and bet 2's route has its first evidence from our own data (no dilution found from one upload a day to two).
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

