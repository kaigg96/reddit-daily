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

## 2026-10-19 (09:50) — Bet 1's final version is being sampled, so your label on #77 becomes a release within minutes; a missed date for bet 2 is fixed

    Worked (% of the shift): gm 40 · product 15 · reliability 15 · strategy 10 · security 10 · data 10

**Summary:** Nothing reached viewers. Bet 1's exact merged version is being sampled, its one sample of the day. On a pass, your label on #77 releases it without another twelve-hour wait. The plan also now says what a late label costs bet 2, and what four uploads a day would need if it goes first.

### Toward revenue
- **Bet 1 can ship the moment you label #77.** The version that would go live (three answers, the host's notes, and last night's backup for AI outages) passes all 615 tests and still merges cleanly. The sample was the last check a merge needed. I requested it at the first minute the once-every-12-hours limit allowed.
- **What a late label costs is now written down.** If #77 is still unlabelled when the subreddit test reads (about 2 November), four uploads a day goes first, as the plan already implied. A later bet 1 then waits about four weeks for that read. So a label by about 1 November keeps both bets on time. The check for this had been set for the 5 November review, after the date it protects. It now falls to the 26 October weekly review, which will tell you on #77 if the label is still missing.
- **Four a day going first would have hit a gap.** Two things it relies on are currently part of bet 1: the backup AI for days when Google's allowance runs short, and a record of which slot each upload belongs to. Both are now listed as steps to take first in that case.

### Done
- **Reliability:** GitHub is moving its standard machines to a newer Ubuntu between today and 19 November. I checked our upload job against it: it needs nothing from the system that changes, so I expect no effect. If an upload fails in that window, the note says to suspect this first, and the fix is a one-line change for you.
- **Data:** style C titles (numbered lists) look 18% behind on watch time, inside the 18.2% gap chance alone produces; read within long and short videos, 8% behind and level. Not a finding; it changes nothing.
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.52 this month, forecast $0.82 of $3). This morning's upload landed with its AI title. The record of the last upload is intact. Nothing more of the account-security check (#59) is visible to a shift: GitHub refuses it the deploy keys and webhooks.
- **General management:** two rounds of eight fresh candidates, each ranked twice in opposite orders. Round one: the bet 2 date led both passes, done; style C's gap came next, done. Round two: the Ubuntu check ranked high both ways, done; the gap for four a day first led one pass, done. **Settled in a line:** four a day's narration cost (about $1.64 a month against the $3 cap, so it fits); the extra plain readings four a day would add before bet 1 (about 56 on top of roughly 1,100, no change). **Considered and dropped:** pre-committing what today's first retention curve decides (retention is never a trigger, and the queue after bet 1 is set); a risk row for slow replies (the decisions log already tracks it); a check that the content screen is not too lenient (uploads are not buried more than usual, and today's weekly review audits the screen); a trademark check on the working name (renaming waits on bet 1); Snapchat's payments and a Partner Program checklist (neither changes a decision before bet 1); wording four a day's view-total clause and a noise-floor requirement (both ranked low, and neither binds before 2 November); this week's usage pace (each shift is already gated on it).
- This shift was mostly fixing: the date, the gap and the sample. The Ubuntu check was prevention.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- Read the sample's verdict. On a pass naming the branch's current commit, bet 1 needs only #77's label.
- Today's weekly snapshot, expected early afternoon, brings the 19 October weekly review. It covers the first week's viewer comments, the dark-morbid question, the watched clip's rule, and whether the five new retention columns fill.
- On #77's label: merge it as the next version, close #74, update the trackers.
- 26 October weekly review: if #77 is still open, one comment on it naming 1 November and the four-week cost.
- 5 November monthly review: reopen long-form if bet 1 is kept?; let a release inside an approved bet that passes every check ship unless you object within a set time; YouTube's originality rules (reach, the voice correction, the paid-channel read); TikTok with its follower caveat; the subscription's price against $34–340 a month; the weekly allowance's dark days; a failed release check going to the next shift before you. Bet 2's window moved to 26 October.
- Once #77 settles: the bundled ask (#50 with the re-raise fix).

### Better?
- **Than last shift:** Slightly: the last check a merge needed is under way, and a deadline that would have passed unseen is now watched.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-18 (22:25) — This afternoon's upload lost its AI title to an outage; the backup that would have saved it is now live, and bet 1 is pre-merged with it

    Worked (% of the shift): reliability 35 · engineering 25 · gm 20 · legal 10 · data 5 · security 5

**Summary:** This afternoon's upload went out with the raw Reddit question as its title, because Google's AI was overloaded twice in a row. From the next upload on, a second Google model answers when that happens. Nothing new reached viewers: bet 1 still waits on your label on #77, and its merge now also needs one sample video, which a shift can request without you.

### Toward revenue
- **Fewer uploads lose their title, keywords and closing line.** The 16:02 upload was the third since 1 October to ship the raw question as its title, each time because the AI was overloaded. A second model, the content screen's backup since 9 October (it answered the one time it was needed), now writes them when the first fails. Under bet 1 this matters more: the same request writes the host's lines, so an outage would ship a plain reading inside the bet's own sample. Reviewed fresh: no defects, and its five smaller findings are fixed. The sample video passed, and all tests pass. No spending: it uses Google's free allowance, one extra request and only when the first model fails.

### Done
- **Reliability (fixing):** the backup above. The daily release check skips it, so the check cannot be passed by the wrong model or spend a request on it.
- **Engineering (fixing):** both versions of bet 1 (three answers, or two if you choose that on #74) rewrite the same code, so I merged each with tonight's change and tested it (615 and 611 tests pass). Either now merges into the live code without conflicts. The three-answer one is now what the daily release check tests, and it will re-test it tomorrow by itself.
- **Data:** in the last 60 uploads, five AI requests failed on overload, never two in one run, which is why a second model is a good bet. The evidence is thin: the screen's backup has been needed once, and it answered.
- **Legal (improving):** the terms of every service whose output is in our videos allow paid use, as far as their own pages say: the narration (Amazon's voice service: "your output belongs to you"), the AI text (Google claims no ownership and does not bar the free tier from paid use; Groq leaves its outputs ours), and the stock clips (commercial use allowed). Pexels forbids showing identifiable people in a bad light; all six live clips are abstract, so a new clip with people needs that check against dark topics. Reddit's terms remain the only bar to paid use, as recorded. Quoted and dated beside the asset licences, for the check before any application. The backup above is Google's too, under the same terms, and is sent only what the first model was just sent.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.51 this month, forecast $0.83 of $3). Both uploads today landed; the record of the last upload is intact.
- **General management:** two rounds of candidates, each ranked in two passes in opposite orders. In the first, the overload backup led both passes and is done; pre-merging the two-answer version and pointing the release check at the merged one came out of it. In the second (eight from a fresh agent), the paid-use terms check led both passes and is done. Drafting the 5 November rule on releases inside an approved bet came second (that review will draft it), and the backup's worst daily use of its model came third (about 17 requests, and it fails soft). Also dropped from that round: a reading for YouTube's reach change (it would change no decision); a story-mode experiment after bet 1 (the queue after bet 1 is set); a test fix already queued after bet 1; a dependency scan (known findings recorded the day before). A late video run at 20:54 was the switched-off third slot, as designed. **Considered and dropped:** whether raw-title uploads underperform (3 uploads, too few to read); marking backup-written titles in the title tests (rare, and both arms are assigned by coin, not by model); weekly review prep (no decision waits on it); a further check of paid channels (YouTube still refuses their transcripts to a server). No experiment's rule has come due: the title test has 4 of its 15 needed uploads at a week old. **Awkward this shift:** any live fix that touches code a waiting release also changes forces a re-merge, which voids that release's sample, and one sample per 12 hours then holds the new one until morning. That cost is small while #77 is unanswered, but it grows with every day bet 1 waits. Handed over about 25 minutes early: both ready items wait on #77, and two rounds of sixteen candidates left nothing above the bar.
- This shift was mostly fixing; the terms check was the one improving step, and bet 1 waits on #77.

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
