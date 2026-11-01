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

## 2026-11-01 (22:50) — Election week can no longer fail an upload: the fix is live a day early. Bet 1's branch is current again, and the watch-time question is set for Monday

    Worked (% of the shift): editorial 30 · data 35 · engineering 15 · gm 10 · reliability 5 · security 5

**Summary:** The election-week fix merged tonight instead of tomorrow. A results-day upload no longer fails when Reddit's top questions are all about the election. Nothing moved revenue directly: bet 1 still waits on #77, and I brought its branch back in line with tonight's change so your label still ships it in one step.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view, and bet 1 is still the only answer to that.
- **Protecting the uploads.** The election fix is live from the next upload, about 06:00, two days before the polls close.
- **Checking that we measure the right thing.** Every test is judged on how long people watch, but revenue needs views. In August, watch time was the best predictor of views we had. Monday's figures will show whether it still is, judged by a rule I wrote down tonight before looking at any number. If it no longer predicts views, a watch-time gain stops counting as progress toward revenue, and the November monthly brings that to you.

### Done
- **Editorial (fix, live):** the last shift timed the election fix's sample video for tomorrow at 11:17. The 12-hour limit on samples actually lifted at 23:09 tonight, so I asked then. It passed: the video plays (32 seconds, picture and sound). I merged it. All 719 checks pass. On an ordinary day nothing changes. When election week leaves no usable question in the day's top 10, the run reads the top 30 instead of failing.
- **Engineering (fix):** merging that fix left bet 1's waiting branch in conflict with it, so your label on #77 would have stalled. I combined the two by hand, keeping bet 1's medical-topic skips where they were. All 973 of that branch's checks pass, and tomorrow's 08:17 release check re-tests it. A fresh review found nothing wrong. It confirmed that git's automatic merge would have crashed the run at the first usable post, and that the hand fix avoids it.
- **Data (rule set, read Monday):** a new report compares each upload's watch time with its views at about a week old, for uploads since 5 October. There are three outcomes: they rise together, they move in opposite directions, or there is no link. A fresh review found no fault and three small points; all three are fixed. It is on main.
- **General management:** the election fix was the only ready item. Five hours ago the 17:45 shift ran two rounds of ideas and named the watch-time question as the best one left. No new data has come in since, so I took that question rather than generate ideas again. With nothing ready after it, I looked once more, only at what tonight changed, and found nothing above the bar. Dropped: a check that every merge keeps bet 1's branch mergeable (each shift's start already runs it, and tonight's break was caught within a minute); removing the election code after 10 November (it switches itself off). Two of tonight's three items were fixes, and one improves how we judge our tests.
- **Reliability, security:** both of today's uploads landed. No workflow has changed since 20 October, and no secret is in the repository. The money controls are in place ($0.01 so far this month, forecast $0.76 of $3).
- AI use: none from the upload allowance; no Polly; one sample video, on the test model's allowance.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #82 (register by 12 January; check the app's name first); #86 (very likely not needed: close it); #65 (it still waits for your "yes" to the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Morning, from about 06:00:** check that the first upload under the election fix landed. A pick ranked 11 or lower means it read the top 30.
- **The 11-02 snapshot, then the weekly review:** read the watch-time question once. The voice test and the second-low-week check are due that day too. Then the November monthly; its single proposal carries the upload alarm's one-step change.
- **08:17 release check:** confirm it passes on bet 1's updated branch.

### Better?
- **Than last shift:** A little, for safety, not for viewers. The election fix is live rather than waiting, and bet 1 still ships with one label.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-11-01 (17:45) — Election week could have failed an upload outright; the fix waits only for its sample. A lasting upload alarm is built, and this morning's #86 ask is very likely not needed

    Worked (% of the shift): reliability 40 · editorial 30 · gm 20 · market 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Two upload risks in the unwatched days around the election are now covered or ready: a run that finds no usable question, and a missed upload whose run never started, which no email reports.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the uploads.** Around results day, Reddit's top questions may nearly all be about the election, which we skip. Today such a day fails the run and loses that upload. The fix is built and reviewed. It needs one sample video, which the rules allow from tomorrow at 11:17.

### Done
- **Editorial (fix, ready):** when the election skip leaves none of the day's top 10 questions usable, or our safety check rejects the few that are left, the run now reads the day's top 30 instead of failing. The same filters and the same cap on AI checks apply. An ordinary day is unchanged. NoStupidQuestions sometimes has only 2 usable questions out of 10 even without the skip. Its first review found no fault and two gaps, both now fixed. A second review ran the old and new code side by side on 3,000 simulated days each: ordinary days matched exactly, and of 226 election-week runs that would have failed, 108 now upload. Uploads that came from the deeper list are marked, so they cannot blur a running test. 714 checks pass.
- **Reliability (built, for the monthly):** a check in the shift job, which runs on your schedule three times a day even when the shift allowance is spent. If fewer than 2 uploads landed in 28 hours, or a scheduled upload run failed, it fails that job, so GitHub emails you. Replayed over the 95 shift runs since 20 September, it raised no false alarm and caught the one real miss, on 5 October. A fresh review found two gaps, both fixed. It is on main but does nothing until your label adds one step to the shift job. To save you a separate email, that step joins the single proposal the monthly review brings you.
- **Reliability (correction, by edit, no email):** this morning's #86 said a failed upload emails no one. That is very likely wrong. GitHub's documentation sends the email to whoever changed the schedule, and GitHub still names you on every scheduled upload run since 11 October. The automatic approver pushes with a personal token, so to GitHub the change was yours. I cannot see who gets the emails, so this is not proof. #86 now says no action is needed.
- **Market (checked):** Reddit stops its public RSS feeds on 13 November. We read Reddit through its registered API, not RSS, so this does not touch us. YouTube's monetization page, read first-hand, still has the wording our plan quotes on readings of others' text, AI personas and shock content.
- **Editorial (answered):** the election skip reads titles only. In 993 past videos, 5 had an election word only in an answer, and none of those was about when or how to vote. So answers need no screening.
- **General management:** nothing was ready. A fresh agent proposed 8 ideas and I added one. Two rankers, reading them in opposite orders, both put the election fallback and the lasting alarm first and second. Dropped: re-checking Monday's libraries (none has a new release since 28 October); a security audit of our libraries (six days after the last, and the tool is not installed); a check on quoted review dates (no effect on any decision); fixing a comment about the clock change (no shift starts in that hour); tallying hype-word titles (the wider guard waits for bet 1's release, so a count now changes nothing). A second round, on the functions this shift missed, found nothing that clearly clears the bar. The closest is below, under Next. Also considered: bet 2's bar is 1.16 times our best four weeks on record, so at two a day it needs a record month (context for the monthly, no decision); a reading rule for the new subscriber share; a required-growth line; the two replacement-source samples expiring on 8–9 November; halving the voice bill (it changes the captions, needs a release, and saves cents).
- **Reliability, security:** this morning's upload landed; this evening's had not started when I handed over (it usually starts between 17:15 and 18:30). No workflow changed. Money controls are in place ($0.89 this month, forecast $0.90 of $3).
- AI use: none from the upload allowance; no Polly; no sample video (the 12-hour cap).

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #82 (register by 12 January; check the app's name first); #86 (very likely not needed: close it); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Tonight's 19:17 shift:** the best open candidate is whether watch time still predicts reach. Every bet is judged on watch time, but revenue needs reach. Set its rule before Monday's figures arrive (about 06:00), then build the read (about 35 minutes).
- **Tomorrow's 11:17 shift, first thing:** request the election fallback's sample video and merge it on a pass, before the polls close on 3 November. It is the only ready item.
- **The weekly, then the November monthly:** the monthly's bundled proposal now also carries the upload alarm's one-step change.
- **Once the alarm's step lands:** check that the shift job printed "uploads ok", then close the technical-list item.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: a results-day upload no longer fails once the fix merges, and a lasting alarm is one label away.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
