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

---

## 2026-10-05 — Monthly review: at today's views the Partner Program is hundreds of times out of reach

    Worked (% of the shift): strategy 30 · legal 20 · finance 5 · data 10 · reliability 5 · gm 30

**Summary:** The first monthly review found two blocks to revenue. YouTube's ad-revenue programme needs 10 million Shorts views in 90 days, while the channel has had about 90,000 in its whole life. And YouTube's own policy refuses to pay for videos that only read out other people's text, which is what we make. Next month should decide how the format becomes ours, and which way to earn.

### Where we stand
- Revenue is $0. Over three weeks, watch time per view rose slightly (12.0 to 12.5 seconds) and views per video fell (75 to 65); the trend is flat.
- **YouTube's own page, read today, sets the bar** at 1,000 subscribers plus either 10 million Shorts views in 90 days or 4,000 watch hours in a year. Our weeks run from about 600 to 3,000 views, which is 8,000 to 39,000 per 90 days, or 250 to 1,250 times short. Lifetime watch time: about 96 hours.
- We do not record subscribers, half the bar; collecting them is now queued.
- **Plainly, the current path does not reach the goal.** Pricing the other platforms will show whether another route does.

### Money
- Speech costs: $0.14 this month, forecast $0.96, against the $3 budget; all four controls intact. Nothing was priced or proposed.

### Risks
- Two risks now carry evidence: revenue too small (the views gap) and an unpayable format (below). Every risk has an answering item, and the standing security check was clean.

### Market and policy
- **YouTube's reused-content policy, read today on its own page, rules out today's format.** It will not pay for content that "exclusively features readings of other materials you did not originally create, like text from websites", and it judges the whole channel. It does pay for commentary, reactions, an added storyline, or a visible creator, so making the format our own is now ready work. A second rule refuses videos that look "made with a template", which ours also do.
- **Reddit's terms could not be read:** its pages refuse automated reads, even archived. A browser read would settle whether a paid channel needs Reddit's approval. Comparable channels: not started.

### Proposals for you
- **Apply one patch (#50):** the automatic landing you approved, built and tested, in a file only you may change.

### Next month
- **Today's afternoon upload had not landed by 18:38**, later than any on record (18:29), and a shift cannot see why. If it never lands, the next shift requests a sample run of the live code to see the error.
- Next shift: the weekly review, then quarterly prep built on both findings.
- Both your decisions are closed: shifts ended early because their remaining work depended on dates, and the redesign gave them nine items that do not (#46); the other is #50.
- **Finding:** Audience, Monetization and Market intelligence still have no work done after their first monthly review, despite having ready items.

### Better?
- **Than last shift:** Yes. For the first time the company knows how far its assumed revenue route is, and that the format itself must change before that route can pay.
- **Than ~10 shifts ago:** Unclear: watch time per view is up about 4%; views are flat.
- **Than ~100 shifts ago:** Too early to say.

---
