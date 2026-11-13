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

## 2026-11-13 (19:31) — The fall in plays that get past the opening is not in anything we choose; four suspects ruled out

    Worked (% of the shift): data 60 · gm 25 · reliability 10 · security 5

**Summary:** Fewer viewers now get past each video's opening (about 40 in 100 before 19 October, 30 since). Tonight's tests show the fall is the same whatever the topic, subreddit or voice. That points at the opening itself, which bet 1 changes, or at YouTube. Nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. Plays past the opening are the units YouTube's paid tier counts, so their fall matters to every revenue route. Tonight ruled out the explanations that are ours to choose: the fall happens inside every topic and both subreddits. Bet 1 is the one ready change that touches the opening.

### Done
- **Data (a question answered: no):** does a change in our topic mix explain the fall? I set the rule and saved it before looking. The share fell from 40.6 to 30.0 in 100, and the mix of topics accounts for none of it. It fell inside each topic group. With only two topics common enough to test alone, the read is coarse.
- **Data (a question answered: no):** the same test by subreddit. Our second subreddit's share of uploads doubled over the same weeks, which made it the likeliest cause. It isn't: the share fell inside both (39 to 30, and 43 to 30). The voice mix shifted a little too. By the figures we already hold, that explains about 1 point of the 10, without touching the voice test that is still sealed.
- **Data (a question answered: too rare to matter):** are reworded repeats of earlier questions buried more often? Only 3 of 219 uploads repeat an earlier question, too few to test and too few to explain the buried uploads. Two are word-for-word repeats from July and August, from before we refused every past title.
- **Reliability (a check, all clear):** the missed-upload alarm waiting for your December bundle would not have raised a false alarm at any of the 129 scheduled shifts since 20 September, even with GitHub starting jobs hours late. It fired only on the one real miss, 6 October. Its closest call was 26.7 hours of its 28-hour window, which I noted so the check is re-run before it lands.
- **Data (a rule set for Monday's review):** whether video length, rank in the candidate list or title style explains the rise in buried uploads. Set before Monday's figures arrive, with a stricter bar because it runs three tests.
- **General management:** the code-findings list was one over its limit for several shifts. It is back at the limit: I moved a finished item's note into the code it describes. All 870 tests pass, and a fresh helper reviewed each change before it merged.
- **General management (your approvals):** I tried again to apply #88's approved text. The tool that runs shifts still refuses to edit those files, so it stays with you; the patch on the issue still applies cleanly. #65 still waits on your "yes" to its corrected sentence.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both orders agreed, and I did all four survivors in that order. Dropped: late-running jobs as a cause of buried uploads (lateness now moves with the calendar, so there is no fair comparison); pinning our build steps to exact versions (only you can land it); counting deleted Reddit posts (it needs Reddit calls); whether closing lines draw comments (no viewer has commented on the last 20 uploads). A second round at 18:57 found only the findings-list fix. It dropped: a note on an old library (live security debt, not a finished item); the sample-video reset hour (dropped 8 November, and it would not close); pre-testing library updates (done 28 October); a risk row for late jobs (already recorded); and the approval guard (a file only you can change). I found the subreddit test myself after that.
- **Security and reliability (checked):** this morning's upload landed; the evening one had not yet run by 19:05, which is normal now that GitHub starts jobs hours late. The money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret is in the repository, and the workflows are unchanged.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label; its sample, review and today's automatic check all passed), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away. Today's automatic check passed on the sampled version. Then the verdict-counting fix, then the time-slot logging, before four a day.
- **16 November, the weekly review:** read the buried-upload rule set tonight, with the weekly swings question, on that day's figures.
- **About 18 November:** the new model's 20th upload and its counts. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals test's read, if its lock opens.

### Better?
- **Than last shift:** no, not toward revenue. We now know the fall past the opening isn't in what we pick, which points the fix at the opening itself.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-13 (11:39) — Bet 1 has passed every check a shift can run; your label now ships it within about a day

    Worked (% of the shift): product 40 · gm 20 · reliability 15 · engineering 15 · data 5 · security 5

**Summary:** Bet 1, the step every revenue plan waits on, now has its sample video and a fresh review of the exact version your label (#77) ships, and neither found a problem. Only the daily automatic check is left, so your label is the only thing between bet 1 and viewers. Nothing reached viewers today.

### Toward revenue
- **Bet 1 is one label from shipping, with nothing else in the way.** Before today, a label would have started a day or more of checks. Now the sample and the review are done, and the automatic check runs this afternoon. Bet 2, doubling weekly views, needs bet 1 by about 20 November.

### Done
- **Product (sample video, PASS):** I brought bet 1's release up to date with the live code (all 1,137 tests pass) and had its sample made: 24.5 seconds, playable. It closes on the host's pick, "I raise my hand for the suffering SREs. Which answer gets your vote?" It is read aloud by a free stand-in voice, because test versions never hold our paid narrator's keys, so you can follow it by ear, as you asked on #77 in October. I first wrote on #77 that it was silent. I corrected that, and test-video reports now name the voice. Our check left out the host's note under the question, and the run skipped a health thread for the next post, both as planned. I added the link to #77 without emailing you. The video stays downloadable until 27 November.
- **Product (fresh review, no blockers):** a fresh helper read the whole release against the live code. It found no way to upload twice or lose our posting record, and the money and safety controls are unchanged. It left four small notes, which I wrote into our code-health list. The one worth knowing: on a day when several top threads are health ones, a run could find no usable post and skip an upload. That is about 1 in 400 runs, against about 1 in 1,200 today. Fixing it would cost AI requests, so it waits until a run actually misses.
- **Reliability (a check, all clear):** the new AI model's first week was to be watched for running out of its daily allowance. Its 10 uploads so far never hit any limit. Two hit Google's brief overload errors, and both still uploaded.
- **Engineering (ready for after bet 1):** two follow-on changes must go in right after bet 1. One logs which time slot each upload was meant for, which four uploads a day needs. The other fixes how bet 1's verdict counts its videos. I brought both up to date and checked that bet 1 and both of them merge into the live code cleanly, with all 1,141 tests passing.
- **General management (ranking):** a fresh helper proposed eight ideas from our data and plans, and two others ranked the survivors, forwards and reversed. Both put the allowance check first, then the follow-on changes. Dropped: an early count of the new model's over-claiming titles (its rule forbids a count before the 20th upload, about 18 November); two new data questions (the open ones wait on snapshots not yet taken; morning against evening was answered earlier); a fourth attempt at the backup show's title check (over an hour); deleting YouTube text we keep too long (yours, on 7 December); a closing line asking for subscribers (our findings say no subscriber lever reads within a quarter); posting to TikTok (new platforms are yours). Also checked: our one music track can't explain the rise in buried uploads; every upload since July used it. A narrower round at 11:30 found bet 1's side measures (above) and a line that goes stale when bet 1 merges, which the merging shift already updates. Nothing else cleared the bar, so I handed over at 11:39, 19 minutes early.
- **Data (a gap in bet 1's rules closed before any data):** two side measures in bet 1's rules, how much of each video people watch and where they leave, didn't say what bet 1 is compared with: the older format alone, or the new AI model's weeks too, as its main verdict is. Picking after the figures arrive would let us pick the answer we like. They now compare with both pooled, matching the verdict. No bet 1 video exists yet, so no result could have swayed it.
- **Security and reliability (checked):** yesterday's two uploads and this morning's landed. The money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret is in the repository, and the workflows are unchanged.
- **General management (an ask kept true):** from bet 1 on, each test video spends one request of the model that writes our real titles, which the wording #65 awaits denies. I noted it there without emailing you.
- AI use: one sample video (a free stand-in voice; a few AI requests, one from the uploads' allowance); no Polly.

### Blocked
- **For you, in order:** #77 (one label; nothing to watch, though the sample is there), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 on this afternoon's automatic check (it runs about 16:00–17:00 UTC on the sampled version). Don't update the release with the live code before then: a new version would need a fresh sample. Then merge the verdict-counting fix right away. The time-slot logging goes in after bet 1, before four a day.
- **If the automatic check can't reach Google again,** it retries the next day. That is not a failure.
- **16 November:** the weekly review. **About 18 November:** the new model's 20th upload, and the title counts set for it. **23 November:** the capitals test's read, if its lock opens.

### Better?
- **Than last shift:** yes, a little. A label on #77 no longer starts a day of checks: the sample and the review are done. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
