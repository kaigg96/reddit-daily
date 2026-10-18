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

## 2026-10-18 (22:25) — This afternoon's upload lost its AI title to an outage; the backup that would have saved it is now live, and bet 1 is pre-merged with it

    Worked (% of the shift): reliability 40 · engineering 30 · gm 20 · data 5 · security 5

**Summary:** This afternoon's upload went out with the raw Reddit question as its title, because Google's AI was overloaded twice in a row. From the next upload on, a second Google model answers when that happens. Nothing new reached viewers: bet 1 still waits on your label on #77, and its merge now also needs one sample video, which a shift can request without you.

### Toward revenue
- **Fewer uploads lose their title, keywords and closing line.** The 16:02 upload was the third since 1 October to ship the raw question as its title, each time because the AI was overloaded. A second model, the content screen's backup since 9 October (it answered the one time it was needed), now writes them when the first fails. Under bet 1 this matters more: the same request writes the host's lines, so an outage would ship a plain reading inside the bet's own sample. Reviewed fresh: no defects, and its five smaller findings are fixed. The sample video passed, and all tests pass. No spending: it uses Google's free allowance, one extra request and only when the first model fails.

### Done
- **Reliability (fixing):** the backup above. The daily release check skips it, so the check cannot be passed by the wrong model or spend a request on it.
- **Engineering (fixing):** both versions of bet 1 (three answers, or two if you choose that on #74) rewrite the same code, so I merged each with tonight's change and tested it (615 and 611 tests pass). Either now merges into the live code without conflicts. The three-answer one is now what the daily release check tests, and it will re-test it tomorrow by itself.
- **Data:** in the last 60 uploads, five AI requests failed on overload, never two in one run, which is why a second model is a good bet. The evidence is thin: the screen's backup has been needed once, and it answered.
- **Legal:** the backup is Google's too, under the same terms, and is sent only what the first model was just sent. Nothing goes anywhere new.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.51 this month, forecast $0.83 of $3). Both uploads today landed; the record of the last upload is intact.
- **General management:** ranked fresh candidates in two passes, opposite orders. The overload backup led both and is done; pre-merging the two-answer version and pointing the release check at the merged one came out of it. **Considered and dropped:** whether raw-title uploads underperform (3 uploads, too few to read); marking backup-written titles in the title tests (rare, and both arms are assigned by coin, not by model); weekly review prep (no decision waits on it); a further check of paid channels (YouTube still refuses their transcripts to a server). No experiment's rule has come due: the title test has 4 of its 15 needed uploads at a week old.
- This shift was all fixing; the only improving step, bet 1, waits on #77.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- From 09:42 UTC (one sample per 12 hours), and not within an hour of an upload: request a sample of bet 1's merged version. With it and tomorrow's release check passing, your label on #77 becomes a merge within minutes.
- On #77's label: merge it as the next version, close #74, update the trackers.
- 19 October weekly review: the first week's viewer comments; the dark-morbid question; the watched clip's rule; check that the five new retention columns fill.
- 5 November monthly review: reopen long-form if bet 1 is kept?; let a release inside an approved bet that passes every check ship unless you object within a set time; YouTube's originality rules (reach, the voice correction, the paid-channel read); bet 2's window (a label on #77 by about 1 November still covers all four of its weeks); TikTok with its follower caveat; the subscription's price against $34–340 a month; the weekly allowance's dark days; a failed release check going to the next shift before you.
- Once #77 settles: the bundled ask (#50 with the re-raise fix).

### Better?
- **Than last shift:** Slightly: one cause of degraded uploads is closed, and bet 1 is protected from it. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds; bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-18 (14:35) — Bet 1's last check passed, so it is now only your label on #77; a first look at paid channels in our genre finds only spoken commentary

    Worked (% of the shift): gm 35 · reliability 20 · market 20 · data 10 · editorial 5 · security 5 · legal 5

**Summary:** Nothing reached viewers. Bet 1's final automatic check passed today and it still fits cleanly onto the live code, so your label on #77, now waiting about 86 hours, becomes a release within one shift. Nothing else this shift generated was worth doing ahead of it.

### Toward revenue
- **Bet 1 has no technical blocker left.** Today's release check passed on the fixed version: every field came back with all three host notes, and the content screen sorted all five test posts as expected. Merged onto today's live code, it passes all 607 tests. #78 is closed. The pass holds a week; after that the check re-runs by itself.
- **Market (first read):** among about 185 channels in our genre found by search, 11 show a members button, which only paid channels can have. Every one of those whose format could be confirmed adds a spoken human voice, reading or reacting; none with text-only commentary like bet 1's turned up. A missing button proves nothing, so this cannot tell whether text-only commentary gets paid; it leans weakly toward voice. It changes nothing before bet 1 (still the only step toward pay, and a voice was your call, #71), but it belongs with the originality item on 5 November.

### Done
- **Reliability (fixing):** the merge check above. The late-starting release check cannot starve the afternoon upload: in 12 days they never ran within three hours of each other, and a day's AI requests fit the cap even if they met.
- **Editorial and legal:** the ban on shock phrases in titles holds: none of the 17 titles since it went live uses one.
- **Data:** bet 2 looks ahead on paper: the last complete week drew 4,334 views at a week old, about the weekly pace its quarter-end target needs (16,600 over four weeks). One week sits inside the channel's normal 27–50% swing, so it changes nothing yet.
- **General management:** eight fresh candidates, ranked twice in opposite orders, then the sources the first round missed. Done: the title check, the merge check, the market read. Closed the superseded 5 October digest issue. Handed over about 45 minutes early: both ready items wait on #77, and nothing else cleared the bar. A follow-up on the closest paid channel could not settle whether its commentary is spoken: YouTube refuses its transcripts to a server. That is the fourth shift running to stop early for this one reason; the 5 November item on releases inside an approved bet is its only fix.
- **Considered and dropped:** a way for a shift to start the release check (first one way, fifth the other; it needs a new once-a-day guard on the AI allowance and your hands after #77); public-domain music for variety (it changes the video, so it waits about a month for bet 1's read, and YouTube's own library, your task, is safer against copyright claims); a reviewer-facing description (already recorded for after bet 1); bet 2's progress in the plan (the review reads it live); a long-form compilation (priced this morning, and a compilation of readings is still a reading); pre-writing the next bundled ask (waits on #77); the spread by topic and subreddit (nothing beyond the two open research questions); traffic (unchanged, 96% from the Shorts feed).
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.51 this month, forecast $0.83 of $3). This morning's upload landed and the record of the last upload is intact.
- This shift was mostly checking and record-keeping; the market read was the one new step.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: merge bet 1 as the next version, close #74, update the trackers.
- 19 October weekly review: as listed in the entry below.
- Once #77 settles: the bundled ask (#50 with the re-raise fix).
- 5 November monthly review: as listed below, with the market read above beside the originality item.

### Better?
- **Than last shift:** No change in substance: bet 1's last check passed, as expected, so only your label remains. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time flat at 12.0 seconds; bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.
