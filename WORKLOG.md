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

## 2026-11-12 (11:58) — Bet 1 now ships on one label with nothing to watch, and the version that label ships is staged; the backup show's fixes are merged, switched off

    Worked (% of the shift): strategy 35 · product 25 · gm 20 · data 15 · security 5

**Summary:** The decision that gates every revenue step, bet 1 (#77), is rewritten so one label settles it from a phone. Tomorrow's automatic release check will test exactly the version that label ships. Nothing reached viewers, and the company is closer to revenue only once you label it.

### Toward revenue
- **Bet 1 is one label away.** The audit found you answer quick asks and pass over ones that need a watch. #77 needed a watch, a reply, then another watch. It now asks for one label, which ships bet 1 without the weak per-answer reactions, and it says in a few lines what a viewer would see change. Bet 2 needs bet 1 by about 20 November.

### Done
- **General management (#77 rewritten):** the issue now holds one ask: label it to ship bet 1 without the short reaction after each answer. Viewers would see the closing line become the host's pick ("My hand goes to the glorified lunch driver. Which ruined dream gets your vote?") and, now and then, a short host note under the question. A comment saying "sample" or "with reactions" keeps your other options open. **A correction followed at 11:45:** I had written that viewers would see nothing else new. A check of the release's code then found smaller changes. When the host's pick is dropped, the video closes on our stock line. The pause after a note is longer. The pinned comment becomes the pick. Medical threads are skipped. Narration costs a few cents a month more. The issue now lists them all.
- **Product (staged, not shipped):** the version your label ships is now the release in waiting, so tomorrow morning's automatic check tests exactly it. All 1,121 tests pass. One follow-on branch stopped merging cleanly with it, and I fixed that (1,123 pass).
- **Strategy (merged, switched off):** the backup show's fixes passed their sample at 11:15 (27 seconds, playable) and all 848 tests. A fresh review found the live show untouched. It found one fault that matters only once the backup show is on: the check that stops titles passing the AI's takes off as real people's also drops ordinary titles like "Why do people say sorry so much?". I fixed it on a separate branch. Three fresh reviews in a row each found new wordings it gets wrong, so I stopped. I recorded that a different kind of check is worth weighing before the backup show is switched on.
- **Data (a question answered: no):** I set the rule before looking. Neither video length nor the background clip explains the fall in the share of plays that get past the opening (43 to 34 per 100). Long videos trail by 28%, where chance alone gives 30%, and every clip sits inside its own chance range. So nothing we can read before 23 November explains the fall.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both put the #77 rewrite first and the split above second. Dropped: getting four uploads a day ready ahead of bet 1 (it needs a sample, and none can render until tomorrow); checking new brand names and a plan for Shorts series (both come after bet 1, by earlier decisions); stripping two characters YouTube refuses in titles (none in 2,300 so far); and working out which Claude plan we are on (the status line can't tell).
- **Security and reliability (checked):** yesterday's two uploads and this morning's landed. The money controls are intact ($0.30 this month, forecast $0.79 of $3), no secret is in the repository, and the workflows are unchanged.
- AI use: none by the shift itself; one sample video (test model, silent); no Polly.

### Blocked
- **For you, in order:** #77 (one label now), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **Tomorrow's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled, the first render the 12-hour limit allows. Then "sample" costs you no wait, and a label meets every merge check but the review.
- **If #77 is labelled:** merge on tomorrow's release check, that sample and a fresh review of the whole release.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** yes, a little. The decision that blocks revenue is now cheaper for you to make, and what it ships is staged. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-12 (02:14) — The process audit found why shifts kept re-proposing ideas they had already dropped, and fixed it; nothing reached viewers

    Worked (% of the shift): gm 75 · strategy 5 · data 10 · reliability 5 · security 5

**Summary:** The process audit, due after 16 shifts since the last one, ran this shift. Its main find: since 4 November the helpers that propose work could not see what earlier shifts had rejected, which explains most of the repeated work the last two audits complained of, and it is now fixed. Nothing reached viewers, and the company is no closer to revenue directly.

### Toward revenue
- **Nothing directly**, because every step that changes what we ship still waits on you (#77, #90). Indirectly, shift time wasted re-proposing rejected ideas is time not spent on work that could move revenue, and that waste had a mechanical cause, now removed.

### Done
- **General management (the process audit):** 16 shifts since 5 November. Half began with nothing ready, they averaged 38 of 60 minutes, and about 40 fixes and checks ran against 8 bets. One change reached viewers, the forced switch of our AI model. All 16 answered "no" to "better than ten shifts ago". The numbers agree: watch time is flat, and the share of videos nobody is shown, 14.7%, is still past its limit. Fresh reviews caught about 50 faults before merging. The sample videos and release checks passed every time and caught nothing, and the faults viewers could see were again found only by reading what we published. The rules held: no AI credit lines, no unapproved process changes, and production data was touched only by the upload job. You answered five quick asks on 10 November and passed over the five needing a watch, a direction call or your hands. That is the pattern that decides what ships.
- **General management (fixed, live):** the idea helpers read a list of what recent shifts rejected. Since 4 November shifts have written that label in a different style, so the list stopped at 3 November and about seven rejected ideas came back. The list now shows all ten recent shifts. The same reading fault showed two shifts twice in our time-by-function table and left two others out, and that is fixed too. Each fix had a fresh review: the first two reviews each caught a real flaw in my first version, and both flaws are fixed.
- **General management (one new ask, #95):** the tool that runs shifts asks every shift to add an AI credit line to each commit, which our rules forbid. Our check only catches it after the push. A one-line setting switches the request off, and your label applies it.
- **General management (a cap, then a cut):** our findings record grew by about a third in a week with no limit. It now has a word limit that can only go down. I then shortened five findings that were closed and already acted on, about 400 words, keeping each headline, and moved the limit down with them. A fresh review found nothing lost.
- **General management (ranking):** a fresh helper proposed eight ideas and two others ranked them, forwards and reversed. The top two in both orders were already settled. Bet 2's views gap is due on 20 November, and the rule for reading four new unseen videos was set on 10 November. So I did the fourth, the cap above. A per-entry length cap for this report ranked last both times and is dropped. The last idea, a way to depend less on YouTube's Shorts feed, repeats a recorded finding that every such route needs bet 1 first. With nothing above the bar left, I handed over at 02:16.
- **Strategy:** brought the backup show's fixes up to date with the live code twice, the second time at 02:13 after my own changes, and all 848 tests pass. Its sample cannot run before 07:00, when the sample job starts taking requests.
- **Data (a question, no answer yet):** the share of plays that get past the opening fell from 43 to 34 per 100. Split by topic, only three topics have enough videos, and none stands out. Split by subreddit it is within chance. Split by voice, the report tool won't show it until that test is read on 23 November, and that refusal is the answer. So it stays unexplained for now.
- **Security and reliability (checked):** both of yesterday's uploads landed. The money controls are intact ($0.25 this month, forecast $0.75 of $3). No secret is in the repository, and the workflows are unchanged. Monday's weekly figures job installs three Google libraries at whatever version is newest. Today's newest still install and set up both YouTube connections, so nothing released so far puts Monday's figures at risk.
- AI use: none on uploads; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1: reply "without reactions", or label it as it stands), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **From 07:00 UTC:** request the backup show's fixes' sample (the branch is current as of 02:13), and merge on a pass.
- **Keep shrinking the findings record:** the larger findings still feed tests that haven't been read yet. Compress each as its test is read: the capitals test on about 23 November, the new AI model on about 25 November.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** a little, in process only. The idea helpers can see what was rejected again, which removes the main source of repeated work two audits found. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, the share of videos nobody is shown is still too high, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
