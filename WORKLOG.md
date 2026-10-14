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

## 2026-10-14 (16:45) — Bet 1 is one label from shipping again, and the title test no longer compares against lower-case titles

    Worked (% of the shift): product 35 · data 25 · gm 20 · market 5 · reliability 5 · security 5 · audience 5

**Summary:** Two faults that would have quietly cost us were found and fixed. Bet 1's branch had stopped merging, so your label on #74 would have met a broken step; it merges again and has a fresh passing sample. And the title-capitals test was comparing against titles shipped entirely in lower case. Nothing new reached viewers except tonight's corrected titles; #74 is still the one step that changes what they see.

### Toward revenue
- **Bet 1 is a one-step merge again.** This morning's reporting work had made bet 1's branch conflict with the live code, so "one label, then merge" was no longer true, and the trackers still said it was. I brought the branch up to date and re-sampled it: it plays, shows all four of the host's lines, and our own words are 66% of what the viewer gets. A check now runs at the start of every shift, so this can't go stale silently again.
- **The title-capitals test (bet 2's views lever) was measuring the wrong thing.** 4 of the first 5 "no capitals" titles shipped all lower case ("how to get jehovah's witnesses to leave you alone"), so the test was setting capitals against titles that look unfinished. Uploads with that look earn about half the views. Fixed from tonight's upload; the test now counts from 15 October and reads about 23 November, a week later.
- **Bet 2 is now also judged in the views YouTube's bar counts:** the share of plays that get past the opening. Written down before the data: doubling plays can't pass for progress unless the counted views double too.

### Done
- **Product (fixing):** the title fix above. A title written with no capital letter at all now ships with normal capitals; any title with a capital is left alone, so neither arm of the test changes. A fresh review found no bugs and two risks, both fixed: the reporting tool could have filed a re-capitalised title as a raw one, and abbreviations like "i.e." were being capitalised as if they ended a sentence (merged; no change to the video).
- **Product (fixing):** bet 1's branch brought current (one test file, both sides kept), checked against the two branches that follow it, and re-sampled (pass).
- **Data:** viewers rarely comment or subscribe: about one comment per seven uploads, and 11 subscribers from 33,550 views. Bet 1's vote is meant to raise both, but at its read that is about 1–2 subscribers and 3–6 comments, so I recorded now that anything under two to three times the current rate is chance. The release check now prints both pooled, with that chance figure, so the read needs no one-off analysis. Checked that YouTube doesn't count our own vote comment.
- **Data:** the background clip doesn't change the share of plays that count (within one release, 24% against 26%, well within chance), so swapping clips gets us no more counted views. Pre-committed the subreddit test's read in counted views too.
- **General management:** the last audit named one decision as overdue for re-checking (no new spending until we earn): it still holds. The rule on waiting asks fired today. Nothing of yours has moved since Saturday evening (67 hours, inside your longest gap of 76), and the plain-label ask (#75) has waited as long as #74, so the problem is that you've been away, not how the asks are worded. No re-ask. Closed #53 as replaced by #75 so it stops showing among your decided items.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.42 this month, forecast $0.87 of $3).
- **Reliability:** every upload since the last shift landed, the record of the last upload is intact, and tonight's run hasn't started yet (GitHub starts our runs 4–7 hours late).
- **Finance (for the 5 November review):** at the full bar, $33–$333 a month against the public subscription prices ($20, $100, $200): revenue above costs only on the cheapest plan or at the top of the quoted rates.
- **Market (a bounded check):** I found no report either way of on-screen text commentary passing YouTube's monetization review, and YouTube's policy page is unchanged since July 2025. A July 2026 press report (TechTimes) lists "text-to-speech narration over stock footage" among the patterns YouTube's crackdown hit. That describes our videos, with or without bet 1. One app vendor's article says a 246,000-subscriber Reddit-story channel with human narrators was demonetized in May 2026, but I could not open it to confirm. Nothing here changes a decision: this risk is already in front of you on #74.
- **Dropped after ranking** (a fresh agent proposed eight; ranked both ways): retiring the watched clip early (its rule reads on 19 October); whether politics posts get buried (4 uploads); likes per view (no decision waits on it). Fixing against improving: mostly fixing (the title test, bet 1's branch, the merge check). Improving: two written-down reads and the vote diagnostics.

### Blocked
- **For you, in order:** #74 (bet 1: a glance at four frames, then a label; by about 6 November for bet 2); #50 (four commands, checked today: they still apply to the current code and every test passes; it unblocks #65); #75 (comments, one label); #59 (account checks).

### Next
- On #74's label, merge bet 1's branch as the next version in one step (its sample names its current commit), then update the trackers.
- After 01:17 on 15 October your gap passes its longest. Change how #74 is asked only if you act on other issues while it waits.
- 19 October snapshot: the dark-morbid topic question and the watched clip's rule.

### Better?
- **Than last shift:** Slightly. Bet 1's one-step merge is real again, and bet 2's main test now measures what it set out to. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds, and bet 1 is unshipped, though built, sampled and mergeable.
- **Than ~100 shifts ago:** Too early to say.

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
