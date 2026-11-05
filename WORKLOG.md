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

## 2026-11-05 (11:30) — Doubling views this quarter now needs bet 1 by about 13–20 November; tomorrow's reason to wait on Stephen's voice is corrected

    Worked (% of the shift): gm 25 · data 30 · strategy 15 · reliability 10 · security 10 · legal 5 · audience 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label. Doubling weekly views this quarter (bet 2) now fails unless bet 1 merges by about 13–20 November. Stephen's voice may hold viewers longer than the shared voice; a test set today on newer uploads settles it on 23 November.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.
- **Bet 2's real deadline:** views over the last four weeks run about 2,760 a week. At two uploads a day that reaches about 11,000 of the 16,600 bet 2 needs. Even if four a day doubled views, about two of the quarter's last four weeks must run at four a day, so four a day must start by 14 December. Four a day can only start 24–31 days after bet 1 merges, so bet 1 must merge by about 13–20 November.

### Done
- **Data (a lead, not acted on):** last shift said that if bet 1 is still unlabelled on 6 November, the one alternative, Stephen's voice alone, should wait, because his lead was only in plays past the opening (watch time +9%, within chance). That figure was out of date. On the latest figures, his uploads are watched 35% longer (13.5 against 10.0 seconds), beyond the 20% chance gives. Within AskReddit alone, though, the gap is 26%, inside chance. I found this by looking, so it isn't evidence yet. I set a test in advance on uploads from 30 October onward, which this look could not see, to be read on 23 November. If it holds and bet 1 is still unlabelled, the next shift brings Stephen's voice to you as the alternative to waiting. It needs your hand-run sample with the real voice either way, so no shift could ship it tomorrow.
- **Reliability (measured):** uploads now start about 7 hours after their scheduled time (all seven this week over 6 hours), up from 4.6 in mid-October. At two a day nothing breaks. At four a day each run would land after the next was due. The slot logging waiting behind bet 1 already covers that.
- **Security:** a permanent copy of bet 1's waiting release now exists, so deleting its branch by accident can't lose it. No workflow change since 20 October, no secret in the repository, money controls intact ($0.11 this month, forecast $0.71 of $3).
- **Legal (checked):** of the 219 uploads the pipeline made, two contain a swear today's filters refuse: the 22 October title (already age-restricted) and one 6 August narration (1 view). So do 22 of the older readings. Those are the first candidates when you decide the old videos' fate. No new ask.
- **General management (ranking):** a fresh agent proposed eight ideas and I added two. Two rankers, reading the list in opposite orders, both put the four items above at the top. A fresh review found five small faults in my changes, all fixed before merging. Dropped:
  - updating the AI quota's reset hour for winter (already dropped 31 October: only a protected file uses it)
  - a comparison tool that splits by subreddit (it could quietly replace a pre-set rule mid-test)
  - building the Reddit replacement now (it needs AI requests and your choice on #90; 14 December stands)
  - a word limit for the product plan's findings (the audit's job)
  - a search-traffic lever (search is 2% of views)
- **Audience (checked):** the three replies waiting on your #89 label become too old to post on 17 November. After that the label would post nothing, so a shift redrafts them then. A second round of ideas, aimed at the functions not yet touched today (money, audience, distribution, editorial, market), found only this.
- Nearly all of this was checks and corrections. The voice test is the one bet-shaped piece.
- AI use: none from the upload allowance, no Polly, no sample video. All helpers ran in the foreground.

### Blocked
- **For you, in order:** #77 (bet 1, now by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #86, #65 (your reply to its corrected sentence), #80, #59. Nothing new.

### Next
- **6 November:** if #77 is still unlabelled, there is nothing to ship. Stephen's voice waits for 23 November's test and needs your sample anyway.
- **Today, around 16:15:** the release check on bet 1's latest version. GitHub runs the 08:17 job about eight hours late. Read it before any merge on your label.
- **9 November weekly:** mark the two friction fixes from 2 and 3 November as fixed, and re-read the zero-view uploads.
- **Later dates:** 10 November, Reddit's terms; 16 November, the view-swing read; 17 November, the three viewer replies waiting on #89 become too old to post, so redraft them if #89 is still unlabelled, or your label posts nothing; 23 November, the capitals read and the voice test.

### Better?
- **Than last shift:** no for viewers. The dates you are deciding against are now right.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-05 (01:05) — The plan for losing Reddit no longer stalls if you're away; the process audit is done

    Worked (% of the shift): gm 55 · strategy 15 · security 10 · reliability 10 · product 5 · data 5

**Summary:** If Reddit's January cutoff comes with your choice of replacement (#90) still open, shifts now build the recommended one, our own questions, switched off, so one label from you turns it on. Nothing viewers see changed, and the company is no closer to revenue: everything that would be waits on you, and you have not acted since 27 October.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds; bet 1 (#77) is still the step every revenue route needs.
- **Protecting the company's survival:** the replacement-source plan said shifts build "the source you chose" on 14 December, but nothing said what to do if you hadn't chosen. Uploads would have stopped on 12 January. Now the default is your recommended option, built switched off; only your label turns it on, and nothing is spent.

### Done
- **Strategy (sized):** the replacement source is about one shift of building and one sample, with or without bet 1. Your label and the extra music tracks #90 already asks for set the lead time, not the build, so 14 December stands. A fresh review caught two errors in my first sizing, both fixed before merging.
- **General management (process audit, 13 shifts since 28 October):** the process works at the margin, and your absence is what binds it. 8 of 13 shifts began with nothing ready, and about four in five things done were fixes. The two text defects viewers saw on 4 November were found by reading what we published, which no check requires; proposed as a check for any text change. The findings section of the product plan has grown 24% to about 15,000 words with no limit, carried by two monthly reviews. Proposals are recorded, not sent, while you're away.
- **Reliability (checked):** the loss of 4 November's morning shift can be prevented by a one-line setting, which our pinned Claude Code version supports. Your waiting ask (#93) does the same job, so I sent no new ask.
- **Data (answered, no change):** no topic has enough uploads in today's format for the topic-ranking test to reopen.
- **Product (checked, for bet 1's merge):** all 218 titles we have shipped come out the same through bet 1's waiting release as through today's code, so the release changes nothing about how titles are cleaned. This is the check that caught 4 November's defects. I also brought the release up to date with last night's closing-line fix: it combines cleanly, all its tests pass, and closing lines keep their capitals either way, so the capitals test isn't skewed again when bet 1 merges. I also fixed a small flaw in the release: bet 1's vote, posted as our comment, could show "i" in lower case or a stray capital after "vs.". Two fresh reviews found three regressions in my fix, all fixed before it went on the release.
- **Security:** no workflow change since 20 October, no secret in the repository, library advisories unchanged since 26 October, money controls intact ($0.10 this month, forecast $0.74 of $3).
- **General management (ranking):** a fresh agent proposed eight ideas, and two rankers reading in opposite orders both put the sizing first. Dropped: widening the shock-title guard (it would change titles while the capitals test runs), per-video traffic sources (YouTube refuses them), a comments-and-closing-lines read (too few comments), and a rule for when to give up on Shorts revenue (no other route to switch to yet).
- AI use: none from the upload allowance; no Polly; no sample video. All helpers ran in the foreground.

### Blocked
- **For you, in order:** #77 (bet 1, by about 6 November), #82, #89, #90, #91, #92, #93, #88, #86, #65 (your reply to its corrected sentence), #80, #59. Nothing new.

### Next
- **Bet 1's release:** read today's 08:17 release check; it must pass on the version pushed tonight before a merge on your label.
- 6 November: #77's fallback, Stephen's voice alone. Still wait: its lead is in plays past the opening, not watch time, and it would push bet 1's read back about three weeks. The 9 November weekly: mark the two friction fixes from 2 and 3 November as fixed, or the 24 November read fails; also the zero-view re-read. 10 November: Reddit's terms. 16 November: the view-swing read. 23 November: the capitals read.

### Better?
- **Than last shift:** no for viewers. A gap that would have stopped uploads after 12 January is closed.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** too early to say.

---
