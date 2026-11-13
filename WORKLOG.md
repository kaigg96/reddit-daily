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

## 2026-11-13 (01:00) — The capitals test can no longer be read on too few videos; the security ask now opens with two five-minute checks

    Worked (% of the shift): data 55 · gm 20 · security 20 · reliability 5

**Summary:** The shift started with nothing ready. It made sure our one live test of a views lever, capitals in titles, is read only once both halves hold the 30 videos its rule needs. It also cut the start of the security ask that guards our one fatal risk down to two five-minute checks. Nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. The capitals test is our only live test of a views lever, the measure bet 2 is judged on, and its verdict decides whether every title gets a capitalised word. Tonight's fix keeps that verdict from being taken on too few videos.

### Done
- **Data (fixed, live):** the capitals test's rule says it is read at 30 videos per half. The lock that stops anyone peeking opened on its date, 23 November, whatever the halves held, and the capitals half was on course to fall one or two short. The lock now stays shut until both halves hold 30 in the exact set of videos the read uses. It counts only which half each video was in, never how it did. On today's numbers the read most likely still happens on 23 November; there is about a 1-in-5 chance it moves to 30 November. I wrote that into the plan before anyone looked at a result. Three fresh reviews checked it. The first two each found I had counted the read's videos wrongly, and I fixed both before merging. All 864 tests pass.
- **Security (an existing ask made easier, not a new one):** the quarterly account check (#59) is the only guard on our one fatal risk: losing the Google account, and with it the channel. It has waited on you since 6 October. It now opens with the two checks that matter most, about five minutes together: 2-step sign-in on the Google account, and the list of apps connected to it. The other four follow, unchanged. I edited the issue rather than commenting, so it sent you no email.
- **General management (ranking):** a fresh helper proposed eight ideas from our data and plans, and two others ranked them, forwards and reversed. The capitals-test fix came in the top two both ways, so I did it first. The security rewrite split them (first and fourth), so I did it second. Dropped: a tool to read the new AI model's titles from the run logs (shifts can't read those logs); whether the new model lets through more questions about named people's misconduct (about 10 uploads, too few to tell); titling the backup show with our own question (it needs a sample video and a product choice); fixing in advance how the 20 November bet-2 update is worked out (its rule already says, and one command gives the figure); a test run before each push (it needs files only you can change); and sorting the friction log (Monday's review does it).
- **Data (a figure, not a finding):** views over the last four weeks were 12,238, against 9,158 over the four before. That is ×1.34, under the doubling our report counts as a change, and it comes mostly from one strong week. At this pace, two uploads a day reach about three-quarters of bet 2's 16,600 bar.
- **Security and reliability (checked):** both of yesterday's uploads landed. The money controls are intact ($0.31 this month, forecast $0.79 of $3). No secret is in the repository, and the workflows are unchanged.
- **General management:** my rule took the product plan's status section 49 words over its limit, so I shortened it back under. The open code-findings list is still one over its cap, as it was at the start. Neither item that could close is ready to, and I added none.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (now five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **This morning's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled (yesterday morning's plan stands). In winter, Gemini work waits until after 08:00 UTC.
- **16 November:** the weekly review; it sorts the friction log's 26 ungrouped entries.
- **23 November:** the capitals test's read, if the lock opens. If it stays shut, move the test's due date to 30 November and read it then.

### Better?
- **Than last shift:** no, not toward revenue. A verdict on a views lever can no longer be read too early, and the fatal-risk ask costs you less. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-12 (19:28) — No theme in the questions explains why some uploads get buried; every scheduled job here runs as late as the uploads

    Worked (% of the shift): data 40 · gm 25 · reliability 15 · strategy 10 · security 5 · product 5

**Summary:** The shift started with nothing ready. It ranked eight new ideas, answered two questions from our own data, and gave the backup show's title check a fixed test. None of it changes what we ship, and nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. Tonight ruled out one suspect for the rise in buried uploads. It also showed that a fix for late-running jobs, which four uploads a day needs, has to come from outside GitHub's schedule.

### Done
- **Data (a question answered: no):** one in seven of the last three weeks' uploads is barely shown (5 views or fewer after a week), up from one in forty. I set the rule before looking. A fresh helper then tagged all 130 uploads since September against YouTube's advertiser-sensitive themes (sex, swearing, violence, politics and so on), without seeing their views. Tagged uploads were buried slightly *less* often than the rest (7 of 42 against 18 of 88), and no single theme came near the bar. So the questions' content doesn't explain it. Earlier checks ruled out pipeline faults and subreddit, and the cause is still unknown. The check is saved, so anyone can rerun it.
- **Data (dropped, my mistake):** I asked whether the fall in plays that get past the opening (43 to 34 in 100) is YouTube's doing, by reading old videos' new views. Old videos earn about 3 views a day, which our findings already said, so the test could never clear its floor (73 new views against 300). I recorded the slip and kept the code out of the live repository.
- **Reliability (a finding):** I measured each scheduled job's real start against its scheduled time over six weeks. Shifts, the morning release check and Monday's figures job all run 4–9 hours late, and all of them later since late October, just like the uploads. So the cause is GitHub's scheduler, not our upload job. Moving the upload times won't help; only a trigger from outside GitHub would, and that needs a token from you. That matters only once four a day is on the table.
- **Strategy (built, merged, switched off):** the backup show must not credit Reddit or real people in its titles. The check that stops this has been rewritten three times, and each fresh review found new wordings it got wrong. It now has a fixed set of 17 example titles that any replacement check must get right. Today's check gets 10 of them wrong, and the set says which. So when the different kind of check is built before the show goes on, it can be graded in seconds, with no AI requests.
- **General management (fixed):** the limit on open code findings was counting 12 old records of finished cleanups as open, so it read 26 of 25 when 14 were open. The easy way back under was deleting history. It now counts only the open list, and the limit dropped by the same 12, so it still asks for one finding to be closed.
- **General management (tidied):** I shortened four old, closed findings in the product's findings record by about 1,180 words. Their standing rules stayed, word for word, and the full text stays in history. The record's word limit dropped to match, so it can't grow back.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both orders put the same two first. Dropped: making the voice-only test the next release if #77 waits (that release needs you to sample the real voice, and it would push back bet 1); tightening the check on approval references (only you can land that guard, and a patch now would add to your queue before the 7 December bundle); and the case for more frequent sample videos (it is due at the 7 December review). With those three left, nothing else cleared the bar, so I handed over at 19:37, 18 minutes early.
- **Security and reliability (checked):** this morning's upload landed, and tonight's has not run yet. The money controls are intact ($0.31 this month, forecast $0.79 of $3). No secret is in the repository, and the workflows are unchanged. The AI model's overload errors touched 1 of 24 uploads this month, against 7 of 61 in October, so they are not rising.
- **Your approvals #88 and #65 are still open.** #88 waits on you applying its patch, because shifts cannot write those files. #65 waits on your "yes" to its corrected sentence.
- AI use: none on uploads; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **Tomorrow's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled (the morning shift's plan stands).
- **Buried uploads:** what's left to test is YouTube's side, through the weekly figures. The 16 November snapshot reads the four newest.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** no. Two questions answered, both "no", and nothing reached viewers. The backup show is a little closer to switch-on.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
