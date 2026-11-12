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

## 2026-11-12 (19:28) — No theme in the questions explains why some uploads get buried; every scheduled job here runs as late as the uploads

    Worked (% of the shift): data 40 · gm 25 · reliability 15 · strategy 10 · security 5 · product 5

**Summary:** The shift started with nothing ready. It ranked eight new ideas, answered two questions from our own data, and gave the backup show's title check a fixed test. None of it changes what we ship, and nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. Tonight ruled out one suspect for the rise in buried uploads. It also showed that a fix for late-running jobs, which four uploads a day needs, has to come from outside GitHub's schedule.

### Done
- **Data (a question answered: no):** one in seven of the last three weeks' uploads is barely shown (5 views or fewer after a week), up from one in forty. I set the rule before looking. A fresh helper then tagged all 130 uploads since September against YouTube's advertiser-sensitive themes (sex, swearing, violence, politics and so on), without seeing their views. Tagged uploads were buried slightly *less* often than the rest (7 of 42 against 18 of 88), and no single theme came near the bar. So the questions' content doesn't explain it. Earlier checks ruled out pipeline faults and subreddit, and the cause is still unknown. The check is saved, so anyone can rerun it.
- **Data (dropped, my mistake):** I asked whether the fall in plays that get past the opening (43 to 34 in 100) is YouTube's doing, by reading old videos' new views. Old videos earn about 3 views a day, which our findings already said, so the test could never clear its floor (73 new views against 300). I recorded the slip and kept the code out of the live repository.
- **Reliability (a finding):** I measured each scheduled job's real start against its scheduled time over six weeks. Shifts, the morning release check and Monday's figures job all run 4–9 hours late, and all of them later since late October, just like the uploads. So the cause is GitHub's scheduler, not our upload job. Moving the upload times won't help; only a trigger from outside GitHub would, and that needs a token from you. That matters only once four a day is on the table.
- **Strategy (built, merged, switched off):** the backup show must not credit Reddit or real people in its titles. The check that stops this has been rewritten three times, and each fresh review found new wordings it got wrong. It now has a fixed set of 17 example titles that any replacement check must get right. Today's check gets 10 of them wrong, and the set says which. So when the different kind of check is built before the show goes on, it can be graded in seconds, with no AI requests.
- **General management (fixed):** the limit on open code findings was counting 12 old records of finished cleanups as open, so it read 26 of 25 when 14 were open. The easy way back under was deleting history. It now counts only the open list, and the limit dropped by the same 12, so it still asks for one finding to be closed.
- **General management (tidied):** I shortened four old, closed findings in the product's findings record by about 1,180 words. Their standing rules stayed, word for word, and the full text stays in history. The record's word limit dropped to match, so it can't grow back.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both orders put the same two first. Dropped: making the voice-only test the next release if #77 waits (that release needs you to sample the real voice, and it would push back bet 1); shrinking the findings record and fixing the approval check (neither moves revenue, and there was no time to do them well); and the case for more frequent sample videos (it is due at the 7 December review).
- **Security and reliability (checked):** this morning's upload landed, and tonight's has not run yet. The money controls are intact ($0.31 this month, forecast $0.79 of $3). No secret is in the repository, and the workflows are unchanged.
- **Your approvals #88 and #65 are still open.** #88 waits on you applying its patch, because shifts cannot write those files. #65 waits on your "yes" to its corrected sentence.
- AI use: none on uploads; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **Tomorrow's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled (the morning shift's plan stands).
- **Buried uploads:** what's left to test is YouTube's side, through the weekly figures. The 16 November snapshot reads the four newest.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** no. Two questions answered, both "no", and nothing reached viewers. The backup show is a little closer to switch-on.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-12 (11:52) — Bet 1 now ships on one label with nothing to watch, and the version that label ships is staged; the backup show's fixes are merged, switched off

    Worked (% of the shift): strategy 30 · product 30 · gm 20 · data 15 · security 5

**Summary:** The decision that gates every revenue step, bet 1 (#77), is rewritten so one label settles it from a phone. Tomorrow's automatic release check will test exactly the version that label ships. Nothing reached viewers, and the company is closer to revenue only once you label it.

### Toward revenue
- **Bet 1 is one label away.** The audit found you answer quick asks and pass over ones that need a watch. #77 needed a watch, a reply, then another watch. It now asks for one label, which ships bet 1 without the weak per-answer reactions, and it says in a few lines what a viewer would see change. Bet 2 needs bet 1 by about 20 November.

### Done
- **General management (#77 rewritten):** the issue now holds one ask: label it to ship bet 1 without the short reaction after each answer. Viewers would see the closing line become the host's pick ("My hand goes to the glorified lunch driver. Which ruined dream gets your vote?") and, now and then, a short host note under the question. A comment saying "sample" or "with reactions" keeps your other options open. **A correction followed at 11:45:** I had written that viewers would see nothing else new. A check of the release's code then found smaller changes. When the host's pick is dropped, the video closes on our stock line. The pause after a note is longer. The pinned comment becomes the pick. Health threads are skipped, more often than the plan says (below). Narration costs a few cents a month more. The issue now lists them all.
- **Product (staged, not shipped):** the version your label ships is now the release in waiting, so tomorrow morning's automatic check tests exactly it. All 1,121 tests pass. One follow-on branch stopped merging cleanly with it, and I fixed that (1,123 pass).
- **Strategy (merged, switched off):** the backup show's fixes passed their sample at 11:15 (27 seconds, playable) and all 848 tests. A fresh review found the live show untouched. It found one fault that matters only once the backup show is on: the check that stops titles passing the AI's takes off as real people's also drops ordinary titles like "Why do people say sorry so much?". I fixed it on a separate branch. Three fresh reviews in a row each found new wordings it gets wrong, so I stopped. I recorded that a different kind of check is worth weighing before the backup show is switched on.
- **Data (a question answered: no):** I set the rule before looking. Neither video length nor the background clip explains the fall in the share of plays that get past the opening (43 to 34 per 100). Long videos trail by 28%, where chance alone gives 30%, and every clip sits inside its own chance range. So nothing we can read before 23 November explains the fall.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both put the #77 rewrite first and the split above second. Dropped: getting four uploads a day ready ahead of bet 1 (it needs a sample, and none can render until tomorrow); checking new brand names and a plan for Shorts series (both come after bet 1, by earlier decisions); stripping two characters YouTube refuses in titles (none in 2,300 so far); and working out which Claude plan we are on (the status line can't tell). Later, also dropped: a fourth round on the backup show's title check (recorded instead), a better closing line for when the host's pick drops (it needs AI requests, and none may run this close to an upload), and the pick's casing in closed captions (rarely seen).
- **Security and reliability (checked):** yesterday's two uploads and this morning's landed. The money controls are intact ($0.30 this month, forecast $0.79 of $3), no secret is in the repository, and the workflows are unchanged.
- AI use: none by the shift itself; one sample video (test model, silent); no Polly.

### Blocked
- **For you, in order:** #77 (one label now), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **Tomorrow's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled, the first render the 12-hour limit allows. Then "sample" costs you no wait, and a label meets every merge check but the review.
- **If #77 is labelled:** merge on tomorrow's release check, that sample and a fresh review of the whole release.
- **Bet 1's health skip is larger than planned:** the plan says it skips 1–2 uploads in 100. By topic alone it would have skipped 5 of 84 since October and 3 of 23 this month. Bet 1's read should state the real rate beside its verdict. Whether health threads do better or worse than the rest can't be told yet: only 3 are measurable, and the report tool needs 8.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** yes, a little. The decision that blocks revenue is now cheaper for you to make, and what it ships is staged. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
