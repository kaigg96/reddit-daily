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

---

## 2026-11-14 (00:59) — The fall in plays past the opening is smaller per video than we reported, but real per play; YouTube tests a way back from some spam bans

    Worked (% of the shift): data 45 · gm 15 · security 10 · market 15 · legal 10 · reliability 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every step that changes the videos still waits on you, bet 1 (#77) first. Tonight found that a few barely-shown videos inflated our figure for the fall in plays past the opening, though per play the fall is real, fixed in advance how much the capitals test can explain, and recorded a YouTube test that gives some spam bans a 30-day way back.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. Per play, which is how YouTube's paid tier counts, the share past the opening did fall, by 9 points, and counted plays per upload fell about a sixth after 19 October (below).

### Done
- **Data (a rule set before its read):** the capitals test is read about 23 November. It began four days before the fall, so its timing fits. Before its result is seen, I fixed how much of the fall it could explain. Titles with a capitalised word rose from 38 to 50 in 100 uploads, so capitals explain a quarter of the fall only if the capitalised half trails by 22 points or more, a very large gap. A fresh helper confirmed the figures; its two fixes are in. A related rule got its missing due date.
- **Data (a question answered: partly barely-shown videos):** the 10.6-point fall averaged every video's share, including videos shown a handful of times, where 2 plays of 3 reads as 67%. I set a rule first, then left out videos under 10 plays, 4 in each period. The fall shrank to 4.5 points (38 to 34 in 100), which by the rule makes barely-shown videos most of it: a lead for Monday, thin at 26 videos. Per play, though, the scorecard still shows 43 to 34 in 100; barely-shown videos have too few plays to move it. So the per-play fall is real, and may sit in our most-played videos: the week of 26 October had our most plays per upload and lowest share. Counted plays per upload averaged 84 after 19 October against 100 before. A fresh helper reviewed it; its fixes are in.
- **Market intelligence (answered: no change found):** outside sources report no YouTube change to how plays are counted near 19 October. On 22 October YouTube moved Subscriptions out of the phone app's bottom bar; our subscriber traffic is 0–1 views a week, and whether it sent casual viewers to Shorts our data can't tell.
- **Legal (risk register updated):** since 29 October YouTube has been testing a 30-day lock before some spam-policy bans. Uploads stop; the channel can fix or delete the videos, or appeal; deleting every video unlocks it and keeps the subscribers. It is a limited test, so the risk stays fatal. It doesn't change my advice on #80 (four a day waits for bet 1).
- **Security (checked, nothing new):** I scanned our public repository's whole history for leaked keys inside files; our automatic check looks only at file names. It found only a test's fake keys and the two dead Google tokens already on the 7 December list.
- **General management (ranking):** a fresh helper proposed eight ideas; two others ranked them forwards and reversed, and I did the three that placed well both ways. Dropped: a rule to stop hunting the fall's cause if counted plays held (the rankings split, and rising plays can hide a loss); re-checking the fall on videos read at the same age (split, and too long); viewers' countries (needs YouTube access shifts lack). A second round of six used tonight's evidence, and the spam-lock note topped it both ways. Dropped: testing the extra-brief-plays lead or setting one for 7 December (I had seen the data); a plan for a lock notice (those reach you, not shifts); YouTube's 16 October Shorts bonus pilot (invite-only, for Partner Program members). A third look found the bet 1 merge check and the barely-shown test. Nothing else cleared the bar, so I handed over at 00:59, 20 minutes early.
- **Security and reliability (checked):** both of yesterday's uploads landed; two very short runs were the normal skips. Bet 1 and its two follow-on fixes still merge cleanly into tonight's live code, and all 1,147 tests pass on the result. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; workflows unchanged.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label; its sample, review and automatic check all passed), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging, before four a day.
- **16 November, the weekly review:** the buried-upload rule set on 13 November, the weekly swings question, and tonight's lead that the fall may sit in our most-played videos. Unless a field we log explains it, I'd stop hunting its cause: bet 1 is the answer either way.
- **About 18 November:** the new model's 20th upload and its title counts. **20 November:** if bet 1 is still unmerged, update #80, mentioning YouTube's spam-lock test. **23 November:** the capitals read, with tonight's rule.

### Better?
- **Than last shift:** no, not toward revenue. Our figure for the fall past the opening is now honest per video and per play, and the fatal risk has a recorded way back.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
