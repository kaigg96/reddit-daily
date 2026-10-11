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

## 2026-10-11 (23:13) — Bet 1's final sample passed and is with you; the viewer-comments approval rested on a wrong fact, now corrected

    Worked (% of the shift): product 35 · engineering 15 · gm 15 · legal 15 · reliability 10 · audience 5 · security 5

**Summary:** Bet 1's final sample passed on the exact version that would ship. It is on #74: one label from you, then it ships as v8 after Monday's read. The viewer-comments change you approved (#53) said the project is private. It is public, and as built it would also have kept comments longer than YouTube allows, so a compliant replacement is with you.

### Toward revenue
- **Yes, on bet 1**, the step YouTube's payment rules need. Nothing technical stands between it and shipping: the sample played cleanly at 22.5 seconds, with our own words 55% of what the viewer gets. What remains is your label and Monday's read of the current version.
- **Indirectly, on audience.** Viewer comments are our only direct signal from viewers. The approved route would have broken YouTube's rules; the replacement does not.

### Done
- **Product (bet 1):** got the final sample on bet 1's current version: a real post, the host's setup and two reactions on screen, the vote at the end, no faults. Added it to #74 with what the AI wrote. One flaw: the vote is also posted as the channel's comment, and the AI writes it in lower case. Fixed as a separate change that lands right after v8, so the sample stays valid; a fresh review caught a bug in the fix, now fixed. Also settled before any v8 upload what it means if our own words fall under half on some upload: never a revert, but raising the share becomes bet 1's next step. Seven posts so far ran 51% to 67%, so a miss is plausible.
- **Legal and audience:** applied, #53 would have put viewers' comments in the public project history for good. YouTube's developer rules allow view counts and analytics to be kept indefinitely, but comment text for at most 30 days. I corrected #53 and asked you not to re-label it. Its replacement keeps each week's comments as a download GitHub deletes after 30 days, never saved in the project; I checked a shift can fetch one. Nothing was ever applied, so nothing needs undoing.
- **Engineering:** the upload log's "which AI wrote the title" column, needed before Groq's backup goes on, had no review on record. A fresh review found no faults; one comment fixed. Both follow-ups merge cleanly with bet 1 and today's live code, all tests passing, so they can land the same day as v8.
- **Reliability:** your four-a-day schedule is live and safe while switched off: the two extra runs exit without uploading and finish cleanly. GitHub starts our runs 3 to 7.4 hours late (median 4.75, 81 runs since 1 September), so at four a day uploads stay hours apart and Gemini's daily allowance still sees four.
- **General management:** the rule that asks reaching you are one label, closed within a day, hit its own review trigger: #53's re-label waited six days. Of the asks needing your hands (#50, #65, #59), #50 is the root: it turns #65 and every later rule change into one label. Its patch still applies cleanly tonight, all tests passing. Tracker kept true and within its word limits.
- **A mistake, and its fix:** while trimming the product plan I broke one item's status line, so a test failed and the ready count misread it, for about a minute on the live branch. My command had filtered the test output, so the failure did not stop the push. I now check for a failing test before pushing.
- **Security:** standing check clean: no secrets in the project, workflow permissions unchanged, money controls in place, narration $0.33 this month (forecast $0.92 of $3).
- Fixing against improving: about half each. Improving: bet 1's sample and its pre-commitment, the log column made ready. Fixing: the comment capitals, the comments approval, the tracker.

### Blocked
- **For you, in order of what each unblocks:** #50 (four commands, still current); #74 (bet 1, one label); #75, the comments replacement (one label, then close #53 unapplied); #65 (one label once #50 is in); the account checks (#59).

### Next
- **Morning shift (about 07:00):** the weekly review is due. Monday's snapshot lands about 11:00 to 13:00, so the `v7` read waits for the afternoon shift.
- **Afternoon shift:** read `v7` under its rule, with the other reads due on that snapshot. If #74 is labelled, merge bet 1 as `v8`, then the log column, then the comment fix. Then Groq's backup, with a sample.

### Better?
- **Than last shift:** Yes. Bet 1 is ready to ship on your label, and a compliance mistake was caught before it applied.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds; bet 1, the first change aimed at earning, has not shipped.
- **Than ~100 shifts ago:** Too early to say.

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
- **Security:** standing check clean: no secrets in the project, no unapproved workflow change, money controls in place, narration spend $0.33 this month (forecast $0.92 of $3). A fresh dependency audit found nothing new since 30 September.
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
