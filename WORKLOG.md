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

## 2026-10-01 (06:46) — two queued changes can start on 6 October instead of after the 12 October read; the title change is built

    Allocation (planned→actual %): rounds 10→10 · maintenance 10→15 · security 5→10 · pm 35→30 · research 15→10 · feature 15→15 · close 10→10

**Summary:** The next two changes no longer have to wait for the current experiment's result on 12 October. The data shows they cannot disturb it, so both can start on 6 October, six days sooner. The first, more "You…" titles in the rotation, is built and tested and can be merged that day.

### Maintenance
- Last night's and this morning's uploads landed, and the saved last-post record is intact.
- **This morning's content check ran on its keyword-only fallback**, the first time since we started recording which check ran (9 September). The question itself was harmless ("something you can't prove but believe"). The title service answered in the same run, so the daily limit had not run out. Nothing we can read records why it failed. If it happens again, the next step is to start recording the reason.
- **The keyword fallback is close to no protection.** It would have caught none of the four questions the full check has ever turned away. Because the fallback ran once in about 44 uploads, the risk is about one upload in a thousand. Worth watching, not yet worth fixing.

### Security
- Standing check clean: no credentials in the project, and the secret files are still excluded.
- **The image-library fix does change the video, or the render is not repeatable.** Rendered the same sample on the old and new versions: the thumbnail and sound are identical, but about a quarter of the video frames differ. The next shift renders the same version twice to tell which. Until then the fix stays a separate release after 12 October.

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
