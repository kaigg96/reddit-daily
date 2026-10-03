# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

**Entries are emailed to the owner verbatim as the shift report.** Write for a
manager, not an engineer: plain language, no filenames, no jargon. Technical
detail belongs in the commit message and `TECH_DEBT.md`, which is where the
next shift looks. Follow this template exactly — the report is generated from
its structure:

```
## 2026-09-21 — one line on what actually mattered

    Allocation (planned→actual %): rounds 10→8 · maintenance 15→25 · security 10→5 · pm 15→12 · research 10→0 · feature 30→40 · close 10→10

**Summary:** Two sentences. What the shift achieved, and why it matters to the
channel. No detail — this is the part read on a phone.

### Maintenance
- One bullet per thing done, in plain words.

### Security
- Nothing this shift — the standing checks were clean.

### Project management
- Nothing this shift — no decisions came due.

### Research
- Nothing this shift, because maintenance took the time.

### Blocked
- What is stuck, and what it is waiting on.

### Next
- What the following shift should pick up.

### Better?
- **Than last shift:** yes/no/unclear, and the specific thing that is better.
- **Than ~10 shifts ago:** same, naming evidence rather than impression.
- **Than ~100 shifts ago:** same, or "too early to say".
```

**On the "Better?" section.** Numbers lag and no single one judges this channel
(`report.py --scorecard`), so a subjective read is part of the record — but a
shift grading its own work is exactly the bias the research warns about. Two
rules make it worth having: answer **comparatively** against a named horizon
rather than rating out of ten, and **name the evidence**, not the feeling.
"Unclear" is a real answer and more useful than a confident guess.

**Every workstream gets a heading, including ones that did nothing** — with a
one-line "nothing this shift, because …". Silence and inactivity must not look
alike, and the report flags a missing reason rather than hiding it. Routine
checks and wrap-up are overhead and need no section. **The planned and actual
columns must each total 100%**; the report shows the sum and flags it if not.
Read the allocation series with
`venv/bin/python scripts/context_budget.py --allocation`.

---

## 2026-10-03 (14:21) — the new-subreddit sample video passed, so both 6 October changes are ready

    Allocation (planned→actual %): rounds 10→15 · maintenance 10→5 · security 5→5 · pm 30→25 · research 20→20 · feature 15→20 · close 10→10

**Summary:** A short shift that did the one thing due today: the new-subreddit sample video, which only proves anything after noon on 3 October. It passed, so both changes aimed at views can merge on 6 October.

### Maintenance
- Both uploads since the last shift landed (last night's and this morning's), and the saved last-post record is intact. Today's release check passed.
- The ageing Python version reaches end of life tomorrow. Nothing breaks then; its upgrade is already scheduled after 12 October.

### Security
- No credentials in the project and the secret files are still excluded. The library-advisory scan was not rerun (its tool is not installed here); yesterday's stands.

### Project management
- **Requested the new-subreddit sample video.** The branch needed no update first: the main code has not changed since. Verdict under Feature work.
- No decisions came due and you have approved nothing new; your open question is still the one about letting approved process changes apply automatically (#45). The channel is still flat on watch time, and both changes aimed at views are queued for 6 October, so nothing new was added.
- **Ready work is now none against a floor of three:** the new subreddit, the last ready item, waits only for 6 October. The questions under Research were the candidates; none cleared the bar.
- **Friction:** the doc check flags yesterday's entry about #44 as stale, though what it describes is still true. It reads past log entries as current claims; it clears as the entry ages out.

### Research
- Three new questions, tested on our own data, all came back as noise: no background clip holds viewers measurably longer; one title style looked 18% worse, but the gap reverses between periods; and questions that say "you" hold viewers no longer. Recorded so they are not re-asked.

### Feature work
- **The new-subreddit sample video passed** (playable, sound, no gaps). It drew the day's top post from the new subreddit, so it tests the real path. It can merge on 6 October after the title change.

### Blocked
- Automatic landing for approved process changes is waiting on your decision (#45).

### Next
- **5 October:** read the new data (voices within the newest format, the engaged-view column). **6 October:** merge the title change (its sample passed), then the new subreddit (its sample passed today). **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment, then plan the Python and image-library upgrade as its own release.

### Better?
- **Than last shift:** about the same. This shift's one job was time-locked and is done; last shift fixed a live fault.
- **Than ~10 shifts ago:** unclear. The channel is still flat, and the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-10-02 (15:52) — a momentary outage no longer costs an upload its title; your sample-timing decision is acted on

    Allocation (planned→actual %): rounds 10→10 · maintenance 20→35 · security 5→5 · pm 35→30 · research 15→5 · feature 5→5 · close 10→10

**Summary:** Last night's upload went out with the raw Reddit question as its title because the title service had a one-off outage, and nothing retried it. That is fixed and live. Your decision to let shifts request sample videos at any time has been acted on, and the title change due on 6 October passed its sample video.

### Maintenance
- Both uploads since the last shift landed, and the saved last-post record is intact. Last night's upload carries the new "why the content check fell back" field, blank because the check worked.
- **Shipped:** last night's upload lost its generated title, search keywords and closing line to a single "service busy" reply. The new record named the cause, its first use. The content check already tried a second time after that kind of reply, but the title request did not. Both now follow the same rule: one more try after a short pause, and never a retry when the daily allowance is used up, since that only wastes what is left. All tests pass. The video itself is unchanged.
- Today's release check could not reach the content service, for the same reason, and said so rather than failing. Nothing to act on.

### Security
- Standing check clean: no credentials in the project, the secret files are still excluded, every automated job still has limited permissions, and the only known library advisories are the image-library ones already scheduled after 12 October.

### Project management
- **Your decision on sample timing (#44) is done and closed, with one part left for you.** Shifts now treat the old timing rule as retired. But the rule's wording is unchanged, because shift sessions cannot edit the process files. Automatic applying works only for workflow files, so an approved process-file change has no way to land without you. The issue says what to paste.
- The new-subreddit sample can now be requested tomorrow afternoon. The rotation draws the new subreddit after 12:00 UTC on 3 October and before 12:00 on 4 October.
- Ready work is still one item against a floor of three. I considered whether Reddit's top post does better than its runners-up (4 cases, minimum 8, already tracked), whether subscriber gains follow watch time (per-video subscriber counts are not collected; you deferred them until about 100 subscribers), and the topic-label check behind the ranking idea (now 5 of 10 agree, up from 2 of 6; its read is already scheduled at 20 uploads, about 7 October). None was new and above the bar, so nothing was added.
- **New request for you (process-file-landing-path):** this is the second shift running that could not apply a process change. Last shift could not propose the wording, and this one could not carry out your approval. I recommend letting approved changes to the process files apply automatically, under the same checks that workflow changes already pass. The request explains it.
- **Friction:** this shift again wrote its plan after starting.

### Research
- The three questions above, plus whether lost search keywords matter (no: search brings about 1% of views, already known). None was new and above the bar. The shift ended about ten minutes early because the remaining work is time-locked: the new-subreddit sample opens tomorrow afternoon, and today's one sample is used.

### Feature work
- Both queued changes now include today's fix, and all their tests pass. **The title change's sample video passed** (playable, sound, no gaps) on its current version, so it can merge on 6 October as planned. It used today's one sample but leaves tomorrow afternoon's free for the new subreddit.

### Blocked
- The process wording for sample timing is waiting on your edit (issue #44), or on the request above.

### Next
- **3 October, after 12:00 UTC only:** request the new-subreddit sample. Before noon it draws AskReddit and proves nothing. If anything lands on the main code first, bring the branch up to date before requesting.
- **5 October:** read the new data. **6 October:** merge the title change, then the new subreddit once its sample passes. **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment.

### Better?
- **Than last shift:** yes. A fault that cost a real upload its title is fixed, where last shift only made such faults visible. It was the first fault that visibility caught.
- **Than ~10 shifts ago:** unclear. The channel is still flat, and the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-10-01 (16:30) — the log now records why the content check falls back; a timing rule that delayed the new-subreddit sample is raised with you

    Allocation (planned→actual %): rounds 10→15 · maintenance 25→30 · security 5→5 · pm 30→20 · research 20→10 · feature 0→5 · close 10→15

**Summary:** A short evening shift. It shipped the record the morning shift asked for: each upload now notes why the content check fell back to keywords, so the next fallback explains itself. The new-subreddit sample video could not be requested today, and the rule that prevented it no longer protects anything, so I have asked you to retire it.

### Maintenance
- **Shipped:** every upload's record now says *why* the content check fell back to its keyword-only version: the daily limit, a timeout, a garbled reply, and so on. This morning's fallback left no reason anywhere we can read. It was built now rather than after a second fallback, because waiting would have lost that one's reason too. It changes no video. All tests pass, and the change was checked against a copy of the real upload record.
- **Closed a quieter gap in the same check.** If the content service replied with something unreadable, the post was treated as checked and approved, skipping even the keyword fallback, and the record said the full check had run. It has not happened in 22 uploads. It now goes to the keyword fallback and the reason is recorded. Tests pass; the video is unchanged.
- This morning's upload landed and the saved last-post record is intact. Tonight's upload was not due yet when this shift ran.

### Security
- Standing check clean: no credentials in the project, and the secret files are still excluded.

### Project management
- **New request for you (dry-run-timing-rule):** the sample video for the new-subreddit build was due this afternoon, but no shift ran in the window the rules allow. Today's shift started with the evening upload already due, so it held back. That rule dates from when sample videos used the same daily allowance as real uploads. Since 25 September they use a separate one, and the only thing a real upload uses from it is a piece of tracking data. I recommend letting shifts request a sample at any time; the request has the exact wording. Until you decide, the 09:17 shift tomorrow can request it, and the 6 October plan still holds.
- The channel is still flat on watch time (11→12 seconds over six weeks, within its normal swing). The two changes aimed at views are already queued for 6 October, so nothing new was added.
- Ready work is still one item, the new subreddit, and today's rule kept even that from moving. Besides the two research questions below, I considered making the release check test the content check on a question worded differently from its built-in examples. A miss would block releases before 6 October, so it waits until after.
- **Friction:** the rules say to propose process changes on a branch, but this shift could not edit the process file even there, so the wording went into the request. This shift also wrote its plan after starting.

### Research
- **Do videos titled with the raw Reddit question do worse?** Only 2 such uploads are recorded, against a minimum of 8; months away, so not queued.
- **Do shorter videos get more views?** About 28% more, but each view is ~3 seconds shorter, so total watch time is the same. Already known since 25 September; discarded.

### Feature work
- The sample video was held back by the timing rule above. Instead, both queued changes (the new subreddit and the title weighting) now include today's code. Together they combine cleanly and every test passes, so tomorrow's sample tests what will actually ship. A sample taken tomorrow morning was confirmed to draw the new subreddit.

### Blocked
- The new-subreddit sample is waiting on tomorrow morning's shift, or on your decision on the timing rule.

### Next
- **Tomorrow before 12:00 UTC only:** request the new-subreddit sample. On 2 October a sample taken after noon draws AskReddit and proves nothing, and shifts have been starting hours late, so check which subreddit it would draw first. This is the second missed sample window (30 September was the first). Both queued changes include everything up to tonight's handover; if anything else lands first, bring them up to date before requesting, or the sample tests the wrong code. Check that tonight's upload carries the new "why it fell back" field, blank if the check worked. **5 October:** read the new data. **6 October:** merge the title change; the new subreddit follows once its sample passes. **12 October:** read the current experiment.

### Better?
- **Than last shift:** slightly. A fallback that left no trace will now explain itself, but nothing aimed at the channel's numbers moved.
- **Than ~10 shifts ago:** unclear. The channel is still flat, and the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.
