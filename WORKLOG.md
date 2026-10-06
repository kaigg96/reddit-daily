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

## 2026-10-05 (22:12) — Quarterly prep: three bets drafted for you; no revenue route is in reach on today's path

    Worked (% of the shift): strategy 25 · data 20 · market 10 · editorial 10 · engineering 10 · reliability 10 · product 5 · legal 5 · gm 5

**Summary:** The first quarterly packet is with you: three bets for October to December, each with a first step and a rule for judging it. Pricing the other platforms found none within reach either. The nearest, TikTok, is about 8 times short and pays only for videos over a minute, so making the format our own (bet 1) comes before any route.

### Toward revenue
- The company now has a drafted plan for the quarter instead of a ranked list: make the format ours, raise weekly views, and price and pilot another platform. It waits on your planning session.
- The gap is measured properly for the first time, counting every view as YouTube does. It is 32,000 to 37,000 views per 90 days against a bar of 10 million, about 300 times short. We have 21 subscribers against the 1,000 needed, 48 times short, so views are the half that binds.
- The "You…" title style, which earned 47% more views, is merged and starts with tomorrow morning's upload.

### Done
- **Strategy:** drafted the three bets and sent them to you as one issue, asking you to hold the planning session. Bet 1: add commentary or a storyline of our own, without which YouTube will not pay. Bet 2: double weekly views. Bet 3: price the other platforms and pilot the best one.
- **Strategy:** priced the other routes from creator guides, because the platforms' own pages refuse automated reads. TikTok needs 10,000 followers and 100,000 views a month (about 8 times short), and pays only for original videos over one minute. Facebook is invite-only and about 160 times short. Instagram pays no reliable rate.
- **Market:** scanned eight comparable channels; this function's first work. Every large one has a human voice or face and gives a verdict. The text-to-speech ones stay small even when they post 9 times a day. That suggests AI commentary may not be enough for bet 1, and I have asked you whether a human voice is ever part of the show.
- **Editorial:** drafted the second format candidate, a host storyline: a setup line before the answers and a verdict line after them, with the length held. Curation is folded into it, because picking other people's text is still a reading. You can now choose between the candidates.
- **Data:** the report tool now gives total weekly views and the channel-wide views the bar counts. Both are needed to judge bet 2. I fixed bet 2's starting point now, before new data arrives: 8,300 views over September's last four weeks, so doubling means 16,600.
- **Data:** found that watch time rises with length up to about 31 seconds, and nothing longer has ever been measured. So any TikTok route needs a one-minute test on YouTube first.
- **Data:** tested my own proposal to run tests on alternating days, and it failed. Split by alternate days, uploads differ as much as consecutive batches do (12% against 13%), so it would not sharpen our tests. I withdrew it on your issue before you spent time on it.
- **Engineering:** checked whether 3 to 4 uploads a day fits the AI service's free daily cap, which bet 2 needs. It fits: 80 of 84 runs used 2 requests, so 4 a day comes to about 16 of the 20. A free setting covers the rare worst case, to be applied when volume ships.
- **Legal:** Reddit's own pages still refuse automated reads, but the guides agree that using its content in a monetized product needs Reddit's written approval. I raised that risk from unknown to likely. Asking Reddit comes before any application for payment.
- **Product:** merged the title-style weighting. Its sample run passed, and no upload runs between now and midnight, so the effect is the same as merging on the 6th. A sample run of the live code after the merge also passed, with a real post, an AI-written title and narration, so tomorrow's upload path is checked.
- **Reliability:** your approval of the viewer-comments change never landed. The job that applies it was cancelled in GitHub's outage before it ran. I have asked you to re-run it. The tool that lists your decisions now flags any approval that never landed. This was a fix.
- **Security:** standing check clean. No credentials are in the project, the secret files are still excluded, no workflow changed this shift, and the Amazon spending controls are intact ($0.15 this month).
- **General management:** brought both trackers back under their reading budgets and retired five finished items. The process-health check raised "shifts end with most of their time unspent" again. I filed it with context: the last three short shifts include the monthly and weekly reviews.
- Fixing against improving: mostly improving. The fixes were the lost approval, the gap figure and the tracker trims.
- **Friction:** I re-ran a check that the newer Python version works, which the code-health log already recorded on 30 September, because I read only part of that entry. It cost about six minutes and taught nothing new. It was my mistake, not a process gap.

### Blocked
- **For you:** the quarterly planning session, one re-run of the comments job, landing the auto-apply extension by hand (a shift cannot), and the browser read of TikTok's, Meta's and Reddit's terms (bet 3's first step).
- The first format test cannot start before you approve bet 1. The format and narrator reads wait on the 12 October snapshot.

### Next
- Check that tomorrow's morning upload landed with a title. Then merge subreddit rotation, which passed its sample run.
- No work is ready: everything waits on your session or on 12 October. Generating more considered a single-story format test and a one-minute test (both wait on your bet choices), a faster testing method (refuted tonight), and the Python upgrade (scheduled after the 12 October read). Until your session, the next shift's best use is the rotation merge above, then the 12 October reads.
- On 12 October: judge the "open on the question" change under its rule, and read the narrator and topic questions.

### Better?
- **Than last shift:** Yes. The quarter has a drafted plan, the gap is measured correctly, and one change aimed at views is live from tomorrow.
- **Than ~10 shifts ago:** Somewhat. We now know what blocks revenue: the format and the scale. We did not know that two weeks ago. Watch time per view is flat, and views per upload fell by about 40% over September, which is still within normal swings.
- **Than ~100 shifts ago:** Too early to say.
