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

## 2026-10-09 (17:27) — When our main AI model is overloaded, the safety check now asks a second model instead of falling back to a keyword list

    Worked (% of the shift): reliability 45 · engineering 20 · market 10 · security 10 · gm 10 · product 5

**Summary:** The safety check that keeps risky posts out of our videos used to drop to a crude keyword list whenever Google's main model was overloaded. That happened to this morning's upload. It now asks a second model first, which has its own daily allowance. This is a fix, not a step toward revenue: it protects uploads from being buried, and it does not grow views.

### Toward revenue
- **Nothing directly.** Videos YouTube quietly buries earn nothing, and this check is our only defence against that, so keeping it working protects what we have. The steps that would move revenue still wait on you, #70 first.

### Done
- **Reliability (a fix):** before changing anything, I tested the second model on the safety check's five known cases. All five were right (5 AI requests, on that model's own allowance, so the upload's was untouched). The upload log shows the problem is real but rare: 2 of the last 38 uploads lost the full check. Both times the second model was answering in that same run. And on the two occasions the second model was overloaded, the main one was fine. The two don't fail together, so either of those uploads would have had a proper check. A sample video passed and a fresh review checked the change before it went live. The log records whenever the second model stands in, so we will see it working.
- **Market intelligence:** our main AI model's sibling was closed to new users last month, and one Google page lists our model for retirement on 20 October. Google's own page for the service we use says it is "not deprecated and will continue to be served until further notice"; the 20 October date is for a different Google service. So nothing is closing, and today's change covers the safety check if that changes without notice.
- **Product:** the safety check's weekly audit found nothing to fix. Its last skipped post was on 12 September, far under the level where it would need narrowing.
- **Security:** standing check clean. $0.25 spent on narration this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- **Engineering:** the fresh review found nothing blocking, plus a few small things. The one that matters was there before today: an oddly shaped answer from the AI could crash a run, and that slot would get no upload. It has never happened, but the second model now sends its answers through the same code. The fix and the rest are on a separate branch. Two more fresh reviews went over it, and their suggestions are in: the check can no longer crash a run on any reply. It waits for tomorrow morning's sample-video slot, because changing the merged version after its sample would have voided it.
- **General management:** closed a long-standing code-health item about the AI's daily limit running out before the morning upload. Since we began recording why AI calls fail, 28 uploads in, it has not happened once. Every failure was an overload, which the earlier fix and today's change now cover. The comments change you approved (#53) never applied because GitHub's job died before running a single step. That looks like a GitHub glitch, not a fault in the change, so a re-run should do it.
- Fixing against improving: all fixing. Everything that would improve the video or the business waits on you or on Monday's data.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50, which let every approved rule change land by label (#65 waits on it); the Groq key and the label on #69 (#68); the planning session for bets 2 and 3 (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53.

### Next
- 12 October: read `v7` under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, the b-roll clip check, and the first subscriber count.
- If #70 is approved: build it on a branch as the last entry describes.
- First: check tonight's upload landed cleanly. It is the first live run of today's change, and it starts after this shift ends.
- Tomorrow morning, after 07:00: ask for a sample video of the follow-up branch, which three fresh reviews have already passed, and merge it on a pass.
- Watch the upload log for the second model standing in, and for any upload where both models failed.
- Process: I asked for the sample video before the fresh review, so the review's fixes could not use it, and only one sample is allowed per 12 hours. Review first, then ask for the sample: it costs about six minutes and lets fixes ship the same shift.
- I spent the last 25 minutes watching for tonight's upload, ready to undo the change. It had not started by 18:16. Nothing else cleared the bar. Considered and dropped: testing the second model on two more cases (2 requests; whatever the result, it beats the keyword list, so no decision rides on it); a title fallback for the main model being retired (Google says it is served "until further notice"); stopping two runs from overlapping (still belongs with four uploads a day); reading engaged views by topic (one week of data, wait for Monday's); whether long questions lose viewers now that videos open on them (answered on 25 September: it was video length, not the question); building bet 1 ahead of your label (the audit's lesson).

### Better?
- **Than last shift:** Slightly, on reliability only. An overload no longer leaves an upload with only the keyword list. Nothing in the video or the business changed.
- **Than ~10 shifts ago:** No, on the audit's evidence: no video change, watch time flat (12.0 seconds a week ago and now), and the decisions that would change it wait on you.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-09 (10:33) — Bet 1 now has a tested first step you can approve with one label: a host's commentary makes up half of each video, at today's length and cost

    Worked (% of the shift): gm 30 · product 20 · editorial 15 · strategy 10 · engineering 10 · data 5 · reliability 5 · security 5

**Summary:** I tested whether our AI can write commentary that fills half of each video. It can, at today's length and narration cost, so bet 1 (making the format ours) is now one label for you on #70. This shift's audit found the company's limit is the tasks that need your own hands, not your decisions. No revenue yet, but this is the step YouTube's rules make the precondition for any.

### Toward revenue
- **One step closer, not yet shipped.** YouTube will not pay for videos that only read other people's words. One host line per video is unlikely to change that. Commentary making up the bulk of each video might. Five drafts put our own words at 51–67% of each script, with no phrasing repeated between them, at today's length and cost. Approving #70 starts the build.

### Done
- **Editorial / product:** five commentary drafts, then three reruns under tighter rules: eight AI requests in all, on the separate test model, so the upload's allowance was untouched. Results, the best draft, and what went wrong are on #55. The failures were facts stated in our voice, jokes on grim threads, and answers referred to by number. Tighter rules fixed the last two kinds but not the first: on medical threads it still slipped in facts and advice. So the proposal skips medical threads when picking the post. They are 2 of our 165 uploads, and the next post runs instead, so every upload keeps its commentary. Two corrections on #70 keep your rule that answers are read in vote order, and adopt the "show of hands" stance unless you name another.
- **Strategy / gm:** split bet 1 out of the planning session as #70, a single label. Since 25 September, all 12 of your label-only decisions were answered, most within a day. All 8 open items need your hands or a session.
- **General management (audit, due):** none of the eight shifts since the last audit changed a video, and every self-assessment hedged. Two of the decisions behind how shifts work rest on an assumption that is false while your hands-on queue is this long: that there is always work above the bar. That is recorded, with dated notes on five decisions. The vote built two shifts ago, ahead of your answer, is now undercut by the market read. So the lesson is to build after a label, not before.
- **Engineering (a fix):** a shift missed your "no" on #62: the decision list skipped every issue you had closed. It now shows the ones you closed without approving, with your reply. A fresh review caught that a shift's own close could pass as yours, and that is fixed.
- **Data:** checked that Monday's two pre-committed reads run on today's data. The `v7` read correctly says not yet (13 of its 20 uploads). The engaged-view read works, but the release command had silently ignored the measure it was asked for and printed watch time instead. It now refuses and names the right command, so Monday's read cannot be misread that way.
- **Reliability:** checked why this morning's upload lost its AI safety check. Gemini was overloaded twice. Titles have not been lost to that since the 4 October fix (0 of 10), so I dropped a title fallback I had started; it had nothing to fix. The safety check's fallback needs a test first, which is next shift's work.
- **Security:** standing check clean. $0.24 spent on narration this month (forecast $0.88 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: half and half. The commentary test and #70 improve; the decision-list fix, the release-read guard, two closed code-health items and the audit notes fix.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50, which make every approved rule change land by label from then on (#65 is waiting on it); the Groq key and the label on #69 (#68); the planning session for bets 2 and 3 (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments change (#53).

### Next
- If #70 is approved: build it on a branch, with the top two answers in vote order, the show-of-hands verdict, medical threads skipped at selection, and the share of our own words logged per upload. Then ask for a sample, and you listen to one with real narration. It ships as its own version after `v7`'s read.
- 12 October: read `v7` under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, and the first subscriber count.
- With fresh AI budget: test the safety check on the second model, five requests. If it passes, let the check fall back to that model when Gemini is overloaded.
- Process: this shift's eight requests went on research, which left none for a sample video. That was the right trade today, but it is the choice a shift makes when it spends them.
- I handed over about 30 minutes early, because nothing else cleared the bar. Considered and dropped: building the commentary step before your label (the audit's lesson); a title fallback (no titles lost since 4 October); the safety check's fallback (it needs AI requests I had spent); asking now for four uploads a day (its read is due in November); the long-video route to the Partner Program (the same reused-content rule blocks it); stopping two video runs from overlapping (rare at two a day; it belongs with four a day).

### Better?
- **Than last shift:** Yes, slightly. Bet 1 has evidence it fits today's length and cost, in the shape you answer fastest. Nothing in the video changed.
- **Than ~10 shifts ago:** No, on the audit's evidence. None of those shifts changed a video. Median watch time is flat (12.0 to 12.5 seconds, inside the usual swing), views per upload went from 75 to 65, and two built features wait on you.
- **Than ~100 shifts ago:** Too early to say.
