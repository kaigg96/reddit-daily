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

## 2026-11-03 (19:25) — The three sample videos your open decisions rest on were due for deletion on 8–9 November; they are now kept

    Worked (% of the shift): gm 50 · legal 20 · reliability 10 · audience 10 · security 10

**Summary:** Nothing viewers see changed, and bet 1 still waits on your label (#77, ideally by 6 November). GitHub deletes every sample video 14 days after it is made, so bet 1's sample and both replacement-source samples would have vanished on 8–9 November, before #90's 14 December decision. They are now kept, and both issues link the copies.

### Toward revenue
- **Nothing directly.** Everything viewers would see waits on bet 1 (#77), and the channel is flat at 12 seconds watched per view.
- **Protecting the decision that matters most.** Bet 1's sample (#77) is the video you were asked to judge. A new render would write different host lines, so the one you were shown could not be made again. A copy now stays on a branch with no expiry date, linked under the original in #77. #90's two samples are kept the same way.

### Done
- **General management (fix):** kept the three sample videos (above). I edited the issue text rather than commenting, so no extra email. #89's text was left alone, since editing it would stop its patch from applying.
- **Legal (results night):** read the narration of the last two uploads before tonight's: none says anything about voting or the election. Tonight's had not started by the time I handed over.
- **Legal (answered, dropped):** should answers, not only questions, be screened for voting claims until 10 November? In 5 of 993 past uploads an answer mentioned voting under a question that wasn't about it, and none gave voting information. Too rare for a release in the window's last week, so the check stays a read.
- **Audience (fix):** checked the three replies #89 would post. The one stating a legal fact ("US courts have allowed some deception during questioning") is accurate, and the note sits beside it in the list #89 links.
- **General management (ranking):** nothing was ready. A fresh agent proposed eight ideas and I added two. Two rankers, reading in opposite orders, both put the sample videos first, results night second and the reply check third. Dropped: a fallback plan if #77 slips (on 6 November only if still unlabelled: it would be a twelfth ask); a cut for Monday's zero-view read (chosen after the fact); Groq's newer models (two failed already); run lateness against four a day (a month away); the election skip's end date (ends by itself); the run logs (nothing exposed); compressing the findings (not in 30 minutes). A second round, aimed at deadlines that could pass unnoticed and at functions rarely worked, ranked the same two ways, put two dated checks first and the expiry warning third (all three below). Dropped from it: an age limit on queued replies (nothing posts until #89; recorded beside the reply rule for before 16 November); a record of bet 2's lost weeks (bookkeeping); closing an old weekly digest (changes nothing); which comments download each reply read uses (the fix that matters is keeping the file).
- **General management (fix, live):** the list of your decisions that every shift reads first now warns when a sample video an open ask links is within a week of deletion, and says whether a kept copy is linked. Today it names the three above, each with its copy; reviewed.
- **Legal (fix):** the check of Reddit's terms against today's saved copies, due on or after 10 November, now has a dated row that the weekly review lists, rather than only a sentence. It must happen before #90's 14 December date.
- **General management:** two lines pointed at the 5 November review, which the monthly replaced; each now says where its item went.
- **Reliability:** both uploads on 2 November and this morning's landed; the afternoon runs were the planned no-ops. Tonight's run had not started at handover; scheduled jobs have run hours late all week.
- **Security:** no workflow change since 20 October, no secret in the repository, money controls intact ($0.05 this month, forecast $0.71 of $3).
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1, by about 6 November), #82 (register by 12 January), #89, #90, #91, #92, #88, #86, #65, #80, #59. Nothing new was added.

### Next
- **Results night, continued:** check tonight's upload landed, then read its narration and tomorrow morning's for election claims. The upload run's log prints every spoken line.
- **6 November:** if #77 is still unlabelled, decide whether a fallback is worth a twelfth ask.
- Carried from the monthly: 9 November's zero-view re-read by subreddit, 16 November's view-swing read.

### Better?
- **Than last shift:** a little, defensively: the evidence for your two biggest open decisions no longer expires.
- **Than ~10 shifts ago:** no for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-03 — Monthly review: no route to revenue is in reach yet; bet 1 still decides the month, and five new asks each need one label

    Worked (% of the shift): gm 25 · data 15 · strategy 15 · legal 10 · market 10 · reliability 10 · finance 5 · monetization 5 · audience 5

**Summary:** For viewers and revenue we are no closer than a month ago: bet 1 has not shipped, and watch time is flat at 12 seconds a view. The next month turns on bet 1 (#77), ideally labelled by 6 November, and the Reddit registration (#82) before 14 December.

### Where we stand
- **Revenue $0.** About 14,500 plays a quarter get past the opening. The Partner Program needs 10 million (691 times short; a month ago, 757), and 20 million for new applicants from February. We have 23 of the 1,000 subscribers it needs. The nearest route, the 500-subscriber tier, is 207 times short.
- **Can the current path reach the goal? Not at today's size, plainly.** Every route needs the format to be ours first (bet 1), then far more views per video: six uploads a day leaves every YouTube route at least 70 times short. What would make it known: bet 1's first 20 uploads, then bet 2's four weeks from 30 November.
- **One warning is real, not noise.** Uploads with no views at a week old rose from 1 in 41 to 6 in 34. It has fired on 3 of the last 5 weekly reads, and held at matched ages. Today's checks found no shared fault in our pipeline; of the five old enough to check, one was age-restricted for a swear in its title, which the filter has refused since 24 October. Next Monday's read checks the other four by subreddit.
- **Every function now has work behind it:** audience, monetization and market intelligence moved off "none".

### Money
- Speech has cost $0.05 so far this month, forecast $0.70 of the $3 budget. Every control at Amazon is intact. Priced this month: four uploads a day at about $1.80 a month. Nothing new spent.

### Risks
- **Ratings unchanged:** YouTube's rules and Reddit's terms, read first-hand today, say what they said a month ago.
- **A line we had not recorded:** YouTube's spam policy, which can end a channel, bars "re-posting material from other websites… without adding anything of your own". Bet 1's host reactions already answer it.
- **New: shifts went dark for two days.** When the weekly usage allowance runs out, shifts are skipped until Friday, three weeks running: six in a row on 28–30 October, with nothing checking uploads or money. #92 answers it.

### Market and policy
- **Policy pages:** no change to YouTube's eligibility, monetization, Shorts or spam pages, or to Reddit's terms. Reddit's registration page confirms 12 January; its builder-policy page refused us. No new asset needs a licence check.
- **Comparable channels:** a Reddit-stories channel with human voices was reportedly demonetised in May, while hosts who give opinions stay paid (secondary source): the host's view, bet 1's plan, matters more than a voice.
- **New on YouTube:** Shorts can be grouped into a series. A free test after bet 1, once you switch it on in Studio: one recurring show.
- **Reddit** reportedly updates on 10 November; today's pages are saved to compare before 14 December.
- Discarded: three platform changes.

### Proposals for you
Five new asks, none costing money:
1. **A replacement source, with a date (#90).** If Reddit hasn't confirmed our app by 14 December, build our own questions as the source, merged switched off; one label turns it on. You can approve the date alone and choose after narrated renders, which only you can make. Both allow earning, unlike Reddit; ours are not a reading and never run out.
2. **What tests are judged on (#91).** For new tests, the share of plays past the opening, with watch time as the viewer check: watch time shows no link to views, and the Partner Program counts views times that share.
3. **Two finished jobs: replies to viewers, and an email to you when an upload is missed (#89).** One label applies both and posts the three queued replies that evening, so please read them first.
4. **Two shifts a day instead of three** (#92), so no day goes without one.
5. **Three stale lines in the shift instructions** (#88), fixed to match the tools.

Still waiting: #77 (bet 1, by about 6 November), #82 (register by 12 January), #86 (closes if #89 lands), #65, #80, #59.

### Next month
- Bet 1 (#77) decides the month: nothing viewers see changes until it ships.
- **Results night:** read tonight's and tomorrow morning's narration for election claims.
- **9 November:** the zero-view re-read by subreddit. **16 November:** are weekly view swings viewers or data. **About 23 November:** the capitals test. **24 November:** the friction log's verdict. **30 November:** bet 2's four weeks begin.
- Carried: shortening the product plan's findings and a word cap per work-log entry.
- **Built (fix, reviewed, merged):** a command listing every past sample video's verdict, which today took digging by hand.
- **Set before any reply posts:** the reply job's keep-or-stop rule.
- **Ranked and dropped:** a screen replay (new tooling); upload delays (timing showed no effect, 09-30); a series row (waits on bet 1); subscribers per upload (nearly all zero); late uploads (two).

### Better?
- **Than last shift:** a little: the source and test-measure decisions are with you.
- **Than ~10 shifts ago:** no for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---
