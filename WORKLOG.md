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

## 2026-10-31 (HH:MM) — Your Reddit registration ask pointed at a form that closed today; fixed. Your monthly report now comes after Monday's figures, not the day before

    Worked (% of the shift): gm 50 · legal 20 · security 15 · reliability 10 · market 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Two of your asks were corrected or settled for you, and the monthly report will now read the current month's figures.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the source.** Every upload reads Reddit, and an unregistered app loses access on 12 January. The ask now sends you to the one page that registers existing apps.

### Done
- **Legal (fix):** #82's description listed the questions on Reddit's form for *new* API access as if they were the registration form's, and linked that form. New requests closed today. Reddit's registration page says only "log in to start registration". Corrected by edit, so no email.
- **General management (fix, live):** every plan expected your November monthly report on 5 November. The scheduler would have called it due tomorrow, Sunday, on figures already reviewed on 26 October, a day before Monday's figures and four test reads. It now waits for the month's first weekly review, as October's did: 2 November, after the weekly, or from the 10th if Monday's figures never arrive. A fresh agent's round of ideas found it. A fresh review then found three ways my first version could hide a late review from its alarm, and a test sweeping eight months of dates found two more. All fixed and merged.
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

---

## 2026-10-30 (23:23) — The release check was spending 6 of our uploads' 20 daily AI requests re-checking a release that had not changed; fixed

    Worked (% of the shift): reliability 40 · gm 40 · legal 10 · editorial 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. The daily check of the next release had re-run every afternoon since 25 October on a release that had not changed, using 6 of the 20 free AI requests our uploads share. It now runs only when the release changes, or weekly, as designed.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting what we publish.** Each upload's title, closing line and safety screen draw on that allowance of 20 a day. The check took 6 of them a few hours before each evening upload. Running out cost an upload its title on 20 September. It also matters for four uploads a day: our plan says four fits the allowance, but it never counted this.

### Done
- **Reliability (fix, live):** a fresh agent's round of ideas found it, and the build log confirmed it. The build machine knows the release only by its remote name, so the check could never tell that nothing had changed. Fixed and tested. A fresh review found no defects; its one test gap is closed. Merged 23:12. The release's sample tags now print when it changes or weekly, not daily.
- **General management (fix, live):** the check that catches the plan calling finished work "pending" could never fire, for the same reason and because it looked for old branch names. A fresh review then found that fixing it would have woken a second fault: it read the start of each paragraph, not the words beside the work it names. Both fixed and tested; today it finds nothing stale.
- **Legal (check):** the stock-footage licence bars reselling clips on stock or wallpaper sites and selling unaltered copies. Keeping our five clips in our public project is neither. Recorded beside the credits.
- **Editorial (check):** this evening's upload asked about Patrick Stewart's death. Major outlets confirm he died on 28 October, so we did not spread a false claim.
- **General management:** no shift ran on 29 or 30 October. The weekly shift allowance was spent by the evening of the 28th (228 units over 15 shifts, against a ceiling near 200), so five shifts were skipped. It also tripped a day early the week before (210). Nothing was lost, since everything waits on you. But the breaker meant to catch a runaway shift now sets the weekly pace, as the average shift rose from about 11 units to 15. Recorded for the 5 November review, so this shift stopped once nothing above the bar was left rather than spend a later shift's allowance.
- **General management:** nothing was ready. A fresh agent proposed eight ideas from the data. Two rankers, in opposite orders, put the release check first and the licence second. **Dropped:** counting AI requests per day (the logs do not print them, and the fix removes the uncounted share); logging why a title was refused (bet 1's release rewrites that code, so it is in the technical list for after it); updating our Reddit library (its new version adds nothing for Reddit's API change); a shorter list of dropped ideas, and compressing the findings section (both already proposals for the 5 November review); recording the Claude plan (it changes no decision).
- **Reliability:** all five uploads since the last shift landed. On the 29th one shipped the Reddit question as its title, as designed, after the shock-phrase guard refused the AI's.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, money controls in place ($0.87 this month, forecast $0.90 of $3).
- **Product:** bet 1 is still ready the day you label it: tonight's live code and the release combine with no conflicts, and all 942 checks pass.
- Two fixes live, three checks. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; bet 2's window for it opened today and closes about 6 November); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **Tomorrow's release check (about 13:00–15:00 UTC):** its build log should say it skipped, as already validated. If it ran, read why.
- **2 November snapshot:** as the 28 October (17:44) handover says: refused figures first, then the views rule, the subreddit test, the title-style test and the voice question, each with its fairness check and rule as written. The zero-view guardrail: a second breach is a decision's revisit trigger.
- **If #77 is labelled:** merge the release, then the counting fix, set the live format to v8 in the product plan, and close #77.
- **5 November monthly:** the audit's proposals, plus the weekly shift breaker now setting the pace.
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. Yes for the uploads' margin: 6 of 20 daily AI requests are back.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
