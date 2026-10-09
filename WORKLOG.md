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

## 2026-10-09 (10:33) — Bet 1 now has a tested first step you can approve with one label: a host's commentary makes up half of each video, at today's length and cost

    Worked (% of the shift): gm 35 · product 20 · editorial 15 · strategy 10 · engineering 10 · reliability 5 · security 5

**Summary:** I tested whether our AI can write commentary that fills half of each video. It can, at today's length and narration cost, so bet 1 (making the format ours) is now one label for you on #70. This shift's audit found the company's limit is the tasks that need your own hands, not your decisions. No revenue yet, but this is the step YouTube's rules make the precondition for any.

### Toward revenue
- **One step closer, not yet shipped.** YouTube will not pay for videos that only read other people's words. One host line per video is unlikely to change that. Commentary making up the bulk of each video might. Five drafts put our own words at 51–67% of each script, with no phrasing repeated between them, at today's length and cost. Approving #70 starts the build.

### Done
- **Editorial / product:** five commentary drafts, then three reruns under tighter rules: eight AI requests in all, on the separate test model, so the upload's allowance was untouched. Results, the best draft, and what went wrong are on #55. The failures were facts stated in our voice, jokes on grim threads, and answers referred to by number. Tighter rules fixed the last two kinds but not the first: on medical threads it still slipped in facts and advice. So the proposal skips medical threads when picking the post. They are 2 of our 165 uploads, and the next post runs instead, so every upload keeps its commentary. Two corrections on #70 keep your rule that answers are read in vote order, and adopt the "show of hands" stance unless you name another.
- **Strategy / gm:** split bet 1 out of the planning session as #70, a single label. Since 25 September, all 12 of your label-only decisions were answered, most within a day. All 8 open items need your hands or a session.
- **General management (audit, due):** none of the eight shifts since the last audit changed a video, and every self-assessment hedged. Two of the decisions behind how shifts work rest on an assumption that is false while your hands-on queue is this long: that there is always work above the bar. That is recorded, with dated notes on five decisions. The vote built two shifts ago, ahead of your answer, is now undercut by the market read. So the lesson is to build after a label, not before.
- **Engineering (a fix):** a shift missed your "no" on #62: the decision list skipped every issue you had closed. It now shows the ones you closed without approving, with your reply. A fresh review caught that a shift's own close could pass as yours, and that is fixed.
- **Reliability:** checked why this morning's upload lost its AI safety check. Gemini was overloaded twice. Titles have not been lost to that since the 4 October fix (0 of 10), so I dropped a title fallback I had started; it had nothing to fix. The safety check's fallback needs a test first, which is next shift's work.
- **Security:** standing check clean. $0.24 spent on narration this month (forecast $0.88 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: half and half. The commentary test and #70 improve; the decision-list fix, three closed or re-recorded code-health items and the audit notes fix.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50, which make every approved rule change land by label from then on (#65 is waiting on it); the Groq key and the label on #69 (#68); the planning session for bets 2 and 3 (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments change (#53).

### Next
- If #70 is approved: build it on a branch, with the top two answers in vote order, the show-of-hands verdict, medical threads skipped at selection, and the share of our own words logged per upload. Then ask for a sample, and you listen to one with real narration. It ships as its own version after `v7`'s read.
- 12 October: read `v7` under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, and the first subscriber count.
- With fresh AI budget: test the safety check on the second model, five requests. If it passes, let the check fall back to that model when Gemini is overloaded.
- Process: this shift's eight requests went on research, which left none for a sample video. That was the right trade today, but it is the choice a shift makes when it spends them.

### Better?
- **Than last shift:** Yes, slightly. Bet 1 has evidence it fits today's length and cost, in the shape you answer fastest. Nothing in the video changed.
- **Than ~10 shifts ago:** No, on the audit's evidence. None of those shifts changed a video. Median watch time is flat (12.0 to 12.5 seconds, inside the usual swing), views per upload went from 75 to 65, and two built features wait on you.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-09 (00:00) — The free AI route that keeps Reddit posts out of training is now in the live code, switched off: your key and one label turn it on

    Worked (% of the shift): engineering 45 · market 15 · product 15 · gm 10 · security 10 · reliability 5

**Summary:** The free AI route that keeps Reddit posts out of training (#68) is now in the live code, switched off and checked, so your ten minutes on #68 and #69 leave no building to do. Outside evidence also says one host line per video is unlikely to be enough originality for YouTube, which matters for bet 1; neither brings revenue directly.

### Toward revenue
- **Nothing directly.** Two things moved. Once you add the key, Groq takes away the AI-training part of the Reddit-terms problem and lifts the 20-a-day AI limit. And bet 1 now has YouTube's own wording on what originality earns money, which bears on how big that bet has to be.

### Done
- **Engineering:** finished the steps that had to come before switching to Groq, then merged it into the live code, switched off. If it is switched on without its key, calls fall back to Gemini rather than costing the upload its title. The upload log now records which AI answered. Groq's per-minute limit gets one short wait. A sample video passed. A fresh review found nothing blocking, and its fixes went in. The sample's title call failed on Gemini's side, a model overload like one that hit tonight's upload, so the error message now says why. A bet, built ahead of your answer.
- **Engineering:** the workflow change that gives the Groq key to the four jobs that make AI calls, and strips it from their saved logs, is #69, waiting on your label. #68 now points to it.
- **Product:** set the rule for switching to Groq before anyone can flip it. It changes the spoken closing line and which post runs, so it ships as its own version. Revert if watch time falls beyond the usual limit, or if titles fail on 4 or more of its first 20 uploads (Gemini: 3 of the last 30).
- **Market intelligence (this function's first work):** YouTube's policy page, read first-hand, allows "reaction videos where you comment". It refuses videos that "feel interchangeable", and "templated storylines … with minimal or no … commentary". It says nothing against synthetic voices. One Reddit-stories channel that used human voice actors was still demonetized in May 2026. So one quip per video, or a fixed opening and closing around the readings, is unlikely to pass alone; commentary would need to fill most of each video. My recommendation is on #55, and the host-storyline plan now carries the caveat.
- **Security:** the safety screen's two new test questions, which it had never seen, both got the right answer on Gemini (2 requests). That is the first sign the screen generalizes. Standing check clean: $0.21 spent on narration this month (forecast $0.96 of $3), money controls in place, no secrets in the project, no workflow change. The dependency warnings are unchanged, and they sit in the image library, which only reads our own files.
- **General management:** the product tracker had grown past its size limit; it is now shorter than at the start of the shift.
- Fixing against improving: mostly improving (the Groq route, its switch rule, the market read). Three small fixes rode along.

### Blocked
- **For you, in order of what they unblock:** the planning session and the vote's one sentence (#55); asking Reddit (#60); the Groq key and the label on #69, about ten minutes together, or telling us you are in the UK, EEA or Switzerland (#68); the music script (#66); the sample-video sentence (#65); the account checks (#59); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Check this morning's upload landed and is not a repeat.
- When the Groq key and #69 land: run the screen check on Groq and take a sample. Then switch on as its own version, by changing the code's default, never a workflow setting, under the rule above.
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, the first subscriber count, and the scorecard with private videos excluded.
- The workflow audit comes due in a shift or two (eight shifts since the last one).
- I handed over about 35 minutes early because nothing else cleared the bar. Considered and dropped: posting-time research (answered 30 September); title failures (none since the 4 October fix); a safety check in the upload step that practically cannot fire and would need its own sample; a draft to Reddit (one is on #60 already); closing old digest issues (your email channel); pre-building the Groq switch (two lines, and it cannot be checked without the key).
- Process: a background reviewer reads the shared working copy, so switching branches while it runs can show it the wrong code. It coped this time; next time, give it its own copy.

### Better?
- **Than last shift:** Yes, slightly. The Groq route went from a branch to the live code, so switching it on needs only your ten minutes, and bet 1 has outside evidence on how big it must be.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a first step and a rule, and the AI-limit and AI-training problems have a free fix merged and waiting on a key. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.
