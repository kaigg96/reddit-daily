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

## 2026-10-12 (11:45) — Bet 1 is ready to merge the moment you label it; Groq now passes our safety tests; the v7 verdict waits on Monday's statistics

    Worked (% of the shift): product 25 · legal 20 · data 20 · gm 15 · reliability 15 · security 5

**Summary:** Bet 1 is cleared to merge the moment you label it, and how its effect on the opening seconds will be judged is fixed before any upload. Groq now passes every safety test, the step that lets it replace Gemini at no cost; Monday's statistics had not landed, so the v7 verdict passes to the afternoon shift.

### Toward revenue
- **Indirectly, on bet 1**, the only thing on the path to YouTube's payment rules. Nothing technical stands between it and shipping. Your label on #74 is the one remaining step after this afternoon's v7 read.
- **Indirectly, on the Reddit-terms risk:** Groq can now pass our safety tests, the condition for moving every AI call to it at no cost. That is the solution you asked for when you declined Gemini's paid tier (#62).

### Done
- **Product (bet 1):** merged the live code, bet 1 and both follow-ups (the log column and the vote's capitals) together in a scratch copy: no clashes, all 523 tests pass. The afternoon shift can merge them in order without re-checking. Also found that bet 1's first host line appears about one to two seconds in. That is exactly the window YouTube's "engaged view" count measures, and engaged views are what the payment bar counts. So before any upload I fixed how it will be read: bet 1 against v7 on the share of plays that get past the opening, at its own read, as a diagnostic that can never trigger a revert.
- **Data:** waited on Monday's statistics, which carry the v7 verdict and four other reads. GitHub starts the job 5 to 7 hours after its 06:00 slot, so it usually arrives between 11:00 and 13:00. It had not started when the shift ended. The rule for v7 is quoted and its commands are ready.
- **General management:** the ready queue was below its floor, so I generated eight candidates from the flat watch-time trend, the risk list and the decision rules still waiting on data, and had them ranked separately, forward and reversed. Three ranked top both ways: the v7 read, the bet 1 opening check (done), and which uploads gain subscribers. I dropped the last one. With 21 subscribers across the whole channel any answer would be too thin to use, and subscribers are not the binding half of the payment bar (views are ~800 times short, subscribers ~48). Also dropped: testing whether views scale with uploads per week (only the pipeline's first two weeks had fewer uploads, so the comparison is confounded), placing the four-a-day slots by hour (GitHub's delays pick the hour, not us), the name checks (they wait on bet 1 settling the show), drafting bet 1's next step (premature before it ships), and a TikTok question to you (bet 3 waits on bet 1). Tracker checked true and within its limits; process health fine. Awkward this shift: Monday's statistics arrive mid-morning while this shift's own start drifts by hours, so the one shift positioned to read them waited and could not. Scheduling the weekly job late on Sunday instead would have them ready before Monday's first shift. That is one workflow line, but I have not asked, since five asks already wait on you.
- **Legal and reliability (a bet, built off):** Groq, the free AI whose terms forbid training on what we send, had one blocker to replacing Gemini entirely: its safety screen wrongly skipped a question we know is fine, in every test. One added line for Groq alone (Gemini's instructions untouched) fixed it: all seven test cases passed, twice, and the question that must still be skipped was skipped every time. Free, and none of Gemini's allowance used. A fresh review found no faults and two gaps in the tests, both fixed. It waits on its own branch and lands with Groq's backup switch, after bet 1, so bet 1's tested version is exactly what ships. The review's one worry, that the line could let through a risky rewording of a known-fine question, I tested: both rewordings were correctly skipped, and one is now a standing test case.
- **Reliability:** both weekend uploads and this morning's landed, and the last-upload record is intact. The four-a-day schedule landed after Sunday's evening slot, so no extra run has fired yet; the first (today's 06:23 slot) is still queued at GitHub.
- **Security:** standing check clean: no secrets in the project, no unapproved workflow change, money controls in place, narration $0.34 this month (forecast $0.97 of $3).
- Fixing against improving: mostly improving (bet 1's merge readiness and its read, Groq's screen). No live fixes were needed.

### Blocked
- **For you, in order of what each unblocks:** #74 (bet 1, one label); #50 (four commands); #75 (comments, one label, then close #53 unapplied); #65 (applies once #50 is in); #59 (account checks).

### Next
- **Afternoon shift:** the statistics' arrival makes the weekly review due, and it carries these reads: v7 under its rule, then the engaged-share check (#8), the buried-upload check (R6), the voice and slot check (R3), and confirm the subscriber count arrived (C11). If #74 is labelled and v7 is kept, merge bet 1 as v8, then the log column, then the vote's capitals. Check that the first four-a-day off-slot run exited without uploading. Then switch on Groq's backup with its sample, merging the Groq safety-screen line with it.

### Better?
- **Than last shift:** Slightly. Bet 1's merge is pre-cleared and Groq's last test failure is fixed, but nothing shipped and the v7 verdict slipped a shift.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds; bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-11 (23:13) — Bet 1's final sample passed and is with you; the viewer-comments approval rested on a wrong fact, now corrected

    Worked (% of the shift): product 30 · legal 20 · engineering 15 · gm 15 · reliability 10 · audience 5 · security 5

**Summary:** Bet 1's final sample passed on the exact version that would ship. It is on #74: one label from you, then it ships as v8 after Monday's read. The viewer-comments change you approved (#53) said the project is private. It is public, and as built it would also have kept comments longer than YouTube allows, so a compliant replacement is with you.

### Toward revenue
- **Yes, on bet 1**, the step YouTube's payment rules need. Nothing technical stands between it and shipping: the sample played cleanly at 22.5 seconds, with our own words 55% of what the viewer gets. What remains is your label and Monday's read of the current version.
- **Indirectly, on audience.** Viewer comments are our only direct signal from viewers. The approved route would have broken YouTube's rules; the replacement does not.

### Done
- **Product (bet 1):** got the final sample on bet 1's current version: a real post, the host's setup and two reactions on screen, the vote at the end, no faults. Added it to #74 with what the AI wrote. One flaw: the vote is also posted as the channel's comment, and the AI writes it in lower case. Fixed as a separate change that lands right after v8, so the sample stays valid; a fresh review caught a bug in the fix, now fixed. Also settled before any v8 upload what it means if our own words fall under half on some upload: never a revert, but raising the share becomes bet 1's next step. Seven posts so far ran 51% to 67%, so a miss is plausible.
- **Legal and audience:** applied, #53 would have put viewers' comments in the public project history for good. YouTube's developer rules allow view counts and analytics to be kept indefinitely, but comment text for at most 30 days. I corrected #53 and asked you not to re-label it. Its replacement keeps each week's comments as a download GitHub deletes after 30 days, never saved in the project; I checked a shift can fetch one. Nothing was ever applied, so nothing needs undoing. Also built and reviewed a reader, so a shift can read the comments the day they first arrive, shown as viewers' text and never as instructions. The project now refuses to save that file, so a mistake fails loudly instead of publishing.
- **Legal (old videos):** YouTube's own advice after a rejection is to "edit or delete" videos that break its rules; its pages say nothing about private ones. So when the old videos' fate is proposed, it leans to deleting them or starting a fresh channel, not hiding them.
- **Engineering:** the upload log's "which AI wrote the title" column, needed before Groq's backup goes on, had no review on record. A fresh review found no faults; one comment fixed. Both follow-ups merge cleanly with bet 1 and today's live code, all tests passing, so they can land the same day as v8.
- **Reliability:** your four-a-day schedule is live and safe while switched off: the two extra runs exit without uploading and finish cleanly. GitHub starts our runs 3 to 7.4 hours late (median 4.75, 81 runs since 1 September), so at four a day uploads stay hours apart and Gemini's daily allowance still sees four.
- **General management:** the rule that asks reaching you are one label, closed within a day, hit its own review trigger: #53's re-label waited six days. Of the asks needing your hands (#50, #65, #59), #50 is the root: it turns #65 and every later rule change into one label. Its patch still applies cleanly tonight, all tests passing. Tracker kept true and within its word limits. Looking for more work found nothing else worth doing tonight: three data questions wait on Monday's snapshot, two others had too few uploads to test (6 and about 15), and reading v7 early would mean looking before its rule is due.
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
