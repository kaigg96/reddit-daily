# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PLAN.md](PLAN.md) (the company), [PRD.md](PRD.md) §0 (the product) and
[TECH_DEBT.md](TECH_DEBT.md) (code health).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it within its word budget (`scripts/context_budget.py`) by deleting the
oldest entries; git history keeps them, and the audit reads them there.

**Entries are emailed to the owner verbatim as the shift report.** Write for a
manager, not an engineer: plain language, no filenames, no jargon. Technical
detail belongs in the commit message and `TECH_DEBT.md`, which is where the
next shift looks. Follow this template exactly — the report is generated from
its structure:

```
## 2026-10-06 — one line on what actually mattered

    Worked (% of the shift): reliability 10 · product 30 · engineering 30 · strategy 20 · gm 10

**Summary:** Two sentences. What moved, and whether it brought the company
closer to revenue. No detail — this is the part read on a phone.

### Toward revenue
- What this shift did that moves the company toward revenue, or "nothing
  directly, because …". Say it plainly either way.

### Done
- **Engineering:** one bullet per thing done, in plain words, led by its
  function. Say whether it fixed something or was a bet, when that isn't obvious.

### Blocked
- What is stuck, and what it is waiting on.

### Next
- What the following shift should pick up.

### Better?
- **Than last shift:** is the company closer to revenue — yes/no/unclear, and the specific thing.
- **Than ~10 shifts ago:** same, naming evidence rather than impression.
- **Than ~100 shifts ago:** same, or "too early to say".
```

**`Worked`** uses the short names of the functions in `ORG.md` (strategy, gm,
market, audience, distribution, monetization, product, editorial, engineering,
reliability, data, finance, legal, security), and it must total 100%. Since
2026-10-05 a shift works one ranked queue, so there is no planned column and no
heading per function: a function the shift did not touch is simply absent.
Reviews (`/review`) use the same shape, and the monthly one adds the sections
its skill lists. Read the series with
`venv/bin/python scripts/context_budget.py --allocation`.

**On the "Better?" section.** Numbers lag and no single one judges the
company, so a subjective read is part of the record — but a shift grading its
own work is exactly the bias the research warns about. Two rules make it worth
having: answer **comparatively** against a named horizon rather than rating out
of ten, and **name the evidence**, not the feeling. "Unclear" is a real answer
and more useful than a confident guess.

---

## 2026-10-22 (16:50) — A swear word reached this morning's title; the filter's gap is fixed and waits for one render. Reddit's own page: register by 12 January; free access still ends in March

    Worked (% of the shift): reliability 40 · legal 25 · strategy 15 · gm 15 · security 5

**Summary:** This morning's upload went out titled with a swear word, because our word filter misses words inside quote marks. The fix is built and reviewed, and goes live after one sample render. Reddit's own registration page shows that registering is not a new request, so 12 January is the real deadline. Free access still ends in March whatever we do, which makes the 5 November source choice the real answer.

### Toward revenue
- **Nothing directly.** The fix protects the channel rather than growing it. The three reads sharpen the 5 November choice of a source after Reddit, the company's one fatal, dated risk.

### Done
- **Reliability (a fix):** this morning's video went out as "Could YOUR Will Start with "Alright Fuckers"?". Our word filter misses a swear word touching a quote mark or Reddit's bold and italic marks, and the AI title then quoted the post. It was 1 of 191 uploads. The filter on answers shares the gap, and so do contractions ("shit's"). The fix catches all of these and leaves "he'll" and "who're" alone. A fresh review found one miss in my first version (a starred-out word in quotes), now fixed; a second review of that fix is noted in the tracker. On 959 old questions it flags nothing new. It changes which posts qualify, not the video. **I recommend leaving the live video as it is:** retitling it would alter one row of two running title tests, and we earn no ad money it could lose. That is yours to overrule.
- **Legal (Reddit):** Reddit's own registration page, read first-hand from an archive copy. It is for "existing apps", so 31 October (the end of *new* requests) does not apply to us. Uploads stop from 12 January if we have not registered. It needs the login of the account that owns our app and a personal Reddit account. In Reddit's words, "remaining public API access will end in March 2027", registered or not. #82 now carries the link and these steps.
- **Legal (Stack Exchange):** its licence fits a Short, on conditions: credit in the description, and the upload left on YouTube's standard licence setting. The cost: anyone could re-upload those videos, even for money, and we could not claim them.
- **Strategy:** 16 Stack Exchange sites, read for free. Not one recent question has three answers short enough to use as written (30 words or fewer). So every such video needs AI shortening, which is what made yesterday's sample read as dry advice.
- **General management:** nothing was ready. A fresh agent proposed eight ideas; five survived its filter. Two rankers, in opposite orders, put the same three on top: the filter, Reddit's page and the licence, all done, plus the fourth (the survey). **Dropped:** a sample of the "our own questions" show (not finishable in time, and its render queues behind three others). Also closed #74, as you said on #77.
- **Reliability (tonight's render):** the stand-in voice branch merges cleanly, and all its tests pass on its own and with live code.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.65 this month, forecast $0.85 of $3).
- Mostly fixing, plus reads. AI use: no Gemini, Polly or Groq; 18 free Stack Exchange requests.
- **Process:** one render per 12 hours now queues a live fix behind a sample. Tonight's slot is bet 1's, so the fix waits about a day.

### Blocked
- **For you, in order:** #82 (register; the exact page is on the issue; by 12 January, sooner is safer); #77 (tonight: watch the sample); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- **Tonight, after 20:56 UTC:** as planned, render the stand-in branch and post it to #77.
- **The slot after:** render the filter branch; on a pass naming its commit, merge it into the live branch (no version bump). Then the Stack Exchange sample.
- The 28 October re-raise of #82 can wait: re-raise in early December if it is still open.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Slightly. A live gap in what we publish is closed, pending one render, and #82's step is now exact.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. The source decision has firmer facts.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-22 (09:30) — Bet 1's samples can now speak without your hands; tonight's shift brings you one on #77. Reddit's deleted-post rule reaches our published videos

    Worked (% of the shift): product 35 · engineering 25 · strategy 15 · gm 10 · legal 10 · security 5

**Summary:** You asked on #77 for a narrated render, "or a way to get one". Sample renders can now speak in a free stand-in voice. The first one proved it works, but it was not faithful enough to send you. Tonight's shift renders the corrected version and posts it to #77, so watching it should be all bet 1 needs from you. Separately, Reddit's terms require removing posts their authors delete, which our published videos can only do by being deleted.

### Toward revenue
- **Bet 1's last step should shrink to watching an 18-second video.** Unreleased versions rendered silently, because they never hold the keys to the paid voice. Now they speak in a free voice that runs on the build machine, at Polly's pace. This morning's sample rendered and plays with speech throughout. I held it back: its tags came 0.3 seconds late, flattering exactly the timing you objected to, and they came from the weaker free model. Both are fixed. Future spoken samples also take their tags from the model uploads use. A sample can be rendered only once every 12 hours, so the corrected one comes tonight, with the link on #77.
- Uploads never reach the stand-in; their paid voice is unchanged.

### Done
- **Product and engineering (a bet on unblocking bet 1):** the stand-in voice, reviewed by a fresh agent. It found nothing that could touch uploads or spend Polly. It did find four real problems, now fixed. A stalled download could have overrun the render's time limit. A half-installed voice would never have been repaired. The voice's software could see our API keys. And the captions split sentences differently from uploads. A second review of the fixes found three smaller ones, also fixed: a slow download could still overrun, one test could not fail, and captions dropped symbols such as "$". Also done, as it advised: downloads locked by fingerprint, and a test that uploads cannot reach the voice.
- **Strategy (a bet, for the 5 November review):** a sample of the Stack Exchange show is built and renders locally: today's top workplace question, three answers each cut to one sentence by the free AI model, credited by name, spoken by the stand-in. As found yesterday, it reads as dry advice, and the host's tags came out as labels ("Smart move", "Realistic"). It renders after bet 1's sample, so the review can show it.
- **Legal:** Reddit's rule on deleted posts, read first-hand. It is not new: it has been in Reddit's developer terms since September 2024. Deleted posts and comments must be removed "as soon as possible", and Reddit's help pages say anyone using its content must "stop displaying or using" them. No clause names videos, but it most likely reaches ours, and a video can honour it only by being deleted. That bears on the old videos' fate, which comes to you with the rename.
- **General management (ranking):** nothing was ready. A fresh agent proposed eight ideas, and five survived its own filter. Two more agents ranked those, in opposite orders, and agreed on the top three: the stand-in voice, the Stack Exchange sample, and the deleted-post read, all three done. **Dropped:** Reddit's developer fund ($4,000 once, at 5,000 daily users of an app inside Reddit, which we do not have); re-tuning when the host's opening tag shows (it tunes a version you have not approved); and putting bet 1 onto the live branch switched off so the paid voice narrates it (the stand-in does the same without that risk).
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.64 this month, forecast $0.85 of $3).
- **Process:** with one render per 12 hours, a flaw the review caught became a half-day wait for your sample. Reviewing before requesting would have avoided it.
- Mostly bets. AI use: one sample render (2–5 Gemini requests), one local Gemini request, two Groq; no Polly. Handed over ~15 minutes early: a last round found nothing finishable (the clip rule, its closest, was read 10-21).

### Blocked
- **For you, in order:** #82 (register our Reddit app, before 31 October); #77 (tonight: watch the linked sample, then one label); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- **Tonight, after 20:56 UTC:** request a render of the stand-in branch. On a pass that names its current commit, merge it into the release branch and post the sample's link to #77 with the same key, saying what differs from an upload (the voice only).
- The next 12-hour slot after that: render the Stack Exchange sample branch, for the 5 November review.
- If #82 is still open on 28 October, raise it once more with the same key.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes. Bet 1's last step no longer needs you to run anything, once tonight's sample is posted.
- **Than ~10 shifts ago:** Slightly. Watch time is flat at 12 seconds and bet 1 has not shipped, but the step holding it since 19 October is nearly the smallest it can be.
- **Than ~100 shifts ago:** Too early to say.
