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

## 2026-11-15 (18:30) — Your approval on bet 1 can no longer lose its sample video; the backup show's kind of question shows no cost in watch time

    Worked (% of the shift): data 30 · engineering 20 · strategy 15 · gm 15 · product 10 · reliability 10

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). Three of your open asks got easier to answer: bet 1's sample video no longer expires, the backup show's music has a route that needs only your say-so, and four uploads a day no longer has to wait for bet 1.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest step: bet 1's sample video, the one piece of evidence behind that label, would have been deleted by GitHub on 27 November. It is now kept for good, and #77 links to the kept copy.

### Done
- **Product (bet 1's evidence kept; a fix):** the 13 November sample is copied, byte for byte, to where we keep the backup show's samples. Editing #77's text sent you no email.
- **Data (a question answered: no evidence of a cost):** the backup show replaces Reddit's questions with plain everyday ones, with no news, health, sex or named people or brands. Do questions of that kind hold viewers less? I set the rule and saved it before seeing any figure. A fresh reviewer found my sorting misfiled 21 questions one way, for example "…of Reddit" openers and capitals used for emphasis. I fixed that, again before any figure. Among AskReddit videos at a week old, everyday questions held viewers 10.0 seconds against 11.0 for the rest, 9% lower. Random halves of these videos differ by 10% one time in ten, so by the rule that is no evidence of a cost, and nothing changes. It is narrow, and the two groups mix our older formats unevenly.
- **Strategy (music for the backup show; a bet):** #90 needs more music tracks, which today means your hands. Kevin MacLeod's library is free to use with a credit, may be kept openly in our public files, and is registered with YouTube's copyright matching. A video only gets claimed when the credit is missing, and a claim is released within three days of a dispute. So "use those" on #90 would let a shift do the rest: pick the tracks and add the credit to each description. I built nothing, because the track choice is yours to approve.
- **Strategy (a loose end closed):** after the backup show is on, sample videos of Reddit's show still work from a test branch. No workflow change of yours is needed, despite what the last handover said.
- **Engineering (four a day, unblocked from bet 1; a bet):** going to four uploads a day needs each run's time slot in the upload log. That change was built on top of bet 1, so four a day had to wait for it. It now also exists on the live code, ready but not merged. It still merges cleanly with bet 1 in either order, and all 1,242 tests pass on the two together. A fresh review found nothing blocking. I fixed its two small points: the slot is now worked out before the upload, and the weekly report counts late uploads on the right day. So the 20 November update to #80 can offer four a day first.
- **Reliability (a four-a-day risk re-checked):** a pile-up of late runs could cancel a waiting upload. None of the 394 scheduled runs since June was cancelled. Since 13 October no two runs started closer than 3 hours apart, even with GitHub starting them hours late.
- **General management (ranking):** with nothing ready, a fresh helper proposed seven ideas and two others ranked them forwards and reversed. The top four came out in the same order both ways, and I did them plus a fifth. Dropped: an automatic switch to the backup show only if Reddit cuts us off. It is the costliest of the seven, more than this shift had left, and both rankings put it last or nearly last.
- **Security and reliability (checked):** both of yesterday's uploads and this morning's landed; the 12:23 run was a normal skip. Money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret committed, and no workflow change since #95.
- AI use: none of Google's allowance (the 18:23 upload was within the hour), no sample video, no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #90 (one label, plus music, or "use those" for the route above), #65 (your yes to the corrected sentence), #80, #59.

### Next
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and AskReddit's falling share watched.
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging (today's copy, which has the review's fixes; all tests pass with bet 1).
- **If #90 is labelled:** settle the release check's AI request count, then take a sample video of the switch-on, then merge it.
- **About 18 November:** the new model's 20th video. **20 November:** if bet 1 is still unmerged, update #80 and offer four a day first. **23 November:** the capitals read. **7 December:** the data-retention decision.

### Better?
- **Than last shift:** no, not toward revenue. Three of your asks got easier to answer, and one doubt about the backup show was tested and not borne out.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

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
