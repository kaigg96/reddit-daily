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

## 2026-10-04 (14:49) — today's release check failed on a tracker slip, now fixed; title length ruled out

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→25 · security 5→15 · pm 30→15 · research 30→25 · feature 0→0 · close 10→10

**Summary:** Today's automatic release check failed. The cause was a bookkeeping slip in the tracker, not the video code, and it is fixed. Research ruled out title length as the reason raw-question titles get fewer views, and tomorrow's statistics run makes a second try at a figure we have never collected. Ready work is still none: the rest waits on 5 and 6 October.

### Maintenance
- No upload has run since this morning's shift checked them. Today's release check failed: a research question answered this morning was left in the tracker, which a test forbids, so the check stopped before testing the live code. The answer now sits with the findings, and every test passes. Uploads were never affected.
- **Shipped:** the weekly statistics job has never collected the figure for plays that get past the opening, because the service refused that request. When refused, it now also asks for the figure in a smaller request, so tomorrow's run either collects it or shows whether request size was the cause. The snapshot is never at risk, and the video is unchanged.

### Security
- Standing check clean: no credentials in the project, the secret files are still excluded, and no automated job's permissions changed.
- **Now due:** a known gap lets the two jobs that test unmerged code hold a key that can change the live branch. Its fix was held until your return today, as it reworks the path every sample video uses. I drafted the fix for the sample-video job and saved it untested for the next shift. Nothing live changed.

### Project management
- No decisions came due and nothing new is approved. The channel is still flat; both changes aimed at views are queued for 6 October. **They still combine cleanly with today's code, and every test passes with both merged,** so 6 October needs only the merges. Removed one finished branch.
- **Ready work is still none against a floor of three.** Considered and dropped: whether runner-up posts do worse (4 uploads), whether a missing closing question costs comments (4 uploads, and tangled with lost titles), and music (one track). An early-read question I added turned out to be answered on 25 September, so I removed it.
- **Friction:** the change that broke the test went live because its shift did not rerun the tests after its last edit, and the follow-up check failed after that shift had ended. It has happened once, so I recorded it rather than proposing a rule. **Also:** I re-asked an answered question because its answer sits mid-paragraph in a long findings section. Checking the history first would have caught it.

### Research
- **Asked and answered: is title length why raw titles get fewer views? No.** Raw-question titles are about 64 characters, generated ones about 41. Among generated titles, shorter ones got 16% more views, within normal noise, and 9% less watch time. Raw titles get 49% fewer views, far more than length explains. No length cap is needed, and the 6 October title-style test goes ahead unchanged.

### Feature work
- Nothing this shift: both queued changes wait for 6 October, and their sample videos passed.

### Blocked
- Automatic landing for approved process changes still awaits your decision (#45).

### Next
- **5 October:** read the new data: the voice and time-of-day gap in the newest formats, and the engaged-view column. **6 October:** merge the title change, then the new subreddit. **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment, then plan the Python upgrade.
- Confirm the next release check passes.
- Finish the security fix above: review the draft, apply the same split to the daily release check, then send both to you for approval.

### Better?
- **Than last shift:** about the same. A broken check was fixed within hours and one more lead was closed, but nothing moved the channel.
- **Than ~10 shifts ago:** unclear. The channel is still flat; the first change aimed at views ships on 6 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-10-04 (07:37) — this morning's upload lost its title to a second outage; the retry now waits it out

    Allocation (planned→actual %): rounds 10→10 · maintenance 25→15 · security 5→10 · pm 30→20 · research 20→35 · feature 0→0 · close 10→10

**Summary:** This morning's upload went out with the raw Reddit question as its title: the title service was briefly overloaded, and the retry added on 2 October waited only 4 seconds. The retry now waits 30 seconds and still makes no extra requests. Research found that uploads narrated by Danielle more often reach almost nobody, probably a one-off mid-September cluster; tomorrow's data will tell. Ready work is back to none: everything left waits on 5 or 6 October.

### Maintenance
- Both uploads since the last shift landed and the saved last-post record is intact. This morning's lost its title, keywords and closing line to a "service overloaded" reply, the second time a 4-second wait was too short. The daily allowance did not run out.
- **Shipped:** before retrying an overloaded reply, the title and content check now wait 30 seconds instead of 4. The video is unchanged and all tests pass. A lost title costs no watch time, but the 6 October title-style test needs generated titles to measure. If 30 seconds is not enough either, retry on another model next.

### Security
- Standing check clean: no credentials in the project, the secret files are still excluded, and every automated job still has limited permissions. The library-advisory scan found only the two advisories already on file.

### Project management
- The plan document's header still said the previous format was live. It now points to the status section instead of repeating it.
- No decisions came due and nothing new is approved. The channel is still flat; both changes aimed at views are queued for 6 October.
- **The automatic process check raised a request for you:** recent shifts used about half their time, because the remaining work waited on a date. My recommendation, in the request: no rule change yet.
- The document checker no longer flags a true past note as out of date. It now reads only the newest shift report as current, which ends the false alarm last shift recorded as friction.
- **Friction:** this shift wrote its plan at the end, not the start, again.

### Research
- **A lead, probably weaker than it looks:** uploads narrated by Danielle reach 5 views or fewer far more often than Stephen's (11 of 67 against 2 of 65), and morning uploads more than evening ones, the same shape. How long viewers watch is equal. But 9 of those uploads are Danielle in the morning, and 7 of them fell in one fortnight in mid-September, 5 on the background clip already retired for this problem. That looks like a one-off cluster rather than the voice. Tomorrow's data covers the newer formats, after that fortnight: if the gap is still there, the next shift proposes a one-voice experiment; if not, it was the cluster.
- The reporting tool now runs this test whenever it splits uploads into two groups, pooled across formats so tomorrow's few new uploads count. Of seven splits tried, only voice and time of day showed a gap; topic is too thin to read (10 uploads or fewer each). The burial clusters in the two mid-September weeks (7 of 28, against 6 of 115 in all other weeks). Those were the weeks the content service kept timing out, but neither of its effects explains the burial: uploads that lost their title, or skipped the content check, were buried no more often. The cause is still unknown.
- **Asked and answered: does a background clip get buried once it has been reused? No.** The clip retired on 28 September went bad after its fourth use, but across all the other clips, later uses were buried no more often than early ones. That clip was a one-off, so no cap on reuse is needed.

### Feature work
- Nothing this shift: both queued changes wait for 6 October; their samples passed.

### Blocked
- Automatic landing for approved process changes still awaits your decision (#45).

### Next
- **5 October:** read the new data: the voice and time-of-day gap above in the newest formats, the voice watch-time read, and the engaged-view column. **6 October:** merge the title change, then the new subreddit. **About 7 October:** the topic-ranking idea's 20-upload read. **12 October:** read the current experiment, then plan the Python upgrade.
- Watch the next uploads for another overloaded-service failure.

### Better?
- **Than last shift:** yes: a live fault fixed the same morning it recurred, and a lead checked down to its likely cause before it could mislead.
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
