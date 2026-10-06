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

## 2026-10-06 (23:04) — Bet 1 needs your point of view more than a voice; the AI service we use for free breaks Reddit's terms

    Worked (% of the shift): legal 35 · engineering 25 · editorial 15 · distribution 10 · gm 10 · security 5

**Summary:** Nothing shipped. I read four sets of rules first-hand. They changed what bet 1 needs and found a breach of Reddit's terms that a few dollars a month would fix. Both are with you, with recommendations. The overdue Python upgrade turns out not to change the video, so it needs one approval and no test slot.

### Toward revenue
- **Bet 1, sharpened.** YouTube's policy page, read directly for the first time, does not ask for a human voice. It refuses AI-written content from "generic or unoriginal templates" that lacks "the creator's original, authentic insights or perspective". A quip from a fixed prompt may not pass. A house stance that you set, which the AI writes from, is the cheapest step that fits the wording. A newer rule also bars AI hosts from giving advice on health, law, money or politics, the topics of about a third of our uploads. So the commentary must judge, never advise. Both points are in the plan's specs and on the planning issue.
- **A breach we can close.** Reddit's terms forbid letting anyone "acting on your behalf" train AI on its posts. Gemini's free allowance, which reads every post we consider, is used to improve Google's models; the paid tier is not. I recommend the paid tier, about $1–3 a month with a daily cap set at Google, before anyone writes to Reddit. It also lifts the 20-a-day limit that blocks the topic ranker.
- **The fallback source is real.** Stack Exchange licenses its posts for commercial reuse with changes allowed, on three conditions: credit every author, release our videos under the same licence, and keep its text out of AI training (the paid tier covers that).

### Done
- **Legal:** read the terms of Reddit, Stack Exchange, Google's Gemini and YouTube's monetization page directly, and sent the results to you (two new notes on existing issues, one new decision).
- **Engineering:** rendered the fixed sample video on the old and new Python. The files are byte-for-byte identical, and every test passes on both. Python 3.10 lost security support on 4 October. The upgrade is ready for you as one patch. A fix.
- **Distribution:** a browser on our runner now opens Meta's pages, but their rule lists stay empty unless logged in. Facebook and Instagram stay with you.
- **Security:** standing check clean: $0.19 spent this month, no secrets in the project, and the only workflow change today was your approved fix.
- **General management:** the ready queue was empty. I ranked six new candidates and took the four that could move now. One had been answered in September (question length); I caught it before re-running it. Trackers updated, including a stale "250 to 1,250 times short" figure.
- Fixing against improving: one fix (the runtime); the rest improved the map for bet 1 and the Reddit decision.
- **Friction:** answered research questions leave the table, so nothing stops a shift from regenerating one. Searching the findings first caught it this time.

### Blocked
- **For you:** turning on Gemini billing (#62, new); the Python upgrade patch (#63, new); asking Reddit (#60); the planning session (#55), where the question is now whose perspective the commentary carries; the account checks (#59); the review-step proposal (#61); re-running the comments change (#53); the auto-apply patch (#50). Also the old music task: every upload uses one track, and YouTube's template rule now gives that a reason. Two or three Audio Library tracks would do.

### Next
- Tomorrow morning: confirm the upload landed, then read the topic ranker's count at its 20th run, under its rule.
- Tomorrow evening: the first NoStupidQuestions upload. Check it lands with a title.
- If you apply the Python patch: one sample run of the live code before the next upload, then fix the setup line in the readme.
- 12 October: judge "open on the question" under its rule, with the engaged-view, narrator and subscriber reads beside it.
- Considered and not taken: building the reaction beat now (it should wait for your stance), and re-reading engaged views by background clip. The dip from late August to mid-September shows on every clip, and the current releases are back up.

### Better?
- **Than last shift:** Slightly. Bet 1's real requirement is clearer, and a live breach has a cheap fix on the table. Nothing changed in what we ship.
- **Than ~10 shifts ago:** Somewhat. We now have first-hand rules for YouTube, Reddit, TikTok, Stack Exchange and Gemini. Views per upload have not moved, and watch time reads flat.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-06 (17:11) — We are about 800 times short of YouTube's bar, not 300; Reddit's own terms say our use needs its agreement

    Worked (% of the shift): data 30 · legal 15 · security 15 · product 10 · reliability 10 · distribution 10 · gm 5 · engineering 5

**Summary:** Two facts changed the company's picture; both are with you, with recommendations. YouTube's bar counts only "engaged" views, about a third of our plays, so we are about 800 times short, not 300. Reddit's own terms, read first-hand for the first time, say making money from its posts needs Reddit's written agreement. Read plainly, they leave even today's unpaid videos outside the licence.

### Toward revenue
- Nothing moved revenue directly; this shift corrected the map the bets rest on.
- **The gap is wider than we thought.** YouTube counts a view whenever a Short starts playing, but the 10-million bar counts only "engaged" views, and only 36% of ours are, so we earn about 11,000 to 13,000 of the views that count per 90 days, roughly 800 times short. I recommended on the planning issue that bet 2 ("double weekly views") be measured in engaged views, so a change that wins only swipe-past plays cannot pass it.
- **Reddit's terms are now first-hand.** Earning from Reddit content needs "express written approval from Reddit" and "a separate agreement". Its newer terms (September 2024) go further: any use "by or on behalf of a business" needs written approval, paid or not. The licence covers showing posts inside our own app, unmodified. Republishing them as YouTube videos sits outside a plain reading. I recommend asking Reddit now, before the quarter is committed to this format; the answer decides whether any of the three bets has a future. Nothing changes in production meanwhile. If Reddit says no, Stack Exchange is a fallback: its users' posts are licensed for reuse, commercial use included, with credit and the same licence passed on (its terms, updated November 2025).
- **TikTok's own page adds a rule:** the account must be based in one of eight countries (US, UK, Germany, Japan, South Korea, France, Mexico, Brazil). If you are not, bet 3's TikTok pilot is closed.

### Done
- **Reliability:** last night's evening upload never happened. GitHub could not give the job a machine during its outage, so the run failed before any of our code ran, and neither of today's earlier shifts noticed it. Nothing of ours to fix; Monday's digest will list the missed day. GitHub's machines move to a newer Ubuntu on 19 October; I checked our video job is unaffected. Separately, your Monday digest now carries the keep-or-revert verdict for the current and previous release, each at the size its rule committed to. So the opening test's verdict reaches your email from 12 October even if no shift remembers. A fix.
- **Data:** built the engaged-view measure, with tests. Our "You…" titles keep their lead in engaged views (+60%), so that change counts toward the bar. No trait we log moves the engaged share: title style, voice, length and time of day all sit between 0.29 and 0.32. Only the video itself can move it. Bet 2's weekly totals and the scorecard read engaged views too, from mid-October and mid-November. I also fixed a report line that mislabelled total plays.
- **Product:** built the topic ranker's go/no-go count, set in September: how often Reddit's top post is a weak topic with a strong one close behind. Due with tomorrow's uploads (18 of 20 runs; 5 fired), it sets the ranker's test length.
- **Legal:** read Reddit's terms first-hand and sent them to you (#60). Our pipeline only reformats Reddit text: it strips formatting, and it skips posts with profanity rather than editing them. So the exposure is the licence's scope and the money clause, not editing. The channel's name also uses Reddit's, which its terms restrict.
- **Distribution:** confirmed TikTok's terms from its own page, including the country rule above. Meta's pages still refuse.
- **Security:** standing check clean: $0.19 spent this month, you are the only collaborator, no secrets in the project, and the only workflow change was your approved security fix. The quarterly account-security check, the plan's only answer to losing the channel, had never run. I sent you six checks, about 15 minutes, all needing your logins (#59). Your security fix from this afternoon works: the 15:08 release check ran on the new split and recorded its result, so I closed it in the code-health list.
- **General management:** trackers updated; three finished items closed. Two same-day messages to you on one issue can no longer overwrite each other (a fix).
- Fixing against improving: mostly fixing the record (the gap, two risk ratings, a misleading label). Nothing shipped changes the video; every product change waits on 12 October or your session.
- **Friction:** a plain download reads Reddit's and TikTok's pages, marked "needs a browser" for two shifts. And this log's word budget now holds two entries, not the ten its header asks for.

### Blocked
- **For you:** whether to ask Reddit for an agreement (#60, new; a ready-to-send draft is on it); the six account checks (#59, new); the quarterly planning session (#55, now with two notes: bet 2 in engaged views, and TikTok's country rule); the review-step proposal (#61, new; I recommend approving); one re-run of the comments change (#53); landing the auto-apply patch by hand (#50).

### Next
- Check that tonight's upload landed (not started by 17:50, normal for the evening slot) and tomorrow evening's first NoStupidQuestions one.
- Tomorrow, once the morning upload lands: read the topic ranker's count under its rule.
- On 12 October: judge "open on the question" under its rule. Read the engaged-view question beside it with the new measure, at 14 days old. Then the narrator and dark-morbid questions, and the first subscriber count.
- If you accept bet 2 in engaged views, fix its baseline once four complete weeks exist (early November).
- The next sample-run request is the first on the new security split: confirm its verdict lands.
- A fresh second review of today's code caught a real counting error (fixed; no reported number changed). Two uses, two catches, so I proposed it as a standing merge step (#61).
- Considered and not taken: a catch-up run after a missed slot (one miss in about 80 runs), and pinning the Ubuntu version (unaffected).

### Better?
- **Than last shift:** Unclear for revenue, but better informed. The gap is wider than we believed, and a legal question that could end the format now has a first-hand answer before bet 1 is built on it.
- **Than ~10 shifts ago:** Somewhat. We measure in the bar's own unit and know three platforms' rules first-hand. Views per upload have not moved; watch time reads flat.
- **Than ~100 shifts ago:** Too early to say.
