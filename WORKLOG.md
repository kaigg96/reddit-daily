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

## 2026-11-08 (17:35) — We switched to the replacement AI before Google retires ours, so uploads keep their titles past 1 December; it writes weaker host lines for bet 1, and tomorrow's test tries to win them back

    Worked (% of the shift): reliability 40 · product 25 · data 15 · gm 15 · security 5

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
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.20 this month, forecast $0.80 of $3).
- **Reliability (checked):** this morning's upload landed. This morning's shift was cut off before it did anything, so today's test fell to this one.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2; now with weaker host lines, see the comment), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **9 November, after 07:00 and an hour clear of an upload:** stage 1 of the host-line test, under its rule. **The new model's first week:** check each upload's title came from it and none hit its daily limit.
- **9 November weekly**, as listed in yesterday's entry, including whether the switch's videos may count with today's as bet 1's comparison.

### Better?
- **Than last shift:** yes, slightly: uploads are safe past 1 December, and bet 1's weaker host lines are known, measured fairly, and have a test lined up, all before it ships.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-07 (23:07) — Nothing was ready and two rounds of ideas found nothing worth doing tonight; one flawed title is now set aside before the capitals test is read

    Worked (% of the shift): gm 45 · editorial 20 · data 10 · reliability 10 · security 10 · product 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: what would move it still waits on your label on bet 1 (#77) or on tomorrow's model trial. Reading our published titles found one flaw that the capitals test's read would have missed. It is now excluded, by a rule set before any result.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds. Every change to what we ship waits on bet 1, on the capitals test running to 23 November, or on tomorrow's AI allowance.

### Done
- **Editorial (read, found):** I read every title, closing line and narrated answer of the last nine uploads. One title from 5 November came out in lower case where Reddit had capitals: "Why doesn't batman just end the joker? your theories." Our 14 October fix only catches titles with no capital at all. It is 1 of about 29 titles in the test's no-capitals half since that fix, and none in the other half, so it slightly favours capitals. It joins the 11 uploads that test is already re-read without, decided from the text alone. No fix while the test runs.
- **General management (ranking):** nothing was ready. A fresh helper proposed seven ideas, and two rankers reading them in opposite orders agreed on none worth doing tonight:
  - a rule for the topic-picking experiment (its deadline was false: the experiment is switched off, so no results accumulate; the plan now says so)
  - a measure of how alike our videos are (it would only repeat what #80 already tells you: one music track on all 20 recent uploads, while clips and voices vary)
  - building the replacement question source early (it can't finish tonight, and it gets ahead of your choice in #90)
  - moving one logging change ahead of bet 1 (no sample video is possible before 05:15, and it would conflict with bet 1's release)
  - researching music (the source is already your Audio Library task) and studying quiz channels (it shapes a build that waits on #90)
- A second round, aimed only at what we ship or earn, checked each idea against the code and data first. None cleared the bar. No background clip meets the rule for retiring one. The title retry and the guard against repeat questions already exist. A subscribe ask would change the spoken closing line, and subscribers are not what holds us back; views are. Everything else waits on bet 1, the capitals test or you. So I handed over at 23:07 with nothing ready.
- **Reliability (checked):** both of today's uploads landed and nothing has failed. The model switch still combines cleanly with today's code, and all 790 tests pass. GitHub deletes three sample downloads your open asks link over the next two days, but permanent copies were made on 3 November.
- **Product (checked):** the safety screen acted on 3 of 17 posts this week, under its 15% bar, and both skips look right.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.18 this month, forecast $0.76 of $3).
- All of this was checks and one recorded flaw. None changes what we ship.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- Unchanged from the last shift: **8 November, after 07:00 and an hour clear of an upload,** the two-candidate host-line trial and its rule, shipping the switch that day if 3.6 Flash wins. **9 November weekly**, and the later dates, as listed there.

### Better?
- **Than last shift:** no. One flaw that would have tilted a test's read is set aside, which is small.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
