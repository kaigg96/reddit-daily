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

## 2026-10-18 (08:50) — Bet 1 still waits on your label; two reads change what the 5 November review weighs: long-form is the nearest YouTube route on paper, and yesterday's "no voice requirement" was wrong

    Worked (% of the shift): strategy 25 · legal 25 · gm 20 · engineering 15 · reliability 10 · security 5

**Summary:** Nothing reached viewers; bet 1 still waits on your label on #77, and nothing of yours has moved for 79 hours, your longest gap yet. Two policy reads moved the plan instead: YouTube's long-form route is nearer on paper than any Shorts route, and I correct something yesterday's report told you about voice.

### Toward revenue
- **A correction to yesterday's report.** It said YouTube's monetization page sets no voice requirement. That page itself lists "mostly non-verbal reactions … without added voice commentary" as content that cannot earn. Bet 1's host writes its reactions, which is not non-verbal but is not voiced, so the wording does not settle it. My recommendation on #77 is unchanged: it is the only step toward pay we have, and a voice was your call (#71). The same page lets reused content earn where the creator "explains how the creator added to the content", and its reviewers read the channel and video descriptions: a cheap step once bet 1 ships.
- **Long-form is the nearest YouTube route on paper.** The Partner Program also admits 1,000 subscribers with long-form watch hours: 8,000 a year for channels applying from February. Shorts hours never count, and we have none. At 1.5 to 5 minutes watched that is about 100,000 to 320,000 long-form views a year, against about 81 million Shorts views. So views stop being the gap (about 800 times short) and subscribers become it (about 48 times short). Either bar pays little: about $34–340 a month for Shorts, and roughly the same for long-form on industry estimates. It changes nothing before bet 1, because the reading rule applies to the whole channel. Long-form has been out of scope since July; reopening it is yours, for 5 November.
- **No AI label is needed, and bet 1's host already meets the AI-persona rule.** YouTube asks for disclosure only of AI content that "seems realistic", and AI-written scripts and titles are exempt. A newer rule refuses pay to AI personas that give advice on health, law, money or politics; the host's instructions already forbid exactly those four.

### Done
- **Strategy and legal (improving):** the three reads above, from YouTube's own pages (fetched and checked today), recorded in the plan and product findings.
- **General management (improving):** eight fresh candidates, ranked in two passes in opposite orders. The four that ranked well both ways are done above or below. Dropped: titles against the advertiser rules (5 of the last 23 touch politics, religion or a nationality, but ad rules limit pay only once we are paid); what a reviewer sees first (the old-videos item already covers all 1,041 readings); a second reopening rule for the parked topic ranker (not due for about 40 days); making the scorecard's length check length-aware (bet 1's own read already compares like with like).
- **Engineering (fixing):** the defect behind #77's mixed message is fixed on a branch: a re-raise that changes an ask can now rewrite the issue's opening text, never on an approved issue. The same patch pins the weekly snapshot's libraries. It is a workflow change, so it waits for one ask after #77 settles; a fresh review is on the branch.
- **Reliability:** bet 1 merged onto today's live code passes all 605 tests, and today's title-capitals change does not touch bet 1's AI request, so the merge plan stands. Tomorrow's first retention snapshot: its job loads cleanly with the libraries it installs. The daily release check, set for 08:17, has started between 12:10 and 17:51 on all of the last 8 days, so a morning shift cannot read it.
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.48 this month, forecast $0.82 of $3).
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.
- This shift was mostly improving (three reads), with one fix (the ask defect).

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- 18 October, afternoon: read today's release check, which lands around 12:00–18:00. On a pass, close #78; with #77 labelled, merge bet 1 as the next version and close #74, #77 and #78.
- 19 October weekly review: first week's viewer comments; the dark-morbid question; the watched clip's rule; check the five new retention columns fill.
- Once #77 settles: raise the re-raise fix with #50 as one ask, then merge its branch.
- 5 November monthly review: reopen long-form after bet 1 keeps?; a release inside an approved bet that passes every check could ship unless you object within a set time; YouTube's originality rules (reach, and today's correction); bet 2's window (a label on #77 by about 1 November still covers all four of its weeks); TikTok with its follower caveat; the subscription's price against the $34–340 a month above; the weekly allowance's dark days; a failed release check going to the next shift before you.

### Better?
- **Than last shift:** Slightly, in knowledge rather than product: a wrong statement about voice is corrected before you decide on #77, and a nearer route is priced. Nothing reached viewers.
- **Than ~10 shifts ago:** No: watch time is flat at 12.0 seconds and bet 1, built 11 October, is unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-17 (22:08) — Bet 1's ask could be read two ways; it now says one thing, and the audit finds the company waiting on that one label, not on work

    Worked (% of the shift): gm 40 · data 20 · reliability 15 · product 10 · legal 10 · security 5

**Summary:** Nothing reached viewers; bet 1 still waits on your label on #77, whose opening text could be read two ways and now says one thing. The backup AI and its no-training terms check out for bet 1's launch, and where viewers leave each video can now be collected without a change from you.

### Toward revenue
- **The one decision that gates revenue is now asked one way.** #77's opening text, which you read first, still said a label there approved a rebuild and your label on #74 would ship it. A later comment said one label on #77 ships it. A label on that text could have meant either. It now says plainly: one label ships bet 1 once its morning check passes, and closes #74 for you. #74 still showed its old two-answer sample; it now says at the top, and in its title, that it is superseded and that a label there chooses two answers. Neither edit sent you an email.
- **The backup AI holds bet 1's notes.** When Gemini's daily allowance runs out, which happens more at four uploads a day, a backup AI writes the host's notes. In 12 free test calls on six posts it returned the right shape every time, with three notes. One vote ran long and would fall back to the usual closing line. So the four-a-day plan can lean on it as planned.
- **Legal:** the backup's agreement still bars it from training on what we send (it applies to free use too, last changed 22 June). The reason for moving our AI calls there stands.

### Done
- **General management (audit, fixing):** 8 shifts since the last audit. Two changes reached viewers (title fixes). Bet 1, built 11 October, is unshipped, and every shift's "better?" said slightly or no. Your one decision in that time was #75; everything that would reach viewers waits on #77, so more shift work cannot stand in for that label. #77's mixed message came from how re-raised asks work: they add a comment and leave the opening text stale. Proposed for later, bundled with #50 so #77 stays the one ask: a re-raise updates the opening text.
- **General management (improving):** shifts kept re-proposing ideas already dropped (four were dropped twice), because this log keeps only about two entries. A shift can now list what the last ten shifts dropped, and why. Reviewed fresh and merged.
- **Data (improving):** where viewers leave each video, the best-ranked idea for flat watch time, had waited on a workflow change only you can make. It does not need one: the weekly job can add it to the file it already saves. Now live, reviewed twice: from Monday's snapshot it records the share still watching at five points in each recent upload, the report can read it, and a failure costs only those columns. It went in before Monday, not after, so today's version has a week of readings to compare bet 1 against.
- **Product:** how bet 1 will read the new retention points is written down before any exist: the same cut as its "share watched" rule, never a trigger, and the first point that falls more than 5 points names where viewers leave (a quarter in: the setup note; half and three quarters in: the notes on the answers). Two ranked checks were already answered. Bet 1's pre-committed rule already counts a vote that falls back. And three answers cannot push a video past the 45-second limit: today's version reads three too, and its longest of 45 uploads ran 31.5 s.
- **Data:** every pending experiment's pre-committed read still runs on today's tools (results not looked at, so nothing was peeked).
- **Considered and dropped:** a wider backup-AI check of the content screen (it needs Reddit access, and the current check passes 7 of 7 twice); questions addressed to a profession ("Nurses, …"; 5 in 168 uploads, too few to test); logging repaired AI replies (waits on bet 1's merge). Ranked in two passes, opposite orders. Also below the bar at the end: a survey of comparable channels (dropped once already: ads show on unpaid channels too, so it cannot tell who is paid); a re-raise that rewrites the ask itself (a workflow change, so it waits for the bundle after #50); two code-health items whose closing conditions have not arrived. Handed over about 20 minutes early: both remaining ready items wait on #77. This shift was mostly fixing, with two improvements (the dropped list, retention).
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.48 this month, forecast $0.82 of $3).
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- 18 October: read the 08:17 release check. On a pass with #77 labelled, merge bet 1 as the next version, close #74, #77 and #78, and update the trackers.
- 19 October: the weekly review; first week's viewer comments; the dark-morbid question; the watched clip's rule. Check that snapshot carries the five new retention columns, filled or with a reason.
- 5 November monthly review: as listed in the entry below (retention curves now need nothing from you), plus re-raises that update an ask's opening text.

### Better?
- **Than last shift:** Slightly, in the ask rather than the product: the decision that gates revenue can no longer be read two ways. Nothing reached viewers.
- **Than ~10 shifts ago:** No, on the audit's evidence: two title fixes in 8 shifts, watch time flat at 12.0 seconds, bet 1 unshipped since 11 October.
- **Than ~100 shifts ago:** Too early to say.
