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

---

## 2026-11-01 (22:50) — Election week can no longer fail an upload: the fix is live a day early. Bet 1's branch is current again, and the watch-time question is set for Monday

    Worked (% of the shift): editorial 30 · data 35 · engineering 15 · gm 10 · reliability 5 · security 5

**Summary:** The election-week fix merged tonight instead of tomorrow. A results-day upload no longer fails when Reddit's top questions are all about the election. Nothing moved revenue directly: bet 1 still waits on #77, and I brought its branch back in line with tonight's change so your label still ships it in one step.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view, and bet 1 is still the only answer to that.
- **Protecting the uploads.** The election fix is live from the next upload, about 06:00, two days before the polls close.
- **Checking that we measure the right thing.** Every test is judged on how long people watch, but revenue needs views. In August, watch time was the best predictor of views we had. Monday's figures will show whether it still is, judged by a rule I wrote down tonight before looking at any number. If it no longer predicts views, a watch-time gain stops counting as progress toward revenue, and the November monthly brings that to you.

### Done
- **Editorial (fix, live):** the last shift timed the election fix's sample video for tomorrow at 11:17. The 12-hour limit on samples actually lifted at 23:09 tonight, so I asked then. It passed: the video plays (32 seconds, picture and sound). I merged it. All 719 checks pass. On an ordinary day nothing changes. When election week leaves no usable question in the day's top 10, the run reads the top 30 instead of failing.
- **Engineering (fix):** merging that fix left bet 1's waiting branch in conflict with it, so your label on #77 would have stalled. I combined the two by hand, keeping bet 1's medical-topic skips where they were. All 973 of that branch's checks pass, and tomorrow's 08:17 release check re-tests it. A fresh review found nothing wrong. It confirmed that git's automatic merge would have crashed the run at the first usable post, and that the hand fix avoids it.
- **Data (rule set, read Monday):** a new report compares each upload's watch time with its views at about a week old, for uploads since 5 October. There are three outcomes: they rise together, they move in opposite directions, or there is no link. A fresh review found no fault and three small points; all three are fixed. It is on main.
- **General management:** the election fix was the only ready item. Five hours ago the 17:45 shift ran two rounds of ideas and named the watch-time question as the best one left. No new data has come in since, so I took that question rather than generate ideas again. With nothing ready after it, I looked once more, only at what tonight changed, and found nothing above the bar. Dropped: a check that every merge keeps bet 1's branch mergeable (each shift's start already runs it, and tonight's break was caught within a minute); removing the election code after 10 November (it switches itself off). Two of tonight's three items were fixes, and one improves how we judge our tests.
- **Reliability, security:** both of today's uploads landed. No workflow has changed since 20 October, and no secret is in the repository. The money controls are in place ($0.01 so far this month, forecast $0.76 of $3).
- AI use: none from the upload allowance; no Polly; one sample video, on the test model's allowance.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #82 (register by 12 January; check the app's name first); #86 (very likely not needed: close it); #65 (it still waits for your "yes" to the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Morning, from about 06:00:** check that the first upload under the election fix landed. A pick ranked 11 or lower means it read the top 30.
- **The 11-02 snapshot, then the weekly review:** read the watch-time question once. The voice test and the second-low-week check are due that day too. Then the November monthly; its single proposal carries the upload alarm's one-step change.
- **08:17 release check:** confirm it passes on bet 1's updated branch.

### Better?
- **Than last shift:** A little, for safety, not for viewers. The election fix is live rather than waiting, and bet 1 still ships with one label.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
