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

## 2026-10-24 (22:30) — Bet 1's release passed a full review with no blockers; its tag filter now also drops tags that call an answer right

    Worked (% of the shift): product 30 · engineering 25 · gm 25 · data 10 · reliability 5 · security 5

**Summary:** Everything bet 1 changes passed its first full review since 13 October with no blockers, which clears one of the steps between your approval and the merge; its two small findings are fixed. Today's release check showed a host tag agreeing with its answer ("Plastic crack is right"), and the filter now drops that kind too, before tomorrow morning's sample for you.

### Toward revenue
- **Bet 1 is closer.** Every route to revenue needs bet 1. Its last gate is you watching a sample whose tags react rather than grade or agree, and the merge after that needs a full review, now done. One more way of agreeing is stopped in code before that render, and a blank line can no longer cost an upload its whole host.

### Done
- **Engineering (a check, then two fixes, on the release):** a fresh review of everything bet 1 changes. **No blockers**: uploads, the live record files, the Polly budget and the test-mode guard all check out. It found one thing worth fixing: one blank host line cost every host line, so the upload went out as a plain reading; now only the blank line drops. Flag emoji also slipped past the emoji check (they would show as empty boxes); now caught in tags, and in titles and on-screen answers too (one past answer carried a flag).
- **Product (a fix, on the release):** "Plastic crack is right" agrees with the answer, which on a politics thread takes a side, and the afternoon's filter let it through. Tags that call an answer right ("That's right", "Exactly right", "Sounds about right") and "Truth" on its own now drop; after "not" they ship, as doubt ("Not quite right"). It drops none of the 30 tags from past release checks and renders, or of 204 short quoted phrases in our records. A fresh review found one wrongly dropped kind of doubt and a few missed forms; fixed. Rare edge cases are recorded, not chased.
- **Product (measurement, on the release):** when a filter drops a tag, the log now shows what the tag said, not only its length. For four days the release check has said only that the opening tag dropped, so nobody could tell whether the filter was right; tomorrow's will show it. Its review caught two faults (cutting a long line could create a slur; a tag like "Failed attempt" would read as a failed render); both fixed.
- **General management (a fix, live):** the tool that shows the idea generator what earlier shifts dropped had been blind since 20 October: shifts began listing drops inside another bullet, and it only read bullets that opened with them, so any round since could re-propose a rejected idea. It now reads both, whole. Its review found it could mistake ordinary text for a drop list; fixed before it went live.
- **Reliability (a check):** the release passes all its tests on Python 3.10, the version on your machine (last checked 21 October), and a silent sample renders there (1080×1920, 28 seconds).
- **Data (a fix, live):** the capitals test's one-word arm shipped two capitalised words today ("Which Halloween costume will YOU see the MOST?"), 1 of its 11 titles. It is now held to one in code, as the no-capitals arm has been since 16 October. Titles only, so no render or version change; reviewed, no blockers.
- **General management:** nothing was ready. I found the tag myself; a fresh agent proposed four ideas, one of them the same tag. Two rankers, in opposite orders, agreed: the full review first, a note for tomorrow's sample second, the tool fix third, closing an old record last. All done. A second round found the Python check and the capitals leak, both done. **Dropped:** code to stop two alike tags in one video (no repeat on record); tags that echo the answer with a laugh (still a reaction); refreshing the bet 1 issue's description (tomorrow's sample comment replaces it); the functions with no recent time (two rounds found nothing, and no new figures arrive before the 26th).
- **General management:** closed the record of the shift that ended after 2 minutes on 19 October. Its condition was ten shifts with the new trace: all ran 26–56 minutes and handed over (three short runs on the 22nd and 23rd were the weekly allowance guard, as designed).
- **Reliability and security:** both uploads landed today. The standing check is clean: no secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.70 this month, forecast $0.86 of $3).
- Mostly fixes, plus one measurement. The channel reads flat (12 seconds for six periods); bet 1 is the item that changes what we ship. AI use: none (no upload-model, Groq or Polly requests, no render).
- **Process:** side branches lived in separate copies of the project while agents read the main one, so the trap the last two shifts hit did not recur. Handed over about 20 minutes early: a last look found nothing above the bar (a length cap on the sample report, rarely reached; an unreadable AI reply echoed to the public log, low harm; more agreeing wordings, none yet seen).

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **The first shift after about 07:30 UTC:** read the 08:17 release check (it now shows what each filter dropped), then render the release branch and, if its tags react rather than grade, post the sample to #77. If the sample's question leans on a post body the viewer never sees (first-person or advice, as on 23 October), say so in that comment, so the host is judged and not the post; render again only if a tag fails the bar.
- The trial wording that drops "agreement" from what the prompt asks for, on about three trial posts with the upload model's allowance, after the 07:00 reset.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes, slightly. The full review the merge needs is done with no blockers, and two more ways a tag could fail are stopped before the render you will watch. Nothing reached viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-24 (15:30) — The swear-word fix is live; bet 1's host now also drops tags that agree with an answer, and its sample waits only for tomorrow's render slot

    Worked (% of the shift): reliability 30 · product 35 · gm 25 · security 10

**Summary:** The fix that stops a swear word reaching a title, like Thursday's "Alright Fuckers", passed its sample render and now runs on every upload. Bet 1's host now also leaves out tags that simply agree with an answer ("Well put", "Amen"), which on politics would take a side; its sample waits only for tomorrow morning's render slot.

### Toward revenue
- **Bet 1 is a little closer.** Every route to revenue needs it, and its last gate is you watching a sample whose tags react rather than grade. The filter now catches agreement as well as stock praise, so the next sample is less likely to be held back, or to repeat your 19 October feedback. The next render slot the shift rules allow opens about 07:30 tomorrow.
- The swear-word fix protects the channel rather than growing it: a sworn title risks the advertiser-friendliness the Partner Program checks.

### Done
- **Reliability (a fix, live):** the swear-word filter now catches a word next to a quote mark or inside a contraction, and an AI-written title, closing line or keyword with a swear word or emoji falls back to a safe one. It passed its sample render, four earlier reviews and a fresh check of how it meets today's code. It changes which posts and lines qualify, not the video, so no version change and no effect on the running tests.
- **Product (a fix, on the release):** a check (the pre-set test was whether any political-agreement tag on record gets past the filter). The two or three on record ("Math checks out", "Ah, makes sense") were already caught. But that record is thin, and about 20 common ways of agreeing were not ("Well put", "You're right", "Amen", "Hell yes"), so those now drop too. None of the 55 tags on record from past checks and renders newly drops. A fresh review found two reactions it would have wrongly dropped ("100% chaos", "Got nailed"); both fixed.
- **Product:** the release branch now carries both tag filters and the swear-word guard for the host's vote and tags. So your own render command on #77, tomorrow's automatic release check and the next sample all use them. The issue's description says so (edited, no email).
- **General management:** nothing was ready. A fresh agent read the evidence and proposed eight ideas; two survived, and I added one. Two rankers, in opposite orders: the political-tags check came first and second; moving the filter onto the release branch second and third (both done). **Dropped:** draft answers for your Reddit registration (ranked first by one ranker, but the form's questions were never recorded, so the answers would be guesses, and it would be a fourth email on that issue in four days); restating bet 1's dose rule (accepted on 21 October); an early read of the capitals test (the report refuses it, 1 upload against 6); two other networks as sources (authors keep their rights, as with Mastodon); a related-video link (your Studio, and a new variable mid-test); affiliate links (not clickable on Shorts).
- **General management (second round, aimed at the functions with no recent time):** five ideas, none above the bar. The views needed to cover the AI subscription (its price is written nowhere here, so it needs you, and changes nothing while every route is hundreds of times short); search's trend (1.6–2.2% a week, already answered); a subscriber rate (21 subscribers, too few); what the top tenth of uploads share (it would read the running subreddit test early); a check of the working name (waits for bet 1). One fact for the 5 November review: "revenue above costs" has no cost figure to aim at. Handed over about 20 minutes early for that reason.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.70 this month, forecast $0.86 of $3).
- Mostly fixes. AI use: one sample render (its own test allowance); no Polly, no other AI requests.
- **Process:** I switched branches in the shared working copy while the idea generator was reading from it, the same trap the last shift noted. Work on side branches belongs in a separate copy while an agent reads.

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **The first shift after about 07:30 UTC:** render the release branch and, if its tags react rather than grade, post the sample to #77. The 12-hour limit lifts at about 02:40, but its tags also spend one upload-model request, so the rule of waiting for the 07:00 reset and an hour clear of a scheduled run applies until #65 lands. Read tomorrow's 08:17 release check first: it shows the filtered tags on a fixed post.
- The trial wording that drops "agreement" from the reactions the prompt asks for: read it on about three trial posts with the upload model's allowance, after the 07:00 reset.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Yes, slightly. A live defect seen once in 191 uploads is closed, and bet 1's tags have one more failure stopped in code before the render you will watch.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
