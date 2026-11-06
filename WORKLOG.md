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

## 2026-11-06 (00:16) — The check bet 1's merge needs is now one command; the two blind tests can't be read early by accident

    Worked (% of the shift): gm 30 · product 25 · data 20 · reliability 20 · security 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label. This shift made the day you label it shorter and safer, and made sure the sample you need to watch is still there after GitHub deletes its copy on 8 November.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.
- **Your bet 1 ask now points at a sample that lasts.** Its text linked only the copy GitHub deletes on 8 November; it now links the permanent one. Its deadline line said 30 October, which has passed; it now says 13–20 November, the date bet 2 needs. Editing sends no email.

### Done
- **Product (built, live):** the check that runs every published title through today's code and bet 1's is now one command. On 4 November this check, not the tests, caught two of a fix's own mistakes, but it was rebuilt by hand each time and went wrong twice in the same ways. Today: all 220 titles come out identical. A fresh review found it was checking closing lines the way bet 1 no longer writes them and skipping two title steps; both were fixed before merging.
- **Data (built, live):** the reporting tool now refuses to read the capitals test or the voice test before 23 November, the dates set for them, unless the reader gives a reason, which it prints. Yesterday a helper read the capitals results early by accident; this stops it happening again. A fresh review found two side doors, including a title measure that matches the capitals coin on 49 of 50 uploads; both are closed.
- **Reliability (fix, live):** three tests failed falsely in one test setup. The fix sat on a parked branch; it is now live.
- **General management (fix, live):** the warning about sample videos GitHub is about to delete now says whether the link to fix is in an ask's text or only in a comment. Finding that by hand cost me time this morning.
- **Product (checked):** bet 1's release still combines cleanly with today's code, including the changes above, and all 1,025 tests pass together. Your label can merge it.
- **Reliability (fix, protects bet 2's timing):** the upload-slot logging that must merge between bet 1 and four uploads a day no longer combined with bet 1, and nothing said so; it would have cost time on the day it was needed. It is brought up to date: today's code, then bet 1, then it, combine cleanly and all 1,027 tests pass. A fresh review found nothing.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas, and two rankers reading in opposite orders put the same three first. Dropped:
  - whether four "zero-view" uploads were age-restricted (they were under three days old on 2 November's figures, so the zeros were YouTube's reporting delay; 9 November reads them properly)
  - a search tool for ideas already settled, and grouping the friction log (both the 9 November weekly's to rank)
  - preparing the removal of stored YouTube text for the 7 December decision (four weeks early)
- **Security:** no secret in the repository; the only workflow change since 20 October is the one you applied that day; money controls intact ($0.12 this month, forecast $0.72 of $3). Both 5 November uploads landed.
- All five were fixes. None changes what we ship, because everything that would waits on bet 1.
- AI use: none from the upload allowance, no Polly, no sample video. All helpers ran in the foreground.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #86, #65 (your reply to its corrected sentence), #80, #59. Nothing new.

### Next
- **On your #77 label:** the title check (now one command), the usual gates, then merge.
- **9 November weekly:** mark the two friction fixes from 2–3 November as fixed, re-read the zero-view uploads by subreddit, and rank the two friction items dropped above.
- **Later dates:** 10 November, Reddit's terms. 16 November, the view-swing read. 17 November, redraft the viewer replies if #89 is still unlabelled. 23 November, the capitals and voice reads; the reporting tool opens them that day.

### Better?
- **Than last shift:** no for viewers. Bet 1's merge day is shorter, and the two running tests can't be spoiled by accident.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-05 (19:15) — Bet 2's second target is now written down before anyone can read it; nothing else was ready

    Worked (% of the shift): gm 50 · data 20 · product 15 · security 15

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: every change that would move it still waits on your label for bet 1 (#77). This shift fixed bet 2's second target as a number, and confirmed bet 1 can still merge the moment you label it.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.

### Done
- **Data (fix):** bet 2's second measure counts only plays that get past the opening, the unit YouTube's Partner Program counts. Its rule was set on 14 October, but the number was never worked out. It is 9,412 over the quarter's last four weeks, double the 4,706 of 28 September to 25 October. It is harder than the views target: those four weeks were a typical month, while the views target was set against the weakest one. So if views pass and this misses, the cause is the starting points, not fewer viewers staying.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas, and two rankers reading in opposite orders both put the target first. A fresh review of my change found three things a later reader would misread; all were fixed before merging. Dropped:
  - a test of whether one subreddit gets buried (already set for 9 November)
  - a scan of similar channels (done 5 October, and you made a first-time viewer the test)
  - deciding now what 23 November asks you (it needs that day's capitals result)
  - a guide to re-running a failed Monday report (shifts can't start that job)
  - counting uploads advertisers avoid (at about 691 times short of the bar, it changes nothing)
- A second round, aimed at money, audience, distribution, editorial, market and legal, found only preparation for items waiting on you.
- **Data (disclosed):** the idea helper looked at the capitals test's results by accident while the test is still blind. Its sample is under the test's minimum, and I drew nothing from it. The 23 November rule stands as set, and the peek is recorded beside it.
- **Product (checked):** bet 1's release still combines cleanly with today's main code, all its tests pass, and today's automatic release check passed on its latest version. Your label can merge it.
- **Security:** no secret in the repository, no workflow change since 20 October, money controls intact ($0.12 this month, forecast $0.72 of $3). The sample videos #77 and #90 point at already have permanent copies; GitHub deletes its own on 8–9 November.
- Tonight's upload had not landed by 19:10. That is normal at today's seven-hour delay, and the next shift checks it.
- AI use: none from the upload allowance, no Polly, no sample video. All helpers ran in the foreground.

### Blocked
- **For you, in order:** #77 (bet 1, needed by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #86, #65 (your reply to its corrected sentence), #80, #59. Nothing new.

### Next
- **6 November:** if #77 is still unlabelled, nothing ships.
- **9 November weekly:** mark the two friction fixes from 2–3 November as fixed, and re-read the zero-view uploads by subreddit, as already set.
- **Later dates:** 10 November, Reddit's terms. 16 November, the view-swing read. 17 November, redraft the viewer replies if #89 is still unlabelled. 23 November, the capitals and voice reads.
- **Tooling idea, logged:** the reporting tool could warn anyone who reads a blind test's results before its date.

### Better?
- **Than last shift:** no for viewers. Bet 2 can now be judged on both its measures without anyone picking a number after the fact.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
