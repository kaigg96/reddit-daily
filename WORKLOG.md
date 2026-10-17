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

## 2026-10-17 (22:20) — Bet 1's ask could be read two ways; it now says one thing, and the audit finds your attention, not the work, is the limit

    Worked (% of the shift): gm 40 · data 20 · reliability 15 · product 10 · legal 10 · security 5

**Summary:** Nothing reached viewers; bet 1 still waits on #77. Its opening text said your label only approved a rebuild, while its title and latest comment said one label ships it. It now says one thing, and the backup AI and its no-training terms both check out for bet 1's launch.

### Toward revenue
- **The one decision that gates revenue is now asked one way.** #77's opening text, which you read first, still said a label there approved a rebuild and your label on #74 would ship it. A later comment said one label on #77 ships it. A label on that text could have meant either. It now says plainly: one label ships bet 1 once its morning check passes, and closes #74 for you. #74 still showed its old two-answer sample; it now says at the top, and in its title, that it is superseded and that a label there chooses two answers. Neither edit sent you an email.
- **The backup AI holds bet 1's notes.** When Gemini's daily allowance runs out, which happens more at four uploads a day, a backup AI writes the host's notes. In 12 free test calls on six posts it returned the right shape every time, with three notes. One vote ran long and would fall back to the usual closing line. So the four-a-day plan can lean on it as planned.
- **Legal:** the backup's agreement still bars it from training on what we send (it applies to free use too, last changed 22 June). The reason for moving our AI calls there stands.

### Done
- **General management (audit, fixing):** 8 shifts since the last audit. Two changes reached viewers (title fixes). Bet 1, built 11 October, is unshipped, and every shift's "better?" said slightly or no. You acted once in that time, so the limit is your attention, not the work. #77's mixed message came from how re-raised asks work: they add a comment and leave the opening text stale. Proposed for later, bundled with #50 so #77 stays the one ask: a re-raise updates the opening text.
- **General management (improving):** shifts kept re-proposing ideas already dropped (four were dropped twice), because this log keeps only about two entries. A shift can now list what the last ten shifts dropped, and why. Reviewed fresh and merged.
- **Data (improving):** where viewers leave each video, the best-ranked idea for flat watch time, had waited on a workflow change only you can make. It does not need one: the weekly job can add it to the file it already saves. Built on a branch, it records the share still watching at five points in each recent upload, and a failure costs only those columns. It merges after Monday's snapshot lands, so a fault cannot cost the reads waiting on that snapshot.
- **Product:** two ranked checks were already answered. Bet 1's pre-committed rule already counts a vote that falls back. And three answers cannot push a video past the 45-second limit: today's version reads three too, and its longest of 45 uploads ran 31.5 s.
- **Data:** every pending experiment's pre-committed read still runs on today's tools (results not looked at, so nothing was peeked).
- **Considered and dropped:** a wider backup-AI check of the content screen (it needs Reddit access, and the current check passes 7 of 7 twice); questions addressed to a profession ("Nurses, …"; 5 in 168 uploads, too few to test); logging repaired AI replies (waits on bet 1's merge). Ranked in two passes, opposite orders. This shift was mostly fixing, with two improvements (the dropped list, retention).
- **Security:** standing check clean: no secrets in the project, no workflow changes, you remain the only collaborator, money controls in place ($0.48 this month, forecast $0.82 of $3).
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- 18 October: read the 08:17 release check. On a pass with #77 labelled, merge bet 1 as the next version, close #74, #77 and #78, and update the trackers.
- 19 October: the weekly review; first week's viewer comments; the dark-morbid question; the watched clip's rule. Once that snapshot has landed, merge the retention branch after its review's findings are fixed, then teach the report to read it.
- 5 November monthly review: as listed in the entry below (retention curves now need nothing from you), plus re-raises that update an ask's opening text.

### Better?
- **Than last shift:** Slightly, in the ask rather than the product: the decision that gates revenue can no longer be read two ways. Nothing reached viewers.
- **Than ~10 shifts ago:** No, on the audit's evidence: two title fixes in 8 shifts, watch time flat at 12.0 seconds, bet 1 unshipped since 11 October.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-17 (14:13) — Bet 1's release check failed today, and its cause is fixed: the AI's reply could cost an upload every host note

    Worked (% of the shift): reliability 35 · engineering 20 · product 15 · legal 10 · data 5 · gm 10 · security 5

**Summary:** Today's automatic check on bet 1's three-answer version failed, so a label on #77 alone could not have shipped it. The cause was the AI's reply going wrong in ways that would have cost real uploads the host's notes. It is fixed and tested live, and tomorrow's check decides.

### Toward revenue
- **Bet 1 was quietly blocked on our side, not only on your label.** The midday release check found the AI's reply unreadable, so the title, the vote and every host note fell back to a plain reading. Live, the same request failed two more ways: a stray comma at the end of the reply, and four host notes for three answers. Either drops the host for that whole upload, and one in a handful would have weakened bet 1's read. The request now gives the AI the exact shape of its reply, which it holds to while writing. On the model real uploads use, it returned every field and exactly three notes. The model that writes samples accepts it too.
- **YouTube now rewards originality with reach, not only with pay.** On 1 October YouTube said the Shorts feed, which brings us 96% of our views, will favour original videos and cut reach for channels that mainly re-post others' clips. Readings like ours are not named, and there is no sign of a cut yet: the week it was announced was our best of six for views. But it makes bet 1 a defence of our reach, not only a step toward pay. Also, YouTube's own policy page sets no voice requirement for commentary ("a funny or thoughtful spin" counts), so the worry that a text-only host cannot qualify rests on a community guide and is weaker than the plan said. Both go to the 5 November review.
- **How bet 1 will be judged when some notes drop is now written down, before any upload.** Every bet 1 video counts. If fewer than 15 of the first 20 show all their notes, a keep is credited to the host as shipped, not to the notes, and fixing the drop rate comes next. Decided now, so the read cannot pick the flattering cut later.

### Done
- **Reliability (fixing):** the fix above, on bet 1's branch, reviewed fresh (no bugs; one test that passed for the wrong reason, fixed). It spent 2 of today's 20 shared AI requests; both uploads before the reset still fit. Failures now log the AI's reply around the fault, so the next one can be read without guessing. #78, which the check raised, now explains this and needs nothing from you. A new sample of the fixed branch played, and for the first time on this version every note and the vote showed. Its frames are now on #77, so the version you would be approving is shown whole.
- **Product and data (improving):** bet 1's rule above. The two-answer version (#74) now carries the same fix, so if you choose it, a sample is the only step left.
- **Legal and distribution (improving):** the YouTube reading above, recorded in the plan's risk list.
- **Engineering (fixing):** sample reports had listed a thread's own words as failed steps whenever the thread mentioned failure (today's was about "failed" attempts to domesticate animals). Fixed and merged after a fresh review.
- **General management:** trackers updated; the product tracker trimmed back under its size limit (settled history, all in git). #50's patch still applies cleanly to the live code, so its four commands are still current.
- **Considered and dropped:** the same fix for the content screen (3 fallbacks in 180 uploads) and the backup AI (about 1 upload in 100); logging each repaired reply (it would void the new sample; noted for after bet 1 merges). Ranked eight fresh candidates (two passes, opposite orders): the YouTube reading came first, done; a projection of bet 2's window came second, done as one line under Next; a spelling check found one misspelling in the last 50 AI-written titles (2%), so no guard; the rest scored low (likes, a median of 0 per upload; the old videos' cost, which waits on bet 1; Polly at four a day, already approved). Handed over about 30 minutes early: both ready items wait on #77, and nothing left cleared the bar. Pre-flight: bet 1's branch merged into today's live code passes all 592 tests. This shift was mostly fixing, with two improvements (the rule, the YouTube reading).
- **Security:** standing check clean: no secrets in the project, no workflow changes, no new library advisories, money controls in place ($0.48 this month, forecast $0.82 of $3). The screen has skipped no post since September, only unsafe answers.
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label settles bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- 18 October: read the 08:17 release check. On a pass, close #78; if #77 is labelled, merge the three-answer version as the next version, close #74 and #77, and update the trackers. On a fail, the log now shows the reply.
- 19 October: read the first week's viewer comments, the dark-morbid question and the watched clip's rule.
- 5 November monthly review: YouTube's originality rules (reach, and the policy's wording); bet 2's window: a label on #77 by about 1 November still puts four uploads a day in place for all four weeks bet 2 is measured on, where it needs about 148 views per upload (recent weeks: 71 to 310); the TikTok question with the follower caveat; the subscription's price against Partner Program revenue; retention curves; the weekly allowance's dark days; and a process note from today: a failed release check emails you an issue a shift can usually explain within hours, so it could go to the next shift first and reach you only if it persists.

### Better?
- **Than last shift:** Yes, slightly. A fault that would have stopped bet 1 at the gate, or quietly stripped its host from some uploads, is fixed before any upload. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.
