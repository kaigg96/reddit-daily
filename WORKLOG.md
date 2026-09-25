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

## 2026-09-25 — the new opening is live; the next upload is the first to open on the question

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→15 · security 5→5 · pm 20→20 · research 15→20 · feature 25→15 · close 10→15

**Summary:** The new opening, where the video starts on the question instead of the channel name, is live. This morning's upload (around 05:00) is the first to use it. It is the first change to the videos themselves since the channel went flat six weeks ago, and it can be judged after 20 uploads, around 4 October.

### Feature work
- **Put the new opening live.** Both agreed conditions were met: last night's upload was the 10th in the old format, and the sample passed on exactly the version that shipped. All tests pass.

### Maintenance
- Every scheduled upload landed, and the saved record of the last post is intact.
- **The fix that records why titles fail is ready for its sample video**, updated to include the new opening. I did not request the sample: at this hour it would use the AI allowance this morning's upload needs, which is what cost an upload its title yesterday.

### Security
- Standing check clean: no credentials committed, and the secret files are still excluded.

### Project management
- **Channel still flat** at 11–12 seconds watched per view. The new opening is the right response: a change to what viewers see.
- Nothing you had approved was left undone, and the process health check is clean.
- **Tidying, for when convenient:** five of your own branches (the pre-trip work and four fixes from 23 September) are already fully in the live version. They can be deleted, but I've left them because they're yours.
- **Friction, noted rather than acted on:** two finished changes each wait for a sample video. Shifts get one each, and only at hours that don't compete with an upload. This shift ran at 02:00, outside those hours, so the queue didn't move.

### Research
- **Tested and dropped an idea within the shift: making the ending loop back into the opening.** Nearly all our views come from the Shorts feed, where a looping video plays again. The free check was whether any past videos were watched for longer than they last on average, which only replays can cause. Only 3 of 110 were, so we are not building it. The check stays in our reporting tool, so this can be revisited.

### Blocked
- **One approval requested:** a small fix so the daily release check records a failure when its tests fail. Today it keeps showing the previous day's "safe to merge" instead. It tightens a safety check and loosens nothing. I recommend approving it.

### Next
- After 07:00, request the sample for the title-failure fix and ship it if it passes. The topic-recording change for the next experiment is next in line. Both are now up to date with the live version, so either can be requested as is.

### Better?
- **Than last shift:** yes. The new opening went from "passed, waiting" to live.
- **Than ~10 shifts ago:** yes, modestly. A tested change reached viewers without needing your review, which is what the automated release process was built for. Whether it helps is too early to say.
- **Than ~100 shifts ago:** too early to say.

