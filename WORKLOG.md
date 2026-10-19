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

## 2026-10-19 (18:25) — Weekly review: watch time still flat at 12 seconds; the first read of viewer comments found almost none; a data gap in the weekly job is closed

    Worked (% of the shift): data 30 · engineering 20 · audience 15 · gm 15 · product 10 · reliability 5 · security 5

**Summary:** The weekly review found the channel flat on watch time, and nothing in it moves the company toward revenue until bet 1 ships on your label on #77. It closed one question, fixed a gap that lost a third of this week's retention readings, and parked the comment-reply work, since viewers barely comment.

### Toward revenue
- Nothing directly: both ready items wait on #77. What this shift did keeps bet 1's readings complete: the weekly job now retries when YouTube's servers fail. Without that, one failure loses a week of "where viewers leave" readings for good, and bet 1's check of its notes depends on them. The comparison it needs already has the 8 earlier videos it needs.

### Done
- **Product:** watch time is flat at 12.0 seconds for a sixth week. Typical views at 7 days rose from about 49 to 139 over three weeks, but four-week totals are unchanged (×0.93), so fewer videos are buried while the hits are no bigger. No experiment's rule has come due: the subreddit test has 9 and 8 of its 15 a side, and the title-style test 13 and 5 of its 15 and 8.
- **Data:** dark-morbid topics' lead did not hold. At 12 videos it reads 8% ahead, inside what chance produces, so the idea of ranking posts by topic stays parked. The new retention readings arrived for every recent video with views, except 23 older ones lost to one server error.
- **Engineering (fixing):** that server error now gets two retries before the job gives up, and the comment download no longer counts our own closing-question comments as viewers' (15 of its 22). Reviewed fresh with no defects found; all tests pass; merged.
- **Audience:** the first read of viewer comments: 7 in a week, all on one political video (US support for Israel), mostly heated and one abusive. No other video drew a comment. Building automatic replies would post nothing worth posting, so that work is parked until comments appear on three or more videos in a week.
- **Distribution:** 95% of views still come from the Shorts feed and 2% from search, unchanged.
- **Reliability and security:** every upload this week landed; one (18 October) went out with the raw question as its title, as reported. Today's afternoon upload had not started by 17:40, which is late but inside the 9-hour delays seen before. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.52 this month, forecast $0.82 of $3).
- This shift was fixing (the data gap) and reviewing; nothing new reached viewers.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: merge it as the next version, close #74, update the trackers.
- 26 October weekly review: if #77 is still open, one comment on it naming 1 November and the four-week cost; check the retention readings came through without gaps and the comment count no longer includes ours.
- 5 November monthly review: as listed in the previous entry.

### Better?
- **Than last shift:** No change toward revenue; the measurement bet 1 relies on is more robust.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-19 (09:50) — Bet 1's final version passed its sample, so your label on #77 is now a release within minutes; a missed date for bet 2 is fixed

    Worked (% of the shift): gm 40 · product 15 · reliability 15 · strategy 10 · security 10 · data 10

**Summary:** Nothing reached viewers. Bet 1's exact merged version passed its sample this morning, so your label on #77 releases it within minutes, with no further check to wait for. The plan also now says what a late label costs bet 2, and what four uploads a day would need if it goes first.

### Toward revenue
- **Bet 1 can ship the moment you label #77.** The version that would go live (three answers, the host's notes, and last night's backup for AI outages) passes all 615 tests and still merges cleanly. Its sample, the last check a merge needed, was requested at the first minute the once-every-12-hours limit allowed and passed: 18 seconds, the host's setup and all three reactions on screen. As on earlier samples, the free model that writes samples ran the host's closing vote past its length limit, so the usual closing line played instead.
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
- Today's weekly snapshot, expected early afternoon, brings the 19 October weekly review. It covers the first week's viewer comments, the dark-morbid question, the watched clip's rule, and whether the five new retention columns fill.
- On #77's label: merge it as the next version, close #74, update the trackers.
- 26 October weekly review: if #77 is still open, one comment on it naming 1 November and the four-week cost.
- 5 November monthly review: reopen long-form if bet 1 is kept?; let a release inside an approved bet that passes every check ship unless you object within a set time; YouTube's originality rules (reach, the voice correction, the paid-channel read); TikTok with its follower caveat; the subscription's price against $34–340 a month; the weekly allowance's dark days; a failed release check going to the next shift before you. Bet 2's window moved to 26 October.
- Once #77 settles: the bundled ask (#50 with the re-raise fix).

### Better?
- **Than last shift:** Slightly: bet 1's last check passed, and a deadline that would have passed unseen is now watched.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds, and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.
