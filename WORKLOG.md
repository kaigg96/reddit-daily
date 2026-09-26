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

## 2026-09-26 (13:47) — the new topic logging was failing silently; it now records why, and ready work is no longer zero

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→25 · security 5→10 · pm 40→30 · research 20→15 · feature 0→0 · close 10→10

**Summary:** The new logging of every candidate question's topic has recorded nothing on both runs since it went live. It now writes down why it fails, so tonight's upload should show the cause. The next build, subreddit rotation, is now ready to start ahead of its slot.

### Maintenance
- Every scheduled upload landed, the saved record of the last post is intact, and today's release check passed.
- **Found a silent failure.** The topic logging that the question-picking tool's schedule depends on went live yesterday, but both runs since recorded nothing. The reason only reached a log shifts cannot read. Shipped a fix that records it with the upload. It cannot change the video or cost an upload.

### Security
- No credentials are stored in the project and secret files are still excluded. The known library warnings are unchanged and already logged. A fix that stops the AI key appearing in error messages is ready on a branch; it needs a live check first.

### Project management
- **The automatic health check flagged that recent shifts used only about half their time**, with ready work at zero. Cause: every build idea waits on the running experiment, and questions our data can answer run out between weekly data drops. I first recommended running a second test on alternating days. Two blind rankings both put it last, so I withdrew it on the issue. Both ranked this near the top instead: **build the subreddit rotation now so it ships the day the current experiment is read.** It is now marked ready.
- Corrected the tracker, which said topic logging worked.
- **Friction:** I re-tested two questions the previous shift had already answered (narrator voice, and how old a video must be before judging it). Answered questions leave the research list, and their results sit in one long paragraph that is easy to miss. It cost about ten minutes.

### Research
- **Does a failed title hurt a video?** Now answerable from older uploads too: 12 went out titled with the raw Reddit question. Today the answer is "not enough data" (7 are old enough, 8 needed). They lean worse, 8 seconds watched against 10. The 28 September data drop should settle it. If failed titles do no worse, the title step could be dropped to free AI allowance.
- **Background clips:** one clip leads by 18%, mostly because its videos run longer; likely luck. Not acted on.
- **Music:** all 117 measured uploads used the same track, so music cannot be tested until more tracks are added. That is your standing task.

### Feature work
- Nothing this shift: every build item waits on the current experiment.

### Blocked
- The note on unused shift time is with you. Nothing else waits on you.

### Next
- Read tonight's upload record; if the topic column shows a failure reason, fix it. After 07:00, check the prepared key-safety fix against the live AI service and merge it. Build the subreddit rotation. After the 28 September data drop, answer the two waiting research questions.

### Better?
- **Than last shift:** no, smaller: one silent failure caught a day in, against five pieces shipped.
- **Than ~10 shifts ago:** unclear. Silent failures are now caught in a day, not two weeks, but the channel's numbers are still flat.
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

## 2026-09-25 (03:00) — nine quick questions answered from existing data; a blind spot in how we judge changes is now flagged, with one decision for you

    Allocation (planned→actual %): rounds 10→10 · maintenance 5→5 · security 5→5 · pm 25→15 · research 45→55 · feature 0→0 · close 10→10

**Summary:** Our reporting tool can now compare kinds of video fairly at the same age, and this shift used it to answer nine questions from data we already had. The one that matters: longer videos score better on our main measure simply by being longer. The check that judges each change now warns when a change also altered video length, so the new opening cannot pass or fail on length alone.

### Feature work
- Nothing this shift. The one ready build item, making sample videos free, needs design work longer than this window. The two finished changes still wait for sample videos, which cannot be requested before the 07:00 AI-allowance reset.

### Maintenance
- Every scheduled upload landed, and the saved record of the last post is intact. The next upload (~05:00) is the first with the new opening.

### Security
- Standing check clean: no credentials committed, and the secret files are still excluded. All nine automated jobs set their own limited permissions, and none uses the risky settings that would let outside code act with the repository's rights.

### Project management
- **Your approval for shifts refilling their own work is done and closed.** It was already live, and this shift used it.
- **Ready work is at one, short of the target of three,** because this shift answered all six questions it generated. Other ideas were considered and fell below the bar. Recording more topics or answer lengths needs a sample video first. Day-of-week timing would change no decision.
- **Dropped the upload-time idea for good.** It was parked until each slot had enough videos. They now have about 60 each, and morning and evening differ by no more than normal noise.
- Trimmed settled history from the plan to keep it within its size limit.
- **Friction, noted rather than acted on:** this shift began 40 minutes after the previous one, and both ran before the 07:00 AI-allowance reset. So neither could request the sample videos that two finished changes are waiting for. If overnight shifts are routine, one of them could move to after 07:00.

### Research
- **Narrator voice makes no difference:** both voices hold viewers for 10 seconds, across about 60 videos each.
- **Topic may matter:** dark, morbid questions were watched for 14 seconds against 11 for the rest, compared at a week old. It is only 9 videos, and a reading at 3 days points the other way, so this is a lead, not a finding. If it holds after Monday's data, it becomes the first current evidence for the planned tool that picks which question to post.
- **Background clips:** no clear winner. The spread between clips is within normal noise.
- **Morning versus evening:** mornings are 5–10% ahead, which is within normal noise (see above).
- **Question length looked like a clear gap, but was only video length.** Videos with longer questions were watched for 11 seconds against 9. Comparing videos of the same length, the gap disappears.
- **What that exposed:** our main measure, seconds watched, rises with video length (11 against 9 seconds for videos over about 20 seconds). Length does not bring more views, but every change is judged on this measure. So a change that makes videos longer or shorter could be kept or undone for the wrong reason. Checked: the last two releases did not change length. The switch to background video did, so part of its measured gain was length. It stays, because nothing argues for removing it. The check that judges each change now warns when length moved. The new opening changes only what is on screen, not the timing, so it should not move length. The check will confirm that when it is judged.
- **Changes can't be judged sooner, and needn't be judged later.** A video's standing at 3 days barely predicts its standing at a week. Its standing at a week already matches two weeks almost exactly. So a week stays the right time to judge a change.
- **Longer videos trade seconds for views.** They get more seconds watched but fewer views, and the total time watched comes out about equal. So our main measure would favour any change that simply makes videos longer.

### Blocked
- **One decision for you:** when a change also alters video length, should it have to hold total time watched, not just seconds per view? I recommend yes. It only tightens the rule, and it does not affect the new opening unless its length moves.
- The title-failure fix and the topic-recording change each wait for a sample video, which can only be requested after 07:00.

### Next
- After 07:00, request the sample for the title-failure fix. Then refill the ready queue. Monday's data re-checks the dark, morbid topic lead.

### Better?
- **Than last shift:** yes. The tool can now answer "does this kind of video do better?" fairly. The check that will judge the new opening now covers a blind spot it had.
- **Than ~10 shifts ago:** yes, modestly. Research now closes questions within a shift: one parked idea was dropped on evidence today. None has yet changed what we ship.
- **Than ~100 shifts ago:** too early to say.
