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

## 2026-11-12 (02:30) — The process audit found why shifts kept re-proposing ideas they had already dropped, and fixed it; nothing reached viewers

    Worked (% of the shift): gm 80 · strategy 5 · data 5 · reliability 5 · security 5

**Summary:** The process audit, due after 16 shifts since the last one, ran this shift. Its main find: since 4 November the helpers that propose work could not see what earlier shifts had rejected, which explains most of the repeated work the last two audits complained of, and it is now fixed. Nothing reached viewers, and the company is no closer to revenue directly.

### Toward revenue
- **Nothing directly**, because every step that changes what we ship still waits on you (#77, #90). Indirectly, shift time wasted re-proposing rejected ideas is time not spent on work that could move revenue, and that waste had a mechanical cause, now removed.

### Done
- **General management (the process audit):** 16 shifts since 5 November. Half began with nothing ready, they averaged 38 of 60 minutes, and about 40 fixes and checks ran against 8 bets. One change reached viewers, the forced switch of our AI model. All 16 answered "no" to "better than ten shifts ago". The numbers agree: watch time is flat, and the share of videos nobody is shown, 14.7%, is still past its limit. Fresh reviews caught about 50 faults before merging. The sample videos and release checks passed every time and caught nothing, and the faults viewers could see were again found only by reading what we published. The rules held: no AI credit lines, no unapproved process changes, and production data was touched only by the upload job. You answered five quick asks on 10 November and passed over the five needing a watch, a direction call or your hands. That is the pattern that decides what ships.
- **General management (fixed, live):** the idea helpers read a list of what recent shifts rejected. Since 4 November shifts have written that label in a different style, so the list stopped at 3 November and about seven rejected ideas came back. The list now shows all ten recent shifts. The same reading fault showed two shifts twice in our time-by-function table and left two others out, and that is fixed too. Each fix had a fresh review: the first two reviews each caught a real flaw in my first version, and both flaws are fixed.
- **General management (one new ask, #95):** the tool that runs shifts asks every shift to add an AI credit line to each commit, which our rules forbid. Our check only catches it after the push. A one-line setting switches the request off, and your label applies it.
- **General management (a cap):** our findings record grew by about a third in a week with no limit. It now has a word limit set at today's size, so it can only shrink.
- **General management (ranking):** a fresh helper proposed eight ideas and two others ranked them, forwards and reversed. The top two in both orders were already settled. Bet 2's views gap is due on 20 November, and the rule for reading four new unseen videos was set on 10 November. So I did the fourth, the cap above. A per-entry length cap for this report ranked last both times and is dropped.
- **Strategy:** brought the backup show's fixes up to date with the live code, and all 842 tests pass. Its sample cannot run before 07:00, when the sample job starts taking requests.
- **Security and reliability (checked):** both of yesterday's uploads landed. The money controls are intact ($0.25 this month, forecast $0.75 of $3). No secret is in the repository, and the workflows are unchanged.
- AI use: none on uploads; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1: reply "without reactions", or label it as it stands), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **From 07:00 UTC:** bring the backup show's fixes up to date again, request their sample, and merge on a pass.
- **Shrink the findings record:** compress superseded findings to a line each, now that its limit only lets it shrink.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** a little, in process only. The idea helpers can see what was rejected again, which removes the main source of repeated work two audits found. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, the share of videos nobody is shown is still too high, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-11 (18:42) — Two of the new AI model's latest five titles claim more than the question did; a weekly read of the share of plays past the opening is live, and says there is not enough history yet

    Worked (% of the shift): editorial 30 · data 45 · gm 15 · legal 5 · security 5

**Summary:** An evening shift with nothing ready and everything that changes the videos waiting on you, so I made new work and finished the two items that ranked best. Nothing reached viewers. Two of the five titles the new AI model has written put a claim in the question's mouth, so that count is now part of its scheduled check.

### Toward revenue
- **Nothing directly**, because every step that changes what we ship waits on you (#77, #90). One indirect step: YouTube's monetization review reads our titles, and its rules bar titles that are "maliciously misleading". Ours are far milder than that, but a title that accuses or overclaims is a step in that direction. A check is now set before we know how often it happens.

### Done
- **Editorial (a check, not a fix):** I read the three latest uploads as published. "Why do YOU think people fake autism online?" asked viewers whether people are faking a disability, though the question never said fake. "3 Sports Where Women ACTUALLY Have The Genetic Advantage" stated as fact what its answers only guessed. A fresh helper, not told which model wrote what, checked 12 recent titles: 2 of the new model's 5 added a claim, against 1 of the old model's 7. That is too few to act on, and I found it by looking. So the rule is set first: at the new model's 20th upload, the same check on all 20; 5 or more puts a title-instruction fix in line after the capitals test is read on 23 November. It is never a reason to undo the model change.
- **Data (built, live):** our weekly "are we improving?" read uses watch time. Since your #91 decision, tests are judged on the share of plays that get past the opening, so I added that measure too. The first three fresh reviews each found a real flaw, mostly in how a partly-measured week is counted, and the verdict swung with them, from "falling" to "flat" to "rising". After all the fixes, a fourth review found nothing wrong, and I merged it. Its answer today is "not enough history": we have only five full weeks of this figure, and it needs six. Reporting only, so viewers see nothing.
- **General management (ranking):** a fresh helper proposed eight ideas and two others ranked them, forwards and reversed. The title check came second both ways and the weekly read third, so I did those. The other three split: a pre-set plan for bet 2 if #77 stays unanswered (one ranker found it already written on 6 November), a slice of the process audit, and a re-read of YouTube's policy pages. With time left I did the re-read: the monetization and spam pages are unchanged since 3 November.
- **Security and reliability (checked):** this morning's upload landed. The midday run found nothing to do, and the evening one has not started yet. The money controls are intact ($0.25 this month, forecast $0.75 of $3), no secret is in the repository, and the workflows are unchanged. The morning upload's topic-sorting step hit an overload error. It is logging only, never touches the upload, and has happened 3 times in 91 runs.
- **General management (the process audit, first check):** the five process proposals held on 5 November stay held. They wait until fewer than five of my questions to you are unanswered, and five still are. The audit itself is due and is the next shift's work.
- **Your approvals #88 and #65** are still open. #88 waits on you applying its patch (shifts cannot write those files). #65 waits on your "yes" to its corrected sentence.
- AI use: none; no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1: reply "without reactions", or label it as it stands), #82 (register the Reddit app by 12 January), #88 (one command), #90, #65, #80, #59, and the shift allowance setting (on #92).

### Next
- **From about 23:00 UTC tonight**, when the sample limit clears: request the sample of the backup show's fixes, and merge on a pass.
- **The process audit is due:** 13 shifts since the 5 November one, against about ten.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** about the same. A new risk in the titles is now measured, not guessed at. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
