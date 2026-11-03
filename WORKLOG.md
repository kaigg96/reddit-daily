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

## 2026-11-03 — Monthly review: no route to revenue is in reach yet; bet 1 still decides the month, and five new asks each need one label

    Worked (% of the shift): gm 25 · strategy 20 · legal 10 · market 10 · data 10 · reliability 10 · finance 5 · monetization 5 · audience 5

**Summary:** For viewers and revenue we are no closer than a month ago: bet 1 has not shipped, and watch time is flat at 12 seconds a view. The next month turns on your label for a revised bet 1 (#77), ideally by 6 November, and on the Reddit registration (#82) before the 14 December date proposed below.

### Where we stand
- **Revenue $0.** About 14,500 plays a quarter get past the opening. The Partner Program needs 10 million (691 times short; a month ago, 757), and 20 million for new applicants from February. We have 23 of the 1,000 subscribers it needs. The nearest route, the 500-subscriber tier, is 207 times short.
- **Can the current path reach the goal? Not at today's size, plainly.** Every route needs the format to be ours first (bet 1), then far more views per video: even six uploads a day leaves every YouTube route about 70 times short. What would make it known: bet 1's first 20 uploads, then bet 2's four weeks from 30 November.
- **One warning is real, not noise.** Uploads with no views at a week old rose from 1 in 41 to 6 in 34. It has fired on 3 of the last 5 weekly reads, and held at matched ages. Next Monday's read checks whether one subreddit is being hidden.
- **Every function now has work behind it.** Audience (the reply job), monetization (the income read) and market intelligence (studies of paid channels) moved off "none".

### Money
- Speech has cost $0.05 so far this month, forecast $0.70 of the $3 budget. Every control at Amazon is intact. Priced this month: four uploads a day at about $1.80 a month. Nothing new spent.

### Risks
- **Ratings unchanged.** YouTube's rules and Reddit's terms, read first-hand today, say what they said a month ago: a reading cannot earn, Reddit bars earning from its data, and unregistered apps lose access on 12 January.
- **A line we had not recorded:** YouTube's spam policy, which can end a channel, bars "re-posting material from other websites… without adding anything of your own". Bet 1's host reactions already answer it.
- **New: shifts went dark for two days.** When the weekly usage allowance runs out, shifts are skipped until Friday, three weeks running: six in a row on 28–30 October, with nothing checking uploads or money. Ask 4 answers it.

### Market and policy
- **Policy pages:** no change to YouTube's eligibility, monetization, Shorts or spam pages, or to Reddit's terms (last revised March and July). Reddit's registration page confirms 12 January; its builder-policy page refused us. No new asset needs a licence check.
- **Comparable channels:** a 246,000-subscriber Reddit-stories channel with hired human voices was reportedly demonetised in May, while channels whose host gives an opinion stay paid (secondary source). So a voice alone does not make a reading original; the host's view does. It supports bet 1.
- **New on YouTube:** Shorts can be grouped into a series (YouTube's blog, 27 October). A free test after bet 1: one recurring show, read on views per upload.
- **Reddit** reportedly updates on 10 November; a shift reads it against 14 December.
- Discarded: three platform changes that bring no route nearer.

### Proposals for you
Five new asks, each recommended, none costing money:
1. **A replacement source, with a date.** If Reddit hasn't confirmed our app by 14 December, build our own questions as the source, merged switched off; one label turns it on. You can approve the date alone and choose after hearing narrated renders, which only you can make. Both allow earning, unlike Reddit. Ours are not a reading and never run out; Stack Exchange keeps real answers but needs niche sites.
2. **What tests are judged on.** For new tests, the share of plays that get past the opening, with watch time as the check that viewers aren't worse off. Watch time shows no link to views; the Partner Program's count is views times that share. Rules already set stay.
3. **Two finished jobs: replies to viewers, and an email to you when an upload is missed.** One label applies both and posts the three queued replies that evening, so please read them first.
4. **Two shifts a day instead of three**, so the allowance stops leaving whole days without one.
5. **Three stale lines in the shift instructions**, fixed to match the tools.

Still waiting, in order: #77 (bet 1, by about 6 November), #82 (register by 12 January), #86 (closes if ask 3 lands), #65 (your "yes" to the corrected sentence), #80, #59.

### Next month
- Bet 1 (#77) decides the month: nothing viewers see changes until it ships.
- **9 November:** the zero-view re-read by subreddit. **16 November:** are weekly view swings viewers or data. **About 23 November:** the capitals test. **24 November:** the friction log's first verdict. **30 November:** bet 2's four weeks begin.
- Carried, not done today: shortening the product plan's findings and a word cap per work-log entry.

### Better?
- **Than last shift:** a little: the source decision and the test measure are now with you.
- **Than ~10 shifts ago:** no for viewers. Watch time is flat at 12 seconds, bet 1 has not shipped, and the distance to the Partner Program moved only within normal swings.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-02 (21:40) — Weekly review: watch time shows no link to views, Stephen's voice keeps more viewers past the opening, and bet 1's ask now carries its 6 November date

    Worked (% of the shift): data 45 · audience 15 · gm 15 · strategy 10 · reliability 10 · security 5

**Summary:** The weekly review read four tests by their written rules. The one that matters most for revenue: how long people watch shows no link to how many views a video gets, so watch-time gains stop counting as reach, and the November monthly brings you that choice.

### Toward revenue
- **Nothing viewers see changed.** Bet 1 waits on #77; the channel is flat at 12 seconds per view.
- **Bet 1's date is now on its ask.** Bet 2 is judged from 30 November to 27 December, and four uploads a day can start only after bet 1's own 24-to-31-day test. So bet 1 needs your label by about 6 November to cover all four of bet 2's weeks; each week later loses one. #77, where you decide, now says so.
- **What tests are judged on.** Every test is judged on watch time, because in August longer-watched videos got more views. On today's 38 recent uploads there is no such link, so a watch-time gain no longer counts as reach. Bet 1's case rests on originality, which gates every route to income.
- **A voice lead.** Plays of Stephen's uploads get past the opening more often than Danielle's: 46% against 31% at the median, beyond chance, and it holds within one subreddit alone. Only those plays count toward the Partner Program, but that lead raises the count only if his uploads hold their views, which this size cannot check yet. It is queued after bet 1 (one change at a time) and needs a sample in the real voice, which only you can make.

### Done
- **Data (weekly review):**
  - Watch time and views: no link (above).
  - Voice: Stephen leads (above).
  - Subreddits: NoStupidQuestions is watched 35% longer than AskReddit, so both stay. Fewer of its plays get past the opening (33% against 45%). Recorded for the four-a-day test. Its views trail by half, too noisy to tell at this size.
  - Titles that address "you" are not measurably worse than the others, so they stay at four in six.
  - Last week's low in views was ordinary weather, as predicted. No background clip needs retiring.
  - A fresh review agreed with every number and verdict and caught six overstated wordings, all fixed.
- **Data (built, live):** the reach checks print a range beside their verdict, showing whether "no link" means ruled out or unseen; reviewed.
- **General management (fix, live):** the review nearly missed one of the five reads due today. The check that says a review is due now also lists those reads. Replayed on this morning's records, it names all five; reviewed.
- **Data (for the monthly):** what tests could be judged on instead. Tests can detect a 20 to 30% change in watch time or in the share of plays past the opening, but would see the Partner Program's count only if it roughly doubled. That share is the useful one: the count is views times the share, and the share shows no link to views, so raising it should raise the count while views hold. One option for you at the monthly: judge tests on that share, keep watch time as the check that viewers are not worse off, and judge views on the whole channel over weeks, as bet 2 does.
- **General management (ranking):** a fresh agent proposed four items; ranked in both orders, the input on what tests are judged on came first, then the voice correction and next Monday's routing, all done. Dropped: the first audience figures (no decision changes). Fixes and improvements were about even.
- **Audience (reopened):** viewers commented on 4 uploads this week (7 comments), against 1 upload in each of the two weeks before. Our rule reopens the reply plan at 3. I built and merged its three code parts, each after fresh reviews. One is the list shifts draft replies into, refusing any with a link, a mention of AI, a claim to be a person, or the viewer's own words. Another is the posting step's checks: never our own comment, never one already answered, never past the daily cap, and only on a clear safety-screen pass. The third connects to YouTube. Three first replies wait in the list for you to see; I skipped a graphic comment and one from an apparent school student. Left: one workflow change, which the monthly sends.
- **Data (rule, before any data):** the capitals test will also show its result within each subreddit; its verdict cannot change.
- **Watch:** five uploads since 15 October had no views at a week old, against three in the six weeks before; no shared topic, two on a clip since retired. This check has now tripped three times since 9 October, and our rule names today's as the point to revisit it, so the monthly will.
- **Reliability:** all 15 uploads since last Monday landed, one with a fallback title (29 October); the safety screen skipped no post. Tonight's evening upload had not started by 21:40: every scheduled job ran 8 to 10 hours late today. The alarm that would email you about a missed upload is built but not yet on (it goes in the monthly's bundle); until then the next shift catches a miss.
- **Security:** no workflow change since 20 October, no secret in the repository, money controls in place ($0.01 this month, forecast $0.76 of $3); library warnings unchanged.
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (one label ships bet 1, by about 6 November for bet 2); #82 (register by 12 January); #86 (very likely not needed: close it); #65 (it still waits for your "yes" to the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **The November monthly review is due now** and is the next shift's first work. It brings you three things: the 14 December source date, the income read, and what tests should be judged on (watch time's missing link to views, and the zero-view check that keeps tripping).
- Check that tonight's evening upload landed; after midnight still counts as today's.
- The monthly also sends you the reply job's and missed-upload alarm's workflows, both ready. Next Monday: re-read the no-view uploads by subreddit, as set tonight.

### Better?
- **Than last shift:** a little. Bet 1's ask now shows its deadline, and watch time shows no link to views, which sharpens what the monthly asks you.
- **Than ~10 shifts ago:** no for viewers. Watch time is flat at 12 seconds; first-week views over four weeks are up a third, inside normal swings; bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---
