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

## 2026-10-16 (23:00) — Bet 1's recommended version now has its sample, and one label on #77 ships it; the title test's control arm no longer leaks

    Worked (% of the shift): product 45 · data 25 · gm 20 · security 5 · reliability 5

**Summary:** The week's shift allowance ran out on 14 October, so for two days no shift worked, and the three-answer version of bet 1 that #77 recommends still had no sample. It has one now (it plays; four frames are on #77), and a single label there settles bet 1, #74 included. Separately, the title-capitals test, bet 2's main views lever, had a leak that made a real lead harder to find; that is fixed from tonight's upload.

### Toward revenue
- **Bet 1 is one label from shipping.** You acted on the comments question on 15 October but not on bet 1. #77 then promised a sample that didn't exist yet, so there was nothing to judge. Tonight's sample of exactly the version that would ship played without a fault, and its four frames are on #77, with no download needed. One label there ships it; you no longer need to label #74. Each day bet 1 waits also delays four uploads a day, bet 2's best-evidenced views lever, which comes after bet 1's read.
- **What the sample shows, honestly:** our own words were 35% of what was read, because this thread's answers were long. Its closing vote ran past the length limit on the free AI that writes samples, so the video fell back to the usual "like and subscribe". With the vote, our share would be about 44%; reading two answers instead would give about 45%, so the third answer costs almost nothing in share here. The AI that writes real uploads kept its vote within the limit in today's release check.
- **The title-capitals test (bet 2's views lever) had a leak.** One of the nine "no capitals" titles shipped "What's YOUR unforgetable deathbed confession?", which is the other arm's treatment. Leaks like that make the roughly double views the test is looking for harder to tell from chance. The arm is now held in code. A fresh review replayed it over all 166 past titles and found none mangled; its edge cases (CPR, World War II, a title opening on a number) are fixed. The test keeps its start date, counting each upload in the arm it was given.

### Done
- **Product (fixing):** bet 1's three-answer version brought up to date with the live code, sampled, framed and re-asked as one label (above). Tomorrow's release check now tests that version, so a label can merge it straight away.
- **Product (fixing):** the title-test fix above (merged, reviewed; it changes titles, not the video).
- **Data (improving):** reports can now see topic labels for 76 older uploads that were logged without one. I wrote down the one test before running it: does the dark-morbid topic lead within the older era? The tool refused (5 uploads, fewer than the 8 it needs), so the topic picker stays parked.
- **General management:** the tracker said viewer comments were waiting on you. You approved that on 15 October and it is applied; the first week's comments arrive after Monday's weekly run. Trackers trimmed back under their size limits. Two fresh-agent passes generated candidates (data-led, then company-led); what survived is above, and the rest is listed below.
- **Security:** standing check clean: no secrets in the project, the only workflow change is the comments one you approved, money controls in place ($0.46 this month, forecast $0.80 of $3).
- **Reliability:** all four uploads since the last shift landed, and the record of the last upload is intact. Process note: no shift worked between 14 October 22:54 and tonight because the week's shift allowance ran out. Five scheduled shifts started and stopped at the guard until it reset at 18:00 today. At three shifts a day it lasts about five and a half days, so the end of each week goes dark, and longer shifts (which #67 asks for) would widen the gap. It cost two days on bet 1's sample this time. That is your reserve working as set, so I changed nothing; worth a look at the 5 November monthly review.

### Blocked
- **For you, in order:** #77 (one label settles bet 1; four frames, no download); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: check that the 08:17 release check passed on the three-answer version, merge it as the next version, close #74, then update the trackers.
- 19 October: read the first week's viewer comments, and the weekly snapshot's items (the dark-morbid question, the watched clip's rule).
- After bet 1 merges: the run-slot log, then the vote comment's capitals.

### Better?
- **Than last shift:** Yes, slightly. Bet 1's recommended version is sampled and asked as one label, and bet 2's title test now measures what it set out to. Nothing new reached viewers except the corrected titles.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-14 (22:18) — Bet 1 as built would cut our videos by a quarter, risking a revert for length alone; the fix is built and waits on your label (#77)

    Worked (% of the shift): product 50 · data 20 · gm 15 · reliability 5 · security 5 · legal 5

**Summary:** Bet 1, our step toward revenue, had a flaw nobody had caught. It reads two answers instead of three, which would make our videos about a quarter shorter, and videos that short hold viewers a quarter less: close to the line where bet 1's own rule would undo it. I built and tested a version that keeps all three answers and asked you to choose (#77). Nothing new reached viewers.

### Toward revenue
- **Protecting bet 1 from a revert it hasn't earned.** Two answers were meant to make room for the host's spoken lines. When you turned the voice down, the lines became on-screen text that takes no time, but the third answer stayed cut. Measured on the last 40 live uploads, that makes the typical video about 17 seconds instead of 23, and uploads that short hold viewers 25% less. Bet 1's rule undoes it if watch time falls more than 13%, so a month after shipping it could be reverted for being shorter, not for what the host adds.
- **The fix is built:** all three answers, a host note on each, today's length. A fresh review found no bugs and every test passes. The trade-off, which I first overstated on #77 and corrected there: on threads with long answers our share of the words falls to about half (54% to 50% on our test post). Missing that target never undoes bet 1; it makes raising the share the next step. I recommend three answers.
- Bet 1's current version still merges into today's live code with every test passing, so either choice stays a one-step merge.

### Done
- **Product (fixing):** the finding and the three-answer build above, on its own branch so your #74 label still means what it said.
- **Data (fixing):** once bet 1 ships, its backup AI can write a title when the main one fails. The two title tests can now set those titles apart without losing every upload from before the change; the obvious filter would have dropped them all. A fresh review found no bugs; its one risk is fixed (merged; no change to the video).
- **Data:** the latest full week reached bet 2's weekly views target (4,334 views at a week old, against about 4,150 needed), spread across uploads rather than one hit. Two earlier weeks did as much, so this is normal swing until it repeats. Watch time is still flat at 12.0 seconds.
- **Reliability:** both of today's uploads landed and the record of the last upload is intact. The safety screen has removed no answers since 7 October (15 runs, against about one run in five before). Its code and prompt are unchanged in effect and it answered every time, so this is within chance; half those runs came from the milder second subreddit.
- **Legal:** Groq's contract still bars training on what we send (its terms, revised 22 June 2026), and its free limits are unchanged, so bet 1's backup AI route stays sound. YouTube's AI-disclosure rule covers realistic content that could pass as real, and exempts AI help with scripts and titles, so a generic narrator reading posts needs no label.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.42 this month, forecast $0.87 of $3).
- **General management:** closed the weekly digest's "action needed" issue for 5 October's missed upload (GitHub's outage, diagnosed that day), and fixed a pointer in the onboarding notes that sent readers to the wrong section for the merge rules. Process note: a fix found in the evening cannot get its sample until morning, because the afternoon shift used the one render allowed per 12 hours. Recorded, not changed.
- **Ranked and dropped** (a fresh agent proposed eight; two rankers scored them in opposite orders, and the length risk led both): reading bet 1 across both subreddits to finish it sooner (2nd one way, 7th the other); a length line beside the subreddit test (longer answers are part of what that subreddit supplies, not a distortion); naming GitHub's start delays as a company risk (already tracked, and logging for four a day is built); pricing revenue by viewers' countries, and whether a second upload a day thins each one's views (neither changes a decision: four a day is judged on its weekly total). This shift was fixing, not improving: the only thing merged was the title-test filter. Handed over about 25 minutes early, because nothing else cleared the bar.

### Blocked
- **For you, in order:** #77, then #74 (bet 1, one label each; by about 6 November for bet 2); #50 (four commands, which unblocks #65); #75 (comments, one label); #59 (account checks).

### Next
- After 07:00 on 15 October, request the three-answer sample and post it on #77.
- On #77's label, point the next-release branch at the three-answer version. On #74's label, merge the version #77 picked as the next release, then update the trackers.
- After 01:17 on 15 October your gap passes its longest. Change how #74 is asked only if you act on other issues while it waits.
- 19 October snapshot: the dark-morbid topic question and the watched clip's rule.

### Better?
- **Than last shift:** Yes, slightly. Bet 1 was headed for a read it could fail on length alone; that is caught before any upload, and the fix is built. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds, and bet 1 is unshipped, though now in better shape to be judged fairly.
- **Than ~100 shifts ago:** Too early to say.
