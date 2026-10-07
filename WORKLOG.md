# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PLAN.md](PLAN.md) (the company), [PRD.md](PRD.md) §0 (the product) and
[TECH_DEBT.md](TECH_DEBT.md) (code health).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

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

## 2026-10-07 (10:15) — Bet 1's first step is built, switched off, and can start in mid-October; our project shares a music file it shouldn't

    Worked (% of the shift): product 35 · legal 25 · data 15 · editorial 10 · gm 10 · security 5

**Summary:** Nothing in the video changed, but bet 1 got closer. I drafted three house voices for you to choose from and built the cheapest first step, switched off until you do: the host's vote replaces the closing line, adding no length or AI request, and it can start in mid-October rather than November. I also found our public project shares a music file YouTube's terms forbid sharing, and readied a two-minute fix for you.

### Toward revenue
- **Bet 1 can start three weeks sooner.** Its first step (the reaction beat) was queued behind the subreddit test, which reads around 2 November. That test, and the title test, split each day's uploads between their two sides. A change to every video hits both sides equally, so it biases neither test. Once you set the stance, bet 1 can follow v7's read on 12 October, judged on AskReddit uploads only.
- **Three house voices, tried on this week's real answers** (on the planning issue): a "show of hands" host who votes for one answer and asks the viewer to vote, a skeptic, and a warm "noticer". I recommend the show of hands, with its rule in one sentence of yours. It can replace the closing line every video already speaks ("comment your answer"), so bet 1's first step would add no length, no AI request and almost no narration cost. YouTube asks for the creator's own perspective, so the stance has to be yours.
- **The fallback source does not fit as is.** If Reddit says no, Stack Exchange is the fallback. None of its 95 popular questions across six sites had three answers short enough for our format; the typical answer is seven times too long. It could only feed a show where we condense answers in our own words. That is a rebuild, one more reason to ask Reddit early.

### Done
- **Legal:** since the project went public on 5 October, anyone can download the one YouTube Audio Library track in every upload. Its terms, as quoted by several guides, forbid offering the files apart from videos. I wrote the fix: the music is stored encrypted and unlocked only while rendering. It is yours to apply: a label, then one script on your machine. A fresh review checked it first. The stock clips' licence allows our use. A fix.
- **Product:** the topic ranker's go/no-go count came due: it would change 5 uploads in 20. A ranker that touches one upload in four cannot show up in our test unless each change gains about 50%, and the best topic edge we have measured is 12%. Parked, with the condition that reopens it. The safety screen's weekly check is clean: no post skipped this week, four answers dropped.
- **Data:** v7's videos run 3 seconds longer than any earlier version's (beyond chance), though v7 changed only on-screen text. Longer videos earn more watch time, so most of v7's +25% early lead is length; within long videos it is +8%, inside normal swings. Before the 12 October read I recorded that v7 gets credit only for gains that hold among same-length videos, and the release check now prints that comparison itself whenever a release changes video length. The keep-or-revert rule itself stands, with your total-watch-time check (#39).
- **Product:** built bet 1's first step, switched off: one setting, empty until you choose, turns the closing line into the host's vote, written from your rule. While empty, what the AI is asked is unchanged to the letter, so no video changes. It waits on a branch for its sample run (one is allowed every 12 hours; the next opens at 11:36 today). Once you set the rule, it is a release: a version bump and a real sample. A bet.
- **Data:** from Monday, the weekly statistics also record how many subscribers each upload won. Subscribers are half of YouTube's bar, and until now we had only the channel's total, so no test could say which videos earn them. Bet 1's host is the change most likely to move that. If YouTube refuses the figure, only that column is lost. Your Monday email will also flag any upload that went out without music. A bet.
- **General management:** landed the fresh-review merge step you approved (#61) and closed it. This morning's upload ran on the new Python and credited every Reddit user by name, so both of yesterday's changes are confirmed live; trackers updated.
- **Security:** standing check clean. $0.20 spent this month, no secrets in the project, and the only workflow change was your Python patch.
- Fixing against improving: two fixes (the music licence, the length reading); the rest improved bet 1's path and the plan's evidence.
- **Friction:** a shift cannot read YouTube's data from here, so checking a description meant reading the public page.

### Blocked
- **For you, in order of what they unblock:** the planning session (#55; it gates bet 1, and now has three voices to pick from); asking Reddit (#60); the music fix (#64, new; a label and a two-minute script); Gemini's paid tier (#62); the account checks (#59, about 15 minutes); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Tonight: check the first NoStupidQuestions upload lands with a title.
- After 11:36: request the sample run for the switched-off vote, and merge it on a pass with its review.
- 12 October: read v7 under its rule, with the same-length read beside it; then the engaged-view, narrator and dark-morbid questions and the first subscriber count.
- Once you apply the music fix and run the script: confirm the next upload's log shows the track, not "none".
- If you set the stance: build the reaction beat to follow v7's read. Its spec is now current.
- Considered and not taken: tracing why v7's posts run longer (it would not change the 12 October reading), and preparing Gemini's paid tier (nothing to prepare until you decide).

### Better?
- **Than last shift:** Slightly. Bet 1's start moved from November to mid-October, pending your stance, and a licence breach has a ready fix. Nothing we ship changed.
- **Than ~10 shifts ago:** Somewhat. We know the legal ground for the format and its fallback first-hand, and the experiments are honest about what they can detect. Views per upload have not moved, and watch time reads flat.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-06 (23:04) — Bet 1 needs your point of view more than a voice; the AI service we use for free breaks Reddit's terms

    Worked (% of the shift): legal 30 · engineering 25 · data 15 · editorial 10 · distribution 10 · gm 5 · security 5

**Summary:** Nothing in the video changed; descriptions now credit Reddit's users. I read four sets of rules first-hand. They changed what bet 1 needs and found a breach of Reddit's terms that a few dollars a month would fix. Both are with you, with recommendations. The overdue Python upgrade turns out not to change the video, so it needs one approval and no test slot.

### Toward revenue
- **Bet 1, sharpened.** YouTube's policy page, read directly for the first time, does not ask for a human voice. It refuses AI-written content from "generic or unoriginal templates" that lacks "the creator's original, authentic insights or perspective". A quip from a fixed prompt may not pass. A house stance that you set, which the AI writes from, is the cheapest step that fits the wording. A newer rule also bars AI hosts from giving advice on health, law, money or politics, the topics of about a third of our uploads. So the commentary must judge, never advise. Both points are in the plan's specs and on the planning issue.
- **A breach we can close.** Reddit's terms forbid letting anyone "acting on your behalf" train AI on its posts. Gemini's free allowance, which reads every post we consider, is used to improve Google's models; the paid tier is not. I recommend the paid tier, about $1–3 a month with a daily cap set at Google, before anyone writes to Reddit. It also lifts the 20-a-day limit that blocks the topic ranker.
- **The fallback source is real.** Stack Exchange licenses its posts for commercial reuse with changes allowed, on three conditions: credit every author, release our videos under the same licence, and keep its text out of AI training (the paid tier covers that).

### Done
- **Legal:** read the terms of Reddit, Stack Exchange, Google's Gemini and YouTube's monetization page directly, and sent the results to you (two new notes on existing issues, one new decision).
- **Legal:** merged crediting each Reddit user by name in the description, as Reddit's terms ask beside the link we already give; deleted and offensive names are left out. Its sample run passed, crediting a real asker. A fresh second review caught that it would have broken our topic analysis; fixed before merging. Description only.
- **Engineering:** rendered the fixed sample video on the old and new Python. The files are byte-for-byte identical, and every test passes on both. Python 3.10 lost security support on 4 October. The upgrade is ready for you as one patch. A fix.
- **Data:** one background clip is watched for burying uploads (3 of 13), with no written rule for dropping it. I set one before its next read: drop it if its rate stands out from the other clips beyond chance, corrected for testing seven at once. The report now prints that test; it flags the clip dropped in September. The watched clip stays; re-read 12 October. I refined the test once after seeing a first number (a dropped clip still counted in the comparison); the decision is the same either way. A fix.
- **Distribution:** a browser on our runner now opens Meta's pages, but their rule lists stay empty unless logged in. Facebook and Instagram stay with you.
- **Security:** standing check clean: $0.19 spent this month, no secrets in the project, and the only workflow change today was your approved fix.
- **General management:** the ready queue was empty. Two rounds of candidates; I took the six that could move now. One had been answered in September (question length); I caught it before re-running it. Trackers updated, including a stale "250 to 1,250 times short" figure.
- Fixing against improving: three fixes (the runtime, the clip rule, crediting users); the rest improved the map for bet 1 and the Reddit decision.
- **Friction:** answered research questions leave the table, so nothing stops a shift from regenerating one. Searching the findings first caught it this time.

### Blocked
- **For you:** turning on Gemini billing (#62, new); the Python upgrade patch (#63, new); asking Reddit (#60); the planning session (#55), where the question is now whose perspective the commentary carries; the account checks (#59); the review-step proposal (#61); re-running the comments change (#53); the auto-apply patch (#50). Also the old music task: every upload uses one track, and YouTube's template rule now gives that a reason. Two or three Audio Library tracks would do.

### Next
- Check tomorrow morning's description credits its authors.
- Tomorrow morning: confirm the upload landed, then read the topic ranker's count at its 20th run, under its rule.
- Tomorrow evening: the first NoStupidQuestions upload. Check it lands with a title.
- If you apply the Python patch: one sample run of the live code before the next upload, then fix the setup line in the readme.
- 12 October: judge "open on the question" under its rule, with the engaged-view, narrator and subscriber reads beside it. Apply the new clip rule to the watched clip.
- Considered and not taken: building the reaction beat now (it should wait for your stance), and re-reading engaged views by background clip. The dip from late August to mid-September shows on every clip, and the current releases are back up.

### Better?
- **Than last shift:** Slightly. Bet 1's real requirement is clearer, and a live breach has a cheap fix on the table. Only descriptions changed in what we ship.
- **Than ~10 shifts ago:** Somewhat. We now have first-hand rules for YouTube, Reddit, TikTok, Stack Exchange and Gemini. Views per upload have not moved, and watch time reads flat.
- **Than ~100 shifts ago:** Too early to say.
