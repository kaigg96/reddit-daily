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

## 2026-10-31 (16:30) — The buried-uploads alarm due to reopen a decision on Monday was half two readings taken too young; every upload is now read at the same age

    Worked (% of the shift): data 50 · gm 25 · market 10 · audience 5 · reliability 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Monday's review would have reopened how we judge results on an alarm that rested half on two uploads read at three days old, younger than anything they were compared with. The scorecard now reads every upload at the same age. That was set before Monday's figures exist.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Keeping Monday's decisions honest.** Monday's review reads four tests and the alarm on buried uploads. Each read now counts what its rule says it counts, so a keep or a drop rests on real differences.

### Done
- **Data (fix, live):** the scorecard compares the last three weeks of uploads with the three before, each read about a week old. It also accepted readings at three days, which only the newest week ever has. Two of its four recent zero-view uploads were such readings, both from 22 October. Without them the share is 6.1% against 4.8%, inside the alarm's 3-point margin, not 11.4%. Uploads with views already show their full count at three days, so only the zero count moves. Monday's figures re-read both at ten days, so whether they were buried is Monday's to say. A fresh agent's round of ideas pointed here. My first explanation, that YouTube's figures arrive late, was wrong, and my own check showed it. A fresh review confirmed the rest, corrected one number, and found week labels that would have sorted 1–3 January after the rest of 2027. All fixed.
- **Data (Monday's prep):** the voice test's fairness check reads only who got which voice, so its answer is already fixed: within chance (p 0.19). Its rule stands as written; recorded in the test ledger.
- **Market (answered, changes no decision):** the weekly view swings come from the Shorts feed. It alternated high and low for eight weeks (363 to 2,902 views) while search held at 26–66. A delay in YouTube's figures would have shrunk both alike. The test set for 16 November still decides.
- **Audience (answered):** our 24 subscribers came one each from 23 uploads over 18 months. No topic or upload drew them, so there is nothing to copy.
- **General management (fix, live):** the list of ideas past shifts dropped counted this morning's draft handover as a separate shift, so it showed nine shifts, not ten. Fixed and reviewed.
- **Reliability, security:** all uploads since the last shift landed. This afternoon's release check skipped in 8 seconds, so yesterday's fix works. No workflow changed; money controls in place ($0.89 this month, forecast $0.90 of $3). #65 still needs your "yes" to the corrected sentence: your label predates the correction.
- AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; bet 2's window closes about 6 November); #82 (register at Reddit's registration page by 12 January); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **2 November, the weekly:** as the 10:15 entry says, refused figures first, then each test with its rule as written. The scorecard now reads at 4–10 days. If the alarm on buried uploads breaches on that read, D9's trigger fires as written. The voice test's fairness check is done. The comparison tool takes readings from 3.5 days, so each test's read includes 29 October's morning upload at about 3.75 days. That is one in about 40 uploads, and harmless unless that upload is the only zero in an arm.
- **Then the November monthly**, **if #77 is labelled**, and **7 November** — as the 10:15 entry says.

### Better?
- **Than last shift:** No for viewers or revenue. A little for decisions: Monday's alarm read is no longer tilted by readings only one side could have.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-31 (10:15) — Your Reddit registration ask pointed at a form that closed today; fixed. Your monthly report now comes after Monday's figures, not the day before

    Worked (% of the shift): gm 50 · legal 20 · security 15 · reliability 10 · market 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Two of your asks were corrected or settled for you, and the monthly report will now read the current month's figures.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the source.** Every upload reads Reddit, and an unregistered app loses access on 12 January. The ask now sends you to the one page that registers existing apps.

### Done
- **Legal (fix):** #82's description listed the questions on Reddit's form for *new* API access as if they were the registration form's, and linked that form. New requests closed today. Reddit's registration page says only "log in to start registration". Corrected by edit, so no email.
- **General management (fix, live):** every plan expected your November monthly report on 5 November. The scheduler would have called it due tomorrow, Sunday, on figures already reviewed on 26 October, a day before Monday's figures and four test reads. It now waits for the month's first weekly review, as October's did: 2 November, after the weekly, or from the 10th if Monday's figures never arrive. A fresh agent's round of ideas found it. A fresh review then found three ways my first version could hide a late review from its alarm, and a test sweeping eight months of dates found two more. All fixed and merged. It also now prints when each review next comes due, worked out by the same rule, so a plan quotes a date rather than guessing one.
- **General management (for you, at that review):** the weekly cap on shift usage pays for about 560 shift-minutes, but 21 one-hour shifts are scheduled, and the early-ending alarm asks for all of them. Both cannot hold: full shifts mean about nine a week, then two or three dark days. At this week's pace the cap trips around 4 November, inside bet 1's window. The cap or the schedule is your choice; the review will recommend one.
- **Security (done for you):** the Gemini key is restricted. One free request from it to YouTube's API was refused by the key's own list of allowed APIs. #59 now has six checks.
- **General management:** #50 closed as superseded. Since 27 October a shift lands a rule change you have labelled itself, as #84 and #85 did, which is what it asked for. The 19 October digest is closed too; the 26 October one replaces it.
- **Product:** bet 1 is still ready the day you label it: today's live code, the release and the counting fix combine cleanly, and all 949 checks pass.
- **Reliability, security, market:** all five uploads since the last shift landed. No workflow changed, money controls in place ($0.88 this month, forecast $0.90 of $3). No news on Reddit's API dates or YouTube's rules since 27 October. A major update of a sign-in library came out this morning; uploads pin the old version and Monday's figures job does not use it.
- **General management:** nothing was ready. A fresh agent read the last 40 build runs, the upload log, the technical list and the risks; beyond the two items above, nothing cleared the bar. **Dropped:** a pacing line for the shift cap (it would turn a breaker into a budget, your call); repeated background clips (chance); a lower-case closing line (bet 1's release fixes it); GitHub's warning on old build steps (they already run on the new version).
- AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; bet 2's window closes about 6 November); #82 (register at Reddit's registration page by 12 January); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1 until you answer); #59 (six account checks).

### Next
- **This afternoon's release check (about 13:00–15:00 UTC):** its build log should say it skipped.
- **2 November, the weekly:** first check that Monday's check-in names no figure YouTube refused, and read each test's warnings before its verdict. Then the views rule, the subreddit test, the title-style test and the voice question. Before the voice read, run the fairness check its rule names, counting only the uploads that read will see. Apply each rule as written; record each read in the ledger. The zero-view guardrail: a second breach is a decision's revisit trigger.
- **If Monday's figures do not arrive,** re-run the Monday job that day: the monthly now waits for them, until the 10th.
- **Then the November monthly:** lead with the shift cap (it trips about 4 November), then the audit's proposals in the technical list and the bundle carried from 25 October. A labelled bundle lands by a shift's commit.
- **If #77 is labelled:** merge the release, then the counting fix, set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how).
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. A little for the source and for your monthly report: the registration ask can no longer send you to a closed form, and the report will read November's figures.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
