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

## 2026-10-14 (09:40) — Bet 2 needs bet 1 merged by about 6 November; our engaged-view comparisons no longer raise false alarms

    Worked (% of the shift): data 45 · product 15 · gm 15 · reliability 10 · security 10 · finance 5

**Summary:** Nothing reached viewers: bet 1 still waits on your label (#74), and every other ready item waits on it or on uploads aging. The shift sharpened and fixed the tools that will judge bet 1, set up a fair test of the one lead the data offered, and worked out when #74's wait starts costing bet 2.

### Toward revenue
- **Nothing directly**, because bet 1, the one step that changes what viewers see, waits on your label.
- **When the wait starts to cost:** bet 2 (four uploads a day) is judged on the quarter's last four full weeks, from 30 November. Four a day switches on after bet 1's read, which needs about 24 to 31 days from its merge, not the 20 the plan said (corrected). So bet 1 merged by about 6 November keeps all four measured weeks at four a day; each week later costs one.
- **A possible free lever, tested fairly from the start:** plays of uploads read by one of our two narrators (Stephen) got past the opening more often at a week old (44% against 29%), but not at two weeks, and one gap like it in ten checks is what chance gives. So it is a lead. Its test is written down now, before the uploads it will read exist; it reads about 2 November.

### Done
- **Data:** re-read, at a common age, the finding that nothing we log changes the share of plays YouTube's bar counts: it holds in 9 of 10 checks; the tenth is the narrator lead.
- **Data (fixing):** the reporting tool's warnings beside an engaged-view comparison counted uploads from before we collected engaged views, so they named releases the comparison did not contain, and a fair comparison could have been refused. Three pre-committed reads use it (bet 1's diagnostic, both title tests). Fixed; two fresh reviews found no bugs, and their two smaller points are fixed; every result is unchanged except the warnings (merged).
- **Data (improving):** a sharper watch-time measure. YouTube reports watch time in whole seconds, so our median could only move in half-second steps and a small gain would hide. Percentage viewed times the video's length keeps the fraction (checked first against YouTube's own figure on all 162 uploads). Its first read: watch time really is flat (12.3 seconds), not an artefact of rounding, and week-to-week noise falls from about 1 second to 0.7, so a slow trend shows sooner (at two weeks old it even reads as rising, 11.7 to 12.5 seconds, which is not yet evidence). It barely sharpens head-to-head tests, so the experiments' pre-committed rules stay as written (merged; a fresh review found no bugs).
- **Reliability:** every upload since last night landed, every recent video run succeeded, and the record of the last upload is intact. The weekly snapshot job installs its libraries without fixed versions, unlike every other job; recorded to ride with the next job change you approve rather than raised alone, since it is unlikely to bite and your queue is the limit.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.41 this month, forecast $0.87 of $3). Bet 1's branch still merges cleanly, so your label stays a one-step merge.
- **Finance (for the 5 November review):** at YouTube's full bar (10 million counted views in 90 days), the rates secondary sources quote ($0.01 to $0.10 per thousand) pay about $33 to $333 a month. Whether that is revenue above costs depends on the subscription's price, which the plan does not record. So reaching the bar may still not meet the goal; the review should weigh that.
- **General management (process note):** the product plan started 3 words under its length budget, so adding one research question meant trimming three rows. Research questions are meant to be the supply that never runs dry; a full plan makes each one cost a trim. Recorded, not changed.
- **Dropped after ranking** (a fresh agent proposed eight; ranked both ways): filling 76 older uploads' topics from a saved list (its agreement with our record is circular, since the list was seeded from it, and it would change two pre-committed topic reads); recording where viewers leave each video (no keys here to check YouTube's report, and no decision waits on it); running bet 1 as a coin per upload so four a day need not wait (re-planning without new data); a policy read on four a day looking mass-produced (answered by the order: four a day waits for bet 1); shares per view as a hit predictor (an outcome against an outcome, nothing to act on); hand-reading our biggest hits (ad hoc, outside the reporting tool). Handed over about 30 minutes early because nothing else cleared the bar. Fixing against improving: about even. Fixing: the comparison warnings, the plan's timing. Improving: the sharper watch-time measure, the narrator test.

### Blocked
- **For you, in order:** #74 (bet 1: a glance at four frames, then a label; by about 6 November for bet 2); #50 (four commands; it unblocks #65); #75 (comments, one label); #59 (account checks).

### Next
- On #74's label, merge bet 1's branch as the next version in one step (its sample names its current commit), then update the trackers.
- If #74 is still open after 10:49 today, the decision log's rule on waiting asks has fired: read its evidence note, and the date above, before re-asking.
- After the 19 October snapshot: the dark-morbid topic question.

### Better?
- **Than last shift:** No closer to revenue: nothing reached viewers. The tools that will judge bet 1 are sharper and more trustworthy, the cost of #74's wait now has a date, and one free lever has a fair test.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds and bet 1 is unshipped, though fully built and sampled; views at a week old are inside their normal swing.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-13 (23:17) — Bet 1's final version plays; your label on #74 is now the only step

    Worked (% of the shift): product 25 · data 20 · reliability 20 · gm 15 · engineering 10 · security 10

**Summary:** The exact version of bet 1 that would ship was rendered tonight and plays, with all of the host's lines on screen; its four frames are on #74, so judging it takes a glance from a phone. Nothing reached viewers yet; your label ships it.

### Toward revenue
- **Bet 1, our best answer to YouTube's reused-content rule, is one label from shipping.** Tonight's sample is the final build, brought up to date with this afternoon's library fixes: it played (29 seconds), showed all three of the host's lines plus the vote, with the capitals fixed, and our own words were 44% of what the viewer gets. #74 now shows its four frames inline.
- **Four uploads a day, bet 2's lever, came closer:** the plan no longer reads as if it waits for a separate release, and its last missing piece is built (below), so it can switch on the day its read allows.

### Done
- **Product:** the sample above, and the frames on #74. Two checks a sample cannot make: the first live upload of bet 1 adds four columns to our upload record, so I replayed that on a copy (old rows intact, new row right); and bet 1's pre-committed read runs as written today, so tooling will not hold it up when its 20 uploads are in. Also made plain in the plan that four uploads a day waits only for the Groq backup, which ships inside bet 1, not for a separate release; the old wording could have cost bet 2 about two and a half weeks.
- **Data:** two pre-commitments made before any data, so later reads cannot be bent: the title tests (style B and the capitalised word) will also be read on the share of plays YouTube actually counts, since their extra views could be swipe-aways that don't count toward the bar. Today's read is too thin to say (9 against 14 uploads). Also checked whether buried uploads (5 views or fewer at a week, 13% of them) share a topic, title style or version: none does beyond chance. **Fixed a fault in the reporting tool's count of the views YouTube's bar counts:** it read every video's lifetime total as one week's gain, so it showed about 21,400 such views per 90 days; the one week actually measured supports about 9,600, in line with the plan's 11,000 to 13,000. No tracker had quoted the wrong figure, but the next read of bet 2 in those views would have (reviewed, its two risks fixed, merged). Also closed a quieter gap in the same read: a week missing one upload's reading is now held back instead of summed low (reviewed, merged).
- **Reliability:** every upload landed, including this evening's; the record of the last upload is intact; Gemini failed on 1 of the last 20 uploads. GitHub's late starts have never made two video runs collide (none in 99 runs since August; the closest were 3.5 hours apart), which matters once we post four a day.
- **Reliability, for bet 2 (four uploads a day):** built its last missing piece, on a branch behind bet 1. Each upload now records the slot it was scheduled for, and the weekly report counts it under that day and times its delay from that slot, so a run GitHub starts after midnight no longer reads as a missed day. Two fresh reviews found no bugs and two risks, both fixed: an upload started by hand would have recorded a guessed slot that looked like a scheduled one, and one hand-edited value could have stopped the weekly report. It merges after bet 1, before four a day is switched on; a sample cannot exercise it, since test renders never write the upload record. The safety screen's weekly audit is clean: one post skipped since September.
- **Engineering:** three tests failed whenever a dry run's setting was left on in the shell, which reads like a regression; fixed on the same branch, without loosening the guard that keeps tests from uploading or spending (reviewed).
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.37 this month, forecast $0.88 of $3); tonight's sample logs hold no keys.
- **General management:** your replies since 20 September fall on 15 of 24 days, with gaps of up to three days. So #74's wait is still within your normal rhythm, and the rule that fires tomorrow morning should check that before changing how asks reach you. Fixed the tracker checker, which flagged a closed issue as open for the third time in three weeks (reviewed, merged).
- **Dropped after ranking:** varying the video's template (waits for bet 1's read, as planned); a subscriber-rate metric (views, not subscribers, are what stands between us and the smaller tier); the 60-second safety stop in the upload code (never fired, and it would touch bet 1's branch). Fixing against improving: about even. Improving: bet 1 made shippable, four a day's last piece. Fixing: two faults in the reporting tool, the tracker checker, three tests.

### Blocked
- **For you, in order:** #74 (bet 1: a glance at four frames, then a label); #50 (four commands; it unblocks #65); #75 (comments, one label); #59 (account checks). Adding two or three music tracks also answers the template risk.

### Next
- On #74's label, merge bet 1's branch as the next version in one step (its sample names its current commit), then update the trackers.
- Tomorrow's 08:17 release check reads the same build; a PASS there is expected.
- Once bet 1 is live, merge the slot-recording branch (it sits on top of bet 1; tested and reviewed twice) before four a day is switched on.
- If #74 is still open at 10:49 tomorrow, read the rhythm note in the decision log before re-asking.

### Better?
- **Than last shift:** Slightly. Bet 1 went from "needs a final sample" to "needs only your label", four a day's last piece is built, and our count of the views YouTube's bar counts is now right. Nothing reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds and bet 1 is still unshipped, though it is now fully built and sampled.
- **Than ~100 shifts ago:** Too early to say.
