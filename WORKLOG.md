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

## 2026-10-05 (21:15) — the evening upload was lost to a GitHub outage, not a fault

**Summary:** This evening's scheduled upload was created eight hours late and then cancelled before it started, during GitHub's "Incident with Actions" (runner assignment failing, from 19:11 UTC). No code ran and nothing was uploaded, so there is nothing to diagnose and no sample run is needed.

### Done
- **Reliability:** traced the failed run. It never got a machine, billed 0 minutes, and was cancelled after 15 minutes in the queue. The saved record of the last post is untouched. The Polly permission was already proven by the 18:17 dry run.

### Next
- If the morning upload lands, the missing evening one needs no follow-up. A sample run of the live code is worth requesting only if a run fails *after starting*, with steps in its log.

## 2026-10-05 (18:45) — Weekly review: the "plays past the opening" figure is finally collected; the late upload looks like GitHub delay, not a failure

    Worked (% of the shift): data 25 · engineering 15 · audience 10 · reliability 10 · product 10 · editorial 15 · distribution 5 · gm 10

**Summary:** This is the first weekly review. We now measure how many plays get past the opening and, once you approve one line, the subscriber count, which is half of YouTube's bar. The format work aimed at revenue has started. Today's late upload looks like a GitHub delay, not a failure.

### Toward revenue
- A first step. The first candidate for a format YouTube would pay for is drafted, and the subscriber count, half of the payment bar, will be kept once you approve one line. The views gap is unchanged.

### Done
- **Reliability:** This afternoon's upload had not landed by 18:43, but that is not unprecedented: 28 September's landed at 19:46. GitHub also started every scheduled job seven to nine hours late today, so it should land around 21:00. I did not request a sample run, because it would use the AI quota the late upload still needs.
- **Reliability:** The week's other 15 uploads all landed. Two lost their AI-written title to an outage at the AI service, and there has been none since the longer retry went in on 4 October. The spending controls at Amazon are intact: $0.14 spent this month. The security check was clean: no credentials in the project, the secret files are still excluded, and no automated job changed.
- **Data:** The statistics run collected the share of plays that get past the opening for the first time (1,000 of 1,041 videos). That answered one research question (below) and closes an old code-health item. The experiment that reads it needs a week more: the two releases it compares share no common age until the 12 October snapshot.
- **Data:** Answered: older statistics do not hold the "past the opening" figure, so it can only be read from now on.
- **Data:** The weekly job now also records the subscriber count, half of YouTube's bar, which nothing recorded before. It cannot cost the other statistics if it fails. Keeping it needs one line from you (below).
- **Editorial:** Started the top-ranked item, making the format our own. The idea of a second voice reacting to a comment, shelved in July, is now the first candidate: YouTube pays for videos where the channel comments, not for read-outs. It is judged on whether it costs watch time, and it needs your approval for about 6 cents a month of extra narration before it is built. Still to draft: a storyline candidate and a curation candidate.
- **Product:** No decision rule is due. Whether one narrator is distributed less still has too few uploads per voice to answer, so I moved it to 12 October. Watch time per view is slightly up and views slightly down. The channel is still flat.
- **Distribution:** The Shorts feed is still 96% of views.
- **Audience:** There were no comments to read, because none were collected. The weekly job now saves the past week's comments on the 20 newest videos, without names, failing soft like the subscriber count. It also needs one line from you.
- **General management:** The trackers check clean. Six items are ready. Ranked by path to revenue: make the format our own, price the revenue routes, then the other platforms' terms and comparable channels. The measurement items rank below those. The upload check and the tracker corrections were fixes. The format candidate, the subscriber count and the comments were improvements.
- **Friction:** the tool that files issues for you waited silently for input when not given a description, and cost a few minutes. Recorded so the next shift passes one; not worth a change on one occurrence.

### Blocked
- **For you:** two one-line changes so the weekly job keeps the subscriber count and the viewer comments, filed as two issues with patches that apply in either order. Recommend approving both: without them, the data is collected and thrown away.
- Reddit's terms still need a browser read. Whether the narrator question has an answer waits on the 12 October snapshot.

### Next
- First check that today's afternoon upload landed. If it is still missing tomorrow morning, request a sample run of the live code after the 07:00 reset and away from the upload times. Merge the title-style change (due 6 October). Then the quarterly prep, which is still due, and after that the top of the queue: making the format our own.

### Better?
- **Than last shift:** Slightly. A first format candidate now targets YouTube's payment rule, and half of its bar is measured. Views have not moved.
- **Than ~10 shifts ago:** Unclear: watch time per view is up about 4% and views are flat.
- **Than ~100 shifts ago:** Too early to say.
