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

---

## 2026-11-11 (10:57) — The backup show is merged, switched off; the last fix for bet 1's host lines failed, so I recommended shipping bet 1 without them and built that version

    Worked (% of the shift): product 40 · strategy 30 · engineering 15 · gm 10 · security 5

**Summary:** The show we would run if Reddit's access ends in January is now in the live code, switched off, after its sample passed this morning. Bet 1's last fix for its host lines failed, so #77 now recommends shipping bet 1 without the short reactions, and that version is built and waiting on your reply.

### Toward revenue
- **Keeping uploads going after January:** the own-questions show is merged into the live code, switched off. Its sample of the code exactly as merged passed (26 seconds, playable), and a fresh review found nothing that changes today's videos. Turning it on stays your call (#90).
- **Bet 1, the product's main step toward original content:** the worked-examples fix scored 0 of 9 against a bar of 7, set before the test. Three fixes have now produced nearly the same lines, so the new model is the limit, not how we ask. I posted the result on #77 with the recommendation we committed to beforehand: ship bet 1 without the per-answer reactions, keeping the host's opening line and closing pick. That version is already built and reviewed, so a "without reactions" reply leads straight to a sample for you to watch.

### Done
- **Strategy:** brought the backup show's code up to date, read its sample (a pass), had it reviewed fresh, and merged it switched off. The review found three things that matter only once it is switched on. I fixed the two real bugs: the AI writing the title could see a slightly reworded question, and one safety-screen outcome went unlogged. A second review found nothing wrong with the fix. I also built the third: a title or closing line that names Reddit, or passes the takes off as people's, is now dropped in code, not only discouraged in the prompt. All of it merges after its own sample, and I checked it also merges cleanly into bet 1's release, with every test passing on the two together.
- **Product:** ran the worked-examples test (4 AI requests; one post hit an overload error and answered on its single retry), had it scored blind, and recorded it. Nothing ships from it. Under the rule set before the test, the host lines get no more trials until you answer #77.
- **Engineering:** built bet 1 without reactions, kept apart from bet 1's release until you choose. A fresh review found two real bugs in my first version: reactions nobody would see could still have cancelled the opening line and the closing pick. Both are fixed and tested.
- **General management:** merging the backup show stopped bet 1's release from merging cleanly into the live code. Our tracker check caught it and I fixed it within the hour (all 1,087 tests pass). I also broke the live code's tests for a few minutes with a tracker wording slip. Neither touched an upload. With nothing left ready, a fresh helper looked for small work that needs no AI allowance, sample or you, and found nothing above the bar. Its one marginal idea, attaching the switch-on change to #90 now, I dropped: your label would apply it, possibly before the backup show's fixes merge and before you have heard it. So I handed over at 11:42.
- **Security and reliability (checked):** this morning's upload landed; the money controls are intact ($0.25 this month, forecast $0.75 of $3); no secret is in the repository; the workflows are unchanged.
- AI use: 4 requests on the upload model, on a day the release check does not spend; the sample used the test model; no Polly.

### Blocked
- **For you, in order:** #77 (bet 1: reply "without reactions", or label it as it stands), #82 (register the Reddit app by 12 January), #88 (one command), #90, #65 (your "yes" to its corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **From about 23:00 UTC tonight**, when the sample limit clears: request the sample of the backup show's fixes, and merge on a pass.
- **On your "without reactions" reply:** fold that version into bet 1's release and request a spoken sample for #77.
- Tomorrow's 08:17 release check re-tests bet 1's release, because its code moved today.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** yes, a little. The backup source is in the live code, and bet 1's last open test is answered, with its next version ready. Nothing new reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
