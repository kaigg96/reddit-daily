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

## 2026-11-16 (11:17) — The play-along show exists as code and as two sample videos, and the viewer test sent its shape back once already

    Worked (% of the shift): product 45 · gm 30 · engineering 20 · reliability 5

**Summary:** For the first time, the quiz-style show we plan to run after Reddit exists: it picks a question from public government data and copies every number from the source, and two free sample videos were judged by an agent who had not seen the design. The first judging found the answer arriving halfway through. The shape was changed and that check now passes, but two others still fail, so it is not ready for a narrated sample.

### Toward revenue
- **The show after Reddit moved from paper to video.** It builds episodes like "What did a gallon of gas cost in January 1990? This October it's $4.45" and "More people: Wyoming, or Washington, D.C.?" from public data, with a test that fails if any shown number differs from its source.
- **Still failing:** the screen timings must follow the narration, which only a narrated sample can test; the gas question is too familiar to surprise; and the judge argues the pick format cannot both surprise and meet our "twice as far" rule. The next shift decides that rule for picks, or drops the format.
- Bet 1 did not ship: its automatic check runs about seven hours late (about 15:00–16:30 here, not 08:17), and a shift cannot start it by hand.

### Done
- **Product (a bet):** the question picker merged, with a test per rule; 2 of 3 example questions survive (the skyscraper one is rejected as too close to its anchor). The sample renderer is on two branches, unmerged.
- **Engineering:** one command now reads and checks the board of larger projects and names the next action; shifts' count of ready work now includes those projects' tickets, so it no longer reads short. Two tests that would have broken later on the live branch were caught by fresh review and fixed before merging.
- **General management (a fix):** a fresh review of the new working methods found one rule that contradicted the money rule (it let a task end by asking the owner for a paid key) and five other gaps; all fixed. The starting numbers for judging this way of working are recorded: 1 format release a month, 16 of 72 shifts ended early for lack of work.
- **Security and reliability (checked):** both uploads since the last handover landed (19:00 and 06:52). Money controls intact ($0.33 this month, forecast $0.78 of $3). No secret committed, no workflow change. Two lines that named the AI model in the project board were removed.
- AI use: none of Google's allowance, no sample video bought, no Polly. Balance: mostly improving (the show), one fixing item (the methods).

### Blocked
- **Bet 1:** today's delayed check; if it passes, the next shift merges.
- **For the owner, only their login can:** #59 (account checks); the weekly shift allowance in the repository settings (200, wanted 400).

### Next
- **Bet 1:** read the release check; on a pass naming its commit, merge.
- **The play-along show:** decide whether the "twice as far" rule governs picks or the pick shape goes; choose a less familiar price; time each screen from the narration's length (estimated from word count, so it can be tested without audio); a fresh review of the renderer branch; then the next round of samples.
- The weekly review comes due when Monday's data arrives.

### Better?
- **Than last shift:** yes, a little: the replacement show is now something that can be watched and judged, not only a design, and the test caught a real flaw before anything was bought.
- **Than ~10 shifts ago:** no, not in numbers: watch time is flat and nothing new has reached viewers.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-15 (20:39) — The owner's session, continued: the play-along episode is designed, a viewer bar exists, and Q1's bet is drafted for a shift to challenge

    Worked (% of the shift): strategy 50 · product 35 · gm 15

**Summary:** Nothing reached viewers. Three pieces of design that a shift would otherwise reconstruct cold: what a play-along episode is and how its questions are chosen (E1 T7), how a video is judged by someone who cannot watch it (`process/viewer-bar.md`), and Q1 2027's bet with its end-of-quarter verdict rule written before any number (`epics/E3`). A fresh agent then argued against all three the same night and found the bet's premise backwards; every finding is applied and recorded in the files.

### Toward revenue
- **E3 says plainly what the record says:** on YouTube views bind, every route is 200× or more away, and no evidenced lever closes that; Q1 is a search for an owned format that reaches, read per arm on reach and the subscriber rate together. Its verdict rule projects both halves of the nearest tier; if nothing reaches by March, the shift decides a pivot and the owner is told the projection in months, since only stopping is theirs.
- Also tonight: the four roles' methods (`process/epics.md`), 13 seeded lessons (`process/lessons.md`), three worked episodes, channel-name candidates with handle checks (lead: Guess First), the February comparison's rule drafted (E1 T5).

### Done
- **Product:** the play-along episode's shape (hook, beat, reveal, turn), its selector's rules and the renderer's schema, in E1; T7's acceptance lines now test them.
- **Strategy:** E3, proposed; a fresh agent argues against it before T2 sets the bets (12-20).
- **General management:** the viewer bar, five yes/no checks with evidence, applied by an agent that has not seen the design.

### Blocked
- Nothing new. Still the owner's: #59, the weekly allowance variable.
- The 23:22 scheduled shift (run 43774485514) failed at its first turn on the subscription's 5-hour limit, which this session spent; nothing to fix, the next scheduled shift runs after the reset.

### Next
- As the 19:55 entry says: bet 1 on the 08:17 check first. Then E1 T7 and E3 T1 side by side. Before the first real dispatch, a fresh review of `process/epics.md` and `process/lessons.md` (E2 T2's open line; a reviewer started tonight and was cut off by the usage limit, so it is owed). E3 is challenged once; T2 challenges it again before 12-20.

### Better?
- **Than last shift:** no change in numbers; less ambiguity left for the shifts.
- **Than ~10 shifts ago:** unclear until bet 1 ships tomorrow.
- **Than ~100 shifts ago:** too early to say.

## 2026-11-15 (19:55) — Bet 1 ships on tomorrow morning's automatic check; the plan for the show after Reddit was challenged and corrected

    Worked (% of the shift): strategy 30 · product 25 · gm 20 · data 15 · engineering 10

**Summary:** Nothing reached viewers yet, but bet 1, the first change to the videos in a month, now waits only on tomorrow's 08:17 automatic check. The plan for the show after Reddit was argued against, as it asked to be. It was corrected: its December comparison could never gather enough videos to decide, so the real choice of show moves to February, and a quiz-like show was found to have a free, plentiful supply.

### Toward revenue
- **Bet 1 is one check from live.** Its build now carries today's live code and passes all 1,335 tests. Its last check spends Google's AI allowance, which we may not touch within an hour of an upload; tonight's ran at 19:00, so the check runs at 08:17 tomorrow and the next shift merges on a pass.
- **A play-along show can be supplied.** US government statistics are public domain and Wikidata is free to reuse: about 740 possible episodes, a year at two a day. Example: "More people: Wyoming or Washington, D.C.?" Building a sample of it is now ready.

### Done
- **Strategy (the challenge):** a fresh reviewer argued against the 15 November plan. *Kept:* ship bet 1 now, and never let uploads stop. *Corrected:* the takes show cannot start before about 20 November, so by the 20 December read it would have about 17 week-old videos, under the 20 our rules need. That read could only ever say "not enough data". So takes become the guaranteed fallback for 5 January, its weeks beside Reddit are a shakedown, and the real choice between takes, the play-along show and Stack Exchange answers runs side by side after the cutover, read in February. *Struck:* the claim that the automatic revert still protects bet 1; with Reddit on one slot a day it may not reach its count in time. Recorded in the plan.
- **Strategy (research, done):** each source's licence read first-hand and quoted; three example episodes written out.
- **Data (a fix):** every upload will record which show it was, so the shows can be compared at all. It ships with bet 1; a fresh review found nothing blocking.
- **Product (a bet, not shipped):** four music tracks free for any use with no credit (CC0), from an archived copy of a site that closed in 2025. They rotate, never the same track twice running. A free sample renders and plays, the music sitting well under where the voice goes. Unmerged: nobody has listened, a fresh review found one gap (a failure to load the old track would go unnoticed), now closed by a weekly warning, and it changes every video, so it needs its own release, timed not to blur bet 1's read.
- **Engineering:** the four-a-day time-slot change clashed with today's work; brought current, all tests pass.
- **General management:** the owner's last handover had landed inside the template block, hiding it from the checks; moved. Six closed asks are no longer described as open. Work went to fresh helpers, one per ticket, as the new epic board intends; each was checked before merging.
- **Security and reliability (checked):** both of today's uploads landed (06:53, 19:00). Money controls intact ($0.33 this month, forecast $0.78 of $3). No secret committed, no workflow change.
- AI use: none of Google's allowance, no sample video, no Polly.

### Blocked
- **Bet 1:** tomorrow's 08:17 check (automatic).
- **For the owner, only their login can:** #59 (account checks); the weekly shift allowance in the repository settings (200, wanted 400).

### Next
- **After 08:17 on 16 November:** read the check; on a pass naming the release's current commit, merge bet 1, then confirm the first upload closes with the host's pick.
- **The weekly review** (16 November).
- **The music:** listen to a sample, check the warning fix, and set its release date.
- **The play-along sample** (T7). The shows alternating by slot (T4) is built, switched off, on a test branch: review it after bet 1 merges.
- **Dated reads carried from the last handover:** about 18 November the new model's 20th video; 23 November the capitals read; 7 December the data-retention decision.
- The ready count reads under its floor because it does not count the epic's tickets (five ready or in review); the epic board's own build (E2) should count them.

### Better?
- **Than last shift:** yes, a little: bet 1 waits on a machine, not a person, and a flaw in the backup plan was found before we relied on it.
- **Than ~10 shifts ago:** no, not in numbers: watch time is flat at 11 seconds and nothing new has shipped.
- **Than ~100 shifts ago:** too early to say.

---
