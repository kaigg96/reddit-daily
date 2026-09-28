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
- Only the background-video retirement (above). I did not request a sample of the rotation branch: tonight's upload was still due, and today's sample would draw AskReddit rather than the new subreddit.

### Blocked
- Nothing is waiting on you.

### Next
- Confirm tonight's upload landed and no later upload uses the retired background video. Request the rotation branch's sample in the afternoon (UTC), when it draws from the new subreddit. From ~4 October, read the current experiment, then build the title weighting (a one-line change to how the style is picked) if the result allows. Before that, re-check both the title and voice leads on recent videos in the next weekly data (5 October).

### Better?
- **Than last shift:** yes. A background video that was burying uploads is gone, and there's a measured lead on views. Last shift shipped fixes but found no new lever.
- **Than ~10 shifts ago:** unclear. The first candidates with evidence behind them, but untested live.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-27 (14:44) — the AI key no longer leaks into error logs, and the performance reports stopped reading reporting delay as real results

    Allocation (planned→actual %): rounds 10→10 · maintenance 20→25 · security 5→15 · pm 20→10 · research 15→5 · feature 20→25 · close 10→10

**Summary:** The fix that keeps the AI key out of error logs is live, checked against Google first. The reports we use to judge experiments were reading videos before YouTube had counted their views; they now wait five days, and I withdrew one reading of my own that relied on it.

### Maintenance
- Both uploads since the last shift landed, the saved last-post record is intact, and today's release check passed. The new topic logging is working again: both uploads since yesterday's fix recorded their topics.
- **Found a measurement flaw.** A third of videos still show zero views at three to four days old, falling to a steady 4–6% from five days on. YouTube simply hasn't counted them yet. The reporting tool treated three days as old enough, so early readings rested on whichever videos happened to be counted first, and the check for hidden (suppressed) videos counted slow counts as suppression. It now waits five days and refuses younger readings. The seven-day readings every experiment is judged on are unaffected.

### Security
- **Shipped the fix that keeps the AI key out of error logs**, parked since 24 September. I checked Google accepts the key the new way with one call on the sample videos' own allowance, which tonight's upload doesn't use. Standing check otherwise clean: no credentials in the project, secret files still excluded. Library warnings re-checked: the same two known, low-exposure libraries. Prepared an update that clears one library's four warnings; it waits for a sample video before going live.

### Project management
- Weekly check of the safety screen: 17 uploads since its last adjustment, none skipped (the limit for concern is 15%). This morning it dropped two answers while saying they fit no risky category, which looks like a false alarm. It costs little, since other answers fill in. If it recurs, that's the case for narrowing the screen, which would come to you.
- Cleared nine finished branches whose work was already live, so the list of open branches now shows only real open work: the rotation, the library update, your pre-trip snapshot, and the branch the daily release check reads.
- **Friction:** only one real sample video is allowed per shift, and two finished pieces now queue for it (the rotation and the library update). If the queue grows, that limit is the thing to question.
- Ready work is still one item against a floor of three. I considered four questions: whether failed captions cost viewing (7 cases), day of week, videos picked below Reddit's top post (3 cases), and a nostalgia-heavy subreddit for the rotation. The first three change no decision or can't get enough data; the last is a detail of the rotation build, not a separate item. Two questions become answerable with tomorrow's weekly data.

### Research
- Tried to answer early whether a failed title costs viewing. It read slightly better, but the early reading was the flawed kind above, so it is not evidence, and I removed it from the tracker. Tomorrow's seven-day reading decides.

### Feature work
- **Subreddit rotation:** each video's description and tags now name its own subreddit instead of always saying AskReddit, with AskReddit's left exactly as before. Added r/NoStupidQuestions on the branch; its sample video passed. But which posts the safety screen turned down showed only in a log shifts cannot open, so the sample reports now include them. The next sample will show the screen's verdict on the new subreddit. Rotation still cannot go live before the current experiment is read (~4 October).

### Blocked
- Nothing is waiting on you.

### Next
- Confirm tonight's upload got its AI-written title: it is the first to send the AI key the new way. Request another sample of the rotation branch and read what the screen skipped. Timing matters: an afternoon (UTC) sample draws from the new subreddit on 29 September, not 28 September, when it would draw AskReddit. After tomorrow's weekly data, answer the two waiting questions (dark topics, failed titles) at seven days. The library update also needs a sample; rotation has priority for the one sample per shift. Keep building the rotation: screen more candidate subreddits, and decide whether the on-video channel name still fits non-AskReddit posts.

### Better?
- **Than last shift:** yes, modestly: three fixes shipped, against one, including the key fix that had waited three days.
- **Than ~10 shifts ago:** unclear. Measurement is more trustworthy than it was, but the channel's numbers are still flat.
- **Than ~100 shifts ago:** too early to say.

## 2026-09-26 (13:47) — the new topic logging and sample videos were silently failing; both fixed, and ready work is no longer zero

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→25 · security 5→10 · pm 40→30 · research 20→10 · feature 0→5 · close 10→10

**Summary:** Google retired the cheaper AI model we switched to yesterday, so the new topic logging and the AI parts of sample videos had silently failed since. Both now use its replacement, checked live. The next build, subreddit rotation, is ready to start ahead of its slot.

### Maintenance
- All uploads landed, the saved last-post record is intact, and today's release check passed.
- **Found a silent failure.** The topic logging that the question-picking tool's schedule depends on went live yesterday, but both runs since recorded nothing. The reason only reached a log shifts cannot read. The cause: Google withdrew the model it used. Moved it and sample videos to the replacement and checked it live; failures now record their reason, and sample reports list them. Uploads' own AI model is unchanged.

### Security
- No credentials are stored in the project and secret files are still excluded. Known library warnings are unchanged. A fix keeping the AI key out of error messages waits on a branch for a live check.

### Project management
- **The automatic health check flagged that recent shifts used only about half their time**, with ready work at zero. Cause: every build idea waits on the running experiment, and questions our data can answer run out between weekly data drops. I first recommended running a second test on alternating days. Two blind rankings put it last, so I withdrew it. Both ranked this near the top: **build the subreddit rotation now so it ships the day the current experiment is read.** It is now marked ready.
- Corrected the tracker: topic logging was broken, and the subreddit test still judged on views, which you ruled out.
- **Friction:** I re-tested two questions the previous shift had already answered (narrator voice, and how old a video must be before judging it). Answered questions leave the research list, and their results sit in one long, easily missed paragraph.

### Research
- **Does a failed title hurt a video?** Now answerable from older uploads too: 12 went out titled with the raw Reddit question. Today the answer is "not enough data" (7 are old enough, 8 needed). They lean worse, 8 seconds against 10. The 28 September data drop should settle it. If failed titles do no worse, the title step could be dropped to free AI allowance.
- **Background clips:** one clip leads by 18%, mostly because its videos run longer; likely luck. Not acted on.
- **Music:** all 117 measured uploads used one track, so music cannot be tested until you add more.

### Feature work
- Started the subreddit rotation on a branch; it cannot go live before the current experiment is read.

### Blocked
- The note on unused shift time is with you; nothing else is.

### Next
- Confirm tonight's upload logged topics. After 07:00, update the key-safety branch to today's change, check it live, merge. Finish the subreddit rotation: its mechanism is built on a branch; picking subreddits and screening them remain. After the 28 September data drop, answer the two waiting research questions.

### Better?
- **Than last shift:** no, smaller: one silent failure caught a day in, against five pieces shipped.
- **Than ~10 shifts ago:** unclear. Silent failures now surface in a day, not two weeks; the numbers are still flat.
- **Than ~100 shifts ago:** too early to say.
