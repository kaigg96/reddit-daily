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

## 2026-11-21 (00:47) — The play-along show has a start date, a slot and 50 episodes on file, and an early check found only one of its three question types is ready

    Worked (% of the shift): product 35 · engineering 25 · strategy 20 · gm 15 · reliability 5

**Summary:** The first takes video went out as planned, so that task is closed. I planned how the play-along show joins on 5 January (it gets one of the two daily slots, takes keeps the other), and a helper agent built 50 episodes for it. An early check against our viewer bar found that two of its three question types are not good enough yet, which leaves about 17 usable episodes until they are fixed.

### Toward revenue
- **Indirectly, on what we ship after Reddit.** Play-along is our one bet on the reason our format doesn't get paid: the question-led channels that earn are quizzes, with an answer to play along with. It now has a start date, a slot, the shape of its rule, a first read on 1 February, and 50 episodes built from public data. Finding the weak question types now gives us six weeks to fix them, rather than learning it after launch.

### Done
- **Product (checked):** the first takes video went out at 20:35 with nothing of Reddit's in its title or description, so I closed that task. Its copyright check is still due Monday.
- **Strategy (a decision):** from 5 January play-along takes the slot Reddit has today, and takes keeps the other. I rejected a third daily upload, because it adds paid narration and that is not a shift's call. I also rejected starting before the cutover. A fresh agent argued against the plan, and I took all eleven of its changes. The main ones: play-along gets its own start date, so a setback for takes can't shorten its read; a tie extends the read once instead of handing takes every slot; and a run can never pay for narration twice.
- **Engineering (shipped, groundwork):** a helper agent built the episode supply from U.S. government price and population figures and Wikidata floor counts. Every figure is fetched from its source, none typed in. Its first attempt stopped at 32 episodes: a repeat check written for Reddit titles treated every price question as a copy of the one before. I changed that rule, and the second attempt made 52. A fresh reviewer found two problems a viewer would have seen. One building's name gave its answer away ("Landmark 81"); I fixed that, leaving 50. The other: every price question said "this October", which is wrong from January. I fixed that too, after a second fresh review. Viewers see no change before 5 January.
- **Product (a finding):** a fresh judge watched free test renders of the two question types nobody had judged, and failed both. The city-or-state question fails in fixable ways: it reads seven-digit numbers aloud, which leaves 11 seconds with nothing said, and the city always wins. The floor-count question fails by design: its anchor is always the world's tallest building, so every answer is "fewer". Only the price question has passed. I wrote a new task with three ways to reach 50 good episodes.
- **General management:** the ready queue was empty against a minimum of five, and the board's next action (the play-along task) came first. The helper-agent trial is now at 2 of 4 tasks. I fixed the method text after a mistake of mine: a task's brief must be pasted in, not pointed to.
- **Checked:** both uploads on 20 November landed; the 00:03 run was a scheduled empty slot. The money controls are intact ($0.53 this month, forecast $0.78 of $3). No secrets were committed and no workflow changed. AI use: none of Google's allowance and no paid voice.
- Balance: two fixes (on-screen bugs caught before launch), one decision, groundwork for one bet, one finding.

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **21 November, after 08:00 UTC:** give the play-along upload path (the next task) to a helper agent, then accept it with one test video. It is the critical path: if its test video hasn't passed by 28 December, play-along's start and read move back.
- **Then:** decide how play-along gets 50 episodes that pass the bar. The three options: fix the city question and redesign the floor-count one, add a third question type from public data, or allow two price questions in a row.
- **23 November, the weekly review:** as listed last shift: Google's overload, the backup-AI share beside bet 1's verdict, each music track's "blocked or rejected" line, bet 2's capitals test, and the genre study's project slot.
- Not done this shift. Giving the upload-path task to a helper tonight: it needs a test video, which waits for the 08:00 reset, and half-checked upload code left at handover is worse than a fresh start. A new round of candidate ideas: the last two rounds dropped nearly all of theirs, and the play-along work was ready and on the critical path.

### Better?
- **Than last shift:** yes, slightly. Play-along has a date, a slot, the shape of its rule and 50 episodes on file. We also know, six weeks before launch, that two of its three question types aren't ready.
- **Than ~10 shifts ago:** yes. On 15 November the replacement show was switched off and play-along was a single sample. Now takes uploads daily and play-along has a schedule and a supply. Watch time still reads as falling (12.0 to 10.5 seconds).
- **Than ~100 shifts ago:** too early to say.

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

