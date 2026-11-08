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

## 2026-11-07 (23:07) — Nothing was ready and two rounds of ideas found nothing worth doing tonight; one flawed title is now set aside before the capitals test is read

    Worked (% of the shift): gm 45 · editorial 20 · data 10 · reliability 10 · security 10 · product 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: what would move it still waits on your label on bet 1 (#77) or on tomorrow's model trial. Reading our published titles found one flaw that the capitals test's read would have missed. It is now excluded, by a rule set before any result.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds. Every change to what we ship waits on bet 1, on the capitals test running to 23 November, or on tomorrow's AI allowance.

### Done
- **Editorial (read, found):** I read every title, closing line and narrated answer of the last nine uploads. One title from 5 November came out in lower case where Reddit had capitals: "Why doesn't batman just end the joker? your theories." Our 14 October fix only catches titles with no capital at all. It is 1 of about 29 titles in the test's no-capitals half since that fix, and none in the other half, so it slightly favours capitals. It joins the 11 uploads that test is already re-read without, decided from the text alone. No fix while the test runs.
- **General management (ranking):** nothing was ready. A fresh helper proposed seven ideas, and two rankers reading them in opposite orders agreed on none worth doing tonight:
  - a rule for the topic-picking experiment (its deadline was false: the experiment is switched off, so no results accumulate; the plan now says so)
  - a measure of how alike our videos are (it would only repeat what #80 already tells you: one music track on all 20 recent uploads, while clips and voices vary)
  - building the replacement question source early (it can't finish tonight, and it gets ahead of your choice in #90)
  - moving one logging change ahead of bet 1 (no sample video is possible before 05:15, and it would conflict with bet 1's release)
  - researching music (the source is already your Audio Library task) and studying quiz channels (it shapes a build that waits on #90)
- A second round, aimed only at what we ship or earn, checked each idea against the code and data first. None cleared the bar. No background clip meets the rule for retiring one. The title retry and the guard against repeat questions already exist. A subscribe ask would change the spoken closing line, and subscribers are not what holds us back; views are. Everything else waits on bet 1, the capitals test or you. So I handed over at 23:07 with nothing ready.
- **Reliability (checked):** both of today's uploads landed and nothing has failed. The model switch still combines cleanly with today's code, and all 790 tests pass. GitHub deletes three sample downloads your open asks link over the next two days, but permanent copies were made on 3 November.
- **Product (checked):** the safety screen acted on 3 of 17 posts this week, under its 15% bar, and both skips look right.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.18 this month, forecast $0.76 of $3).
- All of this was checks and one recorded flaw. None changes what we ship.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your "yes" to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- Unchanged from the last shift: **8 November, after 07:00 and an hour clear of an upload,** the two-candidate host-line trial and its rule, shipping the switch that day if 3.6 Flash wins. **9 November weekly**, and the later dates, as listed there.

### Better?
- **Than last shift:** no. One flaw that would have tilted a test's read is set aside, which is small.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

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
