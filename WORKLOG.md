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
- **General management:** a fresh agent proposed eight candidates, and two more ranked them in opposite orders. Both put the vote fix first and a render kit for you second; the kit was covered by the note on #77. **Dropped:** a request counter (production does not record requests); a music shortlist (needs your Audio Library login); re-scoping bet 2 (for review). A second round of six, beyond the product, put an earlier read of new versions first both ways. Checking it, I found our reporting tool had been mislabelling ages, which is behind the rule to read new versions at 7 days. Fixed, reviewed and merged. Read by true age, a video's watch time at 3–4 days ranks it as it does a week later (0.99, 29 videos). If Google retires the upload model, titles fall to the second model, logged (checked in code). Mostly fixing; the trial tool and narration reuse are bets.
- AI use: 18 requests on the test model, 6 on the upload model (the shift may use 8), about 20 on Groq (free). The test model's allowance is undocumented and production falls back to it, so trials there stopped.

### Blocked
- **For you, in order:** #77 (nothing until a render is worth watching); #80 (one label: four a day waits for bet 1, music first; needed by about 1 November); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- First: check that this afternoon's upload landed. Then decide whether bet 1's read moves to 4 days before it has data. Every experiment would read three days sooner; reads already under way keep 7.
- Read today's release check: it runs this build, so it shows the upload model's tags for one post and, if a line is dropped, its length.
- The opening tag on the upload model, using the trial tool after 07:00 UTC and away from uploads. One try this shift (a tease of the answers coming) moved it from 1 of 3 reactions to 2 of 3. But the unchanged reactions also swung from 3 of 3 to 1 of 3 on the same post, so three posts cannot tell two wordings apart. Compare on all nine posts, across two or three shifts' allowance.

### Better?
- **Than last shift:** Yes, slightly: the weakest part of the main bet had been judged on the wrong model, and your next render will show the real thing at less narration cost. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-19 (18:25) — Weekly review: YouTube's spam rules now reach formats like ours, so I recommend four uploads a day waits for bet 1; watch time is still flat

    Worked (% of the shift): legal 25 · data 25 · engineering 15 · audience 10 · gm 10 · product 5 · reliability 5 · security 5

**Summary:** YouTube's spam policy, whose penalties run to closing a channel, now treats mass-producing "similar content with minimal changes" as spam, and its example shares one trait with us exactly: the same music on every video. I recommend four uploads a day waits for bet 1 rather than going first on 2 November, and that the extra music goes in first (#80). Watch time is flat at 12 seconds; nothing reached viewers, and bet 1 still waits on #77.

### Toward revenue
- **A risk to the channel itself, found before we doubled the volume.** The policy's example is word for word: "Channels that use the exact same background music and repetitive AI generated imagery across many videos, with each video reading out an AI-generated script." Every recent upload uses the same music track; our clips are filmed stock, not AI imagery, and our narration is mostly Reddit's own words, so the music is the one exact match. We have had no strike in about 1,050 uploads, so this is a risk, not an event. YouTube does enforce it: 20 channels closed in September for AI-scripted political commentary, and 16 large AI channels over the winter. A Reddit-story channel lost its pay in May but was not closed. I found no small channel like ours closed, so I rate the risk low but rising with volume (added to #80). Bet 1's host takes no side on political threads and states no facts in its own voice, so it does not resemble the closed political channels. But this morning's plan had four a day going first if bet 1 is still unshipped on about 2 November, and a 14 October shift set this concern aside only because four a day then waited for bet 1. #80 asks you to approve waiting (bet 2 would likely miss its window) and the music task first. Your label on #77 is still the main answer: the host's notes are what make each video add something of ours.
- **Two worries about four a day are settled.** YouTube now gives uploads their own allowance of 100 a day (Google's page, 15 October), so four a day uses a fifth of the remaining quota, not most of it. And Google has announced no retirement date for our main AI model.
- The weekly job now retries when YouTube's servers fail. One failure this week lost 23 videos' "where viewers leave" readings, and bet 1's check of its notes depends on those readings. The 8 earlier videos that check compares against are already measured.

### Done
- **Product:** watch time is flat at 12.0 seconds for a sixth week. Typical views at 7 days rose from about 49 to 139 over three weeks, but four-week totals are unchanged (×0.93), so fewer videos are buried while the hits are no bigger. No experiment's rule has come due: the subreddit test has 9 and 8 of its 15 a side, and should have about 17 by 2 November; the title-style test has 13 and 5 of its 15 and 8. Today's version still reads 15% ahead of the one before it (38 uploads). The watched background clip stays (its rule does not fire).
- **Data:** dark-morbid topics' lead did not hold. At 12 videos it reads 8% ahead, inside what chance produces, so ranking posts by topic stays parked. The new retention readings arrived for every recent video with views, except the 23 above. Subscribers held at 21 for the week.
- **Engineering (fixing):** the retry above, and the comment download no longer counts our own closing-question comments as viewers' (15 of its 22). Reviewed fresh with no defects found; all tests pass; merged. The waiting bet 1 release still merges cleanly.
- **Audience:** the first read of viewer comments: 7 in a week, all on one political video (US support for Israel), mostly heated and one abusive. No other video drew a comment. Automatic replies would have nothing to answer, so that work is parked until comments appear on three or more videos in a week.
- **Distribution:** 95% of views still come from the Shorts feed and 2% from search, unchanged.
- **Reliability and security:** every upload this week landed; one (18 October) went out with the raw question as its title, as reported. The scheduler's delay is not rising after all: last week's median was 4.6 hours, against 6.5 from its first three runs. Today's afternoon upload had not started by 18:15, which is late but inside delays seen before (up to 9 hours). The content screen skipped no post and trimmed one comment. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.52 this month, forecast $0.82 of $3).
- **General management:** a fresh agent proposed eight candidates, ranked in both orders. The quota and model checks led both, done; the spam-policy read came from the same list, done. **Dropped:** rebuilding the slot log for four a day going first (wasted if my recommendation holds); re-checking AI disclosure (settled 18 October); three others already done above. Mostly fixing and checking; the spam read is the one finding that changes a plan.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #80 (one label: four a day waits for bet 1, music first; needed by about 1 November, so #77 still comes first); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- First: check today's afternoon upload landed; if not, it is an incident.
- On #77's label: merge it as the next version, close #74, update the trackers.
- On #80's label: make "four a day waits for bet 1" the plan in both trackers and close the issue.
- 26 October weekly review: if #77 is still open, one comment on it naming 1 November and the four-week cost; check the retention readings came through without gaps and the comment count no longer includes ours.
- 5 November monthly review: as listed in the previous entry, plus the spam policy beside YouTube's originality rules, and whether it changes the proposal on the 1,041 old videos (all readings with the same music).

### Better?
- **Than last shift:** Slightly: a risk to the channel itself is on record before we doubled the volume, and two worries about four a day are settled. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.
