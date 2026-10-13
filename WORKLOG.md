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

## 2026-10-13 (18:19) — YouTube doubles its bar for new channels from February; the process audit finds your queue is still the limit

    Worked (% of the shift): gm 40 · monetization 15 · product 10 · reliability 10 · market 5 · strategy 5 · engineering 5 · data 5 · security 5

**Summary:** YouTube announced in August that from 1 February 2027 a new channel needs 20 million qualifying Shorts views in 90 days to earn ad revenue, double today's bar. Its smaller tier (500 subscribers, 3 million views, unlocking fan funding and Shopping) is unchanged and is now our nearest route. The process audit came due and found the owner's queue is still what holds bet 1 back.

### Toward revenue
- **Nothing shipped to viewers.** Bet 1 still waits on your label (#74), and its sample cannot run before 22:43 tonight.
- **Bet 1's ask is now a glance:** until now, judging it meant downloading a zip from GitHub, unzipping it and playing a silent video, which is hard on a phone. #74 now shows four frames of the sample inline, in the email too: the host's three lines and the closing vote.
- **The target moved:** the plan now records the February change and the smaller tier, about 250 times our current qualifying views, against roughly 800 times for today's full bar. No direction changes on this alone; it goes to the monthly review on 5 November.

### Done
- **Reliability:** every upload since Friday landed; the record of the last upload is intact; tonight's evening run had not started at 18:30, which is normal given GitHub's delays. Two libraries that decide which posts, comments and host lines ship were unpinned, so each run took whatever was published that morning. They are now pinned at today's versions, with a check that fails if any library is ever left unpinned (fixing; reviewed, live).
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.37 this month, forecast $0.88 of $3). New this shift: the logs of every job that holds our keys are public, so I scanned the last 17 for leaked credentials, including the short-lived tokens GitHub does not hide. None found.
- **Monetization and market:** read YouTube's own pages and its 10 August announcement (above). The template risk is also audible: all of the last 30 uploads use the same music track, so the music task on your list now answers a confirmed monetization risk.
- **General management (the audit, 13 shifts since 9 October):** re-reviewed all eleven live decisions, each with a date. Findings: label-only asks used to close within a day and #74 has now waited over two; the rule that a shift cannot read the video job's logs is false (three shifts did it), and its fix waits on #50 because shifts cannot edit their own rules; independent reviews caught real defects in 11 of 13 shifts, while sample videos only prove a video plays; 7 of 13 shifts ended early. New from the tool's docs: a stop guard can no longer loop a shift, so "don't stop before the handover is saved" can become a rule enforced in code, proposed after #50. Bet 1's read and four uploads a day would overlap, so four a day now waits for bet 1's read if bet 1 is still being measured.
- **Dropped after ranking:** whether upload time matters (already answered: it doesn't); a fix for false "missed day" warnings at four a day (it needs each run's slot logged, recorded for after bet 1).

### Blocked
- **For you, in order:** #74 (bet 1: watch tonight's sample, then label); #50 (four commands; it unblocks #65 and the rule fixes above); #75 (comments, one label); #59 (account checks). Adding two or three music tracks now also answers a monetization risk.

### Next
- After 22:43, request the sample of bet 1's branch. It also carries the Groq backup; my recommendation is to let it ride, because it only answers when Gemini fails (about 1 upload in 10) and without it those uploads would ship with no host at all. Bet 1's read can count those uploads separately with the existing report.
- When tonight's sample lands, put its frames on #74 the same way (the image lives on its own branch; keep that branch while #74 is open).
- If #74 is still open at 10:49 tomorrow, the rule about how long your asks wait has fired: the next shift should re-think how bet 1 reaches you rather than ask again.

### Better?
- **Than last shift:** Slightly. Nothing reached viewers, but the company's target is now the real one, bet 1's one remaining step can be taken from a phone, and a silent risk to every live run is gone.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds and bet 1 is still unshipped, though median views at 7 days rose from 64 to 91.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-13 (10:36) — Bet 1 could have shipped some videos with none of its host lines; fixed before it ships, and new evidence that text alone may not pass YouTube's review

    Worked (% of the shift): product 35 · engineering 15 · gm 15 · market 15 · data 10 · reliability 5 · security 5

**Summary:** A test render of what would ship showed bet 1 dropping all its host lines whenever the AI writes one too long, leaving a plain reading; I built a fix so only the long line is lost. On #74 I told you only your label now stands in bet 1's way, along with new evidence that on-screen text alone may not satisfy YouTube's monetization review.

### Toward revenue
- **Indirectly, on bet 1.** Without the fix, some of its uploads would ship with none of our words, weakening both its watch-time read and the channel's case at review. It happened on one sample in four, on the cheaper model samples use; the live model fitted both times checked, so the fix is cheap insurance. Your label on #74 is still the one remaining step.
- **A finding for your next decision on bet 1:** I found no report of text-only commentary getting a channel like ours through YouTube's review. YouTube's own help page calls reactions "without added voice commentary" reused content. Bet 1 is still worth shipping (more of ours, measurable, reversible), but the step after it may need our words spoken, in a voice you accept.

### Done
- **Reliability:** every upload since Friday landed and the last-upload record is intact. GitHub starts our scheduled jobs 6 to 9 hours late, in its own scheduler, so nothing we can fix. Security standing check clean: no secrets in the project, no workflow change, money controls in place ($0.37 this month, forecast $0.88 of $3).
- **Product (bet 1):** brought Groq's backup branch up to date and had it rendered. It plays, but one host line ran over its length limit, so the rule dropped all four. I built a fix: an over-long note is left out alone, an over-long vote falls back to the usual closing line, and only with no note left is the video today's reading. A fresh review found no bugs and one real risk: the upload log would have marked a partial host the same as a whole one, so a later read could not tell them apart. It now records how many host lines each video showed. The review also caught a wasted narration charge when the closing line was already the usual one; fixed. A second review's two small points are fixed. Bet 1's verdict will now also say how many of its videos showed all, some or none of the host lines (never a trigger; reviewed, no changes). 543 tests pass, and a local render with one note dropped shows no empty box. The daily release check now tests this branch and warns on a dropped line. It needs its own sample (the next is possible after 22:43 tonight) before it merges.
- **General management:** with both ready items waiting on you, I generated eight candidates from the flat watch time, the risk list, stalled decision rules and uncovered functions, ranked separately forward and reversed. Both orders put first: updating #74 (it said bet 1 would ship "after Monday's read", now done) and sampling the whole bet 1 stack. Both done.
- **Data:** whether any background clip loses more plays in the opening can't be read yet (two to seven uploads per clip). Bet 1's committed read runs as written. Bet 2: 9,158 views in the last four weeks against a 16,600 bar, so it depends on four a day landing in November and holding about 150 views per upload; whether closer uploads dilute views can't be read ahead, since 80% of our gaps are 11 to 13 hours.
- **Market intelligence (its first work):** the review evidence above, from YouTube's own pages, a YouTube spokesman (July 2025), one demonetized Reddit channel (May 2026) and two industry blogs.
- **Product:** a fresh review of the whole bet 1 branch found nothing blocking; its quick fixes are in, and a short display time for the first note waits for your label.
- **Data (engineering):** closed a code-health item: the report now refuses a filter pairing it used to ignore silently; the item's other half proved already handled (reviewed, merged).
- Dropped: a known safety-screen gap (never seen in practice); the comment-reply format (waits on #75); measuring Groq's long lines (no AI keys here). Awkward again: the rules say a shift cannot read the video job's logs, yet I read the sample's directly; left for the next audit. Fixing against improving: mostly fixing (bet 1's long-line loss and its logging); improving: the market read.

### Blocked
- **For you, in order of what each unblocks:** #74 (bet 1, one label, now with the evidence above); #50 (four commands); #75 (comments, one label, then close #53 unapplied); #65 (applies once #50 is in); #59 (account checks).

### Next
- After 22:43 tonight, request a sample of the fix branch, which carries all of bet 1, its follow-ups and Groq's backup. On a pass and your #74 label, merge it as `v8` in one step.
- Once `v8` is live, check how often its uploads lose a host line (the new host-lines column).
- A lead for after bet 1: YouTube also refuses content that "looks like it's made with a template", and every video has the same shape; varying it may matter as much as our words. A proposal once bet 1 has a read.

### Better?
- **Than last shift:** Slightly. A flaw that could have diluted bet 1 was caught before shipping, and the review risk is in front of you. Nothing reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is flat at 12.0 seconds; bet 1 is unshipped.
- **Than ~100 shifts ago:** Too early to say.
