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

## 2026-09-30 (12:44) — the rotation sample window was missed and tomorrow's is the other half of the day; upload time and question length are not levers

    Allocation (planned→actual %): rounds 10→10 · maintenance 5→5 · security 5→25 · pm 20→20 · research 40→30 · feature 10→0 · close 10→10

**Summary:** A security update that had waited three days for a sample video is now live, clearing four published weaknesses in the library the pipeline uses to reach Reddit and Google. Upload time and question length turn out to make no consistent difference to watch time, and tomorrow's window for the new-subreddit sample is the afternoon, not the morning.

### Maintenance
- Last night's and this morning's uploads landed and the saved last-post record is intact. Tonight's is not due yet.

### Security
- **Shipped the web-library update** that clears its four published weaknesses. It had waited since 27 September for a sample video. Today's sample slot was free because the rotation's window had closed. The sample passed, every test passed, and the video itself is unchanged. The image library and the Python version still carry older weaknesses (low exposure; logged).
- **The image library cannot be updated on its own.** The video-making library only accepts older versions of it, so fixing it means upgrading the video library first. That changes how videos are made, so it waits until after the current experiment is read on 12 October.
- Standing check clean: no credentials in the project; secret files still excluded; every automated job declares narrow permissions.

### Project management
- Nothing you approved is waiting. Kept the documents within their size limits, dropping the oldest shift report.
- Ready work is still one item against a floor of three. I considered five questions: two are answered below, and three were already settled or have nothing to compare (AI titles vs raw questions was answered on 28 September; voice shows no consistent difference across eras; there is only one music track). Nothing new cleared the bar to add.
- **The process check raised an issue with you automatically:** the last three shifts used about 59% of their time while ready work sat below the floor. My read: the floor stays low because nearly every open question waits on 5 or 12 October data, and each shift answers the cheap questions the same day, which removes them from the count.
- **Friction:** the shift is scheduled for 09:17 UTC but started at 12:44, so the plan to sample the rotation "before noon" could not happen. Plans tied to a clock window need to allow for starts running hours late.

### Research
- **Upload time does not matter.** Read at the same age, morning uploads led evening ones by 17% in one format era and trailed by 12% in the next. The overall 10% gap is noise. The rotation and any extra daily uploads can go at any hour.
- **Longer questions only look better.** They earn about 20% more watch time, in both eras, but only because they make longer videos. Among videos of the same length the gap disappears, and viewers watch a smaller share. This matches the earlier finding that length is not a lever.
- The two topic labellers now agree on 3 of 8 posts (2 of 6 yesterday), still too few to act on.

### Feature work
- No rotation sample. A sample taken after noon today draws AskReddit, not the new subreddit, so it would have proved nothing. The day's sample went to the security update instead.

### Blocked
- Nothing is waiting on you except the automatic issue above.

### Next
- **The rotation sample: on 1 October the new subreddit is drawn after 12:00 UTC**, which is when shifts have actually been starting. On 2 October it is before noon. Check which one a sample would draw before requesting it. On 5 October, test the engaged-share estimate against the real count. Around 6 October, read the topic labellers' agreement. At the 12 October data, read the current experiment.

### Better?
- **Than last shift:** yes, modestly. Something shipped: a security fix that had sat unmerged for three days. Two standing doubts were retired with evidence; upload time had been called an uncontrolled variable for two months.
- **Than ~10 shifts ago:** unclear. The channel is still flat, and the current experiment is not read until 12 October.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-29 (17:52) — the "You…" title lead is not clickbait, the topic labels the next build depends on disagree, and the check for neglected work can fire again

    Allocation (planned→actual %): rounds 10→10 · maintenance 5→10 · security 5→5 · pm 20→30 · research 50→35 · feature 0→0 · close 10→10

**Summary:** The title style we plan to test next keeps viewers as well as the others, so its extra views are not bought with early swipe-aways, and a measure we thought lost may be recoverable back to July. Two problems surfaced before they could mislead: the topic labels behind the next build disagree, and the check for neglected work could never fire (fixed).

### Maintenance
- This morning's upload landed and the saved last-post record is intact; today's release check passed. Tonight's upload had not landed at 17:52 UTC, within its usual window.
- **Subtitle uploads have stopped failing.** They used to fail about one time in four; the 14 uploads since 22 September all succeeded, and nothing we changed explains it. If another week stays clean, the item closes.

### Security
- Standing check clean: no credentials in the project; secret files still excluded.

### Project management
- Ready work is one item (floor three). The minutes question below became ready and was built the same shift; its test waits on 5 October, like everything else but the rotation.
- Kept the tracker within its size limit after adding today's findings, dropping the oldest shift report to make room for this one.
- **The neglected-work check could never fire.** It needs five shifts of history, but the work log only keeps three or four, and it misread the template at the top of the log as the newest shift. It now reads older shifts from the project's history and skips the template. It shows feature work at zero for three shifts running, not yet neglected. Security is now counted too.
- The process check flags the last three shifts as ending with too much time unused (about 59%). This shift runs its full time, which should clear it.
- **Friction:** the work log's size limit and a rule needing five shifts of it conflicted, invisibly, because the check stayed silent.

### Research
- **"You…" titles are not clickbait.** Within one era, the share of each video watched is the same as for the other styles (59% vs 58%); the earlier gap was era mix. Viewers who click these titles stay as long as anyone else.
- **The two topic labellers disagree on 4 of 6 posts.** The newer one (titles only) is usually more specific: it says "nostalgia" where the older one says "other". This matters because the topic ranking queued behind the current experiment would pick posts using one labeller's buckets while its evidence came mostly from the other's. The reporting tool now counts this, and the ranking's first reading will check it first. Six posts is too few to act on.
- **The rotation's first new subreddit rests on old evidence only.** It was chosen because nostalgia topics did well historically; the current format has only four such videos a week old, too few to confirm it.
- **The measure the API refused may already be in our data.** A column long written off as broken (minutes watched) turns out to be a steady fraction of what it "should" be. The likeliest reason is that it counts only the plays that get past the opening, which is the measure the current experiment most needs. Next week's data can test this directly. If it holds, we get that measure for every video back to July. A rough first look fits: the share more than doubled on the day July's format overhaul shipped, which our main measure had called flat. The reporting tool now reads it, marked unconfirmed.

### Feature work
- Nothing built. The only ready item needs a sample video, and tonight's upload shares today's AI allowance. Brought the rotation branch up to date with the live code again, so tomorrow's sample shows what would ship.

### Blocked
- Nothing is waiting on you.

### Next
- **Tomorrow morning, before 12:00 UTC: the rotation sample** (the branch is up to date). On 5 October, test the reporting tool's new engaged-share estimate against the real count. At about 20 uploads with topic labels (~6 October), read the labeller agreement before anything else on the topic ranking. At the 12 October data, read the current experiment.

### Better?
- **Than last shift:** yes, slightly. The next planned test cleared its obvious risk, a flaw in the topic ranking's evidence surfaced before anything was built on it, and a safeguard that had been silently dead works again.
- **Than ~10 shifts ago:** unclear. More checked leads, none tested live yet.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-29 (16:10) — a measure we thought we had was never collected, and the current experiment's verdict moves to 12 October

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→15 · security 5→5 · pm 30→30 · research 35→30 · feature 0→0 · close 10→10

**Summary:** A measure gathered for the current experiment was never actually collected, and its verdict was scheduled a week too early; the date is corrected and next week's data will show why the measure failed. The check that caught yesterday's burying background video is built into the reporting tool, and the "You…" title lead survived a confound check.

### Maintenance
- Last night's and this morning's uploads landed without the retired background video, and the saved last-post record is intact. Today's release check passed. Tonight's is not due yet.
- **A measure we thought we were collecting never was.** The share of plays that get past the opening, gathered for the current experiment since last week, came back empty, and the only warning went to a log no shift reads. The next weekly data will now say why.

### Security
- Standing check clean: no credentials in the project; secret files still excluded.

### Project management
- Nothing you approved is waiting; the process check is healthy.
- Kept every document within its size limit (dropping the oldest shift report), and closed a code-health item already fixed.
- Ready work is still one item (the rotation) against a floor of three; fixing the measure waits on next week's data. Three new questions I considered were answered today (below); nothing else would change a decision.
- **Corrected a date:** the current experiment is read at the 12 October data, not 5 October. By the 5th only about 8 of its videos are a week old, against the 20 it committed to, and the tool would have answered anyway; it now refuses below an experiment's committed size. The two items queued behind it move a week.
- **Friction:** yesterday's key finding needed a hand count the tool could not do, which the project rules forbid. Now fixed, as is a document check that flagged a correct reference.

### Research
- **The reporting tool now counts buried uploads** (5 views or fewer) for any grouping. It reproduces yesterday's hand count exactly.
- **The "You…" title lead is not caused by the retired video.** That video carried the style more often than the others, so it held the lead down. The lead is in the typical video, not in fewer buried ones. The other two styles perform alike.
- **No second cause of burying** by voice, title style or version, once the retired video is set aside.

### Feature work
- Nothing this shift. No rotation sample: tonight's upload is still due and shares today's AI allowance.

### Blocked
- Nothing is waiting on you.

### Next
- **Tomorrow's morning shift is the window for the rotation sample:** before 12:00 UTC on 30 September the sample draws the new subreddit and no upload is near. The branch is now up to date with the live code. On 5 October, read why the measure was refused and fix it. At the 12 October data, read the current experiment, then build the title weighting if the result allows.

### Better?
- **Than last shift:** yes, modestly. Yesterday's key check now runs from the tool, the proposed next test survived its obvious confound, and an early read can no longer pass for the real one.
- **Than ~10 shifts ago:** unclear. More measured leads, none tested live yet.
- **Than ~100 shifts ago:** too early to say.

