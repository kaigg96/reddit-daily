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

## 2026-10-20 (16:35) — A new wording made the host's opening tag react on the free models, from none of 17 to 9 of 16; a failed AI request now says whether the day's allowance is gone

    Worked (% of the shift): product 30 · reliability 25 · gm 20 · editorial 10 · engineering 5 · legal 5 · security 5

**Summary:** The host's opening tag, which nearly every viewer sees, has come out as a title on every model tried. A new wording made it react on about half of the free models' tries, so tomorrow's few requests on the upload model can go straight to it. Separately, failed AI requests now say whether the day's allowance is spent, and that change is live. Nothing reached viewers.

### Toward revenue
- **A wording for the host's opening tag worth spending tomorrow's AI requests on.** On every model so far the opening tag came out as a title for the question ("Brutal truth"). I asked instead for "the words you would blurt out the moment a friend asked you this question". Both free models then reacted on 9 of 16 tries ("Ouch, right?", "Sounds shady"), against 0 of 17 with today's wording, scored blind in one mixed sheet; a second blind scorer agreed on 32 of the 33. The catch: one model opened most of them with "Sounds…", which is the sameness YouTube's spam policy names. The model uploads use has not tried it yet. The trial tool now runs it with one setting.
- **A better free model for the host's tags, if we must leave Gemini.** Moving every AI call to Groq would stop Reddit's text being used for training, which Reddit's terms forbid. But Groq's model turned the host's reactions into labels. Groq's other free model, on the same nine posts and scored blind, reacted to 10 of 24 answers against 4 of 27 ("Four hours?", "Sad face"). But none of its opening tags reacted with today's wording, and 2 of its 11 replies had no host lines at all. Neither model meets the bar, which the upload model nearly meets, so nothing switches.
- **An upload's lost title can now be explained.** When the AI refuses a request for being over its limit, the upload log and the release check now say which limit it hit. If it was the daily allowance, the next upload's title is at risk until the 07:00 UTC reset. If it was the per-minute limit, a short wait would have cleared it. Today's release check was refused on its fifth content-screen case, after this morning's trials. It was the first such refusal in eight days of checks, and nothing recorded which limit it hit. The change was reviewed fresh with no defects found, all tests pass, and it is merged.

### Done
- **Editorial:** about 1 upload in 20 re-asks a question the channel already covered (4 of the last 60, such as "the scariest story you know is true"). Each was a different post with different answers. Exact repeats numbered 4 in 187, none since the 8 October guard. That is not enough to need a new guard before four a day.
- **General management:** a fresh agent proposed eight candidates, and two more ranked them in opposite orders. The repeat check led both and is done. The Groq model trial came second and third and is done; the opening-tag wording grew out of it. **Dropped:**
  - a pivot checkpoint: the quarterly planning already judges each bet against its set bar.
  - whether 7-day watch time predicts later views: third one way, seventh the other, and under 1% of views come from old videos.
  - the background clip and how many viewers stay: two weeks of data, split across many clips.
  - pricing Reddit's commercial data deal: you said not yet (#60).
  - why shifts end early: nothing records how much ready work each shift had.
  - a subscriber benchmark: it changes no decision.

  Mostly fixing; the two tag trials are bets.
- **Engineering:** the trial tool now takes the new wording and a choice of Groq model, on bet 1's branch. A fresh review found no defect in that, but it did find an older hole: a Groq trial run without Groq's key would quietly spend up to 18 of the day's 20 upload-model requests. It now refuses before any request. All tests pass, and the branch still merges cleanly.
- **Security:** the standing check is clean. No secrets are in the project, no workflows changed, you remain the only collaborator, and the money controls are in place ($0.60 this month, forecast $0.81 of $3).
- AI use: none on Gemini (an upload was due within the hour), and about 55 requests on Groq (free).

### Blocked
- **For you, in order:**
  - #77: nothing until a render is worth watching.
  - #80: one label (four a day waits for bet 1, music first), needed by about 1 November.
  - #50: four commands, which unblocks #65.
  - #59: the account checks.

### Next
- First: check that this afternoon's upload landed, and read its log row. If its title fell back, the new label says whether this morning's trials used up the day's allowance.
- After 07:00 UTC and away from uploads, run the opening tag on the upload model with the new wording against today's, on three posts per shift. Check whether it reacts, and whether every tag opens the same way.

### Better?
- **Than last shift:** Slightly: the weakest, most-seen part of bet 1 has a lead, and a failure that can cost an upload its title is now visible. Nothing changed what viewers see.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, and bet 1, built 11 October, has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-20 (09:25) — The host's weak reactions came mostly from the cheaper test model; your next render can show the real ones and buy its narration once

    Worked (% of the shift): product 45 · engineering 25 · gm 10 · legal 10 · security 5 · reliability 5

**Summary:** The reactions you judged weak in last night's renders were written by the cheaper model that test renders use. On the same posts, the model real uploads use gave real reactions for 7 of 9 answers, against 1 of 9. Your next narrated render can now use the upload model, runs on your machine's Python, and pays for each narrated line only once. Nothing reached viewers.

### Toward revenue
- **Bet 1's tags are closer than they looked.** The main bet's tags were judged on the wrong model. On three posts the upload model reacted ("Ouch", "No thanks"); the test model labelled ("Liquid gold", "Free labor"). That shows direction, not a rate. Posted on #77; nothing there waits on you.
- **Your next render is cheaper and shows what an upload would.** One setting writes its tags on the upload model (one request); another reuses narration already bought, so re-rendering to adjust timing does not pay again. The build now loads on your machine's Python 3.10.
- **What to fix next is clear.** The host's opening tag, shown as the question ends, is seen by nearly every viewer. The first reaction is seen by about half and the third by under a fifth (current version, 14 videos at 7 days). The upload model's opening tag was a title, not a reaction, on 2 of 3 posts ("Brutal truth"), so that comes first.
- **The host's spoken vote no longer gets dropped for running a few words long.** It was held to the on-screen notes' limit though it is spoken, and was dropped on 4 of 12 trial posts, risking bet 1's rule that every host line shows on 15 of its first 20 uploads. It now has a spoken line's limit (22 words).

### Done
- **Legal:** moving every AI call to Groq (whose terms forbid training on what we send) would turn the tags back into labels (about 2 of 27 reactions), so that move must now pass the tag bar too. A rule that lifted Groq to 14 of 24 made every tag open the same few ways, the sameness the spam policy names; not kept.
- **Product:** a reworded prompt did not help on the test model (10 of 27 reactions against 9 of 27); not kept. Reddit blocks this runner, so trials used our real recent questions with answers written in Reddit's style. A small trial tool reruns the same nine posts on any of the three models, capped at 3 upload-model requests a run.
- **Engineering:** the logs and release check now record which host line was dropped and its length. Each change was reviewed fresh, findings fixed, all tests pass; all on bet 1's branch. Merged: two tests no longer fail on your machine's older git.
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.53 this month, forecast $0.80 of $3). Every upload since Sunday landed.
- **General management:** a fresh agent proposed eight candidates, and two more ranked them in opposite orders. Both put the vote fix first and a render kit for you second; the kit was covered by the note on #77. **Dropped:** a request counter (production does not record requests); a music shortlist (needs your Audio Library login); re-scoping bet 2 (for review). A second round of six, beyond the product, put an earlier read of new versions first both ways. Checking it, I found our reporting tool had been mislabelling ages, which is behind the rule to read new versions at 7 days. Fixed, reviewed and merged. By true age, a video's watch time at 3–4 days ranks it as a week later (0.99, 29 videos). Reads stay at 7 days: with weekly data, an earlier target would catch some videos under 3 days old, which a fresh check showed before I changed it. If Google retires the upload model, titles fall to the second model, logged (checked in code). Mostly fixing; the trial tool and narration reuse are bets.
- AI use: 18 requests on the test model, 6 on the upload model (the shift may use 8), about 20 on Groq (free). The test model's allowance is undocumented and production falls back to it, so trials there stopped.

### Blocked
- **For you, in order:** #77 (nothing until a render is worth watching); #80 (one label: four a day waits for bet 1, music first; needed by about 1 November); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- First: check that this afternoon's upload landed.
- Read today's release check: it runs this build, so it shows the upload model's tags for one post and, if a line is dropped, its length.
- The opening tag on the upload model, using the trial tool after 07:00 UTC and away from uploads. One try this shift (a tease of the answers coming) moved it from 1 of 3 reactions to 2 of 3. But the unchanged reactions also swung from 3 of 3 to 1 of 3 on the same post, so three posts cannot tell two wordings apart. Compare on all nine posts, across two or three shifts' allowance.

### Better?
- **Than last shift:** Yes, slightly: the weakest part of the main bet had been judged on the wrong model, and your next render will show the real thing at less narration cost. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.
