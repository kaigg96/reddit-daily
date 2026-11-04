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

## 2026-11-04 (19:25) — Two defects viewers could see were found in what we actually shipped; one is fixed, the other waits on a sample video

    Worked (% of the shift): product 30 · reliability 25 · data 20 · audience 5 · gm 10 · legal 5 · security 5

**Summary:** Reading what the channel actually published turned up two text defects, and both now have fixes. Titles that end on a quoted question no longer lose the closing quote; that fix is live. In the title-capitals test, the no-capitals group was also getting an all-lower-case closing line (11 of its 27 videos), which can skew that test's 23 November result; that fix waits on a sample video. Separately, this morning's shift lost its hour by waiting on work it had sent to the background. A guard against that needs your label.

### Toward revenue
- **Indirectly, by protecting a decision.** The capitals test decides how every future title is written. Its no-capitals group was also ending on a closing line with no capital letter, shown on screen and posted as our comment, in 11 of its 27 uploads, against none in the other group. That could make capitals look better than they are, so the 23 November read must now give the same answer with those 11 left out. The tool to do that is built.
- **Viewer-facing fix, live:** this morning's title shipped as "3 answers to 'House and Senate are Blue, how are we feeling?", missing its closing quote. That can't happen again. It was 1 of 217 uploads.

### Done
- **Product (fix, live):** the title fix above. Before merging I replayed every published title and Reddit question through the old and new versions, which caught two of my own mistakes that the tests had missed.
- **Product (fix, built, not live):** an all-lower-case closing line now ships with sentence capitals. Of the 151 closing lines I could recover, only those 11 change. It changes what is on screen, so it needs a sample video first. I didn't request one, because tonight's upload hadn't started and it would have fallen inside the protected hour before it.
- **Data (built, live):** the reporting tool can now leave a list of uploads out of a read. Reviewed; its one finding is fixed.
- **Reliability (fix, live):** the upload log now records each closing line as shipped. It used to exist only in run logs, which expire after 90 days; that's why this leak went four weeks unseen and took 151 logs to count. Reviewed; checked against a copy of the real log.
- **Audience (fix, live):** if you switch on replies to viewers (#89) weeks from now, replies drafted more than two weeks earlier are now refused instead of answering stale comments. This closes the gap recorded on 3 November. Reviewed.
- **General management (fix):** the new logging clashed with bet 1's waiting release, which would have blocked its merge on your label. I brought the release up to date; all its tests pass. Its automatic release check re-runs on the new version tomorrow at 08:17, before bet 1's 6 November target.
- **Reliability (diagnosis):** the 10:54 shift didn't crash. It started its idea generator in the background and ended its turn to wait, and in a scheduled run that ends the job. I wrote a guard that refuses background work in scheduled shifts only, but the files it belongs in are protected from shifts, so it is with you as a ready patch (new ask, below). This shift kept all its helpers in the foreground.
- **Legal (results night, last day):** this morning's narration is reactions to the results. None of it covers voting procedure or claims fraud. The check is closed.
- **Security:** no workflow change since 20 October, no secret in the repository, money controls intact ($0.10 this month, forecast $0.74 of $3).
- AI use: no Gemini requests, no Polly, no sample video. Five fresh reviews, all foreground.

### Blocked
- **New for you:** #93, label the background-work guard `approved` (one label; it spends nothing and weakens no control). Then, as before: #77 (bet 1, by about 6 November), #82, #89, #90, #91, #92, #88, #86, #65 (still waiting on your reply), #80, #59.

### Next
- **03:17 shift:** request the sample video for the closing-line fix, and merge it on a pass. I recommend no format-version bump: like the 14 October title fix, it repairs a leak inside the capitals test, and a bump would split this version's uploads mid-test.
- **Bet 1's release:** before merging it on your label, read tomorrow's release check, which must pass on the version I pushed today.
- Carried: 6 November (#77 fallback, which I'd still not ship), 9 November zero-view re-read, 10 November Reddit terms, 16 November view-swing read, 23 November capitals read (both ways, as above).

### Better?
- **Than last shift:** yes, a little. One viewer-facing defect is fixed, and a skew in the next test read was caught before the read rather than after.
- **Than ~10 shifts ago:** no for viewers: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-04 (00:25) — Nothing was ready, and two rounds of new ideas found nothing worth doing; bet 1 still waits on your label, ideally by 6 November

    Worked (% of the shift): gm 50 · data 15 · legal 10 · audience 10 · reliability 10 · security 5

**Summary:** Nothing viewers see changed, and nothing moved the company toward revenue: everything that would waits on bet 1 (#77). You have not acted on the repository since 27 October. If bet 1 slips past 6 November, the plan set on 25 October already covers it, so there is no new ask.

### Toward revenue
- **Nothing directly**, for the reason above. The channel is flat at 12 seconds watched per view.

### Done
- **Legal (results night):** last night's narration says nothing about voting or the election.
- **Data (answered, no change):** the title-capitals test still reads on 23 November. Its smaller group should just reach the 30 uploads its rule needs by then; if not, the read waits a week.
- **Audience (answered, no change):** none of last week's 7 comments mentions the voice, AI or reposting, so nothing is added to the case for Stephen's voice alone.
- **General management (fix):** a recorded decision told the 7 November shift to re-render bet 1's sample before GitHub deletes it. The kept copy made that wrong, and a new render would change the host lines you are judging, so the instruction is withdrawn.
- **General management (ranking):** a fresh agent proposed eight ideas and I added two; two rankers, reading in opposite orders, agreed on the top four. The top two were already settled: question length does not move the share of plays past the opening (12 October), and bet 1's late-merge plan exists (25 October). I did the next two (above). Dropped: where viewers are when bet 1's tags appear (it feeds a step after bet 1's read); a tool for the one 10 November terms check; re-pulling a lost weekly snapshot (the build-machine move it guarded against has passed); last week's rise in search views (2–3% of views); re-reviewing how asks reach you (the answer, no re-ask, was known); a marker for spoken lines in the logs (two reads left). A second round, through the risks, constraints, decisions' assumptions, the screen log and the test ledger, found nothing above the bar beyond the fix above.
- **Reliability:** both 3 November uploads landed. Last night's title fell back to the Reddit question after a shock phrase was refused, as designed (2 of 17 since that guard).
- **Security:** no workflow change since 20 October, no secret in the repository, money controls intact ($0.07 this month, forecast $0.72 of $3).
- AI use: none from the upload allowance; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1, by about 6 November), #82, #89, #90, #91, #92, #88, #86, #65 (your reply to its corrected sentence), #80, #59. Nothing new.

### Next
- **Results night, last day:** read this morning's narration.
- **6 November, if #77 is unlabelled:** the one alternative a shift could ship is Stephen's voice alone. I'd wait: its lead is in plays past the opening, not watch time (+9%, inside chance), and it would push bet 1's read back about three weeks.
- 9 November: the zero-view re-read by subreddit (6 of 34 recent uploads at zero views); 10 November: Reddit's terms; 16 November: the view-swing read.

### Better?
- **Than last shift:** no. One stale instruction was withdrawn; nothing else moved.
- **Than ~10 shifts ago:** no for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---
