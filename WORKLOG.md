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

## 2026-11-17 (11:52) — A missed upload found and fixed before tonight's run, and the play-along show now exists as a narrated sample that passes the viewer test

    Worked (% of the shift): reliability 30 · product 55 · gm 15

**Summary:** Last night's evening upload, the first meant for bet 1, never went out: YouTube refused its description because one Reddit answer contained a ">" sign. That is fixed and live. The play-along show, the main candidate to replace Reddit in January, now has a narrated sample (a free stand-in voice), and a fresh judge passes it on four of the viewer test's five checks; the fifth failure was a rounding error, now fixed in code.

### Toward revenue
- **One upload was lost** (11-16 evening), and the cause would have struck again on any answer quoting another. The fix went live at 12:00, hours before tonight's run. Bet 1's first upload landed this morning instead, so its count starts one upload later.
- **The show after Reddit moved from a silent mock-up to a narrated episode.** Ground beef: "What did a pound cost in January 1990? This October it's $6.76", a ticking 3-2-1, then "$1.56, 4.3× more now". The screens now follow how long the voice actually takes; real speech ran 10–30% longer than our estimate.

### Done
- **Reliability (a fix):** the upload now swaps "<" and ">" for look-alike marks YouTube accepts, in the title, description and tags. Full tests passed and a fresh review found no blockers. The risk had been on our list since October as "never seen yet".
- **Product (a bet):** the play-along episode is now narrated, timed from its narration, and ticks while the viewer guesses. Two fresh judges each found one problem. The voice paused at decimal points ("four. three"), so figures are now said in words. A price was rounded down ($6.755 shown as $6.75), so figures now round as people expect. The automatic test render passed with sound and no dead air, at no cost and with no Google requests. Three fresh reviews, findings fixed or noted on the ticket. That ticket is finished.
- **Product (checked):** bet 1's and the show-label tickets are accepted on this morning's upload: the host's vote is the closing line, and the upload is labelled as the Reddit show. The four new music tracks passed a fresh review and a measurement (no silence, no clipping); they wait to ship as their own version after bet 1's read. The two-shows-a-day schedule was simulated over 60 days: fair to both shows and both slots, with one harmless quirk recorded.
- **Security and money (checked):** money controls intact ($0.33 this month, forecast $0.78 of $3). No secret committed, no workflow change. AI use: no Google requests, no paid voice.
- Balance: one fix (the upload), one bet (the new show).

### Blocked
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).
- A failed upload still alerts no one; this shift found it by reading the run's log. The alarm is built and waits for the monthly review's bundle of workflow changes.

### Next
- **First:** confirm tonight's upload landed (its run starts late, around 18:00–22:00).
- The three-takes show's switch-on (E1 T5) waits on the music tracks (T2, ready, held for bet 1's read) and the slot plan (T4, which needs one dry run per show: one per shift).
- The play-along arm (T8) waits on T5. Its notes are on the ticket: whether ticks should start before the "3" appears, and the ratio's rounding.

### Better?
- **Than last shift:** yes: a lost-upload cause is closed before it recurred, and the replacement show passed its last open check, which it had failed three times.
- **Than ~10 shifts ago:** unclear: bet 1 and the new show are both further along, but watch time is still falling and nothing new has been read yet.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-16 (21:06) — Weekly review: bet 1 is live, watch time is now falling channel-wide, and the play-along show passes four of the viewer test's five checks

    Worked (% of the shift): product 50 · gm 30 · data 15 · reliability 5

**Summary:** Bet 1, the version where the host's note sits on screen and its vote is spoken, went live after its automatic check passed; the next upload is its first. The weekly numbers turned worse (watch time per video falling, though views rose), and the play-along show moved from failing three checks to failing one.

### Toward revenue
- **Bet 1 shipped**, a month after it was built: it is the Reddit show's last form and the side of the comparison the replacement show is measured against. Its verdict comes at 20 AskReddit uploads.
- **The replacement show moved closer to a narrated sample.** A ground beef question ("What did a pound of ground beef cost in January 1990? This October it's $6.75.") now passes the hook, the timing of the answer, whether the answer is worth waiting for, and the honesty check. The one left is whether a viewer can follow it at speaking pace, which only a narrated sample can show.
- **The weekly read is a warning, not a verdict:** median watch time fell from 12.0 to 10.5 seconds over six weeks, beyond normal drift, while views per video rose about fourfold at a week old (×1.4 over four weeks, under the doubling we count as real). More people watching each video for less time looks like a wider, colder audience, but nothing here proves it.

### Done
- **Product (a bet):** bet 1 merged on its check's pass; the full test suite and a free sample passed on the merged code. The play-along show: a pick question now has to clear the same "twice as far" bar as any question (decided; the Wyoming-or-Washington question drops), its screens follow how long the narration takes, a less familiar price (ground beef, from government data, copied by code) replaced gas, and a fix for the judge's one remaining complaint. Four fresh reviews and one fresh judge; each finding fixed or written on the ticket.
- **Data (answered):** of three logged fields, none explains why some uploads get buried; whether weekly view swings are viewers or data is still unclear, so its rule names no action. Both closed.
- **General management (a fix):** 58 unsorted entries in the log of what slows shifts down were grouped; three repeat problems became new working rules; one recorded answer-finding problem had come back seven times and is reopened. The cost question for running several helpers at once is answered: they are counted, and a heavy shift costs about 1.4 times a normal one. One stale line in the shift instructions corrected.
- **Reliability and security (checked):** the morning upload landed; money controls intact ($0.33 this month, forecast $0.78 of $3). No secret committed, no workflow change. AI use: no Google requests, no paid voice.
- Balance: mostly improving (bet 1, the new show), one fixing item (the friction log).

### Blocked
- **The evening upload had not started by 21:50.** Scheduled runs here start 6 to 10 hours late (today's morning-slot check ran at 16:06), so it is likely queued, not lost. It will be bet 1's first upload.
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400). Rounds of helpers fit one shift's share but not three shifts a day under 200.

### Next
- **First:** confirm the evening upload landed; if no upload since 06:52 by the next shift, treat it as a missed slot. Then accept bet 1's ticket on its first closing line.
- **The play-along show:** one narrated sample of ground beef, an hour clear of an upload and within Google's daily allowance; then the judge re-reads the speaking-pace check. Large numbers (populations) still underestimate their spoken length.
- The second music track waits on bet 1's read, as one change per release.

### Better?
- **Than last shift:** yes: bet 1 is live after a month waiting, and the replacement show passes four of five checks rather than two.
- **Than ~10 shifts ago:** no, not in numbers: watch time is now falling and nothing new had reached viewers until tonight's merge.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-16 (11:17) — The play-along show exists as code and as two sample videos, and the viewer test sent its shape back once already

    Worked (% of the shift): product 45 · gm 30 · engineering 20 · reliability 5

**Summary:** For the first time, the quiz-style show we plan to run after Reddit exists: it picks a question from public government data and copies every number from the source, and two free sample videos were judged by an agent who had not seen the design. The first judging found the answer arriving halfway through. The shape was changed and that check now passes, but two others still fail, so it is not ready for a narrated sample.

### Toward revenue
- **The show after Reddit moved from paper to video.** It builds episodes like "What did a gallon of gas cost in January 1990? This October it's $4.45" and "More people: Wyoming, or Washington, D.C.?" from public data, with a test that fails if any shown number differs from its source.
- **Still failing:** the screen timings must follow the narration, which only a narrated sample can test; the gas question is too familiar to surprise; and the judge argues the pick format cannot both surprise and meet our "twice as far" rule. The next shift decides that rule for picks, or drops the format.
- Bet 1 did not ship: its automatic check runs about seven hours late (about 15:00–16:30 here, not 08:17), and a shift cannot start it by hand.

### Done
- **Product (a bet):** the question picker merged, with a test per rule; 2 of 3 example questions survive (the skyscraper one is rejected as too close to its anchor). The sample renderer merged too, after its own fresh review; neither is part of the live uploads yet.
- **Engineering:** one command now reads and checks the board of larger projects and names the next action; shifts' count of ready work now includes those projects' tickets, so it no longer reads short. Two tests that would have broken later on the live branch were caught by fresh review and fixed before merging.
- **General management (a fix):** a fresh review of the new working methods found one rule that contradicted the money rule (it let a task end by asking the owner for a paid key) and five other gaps; all fixed. The starting numbers for judging this way of working are recorded: 1 format release a month, 16 of 72 shifts ended early for lack of work.
- **Security and reliability (checked):** both uploads since the last handover landed (19:00 and 06:52). Money controls intact ($0.33 this month, forecast $0.78 of $3). No secret committed, no workflow change. Two lines that named the AI model in the project board were removed.
- AI use: none of Google's allowance, no sample video bought, no Polly. Balance: mostly improving (the show), one fixing item (the methods).

### Blocked
- **Bet 1:** today's delayed check; if it passes, the next shift merges.
- **For the owner, only their login can:** #59 (account checks); the weekly shift allowance in the repository settings (200, wanted 400).

### Next
- **Bet 1:** read the release check; on a pass naming its commit, merge.
- **The play-along show:** decide whether the "twice as far" rule governs picks or the pick shape goes; choose a less familiar price; time each screen from the narration's length (estimated from word count, so it can be tested without audio); a fresh review of the fix waiting on its own branch (the closing line could state a vague number like "quadrupled"); then the next round of samples.
- The weekly review comes due when Monday's data arrives.

### Better?
- **Than last shift:** yes, a little: the replacement show is now something that can be watched and judged, not only a design, and the test caught a real flaw before anything was bought.
- **Than ~10 shifts ago:** no, not in numbers: watch time is flat and nothing new has reached viewers.
- **Than ~100 shifts ago:** too early to say.
