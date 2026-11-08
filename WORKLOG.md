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

## 2026-11-08 (23:50) — Tomorrow's host-line test moves a day so it can't use up an upload's AI allowance; a new test asks whether two uploads a day already split our views

    Worked (% of the shift): reliability 30 · strategy 25 · data 20 · gm 20 · security 5

**Summary:** I found that tomorrow's release check and the planned host-line test would both draw on the AI allowance our uploads now use, together enough to risk the next morning's title. So the test moves to 10 November. A new test of our own history found no sign that a second daily upload takes views from the first, which supports bet 2's four-a-day plan.

### Toward revenue
- **A little evidence for bet 2's route, no revenue yet.** Watch time is flat at 12 seconds. Bet 2's route to doubling views is four uploads a day, which works only if each video keeps its views when more of ours share the feed. Our own history now says that held between one and two a day. Four a day still waits on bet 1 and your answer on #80.

### Done
- **Reliability (found, fixed in the plan):** since the switch, our daily release check runs on the same AI allowance as the uploads. Tomorrow it re-tests bet 1's release (6–8 requests), because that release changed tonight. Add the host-line test's 6 and the uploads' 4–10, and Google's day could reach 24 requests against the 20 we plan around. Its last upload, the next morning's, would then lose its AI title. So the test now waits for a day the check stays idle: 10 November at the earliest. The first week's check on the new model's daily limit now ignores days we spent from it ourselves. Otherwise our own spending would read as "the new model's allowance is too small" and send us to the model that failed every request it was sent today.
- **Data (corrected):** on #77, the comment you will read when you decide on bet 1 still gave the old model's host lines as about 21 of 27 reacting, a figure scored by eye. It now gives the blind scores, 14 of 21 against the new model's 2 of 12. Editing a comment sends no email.
- **Strategy and data (rule set before any view was read, then built):** do views per upload fall when another upload is near? Nearly every day since April 2025 had two uploads; about 45 had one. So our data can compare one a day with two, never two with four, and only a large effect would show. I wrote the rule down and published it before reading anything. It compares uploads alone against paired within the same month, so old and new eras never meet. Then I built the read with tests. A fresh review found my first wording labelled only 1 of 878 videos as alone, since uploads come 12 hours apart, so I amended the rule, still unread, to compare videos beside a missed slot with the regular rhythm. After a second review found no bugs, I ran it once: videos beside a missed slot got 1.08 times the views of the rest, inside the 17% that chance alone produces, and the same watch time. So there's no sign that a second daily upload takes views from the first. That supports four a day, though it can't rule out a smaller effect, or one at six-hour spacing.
- **General management (ranking):** nothing was ready. A fresh helper, checking against the code and data, proposed the two items above and nothing else above the bar. Dropped: a tool to plan each day's AI requests (tonight's note in the plan covers the one case that matters this week); fixing the reset hour in the sample-video gate (since the switch, renders use a separate allowance from the uploads, so the wrong hour costs nothing); redrafting the three viewer replies (they lapse on 17 November, and nothing posts without your label on #89).
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

## 2026-11-08 (17:56) — We switched to the replacement AI before Google retires ours, so uploads keep their titles past 1 December; it writes weaker host lines for bet 1, and tomorrow's test tries to win them back

    Worked (% of the shift): reliability 40 · product 25 · data 15 · gm 10 · editorial 5 · security 5

**Summary:** Today's model test picked Gemini 3.6 Flash, and it is now live: this evening's upload is the first made with it. That protects every upload's title and safety screen past Google's 1 December change. But the new model's host lines for bet 1 react to the answer about half as often as the old model's, so I have told you on #77 and set up tomorrow's test to try to win them back.

### Toward revenue
- **Protects what we have, does not grow it.** Watch time is flat at 12 seconds. Without the switch, Google would have silently changed the AI writing our titles, closing lines and safety checks on 1 December, in the middle of bet 2's measurement window.
- **A setback for bet 1, found before it ships.** Bet 1 is the company's main bet, and its host lines are now the most valuable thing to improve. Tomorrow's test is the next step.

### Done
- **Reliability (tested, then shipped):** the two-candidate test planned yesterday. Gemini 3.8 Flash didn't answer any of its three requests (twice the server was busy, once it timed out at a minute), which disqualifies it under yesterday's rule. Gemini 3.6 Flash answered all three in about two seconds each. 6 AI requests, from the two candidates' own allowances, not the uploads'.
- **Reliability (shipped):** the switch went live as its own version, so its effect can be measured. All tests pass, two fresh reviews found no bugs yesterday, and its sample video played. It is judged around 25 November on watch time and failed titles, by the rule set before any upload. Bet 1's release now runs on the new model too, and I brought it back in line with the live code, so your label can still ship it in one step.
- **Data (scored blind):** fresh helpers, never told which model wrote what, scored the host lines. 3.6 Flash reacted on 4 of 9 today, under yesterday's bar of 5, so as planned I told you on #77. The figure I gave you there for the old model (about 21 of 27) had been scored by eye. Scored the same blind way, the old model reacted on 14 of 21 and the new one on 2 of 12. So the drop is real; the old model's rate is nearer 2 in 3 than the 4 in 5 I quoted.
- **Product (checked, free):** Groq's best free model, our legal fallback, reacted on 1 of 9 beside 3.6 Flash's 4 of 9. So moving to Groq still isn't the fix.
- **Product (built and planned):** the trial tool can now test the new model at a little more "thinking", which is the cheapest single change to try. Tomorrow's test (6 AI requests) compares that, and a wording that tells it only to react, against today's lines. Each is scored blind, and the rule for what ships was set tonight, before any result: 7 of 9 to go further, then 12 of 18 to ship. A fresh review found no bugs.
- **Data (rule set before any result):** the capitals test and the voice test both run across the switch. Their groups are drawn at random per upload, so the switch hits both groups alike, and they will be read as planned, with no after-the-fact split by model.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas, and two rankers reading them in opposite orders both put the old-model check first; it is done. Dropped: a filter for summary-style lines (it would strip the host from most videos), a new sample video (needs paid narration and another ask of you), a combined request to you (each of these reports already ends with your list in order), and pre-filling the Reddit registration (the ask already names the page and what it needs, and the form would put our app's details in a public issue).
- **Editorial (rule set before the first upload):** we already refuse titles that sell shock ("you won't believe"), and those refusals don't count against the switch's pass mark. So at its 20th upload I will count them: 5 or more of 20 (the old model: 2 of 30) puts a fix to the title instructions in the queue.
- **Reliability (found):** Google's free AI allowance resets at midnight California time. Since the clocks changed on 1 November, that is 08:00 UTC, not the 07:00 our shift rules and sample-video gate assume. AI work in that hour draws on the previous day's allowance, which the uploads already used. The exposure is small: shifts start at 03:17, 11:17 and 19:17. It is logged for a fix; until then, tomorrow's test waits until after 08:00.
- **General management (second round):** a fresh helper, aimed at what can be done today without the AI allowance or you, found the two items above and nothing else above the bar. A Reddit terms re-read waits for their 10 November update; the viewer replies wait on #89; preparing tomorrow's review now would be redone once Monday's figures arrive.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.20 this month, forecast $0.80 of $3).
- **Reliability (checked):** this morning's upload landed. This morning's shift was cut off before it did anything, so today's test fell to this one.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2; now with weaker host lines, see the comment), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **First, tonight's upload:** the first on the new model had not started by 17:55. Check that it landed with a title the new model wrote, and no limit refusal.
- **9 November, after 08:00 UTC and an hour clear of an upload:** stage 1 of the host-line test, under its rule. **The new model's first week:** check each upload's title came from it and none hit its daily limit.
- **9 November weekly**, as listed in yesterday's entry, including whether the switch's videos may count with today's as bet 1's comparison.

### Better?
- **Than last shift:** yes, slightly: uploads are safe past 1 December, and bet 1's weaker host lines are known, measured fairly, and have a test lined up, all before it ships.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
