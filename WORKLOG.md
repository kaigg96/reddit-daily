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

## 2026-10-21 (22:45) — Reddit is closing the free access every video starts from: please register our app before 31 October; free access ends by March 2027

    Worked (% of the shift): legal 30 · strategy 25 · gm 20 · market 10 · data 5 · reliability 5 · security 5

**Summary:** Looking for new work turned up a Reddit announcement of 30 September. New requests close on 31 October, apps not registered lose access from 12 January, and free access ends by March 2027. Every video we make starts from that access, so this is now the company's largest risk. You have one new ask (#82), and shifts are pricing other sources for the 5 November review.

### Toward revenue
- **Our supply now has an end date.** I read two reports of Reddit's announcement first-hand (TechCrunch, and a fuller one quoting Reddit's developer posts). New access requests close on 31 October. Apps not registered lose access from 12 January. Free access ends by March 2027; after that Reddit wants "commercial deals", reported at around $12,000 a month, which is out of reach for us. Nothing in the project had recorded it. Bet 1's host carries over to any source; the readings do not.
- **#82 asks you to register our app before 31 October,** and to ask Reddit whether a small registered app keeps access after March. Registering is free and needs your Reddit account; Reddit may already have emailed it a reminder. It is quicker than #77 and has a date, so it comes first. Reddit's replacement platform lacks Python and serves apps inside Reddit, so it cannot carry our source.
- **The alternatives are priced in a first pass** (under Done), and the rule for the 5 November proposal is fixed. It resumes on Reddit's reply or that review.

### Done
- **Legal and market (a bet):** what could replace Reddit. Stack Exchange's terms allow our use, free. The condition: each video credits and links every author and carries the same open licence. It could supply two a day: 13 of 21 live questions on its workplace site have three or more answers. But those answers run 100 to 360 words against our 12. Its licence lets us shorten them, which Reddit's never did. The free AI model cut six to about 14 words each, accurate but dry advice, and both questions were too long for our titles. So it would be a different show, not a replacement. Writing our own questions and having AI write the answers costs no licence. But on two of our questions it wrote stock jokes and invented a personal story, so those answers could only be presented as the host's own. Hacker News and Mastodon do not allow this use. Also noted: Reddit's rules reportedly now bar apps from showing posts their authors deleted, which our published videos cannot honour. No other service we depend on has a shutdown date. Bet 1's host needs three short, distinct answers to react to: shortened Stack Exchange answers give that, while AI-written ones would have the host reacting to itself.
- **Strategy:** the risk register now carries the new risk, rated fatal. The Reddit-terms row also said Groq's no-training tier lands with bet 1; it lands only as a backup (the full move is blocked on its tags), now corrected.
- **General management (ranking):** nothing was ready. A fresh agent proposed eight; two more ranked them in opposite orders and agreed on the top three. First: whether Reddit grants commercial agreements to small creators at all. It turned up the dates above. Second: writing down, before bet 1's results, the numbers that would put a change of direction on your agenda. The end of free access now forces that question by March, so it was overtaken. Third: checking that the 26 October read will run. It will: the step that has never run on real data works on today's figures. **Dropped:** the break-even point (it needs the subscription's price); old duplicate uploads (most share a question, not a video); asking you to change the shift schedule (short shifts are ours to fix); whether views are bunching into a few hits (noise); a comment-hold setting (one abusive comment).
- **General management (second round, after the news):** a fresh agent proposed six more. Taken: the 5 November proposal's rule, fixed now before Reddit replies. If Reddit confirms in writing that our app keeps access after March, stay. Otherwise you watch a narrated sample of each replacement as a first-time viewer, by mid-December, and the one you follow ships by early February. **Dropped:** agents scoring the replacements blind (weaker than your viewing); drafting answers for Reddit's form (we cannot see it); reorganising the code for a second source (before you choose); post titles in our public files (changes nothing); a test that losing Reddit stops a run (it does).
- **Data and reliability:** the scorecard's jump in median views is noise (four-week totals ×0.93). The zero-view recent uploads are the usual reporting lag: every week since July shows 3 to 5. The watched clip stays under its retirement bar. Bet 1's branch with today's main passes 694 tests. A run that loses Reddit access fails loudly rather than skipping an upload silently.
- **Security:** the standing check is clean. No secrets are in the project, no workflow has changed since this afternoon, you remain the only collaborator, and the money controls are in place.
- Neither a fix nor a change to what ships: a risk found. AI use: four free Groq requests. Handed over about 35 minutes early: nothing else ready.
- **Process:** a change fatal to our supply sat public for three weeks while ten shifts looked for work. The monthly review's outside look should cover the source's developer news. For the 5 November review. Also awkward: waiting on helper agents takes timed pauses, because the tool that watches for them is refused here.

### Blocked
- **For you, in order:** #82 (register our Reddit app, before 31 October); #77 (one narrated render, then one label); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- The 5 November proposal on sources follows its fixed rule; Reddit's answer on access after March, if you register, decides which branch.
- If #82 is still open on 28 October, raise it once more with the same key (a comment emails you): after the 31st, registering may need a new request Reddit no longer accepts.
- 26 October weekly read: check how many uploads it marks as failed, then run the opening-reach read once.
- 5 November monthly review: the source proposal, and narration on test renders, now needed twice: bet 1 and the replacement samples.

### Better?
- **Than last shift:** Yes, in what we know: the company now sees that its supply ends by March 2027, with ten days to be safe on registering. Nothing changed for viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. The plan is truer: it now carries a dated, fatal risk it had missed.
- **Than ~100 shifts ago:** Too early to say.
