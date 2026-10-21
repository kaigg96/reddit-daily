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

## 2026-10-21 (22:45) — Reddit is closing the free access every video starts from: please register our app before 31 October; free access ends by March 2027

    Worked (% of the shift): legal 30 · strategy 25 · gm 20 · market 10 · data 5 · reliability 5 · security 5

**Summary:** Looking for new work turned up a Reddit announcement of 30 September. New requests close on 31 October, apps not registered lose access from 12 January, and free access ends by March 2027. Every video we make starts from that access, so this is now the company's largest risk. You have one new ask (#82), and shifts are pricing other sources for the 5 November review.

### Toward revenue
- **Our supply now has an end date.** I read two reports of Reddit's announcement first-hand (TechCrunch, and a fuller one quoting Reddit's developer posts). New access requests close on 31 October. Apps not registered lose access from 12 January. Free access ends by March 2027; after that Reddit wants "commercial deals", reported at around $12,000 a month, which is out of reach for us. Nothing in the project had recorded it, three weeks on. Bet 1's host carries over to any source; the readings do not.
- **#82 asks you to register our app before 31 October,** and to ask Reddit whether a small registered app keeps access after March. Registering is free and needs your Reddit account; Reddit may already have emailed it a reminder. It is quicker than #77 and has a date, so it comes first. Reddit's replacement platform runs no Python and is built for apps inside Reddit, so it cannot carry our source.
- **Pricing the alternatives is now ready work,** to bring you a proposal at the 5 November review. First reads are under Done.

### Done
- **Legal and market (a bet):** what could replace Reddit. Stack Exchange's terms allow our use, free. The condition: each video credits and links every author and carries the same open licence. It could supply two a day: 13 of 21 live questions on its workplace site have three or more answers. But those answers run 100 to 360 words against our 12. Its licence lets us shorten them, which Reddit's never did. The free AI model cut six to about 14 words each, accurate but dry advice, and both questions were too long for our titles. So it would be a different show, not a replacement. Writing our own questions and having AI write the answers costs no licence. But on two of our questions it wrote stock jokes and invented a personal story, so those answers could only be presented as the host's own. Hacker News and Mastodon do not allow this use. Also noted: Reddit's rules reportedly now bar apps from showing posts their authors deleted, which our published videos cannot honour. No other service we depend on has a shutdown date; Google keeps the older model our titles use only for regular users, which we are. Bet 1's host needs three short, distinct answers to react to: shortened Stack Exchange answers give that, while AI-written ones would have the host reacting to itself.
- **Strategy:** the risk register now carries the new risk, rated fatal. The Reddit-terms row also said Groq's no-training tier lands with bet 1; it lands only as a backup (the full move is blocked on its tags), now corrected.
- **General management (ranking):** nothing was ready. A fresh agent proposed eight ideas, drawn from the data, the risk register and the list of past ideas. Two more agents ranked them, in opposite orders, and agreed on the top three. First: whether Reddit grants commercial agreements to small creators at all. That search turned up the dates above. Second: writing down, before bet 1's results, the numbers that would put a change of direction on your agenda. The end of free access now forces that question by March, so it was overtaken. Third: checking that the 26 October read will run. It will: the step that has never run on real data works on today's figures. **Dropped:** the break-even point (it needs the subscription's price); old duplicate uploads (most share a question, not a video); asking you to change the shift schedule (short shifts are ours to fix); whether views are bunching into a few hits (four-week totals read ×0.93, noise); a comment-hold setting (one abusive comment).
- **Data and reliability:** the scorecard's jump in median views is noise, since four-week totals fell (×0.93). The zero-view recent uploads are the usual reporting lag: every week since July shows 3 to 5. The watched background clip stays under its retirement bar. Bet 1's branch, merged with today's main, passes 694 tests. A run that loses Reddit access fails loudly rather than skipping an upload silently.
- **Security:** the standing check is clean. No secrets are in the project, no workflow has changed since this afternoon, you remain the only collaborator, and the money controls are in place.
- Neither a fix nor a change to what ships: a risk found, and the plan changed with it. AI use: no Gemini, no narration; four free Groq requests.
- **Process:** a change fatal to our supply sat public for three weeks while ten shifts looked for work. The monthly review's outside look should cover the source's developer news. For the 5 November review. Also awkward: waiting on helper agents takes timed pauses, because the tool that watches for them is refused here.

### Blocked
- **For you, in order:** #82 (register our Reddit app, before 31 October); #77 (one narrated render, then one label); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- Continue pricing sources for the 5 November proposal (ready). Left: Reddit's answer on access after March if you register, and the proposal itself. The 26 October read of whether the opening decides reach also bears on it: if the question carries a video, the source of answers matters less.
- If #82 is still open on 28 October, raise it once more with the same key (a comment emails you): after the 31st, registering may need a new request Reddit no longer accepts.
- 26 October weekly read: check how many uploads it marks as failed, then run the opening-reach read once.
- 5 November monthly review: the source proposal, and narration on test renders.

### Better?
- **Than last shift:** Yes, in what we know: the company now sees that its supply ends by March 2027, with ten days to be safe on registering. Nothing changed for viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. The plan is truer: it now carries a dated, fatal risk it had missed.
- **Than ~100 shifts ago:** Too early to say.

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
