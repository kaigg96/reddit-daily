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

## 2026-11-01 (10:27) — A failed upload has emailed no one since 11 October, and two clicks of yours fix it; election week's fuller skip is live

    Worked (% of the shift): reliability 30 · editorial 20 · gm 20 · legal 15 · data 10 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Since 11 October a failed upload would have emailed no one, which matters most when the shift allowance runs out around 4 November; #86 asks you for the two clicks that fix it. Election week's skip now also catches questions about polls, live from today.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the uploads and their source.** A failed upload reaches you again once #86 is done. Reddit's terms bar its name from our app's name, so #82 now says to check that before you register.

### Done
- **Reliability (found, for you):** GitHub emails a scheduled job's failures to whoever last changed its schedule. On 11 October our automatic approver applied your four-a-day approval, so the last editor is now a bot, and the upload job has no alert of its own. Nothing has failed since; the last failure, on 5 October, did reach you. Shifts are the only other check, and none runs once the weekly allowance is spent (29–30 October, and again about 4 November). #86 gives the fix: in the Actions tab, disable the upload job and enable it again straight away. A later approved schedule change would repeat it; that is recorded.
- **Editorial (fix, live):** election week's skip now also catches "polls" and "electoral", and logs each post it skips. A fresh review found no fault, and all 707 checks pass. Across 211 past uploads it would skip nothing more than before. Its sample passed; it is live from this evening's upload.
- **Editorial (check):** this morning's upload, on makeup, makes no claim about voting.
- **Legal (for you, no email):** Reddit's developer terms (section 5.3) forbid its name "in the name of your App". We cannot see our app's name, and this project's own name is reddit-daily. #82 now tells you to check the name before you register, and to rename the app if it says "reddit". I edited the issue, so no email.
- **Data (recorded before any read):** bet 2 starts from 8,300 views over four weeks, the lowest of the 11 four-week stretches since July; the middle one is 11,212. So its bar of 16,600 is about one and a half times a typical stretch, not double. It is in the test ledger, so December's read cannot overstate a pass.
- **General management:** nothing was ready. A fresh agent proposed 8 ideas; two rankers, reading them in opposite orders, both put the failure emails first, then the Reddit name check and a read-only key. Dropped: a read-only key for Monday's figures (both jobs can reach every secret, so it closes nothing); what the new country figures would change (at 757 times short, nothing); a plan for bet 1 missing 6 November (the monthly's, after the date); whether long shifts produce less (too big, and your call). One shift's cost row was missing (31 October, 16:05): its run stopped after 18 minutes with no usage figures. That is 1 of the last 60 runs, so the weekly count is one shift short.
- **Reliability, security:** all uploads since the last shift landed. No workflow changed; money controls in place ($0.89 this month, forecast $0.90 of $3).
- AI use: none from the upload allowance; no Polly; one sample render, on the test model's allowance.

### Blocked
- **For you, in order:** #86 (two clicks, about a minute); #77 (one label ships bet 1; bet 2's window closes about 6 November); #82 (register by 12 January; check the app's name first); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Election week:** the full skip is live, so the daily voting check ends; the skip lapses by itself after 10 November.
- **2 November, the weekly; then the November monthly; if #77 is labelled; 7 November:** all as the 31 October (22:29) entry says.
- **Once #86 is done:** close it, and the item in the technical list.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: once #86 is done, a failed upload reaches you again, and your Reddit registration will not use a name Reddit's terms forbid.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

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

