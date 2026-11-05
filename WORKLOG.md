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

## 2026-11-04 (19:30) — Two defects viewers could see were found in what we actually shipped, and both fixes are live

    Worked (% of the shift): product 30 · reliability 25 · data 20 · audience 5 · gm 10 · legal 5 · security 5

**Summary:** Reading what the channel actually published turned up two text defects, and both fixes are live. Titles that end on a quoted question no longer lose the closing quote. In the title-capitals test, the no-capitals group was also getting an all-lower-case closing line (11 of its 27 videos), which can skew that test's 23 November result; from tonight it gets proper capitals. Separately, this morning's shift lost its hour by waiting on work it had sent to the background. A guard against that needs your label.

### Toward revenue
- **Indirectly, by protecting a decision.** The capitals test decides how every future title is written. Its no-capitals group was also ending on a closing line with no capital letter in 11 of its 27 uploads, against none in the other group. Viewers saw it in our posted comment and the optional captions; the video itself shows captions in capitals, so it looked the same. That could make capitals look slightly better than they are, so the 23 November read must now give the same answer with those 11 left out. The tool to do that is built.
- **Viewer-facing fix, live:** this morning's title shipped as "3 answers to 'House and Senate are Blue, how are we feeling?", missing its closing quote. That can't happen again. It was 1 of 217 uploads.

### Done
- **Product (fix, live):** the title fix above. Before merging I replayed every published title and Reddit question through the old and new versions, which caught two of my own mistakes that the tests had missed.
- **Product (fix, live):** an all-lower-case closing line now ships with sentence capitals. Of the 151 closing lines I could recover, only those 11 change. The picture doesn't change, but the text sent to the voice does (only its capitals), so I waited for a sample video. I requested it once the hour around tonight's upload slot had passed; it passed, and I merged it with no format change, since the picture is the same.
- **Data (built, live):** the reporting tool can now leave a list of uploads out of a read. Reviewed; its one finding is fixed.
- **Reliability (fix, live):** the upload log now records each closing line as shipped. It used to exist only in run logs, which expire after 90 days; that's why this leak went four weeks unseen and took 151 logs to count. Reviewed; checked against a copy of the real log.
- **Audience (fix, live):** if you switch on replies to viewers (#89) weeks from now, replies drafted more than two weeks earlier are now refused instead of answering stale comments. This closes the gap recorded on 3 November. Reviewed.
- **General management (fix):** the new logging clashed with bet 1's waiting release, which would have blocked its merge on your label. I brought the release up to date; all its tests pass. Its automatic release check re-runs on the new version tomorrow at 08:17, before bet 1's 6 November target.
- **Reliability (diagnosis):** the 10:54 shift didn't crash. It started its idea generator in the background and ended its turn to wait, and in a scheduled run that ends the job. I wrote a guard that refuses background work in scheduled shifts only, but the files it belongs in are protected from shifts, so it is with you as a ready patch (new ask, below). This shift kept all its helpers in the foreground.
- **Legal (results night, last day):** this morning's narration is reactions to the results. None of it covers voting procedure or claims fraud. The check is closed.
- **Security:** no workflow change since 20 October, no secret in the repository, money controls intact ($0.10 this month, forecast $0.74 of $3).
- AI use: none of my own from the upload allowance; no Polly; one sample video (2–5 requests on the test model's allowance), passed. Five fresh reviews, all foreground.

### Blocked
- **New for you:** #93, label the background-work guard `approved` (one label; it spends nothing and weakens no control). Then, as before: #77 (bet 1, by about 6 November), #82, #89, #90, #91, #92, #88, #86, #65 (still waiting on your reply), #80, #59.

### Next
- **Bet 1's release:** before merging it on your label, read tomorrow's release check, which must pass on the version I pushed today.
- Carried: 6 November (#77 fallback, which I'd still not ship), 9 November zero-view re-read, 10 November Reddit terms, 16 November view-swing read, 23 November capitals read (both ways, as above).

### Better?
- **Than last shift:** yes, a little. Two viewer-facing defects are fixed, and a skew in the next test read was caught before the read rather than after.
- **Than ~10 shifts ago:** no for viewers: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

