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

## 2026-11-07 (00:35) — Two old login tokens sat in the public history (both dead); the build now fails on any committed credential

    Worked (% of the shift): gm 40 · security 35 · strategy 10 · reliability 10 · data 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label, and the 6 November date it asked for has passed. This shift found two old YouTube login tokens in the repository's public history, confirmed both are dead, and made the build fail if a credential is ever committed again.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds; every change that would move it waits on bet 1.
- **Bet 2's fallback is now dated.** If bet 1 has not merged by 20 November, bet 2 is expected to miss at two uploads a day. That day a shift updates #80: four a day before bet 1 then becomes bet 2's only route, against the spam-policy risk #80 describes. The choice stays yours, and the 25 October rule for judging bet 2 stands as written.

### Done
- **Security (found, no harm):** a search of the full history found two YouTube login tokens printed into a notebook's saved output in February–March 2025. Both expired within 7 days, because Google's testing mode capped them at a week; the login in use dates from 19 July 2026 or later. Neither works without the matching client secret, which was never committed. No action needed from you.
- **Security (built, live):** the tests now fail if any committed file holds a credential: GitHub, AWS, Google, Groq or Anthropic keys, Google login tokens and secrets, or private keys. The tool that cleans each shift's public record now also removes Google login tokens and whole private keys. A fresh review found it removed only a private key's first line, plus two smaller faults; all were fixed before merging. It catches a leak after it is public, not before.
- **Security (checked):** library advisories unchanged since 26 October (the image library's fix is still blocked by the video library). No workflow change since 20 October. Money controls intact ($0.15 this month, forecast $0.71 of $3).
- **General management (built, live):** the start-of-shift tracker check now also trial-merges the two branches that must land right after bet 1. On 6 November one had silently stopped merging. Both merge cleanly today. A fresh review found a test gap and two small faults; all fixed before merging.
- **Product (checked):** bet 1's release and its two follow-on branches still combine with tonight's code, new credential check included, and all 1,040 tests pass together. Your label can still merge it.
- **General management (closed):** I withdrew #86. Its own correction had found it unnecessary, and its one lasting piece is in #89, so you have one ask fewer.
- **Reliability (checked):** both 6 November uploads landed, the evening one on GitHub's new build machines, so their switch, due by 19 November, is done and harmless. The morning one went out without its separate caption track, which YouTube refused (the first since 22 September; 7 in September). The words are burned into the video, so viewers saw no difference; I built no retry.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas; two rankers reading in opposite orders put the same two first: withdrawing #86, and bet 2's dated step. Dropped:
  - a caption retry (one refusal in 45 days, and refusals like it usually repeat)
  - asking for viewers' answers in our comment (it would disturb the capitals test and bet 1's vote)
  - starting the replacement source early (dated 14 December; your label and #90 set its lead time)
  - a search-traffic measure (search brings under 2% of views)
  - re-reading YouTube's policy pages (read 3 November)
- A second round, aimed at money, audience, distribution, editorial, market, legal and finance, found nothing in those. On the security side it found that the plain music track, sealed on 10 October, can still be downloaded from the public history; no one ever took the history decision its sealing deferred. I added it, with the dead tokens, to the history question already set for the 7 December monthly, so it costs you no new ask. No viewer names, Reddit usernames beyond the public credits, or account numbers are kept in the repository.
- All of this was fixes and checks. None changes what we ship, because everything that would waits on bet 1.
- AI use: none from the upload allowance, no Polly, no sample video. No helper was left running at hand-over.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your reply to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **On your #77 label:** the title check, the usual gates, merge, then the two follow-on branches; the start-of-shift check says whether they still merge.
- **9 November weekly:** as set: the friction fixes, the zero-view re-read by subreddit, the two dropped friction items.
- **Later dates:** 10 November, Reddit's terms. 16 November, the view-swing read. 17 November, redraft the viewer replies if #89 is unlabelled. 20 November, bet 2's step above if bet 1 is unmerged. 23 November, the capitals and voice reads.

### Better?
- **Than last shift:** no for viewers. The public repository is safer: a committed credential now fails the build.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

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
- A second round, aimed at money, audience, distribution, editorial, market, legal, strategy and finance, found nothing: each idea was blocked on bet 1 or you, already dated, or already dropped. I also closed the 26 October weekly digest, which the 2 November one replaces; its findings are in the plan.
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
