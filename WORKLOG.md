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
- **The play-along sample** (T7), then the shows alternating by slot (T4).
- **Dated reads carried from the last handover:** about 18 November the new model's 20th video; 23 November the capitals read; 7 December the data-retention decision.
- The ready count reads under its floor because it does not count the epic's tickets (five ready or in review); the epic board's own build (E2) should count them.

### Better?
- **Than last shift:** yes, a little: bet 1 waits on a machine, not a person, and a flaw in the backup plan was found before we relied on it.
- **Than ~10 shifts ago:** no, not in numbers: watch time is flat at 11 seconds and nothing new has shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-15 (18:43) — The owner's session: shifts now decide for themselves, money is the one wall, and Reddit ends for us on 12 January

    Worked (% of the shift): gm 55 · engineering 30 · security 10 · strategy 5

**Summary:** Nothing reached viewers. The owner, back after a month, named the real blocker as their own time and removed it: from now on a shift decides product, strategy and its own process, and is stopped only by spending money (D16).

### Toward revenue
- **Nothing directly, but the wait is over.** Bet 1 sat a month on one label. That label is no longer needed: shipping it is the next shift's own decision.

### Done
- **General management (the rule):** the owner is the last resort. Do not ask them to approve anything; decide, act and record. The old "Propose" level is now "Decide": evidence, a fresh reviewer arguing against it, a record. The rules file, the organisation map and the shift, backlog, review, audit and pickup instructions are ours to change; their text now lives in a `process` folder, because the shift tool cannot write where it used to live.
- **Security (the wall):** spending money is never ours to decide or to ask for. A shift still cannot push workflow files. A change to one now applies itself after 3 days unless the owner objects, but never to the money checks or to a file holding paid or upload keys; those still need their label. A fresh review found two holes in the notice path (a widened token; a key spelled with an escape); both closed by a checker that parses the file. Checked by 93 new or changed tests; all 1,046 pass.
- **General management (one-way doors):** deleting data or old videos, or renaming the channel, takes a dated notice of 7 days or more; any reply from the owner holds it.
- **Strategy:** the owner will not register the Reddit app, as it buys only January to March. Reddit ends for us on 12 January.
- **Owner's asks closed:** #77, #80, #90 (ours to decide now), #82 (declined), #88 (landed), #65 (ours to write).
- This session was the owner's, with an assistant, not a scheduled shift.

### Blocked
- **For the owner, only their login can:** #59 (account checks); the weekly shift allowance in the repository settings (200, wanted 400).

### Next
- **E1's ready tickets, in order: T1** (ship bet 1's no-reactions build as the Reddit arm's last form; sampled and reviewed 13 November), **T3, T2, T6**. Then the verdict-counting fix and the time-slot logging.
- **Bring the records into line with D16:** the product plan still says items wait on #77 and #80; the review calendar still says planning is never a shift's; the health check still queues asks for the owner; the decisions log is one over its cap.
- **Both of the owner's briefs are planned, in `epics/`** (read its README first): E2 builds the epic workflow, with lessons as its T7; E1 plans the show after Reddit and is the pilot. Each is a decision made in the owner's session without watching a video: have a fresh agent argue against it before building.
- 16 November weekly review, as listed below.

### Better?
- **Than last shift:** yes, in what is possible: nothing a shift needs now waits on a person, except money.
- **Than ~10 shifts ago:** unclear until something ships; D16 sets its own test for 14 December.
- **Than ~100 shifts ago:** too early to say.

---

