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

## 2026-10-17 (08:27) — TikTok, which the plan called our nearest paying route, is far further away; bet 1's judging rule is fixed before its first upload

    Worked (% of the shift): monetization 25 · product 20 · gm 20 · data 20 · market 5 · security 5 · reliability 5

**Summary:** Bet 1 still waits on your label on #77, so nothing new reached viewers. This shift corrected the plan's claim that TikTok is the nearest paying route (its follower requirement, not its views requirement, is the hard half), and fixed how bet 1 will be judged on a measure that already reads worse, before any upload can colour the rule.

### Toward revenue
- **TikTok is close only on views.** The plan put it about 8× short on its 100,000 views a month. It also needs 10,000 followers, and we gain about one subscriber per 3,000 views (11 from 33,650 views over 90 days). At that rate 10,000 followers takes about 30 million views (17 to 60 million, since 11 is a small count). So TikTok is nearer than YouTube's lowest paying tier only if it turns viewers into followers 3 to 4 times better than YouTube does for us. No published figure says whether it does (one unsourced one puts a typical Shorts channel's subscribe rate near ten times ours). The TikTok country question for the 5 November review now carries that caveat.
- **What the Partner Program would pay:** at its bar, Shorts ads would bring roughly $33 to $330 a month (10 million counted views a quarter at the $0.01 to $0.10 per 1,000 that outside sources quote). Whether that is "revenue above costs" depends on the Claude subscription's price, which the plan does not record. Worth naming on 5 November.
- **Bet 1's "share watched" flag can no longer sink it, or be waved away, over video length.** The channel's scorecard already flags "share of each video watched" as worse, because recent posts run longer. Unwritten, that flag would either sink bet 1 or be explained away afterwards. Now written down: it never triggers a revert (your rule is watch time only), and it is read on longer videos only, against today's version over the same mix of subreddits. More than 5 points lower means viewers leave during the host's notes, bet 1 claims no watch-time gain, and fixing that comes next.

### Done
- **Monetization (improving):** the subscriber rate is now in the standard report, with its likely range and tests, so the follower half of any route, and how unsure it is, comes from the tool rather than a hand count. Reviewed fresh: no bugs.
- **Product (fixing):** bet 1's rule above. A fresh review caught three wrong claims in my first draft: one compared two different kinds of view count (it said 10×, the right figure is 3 to 4×), and one named a length window the report cannot read. All were fixed before merging. Both versions of bet 1 still merge cleanly.
- **General management:** trackers trimmed back under their limits; one stale line corrected (the backup AI that bans training on what we send was described as waiting on you; it ships with bet 1).
- **Ranked and dropped** (a fresh agent proposed eight and I added one; two rankers scored them in opposite orders and agreed on the top three, done above): per-video retention curves from the weekly job, the best idea for the flat watch time, but it needs a workflow change only you can land, and #77 should stay the one thing asking for you (for a later review); the chance of a 10,000-view hit (none of 1,054 uploads has reached 2,000, so it changes no decision); audience numbers on their own (the subscriber rate covers the one that matters); a survey of comparable channels' monetization (ads show on unpaid channels too); selling the pipeline (no sign of demand); making the upload step's last length check fail soft (it cannot be reached). A second pass (five more, ranked the same way) added one finding: no subscriber experiment can be read within a quarter, since a test arm gains about five subscribers in that time, so none may decide anything; two shifts running had proposed and dropped one. Its others: whether longer videos hold more watch time within one version (already recorded: yes, by 37%); a steadier views measure for the title-capitals test (chosen after seeing data, it invites picking the flattering one); a daily stats snapshot (needs a workflow change from you). This shift was mostly improving, with one fix.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.47 this month, forecast $0.82 of $3).
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label settles bet 1; four frames, no download); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: check that today's release check (it lands around 13:15) passed on the three-answer version, merge it as the next version, close #74, then update the trackers. If you label #74's two-answer version instead, its videos run about a quarter shorter, so before its first upload ask you whether its watch-time check should allow for length (the one ranked idea this shift left for you).
- 19 October: read the first week's viewer comments, the dark-morbid question and the watched clip's rule.
- 5 November monthly review: the TikTok question with the follower caveat above; the subscription's price against Partner Program revenue; retention curves, as a change for you to land; the weekly shift allowance's dark days.

### Better?
- **Than last shift:** Slightly, in planning rather than for viewers. A route the plan leaned toward is now priced on both halves, and bet 1 cannot be judged on a flag that measures length. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-16 (22:36) — Bet 1's recommended version now has its sample, and one label on #77 ships it; the title test's control arm no longer leaks

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
- **General management:** the tracker said viewer comments were waiting on you. You approved that on 15 October and it is applied; the first week's comments arrive after Monday's weekly run. Trackers trimmed back under their size limits.
- **Ranked and dropped** (two fresh agents proposed sixteen; three survived): your own voice as bet 1's fallback (already in front of you on #74); a format of our own questions with no Reddit text (reopens the bets you set); a 60-second length test for TikTok (changes the video while two tests run); whether this year's crackdown on AI channels could close ours (it ends in losing payment, which bet 1 already answers); which uploads bring subscribers (23 gains in all, too few to read); reading next week's comments with a set rubric (about one comment per seven uploads). The third survivor, whether your TikTok account could be based in one of TikTok's eight eligible countries, asked on #55 and never answered, goes to the 5 November review rather than a new issue now, so #77 stays the one thing asking for you. This shift was mostly fixing (bet 1's sample and ask, the title test's leak), with one improvement (the older topic labels). Handed over about 30 minutes early: the code-health list's remaining items either ship with bet 1, are deferred on purpose, or touch the same code as bet 1's branch, where a change now would cost its fresh sample.
- **Security:** standing check clean: no secrets in the project, the only workflow change is the comments one you approved, money controls in place ($0.46 this month, forecast $0.80 of $3).
- **Reliability:** all four uploads since the last shift landed, and the record of the last upload is intact. Process note: no shift worked between 14 October 22:54 and tonight because the week's shift allowance ran out. Five scheduled shifts started and stopped at the guard until it reset at 18:00 today. At three shifts a day it lasts about five and a half days, so the end of each week goes dark, and longer shifts (which #67 asks for) would widen the gap. It cost two days on bet 1's sample this time. That is your reserve working as set, so I changed nothing; worth a look at the 5 November monthly review.

### Blocked
- **For you, in order:** #77 (one label settles bet 1; four frames, no download); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: check that the 08:17 release check passed on the three-answer version, merge it as the next version, close #74, then update the trackers.
- 19 October: read the first week's viewer comments, and the weekly snapshot's items (the dark-morbid question, the watched clip's rule).
- After bet 1 merges: the run-slot log, the vote comment's capitals, then make the upload step's last length check fail soft (it would stop the run rather than drop an answer; it has never fired).
- 5 November monthly review: put the TikTok country question to you (it decides whether TikTok, the nearest paying route, stays open for bet 3), and look at the weekly shift allowance's dark days.

### Better?
- **Than last shift:** Yes, slightly. Bet 1's recommended version is sampled and asked as one label, and bet 2's title test now measures what it set out to. Nothing new reached viewers except the corrected titles.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.
