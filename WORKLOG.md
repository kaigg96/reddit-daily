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

## 2026-10-11 (16:39) — Bet 1's branch is up to date, so tonight's sample can be its last; titles get a backup AI, switched off

    Worked (% of the shift): product 35 · reliability 35 · data 10 · gm 10 · engineering 5 · security 5

**Summary:** Bet 1 (making the format ours) was behind the live code. That would have voided tonight's sample and cost at least another half-day, so it is now up to date, reviewed, and plays cleanly. Titles now have a backup AI for when Gemini fails, built switched off; it is also what lets four uploads a day fit Gemini's free allowance.

### Toward revenue
- **Yes, indirectly, on both bets.** Bet 1 is the step YouTube's payment rules need. A sample must name the exact version that ships, and the live code's last day of changes were missing from bet 1. Folding them in after tonight's sample would have voided it and pushed v8 back by at least 12 hours. That is done, so tonight's sample can be the final one. Bet 2 (four a day) had one open problem: on a bad day it would overspend Gemini's 20 free requests. Groq now covers both AI calls when Gemini runs out, so that problem goes away once the switch is on.

### Done
- **Product (bet 1):** merged the live code into bet 1's branch three times, ending with this shift's own changes, so it carries everything now live. Two small clashes, both resolved; two fresh reviews found no faults; all tests pass; a free local render plays (19.9 seconds, the host's lines capitalised on their dark band). Also fixed in advance how bet 1 will be judged: it skips medical threads, but those are only 1 to 2% of uploads, too few to move its result, so no allowance is made for them.
- **Reliability (a bet on reliability, built off):** when Gemini fails, the title request now gets one try on Groq before the upload falls back to the plain Reddit question, as the safety screen already does. One switch turns on both. Titles were lost on 2 of the last 30 uploads. A review found the daily release check would have judged Groq's answer as if it were Gemini's; that is fixed. Merged, switched off. A second piece is built and waiting: the upload log will name which AI wrote each title, so Groq's titles cannot blur the title experiments. It lands after bet 1, before the switch.
- **Data:** ran the safety screen's test cases on Groq a second time (free, no Gemini use). Same result as this morning: 6 of 7, and the same must-pass question skipped. So Groq is consistently stricter. That is fine as a backup, where a wrong skip costs one candidate post, but not yet as the main screen. Also checked whether Gemini's failures cluster by time of day, which would matter for the new slots at four a day: 4 failures in 42 runs, too few to say.
- **A mistake, and its fix:** I ran the screen's test script with a request for its help text. It ignores arguments, so it ran the whole test instead: about 5 Gemini requests from production's allowance, an hour before the evening upload. My estimate for today is about 13 of 20 requests used, leaving room for the evening upload's usual 2 and its worst case of 5. The script now refuses any argument before spending anything, with a test.
- **Security:** standing check clean: no secrets in the project, no unapproved workflow change, money controls in place, narration spend $0.33 this month (forecast $0.92 of $3).
- **General management:** process health is fine. Awkward this shift: every merge into the live code has to be folded into bet 1's branch before its sample, and that happened three times. Until the sample passes, the live code should take nothing but tracker edits.
- Fixing against improving: mostly improving (both bets). Two fixes: the release check's blind spot, and the test script's guard.

### Blocked
- **For you, each one label:** bet 1's sample (#74); four a day's schedule (#73). Still open: re-label #53 (comments); the account checks (#59).

### Next
- **Tonight (render slot from about 22:49):** request bet 1's sample on its current version, and add the new video to #74. Merge nothing but tracker edits into the live code until it passes.
- **12 October:** read `v7` under its rule, with the buried-upload check beside it. Check that the evening upload kept its title. If you approve bet 1 (#74), it ships as `v8` after that read.
- **After v8:** land the log column, then switch on Groq's backup for the screen and titles with a sample. It is a backup, so no version change: v8's two-week trial runs on undisturbed.

### Better?
- **Than last shift:** Yes, a little. Bet 1 can ship on tonight's sample without another half-day's wait, and four a day's last technical gap is closed, behind a switch.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat (12.0 seconds); both bets that would change it wait on you and on data.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-11 (10:55) — Bet 1's host is easier to read; its sample is with you as one label; four a day is built, switched off

    Worked (% of the shift): product 45 · engineering 20 · reliability 10 · data 10 · gm 10 · security 5

**Summary:** Bet 1's on-screen host now reads clearly on any background. Its sample rendered cleanly and is with you as one label (#74): you can judge it by watching, with nothing to run. Bet 2, four uploads a day, is built and switched off: it waits on one label from you for the schedule, then on the subreddit read about 2 November.

### Toward revenue
- **Yes, both bets moved.** Bet 1 (make the format ours) is the step YouTube's payment rules need. It is now one label from you, judged on a video you can watch. Bet 2 (four a day, the views lever) needs only your label on the schedule change, and the read it was always waiting for.

### Done
- **Product (bet 1):** the sample passed: a playable video on a real post, the host's setup, two reactions and the vote all present, our own words 67% of what the viewer gets. Its one flaw, lines in lower case, is fixed and reviewed. The host's yellow lines now sit on a see-through dark band. Before it, last night's free local render showed the lines readable on a busy, bright background, but not crisp. On orange, the band makes them plainly legible. A free local render played cleanly. A fresh review found no faults.
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
