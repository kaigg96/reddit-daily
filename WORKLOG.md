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

## 2026-10-12 (20:18) — Weekly review: the opening change is kept, but its gain is longer posts, not the change; Groq's backup is built and waits behind bet 1

    Worked (% of the shift): data 40 · reliability 20 · product 15 · engineering 10 · gm 10 · security 5

**Summary:** The current format's verdict came due: it is kept, but the gain came from Reddit's posts running longer, and it did not raise the share of plays YouTube counts toward payment. That clears the last gate before bet 1 except your label (#74), and Groq's free backup is now built on top of bet 1, ready to follow it.

### Toward revenue
- **Indirectly, on bet 1.** Its read now waits for its full 20 uploads (the automatic Monday read would have answered at 8) and shows whether near-silent uploads drive the result; they doubled v7's gain.
- **Indirectly, on the Reddit-terms risk:** Groq's backup, which keeps our posts out of Google's training at no cost, is one merge plus a sample after bet 1.

### Done
- **Data (the v7 rule, quoted):** "keep if median watch-seconds holds or improves; revert only if it drops by more than the detection limit … Credit it to `v7` only if it holds within a length half beyond drift." **Kept:** +20% (12.0 against 10.0 seconds, 24 uploads). **Not credited:** its videos ran 3 seconds longer, and within longer videos it reads +8%, inside the 13% normal drift. Leaving out uploads under 10 views, it reads +9%: same verdict, half the size.
- **Data (reads that waited on this snapshot):** the share of plays past the opening, which the payment bar counts, did not rise with v7 (0.34 against 0.36), so the opening change did not move it. v7 does not bury more uploads beyond chance. The narrator-voice gap has reversed and faded, so no one-voice test. The subscriber count now arrives each week (21), closing that item. Standing checks pass: no background clip is burying uploads beyond chance (the one being watched, 4 of 17), and the safety screen has skipped no post since 12 September. Nor does the question's length (0.32 against 0.31); topics are too thin.
- **Product:** watch time still flat at 12.0 seconds for six weeks. The scorecard reads worse on share watched because videos ran 2.9 seconds longer with no more watching, which that check exists to catch. Bet 1's rule now also states it is read on AskReddit posts alone while the subreddit test runs, as its spec already said.
- **Distribution:** 95% of views still come from the Shorts feed. Views gained per day halved last week (617 to 306) after the best week on record; within the usual range and all from recent uploads, so weather unless next week repeats it. Bet 2: the last four weeks earned 9,158 views at 7 days against the 8,300 baseline; the bar is 16,600.
- **Audience:** viewer comments are not collected yet; that waits on #75.
- **Reliability:** 14 of 15 slots landed this week; the 5 October evening one was lost to GitHub's outage, recorded at the time. One title fell back when Gemini failed. The first four-a-day off-slot run exited without uploading, as designed, but started 9.4 hours late, beyond the 7.4 hours seen before. This evening's upload had still not started at 20:42.
- **Reliability (Groq):** built the backup switch on its own branch over bet 1 and its follow-ups; all merge cleanly. Switching it on exposed a test leak (a key in the shell sent six tests to Groq), now fixed. A fresh review found no bugs and two risks. On a day Gemini's allowance is spent, Groq's per-minute limit could have cost the title and bet 1's host lines: fixed with one short wait, itself reviewed. And Groq had never written bet 1's host lines: I ran the release checks on Groq alone, free and without touching Gemini, and its setup, both reactions and all eight safety cases passed.
- **Data (engineering):** the release check now reads bet 1 at its committed 20 uploads, and prints the read without near-silent uploads beside its verdict, never as a trigger. A fresh review found no bugs and one real risk: the extra line could have shown bet 1's result before its 20 uploads, which the commitment exists to prevent. Fixed, with three smaller points, and live.
- **Security:** no secrets in the project, no workflow change since this morning, money controls clean ($0.36 this month, forecast $0.97 of $3). Dependency check: the same 34 known advisories (image library 33, login library 1), nothing new since 30 September; exposure stays low, as recorded.
- **General management:** ready queue below its floor, so I generated eight candidates from the flat trend, the engaged share, traffic and the risk list, ranked separately forward and reversed. Both orders agreed on the top four, all done above. Dropped both ways: asking you to let Groq go before bet 1 (another ask for no time saved) and which uploads gain subscribers (23 gains, too thin). Also dropped: changing the scorecard's length check, which works as intended. Tracker checked true. Awkward this shift: the shift rules say a shift cannot read the video job's logs, so to learn why a run failed it should spend its one sample run. It can read them: I read today's off-slot run directly and saw it exit as designed. The rule change is yours to approve; I left it for the next audit rather than add a sixth ask. Handed over about 30 minutes early: nothing else cleared the bar. Merging a second chance figure beside bet 1's verdict would invite a misread, and the rest were small test and tool tidy-ups no decision waits on.
- Fixing against improving: mostly measurement (the review, the release check's fix); improving: Groq's switch built.

### Blocked
- **For you, in order of what each unblocks:** #74 (bet 1, one label: v7's read is done, so nothing else stands in the way); #50 (four commands); #75 (comments, one label, then close #53 unapplied); #65 (applies once #50 is in); #59 (account checks).

### Next
- **On #74's label:** merge bet 1 as `v8`, then the log column, then the vote's capitals; then request a sample of Groq's switch branch (rebased on that `main`) and merge it on a PASS.
- Check this evening's upload landed, and that the late off-slot runs keep exiting.
- Next weekly review (19 October): whether the views halving repeats.

### Better?
- **Than last shift:** Slightly. The v7 verdict is in and bet 1's read is protected from two mistakes, but nothing shipped to viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds; bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

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

