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

## 2026-10-01 (06:46) — two queued changes can start on 6 October instead of after the 12 October read; the title change is built

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→15 · security 5→10 · pm 35→30 · research 15→10 · feature 15→15 · close 10→10

**Summary:** The next two changes no longer have to wait for the current experiment's result on 12 October. The data shows they cannot disturb it, so both can start on 6 October, six days sooner. The first, more "You…" titles in the rotation, is built and tested and can be merged that day.

### Maintenance
- Last night's and this morning's uploads landed, and the saved last-post record is intact.
- **This morning's content check ran on its keyword-only fallback**, the first time since we started recording which check ran (9 September). The question itself was harmless ("something you can't prove but believe"). The title service answered in the same run, so the daily limit had not run out. Nothing we can read records why it failed. If it happens again, the next step is to start recording the reason.
- **The keyword fallback is close to no protection.** It would have caught none of the four questions the full check has ever turned away. Because the fallback ran once in about 44 uploads, the risk is about one upload in a thousand. Worth watching, not yet worth fixing.

### Security
- Standing check clean: no credentials in the project, and the secret files are still excluded.
- **The image-library fix changes the video.** Rendered the same sample on the old and new versions: the thumbnail and sound match, but about a quarter of the video frames differ. Two renders on the same version match exactly, so the difference is real. The fix therefore ships as its own release, with a sample video, after 12 October.

### Project management
- **Your decision on shifts ending early (issue #43) is done and closed.** The three short shifts each stopped because only one piece of work was ready. There were two causes. Most queued work was dated to the 12 October read, but that read only measures uploads up to 5 October. And research questions get answered in the shift that raises them, so a supply never builds up. This shift fixed the first cause and used its full time.
- Ready work is still one item against a floor of three, but two blocked items now unblock on 6 October rather than 12.
- **Friction, fixed:** the list of your approved decisions showed only titles, so I had to open the issue itself to read what it asked for. It now shows the recommendation you approved.

### Research
- **"You…" titles do not change watch time.** It is 10 seconds either way across 129 videos: a little higher in one period, a little lower in the next. So using more of them cannot move the current experiment's measure, which is watch time.
- **The title change and the new subreddit can run side by side.** Each day's two uploads share a title style and go to different subreddits, so neither comparison skews the other. This holds for two subreddits only; a third would need the schedule changed.

### Feature work
- **Built the title-weighting change:** four "You…" days in every six, with the other two styles kept for comparison. The tests and a free sample run passed. Merge it on or after 6 October.

### Blocked
- Nothing is waiting on you.

### Next
- **Today after 12:00 UTC:** request the new-subreddit sample, but not within an hour of the evening upload. **5 October:** read the new data (engaged-share estimate, clips, voice). **6 October:** merge the title change; the new subreddit follows once its sample passes. **12 October:** read the current experiment. After that, the Python upgrade and the library fixes, one release each.

### Better?
- **Than last shift:** yes. A change is built and ready to ship, and two changes move six days earlier, based on data.
- **Than ~10 shifts ago:** unclear. The channel is still flat; the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-30 (15:58) — the new-subreddit build is ready for tomorrow afternoon's sample; background clips do not differ on watch time

    Allocation (planned→actual %): rounds 10→15 · maintenance 10→10 · security 20→25 · pm 20→10 · research 20→15 · feature 10→10 · close 10→15

**Summary:** A short shift (24 minutes) that got the subreddit-rotation build ready for tomorrow's sample video, and showed that the Python upgrade due after 12 October needs no other changes. The only new question worth testing had a clear answer: once the weak clip retired on 28 September is set aside, the background clip makes no difference to watch time.

### Maintenance
- This morning's upload landed and the saved last-post record is intact; today's release check passed. Tonight's upload is not due yet.
- Subtitle uploads: 16 in a row have now succeeded since the last failure on 22 September. The item closes if none fail by 6 October.

### Security
- **The Python upgrade looks straightforward.** The version the pipeline runs on stops getting security fixes on 4 October. On the newer version every test passes and a free test video renders correctly, with no library changes needed. The upgrade still waits until after the 12 October read and ships as its own release, because it could change how videos render.
- **Upgrading the video library would not fix the image library's weaknesses**, contrary to last shift's plan: every fix is above the version it allows. The fix is overriding that cap, which a test render already survived.
- A new published weakness in the sign-in library does not affect us: it is a server-side flaw, and we only sign in as a client, from a one-off setup script. The fixed version passes every test and joins the next dependency release.
- Standing check clean: no credentials in the project; secret files still excluded.

### Project management
- Nothing you approved is waiting. Ready work is still one item against a floor of three. The one new question considered is answered below; nothing else cleared the bar.

### Research
- **Background clips do not differ on watch time.** At 7 days the six clips still in use sit between 11 and 13 seconds, within the channel's normal swing. The clip retired on 28 September was also the lowest on watch time (10 seconds), which supports retiring it.

### Feature work
- **The rotation build is ready for its sample.** It had fallen 27 changes behind what is live; it now includes them and every test passes. Only a sample requested **after 12:00 UTC on 1 October** draws the new subreddit (checked against the code), and it must not be requested within an hour of the evening upload.

### Blocked
- Nothing is waiting on you.

### Next
- **1 October after 12:00 UTC:** request the rotation sample, which is the build's first check of the content filter on the new subreddit. On 5 October, read the new data (engaged-share estimate, clips, voice). Read the current experiment at the 12 October data. After that, two separate releases: the Python upgrade, then the image-library override bundled with the sign-in library fix. Any shift can first test for free whether that override changes a single pixel (today's attempt used two different background clips); if it doesn't, it can ship sooner.

### Better?
- **Than last shift:** marginally. Nothing shipped, but the next build is ready for its sample, and one more doubt (background clips) was settled with evidence.
- **Than ~10 shifts ago:** unclear. The channel is still flat, and the current experiment is not read until 12 October.
- **Than ~100 shifts ago:** too early to say.
