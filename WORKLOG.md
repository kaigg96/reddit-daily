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

## 2026-10-24 (09:05) — Rewording the host's prompt made its grading worse, so a filter now removes grading tags before they reach the screen; it waits for one sample render

    Worked (% of the shift): product 55 · data 20 · gm 15 · reliability 5 · security 5

**Summary:** The weakness that held bet 1's sample back from you, tags that grade the answers ("Spot on", "Good point"), is not confined to advice posts, and rewording the prompt made it worse. A filter now drops the stock kind of grading tag before it reaches the screen; it waits for one sample render, and catches about 7 of every 12.

### Toward revenue
- **Bet 1 is one render closer.** Every route to revenue needs bet 1, and its last gate is you watching a sample whose tags react rather than grade. Last night's sample was held back for grading. The filter stops the stock verdicts, so the next sample should repeat your 19 October feedback far less, though not never.

### Done
- **Product (a bet, read and not kept):** last night's reworded prompt on three more trial posts, on the model uploads use, one request each. About 4 of 9 tags reacted, against about 21 of 27 for the shipped wording. Three still graded the answer ("Ah, makes sense" on a politics answer, "Sad but true", "Good point"). So grading is a general habit, and naming it in the prompt does not stop it. Not read on the other six posts: even a perfect score there would leave it only one tag ahead of what ships.
- **Product (a fix, on a branch beside the release):** a check that drops a host tag that grades its answer, leaving that answer untagged. It was built from the 9 verdicts on record. It drops none of the 27 reactions or 15 labels on record. On 62 tags it had not seen, scored blind by a fresh agent, it dropped 7, all verdicts. It let 5 of 12 verdicts through, in new wordings ("Actually helpful", "Too honest"). It also drops "Ouch, true", half a wince. A question counts as doubt, a reaction, so it ships ("Is that true?!"). A fresh review found 8 kinds of reaction it wrongly dropped and a dozen verdicts it missed. A second review found two more. All are fixed.
- **General management:** nothing was ready. A fresh agent proposed eight ideas and four survived. Two rankers, in opposite orders, put the same two on top: the filter (done) and whether the free AI could judge tags by meaning, catching what a word list misses. **Dropped:** a sample of the "our own questions" show (cannot be watched until a render, and it waits behind bet 1's); another prompt rewording (it would spend today's last safe AI requests, and the last rewording failed).
- **Data (a research question, answered no):** can the free AI judge tags? The bar was set before reading: agree with the blind scores on 90% of tags and pass no verdict. It agreed on 36 of 62, and called 7 of 12 verdicts reactions, including "Sad but true" and "Direct hit", which the word check catches. The second free model's answer could not be lined up with the tags. So the word check stays, and nothing replaces it.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.69 this month, forecast $0.86 of $3).
- Mostly a fix, plus one read. AI use: three requests on the upload model, 26 free Groq requests; no Polly, no render (the next render slot opens at 10:17).

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **After 10:17 UTC:** as planned, render the swear-word filter branch and, on a pass naming its commit, merge it into the live branch (no version bump).
- **The render slot after:** fold the tag filter and the vote-and-tags swear guard into the release branch, render it, and post the sample to #77 if its tags react.
- The shipped prompt still lists "agreement" among the reactions it asks for. Removing it alone is untested. Read it on the trial posts with the next day's AI allowance before folding it in.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes, slightly. Most of the defect that held the sample back is now stopped in code rather than left to the prompt, tested on every tag on record and 62 it had not seen.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-23 (22:55) — Bet 1's first spoken sample plays, but its host tags praised the answers instead of reacting, so I held it back from you; a reworded prompt shows promise

    Worked (% of the shift): product 40 · reliability 25 · data 15 · gm 15 · security 5

**Summary:** Sample videos now speak on the build machine, and tonight's played end to end. But on tonight's post the host's three tags praised the answers ("Spot on", "Deep insight") instead of reacting to them, the weakness you flagged on 19 October. So I did not ask you to watch it. A reworded prompt fixed that post on a first try, and needs a wider check before you see a new sample.

### Toward revenue
- **Bet 1 is closer, not shipped.** Every route to revenue needs bet 1, and its last gate is you watching a narrated sample. Tonight's sample showed a gap the trials had missed. On personal advice questions ("Why does my friend act like this?"), about one upload in eight, the host grades the answers. Showing you that would have cost you a viewing to repeat your own feedback.

### Done
- **Product (a bet):** the free stand-in voice rendered on the build machine. It passed every check and is now on the release branch, so future samples speak. Your own render command is unchanged by it. The tags were "Direct hit", "Spot on" and "Deep insight", all verdicts. The first answer also only made sense with the post's body, which viewers never see. None of the nine trial posts was a personal advice question; two now are. If you want to see it anyway, the sample stays on tonight's render page for 14 days (https://github.com/kaigg96/reddit-daily/actions/runs/40032165271). It is not an ask.
- **Product (the fix, a bet):** the reworded prompt drops "agreement" from the reactions it invites and names grading as a verdict. On the upload model, one request per post: tonight's post went from 0 of 3 reactions to 2 of 3 ("Wait, what?", "Oof, direct"). A second advice post scored 2 of 3 either way. A direction, not a rate; it stays out of the release until it holds on the other nine posts.
- **Reliability (a fix, built on bet 1):** the swear-word filter now also covers the host's vote and its on-screen tags. They spare "Oh god", "Hell no" and "OMG" but refuse "Holy shit". This was the gap a review found yesterday where the filter fix meets bet 1. Reviewed; it joins the release after the filter's own render.
- **Data (a research question):** is the flat 12 seconds hiding gains at the opening? Our watch-time figure leaves out most viewers who swipe away early, so I added seconds watched per play start, swipe-aways included, and fixed the rule before reading. Across all uploads it rose from 3.7 to 5.3 seconds. Among longer videos it was flat, and the rule needed both, so **it is not a finding**: the rise may come from the mix of lengths. Reviewed and merged as a diagnostic. It never decides a revert.
- **Data:** bet 1's revert check measures total watch time in a way that runs about 2.5× YouTube's own minutes. Recounted from minutes, no past keep-or-revert decision changes, so no change is proposed.
- **General management:** nothing was ready. A fresh agent proposed eight ideas and six survived. Two rankers, in opposite orders, put the same three on top: the watch-time read and the revert check (done above), then the swear-word gap (done). **Dropped:** whether any Shorts money comes before the Partner Program (the plan already answers it); amending the rule for staying on Reddit (your #60 call covers it); a dependency audit (run: Pillow's known flaws grew, still unreachable as we never open outside images).
- **General management (second round):** the three running tests were checked against their own sizes, and none is due: the title-style test has 13 and 5 uploads of the 15 and 8 it needs, the subreddit test 7 and 9 of 15 each, the capitals test almost none. No uploads are newly buried. Handed over about 25 minutes early: nothing else was finishable without the AI allowance, which the 05:00 upload needs, or the next render slot.
- **Process:** three scheduled shifts were skipped from last night to this afternoon because the week's shift allowance ran out a day before Friday's reset. The guard worked as designed, but it is why last night's planned render waited a day.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.68 this month, forecast $0.98 of $3).
- Mostly bets, with one fix. AI use: one sample render (one upload-model request), three upload-model requests for the tag trial, four free Groq requests (the reworded prompt does not help the backup AI); no Polly. #77's description of the release branch is corrected, without an email.

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **After about 10:17 UTC tomorrow:** render the swear-word filter branch; on a pass naming its commit, merge it into the live branch (no version bump). Then fold the vote-and-tags guard into the release branch.
- **The tag check:** the reworded prompt on the other nine trial posts, upload model. The daily release check and both uploads share its allowance, so about three requests a day fit safely; it spans a few days. If it reacts at least as often as before (14 of 18, 21 October), fold it into the release, render, and post that sample to #77.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Slightly. Samples speak without you, and a tag weakness reaching about one upload in eight was found before shipping, not after.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
