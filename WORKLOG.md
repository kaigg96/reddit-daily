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

## 2026-11-14 (17:45) — Watch time is falling inside our main subreddit, which would have tilted bet 1's verdict; the Reddit cutoff now fails safely, by test

    Worked (% of the shift): data 35 · reliability 25 · strategy 15 · gm 25

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). This shift found that watch time inside AskReddit has fallen from 12 to 10 seconds while the channel as a whole reads flat, and set bet 1's read to show that beside its verdict, so a falling baseline cannot pass for a failed bet.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. The nearest thing: bet 1's verdict is the one decision on our way to revenue, and it was at risk of a false "revert" (below). Bet 1 still merges cleanly into today's live code, with all 1,150 tests passing.

### Done
- **Data (a question answered: yes, falling):** bet 1 is judged on AskReddit uploads against the earlier versions' AskReddit uploads, pooled. I set the rule and saved it before looking. Our reporting tool reads AskReddit's watch time at a week old as falling, 12 to 10 seconds since mid-October, beyond its usual 1-second drift, while the channel overall reads flat (12 to 11), so our second subreddit is holding up better. Recent weeks are thinner, 7–8 AskReddit uploads each, since the two subreddits share the slots. So a baseline pooled from the better weeks would make bet 1 look worse than it is. Its rule is unchanged; if its read says revert, it now prints a comparison with the same recent weeks beside it, never as the trigger.
- **Data (a question answered: no):** could a topic now justify reopening the parked idea of choosing posts by topic? Its bar is a 50% lead. The best-placed topic, politics and news, leads by 27%, and our tool refused the comparison because those videos are younger. It stays parked.
- **Reliability (a safeguard for 12 January):** if the Reddit app is not registered by then, Reddit will refuse our requests. A new test proves such a refusal stops the run before it pays for narration, writes a title, uploads, or touches the record of what was last posted, whether the refusal comes on the list of posts or later, after the safety check has spent a request. A fresh reviewer found the first version could pass without ever reaching Reddit; fixed.
- **Strategy (a decision for the backup show):** the check that stops our own-questions show's titles passing AI-written takes off as real people's has leaked through three rounds of word lists. I chose its replacement: a separate AI check of each title, refusing when in doubt, because on our channel a separate check works where instructions inside the writing request do not (bet 1's reactions). One request per video; it fits the daily allowance at two or four a day. Recorded for whoever builds it.
- **Data (record-keeping):** our list of experiments and their rules now has a test holding it in one consistent form. Adding it found a row whose last cell had split in two, losing part of its references; repaired, nothing else changed.
- **General management (ranking):** a fresh helper proposed six ideas; two others ranked them forwards and reversed, and the top two agreed. I did five of the six in that order. Dropped: what our viewers' countries imply for pay per 1,000 views (it changes no decision while we are this far from any paid tier).
- **Security and reliability (checked):** both of yesterday's uploads and this morning's landed. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; no workflow change since 11 November.
- AI use: none of Google's allowance; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65 (waits on your yes to the corrected sentence), #80, #59, and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging.
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and today's lead: AskReddit's watch time is falling while our second subreddit holds.
- **About 18 November:** the new model's 20th video and its title counts. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read.

### Better?
- **Than last shift:** no, not toward revenue. Bet 1's eventual verdict is safer from a false revert, and the Reddit cutoff can no longer cost money or a duplicate upload.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, falling inside AskReddit, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-14 (10:56) — If your label on bet 1 lands early, the new AI model's checks already have their rule; Reddit closing its feeds does not touch us

    Worked (% of the shift): gm 40 · data 25 · engineering 10 · legal 10 · security 5 · editorial 5 · monetization 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every change to the videos still waits on your label on bet 1 (#77). This shift settled in advance how the new AI model's checks are counted if that label lands before the model's 20th video, and confirmed that Reddit closing its feeds yesterday leaves our uploads untouched.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. When it comes, the shift that merges it has nothing left to decide first: the rule below covered the one open case.

### Done
- **Data (a rule set before its read):** your label merges bet 1 straight away, on top of the new AI model that went live on 8 November. That model's own checks (watch time, and how often its titles fail or claim more than the question) each count its first 20 videos, and it has 12. A label before the 20th would have left them short and open to argument. Now, before any is read: its watch time reads "too few to tell", and bet 1 keeps the comparison chosen on 10 November, saying beside its verdict that this check never ran. The title checks count the model's first 20 videos, bet 1's included, since the same model writes the titles with the same wording. A fresh helper found two counts my first draft missed, and that bet 1's closing lines come from a different instruction; all six of its fixes are in.
- **Legal (checked, no change):** Reddit ended its feeds yesterday and had already shut its open data pages to logged-out readers. We read Reddit through our registered app's own keys, so neither touches us. The 12 January registration date (#82) is unchanged, and #82 already holds the answers to give.
- **Editorial (checked, no fault):** the 12 November video asking why "Jensen" was fired over an affair is about real news: Nvidia's chief executive resigned that day, four days after admitting an affair. Our safety check did not let an unproven claim about a named person through.
- **Monetization (checked, no change):** nothing new on YouTube's Partner Program bar or its rules on mass-produced content beyond what we already hold.
- **Engineering (two notes corrected for later shifts):** the suggested fix for the backup show's title check could not work, because the check it named runs before the title is written; the note now lists the two that can. The plan to move our AI to Groq assumed a short reaction after each answer. If bet 1 ships without them, Groq must first be tried on the host lines that remain, when that plan comes up.
- **Security and reliability (checked):** yesterday's two uploads and this morning's landed. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; the only workflow change this week was #93, which you approved.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed, with the same order both ways. Dropped: trimming your list of open asks (you have been away 91 hours, past your longest usual gap, and our rule then is no re-asking; #77 already states its dates); proposing the backup show on a new channel (already set to follow bet 1); re-reading our second subreddit on plays past the opening (read on 2 November under its own rule); a rule for when to change course (the plan is at its length limit, and the quarterly review owns that); search traffic (under 2% of views); a stock-footage list (your open task is music). Two more rounds found the bet 1 rule and the two notes above, and nothing else above the bar, so I handed over at 10:56, 29 minutes early.
- AI use: none of Google's allowance; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65 (the sentence you approved is out of date; it waits on your yes to the corrected one), #80, #59, and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging; count the new model's checks by today's rule.
- **16 November, the weekly review:** the buried-upload rule, the weekly swings question, and the lead that the fall may sit in our most-played videos.
- **About 18 November:** the new model's 20th video and its title counts. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals read.

### Better?
- **Than last shift:** no, not toward revenue. The day your label arrives now needs no decision, and one threat to our source is ruled out.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

