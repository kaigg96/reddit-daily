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

## 2026-10-28 (10:35) — One passing YouTube error can no longer lose an upload or ship a post twice; the next two coin-flip tests get a fairness check first

    Worked (% of the shift): reliability 55 · data 25 · gm 15 · security 5

**Summary:** The upload is now protected end to end. A passing error from YouTube no longer loses that run's video, and a blip just after a video goes live can no longer leave it unrecorded, which could have uploaded the same post twice. Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting what we publish.** No upload has been lost or repeated this way yet, but each was one network blip away. A repeated video is the kind of thing YouTube's spam rules count, and a lost one costs a day's test data. Bet 1 adds four columns to the upload log, so its first live run rewrites that file; the rewrite can no longer damage it.
- **Keeping two tests honest.** The voice question (2 November) and the one-capital-word title test (about 23 November) each compare two groups that chance filled from different subreddit mixes. A check now shows how different, from assignments alone without seeing any result. Today both gaps are within chance. A rule, set before either read, says what happens if they are not.

### Done
- **Reliability (fix, live):** the upload retry is merged. A fresh review ran the real upload library against a pretend YouTube server and found two kinds of dropped connection the retry still missed; both are covered, and the tests now run the real library, so an upgrade cannot quietly break it. Videos run 3–11 MB, one request each. Merged at 09:48, eight hours before the next upload.
- **Reliability (fix, live):** after the upload, the thumbnail, captions and comment each sign in again. Any of those six network requests failing crashed the run after the video was live, so nothing recorded it and a later run could have uploaded the post again. They now carry on and flag a warning. Reviewed; its findings fixed.
- **Reliability (fix, live):** the same for the last step, writing the upload log: it now cannot crash the run, and a failure part-way can no longer leave a damaged file. The first review found that this fix itself could have saved half a row; that is prevented and checked. Bet 1's release still combines with everything live; all 933 checks pass.
- **Data (built and live):** the fairness check, and the rule for the two reads. Two review passes; the second caught wording that a later shift could have read two ways, now exact.
- **General management:** nothing was ready. A fresh agent proposed seven ideas; two rankers, in opposite orders, both put the post-upload fix and the fairness check in their top three. **Dropped:** a map of the Partner Program's review criteria (every one already has an answer, AI disclosure settled on 18 October); longer videos and reach (answered 7 October for 15–31 seconds, and no upload has run longer); due dates in the test ledger (the dates are known); a rule for judging a lifted reach cut (applies only if 2 November finds a cut). A second round, aimed at the functions this shift did not touch, asked whether our music track halves our cut of Shorts revenue: YouTube's page says music shrinks the pool all creators share, but each creator's share still counts all its engaged views, so the earnings estimate stands. Also dropped: the revenue-route report's TikTok line (it already shows our 0 followers against 10,000) and the voice cost of each replacement source (cents a month, so it cannot decide 5 November). The start of a run is covered too: fetching from Reddit already retries a passing error. The test ledger now dates the title-style read to 2 November (27 against 14 videos, counted without any result), so a late read would show. GitHub moved its build machines to a new system this morning; Monday's analytics job is no risk, as this morning's upload set up the same Python on it.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.78 this month, forecast $0.88 of $3).
- **Reliability:** yesterday's two uploads and this morning's landed. A free sample of today's code renders and plays. #50's patch still applies to the current code as written.
- Three fixes and one measurement live. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **This evening's upload** is the first on today's code: check its log row, and that the run shows no warning. A warning means a step after the upload failed and was survived; read it.
- **2 November snapshot:** as the 23:45 handover says. Before the voice read, run the fairness check its rule names, counting only the uploads that read will see, and apply the rule as written.
- **If #77 is labelled:** merge the release, then the counting fix built beside it (the technical list names both), set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how).

### Better?
- **Than last shift:** No for viewers or revenue. Yes for safety: an upload can no longer be lost, or repeated, by one passing error.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-27 (23:45) — Your ledger decision is live; Monday's figures, which four test reads depend on, are now protected from a one-off YouTube error

    Worked (% of the shift): reliability 30 · data 25 · gm 20 · legal 10 · strategy 10 · security 5

**Summary:** The experiment-ledger wording you approved (#85) is live. Last Monday YouTube's reporting service failed once and the weekly figures lost nearly every video's subscriber count without anyone noticing; that can no longer pass silently, and a repeat on 2 November, when four test reads are due, is now retried. Nothing viewers see changed, and nothing moved revenue directly.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the evidence.** Every bet is judged on the Monday figures, and a lost week cannot be fetched later. On 26 October one "internal error" from YouTube cost nearly every video its subscriber count; on the first requests it would have cost the whole week, including the four reads due on 2 November. Each request now tries up to three times.
- **One more fact for 5 November.** AI use does not decide between replacement sources at two a day (2–5 requests per video for Reddit and Stack Exchange, 2–3 for our own questions, against 20 a day); at four, the first two reach the cap on a bad day.

### Done
- **General management (your decision, #85):** landed as one approved commit at 23:00 UTC; #85 is closed. Quarterly preparation now quotes the ledger before proposing any bet's rule, and every rule set or read updates its row; first read in early January.
- **Reliability (three fixes, live):** every request the Monday jobs make to YouTube now retries a server error, as one kind already did after 19 October, including the 22-page list of our videos that comes before any figure, and your check-in's own requests. Fresh reviews found no bugs; each found a request still left out, now covered. The three libraries that job installs without fixed versions work at their newest releases, so are no risk for Monday unless one ships first.
- **Reliability (built, not merged):** the upload itself has no retry, so one passing YouTube error loses that run's video. Two reviews each caught a flaw in the library's own retry; the branch now resumes as YouTube's example does, which cannot make a second video. Not merged at 23:40, just before a scheduled upload.
- **Data (three fixes, live):** the reports said "insufficient data" about subscribers when the truth was "YouTube refused the request". Our rules tell a shift to accept a report's refusal as the answer, so a failed collection would have read as too few videos. They now say it was not collected. Your Monday check-in, which said "ran clean" that day, now names any refused figure. Test reads dropped a refused figure silently too; each now warns (today: 11 videos' subscriber figures). Fresh reviews found no bugs. To check the warning I ran the voice question's command filtered to warnings only, so none of its result was seen early.
- **Legal (for #82):** its description now lists the questions on Reddit's API request form, from an archived copy (Reddit refuses automated reads); editing sends no email. One choice is yours: "developer" or "commercial developer", which asks for a monthly data budget. I recommend "developer", saying plainly that the videos go on YouTube, earn nothing today, and that we would ask Reddit before earning from them, as you decided on 10 October. A news check of Reddit's and YouTube's rules found nothing new; Reddit's $1,000 migration bounty is for community tools, not us.
- **General management:** #65 stays open: your label predates its corrected sentence and has no reply since; a "yes" lands it.
- **Reliability:** both of today's uploads landed. Bet 1's release still combines cleanly with everything live.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.78 this month, forecast $0.88 of $3).
- **General management:** nothing was ready. A fresh agent proposed eight ideas, finding the refused subscriber counts; two rankers, in opposite orders, put the same three first. **Dropped:** a topic test chosen after seeing the data (both rankers last); counting deleted Reddit posts (Reddit refuses our build machine); why likes per 100 views rose (under one like per video).
- Six fixes live, one built, two findings. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January; the form's questions are now on it); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **2 November snapshot:** check first that the Monday check-in names no figure YouTube refused, and read each test's warnings before its verdict; the voice question reads engaged views. Then the views rule, the subreddit test, the title-style test and the voice question; all should have enough videos (20 a side; 27 against 14; 21 and 17), counted from the upload log without reading any result. Record each read in the ledger.
- **The upload retry** (its branch's last commit): a fresh review of that commit, a check that a render fits its 100 MB request, then merge early in a shift and watch the next upload land.
- **If #77 is labelled:** merge the release, then the counting fix built beside it (the technical list names both), set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how). **If #65 gets a yes:** land the corrected sentence as one commit with the approval line.

### Better?
- **Than last shift:** No for viewers or revenue. Yes for the evidence: a one-off YouTube error can no longer quietly cost a week of test data, and a failed collection no longer reads as "too few videos".
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---
