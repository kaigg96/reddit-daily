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

## 2026-10-10 (22:32) — You approved bet 1, and it is built: a host's commentary, ready to ship after Monday's read

    Worked (% of the shift): product 40 · engineering 25 · editorial 10 · gm 10 · data 5 · legal 5 · security 5

**Summary:** You approved bet 1 on #70, so this shift built it. A host now sets up each question, reacts to the top two answers and casts the show's vote, from the AI request we already make. It is the first change aimed squarely at getting the channel paid, since YouTube does not pay for readings. It is switched off until Monday's read of the current version, and I have asked you to listen to one sample first (#71, about five minutes).

### Toward revenue
- **Yes, the most direct step yet.** YouTube refuses to pay for "readings of other materials". On tonight's sample, with real AI lines on a real post, our own words were 63% of the narration, against none today. Whether that is enough for YouTube's review is unknown until we apply. Without it, the answer is no.

### Done
- **Product (a bet):** built the commentary-led video as you approved it. The host speaks in the voice the narrator is not using, with yellow captions. The answers are still read word for word, the top two in vote order. The host's vote replaces the closing line and is posted as the channel's comment. If any host line is missing or far too long, that upload ships as today's reading, and the log records it. The log also records our own words' share for every upload. Medical threads are skipped when picking the post: that would have skipped 3 of our 168 uploads.
- **Product:** tonight's sample with commentary on passed: a playable video of 29.5 seconds on a real politics thread, a little longer than today's usual 15 to 28. Reading its captions showed two faults. The setup only restated the question ("Reddit weighs in on …"), and one reaction took a side on the issue. The prompt now forbids both. Re-tried with the sample AI on two posts (3 requests on its own allowance): both rules held, but one vote called an answer "the second one". After a rule against that, the vote ran a few words past its limit, so that upload would have been a plain reading. Your listen will show whether the AI that uploads use does the same.
- **Engineering:** two fresh reviews. The first found seven real problems, all with commentary on, and all are fixed. The worst two: a fallback upload would still have spoken the host's vote after a plain reading, and an over-long AI line could have cost an upload. The second found three small ones, also fixed. Both confirmed that with commentary off, nothing changes.
- **Engineering:** the daily release check, once this ships, fails if the host's lines are missing and prints them, so a shift can read real host lines every day without a render. Sample verdicts now show them too: that part is merged and live for the next sample.
- **Data:** the reporting tool's release read now prints bet 1's "done" test beside its verdict: how many uploads had our own words at half or more. It never triggers a revert, and it prints nothing for `v7`, so Monday's committed read is unchanged. Reviewed (its crash on a malformed value fixed) and merged.
- **General management:** closed #70. Bet 1 is marked approved in the plan, and the host-storyline experiment is folded into it. Two gaps for the release are recorded: long answers can keep our own words under half, and the length guard's fallback has never fired on a real post.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Tonight's upload carried its capitals group (none), and its title obeyed it.
- Fixing against improving: an improvement, the first change to what we ship since the capitals test.

### Blocked
- **For you, newest first:** #71, listening to one sample of bet 1 (two commands, about 2 cents of narration); the four commands on #50; the Groq key and label on #69; the planning session for bets 2 and 3 (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53; pasting #65's sentence.

### Next
- **12 October:** read `v7` under its rule, with the buried-upload check beside it. If it keeps (or reverts), merge the commentary build and release `v8` once you have listened. The release needs its own sample of the branch's current commit and a release-check pass showing the host lines. If host lines fall back on length there, raise the vote's limit by three words first.
- Then the engaged-view, narrator, dark-morbid and zero-view questions, the clip check and the first subscriber count.

### Better?
- **Than last shift:** Yes. Bet 1, the change YouTube's own wording says the channel needs to be paid at all, went from a question to a built release.
- **Than ~10 shifts ago:** Yes, though unproven. Then, bet 1 was a draft waiting on your choice of stance. Now it is approved, built and sampled. Watch time is still flat (12.0 seconds).
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-10 (16:14) — Most of the rise in buried uploads was the clip we already retired; a check on the new opening is set for Monday

    Worked (% of the shift): data 45 · gm 25 · reliability 15 · security 10 · market 5

**Summary:** Since mid-August more of our uploads have been barely shown (5 views or fewer in their first week). Most of that rise was the background clip we retired on 28 September. The rest leans toward the new opening, so I fixed the reporting tool so it can test that, and set Monday's check before seeing Monday's data. Nothing moved revenue directly. This protects Monday's verdict on the new opening.

### Toward revenue
- **Nothing directly.** Every change to what we ship is waiting on Monday's data or on you. If the new opening gets more videos buried, Monday's verdict will now show it, where before the tool would have missed it.

### Done
- **Data (research and a fix):** 15 uploads since mid-August got 5 views or fewer in a week, and 9 of them were on the retired clip. In the same week, that clip's uploads were buried 3 of 4 and the other clips' 0 of 10. So retiring it looks right, not a coincidence of timing, though the weekly groups are small. Of the rest, 3 of the new opening's 12 measured uploads were buried, against 5 of 119 before. That is suggestive but not yet beyond chance. The tool could not test a release this way at all: it compared each release only with itself and always reported no difference. Fixed, reviewed by a fresh agent (its corrections made) and merged. Monday's check is written down in advance, beside the release verdict and **never a trigger**.
- **Data:** without the clip, burying began rising a week *before* the new opening went live, and Monday's reader needs that. A small option to group uploads by week shows it. Reviewed and merged.
- **Data:** the "zero watch time" readings on a few viewed uploads are YouTube's own figures, in whole seconds, not something we store wrongly. Nothing to fix.
- **Reliability:** when both safety-check AI models are overloaded, the upload still ships, checked only by a keyword filter. The keyword filter alone has checked two uploads this month, and none was lost. The check has skipped no post since 30 September, so it is not using up material. Tonight's upload is the first to record the capitals coin, and the log adds the new column safely.
- **General management:** had six candidates ranked in a separate pass. Ran the reporting commands Monday's reads use against last week's data, and all of them run. Closed a month-old code-health item: a YouTube figure that disagrees with the others, which nothing decides on.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- **Market:** looked for real approval outcomes for AI-voiced channels that add commentary, to inform your answer on #70. Found nothing new: vendor blogs repeat YouTube's line (AI voice is allowed, interchangeable narration is not), and the only first-hand report is from 2019, before the policy was rewritten. Nothing to add to #70.
- Fixing against improving: all measurement and fixes. The one improvement viewers will see, the capitals test, goes live tonight.

### Blocked
- **For you, unchanged since this morning:** the label on #70 (bet 1's first step); the four commands on #50; the Groq key and label on #69; the planning session (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53; pasting #65's sentence.

### Next
- **12 October:** read `v7` under its rule, then the new buried-upload check beside it (remember the rise began a week before `v7`). Then the engaged-view, narrator, dark-morbid and zero-view questions, the clip check and the first subscriber count.
- After tonight's upload: check its log row carries a capitals group (1 or 0) and that the title obeys it.
- Considered and dropped: pricing the revenue routes (already in the plan, and the third bet is yours to take); a story-mode spec (waits on your bet-1 answer); the overlapping-runs workflow fix (needed only for four a day, about three weeks off, and it would be a ninth ask); a buried-upload line in the release check (Monday's new check decides whether it is worth having, and adding it before `v7`'s read would change a read already committed).
- I handed over about 40 minutes early. Nothing is ready until Monday's data or your answers, and two rounds of generating found nothing else above the bar.

### Better?
- **Than last shift:** Unclear. The video did not change. Monday's verdict can now see a cost to the new opening that it would have missed.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the capitals test, the first change aimed at views in two weeks, goes live tonight.
- **Than ~100 shifts ago:** Too early to say.
