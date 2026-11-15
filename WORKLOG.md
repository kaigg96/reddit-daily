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

## 2026-11-15 (18:18) — Your approval on bet 1 can no longer lose its sample video; the backup show's kind of question shows no cost in watch time

    Worked (% of the shift): data 30 · engineering 20 · strategy 15 · gm 15 · product 10 · reliability 10

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). Three of your open asks got easier to answer: bet 1's sample video no longer expires, the backup show's music has a route that needs only your say-so, and four uploads a day no longer has to wait for bet 1.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest step: bet 1's sample video, the one piece of evidence behind that label, would have been deleted by GitHub on 27 November. It is now kept for good, and #77 links to the kept copy. Bet 1 and the two changes that follow it still merge cleanly into today's live code, with all 1,244 tests passing, so your label still ships it straight away.

### Done
- **Product (bet 1's evidence kept; a fix):** the 13 November sample is copied, byte for byte, to where we keep the backup show's samples. Editing #77's text sent you no email.
- **Data (a question answered: no evidence of a cost):** the backup show replaces Reddit's questions with plain everyday ones, with no news, health, sex or named people or brands. Do questions of that kind hold viewers less? I set the rule and saved it before seeing any figure. A fresh reviewer found my sorting misfiled 21 questions one way, for example "…of Reddit" openers and capitals used for emphasis. I fixed that, again before any figure. Among AskReddit videos at a week old, everyday questions held viewers 10.0 seconds against 11.0 for the rest, 9% lower. Random halves of these videos differ by 10% one time in ten, so by the rule that is no evidence of a cost, and nothing changes. It is narrow, and the two groups mix our older formats unevenly.
- **Strategy (music for the backup show; a bet):** #90 needs more music tracks, which today means your hands. Kevin MacLeod's library is free to use with a credit, may be kept openly in our public files, and is registered with YouTube's copyright matching. A video only gets claimed when the credit is missing, and a claim is released within three days of a dispute. So "use those" on #90 would let a shift do the rest: pick the tracks and add the credit to each description. I built nothing, because the track choice is yours to approve.
- **Strategy (a loose end closed):** after the backup show is on, sample videos of Reddit's show still work from a test branch. No workflow change of yours is needed, despite what the last handover said.
- **Engineering (four a day, unblocked from bet 1; a bet):** going to four uploads a day needs each run's time slot in the upload log. That change was built on top of bet 1, so four a day had to wait for it. It now also exists on the live code, ready but not merged. It still merges cleanly with bet 1 in either order, and all 1,242 tests pass on the two together. A fresh review found nothing blocking. I fixed its two small points: the slot is now worked out before the upload, and the weekly report counts late uploads on the right day. So the 20 November update to #80 can offer four a day first.
- **Reliability (a four-a-day risk re-checked):** a pile-up of late runs could cancel a waiting upload. None of the 394 scheduled runs since June was cancelled. Since 13 October no two runs started closer than 3 hours apart, even with GitHub starting them hours late.
- **General management (ranking):** with nothing ready, a fresh helper proposed seven ideas and two others ranked them forwards and reversed. The top four came out in the same order both ways, and I did them plus a fifth. Dropped: an automatic switch to the backup show only if Reddit cuts us off. It is the costliest of the seven, more than this shift had left, and both rankings put it last or nearly last. A second, smaller round at 18:16 found two fixes to title wording: refusing "<" and ">", and catching stretched swear words. Both change code bet 1 rewrites, and our rule for both is to wait for bet 1's first 20 uploads. Nothing else cleared the bar, so I handed over at 18:18, 24 minutes early.
- **Security and reliability (checked):** both of yesterday's uploads and this morning's landed; the 12:23 run was a normal skip. Money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret committed, and no workflow change since #95.
- AI use: none of Google's allowance (the 18:23 upload was within the hour), no sample video, no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #90 (one label, plus music, or "use those" for the route above), #65 (your yes to the corrected sentence), #80, #59.

### Next
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and AskReddit's falling share watched.
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging (today's copy, which has the review's fixes; all tests pass with bet 1).
- **If #90 is labelled:** settle the release check's AI request count, then take a sample video of the switch-on, then merge it.
- **About 18 November:** the new model's 20th video. **20 November:** if bet 1 is still unmerged, update #80 and offer four a day first. **23 November:** the capitals read. **7 December:** the data-retention decision.

### Better?
- **Than last shift:** no, not toward revenue. Three of your asks got easier to answer, and one doubt about the backup show was tested and not borne out.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
