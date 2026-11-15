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

## 2026-11-15 (11:37) — The backup show is finished and switching it on is one prepared change; bet 1 merges with every test passing again

    Worked (% of the shift): strategy 45 · gm 20 · reliability 15 · legal 10 · security 5 · engineering 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). The backup show, which keeps uploads going if Reddit access ends on 12 January, is now fully built and switched off. Turning it on is prepared as one change, which your label on #90 merges once its music tracks are in.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. I found and fixed one problem: bet 1 had stopped merging cleanly into the live code, because two of its tests failed against a change made yesterday. With that fixed, bet 1 merges with all 1,239 tests passing, so your label can still merge it straight away.

### Done
- **Strategy (the backup show, finished):** its last condition, never the same background clip twice in a row, passed its sample video (playable, 28 seconds) and merged switched off. Every condition a shift can build is now done.
- **Strategy (its switch-on, prepared; a bet):** turning the backup show on is now one ready change. Its videos are recorded under their own version name, so their verdict never mixes with Reddit's. A fresh reviewer found that my first version would have filed bet 1's videos under the backup show's name if bet 1 landed later. I fixed that by naming the version after the format it runs on. The naming is live and changes nothing today.
- **Reliability and general management (the switch-on's loose ends, two of three fixed):** once the backup show was on, our release check would have reported a failed release whenever the backup show's title check could not reach the AI. It now reports "could not check", and a garbled answer still fails. Our tracker check now reads the version an upload actually ships, so after the switch it will flag the tracker until the tracker names the new version. The third loose end is written down for the shift that switches it on: after the switch, sample videos could only show the backup show. Both fixes were reviewed fresh and merged.
- **Legal (ready for 7 December):** the fix for YouTube text we keep past YouTube's 30-day limit is ready as a separate change. The stored copy keeps video IDs and statistics and drops titles, questions and answers. It rewrites stored data, so it waits on your decision at the 7 December review.
- **General management (ranking):** with nothing ready, a fresh helper proposed eight ideas and two others ranked them forwards and reversed. Both rankings put the same two first, and I did both. Dropped:
  - steering the backup show's questions toward topics that seem to do better: those figures are not compared at the same video age, which our rules count as no evidence;
  - a countdown to 12 January for shifts: only you can register the app;
  - upgrading a login library with a known flaw: already checked, our use cannot reach the flaw, and it goes in with the next library update;
  - moving sample videos to Google's winter reset hour: it needs a workflow change and a rule change, both yours, for little exposure;
  - a question on how concentrated views are: a weak reason, and probably too few videos to answer;
  - measuring how often the backup show's question writer repeats itself: about 5 AI requests, more than was safe before the 12:23 upload.
  After the top two I fixed two of the switch-on's three loose ends (above). The third needs a workflow change of yours, and only matters once #90 is labelled. Nothing else cleared the bar, so I handed over at 11:37, 15 minutes early.
- **General management (your approved asks):** #88 and #65 are labelled approved, but a shift can do neither. #88 is a change to the shift instructions that only you can apply; its patch, posted there, still applies cleanly today. #65 still waits on your yes to the corrected sentence.
- **Security and reliability (checked):** both of yesterday's uploads and this morning's landed. Money controls are intact ($0.33 so far this month, forecast $0.78 of $3). No secret committed, and the only workflow-side change was the settings line you approved on #95.
- AI use: one sample video, whose requests go to the sample model, at 10:56, well over an hour before the 12:23 run. No other AI requests and no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #90 (now one label plus the music tracks), #65 (waits on your yes to the corrected sentence), #80, #59.

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging.
- **If #90 is labelled and the music is in:** settle the switch-on's last loose ends (the release check's AI request count, and sample videos of Reddit's show), take a sample video of the switch-on, then merge it.
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and AskReddit's falling share watched (read last night under its rule). **About 18 November:** the new model's 20th video. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read. **7 December:** the data-retention decision, now ready.

### Better?
- **Than last shift:** no, not toward revenue. The backup show is finished, its switch-on is one label away, and bet 1 merges cleanly again after quietly breaking.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds and bet 1 hasn't shipped. The backup show has gone from a sample to built, with its switch prepared.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-14 (23:45) — The backup show's title check passes every test case on our AI models, and it no longer repeats a question in new words

    Worked (% of the shift): strategy 60 · engineering 15 · gm 15 · data 5 · security 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). The backup show, which keeps uploads going if Reddit access ends on 12 January, is two steps nearer being ready to switch on: its title check is finished and proven, and it now refuses a question it has already asked in different words.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest thing is the backup show: without it, uploads stop on 12 January if the Reddit app is not registered (#82), and they stop in March 2027 either way. It stays switched off; turning it on is still your call (#90).

### Done
- **Strategy (the backup show's title check, finished; a fix):** a word list was meant to stop its titles passing the AI's takes off as real people's, but it kept letting wordings through and blocking ordinary questions ("Why do people say sorry so much?"). It now only blocks the word Reddit and subreddit names, and a separate AI check judges the rest. When that check refuses a line, the upload record now says so; before, a refusal looked like a title the AI never wrote. I tested the check on our two AI models with the fixed set of example titles: 15 of 17 right at first. It let through "3 Answers That Changed How I Tip" and "A stranger told me something I can't forget". I tightened its instructions, using examples unlike the test cases so it could not just learn the answers. After that it got 20 of 20, then 26 of 26 on both models, once I added six cases unlike its examples and three closing lines. Two fresh reviewers found nothing that had to be fixed; their smaller points are fixed or noted in the code.
- **Strategy (a sameness check; a bet):** YouTube's spam rules name AI videos made "with minimal changes". The backup show refused only an exact repeat of a past question, while an AI writing questions rewords itself ("relax after a long day" / "unwind after a long day"). It now refuses any question that shares half or more of its words with one we have shipped. Only 3 of our 238 Reddit questions would have tripped that rule, so it catches rewordings, not variety. A reviewer then found that a refused question would have failed the whole run, about 3% of runs, because the backup AI route is off. So a repeat now gets one more try, with the AI told which question to avoid. Both changes were reviewed fresh and merged switched off. The last condition, never the same background clip twice in a row, is built and reviewed too, and waits on a sample video.
- **General management (ranking):** with nothing ready, a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. The same four came top both ways. I did the top one, the sameness check. Dropped: re-reading YouTube's template rule against the backup show's format (answered on 26 October, and that answer is where the music and sameness conditions came from); a test that the backup show never contacts Reddit (reading the code answers it: only the Reddit path ever connects). Fourth both ways, measuring how often the question writer repeats itself, needs AI requests after 08:00, so it is for a later shift.
- **Security and reliability (checked):** both of today's uploads landed. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; no workflow change. One slip: a merge pushed the live branch with one failing test (a status written in the wrong form in our plan). I fixed it a minute later and nothing ran on it.
- **Data (a question answered, narrowly):** is AskReddit's falling watch time just shorter videos? With the rule set first, our reporting tool now shows the share of each video watched week by week. That share is falling, so viewers are leaving earlier too (details under Next).
- AI use: 6 of Google's free requests (4 on the sample model, 2 on the uploads' model), all between 23:10 and 23:16, over an hour before the 00:23 run; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65 (waits on your yes to the corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging.
- **Ready now:** the backup show's last buildable condition, never the same background clip twice in a row, is built and reviewed on a branch; it changes how the video is put together, so it merges only after a sample video passes. Ask for one after 08:00, an hour clear of an upload. Then measure how often its question writer repeats itself (about 5 requests, with the rule set first).
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and AskReddit's falling watch time. For that last one I set the rule tonight before seeing any figure, added the missing weekly view of the share of each video watched, reviewed fresh, and read it: AskReddit's share fell from 58% to 53%, just beyond its usual weekly swing of 5 points. By the rule, viewers are leaving earlier, not only watching shorter videos, though narrowly; the review weighs it. **About 18 November:** the new model's 20th video. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read.

### Better?
- **Than last shift:** no, not toward revenue. The backup show's title check is proven on both our AI models, and it now refuses reworded repeats, which YouTube's spam rules would count against it.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds and bet 1 hasn't shipped. The backup show has gone from a sample to built, checked and switched off, waiting on you.
- **Than ~100 shifts ago:** too early to say.
