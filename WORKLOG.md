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

## 2026-10-14 (22:18) — Bet 1 as built would cut our videos by a quarter, risking a revert for length alone; the fix is built and waits on your label (#77)

    Worked (% of the shift): product 50 · data 20 · gm 15 · reliability 5 · security 5 · legal 5

**Summary:** Bet 1, our step toward revenue, had a flaw nobody had caught. It reads two answers instead of three, which would make our videos about a quarter shorter, and videos that short hold viewers a quarter less: close to the line where bet 1's own rule would undo it. I built and tested a version that keeps all three answers and asked you to choose (#77). Nothing new reached viewers.

### Toward revenue
- **Protecting bet 1 from a revert it hasn't earned.** Two answers were meant to make room for the host's spoken lines. When you turned the voice down, the lines became on-screen text that takes no time, but the third answer stayed cut. Measured on the last 40 live uploads, that makes the typical video about 17 seconds instead of 23, and uploads that short hold viewers 25% less. Bet 1's rule undoes it if watch time falls more than 13%, so a month after shipping it could be reverted for being shorter, not for what the host adds.
- **The fix is built:** all three answers, a host note on each, today's length. A fresh review found no bugs and every test passes. The trade-off, which I first overstated on #77 and corrected there: on threads with long answers our share of the words falls to about half (54% to 50% on our test post). Missing that target never undoes bet 1; it makes raising the share the next step. I recommend three answers.
- Bet 1's current version still merges into today's live code with every test passing, so either choice stays a one-step merge.

### Done
- **Product (fixing):** the finding and the three-answer build above, on its own branch so your #74 label still means what it said.
- **Data:** the latest full week reached bet 2's weekly views target (4,334 views at a week old, against about 4,150 needed), spread across uploads rather than one hit. Two earlier weeks did as much, so this is normal swing until it repeats. Watch time is still flat at 12.0 seconds.
- **Reliability:** both of today's uploads landed and the record of the last upload is intact. The safety screen has removed no answers since 7 October (15 runs, against about one run in five before). Its code and prompt are unchanged in effect and it answered every time, so this is within chance; half those runs came from the milder second subreddit.
- **Legal:** Groq's contract still bars training on what we send (its terms, revised 22 June 2026), and its free limits are unchanged, so bet 1's backup AI route stays sound. YouTube's AI-disclosure rule covers realistic content that could pass as real, and exempts AI help with scripts and titles, so a generic narrator reading posts needs no label.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.42 this month, forecast $0.87 of $3).
- **General management:** closed the weekly digest's "action needed" issue for 5 October's missed upload (GitHub's outage, diagnosed that day), and fixed a pointer in the onboarding notes that sent readers to the wrong section for the merge rules. Process note: a fix found in the evening cannot get its sample until morning, because the afternoon shift used the one render allowed per 12 hours. Recorded, not changed.
- **Ranked and dropped** (a fresh agent proposed eight; two rankers scored them in opposite orders, and the length risk led both): reading bet 1 across both subreddits to finish it sooner (2nd one way, 7th the other); a length line beside the subreddit test (longer answers are part of what that subreddit supplies, not a distortion); naming GitHub's start delays as a company risk (already tracked, and logging for four a day is built); keeping Groq-written titles apart in the title tests (needed only once bet 1 ships); pricing revenue by viewers' countries (it changes no decision). This shift was fixing, not improving: nothing new shipped.

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

## 2026-10-14 (16:45) — Bet 1 is one label from shipping again, and the title test no longer compares against lower-case titles

    Worked (% of the shift): product 35 · data 25 · gm 20 · market 5 · reliability 5 · security 5 · audience 5

**Summary:** Two faults that would have quietly cost us were found and fixed. Bet 1's branch had stopped merging, so your label on #74 would have met a broken step; it merges again and has a fresh passing sample. And the title-capitals test was comparing against titles shipped entirely in lower case. Nothing new reached viewers except tonight's corrected titles; #74 is still the one step that changes what they see.

### Toward revenue
- **Bet 1 is a one-step merge again.** This morning's reporting work had made bet 1's branch conflict with the live code, so "one label, then merge" was no longer true, and the trackers still said it was. I brought the branch up to date and re-sampled it: it plays, shows all four of the host's lines, and our own words are 66% of what the viewer gets. A check now runs at the start of every shift, so this can't go stale silently again.
- **The title-capitals test (bet 2's views lever) was measuring the wrong thing.** 4 of the first 5 "no capitals" titles shipped all lower case ("how to get jehovah's witnesses to leave you alone"), so the test was setting capitals against titles that look unfinished. Uploads with that look earn about half the views. Fixed from tonight's upload; the test now counts from 15 October and reads about 23 November, a week later.
- **Bet 2 is now also judged in the views YouTube's bar counts:** the share of plays that get past the opening. Written down before the data: doubling plays can't pass for progress unless the counted views double too.

### Done
- **Product (fixing):** the title fix above. A title written with no capital letter at all now ships with normal capitals; any title with a capital is left alone, so neither arm of the test changes. A fresh review found no bugs and two risks, both fixed: the reporting tool could have filed a re-capitalised title as a raw one, and abbreviations like "i.e." were being capitalised as if they ended a sentence (merged; no change to the video).
- **Product (fixing):** bet 1's branch brought current (one test file, both sides kept), checked against the branches that follow it, re-sampled (pass).
- **Data:** viewers rarely comment or subscribe: about one comment per seven uploads, and 11 subscribers from 33,550 views. Bet 1's vote is meant to raise both, but at its read that is about 1–2 subscribers and 3–6 comments, so I recorded now that anything under two to three times the current rate is chance. The release check now prints both pooled, with that chance figure, so the read needs no one-off analysis. YouTube doesn't count our own vote comment.
- **Data:** the background clip doesn't change the share of plays that count (within one release, 24% against 26%, well within chance), so swapping clips gets us no more counted views. Pre-committed the subreddit test's read in counted views too.
- **General management:** the last audit named one decision as overdue for re-checking (no new spending until we earn): it still holds. The rule on waiting asks fired today. Nothing of yours has moved since Saturday evening (67 hours, inside your longest gap of 76), and the plain-label ask (#75) has waited as long as #74, so the problem is that you've been away, not how the asks are worded. No re-ask. Closed #53 as replaced by #75 so it stops showing among your decided items.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.42 this month, forecast $0.87 of $3).
- **Reliability:** every upload since the last shift landed, the record of the last upload is intact, and tonight's run hasn't started yet (GitHub starts our runs 4–7 hours late).
- **Finance (for the 5 November review):** at the full bar, $33–$333 a month against the public subscription prices ($20, $100, $200): revenue above costs only on the cheapest plan or at the top of the quoted rates.
- **Market (a bounded check):** I found no report either way of on-screen text commentary passing YouTube's monetization review, and YouTube's policy page is unchanged since July 2025. A July 2026 press report (TechTimes) lists "text-to-speech narration over stock footage" among the patterns YouTube's crackdown hit. That describes our videos, with or without bet 1. One app vendor's article says a 246,000-subscriber Reddit-story channel with human narrators was demonetized in May 2026, but I could not open it to confirm. Nothing here changes a decision: this risk is already in front of you on #74.
- **Dropped after ranking** (a fresh agent proposed eight; ranked both ways): retiring the watched clip early (its rule reads on 19 October); whether politics posts get buried (4 uploads); likes per view (no decision waits on it). Mostly fixing (the title test, bet 1's branch, the merge check); improving: two written-down reads, the vote diagnostics. Handed over about 30 minutes early: nothing else cleared the bar.

### Blocked
- **For you, in order:** #74 (bet 1: a glance at four frames, then a label; by about 6 November for bet 2); #50 (four commands, checked today: they still apply to the current code and every test passes; it unblocks #65); #75 (comments, one label); #59 (account checks).

### Next
- On #74's label, merge bet 1's branch as the next version in one step (its sample names its current commit), then update the trackers.
- After 01:17 on 15 October your gap passes its longest. Change how #74 is asked only if you act on other issues while it waits.
- 19 October snapshot: the dark-morbid topic question and the watched clip's rule.
- After bet 1's read: widen the background library from 6 clips toward the 10–15 planned. Variety across videos is what YouTube's template rule looks at; doing it now would muddy bet 1's read.

### Better?
- **Than last shift:** Slightly. Bet 1's one-step merge is real again, and bet 2's main test now measures what it set out to. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds, and bet 1 is unshipped, though built, sampled and mergeable.
- **Than ~100 shifts ago:** Too early to say.
