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

## 2026-11-11 (10:57) — The backup show is merged, switched off; the last fix for bet 1's host lines failed, so I recommended shipping bet 1 without them and built that version

    Worked (% of the shift): product 40 · strategy 30 · engineering 15 · gm 10 · security 5

**Summary:** The show we would run if Reddit's access ends in January is now in the live code, switched off, after its sample passed this morning. Bet 1's last fix for its host lines failed, so #77 now recommends shipping bet 1 without the short reactions, and that version is built and waiting on your reply.

### Toward revenue
- **Keeping uploads going after January:** the own-questions show is merged into the live code, switched off. Its sample of the code exactly as merged passed (26 seconds, playable), and a fresh review found nothing that changes today's videos. Turning it on stays your call (#90).
- **Bet 1, the product's main step toward original content:** the worked-examples fix scored 0 of 9 against a bar of 7, set before the test. Three fixes have now produced nearly the same lines, so the new model is the limit, not how we ask. I posted the result on #77 with the recommendation we committed to beforehand: ship bet 1 without the per-answer reactions, keeping the host's opening line and closing pick. That version is already built and reviewed, so a "without reactions" reply leads straight to a sample for you to watch.

### Done
- **Strategy:** brought the backup show's code up to date, read its sample (a pass), had it reviewed fresh, and merged it switched off. The review found three things that matter only once it is switched on. I fixed the two real bugs: the AI writing the title could see a slightly reworded question, and one safety-screen outcome went unlogged. A second review found nothing wrong with the fix. I also built the third: a title or closing line that names Reddit, or passes the takes off as people's, is now dropped in code, not only discouraged in the prompt. All of it merges after its own sample, and I checked it also merges cleanly into bet 1's release, with every test passing on the two together.
- **Product:** ran the worked-examples test (4 AI requests; one post hit an overload error and answered on its single retry), had it scored blind, and recorded it. Nothing ships from it. Under the rule set before the test, the host lines get no more trials until you answer #77.
- **Engineering:** built bet 1 without reactions, kept apart from bet 1's release until you choose. A fresh review found two real bugs in my first version: reactions nobody would see could still have cancelled the opening line and the closing pick. Both are fixed and tested.
- **General management:** merging the backup show stopped bet 1's release from merging cleanly into the live code. Our tracker check caught it and I fixed it within the hour (all 1,087 tests pass). I also broke the live code's tests for a few minutes with a tracker wording slip. Neither touched an upload. With nothing left ready, a fresh helper looked for small work that needs no AI allowance, sample or you, and found nothing above the bar. Its one marginal idea, attaching the switch-on change to #90 now, I dropped: your label would apply it, possibly before the backup show's fixes merge and before you have heard it. So I handed over at 11:42.
- **Security and reliability (checked):** this morning's upload landed; the money controls are intact ($0.25 this month, forecast $0.75 of $3); no secret is in the repository; the workflows are unchanged.
- AI use: 4 requests on the upload model, on a day the release check does not spend; the sample used the test model; no Polly.

### Blocked
- **For you, in order:** #77 (bet 1: reply "without reactions", or label it as it stands), #82 (register the Reddit app by 12 January), #88 (one command), #90, #65 (your "yes" to its corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **From about 23:00 UTC tonight**, when the sample limit clears: request the sample of the backup show's fixes, and merge on a pass.
- **On your "without reactions" reply:** fold that version into bet 1's release and request a spoken sample for #77.
- Tomorrow's 08:17 release check re-tests bet 1's release, because its code moved today.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** yes, a little. The backup source is in the live code, and bet 1's last open test is answered, with its next version ready. Nothing new reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-11 (00:03) — Reddit's terms are unchanged; the backup show is ready for its last check this morning, and Monday's views question can now be answered by our tools

    Worked (% of the shift): data 40 · gm 25 · legal 20 · strategy 10 · security 5

**Summary:** A night shift with no AI allowance and no sample videos, so it did the checks and preparation that need neither. Nothing reached viewers. The backup show is set for its final check after 08:00 this morning, and Reddit's terms show no change that would move our January deadline.

### Toward revenue
- **Keeping uploads going after January.** The backup show's code now matches the live code exactly, so this morning's sample tests what will actually merge. On a pass it merges switched off, the same day.
- **Reddit's terms, read late in the afternoon of the 10th, California time:** unchanged. The reminder to developers that Reddit announced for the 10th has not been reported anywhere I could find. Registering our app (#82) is still what keeps uploads going past 12 January.
- Bet 1 (#77) still waits on you; nothing tonight changes that.

### Done
- **Legal:** read Reddit's three terms pages live, and all three are unchanged. The same news reports say Reddit's feeds for news readers end on 13 November. I checked our code: we read Reddit only through its official connection, never those feeds, so uploads are unaffected. That check is now closed in our test ledger.
- **Strategy:** brought the backup show's copy of the code up to date with today's live code. All 823 tests pass, and it will merge without conflict.
- **Data (correction):** Monday's review wrote that our report on videos nobody is shown could not run without a login. It can, and I ran it. The five such videos since 15 October all went up between 15 and 26 October, and none since. Four newer ones are too young to judge until Monday. Counts only; nothing concluded.
- **Data (built, live):** Monday's question, whether our weekly view swings are real viewers or a quirk of when our figures are collected, is now one command. It refuses to answer before Monday's figures arrive, as the rule set on 26 October requires. Two fresh reviews found five problems, all fixed before merging. My first version would have called one shared dip a pattern; it now needs two. While testing it I saw the figures so far, which show one shared dip. I drew no conclusion and wrote that down where the rule lives. Reporting only, so viewers see nothing.
- **General management (ranking):** with one item ready, a fresh helper proposed eight ideas and two more ranked them, forwards and backwards. Both put the terms check and the correction near the top. The backup-show update split them, because one ranker took it for a merge. The views tool came last both ways; I built it because time remained and Monday's review needs it. A second round, aimed at money, distribution, naming and reliability, found nothing above the bar. Our distance to YouTube's bar moved from 691× to 677× short, too little to change a decision. This week's longest scheduled-upload delay was 10 hours, and a fix is already built for after bet 1. So I handed over at 00:37, 25 minutes early: everything else waits on this morning's reset, the sample limit, or you.
- **Security and reliability (checked):** both of yesterday's uploads landed, and the money controls are intact ($0.25 this month, forecast $0.75 of $3). No secret is in the repository, and nothing in the workflows has changed since yesterday's patch of yours.
- AI use: none; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1), #82 (register the Reddit app by 12 January), #88 (one command), #90, #65 (your "yes" to its corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **11 November, after 08:00 UTC:** request the backup show's sample; on a pass naming its current commit, merge it switched off. Then bet 1's worked-examples test (3 requests), blind-scored, and its rule. If the morning upload runs late, after 08:00, it shares the same AI allowance; there is room for all three, but check first.
- **16 November:** the weekly review, which now answers the view-swings question with one command.

### Better?
- **Than last shift:** about the same. The backup show is one step closer to merging, and Monday's read is ready. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
