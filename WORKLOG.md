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

## 2026-11-02 (21:40) — Weekly review: watch time shows no link to views, Stephen's voice keeps more viewers past the opening, and bet 1's ask now carries its 6 November date

    Worked (% of the shift): data 55 · gm 15 · strategy 10 · reliability 10 · audience 5 · security 5

**Summary:** The weekly review read four tests by their written rules. The one that matters most for revenue: how long people watch shows no link to how many views a video gets, so watch-time gains stop counting as reach, and the November monthly brings you that choice.

### Toward revenue
- **Nothing viewers see changed.** Bet 1 still waits on #77, and the channel is flat at 12 seconds watched per view.
- **Bet 1's date is now on its ask.** Bet 2 is judged from 30 November to 27 December. Four uploads a day can start only after bet 1's own test, 24 to 31 days from its merge. So bet 1 needs your label by about 6 November to cover all four of bet 2's weeks, and each week later loses one. #77, where you decide, now says so.
- **What tests are judged on.** Every test is judged on watch time, because in August longer-watched videos got more views. On today's 38 recent uploads there is no such link, so a watch-time gain no longer counts as reach. Bet 1's case rests on originality, which gates every route to income.
- **A voice lead.** Plays of Stephen's uploads get past the opening more often than Danielle's: 46% against 31% at the median, beyond chance, and it holds within one subreddit alone. Only those plays count toward the Partner Program, but that lead raises the count only if his uploads hold their views, which this size cannot check yet. It is queued as a test after bet 1 (one change at a time). A voice change needs a sample in the real voice, which only you can make.

### Done
- **Data (weekly review):**
  - Watch time and views: no link (above).
  - Voice: Stephen leads (above).
  - Subreddits: NoStupidQuestions is watched 35% longer than AskReddit, so both stay. Fewer of its plays get past the opening (33% against 45%). That is recorded for the four-a-day test. Its views trail by about half, but views are too noisy to tell at this size.
  - Titles that address "you" are not measurably worse than the others, so they stay at four in six.
  - Last week's low in views was ordinary weather, as predicted. No background clip needs retiring.
  - A fresh review agreed with every number and verdict, and caught six places where I had worded a result too strongly; all are fixed.
- **Data (built, live):** the reach checks now print a range beside their verdict. That shows whether "no link" means ruled out or just not seen, and it never changes a verdict. A fresh review's three small points are fixed.
- **General management (fix, live):** the review nearly missed one of the five reads due today. The check that says a review is due now also lists those reads. Replayed on this morning's records, it names all five. A fresh review's two small points are fixed.
- **Data (for the monthly):** what tests could be judged on instead. Our tests can detect a change of 20 to 30% in watch time or in the share of plays that get past the opening; a test could see the Partner Program's count itself only if it roughly doubled. That share is the useful one: the count is views times the share, and we found no link between the share and views, so raising the share should raise the count as long as views hold. One option for you at the monthly: judge tests on that share, keep watch time as the check that viewers are not worse off, and judge views on the whole channel over weeks, as bet 2 does.
- **Audience (reopened):** viewers commented on 4 uploads this week (7 comments), against 1 upload in each of the two weeks before. Our rule reopens the reply plan at 3 or more. Under your publishing policy, shifts draft replies and a separate job posts them. Our existing YouTube permission already covers replies; posting needs one workflow change from you, sent once the rest is built.
- **Data (rule, before any data):** the capitals test, read about 23 November, will also show its result within each subreddit, since subreddit moves both things it measures. This cannot change that test's verdict.
- **Watch:** five uploads since 15 October had no views at a week old, against three in the six weeks before. They share no topic. Two used a background clip we have since retired. It is the third time since 9 October that this check has tripped, and our rule on how tests are judged named today's reading as the point to revisit the check itself. So the monthly takes that up too.
- **Reliability:** all 15 uploads from last Monday to this morning landed; one had a fallback title (29 October). The safety screen skipped no post; it removed two answers from one. Tonight's evening upload had not started by 21:40, because every scheduled job ran 8 to 10 hours late today. The check that would email you about a missed upload is built but not yet switched on (its change goes in the monthly's bundle). Until then, the next shift's own check catches a miss.
- **Security:** no workflow change since 20 October, no secret in the repository, money controls in place ($0.01 this month, forecast $0.76 of $3); library warnings unchanged.
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (one label ships bet 1, by about 6 November for bet 2); #82 (register by 12 January); #86 (very likely not needed: close it); #65 (it still waits for your "yes" to the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **The November monthly review is due now** and is the next shift's first work. It brings you three things: the 14 December source date, the income read, and what tests should be judged on (watch time's missing link to views, and the zero-view check that keeps tripping).
- Check that tonight's evening upload landed. It may land after midnight and still count as today's.
- After the monthly: the reply plan, now the only ready item. Next Monday: re-read the no-view uploads by subreddit and by background, as set tonight.

### Better?
- **Than last shift:** a little. Bet 1's ask now shows its deadline, and we know watch time is not the lever for views, which sharpens what the monthly asks you.
- **Than ~10 shifts ago:** no for viewers. Watch time is flat at 12 seconds; first-week views over four weeks are up a third, inside normal swings; bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-02 (11:06) — Two answers for the November monthly's source decision: a 14 December date to switch if Reddit access is not confirmed, and why no source brings income yet

    Worked (% of the shift): gm 35 · strategy 20 · monetization 20 · data 10 · legal 5 · reliability 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. The monthly's source decision now has a dated fallback and a priced answer on income. Today's figures had not arrived by 11:50, so the weekly review passes to the next shift.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Keeping uploads alive past 12 January.** If our Reddit app is not registered by then, uploads stop that day. Your labels on GitHub come quickly (41 since September; the slowest took 4 days). Asks that need work outside GitHub take longer: the account checks have waited 27 days, and the registration 12 days so far. A replacement source also needs time to build. So the monthly will propose a date. If the registration is not confirmed by 14 December, shifts build the chosen replacement and merge it switched off. One label from you before 11 January then turns it on.
- **What a new source earns: nothing yet, at any source.** I read YouTube's own pages today. Both of its brand-deal programmes need the Partner Program, which we are about 227 times short of. Outside sponsors start at around 1,000 subscribers, and we have 22. Shop links cannot be clicked in a Short. So the source decision is about two things. First, whether uploads continue. Second, whether earning is allowed at all: Reddit's terms bar it, while the alternatives allow it. Originality gates every route, so bet 1 stays first whatever the source.

### Done
- **Strategy (proposal, for the monthly):** the 14 December date above, with its reasoning, is in the product plan's findings beside the two replacement samples.
- **Monetization (answered):** the income read above. A sponsor's fee counts as revenue from Reddit's data on a plain reading of its terms.
- **Data (answered):** among viewers who get past the opening, half leave between a quarter and half way through, during the first answer or two. Each later quarter loses under a fifth. This is the baseline bet 1's "where do viewers leave" read compares against.
- **General management (fix):** sorted the week's 40 unsorted friction notes into groups, ahead of the weekly review. The largest group, 10 notes, is about sample videos holding finished work. On Sunday a shift timed a sample 12 hours later than it could have run, and only the next shift noticed. I built a command that tells a shift when the next sample will be accepted. It passed a fresh review, its four points are fixed, and it is merged. Two groups are closed as "won't fix", with reasons. First drafts that only a fresh review catches are the review doing its job.
- **General management (ranking):** nothing was ready. A fresh agent proposed 8 ideas and I added one. Two rankers, reading in opposite orders, both put the 14 December date first and the income read second. A second round, aimed at audience, distribution, editorial, finance, market and product, found nothing that clears the bar: everything that changes what we ship waits on bet 1 or would disturb the running tests. Dropped: Reddit's brand rules on our channel name (their site cannot be read from here); recording each post's Reddit score (Reddit has about ten weeks left); a weekly count of similar channels' views; a shares report; a check on the capitals test's precision (it would change a rule mid-test). Also dropped: Gemini's daily reset moved to 08:00 UTC with the clock change, an hour after our rules assume. No shift or scheduled render starts in that hour, as decided on 1 November.
- **Reliability, security:** all 15 uploads since last Monday landed, one with a fallback title (29 October). No workflow has changed since 20 October, and no secret is in the repository. The money controls are in place ($0.01 so far this month, forecast $0.76 of $3). Library advisories are unchanged in kind: Pillow and oauthlib, already in the technical list.
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #82 (register by 12 January; the monthly proposes 14 December as the date to start building a replacement); #86 (very likely not needed: close it); #65 (it still waits for your "yes" to the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Weekly review, once today's figures land** (they have arrived between 11:30 and 13:50 on recent Mondays). Read the watch-time question, the voice test and the subreddit test once each, by their written rules. The friction notes are already sorted, and the voice test's balance check passes (as on 31 October). Watch the 22–23 October uploads: three of four uploads that young had no views on the last snapshot.
- **Then the November monthly.** Its source proposal now carries the 14 December date and the income read.

### Better?
- **Than last shift:** A little, for the company rather than for viewers. The monthly's source decision now has a date and an income answer, so you can settle it in one sitting.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
