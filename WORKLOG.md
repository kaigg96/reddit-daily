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

## 2026-10-20 (22:18) — Bet 1's planned check of where viewers leave would have missed the opening, and is fixed before any data; the distance to revenue is now computed, and had drifted

    Worked (% of the shift): data 30 · product 25 · gm 15 · monetization 15 · legal 5 · reliability 5 · security 5

**Summary:** Nothing reached viewers: the step that would needs AI requests that tomorrow morning's upload shares. Instead, bet 1 will now be judged on the right viewers, and the plan's distance to revenue is computed from our data (the Partner Program is about 720 times short, not 760–880).

### Toward revenue
- **Nothing directly.** The upload-model trial waits for the 07:00 UTC reset.
- **Bet 1 will be judged on the right viewers.** Its pre-set rule reads where viewers leave from YouTube's retention figures, and would blame the host's opening tag if the 25% mark fell. Those figures leave out everyone who swipes away. On all 29 recent uploads, as many viewers or more are counted at 10% in as started the video, though only 20–58% of their plays count as real views. So a weak opening would never show there. It shows in the share of plays that become real views, which we already track. The rule now says so, written before any of bet 1's uploads exist.
- **One failed request no longer loses a week of that data.** On 19 October a single server error, a third of the way through the weekly read, cost the 23 uploads after it their retention figures. Each upload gets only one reading at a week old. Retries were added that day; now an error that outlasts them costs only its own upload. Reviewed fresh (one missing test, added); merged.
- **Each revenue route's distance is now one command, and the plan's figures were stale.** Partner Program: about 720 times short on views and 48 on subscribers. New applicants from February: about 1,450. The 500-subscriber tier: about 220. TikTok: about 8 times short on views, but about 33 million views to gain its 10,000 followers at our rate. No decision changes: every route stays hundreds of times short, and bet 1 comes first. Reviewed fresh; merged.

### Done
- **Product (a bet):** a second wording for the host's opening tag, naming the "Sounds…" sameness, was tried on both free models and scored blind against the earlier one. It reacted on 7 of 16 against 8, made no sense more often (5 against 1), and repeated other openers. Not kept. The earlier wording stays the one for the upload model, though it once took a side on the privacy post.
- **General management:** fewer than three items were ready, and both need the AI allowance. A fresh agent proposed eight; two more ranked them in opposite orders. The wording trial came first both ways. The two retention items came second and third both ways. The routes command came fourth and fifth, and was done because time remained. **Dropped:**
  - proposing to make the 883 old reading videos private now rather than with the rebrand: no new evidence since you tied the two together, and it spends your attention while every route is hundreds of times short.
  - counting replies to our automatic comment: 7 viewer comments in all, so the answer is already known.
  - YouTube's definition of a qualifying view: read last shift, and it changes no decision.

  A second round of six, from the functions not yet worked, put two quick legal reads top both ways. Neither changes a decision:
  - **Groq's terms** (June 2026) are written for businesses and ban training on what we send, so nothing blocks the planned move there.
  - **YouTube's AI-content label** covers realistic depictions of real people, events or scenes. A stock narrator reading text over stock footage is none of these, so it stays unset.

  Below the bar: Reddit's guidance that deleted posts and comments must stop showing. Ours stay in the videos, but your "not yet" on Reddit's terms already covers it. Also below: a weak-topic test (not due until bet 1's read), the name check (before the rebrand is due), and the content screen's one skip.

  With time left, the one ready item that could move tonight was the move to Groq, which waits on its host reactions: they come out as labels. A wording that rules out the label's shape (never an adjective and a noun) was tried the same way. Groq's main model reacted on 7 of 27 against 2, possibly chance, and labels were still most tags. Not kept: the move stays blocked on this.

  Mostly fixing; the two wording trials were bets.
- **Security:** the standing check is clean. No secrets are in the project, the only workflow change was the one you approved tonight, you remain the only collaborator, and the money controls are in place ($0.60 this month, forecast $0.81 of $3).
- AI use: no Gemini; 72 Groq requests (free).

### Blocked
- **For you, unchanged, in order:** #77 (nothing until a render is worth watching); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- After 07:00 UTC and away from uploads: the host's opening tag on the upload model, with the new wording against today's, three posts. Watch for repeated openings and for taking a side on politics.
- The 26 October weekly read is the first with the per-upload skip. Check how many uploads it marks as failed.

### Better?
- **Than last shift:** Slightly. Bet 1's verdict can no longer be misread at the opening, and the distance to revenue is measured rather than remembered. Nothing changed for viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, and bet 1, built 11 October, has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-20 (16:35) — A new wording made the host's opening tag react on the free models, from none of 17 to 9 of 16; a failed AI request now says whether the day's allowance is gone

    Worked (% of the shift): product 30 · reliability 25 · gm 15 · editorial 10 · engineering 5 · monetization 5 · legal 5 · security 5

**Summary:** The host's opening tag, which nearly every viewer sees, has come out as a title on every model tried. A new wording made it react on about half of the free models' tries, so tomorrow's few requests on the upload model can go straight to it. Separately, failed AI requests now say whether the day's allowance is spent, and that change is live. Nothing reached viewers.

### Toward revenue
- **A wording for the host's opening tag worth spending tomorrow's AI requests on.** On every model so far the opening tag came out as a title for the question ("Brutal truth"). I asked instead for "the words you would blurt out the moment a friend asked you this question". Both free models then reacted on 9 of 16 tries ("Ouch, right?", "Sounds shady"), against 0 of 17 with today's wording, scored blind in one mixed sheet; a second blind scorer agreed on 32 of the 33. The catch: one model opened most of them with "Sounds…", which is the sameness YouTube's spam policy names. The model uploads use has not tried it yet. The trial tool now runs it with one setting.
- **A better free model for the host's tags, if we must leave Gemini.** Moving every AI call to Groq would stop Reddit's text being used for training, which Reddit's terms forbid. But Groq's model turned the host's reactions into labels. Groq's other free model, on the same nine posts and scored blind, reacted to 10 of 24 answers against 4 of 27 ("Four hours?", "Sad face"). But none of its opening tags reacted with today's wording, and 2 of its 11 replies had no host lines at all. Neither model meets the bar, which the upload model nearly meets, so nothing switches.
- **An upload's lost title can now be explained.** When the AI refuses a request for being over its limit, the upload log and the release check now say which limit it hit. If it was the daily allowance, the next upload's title is at risk until the 07:00 UTC reset. If it was the per-minute limit, a short wait would have cleared it. Today's release check was refused on its fifth content-screen case, after this morning's trials. It was the first in eight days of checks, and nothing recorded which limit. Reviewed fresh, no defects; all tests pass; merged.

### Done
- **Editorial:** about 1 upload in 20 re-asks a question the channel already covered (4 of the last 60, such as "the scariest story you know is true"). Each was a different post with different answers. Exact repeats numbered 4 in 187, none since the 8 October guard. That is not enough to need a new guard before four a day.
- **General management:** a fresh agent proposed eight candidates, and two more ranked them in opposite orders. The repeat check led both and is done. The Groq model trial came second and third and is done; the opening-tag wording grew out of it. **Dropped:**
  - a pivot checkpoint: the quarterly planning already judges each bet against its set bar.
  - whether 7-day watch time predicts later views: third one way, seventh the other, and under 1% of views come from old videos.
  - the background clip and how many viewers stay: two weeks of data, split across many clips.
  - pricing Reddit's commercial data deal: you said not yet (#60).
  - why shifts end early: nothing records how much ready work each shift had.
  - a subscriber benchmark: it changes no decision.

  A second round of six, from the functions no recent shift has worked (distribution, finance, money, audience), put the same item first both ways. Four a day's rule said only to revert if "the 4-week view total falls". That names no comparison and contradicts your rule that views, which swing 27–50% on noise, never trigger a revert. Before any data, it now compares the first four full weeks with the four before, a fall being a finding, not a revert. Second both ways, for a later shift: one command printing each revenue route's distance.

  Mostly fixing; the two tag trials are bets.
- **Monetization:** YouTube's eligibility page counts "qualified Shorts views", never saying "engaged" as our plan assumes, and omits the 500-subscriber tier. Unconfirmed, but no decision changes: every route stays hundreds of times short.
- **Engineering:** the trial tool now takes the new wording and a choice of Groq model, on bet 1's branch. A fresh review found no defect in that, but it did find an older hole: a Groq trial run without Groq's key would quietly spend up to 18 of the day's 20 upload-model requests. It now refuses before any request. All tests pass, and the branch still merges cleanly.
- **Reliability (fixing):** if the AI's content screen ever replied without its verdict, or with a blank one, the post went through as checked, skipping even the keyword check. It now falls to the keyword check, which spends no request. Two reviews had left this open since 9 October. A fresh review found no defects, all tests pass, and it is merged.
- **Security:** the standing check is clean. No secrets are in the project, no workflows changed, you remain the only collaborator, and the money controls are in place ($0.60 this month, forecast $0.81 of $3).
- AI use: no Gemini (an upload was due); about 55 Groq requests (free).

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
