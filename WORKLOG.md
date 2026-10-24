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

## 2026-10-24 (15:30) — The swear-word fix is live, and bet 1's sample branch is ready for the next render slot

    Worked (% of the shift): reliability 45 · product 20 · gm 25 · security 10

**Summary:** The fix that stops a swear word reaching a title, like Thursday's "Alright Fuckers", passed its sample render and now runs on every upload. Bet 1's sample branch is brought up to date and waits only for the next render slot, tomorrow morning.

### Toward revenue
- **Indirectly.** The swear-word fix protects the channel rather than growing it: a sworn title risks the advertiser-friendliness the Partner Program checks. Bet 1, which every route to revenue needs, is one render from your inbox; the next slot the shift rules allow opens about 07:30 tomorrow.

### Done
- **Reliability (a fix, live):** the swear-word filter now catches a word next to a quote mark or inside a contraction, and an AI-written title, closing line or keyword with a swear word or emoji falls back to a safe one. It passed its sample render, four earlier reviews and a fresh check of how it meets today's code. It changes which posts and lines qualify, not the video, so no version change and no effect on the running tests.
- **Product:** the same guard for bet 1's spoken vote and on-screen tags is now on the release branch, so it ships with bet 1. The sample branch (that plus the grading-tag filter) takes today's code cleanly, all tests passing.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.70 this month, forecast $0.86 of $3).
- Mostly a fix. AI use: one sample render (its own test allowance); no Polly.

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **The first shift after about 07:30 UTC:** render bet 1's sample branch and, if its tags react rather than grade, post it to #77. The 12-hour limit lifts at 02:40, but its tags spend one upload-model request, so the rule of waiting for the 07:00 reset and an hour clear of the 06:23 run applies until #65 lands.
- The trial wording that drops "agreement" from the reactions it asks for: read it on about three trial posts with the upload model's allowance, after the 07:00 reset.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes, slightly. A live defect seen once in 191 uploads is closed, and bet 1's sample no longer needs any preparation before its render.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-24 (08:50) — Rewording the host's prompt made its grading worse, so a filter now removes grading tags before they reach the screen; it waits for one sample render

    Worked (% of the shift): product 50 · data 20 · gm 15 · legal 5 · reliability 5 · security 5

**Summary:** The weakness that held bet 1's sample back from you, tags that grade the answers ("Spot on", "Good point"), is not confined to advice posts, and rewording the prompt made it worse. A filter now drops the stock kind of grading tag before it reaches the screen; it waits for one sample render, and catches about 7 of every 12.

### Toward revenue
- **Bet 1 is one render closer.** Every route to revenue needs bet 1, and its last gate is you watching a sample whose tags react rather than grade. Last night's sample was held back for grading. The filter stops the stock verdicts, so the next sample should repeat your 19 October feedback far less, though not never.

### Done
- **Product (a bet, read and not kept):** last night's reworded prompt on three more trial posts, on the model uploads use, one request each. About 4 of 9 tags reacted, against about 21 of 27 for the shipped wording. Three still graded the answer ("Ah, makes sense" on a politics answer, "Sad but true", "Good point"). So grading is a general habit, and naming it in the prompt does not stop it. Not read on the other six posts: even a perfect score there would leave it only one tag ahead of what ships.
- **Product (a fix, on a branch beside the release):** a check that drops a host tag that grades its answer, leaving that answer untagged. It was built from the 9 verdicts on record. It drops none of the 27 reactions or 15 labels on record. On 62 tags it had not seen, scored blind by a fresh agent, it dropped 7, all verdicts. It let 5 of 12 verdicts through, in new wordings ("Actually helpful", "Too honest"). It also drops "Ouch, true", half a wince. A question counts as doubt, a reaction, so it ships ("Is that true?!"). A fresh review found 8 kinds of reaction it wrongly dropped and a dozen verdicts it missed. A second review found two more. All are fixed.
- **General management:** nothing was ready. A fresh agent proposed eight ideas and four survived. Two rankers, in opposite orders, put the same two on top: the filter (done) and whether the free AI could judge tags by meaning, catching what a word list misses. **Dropped:** a sample of the "our own questions" show (cannot be watched until a render, and it waits behind bet 1's); another prompt rewording (it would spend today's last safe AI requests, and the last rewording failed; it is built for tomorrow instead); asking for three opening tags in one request and showing the first that reacts (it changes what the AI returns, so not in the time left; the opening tag shows on only about 1 upload in 6–8).
- **Data (a research question, answered no):** can the free AI judge tags? The bar was set before reading: agree with the blind scores on 90% of tags and pass no verdict. It agreed on 36 of 62, and called 7 of 12 verdicts reactions, including "Sad but true" and "Direct hit", which the filter catches. The second free model's answer could not be lined up with the tags. So the filter stays, and nothing replaces it.
- **Legal (a finding, for the 5 November review):** a second round of ideas, aimed at the functions no recent shift has worked, found one. A data file in the project keeps our videos' titles and their Reddit answers, as read from YouTube, longer than the 30 days YouTube allows for anything but statistics. It is our own published text, so the risk is low. Removing it rewrites production data, which is your call, so it is recorded with a recommendation (keep the numbers, drop the text) rather than raised now.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.69 this month, forecast $0.86 of $3).
- **Process:** the idea generator first read an out-of-date list of past drops, because the working copy was on a side branch, where that list is older. It noticed and read the live copy itself; a shift asking for ideas from a branch should point it there.
- Mostly a fix, plus two reads. AI use: three requests on the upload model, 26 free Groq requests; no Polly, no render (the next render slot opens at 10:17). Handed over about 15 minutes early: the second round's one survivor is recorded, and nothing else could finish in the time left without the AI allowance tomorrow's 05:00 upload needs, or the render slot.

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **After 10:17 UTC:** as planned, render the swear-word filter branch and, on a pass naming its commit, merge it into the live branch (no version bump). It still merges cleanly into today's live code, tests passing.
- **The render slot after:** render the branch that already combines the tag filter with the vote-and-tags swear guard (all tests pass; a local silent render completes), and post the sample to #77 if its tags react. Then fold it into the release branch.
- The shipped prompt still lists "agreement" among the reactions it asks for. A trial wording without it, which names no verdicts and leaves taking sides to the vote, is ready to run. Read it on about three trial posts a day with the upload model's allowance before folding it in.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes, slightly. More than half of the defect that held the sample back is now stopped in code rather than left to the prompt, tested on every tag on record and 62 it had not seen.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
