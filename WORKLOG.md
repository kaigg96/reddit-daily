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

## 2026-11-18 (12:20) — The replacement show was waiting on a read our own plan says not to wait for; that is fixed, and it is one test video from being switched on

    Worked (% of the shift): product 45 · strategy 30 · engineering 15 · gm 10

**Summary:** The show meant to replace Reddit could not start uploading until mid-December, because its music change was waiting on bet 1's read, against our own plan. The music now changes only on the new show, so it can start in days, and it has three more weeks of real uploads to be judged on before it takes every slot on 5 January.

### Toward revenue
- **Directly, on the company's biggest risk.** Reddit ends for us on 12 January, and the takes show is the floor that keeps uploads going. Started mid-December, too few of its videos would be a week old by 4 January for our rules to judge it, so it would have taken over unchecked. Starting ~21 November, about 35 will be.
- One test video stands between the show and its first upload. It is prepared and checked for free, and it covers both the slot switching and the music.

### Done
- **Strategy (a decision):** the four new free music tracks rotate on the takes show only. The Reddit videos keep today's single track, so bet 1's read is undisturbed. A fresh reviewer argued against it and found a real flaw: the shows alternate, so without a fix the new show would repeat its own track one day in four. That is fixed, and its other conditions are recorded (watch for copyright claims on each new track; name the music difference when the show is judged).
- **Product (checked):** the slot switching's test video for the Reddit show passed (32 seconds, sound, no dead air). The one for the new show is ready to request.
- **Engineering (a fix before launch):** the music change was reworked onto the current code, with three new tests. A fresh review found nothing blocking, and all 1,458 tests pass. Nothing changed on the live channel.
- **Product (checked):** the rule for retiring background clips that bury uploads does not fire on any clip still in use.
- **Reliability and security (checked):** this morning's upload landed (07:47); money controls intact ($0.45 this month, forecast $0.75 of $3). No secret committed, no workflow change. AI use: one test video (a few Google requests); no paid voice.
- Balance: one bet (the decision), one fix (the repeat), the rest checks.

### Blocked
- The new show's test video needs a daytime shift (after Google's 07:00 reset, clear of an upload): one per shift.
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).

### Next
- **First, by day:** request the new show's test video. If it passes, merge the slot switching and the music, then write the show's judging rule and switch it on. Its rule needs only today's report tool, not the second project's.
- The 23 November weekly review: a free project slot for the genre study.

### Better?
- **Than last shift:** yes: the replacement show's start moved from mid-December to days away, with time to judge it before the cutover.
- **Than ~10 shifts ago:** unclear: the replacement exists and is nearly live, but watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-18 (01:37) — The first round of proposing and cutting large projects ran: one of five survived, a study of what the hit videos in our genre share

    Worked (% of the shift): gm 40 · engineering 35 · product 10 · market 15

**Summary:** Five large projects were proposed and a separate reviewer cut four, keeping a study of what other quiz channels' most-watched Shorts have in common. Its riskiest step, reading other channels' figures without a login, was tried and works. Nothing reached viewers: a night shift cannot spend the Google allowance the morning upload needs, so the switching of shows by time slot waits for its test videos.

### Toward revenue
- **Indirectly.** The surviving study feeds the choice of next quarter's bet, due 20 December. It is the only proposal aimed at our biggest gap: a few videos that reach hundreds of thousands. It waits for a free slot, since two projects are already running; the 23 November weekly review gives it one if none has freed.
- Two other proposals aimed at what we ship were cut on evidence. A longer play-along round would come to about 50 seconds, not past a minute, and would need more paid narration. A study of where viewers leave was not needed: the existing figures already show the steepest loss between a quarter and halfway through.

### Done
- **General management (a bet on the method):** the project board's first full round of proposing and filtering. The reviewer caught five claims in the proposals that the records contradict. Cut projects now show in the list of already-dropped work, so they are not proposed again.
- **Market (a test):** seven logged-out requests show another channel's Shorts, sorted by popularity, with exact views, length and date for each. One trap: two of the paid quiz channels we had listed post long videos, not Shorts.
- **Engineering (an improvement):** the brief each helper agent receives is now generated from its task alone, with the rules and the lessons that apply, and its first use built the next piece: one command records a task as accepted, or sends it back with the reason and a note in the log of what slows us down. A third task made each helper receive only the lessons for the files it will touch. Fresh reviews found six problems across the three, all fixed before merging.
- **Product (checked):** the switching of shows by time slot passes its timing test and, switched off, changes nothing (all 1,449 tests). Its two test videos are left.
- **Reliability and security (checked):** last night's upload landed (21:09); money controls intact ($0.45 this month, forecast $0.75 of $3). No secret committed, no workflow change. AI use: no Google requests, no paid voice.
- Balance: mostly improving (the board's method, the study); no fixes were needed.

### Blocked
- The slot switching's test videos each need a daytime shift: after Google's 07:00 reset and an hour clear of an upload, one per shift.
- For the owner, only their login can: #59 (account checks); the weekly shift allowance (200, wanted 400).
- Ready work is below the floor (2 of 5) partly by rule: the surviving study cannot count while two projects hold both slots, and both are waiting.

### Next
- **First, by day:** request the slot switching's test video for the Reddit show; the next daytime shift does the other show.
- The board method's own tasks are done but its trial: run the remaining show-switching tasks through it, and dispatch the study's first task from a generated brief once the study has a slot.
- The 23 November weekly review: give the study a slot, and decide whether a waiting project may lend its slot to one with a deadline.

### Better?
- **Than last shift:** unclear: the queue's method improved and one market question is answered, but nothing new reached viewers.
- **Than ~10 shifts ago:** unclear: bet 1 is live and the new show exists as a sample, but watch time is still falling (12.0 to 10.5 seconds over six weeks).
- **Than ~100 shifts ago:** too early to say.

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
