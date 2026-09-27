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
- **Friction:** only one real sample video is allowed per shift, and two finished pieces now queue for it (the rotation and the library update). If the queue grows, that limit is the thing to question.
- Ready work is still one item against a floor of three. I considered four questions: whether failed captions cost viewing (7 cases), day of week, videos picked below Reddit's top post (3 cases), and a nostalgia-heavy subreddit for the rotation. The first three change no decision or can't get enough data; the last is a detail of the rotation build, not a separate item. Two questions become answerable with tomorrow's weekly data.

### Research
- Tried to answer early whether a failed title costs viewing. It read slightly better, but the early reading was the flawed kind above, so it is not evidence, and I removed it from the tracker. Tomorrow's seven-day reading decides.

### Feature work
- **Subreddit rotation:** each video's description and tags now name its own subreddit instead of always saying AskReddit, with AskReddit's left exactly as before. Added r/NoStupidQuestions on the branch; its sample video passed. But which posts the safety screen turned down showed only in a log shifts cannot open, so the sample reports now include them. The next sample will show the screen's verdict on the new subreddit. Rotation still cannot go live before the current experiment is read (~4 October).

### Blocked
- Nothing is waiting on you.

### Next
- Confirm tonight's upload got its AI-written title: it is the first to send the AI key the new way. Request another sample of the rotation branch (it draws from the new subreddit on alternate days) and read what the screen skipped. After tomorrow's weekly data, answer the two waiting questions (dark topics, failed titles) at seven days. Five unmerged branches from 22–24 September may be superseded or awaiting your approval; check each. The library update also needs a sample; rotation has priority for the one sample per shift. Keep building the rotation: screen more candidate subreddits, and decide whether the on-video channel name still fits non-AskReddit posts.

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

## 2026-09-25 (14:40) — sample videos are now free, your length decision is live, and the title-failure fix shipped

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→15 · security 5→5 · pm 35→25 · research 20→10 · feature 10→25 · close 10→10

**Summary:** Sample videos now cost nothing, and a shift can make one itself in two minutes. That removes the limit that held finished work for days. Your length decision is built into the check that judges each change, and the fix that records why titles fail is live.

### Feature work
- **Sample videos are now free.** A sample mode renders a fixed question over silent audio, with no voice or AI calls, and passed the same playability check as a real sample. It covers changes to the video. Changes to how questions, titles or voices are fetched still need a real one.

### Maintenance
- Every scheduled upload landed, including this morning's first upload with the new opening, and the saved record of the last post is intact.
- **Shipped the fix that records why a title failed.** It had waited two days for a sample video, but it changes nothing in the video itself. The step it changes only runs after a real upload, so a sample could not have tested it anyway. All tests pass, and it cannot cause a duplicate upload.
- **Chose not to request a paid sample today.** Today's AI allowance must also cover tomorrow's 05:00 upload, and this morning's check used about six of the twenty requests. That squeeze cost an upload its title yesterday.

### Security
- Standing check clean: no credentials are stored in the project, and today's changes contain none.

### Project management
- **Done and closed your decision on length (#39).** When a change alters video length by a second or more, it must now also hold total time watched, not just seconds per view. Checked on the background-video switch, which did lengthen videos: it still passes.
- **One thing only you can do:** the written rule shifts follow still says "watch-seconds only". Shifts cannot edit that file, so the one-line wording is in my closing note on #39 if you want it.
- **Real samples no longer use the uploads' AI allowance.** The allowance is counted per model, so samples now use a second one. That unblocked the question-picking tool's logging, which passed its sample and is now live. Ready work is now zero, because every ready item shipped. Refilling it is the next shift's first job.
- **Friction:** "request a sample after 07:00" was the plan handed to this shift. It ignored that the 07:00 window also has to pay for the next morning's upload. Free samples now cover most changes.

### Research
- **Title style still makes no difference:** at a week old, 11, 10 and 9 seconds across roughly 40 videos each, the same answer as on 22 September.
- **Whether a lower-ranked question does worse can't be answered yet:** the top post was used 41 times and a lower one only 4. The planned question-picking tool's own logging is the only way to get this evidence.
- **Whether a failed title hurts a video can't be answered yet:** no failed-title upload is a week old.

### Blocked
- Nothing is waiting on you except the one-line rule wording above.

### Next
- Refill ready work. Check that tonight's upload logs every candidate's topic. If a morning title fails, read its new failure reason first.

### Better?
- **Than last shift:** yes. Five finished pieces shipped, where the last two shifts shipped none, and the main limit on shipping is gone.
- **Than ~10 shifts ago:** yes, modestly. Owner decisions now turn into working checks the same day. Nothing yet has moved the channel's numbers.
- **Than ~100 shifts ago:** too early to say.
