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

## 2026-10-10 (16:14) — Most of the rise in buried uploads was the clip we already retired; a check on the new opening is set for Monday

    Worked (% of the shift): data 50 · gm 25 · reliability 15 · security 10

**Summary:** Since mid-August more of our uploads have been barely shown (5 views or fewer in their first week). Most of that rise was the background clip we retired on 28 September. The rest leans toward the new opening, so I fixed the reporting tool so it can test that, and set Monday's check before seeing Monday's data. Nothing moved revenue directly. This protects Monday's verdict on the new opening.

### Toward revenue
- **Nothing directly.** Every change to what we ship is waiting on Monday's data or on you. If the new opening gets more videos buried, Monday's verdict will now show it, where before the tool would have missed it.

### Done
- **Data (research and a fix):** 15 uploads since mid-August got 5 views or fewer in a week, and 9 of them were on the retired clip. In the same week, that clip's uploads were buried 3 of 4 and the other clips' 0 of 10. So retiring it looks right, not a coincidence of timing, though the weekly groups are small. Of the rest, 3 of the new opening's 12 measured uploads were buried, against 5 of 119 before. That is suggestive but not yet beyond chance. The tool could not test a release this way at all: it compared each release only with itself and always reported no difference. Fixed, reviewed by a fresh agent (its corrections made) and merged. Monday's check is written down in advance, beside the release verdict and **never a trigger**.
- **Data:** without the clip, burying began rising a week *before* the new opening went live, and Monday's reader needs that. A small option to group uploads by week shows it. Reviewed and merged.
- **Data:** the "zero watch time" readings on a few viewed uploads are YouTube's own figures, in whole seconds, not something we store wrongly. Nothing to fix.
- **Reliability:** when both safety-check AI models are overloaded, the upload still ships, checked only by a keyword filter. The keyword filter alone has checked two uploads this month, and none was lost. The check has skipped no post since 30 September, so it is not using up material. Tonight's upload is the first to record the capitals coin, and the log adds the new column safely.
- **General management:** had six candidates ranked in a separate pass. Ran the reporting commands Monday's reads use against last week's data, and all of them run. Closed a month-old code-health item: a YouTube figure that disagrees with the others, which nothing decides on.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: all measurement and fixes. The one improvement viewers will see, the capitals test, goes live tonight.

### Blocked
- **For you, unchanged since this morning:** the label on #70 (bet 1's first step); the four commands on #50; the Groq key and label on #69; the planning session (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53; pasting #65's sentence.

### Next
- **12 October:** read `v7` under its rule, then the new buried-upload check beside it (remember the rise began a week before `v7`). Then the engaged-view, narrator, dark-morbid and zero-view questions, the clip check and the first subscriber count.
- After tonight's upload: check its log row carries a capitals group (1 or 0) and that the title obeys it.
- Considered and dropped: pricing the revenue routes (already in the plan, and the third bet is yours to take); a story-mode spec (waits on your bet-1 answer); the overlapping-runs workflow fix (needed only for four a day, about three weeks off, and it would be a ninth ask).

### Better?
- **Than last shift:** Unclear. The video did not change. Monday's verdict can now see a cost to the new opening that it would have missed.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the capitals test, the first change aimed at views in two weeks, goes live tonight.
- **Than ~100 shifts ago:** Too early to say.

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
- Checked and cleared: whole-release reads are not exposed the same way. A batch of 20 uploads drops 13% by chance far less than one time in ten (4–8%), so their limit is safe. They still count the zero-watch uploads; one is in Monday's opening-question read, which is read as written.
- I handed over about 20 minutes early: nothing is ready until Monday's data, and the two edge cases left in the new reading option touch no rule's read. Considered and dropped: a backup model for titles (a failed title costs no watch time, per the 28 September finding, and none has failed since the longer overload wait of 4 October); a question-mark title test from existing data (views need about 30 uploads a side, so only an effect larger than the capitals one could show); cutting narration's second paid call per segment by timing words locally (it needs real narration files, which a shift never holds); building four-a-day ahead of your answer (the audit's lesson).

### Better?
- **Than last shift:** Yes. The first change in two weeks aimed at views is live, and the tests that gate more uploads a day can no longer be failed by chance so easily.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the video itself has not changed since 25 September. The capitals test reads in mid-November.
- **Than ~100 shifts ago:** Too early to say.
