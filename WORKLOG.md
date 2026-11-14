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

## 2026-11-14 (23:45) — The backup show's title check passes every test case on our AI models, and it no longer repeats a question in new words

    Worked (% of the shift): strategy 65 · engineering 15 · gm 15 · security 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). The backup show, which keeps uploads going if Reddit access ends on 12 January, is two steps nearer being ready to switch on: its title check is finished and proven, and it now refuses a question it has already asked in different words.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest thing is the backup show: without it, uploads stop on 12 January if the Reddit app is not registered (#82), and they stop in March 2027 either way. It stays switched off; turning it on is still your call (#90).

### Done
- **Strategy (the backup show's title check, finished; a fix):** a word list was meant to stop its titles passing the AI's takes off as real people's, but it kept letting wordings through and blocking ordinary questions ("Why do people say sorry so much?"). It now only blocks the word Reddit and subreddit names, and a separate AI check judges the rest. When that check refuses a line, the upload record now says so; before, a refusal looked like a title the AI never wrote. I tested the check on our two AI models with the fixed set of example titles: 15 of 17 right at first. It let through "3 Answers That Changed How I Tip" and "A stranger told me something I can't forget". I tightened its instructions, using examples unlike the test cases so it could not just learn the answers. After that it got 20 of 20, then 26 of 26 on both models, once I added six cases unlike its examples and three closing lines. Two fresh reviewers found nothing that had to be fixed; their smaller points are fixed or noted in the code.
- **Strategy (a sameness check; a bet):** YouTube's spam rules name AI videos made "with minimal changes". The backup show refused only an exact repeat of a past question, while an AI writing questions rewords itself ("relax after a long day" / "unwind after a long day"). It now refuses any question that shares half or more of its words with one we have shipped. Only 3 of our 238 Reddit questions would have tripped that rule, so it catches rewordings, not variety. A reviewer then found that a refused question would have failed the whole run, about 3% of runs, because the backup AI route is off. So a repeat now gets one more try, with the AI told which question to avoid. Both changes were reviewed fresh and merged switched off. The last condition, never the same background clip twice in a row, is built and reviewed too, and waits on a sample video.
- **General management (ranking):** with nothing ready, a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. The same four came top both ways. I did the top one, the sameness check. Dropped: re-reading YouTube's template rule against the backup show's format (answered on 26 October, and that answer is where the music and sameness conditions came from); a test that the backup show never contacts Reddit (reading the code answers it: only the Reddit path ever connects). Fourth both ways, measuring how often the question writer repeats itself, needs AI requests after 08:00, so it is for a later shift.
- **Security and reliability (checked):** both of today's uploads landed. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; no workflow change. One slip: a merge pushed the live branch with one failing test (a status written in the wrong form in our plan). I fixed it a minute later and nothing ran on it.
- AI use: 6 of Google's free requests (4 on the sample model, 2 on the uploads' model), all between 23:10 and 23:16, over an hour before the 00:23 run; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65 (waits on your yes to the corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging.
- **Ready now:** the backup show's last buildable condition, never the same background clip twice in a row, is built and reviewed on a branch; it changes how the video is put together, so it merges only after a sample video passes. Ask for one after 08:00, an hour clear of an upload. Then measure how often its question writer repeats itself (about 5 requests, with the rule set first).
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and AskReddit's falling watch time. For that last one I set the rule tonight, before any figure was seen: our reporting tool cannot yet show the share of each video watched week by week, so add that first. If AskReddit's share holds or rises while its watch time fell, the fall is shorter videos; if the share falls beyond its usual drift, viewers are leaving earlier. **About 18 November:** the new model's 20th video. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read.

### Better?
- **Than last shift:** no, not toward revenue. The backup show's title check is proven on both our AI models, and it now refuses reworded repeats, which YouTube's spam rules would count against it.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds and bet 1 hasn't shipped. The backup show has gone from a sample to built, checked and switched off, waiting on you.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-14 (17:53) — Watch time is falling inside our main subreddit, which would have tilted bet 1's verdict; the backup show's title check is built

    Worked (% of the shift): data 30 · reliability 20 · strategy 30 · gm 20

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). This shift found that watch time inside AskReddit has fallen from 12 to 10 seconds while the channel as a whole reads flat, and set bet 1's read to show that beside its verdict, so a falling baseline cannot pass for a failed bet.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest thing: bet 1's verdict is the one decision on our way to revenue, and it was at risk of a false "revert" (below). Bet 1 still merges cleanly into today's live code, this shift's changes included, with all 1,162 tests passing.

### Done
- **Data (a question answered: yes, falling):** bet 1 is judged on AskReddit uploads against the earlier versions' AskReddit uploads, pooled. I set the rule and saved it before looking. Our reporting tool reads AskReddit's watch time at a week old as falling, 12 to 10 seconds since mid-October, beyond its usual 1-second drift, while the channel overall reads flat (12 to 11), so our second subreddit is holding up better. Recent weeks are thinner, 7–8 AskReddit uploads each, since the two subreddits share the slots. So a baseline pooled from the better weeks would make bet 1 look worse than it is. Its rule is unchanged; if its read says revert, a comparison with the same recent weeks is now printed beside it, never as the trigger. The same holds for the new AI model's own read, due about 25 November, which comes first.
- **Data (a question the tool can't answer yet):** is AskReddit's fall just shorter videos? The tool cannot read the share of each video watched week by week, so no answer; it stays a question for Monday.
- **Data (a question answered: no):** could a topic now justify reopening the parked idea of choosing posts by topic? Its bar is a 50% lead. The best-placed topic, politics and news, leads by 27%, and our tool refused the comparison because those videos are younger. It stays parked.
- **Reliability (a safeguard for 12 January):** if the Reddit app is not registered by then, Reddit will refuse our requests. A new test proves such a refusal stops the run before it pays for narration, writes a title, uploads, or touches the record of what was last posted, whether the refusal comes on the list of posts or later, after the safety check has spent a request. A fresh reviewer found the first version could pass without ever reaching Reddit; fixed.
- **Strategy (the backup show's title check, chosen and built):** the check that stops our own-questions show's titles passing AI-written takes off as real people's has leaked through three rounds of word lists. I chose its replacement, a separate AI check of each title and closing line that refuses when in doubt, because on our channel a separate check works where instructions inside the writing request do not (bet 1's reactions). It costs one request per video and fits the daily allowance at two or four a day. Built, reviewed fresh twice and merged switched off, so today's show is untouched; a failed request now falls to our backup AI models, as the title request does. Two steps are left before the backup can be switched on, now the next shift's ready work.
- **Data (record-keeping):** our list of experiments and their rules now has a test holding it in one consistent form. Adding it found a row whose last cell had split in two, losing part of its references; repaired, nothing else changed.
- **General management (ranking):** a fresh helper proposed six ideas; two others ranked them forwards and reversed, and the top two agreed. I did five of the six in that order, then two follow-ups from the day's findings. Dropped: what our viewers' countries imply for pay per 1,000 views (it changes no decision while we are this far from any paid tier); leaning the subreddit mix toward our second one (its 2 November read: more watch time, fewer plays past the opening). The title check's two remaining steps could not be built, reviewed and merged in the 14 minutes left (one needs AI requests this close to an upload), so I handed over at 17:53.
- **Security and reliability (checked):** both of yesterday's uploads and this morning's landed. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; no workflow change since 11 November.
- AI use: none of Google's allowance; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65 (waits on your yes to the corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging.
- **Ready now:** the backup show's title check, its two steps left.
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and today's lead: AskReddit's watch time is falling while our second subreddit holds.
- **About 18 November:** the new model's 20th video and its title counts. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read.

### Better?
- **Than last shift:** no, not toward revenue. Bet 1's eventual verdict is safer from a false revert, the Reddit cutoff can no longer cost money or a duplicate upload, and the backup show is one step nearer.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, falling inside AskReddit, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
