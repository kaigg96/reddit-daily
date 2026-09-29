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

## 2026-09-29 (17:52) — the "You…" title lead is not clickbait, the topic labels the next build depends on disagree, and the check for neglected work can fire again

    Allocation (planned→actual %): rounds 10→10 · maintenance 5→10 · security 5→5 · pm 20→30 · research 50→35 · feature 0→0 · close 10→10

**Summary:** The title style we plan to test next keeps viewers as well as the others, so its extra views are not bought with early swipe-aways, and a measure we thought lost may be recoverable back to July. Two problems surfaced before they could mislead: the topic labels behind the next build disagree, and the check for neglected work could never fire (fixed).

### Maintenance
- This morning's upload landed and the saved last-post record is intact; today's release check passed. Tonight's upload had not landed at 17:52 UTC, within its usual window.
- **Subtitle uploads have stopped failing.** They used to fail about one time in four; the 14 uploads since 22 September all succeeded, and nothing we changed explains it. If another week stays clean, the item closes.

### Security
- Standing check clean: no credentials in the project; secret files still excluded.

### Project management
- Ready work rose from one item to two (floor three): the minutes question below is ready to build. Nothing else clears the bar; the rest waits on the 5 October data or the rotation sample.
- Kept the tracker within its size limit after adding today's findings, dropping the oldest shift report to make room for this one.
- **The neglected-work check could never fire.** It needs five shifts of history, but the work log only keeps three or four, and it misread the template at the top of the log as the newest shift. It now reads older shifts from the project's history and skips the template. It shows feature work at zero for three shifts running, not yet neglected. Security is now counted too.
- The process check flags the last three shifts as ending with too much time unused (about 59%). This shift runs its full time, which should clear it.
- **Friction:** the work log's size limit and a rule needing five shifts of it conflicted, invisibly, because the check stayed silent.

### Research
- **"You…" titles are not clickbait.** Within one era, the share of each video watched is the same as for the other styles (59% vs 58%); the earlier gap was era mix. Viewers who click these titles stay as long as anyone else.
- **The two topic labellers disagree on 4 of 6 posts.** The newer one (titles only) is usually more specific: it says "nostalgia" where the older one says "other". This matters because the topic ranking queued behind the current experiment would pick posts using one labeller's buckets while its evidence came mostly from the other's. The reporting tool now counts this, and the ranking's first reading will check it first. Six posts is too few to act on.
- **The rotation's first new subreddit rests on old evidence only.** It was chosen because nostalgia topics did well historically; the current format has only four such videos a week old, too few to confirm it.
- **The measure the API refused may already be in our data.** A column long written off as broken (minutes watched) turns out to be a steady fraction of what it "should" be. The likeliest reason is that it counts only the plays that get past the opening, which is the measure the current experiment most needs. Next week's data can test this directly. If it holds, we get that measure for every video back to July. A rough first look fits: the share more than doubled on the day July's format overhaul shipped, which our main measure had called flat. Unconfirmed.

### Feature work
- Nothing built. The only ready item needs a sample video, and tonight's upload shares today's AI allowance. Brought the rotation branch up to date with the live code again, so tomorrow's sample shows what would ship.

### Blocked
- Nothing is waiting on you.

### Next
- **Tomorrow morning, before 12:00 UTC: the rotation sample** (the branch is up to date). Build the minutes-based engaged share into the reporting tool, age-matched; on 5 October test it against the real count. At about 20 uploads with topic labels (~6 October), read the labeller agreement before anything else on the topic ranking. At the 12 October data, read the current experiment.

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

## 2026-09-28 (17:42) — retired a background video that appeared to bury half the uploads it was used on; one title style gets about 40% more views

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→10 · security 5→5 · pm 30→25 · research 35→40 · feature 0→0 · close 10→10

**Summary:** One of the seven background videos left half its uploads with almost no views, and it is now retired. Titles that speak to the viewer ("You…") get about 40% more views, the first measured difference that could lift a flat channel, and are now the proposed next test.

### Maintenance
- Last night's and this morning's uploads landed, the saved last-post record is intact, and today's release check passed. Tonight's had not landed by 17:48 UTC, which is within its usual window.
- **The reporting tool now warns when a comparison mixes periods unevenly.** That is the mistake that briefly made the voice lead look real (below). It also flags that all nine dark-topic videos come from one period, which the next reading of that question has to allow for.
- **One background video looks like it gets uploads buried.** At a week old, 8 of the 16 uploads that used it had 5 views or fewer. Across the other six videos it was 3 of 62. People who do see those uploads watch them normally, so YouTube is not showing them. The cause is unknown; one guess is that it's a stock clip used by many other channels. Retired it: tests passed and a sample video played correctly without it. The other six stay in rotation.

### Security
- Standing check clean: no credentials in the project, and secret files are still excluded.

### Project management
- **The channel still reads flat**, so this slice had to propose a change to what we ship. Proposed: use the "You…" title style on two videos in three, keeping the other two styles on the rest so the comparison continues. Once the current experiment is read (~4 October), I recommend it takes the next slot, ahead of the subreddit rotation, which has no measured evidence yet.
- Ready work is one item (the subreddit rotation) against a floor of three, now that the background-video fix has shipped.
- **Friction:** earlier tests of voice, title style and background videos judged only seconds watched per view. Your rule that views never trigger a revert is right for before-and-after comparisons, but it had also stopped anyone looking at views for these side-by-side ones. Both of today's findings were hiding there.

### Research
- **A failed title costs no watching time** (11 vs 10 seconds per view, 11 videos). The title step stays: failed-title videos drew about half the views, and dropping the title would not save any AI allowance. The dark-topics question still has only 9 videos and needs 12, so it waits.
- **Title style:** the "You…" style leads on views by 47% at one week and 41% at two, across 129 videos, and in both older periods. Viewers don't watch longer; more of them are shown the video. It is weaker on Danielle's videos, so it is not settled.
- **Voice:** Stephen first appeared to lead by 50%, and I briefly proposed him as the next test. Most of that came from him reading more videos in an older period when every video got more views; within that period he leads by only 6%.

### Feature work
- Nothing this shift; the background-video fix is under maintenance. I did not request a sample of the rotation branch: tonight's upload was still due, and today's sample would draw AskReddit rather than the new subreddit.

### Blocked
- Nothing is waiting on you.

### Next
- Confirm tonight's upload landed and no later upload uses the retired background video. Request the rotation branch's sample in the afternoon (UTC), when it draws from the new subreddit. From ~4 October, read the current experiment, then build the title weighting (a one-line change to how the style is picked) if the result allows. Before that, re-check both the title and voice leads on recent videos in the next weekly data (5 October).

### Better?
- **Than last shift:** yes. A background video that was burying uploads is gone, and there's a measured lead on views. Last shift shipped fixes but found no new lever.
- **Than ~10 shifts ago:** unclear. The first candidates with evidence behind them, but untested live.
- **Than ~100 shifts ago:** too early to say.
