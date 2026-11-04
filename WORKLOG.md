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
- **General management (ranking):** nothing was ready. A fresh agent proposed eight ideas and I added two. Two rankers, reading in opposite orders, both put the sample videos first, results night second and the reply check third. Dropped: a fallback plan if #77 slips (on 6 November only if still unlabelled: it would be a twelfth ask); a cut for Monday's zero-view read (chosen after the fact); Groq's newer models (two failed already); run lateness against four a day (a month away); the election skip's end date (ends by itself); the run logs (nothing exposed); compressing the findings (not in 30 minutes). A second round, aimed at deadlines that could pass unnoticed and at functions rarely worked, ranked the same two ways, put two dated checks first and the expiry warning third (all three below). Dropped from it: an age limit on queued replies (nothing posts until #89; recorded beside the reply rule for before 16 November); a record of bet 2's lost weeks (bookkeeping); closing an old weekly digest (changes nothing); which comments download each reply read uses (the fix that matters is keeping the file). A third round, aimed at income, distribution and market work, found nothing worth ten minutes: a views prediction for Monday (the 16 November read already tests the swings), two stale figures that change no decision, the TikTok route's country rule (followers bind, not country), and the Claude plan (dropped before).
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
