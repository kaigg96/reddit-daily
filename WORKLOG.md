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

## 2026-10-28 (17:35) — The process audit: unchanged since 25 October, the company waits on bet 1; a gap that could have leaked a token into a public file is closed

    Worked (% of the shift): gm 45 · security 15 · reliability 15 · legal 10 · engineering 10 · editorial 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly. Bet 1 still waits on your label (#77). The process audit came due and found the same picture as three days ago: shifts keep the system safe while the one change that matters waits on you. It also found and closed a gap that could have put a working token into a public file.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Bet 1 is ready the day you label it.** Today's live code, the release and the counting fix built beside it combine with no conflicts, and all 936 checks pass.

### Done
- **General management (the audit, due after about ten shifts):** eight shifts since 25 October ran 26 to 61 minutes of 60 (38 on average, as before). Six of eight were fixes, and the two changes viewers saw were protective. Of the last audit's findings, the self-grading is fixed (these reports now answer "No for viewers" first); the rest stand because they wait on bet 1 or on you. New: the product plan's findings section has nearly doubled in ten days and nothing caps it; these reports run about 1,000 words, so only the last two survive for the next shift; six ideas were dropped twice by different shifts; and a recommendation to you went in before its premise was checked (below). Every decision was re-tested and dated; one, settled in the rules, was cut to a line. Proposals go to the 5 November review, not to you now.
- **Security (fix, live):** a helper agent printed the build machine's settings, keys included, into its own working notes. Nothing left the session: the build page hides agent output, and the record each shift commits lists only the shift's own steps. But checking that record showed one token, the machine's own GitHub token, would only have been partly blanked if a shift had ever printed it. Fixed, tested, reviewed and live. No key needs changing.
- **Reliability (check):** a networking component under YouTube's libraries updated at 10:21 this morning, and Monday's job and every upload install it fresh. It only drops a distrusted certificate Google does not use; every Google service we call works on it, and every check passes on Monday's exact versions.
- **Legal and editorial (question closed):** 12 old videos repeat another word for word. I first recorded them as worth removing; a second check found them already private since at least 12 October, so I corrected it within the hour. Other repeated questions read different answers. Nothing to do.
- **General management (your decisions):** our rule on slow answers came due. On 27 October you approved two process items within hours and passed over #77 and #80, so the delay is in asks needing a judgement or a watch, not absence. No re-ask.
- **General management:** nothing was ready. Two rounds of ideas, ranked in opposite orders, gave the library check and the duplicate count. **Dropped:** bet 1's "no tags on fallback days" option before you ask (the rankers split); removing YouTube's text from an old file (5 November decides); filling 82 missing topics and a list of 2 November's rules (change no decision); tying approvals to their issue (your workflow file). A second round sought anything that changes what we ship or earn without disturbing the running tests or needing you: playlists, descriptions, the language setting, more music, a new source. Each failed on a recorded finding, the tests, or you: only #77 changes what we ship.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.79 this month, forecast $0.88 of $3).
- **Reliability:** this morning's upload landed. The safety screen has skipped 1 post in two months, far under the line where it would need narrowing. This afternoon's upload had not started by the handover.
- One fix live, one audit, two checks, one closed question. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **This afternoon's upload** is the first on today's code and on this morning's library update: check its log row, and that the run shows no warning.
- **2 November snapshot:** first check that the Monday check-in names no figure YouTube refused, and read each test's warnings before its verdict. Then the views rule, the subreddit test, the title-style test and the voice question (it reads engaged views); each should have enough videos. Before the voice read, run the fairness check its rule names, counting only the uploads that read will see. Apply each rule as written and record each read in the ledger. Read the scorecard's zero-view guardrail again: a second breach is a decision's revisit trigger.
- **If #77 is labelled:** merge the release, then the counting fix (both rehearsed today), set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how).
- **5 November monthly:** the audit's proposals (the technical list): compress and cap the findings section, a length cap for these reports, one decision ready to retire into the rules, with the bundle carried from 25 October.
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: one token can no longer leak through the shift record.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-28 (10:16) — One passing YouTube error can no longer lose an upload or ship a post twice; the next two coin-flip tests get a fairness check first

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
- **General management:** nothing was ready. A fresh agent proposed seven ideas; two rankers, in opposite orders, both put the post-upload fix and the fairness check in their top three. **Dropped:** a map of the Partner Program's review criteria (every one already has an answer, AI disclosure settled on 18 October); longer videos and reach (answered 7 October for 15–31 seconds, and no upload has run longer); due dates in the test ledger (the dates are known); a rule for judging a lifted reach cut (applies only if 2 November finds a cut). A second round, aimed at the functions this shift did not touch, asked whether our music track halves our cut of Shorts revenue: YouTube's page says music shrinks the pool all creators share, but each creator's share still counts all its engaged views, so the earnings estimate stands. Also dropped: the revenue-route report's TikTok line (it already shows our 0 followers against 10,000) and the voice cost of each replacement source (cents a month, so it cannot decide 5 November). The start of a run is covered too: fetching from Reddit already retries a passing error. The test ledger now dates the title-style read to 2 November (27 against 14 videos, counted without any result), so a late read would show. With nothing above the bar left, I handed over at 10:16. GitHub moved its build machines to a new system this morning; Monday's analytics job is no risk, as this morning's upload set up the same Python on it.
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
