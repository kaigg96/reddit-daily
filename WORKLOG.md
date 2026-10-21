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

## 2026-10-21 (09:20) — The host's opening tag can no longer show a title; bet 1 is ready for your narrated render

    Worked (% of the shift): product 40 · gm 15 · strategy 15 · engineering 10 · data 10 · security 5 · reliability 5

**Summary:** Bet 1's opening tag, the host line nearly every viewer sees, came back a title on every model and wording. It now shows only when it reads as a reaction, so bet 1 is ready for the one narrated render you asked for before deciding. Separately, posting more was priced at its ceiling and cannot reach revenue alone. Nothing reached viewers yet.

### Toward revenue
- **Bet 1 is one step from your decision.** You asked shifts to get the tags to your bar, then bring a narrated render back. The opening tag was the part no wording fixed. It now appears only when it exclaims or opens on a sound ("Oh, THIS question.", "Hmm, tricky"). Otherwise it is left out. A fresh reviewer scored 40 new opening tags blind, from three models and two wordings: every one let through was a reaction, and every title was left out. The cost: the opening tag will appear on only about one video in six to eight. The rest of the host is unchanged, and the upload model's reactions react on about 14 of 18 answers by eye. The command for the render is on #77.
- **Posting more is not a revenue plan.** Even at the most we could post as things stand, every YouTube route stays at least 70 times short (Strategy, below). That keeps bet 1's per-video change first.

### Done
- **Product (a bet):** the planned test of the "blurt" wording for the opening tag, on the upload model, six posts (6 of today's 8 allowed AI requests). It reacted on 3 of 6 against 2 of 6 for today's wording, and repeated "Tricky question". Not kept: no wording has fixed the opening tag on any model, so the fix is a check in code instead.
- **Engineering:** the check, reviewed by a fresh agent. No bugs; its four fixes are in (curly quotes, stretched sounds like "Ohhh", a test that tested the wrong thing). Merged into the release branch, so tomorrow's daily release check prints it on the upload model. The trial tool now prints each opening tag as written, and whether it would show.
- **Strategy:** how far posting more could take us. The Polly budget as you set it ($3 a month) caps us near 6 uploads a day, three times today's volume. Gemini's daily allowance caps us near 4 unless the AI calls move to Groq. Even at 6 a day, and even if views grew fully with volume, the Partner Program stays about 240 times short and the 500-subscriber tier about 70 times. So posting more cannot reach revenue alone; the gap is in each video. No current plan changes. For the 5 November review: a second step up in volume is not a revenue plan.
- **General management:** only one or two items were ready, so a fresh agent proposed eight and two more ranked them in opposite orders. The volume ceiling came first both ways (done above). Second and third: a count of what repeats across our last 60 uploads, against YouTube's spam policy. No title opening repeats more than 4 times and six background clips rotate, so the one music track, your task already, stays the only gap. Also second or third: whether pay at the Partner Program's bar covers our costs. Dropped: the subscription's price isn't recorded, and every route is hundreds of times away. Fourth both ways, whether the opening decides reach, now has its read built, reviewed and merged, with its rule fixed before any number. The review caught that reading ages vary from 4 to 10 days, so an age guard was added before anything was read. Read today: 19 uploads, one short of the 20 needed, so it reads again on Sunday's figures. **Dropped:** a published norm for the engaged share (5th both ways), a reach-cut signature for Sunday's figures, an opinion-question test, and moving only the content screen to Groq (needs a sample render and a review). Also checked, for the move to Groq: Groq's third and last chat model labels too (about 3 of 24 reactions react), and the opening-tag check applied to reactions would drop half the good ones on the upload model. So the move is now marked blocked: none of Groq's models writes the host's tags to your bar.

  Mostly improving: the opening-tag check and the volume read were bets on what ships and on the plan. The trial-tool fix was a repair.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes since last night, you remain the only collaborator, and the money controls are in place ($0.62 this month, forecast $0.86 of $3).
- AI use: 6 Gemini requests (upload model); about 90 Groq requests (free; some repeated after two runs collided).

### Blocked
- **The move to Groq** (the Reddit-terms risk): none of Groq's three chat models writes tags to the bar. It waits on a new model there.
- **For you, in order:** #77 (one narrated render, command inside; best away from the 05:00 and 17:00–18:30 UTC uploads); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- Nothing is ready: generate and rank new work first.
- Read tomorrow's daily release check: its opening-tag line now says whether one was left out.
- If you render bet 1 and it passes your test, the label on #77 ships it after its daily check.
- The 26 October weekly read is the first with the per-upload skip. Check how many uploads it marks as failed, then run the opening-reach read once (`--opening-reach`).

### Better?
- **Than last shift:** Slightly. The one part of bet 1 no wording could fix is now held in code, and bet 1 is in front of you. We also know volume alone cannot get us there. Nothing changed for viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, and bet 1, built 11 October, has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-20 (22:18) — Bet 1's planned check of where viewers leave would have missed the opening, and is fixed before any data; the distance to revenue is now computed, and had drifted

    Worked (% of the shift): data 30 · product 25 · gm 15 · monetization 15 · legal 5 · reliability 5 · security 5

**Summary:** Nothing reached viewers: the step that would needs AI requests that tomorrow morning's upload shares. Instead, bet 1 will now be judged on the right viewers, and the plan's distance to revenue is computed from our data (the Partner Program is about 720 times short, not 760–880).

### Toward revenue
- **Nothing directly.** The upload-model trial waits for the 07:00 UTC reset.
- **Bet 1 will be judged on the right viewers.** Its pre-set rule reads where viewers leave from YouTube's retention figures, and would blame the host's opening tag if the 25% mark fell. Those figures leave out everyone who swipes away. On all 29 recent uploads, as many viewers or more are counted at 10% in as started the video, though only 20–58% of their plays count as real views. So a weak opening would never show there. That shows in the share of plays that become real views, which we track; the rule now says so, before any of bet 1's uploads exist.
- **One failed request no longer loses a week of that data.** On 19 October a single server error, a third of the way through the weekly read, cost the 23 uploads after it their retention figures. Each upload gets only one reading at a week old. Retries were added that day; now an error that outlasts them costs only its own upload. Reviewed fresh (one missing test, added); merged.
- **Each revenue route's distance is now one command, and the plan's figures were stale.** Partner Program: about 720 times short on views and 48 on subscribers. New applicants from February: about 1,450. The 500-subscriber tier: about 220. TikTok: about 8 times short on views, but about 33 million views to gain its 10,000 followers at our rate. No decision changes: every route stays hundreds of times short, and bet 1 comes first. Reviewed fresh; merged.

### Done
- **Product (a bet):** a second wording for the host's opening tag, naming the "Sounds…" sameness, was tried on both free models and scored blind against the earlier one. It reacted on 7 of 16 against 8, made no sense more often (5 against 1), and repeated other openers. Not kept. The earlier wording stays the one for the upload model, though it once took a side on the privacy post.
- **General management:** fewer than three items were ready, and both need the AI allowance. A fresh agent proposed eight; two more ranked them, in opposite orders. The wording trial came first both ways. The two retention items came second and third both ways. The routes command, fourth and fifth, was done as time remained. **Dropped:**
  - making the 883 old reading videos private now, not with the rebrand: no new evidence, and it spends your attention.
  - replies to our automatic comment: 7 viewer comments in all.
  - YouTube's qualifying-view definition: read last shift.

  A second round of six, from the functions not yet worked, put two quick legal reads top both ways. Neither changes a decision:
  - **Groq's terms** (June 2026) are written for businesses and ban training on what we send, so nothing blocks the planned move there.
  - **YouTube's AI-content label** covers realistic depictions of real people, events or scenes. A stock narrator reading text over stock footage is none of these, so it stays unset.

  Below the bar: Reddit's guidance that deleted posts and comments must stop showing. Ours stay in the videos, but your "not yet" on Reddit's terms already covers it. Also below: a weak-topic test (not due until bet 1's read), the name check (before the rebrand is due), and the content screen's one skip.

  With time left, the one ready item that could move tonight was the move to Groq, which waits on its host reactions: they come out as labels. A wording that rules out the label's shape (never an adjective and a noun) was tried the same way. Groq's main model reacted on 7 of 27 against 2, possibly chance, and labels were still most tags. Not kept: the move stays blocked on this.

  A third round found nothing to finish in the last 15 minutes that would change a decision. The three running title and subreddit tests are not yet due, and the open code-health items need you or a render.

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
