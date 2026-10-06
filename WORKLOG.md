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

## 2026-10-06 (17:11) — We are about 800 times short of YouTube's bar, not 300; Reddit's own terms say our use needs its agreement

    Worked (% of the shift): data 30 · legal 15 · security 15 · product 10 · reliability 10 · distribution 10 · gm 5 · engineering 5

**Summary:** Two facts changed the company's picture; both are with you, with recommendations. YouTube's bar counts only "engaged" views, about a third of our plays, so we are about 800 times short, not 300. Reddit's own terms, read first-hand for the first time, say making money from its posts needs Reddit's written agreement. Read plainly, they leave even today's unpaid videos outside the licence.

### Toward revenue
- Nothing moved revenue directly; this shift corrected the map the bets rest on.
- **The gap is wider than we thought.** YouTube counts a view whenever a Short starts playing, but the 10-million bar counts only "engaged" views, and only 36% of ours are, so we earn about 11,000 to 13,000 of the views that count per 90 days, roughly 800 times short. I recommended on the planning issue that bet 2 ("double weekly views") be measured in engaged views, so a change that wins only swipe-past plays cannot pass it.
- **Reddit's terms are now first-hand.** Earning from Reddit content needs "express written approval from Reddit" and "a separate agreement". Its newer terms (September 2024) go further: any use "by or on behalf of a business" needs written approval, paid or not. The licence to posts covers showing them inside our own app, unmodified. Republishing them as YouTube videos sits outside a plain reading. I recommend asking Reddit now, before the quarter is committed to this format; the answer decides whether any of the three bets has a future. Nothing changes in production meanwhile. If Reddit says no, Stack Exchange is a fallback: its users' posts are licensed for reuse, commercial use included, with credit and the same licence passed on (its terms, updated November 2025).
- **TikTok's own page adds a rule:** the account must be based in one of eight countries (US, UK, Germany, Japan, South Korea, France, Mexico, Brazil). If you are not, bet 3's TikTok pilot is closed.

### Done
- **Reliability:** last night's evening upload never happened. GitHub could not give the job a machine during its outage, so the run failed before any of our code ran, and neither of today's earlier shifts noticed it. Nothing of ours to fix; Monday's digest will list the missed day. GitHub's machines move to a newer Ubuntu on 19 October; I checked our video job is unaffected. Separately, your Monday digest now carries the keep-or-revert verdict for the current and previous release, each at the size its rule committed to. So the opening test's verdict reaches your email from 12 October even if no shift remembers. A fix.
- **Data:** built the measure of engaged views and checked it with tests. Our "You…" titles keep their lead in engaged views (+60%), so that change counts toward the bar. No trait we log moves the engaged share: title style, voice, length and time of day all sit between 0.29 and 0.32. Only what the video itself does can move it, which is what the opening-seconds test and bet 1 target. The weekly totals for bet 2 can now be read in engaged views from the 12 and 19 October data, and the scorecard shows the engaged share by itself from about mid-November. I also fixed a report line that mislabelled total plays.
- **Product:** built the topic ranker's go/no-go count, set in September: how often Reddit's top post is a weak topic with a strong one close behind. Due with tomorrow's uploads (18 of 20 runs; 5 fired), it sets the ranker's test length.
- **Legal:** read Reddit's terms first-hand and sent them to you (#60). Our pipeline only reformats Reddit text: it strips formatting, and it skips posts with profanity rather than editing them. So the exposure is the licence's scope and the money clause, not editing. The channel's name also uses Reddit's, which its terms restrict.
- **Distribution:** confirmed TikTok's terms from its own page, including the country rule above. Meta's pages still refuse.
- **Security:** standing check clean: $0.19 spent this month, you are the only collaborator, no secrets in the project, and the only workflow change was your approved security fix. The quarterly account-security check, the plan's only answer to losing the channel, had never run. I sent you six checks, about 15 minutes, all needing your logins (#59). Your security fix from this afternoon works: the 15:08 release check ran on the new split and recorded its result, so I closed it in the code-health list.
- **General management:** trackers updated; two finished items left the plan, one the code-health list.
- Fixing against improving: mostly fixing the record (the gap, two risk ratings, a misleading label). Nothing shipped changes the video; every product change waits on 12 October or your session.
- **Friction:** a plain download reads Reddit's and TikTok's pages, marked "needs a browser" for two shifts. And this log's word budget now holds two entries, not the ten its header asks for.

### Blocked
- **For you:** whether to ask Reddit for an agreement (#60, new; a ready-to-send draft is on it); the six account checks (#59, new); the quarterly planning session (#55, now with two notes: bet 2 in engaged views, and TikTok's country rule); one re-run of the comments change (#53); landing the auto-apply patch by hand (#50).

### Next
- Check that tonight's upload landed (it had not started by 17:30, normal for the evening slot), and that tomorrow evening's first NoStupidQuestions upload lands with a title.
- Tomorrow evening: read the topic ranker's count under its rule.
- On 12 October: judge "open on the question" under its rule. Read the engaged-view question beside it with the new measure, at 14 days old. Then the narrator and dark-morbid questions, and the first subscriber count.
- If you accept bet 2 in engaged views, fix its baseline once four complete weeks exist (early November).
- The next sample-run request is the first on the new security split: confirm its verdict lands.
- Considered and not taken: a standing fresh review before live merges (one use so far), a catch-up run after a missed slot (one miss in about 80 runs), and pinning the Ubuntu version (unaffected).

### Better?
- **Than last shift:** Unclear for revenue, but better informed. The gap is wider than we believed, and a legal question that could end the format now has a first-hand answer before bet 1 is built on it.
- **Than ~10 shifts ago:** Somewhat. We measure in the bar's own unit and know three platforms' rules first-hand. Views per upload have not moved; watch time reads flat.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-06 (11:15) — Subreddit rotation is live; our views are not a lottery of a few hits

    Worked (% of the shift): data 30 · product 25 · gm 20 · engineering 10 · reliability 5 · security 5 · monetization 5

**Summary:** Subreddit rotation is live, the supply step for more uploads a day. Two research questions about our views are answered: no single upload or logged trait drives them, so the quarter's views target stands.

### Toward revenue
- Subreddit rotation is live from this evening. It is the supply step for bet 2's move to 3 to 4 uploads a day, doubling the pool of posts we draw from. Volume follows once the new subreddit's uploads hold up (15 of them, read in early November).
- The views bar is now sharper. About 90% of our views arrive in a video's first week, so old videos do not keep earning. At four uploads a day, YouTube's bar needs about 28,000 first-week views per video. We average 186.

### Done
- **Reliability:** this morning's upload landed with an AI-written "You…" title. Your subscriber-count change landed overnight; first reading 12 October.
- **Product:** merged subreddit rotation. Uploads now alternate between AskReddit and NoStupidQuestions, each taking mornings and evenings in turn. Its sample run passed on the final code with a real NoStupidQuestions post. Before that, I fixed a gap: the topic-analysis script only recognised AskReddit posts, so rotated uploads would have vanished from it. A test pins it.
- **Data:** asked whether a few hit videos earn most of our views. The best tenth earn 42%, and the single best 3%. By the rule set before looking, nothing changes. Of seven traits the hits might share (title style, voice, topic, time of day, length, background, title source), none stands out beyond chance.
- **Product:** a decision rule had come due unrecorded: the 19 September release (safety-screen and AI-timeout fixes). Read as its rule is written, it is **kept**: watch time per view held (up 10%, inside normal drift). Views read 62% lower, but views never trigger a revert, because they swing that much with nothing changed.
- **Data:** refreshed one research count (dark-morbid, 10 of 12 uploads). One background clip is at 3 buried uploads of 13, against 3 of 61 for the others: not significant yet, so watching.
- **Data:** found and fixed a fault in the channel scorecard: it could flag a fall in uploads stuck at zero views, but never a rise. Read correctly, the last three weeks are **mixed**, not better. Watch time is up slightly, but zero-view uploads rose from 2.4% to 5.6%, just past their 3-point limit. One period, so noise unless it repeats. A fix.
- **Monetization:** first work here. YouTube's own page lists no easier tier: 1,000 subscribers and 10 million Shorts views in 90 days.
- **General management:** ran the process audit, which was due (last one: 6 October). I re-checked the past process decisions against today's evidence and added notes to six. One was out of date (shifts no longer slice time by function) and is now marked replaced. Two weak points are recorded. Your approvals reach the code by an automatic step that has failed twice in three tries. And the planned 3 to 4 uploads a day would change the normal-noise yardstick our release checks use, so it must be re-measured then. From current best practice, I tried a fresh second review of the rotation code before merging. It found a formatting slip (fixed) and a quirk in how rotation pairs with title styles (documented; the planned reads are unaffected). I also pruned the first version's history from the product document.
- **General management:** closed September's caption-upload problem (26 clean uploads since). Your pending comments change still applies cleanly, so a re-run will work. The process-health check again flagged short shifts; I added the cause to your issue: the queue waits on your planning session.
- **Security:** standing check clean ($0.17 spent this month). Re-reviewed the two drafted fixes that keep untested code away from a token able to change the live code. Both still hold. I added one small hardening to each and sent them to you as one change to approve.
- Fixing against improving: mostly improving. The fixes were the scorecard, the analysis gap and the tracker closures.
- **Friction:** the merge could not be tested until 10:51, because last night's 22:51 check of the live code used the one automatic render allowed per 12 hours. An evening render on code the next morning's upload will exercise anyway costs the next shift its merge.

### Blocked
- **For you:** the quarterly planning session (#55). It is now the main thing holding the queue: nearly every item waits on it, on your browser read for bet 3, or on the 12 October statistics. Also one re-run of the comments change (#53), and the security change above (#58; I recommend approving).

### Next
- Check that this evening's upload lands, and that the first NoStupidQuestions upload (7 October, evening) lands with a title.
- On 12 October: judge "open on the question" under its rule, and read the narrator, engaged-view and subscriber questions. Beside its rule, never as a trigger: 4 of its 13 uploads are buried (5 views or fewer), against 1 of 10 before. Re-read the watched clip.
- The process audit is done; the remaining old records are already compact and kept on purpose. Weigh proposing the fresh review as a standing step before live merges: it caught real issues on first use.

### Better?
- **Than last shift:** Slightly. The supply step for more uploads a day is live. We also know views are not hit-driven, so no hunt for a viral formula is warranted.
- **Than ~10 shifts ago:** Somewhat. Bet 2's levers are in place or ready, but views per upload have not moved, and the scorecard reads mixed.
- **Than ~100 shifts ago:** Too early to say.
