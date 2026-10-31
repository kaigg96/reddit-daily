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

## 2026-10-31 (22:29) — Election week is covered, your security checklist can no longer cut off our uploader, and we will start learning who watches

    Worked (% of the shift): audience 20 · editorial 15 · market 15 · gm 15 · reliability 10 · security 10 · product 5 · strategy 5 · data 5

**Summary:** The format viewers see is unchanged and nothing moved revenue directly; bet 1 still waits on #77. Shows built on their own questions get paid at scale, which matters for November's choice of a source after Reddit; through election week we skip questions about voting, and following the security checklist can no longer stop our uploads.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Evidence for the source after Reddit.** Of 15 quiz and would-you-rather Shorts channels, 6 show the members button only Partner Program channels get, including 5 of the 7 with over 300,000 subscribers. Among Reddit-reading channels it was 11 of about 185. Their questions are their own, so neither YouTube's reused-content rule nor Reddit's terms reach them. Whether they use a voice cannot be seen from outside.

### Done
- **Security (fix):** check 3 on #59 told you to remove any connected app you do not recognise. It did not say that our uploader is one of them, or that Google labels it unverified. Removing it would stop every upload and Monday's figures until you made a new login on your own machine. The check now says to keep it. Corrected by edit, so no email.
- **Audience (bet, built):** each Monday's figures will add two things we have never had: the share of views from subscribers (the nearest YouTube offers to returning viewers) and the top five countries. Country matters because YouTube shares ad money by country. Live from Monday's run: each sits behind its own guard, so a refusal blanks only its column and can never cost the main figures. A fresh review found no fault; its small notes are fixed. A second change, also reviewed, tests the one guard that matters most: a problem with this file can no longer end Monday's job before the main figures are saved.
- **Audience (answered):** in the last two weeks viewers left 8 comments: 7 on one politics question, reacting to the topic, and 1 answering the closing vote. So the vote draws almost nothing. That changes no decision: bet 1 is judged on watch time.
- **Editorial (fix, live):** the US midterms are on 3 November. Until 10 November a question about voting or the election is not picked, since we read answers word for word and YouTube removes false claims about how or when to vote. Reviewed, and a sample video passed. One gap the review found is fixed on a branch for the next shift (below).
- **Editorial (check):** this evening's upload asked where "$1.8 trillion wiped out" went. Reuters and NBC report the 30 October sell-off, so the premise is true.
- **Strategy (answered):** no reliable figure exists for how often small channels reach the Partner Program bar. Published ones disagree a hundredfold, and the most specific describes channels unlike ours (we have over 1,000 videos and 22 subscribers). Nothing changes.
- **Data (answered):** since January YouTube's bulk reports count thumbnail impressions. The Shorts feed, which brings 97% of our views, shows no thumbnails, so they would miss our reach. No change.
- **Product, reliability, security:** bet 1 still merges cleanly with today's live code. The election skip first clashed with it in one file; I combined the two, and all 959 checks pass. So tomorrow morning's release check re-tests bet 1, as it does after any change. Both of today's uploads landed. No workflow changed; money controls in place ($0.89 this month, forecast $0.90 of $3). Sunday's US clock change moves Google's AI-allowance reset to 08:00 UTC; nothing we run depends on that hour.
- **General management:** nothing was ready. Two fresh agents proposed 14 ideas; two rankers, reading them in opposite orders, put the paid-channels count first and the audience figures third. Dropped: holding back shift time for bet 1's merge (your call at the monthly, which already leads with the shift cap); closing #80 for you (it is yours to decide); building four a day before bet 1 (#80 says wait); a forum search for a reach drop (it invites explaining away Monday's read); pricing sponsorship (Reddit's terms bar it on today's videos, and we are below every minimum); a sample that plays in one tap (GitHub serves a video as a download); the music track's credit terms (checking needs your login, and nothing changes in two weeks). A third round, on the functions the first two missed, found the midterms. I handed over at 23:12, 17 minutes early: the election fix's second half merges cleanly and waits only on the one sample render a shift may request, and nothing else cleared the bar. You have been away since 27 October, so nothing is re-asked.
- AI use: none from the upload allowance; no Polly; one sample render, on the test model's allowance.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; bet 2's window closes about 6 November); #82 (register at Reddit's registration page by 12 January); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks; check 3 now says what to keep).

### Next
- **First, before 3 November (the US midterms):** the skip of questions about voting through 10 November is built and reviewed. YouTube removes content that misleads voters on "the time, place, means, or eligibility requirements for voting". A first violation is a warning, and a second within 90 days counts against the channel. We read answers word for word, jokes included, and 7 of October's 61 uploads were political. It would have skipped 1 of 210 past uploads. It is live from tonight's runs. The review found it misses "polls" and "electoral"; that fix, with a log line for each skipped post, is on its own branch and needs one sample render before it merges. That is the next shift's first job. Until the full version is live, each shift checks that day's uploads for voting claims and raises any it finds with you.
- **2 November, the weekly:** first check that Monday's figures name nothing YouTube refused, and read each test's warnings before its verdict. Then the views rule, the subreddit test, the title-style test and the voice question (its fairness check is done), each applied as written and recorded in the test ledger. The scorecard reads at 4–10 days; a second breach of the buried-uploads alarm is a decision's revisit trigger. If Monday's figures do not arrive, re-run the Monday job that day. Then check that the channel row carries the two new figures; blank means YouTube refused them for a channel this small.
- **Then the November monthly:** lead with the shift cap (it trips about 4 November), then the audit's proposals in the technical list and the bundle carried from 25 October. Put today's paid-channels finding beside the own-questions sample.
- **If #77 is labelled:** merge the release, then the counting fix, set the live format to v8 in the product plan, and close #77.
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. A little for the source decision (outside evidence where we had none) and for safety (election week is covered, and your checklist can no longer stop uploads).
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

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
