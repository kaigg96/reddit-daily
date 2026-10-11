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

## 2026-10-11 (10:55) — Bet 1's host is easier to read; its sample is with you as one label; four a day is built, switched off

    Worked (% of the shift): product 45 · engineering 20 · reliability 10 · data 10 · gm 10 · security 5

**Summary:** Bet 1's on-screen host now reads clearly on any background. Its sample rendered cleanly and is with you as one label (#74): you can judge it by watching, with nothing to run. Bet 2, four uploads a day, is built and switched off: it waits on one label from you for the schedule, then on the subreddit read about 2 November.

### Toward revenue
- **Yes, both bets moved.** Bet 1 (make the format ours) is the step YouTube's payment rules need. It is now one label from you, judged on a video you can watch. Bet 2 (four a day, the views lever) needs only your label on the schedule change, and the read it was always waiting for.

### Done
- **Product (bet 1):** the sample passed: a playable video on a real post, the host's setup, two reactions and the vote all present, our own words 67% of what the viewer gets. Its one flaw, lines in lower case, is fixed and reviewed. The host's yellow lines now sit on a see-through dark band. The last sample's lines read on a busy, bright background, but not crisply. On orange, the band makes them plainly legible. A free local render played cleanly. A fresh review found no faults.
- **Product (bet 2):** built four a day behind a switch that still says two. GitHub starts our runs 4 to 5 hours late, so a run cannot tell four slots apart by the clock. Each run now learns its slot from the schedule line that started it. Today's two runs pick exactly as before, checked hour by hour. At four, no subreddit would run more than twice in a row, and the late-night run keeps its own day's title style. The two new schedule lines are a workflow change a shift cannot make, so they went to you as a patch (#73). The code went to the live branch first, so the extra runs stop at once if the patch lands.
- **Data:** checked whether four a day fits the AI's 20 free requests a day. On 93 runs it does: about 2 requests a run, so about 8 a day, 16 with the daily release check. The worst case, 5 a run, does not fit, so the extra runs will need a lower cap or Groq before the switch goes to four. Also asked whether political posts, the last three uploads, do worse: only 4 are old enough to read, so the tool refused, and that is the answer for now. And how often the title request fails, which would make a bet 1 upload a plain reading: 2 of the last 30, none of the last 10. That is too rare to justify a second AI route for titles yet.
- **Reliability:** when Gemini fails and the Groq fallback (still off) also misses, the upload log now says so, and why. Before, only the console showed it. Reviewed and merged. The weekly digest's lateness figure measured to the nearest scheduled time, so it read a 6.6-hour delay as 5.4 hours, and at four a day would have read today's delays as about 1. It now counts forward from the run's own scheduled time. Reviewed and merged; what is left of it for four a day is recorded.
- **General management:** the sealed music is confirmed working: this morning's upload, the first after the seal, logged its track. That item is closed. Two things made this shift awkward. The one-render-per-12-hours limit meant bet 1's sample could only be asked for in the last quarter-hour, because last night's shift rendered at 22:46. And the daily release check, set for 08:17, has started between 14:27 and 17:07 on each of its last six runs, so a morning shift never sees that day's verdict. The handover had expected it by morning.
- **Security:** standing check clean. Narration spend $0.32 this month (forecast $0.92 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: mostly improving. Both bets moved; two small fixes (the screen's log, the digest's lateness).

### Blocked
- **For you, each one label:** bet 1's sample (#74); four a day's schedule (#73). Still open from before: re-label #53 (comments; its change still applies to today's file, so the label is all it needs); the account checks (#59).

### Next
- **Tonight (render slot from about 22:49):** sample bet 1 again. The AI wrote its lines in lower case; that is fixed and reviewed on the branch, and a merge needs a pass on the current version.
- **12 October:** read `v7` under its rule, with the buried-upload check beside it. If you approve bet 1 (#74), it ships as `v8` after that read.
- **Groq:** switch the safety screen's fallback on with a sample, in the render slot after bet 1's second one. The screen fell to the keyword filter on 2 of the last 30 uploads; those are what it would cover.
- **Four a day, before the switch:** cap the extra runs' AI use or send them to Groq; raise how many posts a run fetches.

### Better?
- **Than last shift:** Yes. Bet 1's next step reached you as one label with a video to watch, and bet 2 went from approved to built.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds), but both bets meant to change what we ship and how far it reaches now wait only on you and on data.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-11 (00:30) — Shifts ended early because work waited on you; fixed by us. Your three replies are now acted on

    Worked (% of the shift): gm 25 · product 30 · engineering 20 · strategy 10 · distribution 5 · legal 5 · security 5

**Summary:** You told us on #67 to find why shifts end early and fix it ourselves. We did. Work waited on you, and shifts missed replies you had already given: three of your comments (the host, the Groq key, Reddit) sat unread for up to a day. Shifts now see your comments. Asked as one label, bet 2 was approved in 11 minutes (#72). Bet 1's voiced host will not ship, as you asked; its text-only successor is built.

### Toward revenue
- **Not yet, but the queue is honest again.** Your verdict on the host settles the step queued for Monday. Bet 1 (make the format ours) still stands, and its next step is built: one voice, no extra audio spend. Facebook, like YouTube and TikTok, pays nothing for narrated readings, so bet 1 comes first whichever platform earns.

### Done
- **General management (a fix, #67):** found the cause in the record. Every ask you could answer with a label closed, most within a day (12 of 12). Asks needing a session, commands, a login or a listen waited for days, and shifts stopped once all their work waited on those. Worse, the list a shift reads at the start showed only labels and closes, so it missed your comments. The alarm no longer emails you. Each shift now starts with the rows waiting on you and a rule: do every part a shift can, so what reaches you is one label. Your comments now reach the shift. Both changes had fresh reviews, and every fault they found is fixed.
- **Product:** acted on your three replies. The voiced host is recorded as rejected. Bet 1's next step is built behind a switch: the host's setup and reactions as text on screen while the answers are read, and the narrator speaking the vote as today's closing line. One voice, no host audio. A free local sample rendered cleanly, with our own words at 54% of what the viewer gets. Groq: tonight's checks on it passed for titles, but its safety screen skipped one test post Gemini passes, so we are not switching yet. Gemini was overloaded on 3 of the last 5 uploads, so Gemini first, with Groq when it fails, is the shape: that fallback for the safety screen is built, reviewed and merged switched off. Reddit: recorded that we ask before applying to any programme, not now.
- **Strategy:** bet 2 went to you as one label (#72), including four a day's narration spend, and you approved it 11 minutes later. With bets 1 and 2 set by label, the quarter's planning is recorded as held, with no session, and #55 is closed. Bet 3's pilot comes back as its own label once bet 1's next step keeps.
- **Distribution:** Meta's own pages answered what the plan said needed your logged-in read. Facebook's programme is invite-only, paid per 1,000 qualified views. It demonetises accounts that mostly narrate what is on screen.
- **Reliability:** two upload runs could overlap and both pick one post. The fix came with #72 and is live. The daily release check was about to spend up to 8 of production's 20 daily AI requests on the rejected release; it now checks the live code.
- **Legal:** you sealed the music; closed #66. Next upload is the first on the sealed file.
- **General management:** closed 11 old weekly digests so your open issues are only the ones needing you. Code-health passes no longer wait on you (the company's rules give them to Engineering). Three rows that said they waited on you did not; corrected.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: mostly fixing. The improvement is how work reaches you.

### Blocked
- **For you, each one action:** re-label #53 (comments); the account checks (#59). #50 and #65 need your hands: Claude Code protects the skills folder by design, and only a looser mode for the whole shift would open it, which is not worth it.

### Next
- **After tonight's upload:** check its log names the music track, not "none".
- **Bet 1's next step:** the text-only host is built, reviewed (its findings fixed) and switched on in its release. Tomorrow's 08:17 release check reads its lines on the AI that uploads use. Then request its sample after 10:46 (one render per 12 hours) and bring it to you as one label. Since the host is silent, you can judge it from the sample link, with nothing to run.
- **12 October:** read `v7` under its rule, with the buried-upload check beside it.
- **Groq:** the safety screen's Groq fallback is merged, switched off; it would have checked the two uploads this month that fell to the keyword filter. Close its two small logging gaps, then switch it on with a sample, after bet 1's (one render slot).
- **Four a day (approved):** build it switched off, for the subreddit read about 2 November.

### Better?
- **Than last shift:** Yes. Three of your answers had sat unread, and shifts were still waiting on you for them. Now they are acted on, and the cause is fixed in code.
- **Than ~10 shifts ago:** Unclear. Watch time is flat (12.0 seconds), and the first originality step is back to a first sample. But the queue now holds work that changes what we ship.
- **Than ~100 shifts ago:** Too early to say.
