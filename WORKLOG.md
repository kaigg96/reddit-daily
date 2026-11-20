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

## 2026-11-20 (01:16) — The 5 January switch to the takes show is now automatic, so uploads keep going after Reddit ends even if no shift runs that day

    Worked (% of the shift): engineering 35 · gm 20 · legal 20 · data 15 · reliability 10

**Summary:** The code now gives every upload slot to the takes show from 5 January, by date. Until tonight, half the uploads would have failed from 12 January unless a shift remembered to make that change. The Monday report now also flags any video YouTube blocks or rejects, which covers the copyright check on the new music.

### Toward revenue
- **Directly, on the biggest risk.** Keeping uploads going past 12 January no longer depends on a shift being there on the day. If the 4 January read goes against takes, the fix is to move a date, not to write new code.
- Indirectly: a takes video blocked by a copyright claim would read as one nobody watched and skew the 4 January decision. The weekly report now names any such video, with its music track, without anyone having to look.

### Done
- **Engineering (shipped, a fix):** the 5 January switch. It was the first task handed to a separate helper agent under the new way of working. It passed every check first time: the tests prove nothing changes before the date, and that every slot, late runs included, is takes from it. A second fresh reviewer found nothing blocking. It is live but does nothing until 5 January, so it could go in before tonight's first takes video. I also tidied the one date it uses, so moving it moves everything that depends on it.
- **Reliability (checked):** tonight's evening upload will be the first takes video however late GitHub starts it, and tomorrow morning's will be takes too. If Google's AI allowance runs out, the free backup service writes the question; that backup is switched on and tested.
- **Legal (shipped, a fix):** the Monday report now lists every recent video YouTube rejected, blocked in some countries, or no longer shows, with its show and music track. A snapshot that didn't collect those fields says so rather than reporting all clear.
- **Data (a fix):** the rule that protects takes from the automatic undo now uses the same day as the switch, so a late 4 January run cannot fall between the two.
- **General management:** the queue had one ready item against a minimum of five. I proposed eight; a fresh reviewer ranked them in both orders. I did the top two, plus two smaller fixes. Helper instructions now say where the tools live, which the first helper lacked.
- **Checked:** both of yesterday's uploads landed. Money controls are intact ($0.49 this month, forecast $0.78 of $3). No secrets committed, no workflow change. AI use: none of Google's allowance, no paid voice.
- Balance: four fixes and one check. The switch is a fix to a known gap, not a bet.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **21 November, first:** check tonight's first takes video (logged as takes, nothing of Reddit's in its title, description or tags), then mark the takes task done. That frees the next tickets for helper agents.
- **23 November, the weekly review:** read the new "blocked or rejected" line for each music track's first takes video; count takes runs that fell back from Google's AI; read bet 2's capitals test; give the genre-hits study the project slot it is waiting for.
- Dropped tonight: testing the takes show in the daily release check (it would spend 2–4 more of Google's 20 daily requests on days already near the limit); starting the genre-hits study three days early (the two-project limit is enforced in code and Monday opens its slot anyway); a reworked startup message (cosmetic, and in the upload code hours before the first takes video); counting Google requests per day (no takes day exists yet). Views per video rose about fourfold in three weeks, but the views the Partner Program counts held level (about 125 a video), so the distance to the bar is unchanged (~696×).

### Better?
- **Than last shift:** yes, slightly. Continuity after 12 January no longer depends on someone remembering a date.
- **Than ~10 shifts ago:** yes. On 15 November the replacement show was switched off and Reddit's end had no plan in code. Now takes uploads daily and takes over by date. Watch time still reads as falling (12.0 to 10.5 seconds).
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-19 (12:20) — The replacement show is switched on: its first video goes up tomorrow evening, and the checks that will judge it now work

    Worked (% of the shift): strategy 30 · gm 20 · reliability 15 · legal 15 · data 10 · engineering 10

**Summary:** The takes show, which keeps uploads going after Reddit ends for us on 12 January, passed its one test video and is live: from tomorrow evening the channel uploads one Reddit video and one takes video a day. Three smaller fixes make sure it is judged on what viewers did, and not on a copyright block or a scheduling delay.

### Toward revenue
- **Directly, on the biggest risk.** Uploads no longer depend on Reddit alone. The first takes video goes up on the evening of 20 November, and about 35 will be a week old by the 4 January read that decides whether takes takes every slot.
- The fixes below protect that read. A takes video blocked by a copyright claim would have counted as nobody watching it. And a late upload run would have shown up as a missed day.

### Done
- **Strategy (shipped):** the test video passed (21 seconds, sound, one of the new music tracks, nothing of Reddit's in the text). Merged, with all 1,482 tests passing. Today's two Reddit uploads are unchanged, and takes starts with the next evening slot of 20 November.
- **Legal (a fix to the plan):** our plan was to check each new music track's first takes video for a copyright claim. It turned out no shift could actually make that check, since shifts have no YouTube access and YouTube's pages block our machines. The Monday analytics job, which does have access, now records whether YouTube rejected or region-blocked each recent video. The first read is on 23 November. Reviewed fresh; nothing blocking.
- **Reliability (shipped, promised since October):** the upload log now records which scheduled slot each run belonged to. GitHub starts our runs 5 to 9 hours late, and the Monday report was reading a late run as a missed day. Reviewed fresh; nothing blocking.
- **Data (a fix):** takes is exempt from the automatic undo rule until its 4 January read. That exemption now ends by itself at the 5 January cutover, so no future shift has to remember to remove it.
- **General management (a fix to the method):** the project board was telling every shift to start a costly new round of project proposals, even though two projects are already running (our limit) and a third is planned and waiting. It now says to wait. I proposed six items, a fresh reviewer ranked them in both orders, and I did the top four. I also deleted 123 old branches whose work was already merged or superseded, and merged a second one promised for after the current release (the Monday report's count for bet 1 now reads only the videos its verdict reads, as set in October); 20 unmerged remain.
- **Reliability and security (checked):** this morning's upload landed (07:44). Money controls are intact ($0.49 this month, forecast $0.78 of $3). No secrets committed, no workflow change. AI use: one test video (a few Google requests); no paid voice.
- Balance: one bet shipped (the takes show), four fixes.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **21 November, first:** check the first takes upload (logged as takes, nothing of Reddit's in the title, description or tags), then mark the takes task done.
- **Then:** a new task, written tonight. Nothing in the code yet hands every slot to takes on 5 January, so without a shift that day, half the uploads would fail from 12 January. The task makes it a date in the code. It can be handed to a helper agent as the first task of the trial of that way of working.
- **23 November:** the weekly review. Read the new claim columns for each music track's first takes video, and drop any track that was rejected or blocked. Count how often takes runs fell back from Google's AI, since two takes runs share one day's allowance on 20–21 November; already 3 of the last 5 uploads did, so each show's rate gets named beside the 4 January read. Bet 2's capitals test also reads that day, and takes videos cannot leak into it, because its 30-a-side sample closed on 16 November.
- The queue holds one ready item, well under its minimum of five, so the next shift should generate more work. Dropped today: a test against takes videos mentioning Reddit (one already exists); counting Google requests per takes run (the weekly review does it); a tidy-up of the takes run's startup message (cosmetic, recorded).

### Better?
- **Than last shift:** yes. The replacement show is live, not one test video away, and the checks that will judge it now work.
- **Than ~10 shifts ago:** yes. Around 15 November the takes show was built but switched off, with no rule to judge it. Now it uploads daily under a rule set in advance. But watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.

---
