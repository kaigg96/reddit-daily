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

## 2026-10-21 (16:31) — Your bet 1 ask had drifted from the build and now says one thing; its render is checked on your Python; a long first answer costs no watch time

    Worked (% of the shift): gm 45 · data 25 · product 10 · reliability 5 · market 5 · audience 5 · security 5

**Summary:** Nothing reached viewers. The one ask that unblocks revenue (#77) now matches the version you would render and asks one thing, and its render command is checked on your machine's Python. A data read found no reason to read the shortest answer first.

### Toward revenue
- **#77 says one thing again.** Its opening text still described the 17 October version (sentence notes, old pictures) and said a label alone ships it, while this morning's comment asked you to render first. Rewritten, with no email: render once with the command inside, then label it if a first-time viewer follows the video. This is the second time an ask has drifted; the lasting fix waits on #50.
- **The render should run on your machine.** It runs Python 3.10, which broke a render once. On the release branch as it stands, all 656 tests pass under 3.10, and a fixed-post render plays (1080×1920, 28 seconds).
- Nothing else moved toward revenue: every other step waits on that render or on uploads accumulating.

### Done
- **Data (a bet):** does a long first answer lose viewers before the halfway point, where most leave? Answer lengths for 176 uploads were recovered from the run records, and the rule was fixed before reading. No link (35 uploads; noise), so reading the shortest answer first is not worth trying. Reviewed fresh; merged.
- **General management (the audit, due after ten shifts):** the ten shifts since 17 October ran 2–56 of 60 minutes. Nothing reached viewers; ten changes merged, all measurement or reliability; bet 1's craft moved on your 19 October feedback. Otherwise the process works: reviews caught real defects, and the daily release check passed. Three fixes. The stale #77 above. The decisions record still said you were absent (you answered #81 the day it opened), and that had seeded a "ship unless you object" idea. And the list of past ideas showed only dropped ones, not finished ones, so the idea generator re-proposed bet 2's start date, worked out twice already. It now shows both (reviewed fresh; merged).
- **General management (ranking):** nothing was ready, so a fresh agent proposed eight and two more ranked ten in opposite orders. Top both ways: bet 2's start date, already done. Answered on the spot: shock phrases in titles (one borderline, "will surprise you", in about 22 titles since the ban); GitHub's server change (still on the old image today, and nothing found depending on it, so no ask). **Audience:** the viewer-reply item's reopen rule now says "weekly": 17 comments sit on 6 of the last 60 uploads, but a week's read shows only 1 or 2. **Dropped:** shipping bet 1 unless you object by a date (you asked to watch first, and it is already queued for the 5 November review); real narration on test renders (it changes how keys are handled, so for that review, not an ask beside #77); clip-by-clip reach (the standing check holds). **Market:** Groq now offers a free, expressive voice (Orpheus), but it gives no word timings for captions and takes 200 characters a request, and a voice change is yours. A second round of five, for distribution, finance and monetization (no time in ten shifts), found nothing above the bar. The keywords and the automatic comment come from one shared AI request, so dropping either frees nothing, and neither varies enough to compare: the comment posted on all 86 uploads that record it. Break-even needs the subscription's price, still unrecorded. Reddit publishes no price for its data. And posting days decide nothing, since four a day means every day. So the shift hands over about 25 minutes early. Mostly fixing; the first-answer read was a bet.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes since this morning, you remain the only collaborator, and the money controls are in place ($0.62 this month, forecast $0.86 of $3). The content screen's weekly audit: 4 skips since late August, none since 12 September.
- AI use: no Gemini (an upload was within the hour); one free model list from Groq.

### Blocked
- **For you, in order:** #77 (one narrated render, command inside, then one label); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- Read tomorrow's daily release check. If you render bet 1 and label #77, it ships after that check.
- 26 October weekly read: the first with the per-upload skip. Check how many uploads it marks as failed, then run the opening-reach read once.
- 5 November monthly review: real narration on test renders, which would take your hands off bet 1's path; the Orpheus note with it.

### Better?
- **Than last shift:** Slightly. The ask that unblocks revenue reads one way, and its command is known to run on your machine. Nothing changed for viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds, bet 1 (built 11 October) has not shipped, and ten shifts merged only measurement and reliability.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-21 (09:20) — The host's opening tag can no longer show a title; bet 1 is ready for your narrated render

    Worked (% of the shift): product 40 · gm 15 · strategy 15 · engineering 10 · data 10 · security 5 · reliability 5

**Summary:** Bet 1's opening tag, the host line nearly every viewer sees, came back a title on every model and wording. It now shows only when it reads as a reaction, so bet 1 is ready for the one narrated render you asked for before deciding. Separately, posting more was priced at its ceiling and cannot reach revenue alone. Nothing reached viewers yet.

### Toward revenue
- **Bet 1 is one step from your decision.** You asked shifts to get the tags to your bar, then bring a narrated render back. The opening tag was the part no wording fixed. It now appears only when it exclaims or opens on a sound ("Oh, THIS question.", "Hmm, tricky"). Otherwise it is left out. A fresh reviewer scored 40 new opening tags blind, from three models and two wordings: every one let through was a reaction, and every title was left out. The cost: the opening tag will appear on only about one video in six to eight. The rest of the host is unchanged, and the upload model's reactions react on about 14 of 18 answers by eye. The command for the render is on #77.
- **Posting more is not a revenue plan.** Even at the most we could post as things stand, every YouTube route stays at least 70 times short (Strategy, below). That keeps bet 1's per-video change first.

### Done
- **Product (a bet):** the planned test of the "blurt" wording for the opening tag, on the upload model, six posts (6 of today's 8 allowed AI requests). It reacted on 3 of 6 against 2 of 6 for today's wording, and repeated "Tricky question". Not kept: no wording has fixed the opening tag on any model, so the fix is a check in code instead.
- **Engineering:** the check, reviewed by a fresh agent. No bugs; its four fixes are in (curly quotes, stretched sounds like "Ohhh", a test that tested the wrong thing). Merged into the release branch, so tomorrow's daily release check prints it on the upload model. The trial tool now prints each opening tag as written, and whether it would show.
- **Strategy:** how far posting more could take us. The Polly budget as you set it ($3 a month) caps us near 6 uploads a day, three times today's volume. Gemini's daily allowance caps us near 4 unless the AI calls move to Groq. Even at 6 a day, and even if views grew fully with volume, the Partner Program stays about 240 times short and the 500-subscriber tier about 70 times. No current plan changes. For the 5 November review: a second step up in volume is not a revenue plan.
- **General management:** only one or two items were ready, so a fresh agent proposed eight and two more ranked them in opposite orders. The volume ceiling came first both ways (done above). Second and third: a count of what repeats across our last 60 uploads, against YouTube's spam policy. No title opening repeats more than 4 times and six background clips rotate, so the one music track, your task already, stays the only gap. Also second or third: whether pay at the Partner Program's bar covers our costs. Dropped: the subscription's price isn't recorded, and every route is hundreds of times away. Fourth both ways, whether the opening decides reach, now has its read built, reviewed and merged, with its rule fixed before any number. The review caught that reading ages vary from 4 to 10 days, so an age guard was added before anything was read. Read today: 19 uploads, one short of the 20 needed, so it reads again on Sunday's figures. **Dropped:** a published norm for the engaged share (5th both ways), a reach-cut signature for Sunday's figures, an opinion-question test, and moving only the content screen to Groq (needs a sample render and a review). Also checked, for the move to Groq: Groq's third and last chat model labels too (about 3 of 24 reactions react), and the opening-tag check applied to reactions would drop half the good ones on the upload model. So the move is now marked blocked: none of Groq's models writes the host's tags to your bar.

  With nothing ready after that, a second round of five came from the functions the first barely touched. Two were answered on the spot. **Security:** no upload of ours has ever left public. The 18 private videos are the same in every snapshot that records it, and all but one predate July. **Reliability:** failure rates by release cannot be compared, because those columns began during the current release. Dropped: posting hour (tangled with the subreddit test, since each day's two uploads split the subreddits), spacing between uploads (read from a retention figure that leaves out everyone who swipes away), and weeks to the Partner Program (flat, so never).

  Mostly improving: the opening-tag check and the volume read were bets on what ships and on the plan. The trial-tool fix was a repair.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes since last night, you remain the only collaborator, and the money controls are in place ($0.62 this month, forecast $0.86 of $3).
- AI use: 6 Gemini requests (upload model); about 90 Groq requests (free).

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
