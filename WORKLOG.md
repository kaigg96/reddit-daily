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

## 2026-11-10 (18:40) — Your three decisions are carried out; the own-questions show's sample video passed, and it can merge switched off after one more check tomorrow

    Worked (% of the shift): gm 30 · strategy 25 · data 25 · legal 10 · security 5 · reliability 5

**Summary:** Your decisions on #91 and #92 are done and closed. #88 needs one command from you, because a shift cannot write its own instruction files. The backup show built on our own questions rendered a playable sample tonight; it is the source that keeps uploads going if Reddit's access ends in January.

### Toward revenue
- **Keeping the channel alive after January, on the one source we could earn from.** The own-questions sample passed: 19 seconds, playable, titled "3 takes on how to spend a free Saturday", crediting no one. The question was as bland as earlier trials. One more sample, of the code exactly as it will merge, is allowed from tomorrow morning; on a pass it merges switched off. Turning it on stays your label (#90), after you have watched a narrated sample.
- **How we will know if it works, set before any of its videos exist:** the first rule under your #91. It is judged on the share of plays past the opening, with watch time as the check. If it does worse and Reddit still works, we switch back; if Reddit has gone, improving its questions becomes the next product work. Either way you hear the same day. Our release check now reports that share for every release, so the rule can actually be read.
- Bet 1 (#77) still waits on you; tomorrow's test is the last fix for its host lines.

### Done
- **General management (your #91):** new tests are now judged on the share of plays that get past the opening, with watch time as the check that viewers aren't worse off. It is in the decisions log and the standing rules; the three tests already running keep theirs. Closed.
- **General management (your #92):** three shifts a day stay. The skipped shifts come from a repository setting only you can change, the weekly shift allowance of 200. I recommended 400 on the issue: it fits three a day, and each shift is already cut off at 70 minutes. Closed.
- **General management (your #88):** the tool that runs shifts refuses any write to the shift instruction files, approved or not, so I posted one exact patch on #88 that you can apply with one command. It also carries #91's two matching lines. Letting shifts make such edits after your label: the tool's documentation says ordinary permissions cannot. One other route might, but testing it here could have billed per use, so I did not.
- **Data (built, live):** the rule above, and the release check's new line. A fresh review caught that my first wording of the rule named a figure our tools never print; it was fixed the same hour, before any data. A second review of the new line found no bugs: it changes no verdict and nothing in the Monday digest. Reporting only, so viewers see nothing.
- **General management (ranking):** with nothing else ready, a fresh helper proposed eight ideas and two more ranked them, forwards and backwards. Both put the rule first and the release-check line second, so I did both. Third was Reddit's reported 10 November reminder to developers: a search found nothing new in it. The rest changed no decision (a merge checklist, a renaming check, comment counts, revenue re-costing), and the rest of tonight's work waits on tomorrow's AI reset, the 12-hour sample limit, or you. So I handed over at 19:15, 25 minutes early.
- **Strategy:** requested and read the sample above, and brought its code up to date with today's live code; all 822 tests pass.
- **Legal:** Reddit's three terms pages are unchanged as of 18:50 UTC (US daytime on the 10th) against the 3 November copies. Its registration page refused our checker. A news site mentions a 10 November "deadline reminder" to developers; if Reddit emailed you today, that is probably it.
- **Reliability and security (checked):** this morning's upload landed; the midday one has not started, as GitHub starts them up to 10 hours late (yesterday's went up at 22:34). Money controls intact ($0.25 this month, forecast $0.75 of $3). No secret in the repository; today's only workflow change is your #93.
- AI use: none from the upload allowance; the sample spent its requests on the test model; no Polly.

### Blocked
- **For you, in order:** #77 (bet 1), #82 (register the Reddit app by 12 January), #88 (one command), #90, #65 (your "yes" to its corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **11 November, after 08:00 UTC:** request the sample of the own-questions code as it will merge, and merge it switched off on a pass. Then the worked-examples test for bet 1's host lines (3 requests), blind-scored, then its rule. Look at Reddit's terms again.
- After that merge, tell #90 how to get a narrated sample on your own machine.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** slightly. The backup source passed its sample and three of your decisions are carried out. Nothing new reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-10 (11:17) — Your "no" on viewer replies is done; the first two fixes for bet 1's host lines failed a blind test, and one more runs tomorrow

    Worked (% of the shift): product 45 · audience 15 · gm 15 · reliability 10 · strategy 10 · security 5

**Summary:** Thanks for your two decisions. The reply job stays off with its queued replies withdrawn, and your label on #93 applied itself this morning. Two fixes for bet 1's host lines failed a blind test; a third runs tomorrow, and #77 now spells out what your label trades.

### Toward revenue
- **Nothing directly.** Bet 1, our main bet on originality, still waits on your label (#77). Today's comment there puts the choice plainly: label it now with weaker host lines, or reply "without reactions".

### Done
- **Audience (your decision on #89):** the reply job stays off, and the three queued replies are withdrawn, so nothing will ever post them. The missed-upload check bundled with it stays off too. Your rule is recorded where any future attempt will see it: first person, never "we", not formulaic, and drafts shown to you first. Our videos' closing line says "us" on 7 of the last 12 and "I" on none; your rule was about replies, so I changed nothing.
- **Product (bet 1's host lines, under the rule set on 8 November):** on the new AI model I tried two fixes on the same three test posts: making it think harder, and a wording that forbids labels. A fresh scorer, not told which line came from which version, found 1 reaction in the 9 lines from 8 November and 0 in 6 for each fix. Thinking harder was also too slow. So nothing ships. Two fresh helpers then ranked what to try next, one reading the list forwards and one backwards. Both put the same two first: showing the model worked examples, and shipping bet 1 without the per-answer reactions. The examples version is built, and reviews found two defects, both fixed. It runs tomorrow under a rule set before any result, scored with today's exact instructions so the two results compare. If it fails, the next shift recommends bet 1 without reactions on #77.
- **Strategy (the source after Reddit):** I could not request its sample video this shift: it would have rendered within an hour of the 12:23 upload slot, which our rules forbid. It still merges cleanly with today's code and passes every test, so tonight's shift can request it.
- **Reliability and security (checked):** all three uploads since yesterday morning landed. The money controls are intact ($0.24 this month, forecast $0.75 of $3). No secret is in the repository, and the only workflow change is your #93 patch, which adds one setting and no new permission. The new model has written all 4 of its uploads' titles without an error; today's overload errors were in my test, which tries only once.
- **General management:** I pushed one tracker edit that broke a test on the live code line for about five minutes. It is fixed; no upload ran in between. The 5 November audit's four process proposals were due to come to you on your return. I am holding them so #77 and #82 get read first. With nothing else runnable, a fresh helper proposed eight more ideas; none cleared the bar (two were already settled in the plan, the rest answered by earlier findings or too thin to read). So I handed over at 11:50, 21 minutes early.
- AI use: 7 of the shift's 8 requests (the test); no Polly; no sample video.

### Blocked
- **For you, in order:** #77 (bet 1; each week past about 20 November costs bet 2 a week at four uploads a day), #82 (register the Reddit app by 12 January or uploads stop), #90, #91, #92, #88, #65 (your "yes" to its corrected sentence), #80, #59.

### Next
- **Tonight (19:17 shift):** request the own-questions sample video; its render copy is ready. The 18:23 slot makes no AI call, so it does not block the request, but check that the late evening upload is not running at that moment.
- **11 November, after 08:00 UTC and an hour clear of an upload** (the 11:17 shift's first minutes, or the 19:17 shift): the worked-examples test (3 requests), blind-scored as today, then its rule. Look at Reddit's terms again the same day.
- **16 November:** the weekly review.

### Better?
- **Than last shift:** slightly. Your two decisions are carried out, and bet 1's host-line question is down to one last test with its fallback already chosen. Nothing reached viewers.
- **Than ~10 shifts ago:** no. Watch time is flat and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
