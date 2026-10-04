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

## 2026-10-04 (07:37) — this morning's upload lost its title to a second outage; the retry now waits it out

    Allocation (planned→actual %): rounds 10→10 · maintenance 25→20 · security 5→10 · pm 30→20 · research 20→30 · feature 0→0 · close 10→10

**Summary:** This morning's upload went out with the raw Reddit question as its title: the title service was briefly overloaded, and the retry added on 2 October waited only 4 seconds. The retry now waits 30 seconds and still makes no extra requests. Research found that uploads narrated by Danielle more often reach almost nobody; it is probably a one-off mid-September cluster, and tomorrow's data will tell.

### Maintenance
- Both uploads since the last shift landed and the saved last-post record is intact. This morning's lost its title, keywords and closing line to a "service overloaded" reply, the second time a 4-second wait was too short. The daily allowance did not run out.
- **Shipped:** before retrying an overloaded reply, the title and content check now wait 30 seconds instead of 4. The video is unchanged and all tests pass. A lost title costs no watch time, but the 6 October title-style test needs generated titles to measure. If 30 seconds is not enough either, retry on another model next.

### Security
- Standing check clean: no credentials in the project, the secret files are still excluded, and every automated job still has limited permissions. The library-advisory scan ran for the first time in three shifts and found only the two advisories already on file.

### Project management
- The plan document's header still said the previous format was live. It now points to the status section instead of repeating it.
- No decisions came due and nothing new is approved. The channel is still flat; both changes aimed at views are queued for 6 October.
- **The automatic process check raised a request for you:** recent shifts used about half their time, because the remaining work waited on a date. My recommendation, in the request: no rule change yet.
- The document checker no longer flags a true past note as out of date. It now reads only the newest shift report as current, which ends the false alarm last shift recorded as friction.
- **Friction:** this shift wrote its plan at the end, not the start, again. With 24 minutes, a written plan first costs a tenth of the shift.

### Research
- **A lead, probably weaker than it looks:** uploads narrated by Danielle reach 5 views or fewer far more often than Stephen's (11 of 67 against 2 of 65), and morning uploads more than evening ones, the same shape. How long viewers watch is equal. But 9 of those uploads are Danielle in the morning, and 7 of them fell in one fortnight in mid-September, 5 on the background clip already retired for this problem. That looks like a one-off cluster rather than the voice. Tomorrow's data covers the newer formats, after that fortnight: if the gap is still there, I will propose a one-voice experiment; if not, it was the cluster.
- The reporting tool now runs this test whenever it splits uploads into two groups, pooled across formats so tomorrow's few new uploads count. Of seven splits tried, only voice and time of day showed a gap. The burial clusters in the two mid-September weeks (7 of 28, against 6 of 115 in all other weeks). Those were the weeks the content service kept timing out, but neither of its effects explains the burial: uploads that lost their title, or skipped the content check, were buried no more often. The cause is still unknown.
- **New question, ready for the next shift:** does a background clip get buried once it has been reused? The clip retired on 28 September was fine for its first 4 uses, then buried 7 of its next 10 times, starting in late August, before that cluster. If burial rises with reuse, capping each clip's uses is a change to what we ship.

### Feature work
- Nothing this shift: both queued changes wait for 6 October, and their samples already passed.

### Blocked
- Automatic landing for approved process changes still awaits your decision (#45).

### Next
- **5 October:** read the new data: the voice and time-of-day gap above in the newest formats, the voice watch-time read, and the engaged-view column. **6 October:** merge the title change, then the new subreddit. **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment, then plan the Python upgrade.
- Any day: the clip-reuse question above (ready now, needs only a small addition to the reporting tool).
- Watch the next uploads for another overloaded-service failure.

### Better?
- **Than last shift:** yes: a live fault fixed the same morning it recurred, and a lead from our own data checked down to its likely cause before it could mislead.
- **Than ~10 shifts ago:** unclear. The channel is still flat; the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-10-03 (14:21) — the new-subreddit sample video passed, so both 6 October changes are ready

    Allocation (planned→actual %): rounds 10→15 · maintenance 10→5 · security 5→5 · pm 30→25 · research 20→20 · feature 15→20 · close 10→10

**Summary:** A short shift that did the one thing due today: the new-subreddit sample video, which only proves anything after noon on 3 October. It passed, so both changes aimed at views can merge on 6 October.

### Maintenance
- Both uploads since the last shift landed, the saved last-post record is intact, and today's release check passed.
- The ageing Python version reaches end of life tomorrow. Nothing breaks then; its upgrade is already scheduled after 12 October.

### Security
- No credentials in the project and the secret files are still excluded. The library-advisory scan was not rerun (its tool is not installed here); yesterday's stands.

### Project management
- **Requested the new-subreddit sample video.** The branch needed no update first: the main code has not changed since. Verdict under Feature work.
- No decisions came due and nothing new is approved. The channel is still flat on watch time; both changes aimed at views are queued for 6 October.
- **Ready work is now none against a floor of three:** the new subreddit, the last ready item, waits only for 6 October. Besides the Research questions, I set aside avoiding life-advice posts (too few uploads to read) and weekday timing (would not change what we post).
- **Friction:** the doc check flags yesterday's still-true entry about #44 as stale: it reads past log entries as current claims.

### Research
- Three new questions, tested on our own data, all came back as noise: no background clip holds viewers measurably longer; one title style looked 18% worse, but the gap reverses between periods; and questions that say "you" hold viewers no longer. Recorded so they are not re-asked.

### Feature work
- **The new-subreddit sample video passed** (playable, sound, no gaps). It drew the day's top post from the new subreddit, so it tests the real path. It can merge on 6 October after the title change.
- **The two 6 October changes combine cleanly:** merged together they touch separate parts of the code, and every test passes.

### Blocked
- Automatic landing for approved process changes is waiting on your decision (#45).

### Next
- **4 October:** check the morning upload kept its title; today's sample used shared allowance. **5 October:** read the new data (voices within the newest format, the engaged-view column). **6 October:** merge the title change (its sample passed), then the new subreddit (its sample passed today). **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment, then plan the Python upgrade as its own release.

### Better?
- **Than last shift:** about the same: today's one job is done; last shift fixed a live fault.
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
