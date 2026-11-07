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

## 2026-11-07 (17:20) — The backup replacement for our title-writing AI passes its title and safety checks but wrote flatter host lines; we will switch to a replacement before bet 1, on a rule set tonight

    Worked (% of the shift): reliability 55 · gm 20 · strategy 10 · data 5 · market 5 · security 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label. I tested Google's backup replacement for the AI that writes our titles and runs our safety screen a day early, on its own unused allowance. It is fast and safe, but on the one post tried it wrote flatter host lines than today's model, so tomorrow pits it against the other candidate on exactly that. When to switch, relative to bet 1, is now decided.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.
- **A risk to bet 1, found three weeks early.** From 1 December, bet 1's host lines come from whichever replacement we pick. If neither candidate reacts the way today's model does, the host gets weaker on that date whatever we do. Tomorrow's test picks the better one, and if both fall short I will tell you in #77, since it changes what you would be approving.
- **The switch goes first, whatever happens with #77.** Bet 1 needs about four weeks on its own before the next change, so a clean measurement needed it live by about 4 November. Switching first also avoids the risk that every request fails over to the backup on 1 December. If you label #77 before the switch, bet 1 waits a few days for it, not weeks. If the switch is not ready by 14 November, bet 1 goes first once you label it, and the switch follows by 28 November.

### Done
- **Reliability (tested, a day early):** the morning shift moved the rest of this test to tomorrow, but only the first candidate's allowance was used up. The backup, Gemini 3.6 Flash, has its own, and uploads never touch it. On it, a title, keywords and closing line took 2.3 seconds (the first candidate took 34). The safety screen got 5 of 5 cases right, each in 1 to 5 seconds, apart from one busy-server refusal that the built-in retry absorbed. The same check on bet 1's release passed. 8 AI requests, the shift's cap.
- **Reliability (found):** on bet 1's release, 3.6 Flash's three host lines summarised the answers ("Glass costs more", "Per day cost"). Today's model, on the same post, has reacted with most of its lines in every daily check since 27 October ("Ouch, lenses", "Two hundred dollars?!"). That is one post, so it shows a direction, not a rate.
- **Reliability (built, on test branches):** both test branches now run 3.6 Flash. The safety screen keeps a little reasoning on either candidate, as the last review asked. The switch has its own version label and a 20-video bar for its measurement. The host-line test tool now reads either candidate with one command and times each request. A fresh review found no bugs, only three wrong comments, all fixed. All tests pass on both branches. A sample video of the switch rendered and played correctly, its last routine check, so if 3.6 Flash wins tomorrow it can ship the same day. A small tool now mixes tomorrow's host lines into one shuffled sheet with the models hidden, so the scoring stays blind.
- **Data (rule set before the result):** tomorrow both candidates write host lines for the same three posts, and a fresh helper scores all 18 blind, mixed together. Whichever reacts more is adopted, and a tie goes to 3.6 Flash. If the winner reacts on fewer than 5 of its 9, I tell you in #77 (today's model reacted on about 21 of 27).
- **Strategy (rule set):** the timing above. One question goes to Monday's weekly review rather than a shift, because it changes how bet 1 is judged: whether the switch's videos may count with today's as bet 1's comparison. Without that, bet 1 approved soon after the switch would be compared with all past versions, a comparison we ruled out on 18 October.
- **Market intelligence (read):** Google lists 3.6 Flash as a fixed model it does not repoint, with no shutdown date. Its daily limit is unpublished. Today's 8 requests drew no refusal, so it is at least 8, against the 4 to 10 a day production needs. The switch's first week watches for any limit refusal.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.17 this month, forecast $0.76 of $3).
- **Reliability (checked):** this morning's upload landed, and nothing has failed since the last shift.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas, and two rankers reading the list in opposite orders put the same three first: the timing rule, the daily-limit floor and the model-name check. All three are done. Dropped:
  - a filter for summary-style host lines (its blind test needs tomorrow's lines)
  - changing bet 1's comparison now (Monday's review, as above)
  - keeping raw AI replies out of the public run log (it lands after bet 1, and is housekeeping)
  - logging why a title was refused (the log already says so)
- A second round, aimed at anything that changes what we ship or earn, found nothing above the bar. Scoring today's model blind beside tomorrow's candidates fails because its lines for those three posts are not on record, and getting them would spend the uploads' own allowance. Checking whether a past model change moved watch time fails because the model has not changed since July. So I handed over at 17:22 with nothing ready.
- All of this was fixes, tests and rules. None changes what we ship yet.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your reply to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **8 November, after 07:00 and an hour clear of an upload:** the two-candidate host-line trial (6 requests), then its rule. If 3.6 Flash wins, ship the switch that day: every check has passed. If 3.8 Flash wins, run its safety screen and title timing on a later day's allowance, then ship.
- **9 November weekly:** whether the switch's videos may count with today's as bet 1's comparison (above). Also as set before: the friction fixes, the zero-view re-read by subreddit, the two dropped friction items, and, for you through that review, a proposal that the technical-debt list's cap count only open items (12 old history notes fill it today).
- **Later dates:** 10 November, Reddit's terms. 14 November, bet 1 may go first on your label if the switch is not ready. 16 November, the view-swing read. 17 November, redraft the viewer replies if #89 is unlabelled. 20 November, bet 2's step if bet 1 is unmerged. 23 November, the capitals and voice reads. 30 November, the switch done at the latest.

### Better?
- **Than last shift:** no for viewers. The replacement is one test from ready, its timing against bet 1 is settled, and a weaker host from 1 December is known three weeks ahead.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-07 (10:08) — The replacement for our title-writing AI is half-tested: it writes well but is slow as Google ships it, so tomorrow's test runs it at its lowest thinking setting

    Worked (% of the shift): reliability 60 · product 10 · market 10 · gm 10 · data 5 · security 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label. This shift tested Google's suggested replacement for the AI that writes our titles and runs our safety screen, which Google swaps out on 1 December; tomorrow's shift finishes the test.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.
- **When to switch against bet 1 is now a real choice, set out for the next shift.** For switching first: bet 1's host lines run on the new model from 1 December whatever we do, so reading bet 1 wholly on today's model measures a setup that ends that day. Against: if the switch ships as its own version, bet 1's fair comparison needs about 20 days of it first, because our reporting tool otherwise mixes in all older versions. If that holds bet 1 past mid-November, bet 2 suffers, so the next shift weighs it with the test result.
- **The 1 December swap may not be silent.** Our calls send settings the replacement model refused in September, so every call might fail and fall to the backup, using twice the requests. Switching first avoids it either way.

### Done
- **Reliability (half tested):** Google's suggested successor, Gemini 3.8 Flash, works on our free key and has no shutdown date. It wrote a good title, keywords and closing line, but took 34 of the 60 seconds allowed, because it thinks at length unless told not to. It refuses "off", so "low" is the nearest. The safety-screen test ran past 7 minutes and I stopped it unread. I built two test branches at "low", on today's code and on bet 1's; all tests pass on both.
- **AI use, over the cap:** probably over a shift's 8 requests, up to 13, all on the candidate model, whose allowance uploads do not use. The test tool's retries caused it; the next item fixes that.
- **Reliability (built, live):** the safety-screen test now shows each case's requests and time as it finishes, and stops one request past its five cases. Before, a slow model could spend 10 requests unseen. A fresh review found that once the cap cut off later cases, the release check would have called a real wrong answer "inconclusive". Fixed before merging.
- **Market intelligence (read):** Google's pages make 3.6 Flash the backup; of its migration changes, only the thinking setting touches us.
- **Reliability (checked):** all three uploads since the last shift landed; this morning's used the Reddit question as its title, because the shock-bait guard refused the AI's, as designed. The samples your asks link are kept permanently.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.17 this month, forecast $0.76 of $3).
- **General management (ranking):** with nothing ready, a fresh helper proposed five ideas; I took four, without the usual two rankers (no time). Three corrected claims I wrote earlier today that tomorrow's timing decision relies on: the 20-day point above, the 1 December failure risk, and the test ledger's bar for title fallbacks, which had dropped "shock refusals aside" and would have tripped at today's normal rate (3 of the last 30). The fourth is the data rule below. Dropped: a new risk row for AI model changes (the plan's row and the 7 December re-read already cover it).
- **Data (rule set before the read):** the capitals test's check without its 11 flawed uploads will hold about 25 in one group, under the main read's 30. Set now, from counts only: it is read at that size against its own chance margin, and a narrow lead there extends the test once.
- All fixes and checks, apart from the forced model test. None changes what we ship yet.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your reply to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **8 November, after 07:00:** finish the successor test within 7 requests: the safety screen on one branch, the title check on both, timing every call. Any call over about 20 seconds, or an unexercised case, means trying 3.6 Flash, which can turn thinking fully down. A fresh review found no bugs; three pre-merge fixes are noted. Then, on a later allowance, check its host lines over bet 1 against your bar; decide the date.
- **9 November weekly, later dates:** as last set; the switch done by 30 November.

### Better?
- **Than last shift:** no for viewers. The forced switch is half-tested, with a working setting.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
