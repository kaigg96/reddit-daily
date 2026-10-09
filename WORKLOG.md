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

## 2026-10-09 (23:15) — Titles with one word in capitals get about twice the views; a fair test of it is built and needs only its sample video

    Worked (% of the shift): data 35 · product 20 · legal 10 · market 10 · engineering 10 · strategy 5 · security 5 · gm 5

**Summary:** Our videos whose titles put a word in capitals ("Who's YOUR Hero?") got about twice the views of the rest. That held in every split with enough uploads to read, and viewers watched them about as long. I built a fair test that flips a coin for each upload, and it needs only tomorrow's sample video to go live. Views are the half of YouTube's payment bar we are furthest from, so this is the first step in days aimed at it.

### Toward revenue
- **Yes, a bet on views.** The pattern is a correlation: the AI may capitalise when a post is livelier anyway. The coin-flip test settles it at no cost, with no extra AI or narration calls. Its rule is set in advance. After 30 uploads in each group, keep capitals if their views lead is bigger than chance alone produces one time in ten at that size (73% today), and watch time holds. A smaller lead gets one extension, to 45 uploads per group. My first bar (30%) sat inside chance; I reset it before anything shipped.

### Done
- **Data (a bet):** taught the reporting tool to tell titles with emphasis capitals apart from plain ones. Read at 7 days old: +120% views overall (65 against 68 uploads), and ahead in each of the two earlier releases with enough uploads, each title style, short and long titles, and morning and evening, and it still holds at 14 days old (+77%). Watch time 10 against 11 seconds, inside the normal swing. The extra plays are the kind YouTube's payment bar counts: the same share are engaged views (31% against 30%). It also explains most of the lead behind the 5 October decision to favour "You…" titles. Those titles nearly always capitalise "YOU", and among capitalised titles they lead the others by only 7%. That decision stands, since its rule is on watch time, but the new test now measures what actually moved views. A lead, on small weekly numbers: the fall in views since mid-September is almost all in titles without capitals. A fresh review caught four titles misfiled by abbreviations; fixed before the numbers were recorded. Live, measurement only.
- **Product (a bet):** built the coin-flip test on a branch. One group is asked for exactly one capitalised word, the other for none. Both are banned from shock phrases. A free sample on this machine rendered a playable video, and a fresh review found nothing blocking (its two small points are fixed). It needs only a real sample before it goes live.
- **Legal / market intelligence:** read first-hand that since July 2026, YouTube will not pay for content "designed to shock or surprise viewers for the sole purpose of getting views", and its reviewers read titles. 9 of our 166 titles use phrases like "SHOCKING" or "You Won't Believe", so both test groups now forbid them. Capitals for emphasis are not what that rule names.
- **Strategy:** the channel holds 1,041 videos, and 883 come from before July's pipeline, including 30 duplicate copies. All are readings of Reddit. YouTube's reviewers check a channel's "main theme", so at two uploads a day the new show stays a minority for over a year. Those old videos earn under 1% of today's views. Added to the brand decision: when you settle the name, also decide whether to make them private or start the new show fresh.
- **Market intelligence:** secondary sources say Reddit's commercial access is a negotiated deal from about $12,000 a year, with no self-serve tier. I could not confirm it on Reddit's own pages (they refuse automated reads). If true, the answer to #60 may decide the content source more than the format does.
- **Security:** standing check clean. Narration spend $0.25 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change. Tonight's upload landed normally.
- Fixing against improving: almost all improving; the last shift was all fixing.

### Blocked
- **For you, in order of what they unblock:** the label on #70 (bet 1's first step); the four commands on #50 (#65 waits on it); the Groq key and label on #69; the planning session (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53.

### Next
- Morning, after 07:00: one sample video is allowed per shift, and two reviewed branches wait for one: the safety check's crash fix and the capitals test. I have combined them on one branch, with all tests passing, so one sample clears both. The crash fix changes nothing viewers see, so this still tests one thing, and the test starts a day sooner. If the combined sample fails, take the crash fix alone first. The sample's report shows the title beside its group; check the title obeys it.
- Before the subreddit and title-style tests read (about 2 November): their watch-time limit sits where chance lands half the time at their size, not one time in ten. Reset it against the new measure before their data is read, as I did for the capitals test.
- 12 October: read `v7` under its rule, then the engaged-view, narrator, dark-morbid and zero-view questions, the b-roll clip check, and the first subscriber count.
- If #70 is approved, build it on a branch. The capitals test is a coin per upload, so it runs alongside bet 1 without spoiling either read.
- Process: the company plan and the product tracker both sit at their word limits. So each finding tonight meant first trimming unrelated text, about a tenth of the shift. Worth a look at the next audit; I changed nothing.

### Better?
- **Than last shift:** Yes. For the first time in several shifts, something that changes what we ship is ready, aimed at views, and costs nothing to run.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), and the video itself has not changed since 25 September. The capitals result is the largest views difference any logged title trait has shown, but it is a correlation until the test reads, in mid-November at the earliest.
- **Than ~100 shifts ago:** Too early to say.

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
