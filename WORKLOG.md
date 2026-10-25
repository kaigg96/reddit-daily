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

## 2026-10-25 (08:25) — Bet 1's spoken sample met the bar and is on #77; one label from you ships it

    Worked (% of the shift): product 30 · data 25 · gm 20 · strategy 10 · engineering 5 · reliability 5 · security 5

**Summary:** Bet 1's spoken sample, whose three host tags all react ("Oof", "No way", "Uh oh"), is on #77, so one label from you ships it. A check of how its first two weeks could go wrong found three ways its verdict would have been misread, all fixed before any upload.

### Toward revenue
- **Bet 1 is one label from shipping.** Every route to revenue needs it, and this is the first sample since your 19 October feedback whose tags meet your bar.
- **The revenue gap is sharper.** At four a day every upload would need about 75,000 plays, about 70 times our best ever, so no hit rate closes it: the gap is each video's reach. For the 5 November review.

### Done
- **Product (bet 1, the sample):** rendered on the build machine in the free stand-in voice, with tags from the model real uploads use: 30 seconds, no faults, each tag in the pause after its answer. The opening tag ("My money's on…") was not a reaction, so it was left out as designed. Our own words are 17% of what is read (long answers); reported, never a gate. Posted to #77 with frames, the video, and this morning's upload of the same post.
- **Product (a measurement, set before it ships):** bet 1's answer to YouTube's spam rule (#80) is that the host makes each video different, but stock tags like "Oof" could repeat across videos. Fixed now: a tag on 5 or more of the first 20 uploads means a check against recent uploads' tags comes next. The three samples so far repeat none.
- **Strategy and data (a correction):** the record said each upload needs about 28,000 views at four a day, counting plays; the bar counts engaged views (37% of plays), so it is about 75,000. Corrected in both plans.
- **Data (a pre-mortem of bet 1's first two weeks: one fix, live, and three corrections):** a fresh agent assumed bet 1's read went wrong and found four causes, all confirmed. (1) The Monday report and the shifts' command would have judged bet 1 across both subreddits, though its rule reads AskReddit only and the mix shifts with it (70% before, about half after). Both now read AskReddit, with a test against misspelling; reviewed twice, no blockers, live, no video change. (2) Bet 1's videos run ~2 seconds longer by design, which alone would trip its two warning signs; both now allow for length, worked out from the old version's data alone. (3) Own words' share no longer sets the next step (your 19 October call). (4) The live tags get read by eye at the 6th upload, not first at the 20th.
- **Data (a research question, "cannot tell"):** do some topics keep more viewers past the opening? Only one topic has 8 uploads at a common age, so the report refuses; that is the answer.
- **General management:** nothing was ready. A fresh agent proposed eight ideas; two failed the filters (upload hour, already read as the time slot; counting deleted Reddit sources, which Reddit refuses our build machine). Two rankers, in opposite orders, put the same two first: the per-upload need (done) and a Partner Program readiness list (dropped: those gates bite only when we apply, about 720 times away). Third on both, the topic read (done). A second round, the pre-mortem above, found the rest. **Dropped:** a within-day pairing test (answered 5 October); a scan for paid text-only channels (done 18 October); generated music (your task, and AI music needs disclosure); the prompt trial without "agreement" (changing the prompt now would change what you are judging on #77).
- **Reliability and security:** both uploads landed today. The standing check is clean (no secrets, no workflow changes, you the only collaborator); money controls in place ($0.71 this month, forecast $0.86 of $3).
- Mostly fixes and measurement; the sample is the bet. AI use: one sample render, clear of both uploads; no Polly.
- **Process:** the "08:17" release check runs at 12:40–13:45 (GitHub starts every schedule here 4–5 hours late), so a morning shift cannot read it first, as the last handover asked; the render went ahead without it. The answer-length tool ran its whole collection when asked for usage, appending rows; reverted and fixed (reviewed). Handed over ~20 minutes early: what was left fell below the bar (a tool listing live tags, which one planned command does).

### Blocked
- **For you, in order:** #77 (watch the sample; one label ships bet 1); #82 (register our Reddit app, by 12 January); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- **If #77 is labelled:** merge the release branch once that day's release check passes on its current commit, then update the plans. The next upload is the first of the new version.
- **If you comment instead:** fix it and render again (next slot ~20:30).
- The Stack Exchange spoken sample, in a free render slot.
- 26 October weekly read, then the opening-reach read.
- The audit comes due at about ten shifts since 21 October; this was the ninth.

### Better?
- **Than last shift:** Yes. A sample whose tags meet your bar is in front of you, where last shift's was still being filtered, and bet 1's verdict can no longer be read on the wrong cut.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped, though it now waits on one label, not your machine.
- **Than ~100 shifts ago:** Too early to say.

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
