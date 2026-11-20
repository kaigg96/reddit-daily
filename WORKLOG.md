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

## 2026-11-20 (12:08) — The daily release check stops spending a third of Google's AI allowance to learn nothing, and switching off the two-show rotation can no longer stop uploads after Reddit ends

    Worked (% of the shift): reliability 45 · data 30 · gm 20 · security 5

**Summary:** Two fixes protect uploads through the takes launch and the 12 January cutoff. The daily release check no longer re-asks Google's AI every day after an inconclusive result, and from 5 January every upload is takes even if the two-show rotation is switched off. Bet 1's verdict will now also say how many of its videos the weaker backup AI wrote, which so far is most of them.

### Toward revenue
- **Directly, on the fatal risk.** One switch, if it were turned off after a bad read, would have stopped every upload from 12 January. That can no longer happen.
- **Indirectly, by protecting the two reads that set direction.** Bet 1 (~25 November) and takes (4 January) are judged on uploads. The release check was taking 6–8 of the 20 daily AI requests those uploads share, and on 18 November an upload then ran out.

### Done
- **Reliability (shipped, a fix):** the release check has come back inconclusive three days running because Google's AI wasn't answering. It retried every day, and it also re-ran on almost any change a shift made. Now an inconclusive result on unchanged code waits three days, and only the code it actually tests sets it off. A fresh reviewer found one real gap (the branch for a pending release gets no other test run), and I fixed it before merging. Today's check still runs once, because code it tests changed.
- **Reliability (shipped, a fix):** from 5 January every run is takes, whether or not the rotation is on. Before, turning the rotation off would have sent every run to Reddit, which closes to us on 12 January. Nothing changes for viewers before then. Reviewed fresh; nothing blocking.
- **Data (shipped):** bet 1's verdict now prints, beside its other side figures, how many of the videos it reads were written by the backup AI. It never triggers anything.
- **Data (a finding):** in practice, bet 1's host is its closing vote alone. On its first 7 videos our quality filter dropped the opening line every time (we expected about 1 in 6–8 to pass), and the vote shipped on 6. This morning's video lost both: the backup AI wrote a vote one word too long, so it went out as a plain reading. Not acted on, because bet 1's rule already covers a thin dose, and raising it comes after the read.
- **Reliability (a finding):** Google's AI was overloaded on 5 of this week's 8 uploads, against 0–2 a week before, on the same model as last week. The cause is on Google's side, not our change, but it means the backup wrote most of bet 1's videos so far. Recorded for Monday.
- **General management:** the queue had no ready items against a minimum of five. I proposed two rounds of eight, and a fresh reviewer ranked each round in both orders. I did the top items that were neither blocked nor already done.
- **Checked:** this morning's upload landed (07:33) and its run succeeded. Money controls are intact ($0.52 this month, forecast $0.79 of $3). No secrets committed, no workflow change. AI use: none of Google's allowance, no paid voice.
- Balance: three fixes and two findings, no bet. The takes show, which changes what we ship, goes live tonight.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **Today's later shifts (20 November):** still no test videos and no Google AI requests until 08:00 UTC on 21 November.
- **21 November, first:** check tonight's first takes video (logged as takes, nothing of Reddit's in its title, description or tags), then mark the takes task done. That frees the next tickets for helper agents, starting with the choice of how the play-along show gets its slots.
- **23 November, the weekly review:** check whether Google's overload persisted (this week, 5 of 8), and read the new backup-AI figure beside bet 1's verdict. Also: the "blocked or rejected" line for each music track's first takes video, bet 2's capitals test, and the genre-hits study's project slot. The release check should by then have skipped at least one day.
- Dropped this shift: telling the backup AI the vote's word limit (it changes the video during bet 1's read); a brand-name check (the handles were checked on 15 November, and the pick waits for the show choice); an automatic check of the first takes video (a minute by hand, once); the cosmetic startup line; pricing fan funding (no show chosen yet, and we are ~209× short); how concentrated views are (dropped before); the winter reset hour for test videos (a workflow change only you can approve, and low exposure); retrying Google's main model before the backup (it already retries once); the vote's opening repeating across videos (the prompt asks for it: it's the show's signature line, not template content). Nothing else cleared the bar, so I handed over at 12:08, 31 minutes early.

### Better?
- **Than last shift:** yes, slightly. Uploads after 12 January no longer depend on a switch staying on, and from tomorrow the uploads keep more of their AI allowance.
- **Than ~10 shifts ago:** yes. On 15 November the replacement show was switched off. Tonight it uploads, and the reads that will judge it now show which AI wrote each video. Watch time still reads as falling (12.0 to 10.5 seconds).
- **Than ~100 shifts ago:** too early to say.

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
- **General management:** the queue had one ready item against a minimum of five. I proposed eight; a fresh reviewer ranked them in both orders. I did the first, second and fourth (the copyright line), plus two smaller fixes; the third is dropped below. Helper instructions now say where the tools live, which the first helper lacked.
- **Checked:** both of yesterday's uploads landed. Money controls are intact ($0.49 this month, forecast $0.78 of $3). No secrets committed, no workflow change. AI use: none of Google's allowance, no paid voice.
- Balance: four fixes and one check. The switch is a fix to a known gap, not a bet.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **Today's later shifts (20 November):** no test videos and no Google AI requests until 08:00 UTC on 21 November. Tonight's takes video, tomorrow's early-morning takes video and the daily release check all draw on the same day's 20 requests (about 14–16 expected).
- **21 November, first:** check tonight's first takes video (logged as takes, nothing of Reddit's in its title, description or tags), then mark the takes task done. That frees the next tickets for helper agents.
- **23 November, the weekly review:** read the new "blocked or rejected" line for each music track's first takes video; count takes runs that fell back from Google's AI, beside the daily release check, which has come back inconclusive three days running (Google's AI failing) and so re-spends 6–8 of the 20 requests every day; read bet 2's capitals test; give the genre-hits study the project slot it is waiting for.
- Dropped tonight: testing the takes show in the daily release check (it would spend 2–4 more of Google's 20 daily requests on days already near the limit); starting the genre-hits study three days early (the two-project limit is enforced in code and Monday opens its slot anyway); a reworked startup message (cosmetic, and in the upload code hours before the first takes video); counting Google requests per day (no takes day exists yet); closing an old code-health item (each waits on bet 1's 20th video, the 7 December review or an owner change); limiting when the release check runs (the same trigger runs the test suite, so it needs a workflow change, recorded for Monday). Views per video rose about fourfold in three weeks, but the views the Partner Program counts held level (about 125 a video), so the distance to the bar is unchanged (~696×). Nothing else cleared the bar, so I handed over at 01:52, 23 minutes early.

### Better?
- **Than last shift:** yes, slightly. Continuity after 12 January no longer depends on someone remembering a date.
- **Than ~10 shifts ago:** yes. On 15 November the replacement show was switched off and Reddit's end had no plan in code. Now takes uploads daily and takes over by date. Watch time still reads as falling (12.0 to 10.5 seconds).
- **Than ~100 shifts ago:** too early to say.
