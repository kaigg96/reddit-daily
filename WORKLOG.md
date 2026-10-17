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

## 2026-10-17 (14:13) — Bet 1's release check failed today, and its cause is fixed: the AI's reply could cost an upload every host note

    Worked (% of the shift): reliability 35 · engineering 20 · product 15 · legal 10 · data 5 · gm 10 · security 5

**Summary:** Today's automatic check on bet 1's three-answer version failed, so a label on #77 alone could not have shipped it. The cause was the AI's reply going wrong in ways that would have cost real uploads the host's notes. It is fixed and tested live, and tomorrow's check decides.

### Toward revenue
- **Bet 1 was quietly blocked on our side, not only on your label.** The midday release check found the AI's reply unreadable, so the title, the vote and every host note fell back to a plain reading. In live tests afterwards the same request failed two more ways: a stray comma at the end of the reply, and four host notes for three answers. Either drops the host for that whole upload, and one in a handful would have weakened bet 1's read. The request now gives the AI the exact shape of its reply, which it holds to while writing. On the model real uploads use, it returned every field and exactly three notes. The model that writes samples accepts it too.
- **YouTube now rewards originality with reach, not only with pay.** On 1 October YouTube said the Shorts feed, which brings us 96% of our views, will favour original videos and cut reach for channels that mainly re-post others' clips. Readings like ours are not named, and there is no sign of a cut yet: the week it was announced was our best of six for views. But it makes bet 1 a defence of our reach, not only a step toward pay. Also, YouTube's own policy page sets no voice requirement for commentary ("a funny or thoughtful spin" counts), so the worry that a text-only host cannot qualify rests on a community guide and is weaker than the plan said. Both go to the 5 November review.
- **How bet 1 will be judged when some notes drop is now written down, before any upload.** Every bet 1 video counts. If fewer than 15 of the first 20 show all their notes, a keep is credited to the host as shipped, not to the notes, and fixing the drop rate comes next. Decided now, so the read cannot pick the flattering cut later.

### Done
- **Reliability (fixing):** the fix above, on bet 1's branch, reviewed fresh (no bugs; one test that passed for the wrong reason, fixed). It spent 2 of today's 20 shared AI requests; both uploads before the reset still fit. Failures now log the AI's reply around the fault, so the next one can be read without guessing. The issue the check raised (#78) has the explanation and needs nothing from you. A new sample of the fixed branch played, and for the first time on this version every note and the vote showed. Its frames are now on #77, so the version you would be approving is shown whole.
- **Product and data (improving):** bet 1's rule above. The two-answer version (#74) now carries the same fix, so if you choose it, a sample is the only step left.
- **Legal and distribution (improving):** the YouTube reading above, recorded in the plan's risk list.
- **Engineering (fixing):** sample reports had listed a thread's own words as failed steps whenever the thread mentioned failure (today's was about "failed" attempts to domesticate animals). Fixed and merged after a fresh review.
- **General management:** trackers updated; the product tracker trimmed back under its size limit (settled history, all in git). #50's patch still applies cleanly to the live code, so its four commands are still current.
- **Considered and dropped:** the same fix for the content screen, which has fallen back 3 times in 180 uploads; the same fix for the backup AI, which answers about 1 upload in 100; logging each repaired reply in the upload record (worth doing, but it would change the branch again and void the new sample; it is noted for after bet 1 merges). Ranked from eight fresh candidates (two passes, opposite orders): the YouTube reading came first and was done; a projection of whether bet 2's views target is still reachable came second, and goes to the 5 November review as a sentence, not a document; the spelling check on titles was quick, so I ran it: one misspelling in the last 50 AI-written titles (2%), so no guard; the rest scored low (likes as a side measure, the old videos' cost, Polly per upload at four a day). Pre-flight for tomorrow: bet 1's branch merged into today's live code passes all 592 tests and carries the new version number. This shift was mostly fixing, with two improvements (the rule, the YouTube reading).
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.48 this month, forecast $0.82 of $3). The screen's weekly audit is clean: it has skipped no post since September, only dropped unsafe answers.
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label settles bet 1); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- 18 October: read the 08:17 release check. On a pass, close #78; if #77 is labelled, merge the three-answer version as the next version, close #74 and #77, and update the trackers. On a fail, the log now shows the reply.
- 19 October: read the first week's viewer comments, the dark-morbid question and the watched clip's rule.
- 5 November monthly review: YouTube's originality rules (reach, and the policy's wording); whether bet 2's views target is still reachable; the TikTok question with the follower caveat; the subscription's price against Partner Program revenue; retention curves; the weekly allowance's dark days; and a process note from today: a failed release check emails you an issue a shift can usually explain within hours, so it could go to the next shift first and reach you only if it persists.

### Better?
- **Than last shift:** Yes, slightly. A fault that would have stopped bet 1 at the gate, or quietly stripped its host from some uploads, is fixed before any upload. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-17 (08:28) — TikTok, which the plan called our nearest paying route, is far further away; bet 1's judging rule is fixed before its first upload

    Worked (% of the shift): monetization 25 · product 20 · gm 20 · data 20 · market 5 · security 5 · reliability 5

**Summary:** Bet 1 still waits on your label on #77, so nothing new reached viewers. This shift corrected the plan's claim that TikTok is the nearest paying route (its follower requirement, not its views requirement, is the hard half), and fixed how bet 1 will be judged on a measure that already reads worse, before any upload can colour the rule.

### Toward revenue
- **TikTok is close only on views.** The plan put it about 8× short on its 100,000 views a month. It also needs 10,000 followers, and we gain about one subscriber per 3,000 views (11 from 33,650 views over 90 days). At that rate 10,000 followers takes about 30 million views (17 to 60 million, since 11 is a small count). So TikTok is nearer than YouTube's lowest paying tier only if it turns viewers into followers 3 to 4 times better than YouTube does for us. No published figure says whether it does (one unsourced one puts a typical Shorts channel's subscribe rate near ten times ours). The TikTok country question for the 5 November review now carries that caveat.
- **What the Partner Program would pay:** at its bar, Shorts ads would bring roughly $33 to $330 a month (10 million counted views a quarter at the $0.01 to $0.10 per 1,000 that outside sources quote). Whether that is "revenue above costs" depends on the Claude subscription's price, which the plan does not record. Worth naming on 5 November.
- **Bet 1's "share watched" flag can no longer sink it, or be waved away, over video length.** The channel's scorecard already flags "share of each video watched" as worse, because recent posts run longer. Unwritten, that flag would either sink bet 1 or be explained away afterwards. Now written down: it never triggers a revert (your rule is watch time only), and it is read on longer videos only, against today's version over the same mix of subreddits. More than 5 points lower means viewers leave during the host's notes, bet 1 claims no watch-time gain, and fixing that comes next.

### Done
- **Monetization (improving):** the subscriber rate is now in the standard report, with its likely range and tests, so the follower half of any route, and how unsure it is, comes from the tool rather than a hand count. Reviewed fresh: no bugs.
- **Product (fixing):** bet 1's rule above. A fresh review caught three wrong claims in my first draft: one compared two different kinds of view count (it said 10×, the right figure is 3 to 4×), and one named a length window the report cannot read. All were fixed before merging. Both versions of bet 1 still merge cleanly.
- **General management:** trackers trimmed back under their limits; one stale line corrected (the backup AI that bans training on what we send was described as waiting on you; it ships with bet 1).
- **Ranked and dropped** (nine candidates; two rankers, opposite orders, agreed on the top three, done above): per-video retention curves from the weekly job, the best idea for the flat watch time, but it needs a workflow change only you can land, and #77 should stay the one thing asking for you (for a later review); the chance of a 10,000-view hit (none of 1,054 uploads has reached 2,000, so it changes no decision); audience numbers on their own (the subscriber rate covers the one that matters); a survey of comparable channels' monetization (ads show on unpaid channels too); selling the pipeline (no sign of demand); making the upload step's last length check fail soft (it cannot be reached). A second pass of five added one finding: no subscriber experiment can be read within a quarter, since a test arm gains about five subscribers in that time, so none may decide anything; two shifts running had proposed and dropped one. Its others: whether longer videos hold more watch time within one version (already recorded: yes, by 37%); a steadier views measure for the title-capitals test (chosen after seeing data, it invites picking the flattering one); a daily stats snapshot (needs a workflow change from you). This shift was mostly improving, with one fix. Handed over about 18 minutes early: both ready items wait on #77, and nothing else left cleared the bar.
- **Security:** standing check clean: no secrets in the project, no workflow changes, money controls in place ($0.47 this month, forecast $0.82 of $3).
- **Reliability:** both uploads since the last shift landed, and the record of the last upload is intact.

### Blocked
- **For you, in order:** #77 (one label settles bet 1; four frames, no download); #50 (four commands, which unblocks #65); #59 (account checks).

### Next
- On #77's label: check that today's release check (it lands around 13:15) passed on the three-answer version, merge it as the next version, close #74, then update the trackers. If you label #74's two-answer version instead, its videos run about a quarter shorter, so before its first upload ask you whether its watch-time check should allow for length (the one ranked idea this shift left for you).
- 19 October: read the first week's viewer comments, the dark-morbid question and the watched clip's rule.
- 5 November monthly review: the TikTok question with the follower caveat above; the subscription's price against Partner Program revenue; retention curves, as a change for you to land; the weekly shift allowance's dark days.

### Better?
- **Than last shift:** Slightly, in planning rather than for viewers. A route the plan leaned toward is now priced on both halves, and bet 1 cannot be judged on a flag that measures length. Nothing new reached viewers.
- **Than ~10 shifts ago:** Unclear. Watch time is still flat at 12.0 seconds, and bet 1 is still unshipped.
- **Than ~100 shifts ago:** Too early to say.
