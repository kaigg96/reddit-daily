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

## 2026-11-13 (11:58) — Bet 1 has passed every check a shift can run; your label now ships it within about a day

    Worked (% of the shift): product 40 · gm 20 · reliability 15 · engineering 15 · data 5 · security 5

**Summary:** Bet 1, the step every revenue plan waits on, now has its sample video and a fresh review of the exact version your label (#77) ships, and neither found a problem. Only the daily automatic check is left, so your label is the only thing between bet 1 and viewers. Nothing reached viewers today.

### Toward revenue
- **Bet 1 is one label from shipping, with nothing else in the way.** Before today, a label would have started a day or more of checks. Now the sample and the review are done, and the automatic check runs this afternoon. Bet 2, doubling weekly views, needs bet 1 by about 20 November.

### Done
- **Product (sample video, PASS):** I brought bet 1's release up to date with the live code (all 1,137 tests pass) and had its sample made: 24.5 seconds, playable. It closes on the host's pick, "I raise my hand for the suffering SREs. Which answer gets your vote?" It is read aloud by a free stand-in voice, because test versions never hold our paid narrator's keys, so you can follow it by ear, as you asked on #77 in October. At first I wrote on #77 that it was silent, and I corrected that at 11:35. Our check left out the host's note under the question, and the run skipped a health thread for the next post, both as planned. I looked at its frames too: the question, the answer count and the captions all show correctly. I added the link to #77 by editing it, so you got no extra email. The video stays downloadable until 27 November.
- **Product (fresh review, no blockers):** a fresh helper read the whole release against the live code. Nothing in it can cause a double upload or lose our record of what we've posted. The money and safety controls are unchanged, and every retry has a limit. It left four small notes, which I wrote into our code-health list. The one worth knowing: on a day when several top threads are health ones, a run could find no usable post and skip an upload. That is about 1 in 400 runs, against about 1 in 1,200 today. Fixing it would cost AI requests, so it waits until a run actually misses.
- **Reliability (a check, all clear):** the new AI model's first week was to be watched for running out of its daily allowance. Its 10 uploads so far never hit any limit. Two hit Google's brief overload errors, and both still uploaded.
- **Engineering (ready for after bet 1):** two follow-on changes must go in right after bet 1. One logs which time slot each upload was meant for, which four uploads a day needs. The other fixes how bet 1's verdict counts its videos. I brought both up to date and checked that bet 1 and both of them merge into the live code cleanly, with all 1,141 tests passing.
- **General management (ranking):** a fresh helper proposed eight ideas from our data and plans, and two others ranked the survivors, forwards and reversed. Both put the allowance check first, then the follow-on changes. Dropped: an early count of the new model's over-claiming titles (its rule forbids a count before the 20th upload, about 18 November); two new data questions (the open ones are answered or wait on snapshots not yet taken, and morning against evening uploads was answered earlier); a fourth attempt at the backup show's title check (over an hour, and needs AI requests); deleting YouTube text we keep too long (needs you, set for the 7 December review); a closing line asking for subscribers (our findings say no subscriber lever reads within a quarter); posting to TikTok (new platforms are yours). One more I checked: our single music track can't explain the rise in buried uploads, since every upload since July used it.
- **Data (a gap in bet 1's rules closed before any data):** two side measures in bet 1's rules, how much of each video people watch and where they leave, didn't say what bet 1 is compared with: the older format alone, or the new AI model's weeks too, as its main verdict is. Picking after the figures arrive would let us pick the answer we like. They now compare with both pooled, matching the verdict. No bet 1 video exists yet, so no result could have swayed it.
- **Security and reliability (checked):** yesterday's two uploads and this morning's landed. The money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret is in the repository, and the workflows are unchanged.
- **General management (an ask kept true):** from bet 1 on, each test video asks the model that writes our real titles for one request. The wording #65 awaits says it doesn't, so I noted that on #65 without emailing you; a shift rewords it before landing it.
- AI use: one sample video (a free stand-in voice; a few AI requests, one from the uploads' allowance); no Polly.

### Blocked
- **For you, in order:** #77 (one label; nothing to watch, though the sample is there), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 on this afternoon's automatic check (it runs about 16:00–17:00 UTC on the sampled version). Don't update the release with the live code before then: a new version would need a fresh sample. Then merge the verdict-counting fix right away. The time-slot logging goes in after bet 1, before four a day.
- **If the automatic check can't reach Google again,** it retries the next day. That is not a failure.
- **16 November:** the weekly review. **About 18 November:** the new model's 20th upload, and the title counts set for it. **23 November:** the capitals test's read, if its lock opens.

### Better?
- **Than last shift:** yes, a little. A label on #77 no longer starts a day of checks: the sample and the review are done. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-13 (01:00) — The capitals test can no longer be read on too few videos; the security ask now opens with two five-minute checks

    Worked (% of the shift): data 55 · gm 20 · security 20 · reliability 5

**Summary:** The shift started with nothing ready. It made sure our one live test of a views lever, capitals in titles, is read only once both halves hold the 30 videos its rule needs. It also cut the start of the security ask that guards our one fatal risk down to two five-minute checks. Nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. The capitals test is our only live test of a views lever, the measure bet 2 is judged on, and its verdict decides whether every title gets a capitalised word. Tonight's fix keeps that verdict from being taken on too few videos.

### Done
- **Data (fixed, live):** the capitals test's rule says it is read at 30 videos per half. The lock that stops anyone peeking opened on its date, 23 November, whatever the halves held, and the capitals half was on course to fall one or two short. The lock now stays shut until both halves hold 30 in the exact set of videos the read uses. It counts only which half each video was in, never how it did. On today's numbers the read most likely still happens on 23 November; there is about a 1-in-5 chance it moves to 30 November. I wrote that into the plan before anyone looked at a result. Three fresh reviews checked it. The first two each found I had counted the read's videos wrongly, and I fixed both before merging. All 864 tests pass.
- **Security (an existing ask made easier, not a new one):** the quarterly account check (#59) is the only guard on our one fatal risk: losing the Google account, and with it the channel. It has waited on you since 6 October. It now opens with the two checks that matter most, about five minutes together: 2-step sign-in on the Google account, and the list of apps connected to it. The other four follow, unchanged. I edited the issue rather than commenting, so it sent you no email.
- **General management (ranking):** a fresh helper proposed eight ideas from our data and plans, and two others ranked them, forwards and reversed. The capitals-test fix came in the top two both ways, so I did it first. The security rewrite split them (first and fourth), so I did it second. Dropped: a tool to read the new AI model's titles from the upload runs' records (my reason, that shifts can't read those records, was wrong: at 00:58 I read them, so it is ready for whoever does that count, below); whether the new model lets through more questions about named people's misconduct (about 10 uploads, too few to tell); titling the backup show with our own question (it needs a sample video and a product choice); fixing in advance how the 20 November bet-2 update is worked out (its rule already says, and one command gives the figure); a test run before each push (it needs files only you can change); and sorting the friction log (Monday's review does it). A second, narrower round at 00:56 found two more, and both came back "no change" within minutes. Will the new AI model's read around 25 November have the 20 videos it needs? Yes, about 22, if no run is missed. Can its count of refused shock phrases come from our own upload log instead? No: the log can't tell those from other refused titles, showing 3 of the old model's last 30 where the records show 2. The title-reading tool could not have been built, reviewed and merged safely in the 20 minutes left, and the count it serves takes a shift about five minutes by hand. So I handed over at 01:00, 23 minutes early.
- **Data (a figure, not a finding):** views over the last four weeks were 12,238, against 9,158 over the four before. That is ×1.34, under the doubling our report counts as a change, and it comes mostly from one strong week. At this pace, two uploads a day reach about three-quarters of bet 2's 16,600 bar.
- **Security and reliability (checked):** both of yesterday's uploads landed. The money controls are intact ($0.31 this month, forecast $0.79 of $3). No secret is in the repository, and the workflows are unchanged.
- **General management:** my rule took the product plan's status section 49 words over its limit, so I shortened it back under. The open code-findings list is still one over its cap, as it was at the start. Neither item that could close is ready to, and I added none.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (now five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **This morning's 11:17 shift:** request bet 1's sample video whether or not #77 is labelled (yesterday morning's plan stands). In winter, Gemini work waits until after 08:00 UTC.
- **About 18 November, the new AI model's 20th upload:** the counts set for it (titles that claim more than the question, refused shock phrases, closing lines that repeat) read the upload runs' records, which a shift can read.
- **16 November:** the weekly review; it sorts the friction log's 26 ungrouped entries.
- **23 November:** the capitals test's read, if the lock opens. If it stays shut, move the test's due date to 30 November and read it then.

### Better?
- **Than last shift:** no, not toward revenue. A verdict on a views lever can no longer be read too early, and the fatal-risk ask costs you less. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
