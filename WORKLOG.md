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

## 2026-10-10 (10:00) — The capitals test goes live tonight, and three tests are now judged against what chance actually produces

    Worked (% of the shift): data 45 · product 20 · gm 15 · reliability 10 · strategy 5 · security 5

**Summary:** The fair test of capital letters in titles passed its sample video. It goes live with tonight's upload, together with the safety check's crash fix. I also corrected how three of our tests will be judged. Their watch-time limits were small enough that chance alone would trip them about one read in five, which could wrongly drop the second subreddit and, with it, the case for more uploads a day.

### Toward revenue
- **Yes, a bet on views is live.** From tonight each upload flips a coin: one word in capitals in its title, or none. Titles with capitals got about twice the views, but that was an observation; this test shows whether the capitals cause it. It reads around 16 November.
- **The judging fix protects the route to four uploads a day,** the one lever our data says grows views. The subreddit test decides whether we have enough material for it.

### Done
- **Product (a bet):** the sample passed, and its title obeyed its coin (a "none" draw, no capitals). Merged with the crash fix, which stops an oddly shaped AI reply from costing a slot its upload.
- **Data (a fix):** beside every two-way comparison, the reporting tool now prints how far two random groups of the same sizes land apart one time in ten with nothing changed, measured over the last six weeks. It can also keep a comparison to the weeks a test ran. The subreddit, title-style and capitals tests now judge watch time against that: about 18%, 30% and 16%, in place of 12–13%. All three were set before any of their data was read. A fresh review found real problems in my first version, and the biggest changed the answer: random groups of our uploads now land about three times further apart than in July, so measuring chance over all history understated it. Fixed, and checked again before going live.
- **Data (research):** found most of why chance has grown. More uploads now get only a handful of plays (11 of the newest 90, against 1 of the first 45), and six of those are recorded with no watch time at all, which may be YouTube reporting nothing. Leaving such uploads out cuts the noise at 15 a side from 31% to about 18–20%, roughly what two to three times the uploads would buy. We cannot tell a missing figure from a real zero, so the subreddit and title-style tests now leave out uploads under 10 plays, with the count of buried uploads printed beside them, rather than declaring the zeros missing. One of the zeros is in the opening-question release read on 12 October.
- **Reliability:** this morning's upload was the first live need for the backup safety model. It answered, and the log recorded it. The main model was overloaded on 3 of the last 5 uploads, and all were covered.
- **General management:** ranked the queue in a separate pass. Checked that the patch on #50 still applies cleanly to today's code, so your four commands work as written. Cut the product tracker's release history to one line per release, which two shifts running had spent about a tenth of their time working around.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: one of each. The improvement is the one viewers will see.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50 (still current); the Groq key and label on #69; the planning session (#55); asking Reddit (#60, a draft is in the issue); the music script (#66); the account checks (#59); re-running the comments job on #53.

### Next
- After tonight's upload: check its log row carries a capitals group (1 or 0) and that the title obeys it.
- 12 October: read `v7` under its rule, then the engaged-view, narrator, dark-morbid and zero-view questions, the b-roll clip check, and the first subscriber count.
- Around 26 October, a week before the subreddit test reads: ask you by label for four-a-day's narration spend (about $0.90 a month more, inside the $3 budget), so volume can ship the day the test passes. Not now: it is three weeks from being needed, and you have eight open asks.
- Before the next release read after 12 October: decide whether release reads should also leave out uploads with almost no plays. Today they still count the zeros.
- Considered and dropped: a backup model for titles (a failed title costs no watch time, per the 28 September finding, and none has failed since the longer overload wait of 4 October); a question-mark title test from existing data (views need about 30 uploads a side, so only an effect larger than the capitals one could show); cutting narration's second paid call per segment by timing words locally (it needs real narration files, which a shift never holds); building four-a-day ahead of your answer (the audit's lesson).

### Better?
- **Than last shift:** Yes. The first change in two weeks aimed at views is live, and the tests that gate more uploads a day can no longer be failed by chance so easily.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the video itself has not changed since 25 September. The capitals test reads in mid-November.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-09 (23:15) — Titles with one word in capitals get about twice the views; a fair test of it is built and needs only its sample video

    Worked (% of the shift): data 35 · product 20 · legal 10 · market 10 · engineering 10 · strategy 5 · security 5 · gm 5

**Summary:** Our videos whose titles put a word in capitals ("Who's YOUR Hero?") got about twice the views of the rest. That held in every split with enough uploads to read, and viewers watched them about as long. I built a fair test that flips a coin for each upload, and it needs only tomorrow's sample video to go live. Views are the half of YouTube's payment bar we are furthest from, so this is the first step in days aimed at it.

### Toward revenue
- **Yes, a bet on views.** The pattern is a correlation: the AI may capitalise when a post is livelier anyway. The coin-flip test settles it at no cost. Its rule is set in advance. After 30 uploads in each group, keep capitals if their views lead is bigger than chance alone produces one time in ten at that size (73% today), and watch time holds. A smaller lead gets one extension, to 45 uploads per group. My first bar (30%) sat inside chance; I reset it before anything shipped.

### Done
- **Data (a bet):** taught the reporting tool to tell titles with emphasis capitals apart from plain ones. Read at 7 days old: +120% views overall (65 against 68 uploads), and ahead within each earlier release, title style, title length and time of day, and still at 14 days old (+77%). Watch time 10 against 11 seconds, inside the normal swing. The extra plays are the kind YouTube's payment bar counts: the same share are engaged views (31% against 30%). It also explains most of the lead behind favouring "You…" titles (5 October). Those nearly always capitalise "YOU", and among capitalised titles they lead by only 7%. That decision's rule is on watch time, so it stands. A lead, on small weekly numbers: the fall in views since mid-September is almost all in titles without capitals. A fresh review's fixes came before the numbers were recorded. Live, measurement only.
- **Product (a bet):** built the coin-flip test on a branch. One group is asked for exactly one capitalised word, the other for none. Both are banned from shock phrases. A free local sample rendered, and a fresh review found nothing blocking. It needs only a real sample.
- **Legal / market intelligence:** read first-hand that since July 2026, YouTube will not pay for content "designed to shock or surprise viewers for the sole purpose of getting views", and its reviewers read titles. 9 of our 166 titles use phrases like "SHOCKING" or "You Won't Believe", so both test groups now forbid them. Capitals for emphasis are not what that rule names.
- **Strategy:** 883 of the channel's 1,041 videos predate July's pipeline (30 are duplicates). All are readings, and they earn under 1% of today's views. YouTube's reviewers check a channel's "main theme", so I added to the brand decision: when you settle the name, also decide whether to make them private or start the new show fresh.
- **Market intelligence:** secondary sources say Reddit's commercial access is a negotiated deal from about $12,000 a year. Reddit's own pages refuse automated reads, so this is unconfirmed. If true, it matters to #60 more than the format does.
- **Security:** standing check clean. Narration spend $0.25 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change. Tonight's upload landed normally.
- Fixing against improving: almost all improving; the last shift was all fixing.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50 (#65 waits on it); the Groq key and label on #69; the planning session (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53.

### Next
- Morning, after 07:00: one sample video is allowed per shift, and two reviewed branches wait for one: the safety check's crash fix and the capitals test. I have combined them on one branch, with all tests passing, so one sample clears both. The crash fix changes nothing viewers see, so this still tests one thing, and the test starts a day sooner. If the combined sample fails, take the crash fix alone first. The sample's report shows the title beside its group; check the title obeys it.
- Before the subreddit and title-style tests read (about 2 November): their watch-time limit sits where chance lands half the time at their size, not one time in ten. Reset it against the new measure before their data is read, as I did for the capitals test.
- 12 October: read `v7` under its rule, then the engaged-view, narrator, dark-morbid and zero-view questions, the b-roll clip check, and the first subscriber count.
- If #70 is approved, build it on a branch. The capitals test is a coin per upload, so it runs alongside bet 1 without spoiling either read.
- Process: the company plan and the product tracker sit at their word limits, so each finding meant trimming unrelated text first, about a tenth of the shift. Worth a look at the next audit.
- I handed over about 20 minutes early. Considered and dropped: resetting the two tests' limits tonight (two titles in three are style B, so the other group stays small; that needs a deliberate redesign before 2 November); a note to you on bet 1 about YouTube's AI-host rule (the plan already says the host never advises); a question-mark title test (it would queue behind the capitals test); the open code-health items (each needs you, a sample, or Monday's read).

### Better?
- **Than last shift:** Yes. For the first time in several shifts, something that changes what we ship is ready, aimed at views, and costs nothing to run.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the video itself has not changed since 25 September. The capitals result is the largest views difference any logged title trait has shown, but it is a correlation until the test reads, in mid-November at the earliest.
- **Than ~100 shifts ago:** Too early to say.
