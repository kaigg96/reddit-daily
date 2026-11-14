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

## 2026-11-14 (00:50) — The capitals test can't be stretched to explain the fall in plays past the opening; YouTube now tests a way back from some spam bans

    Worked (% of the shift): data 35 · gm 20 · security 15 · market 15 · legal 10 · reliability 5

**Summary:** Nothing reached viewers, so the company is no closer to revenue: every step that changes the videos still waits on you, bet 1 (#77) first. Tonight fixed in advance how much of the fall in plays past the opening the capitals test can be blamed for, found no leaked keys anywhere in our history, and recorded a YouTube test that gives some spam bans a 30-day way back.

### Toward revenue
- **Nothing directly**, because bet 1 still waits on your label. One lead touches revenue: the plays YouTube counts toward its Partner Program (those past the opening) have not fallen per upload, even though their share of all plays has. If that holds, the fall costs less than it looked; it is only a lead (below).

### Done
- **Data (a rule set before its read):** the capitals test is read about 23 November. It began four days before the fall started, so it is the one suspect of ours whose timing fits. Before its result is seen, I fixed how much of the fall it could explain. Titles with a capitalised word rose from 38 to 50 in 100 uploads, so capitals explain a quarter of the fall only if the capitalised half trails by 22 points or more, a very large gap. A fresh helper confirmed the figures; its two fixes, which rule out a convenient reading, are in. I also gave a related rule its missing due date, so a missed read will show up.
- **Data (a lead for Monday):** the week of 26 October had the most plays per upload we have ever had, the lowest share past the opening, and per-upload counted plays tied with our best of the last five weeks. So the fall may be extra brief plays, not lost viewers. Our report tool can't compare it until about 30 November, and an October finding saw no such link video by video.
- **Market intelligence (answered: no change found):** outside sources report no YouTube change to how plays are counted near 19 October. On 22 October YouTube moved Subscriptions out of the phone app's bottom bar and launched AI-built custom feeds in the US. Our subscriber traffic is 0–1 views a week, and whether the move sent more casual viewers to Shorts our data can't tell. A "no" from outside sources is weak evidence.
- **Legal (risk register updated):** since 29 October YouTube has been testing a 30-day lock before some spam-policy bans. Uploads stop; the channel can fix or delete the videos, or appeal; deleting every video unlocks it and keeps the subscribers. It is a limited test, so the risk stays fatal, but it is a first way back. It doesn't change my advice on #80 (four a day waits for bet 1).
- **Security (checked, nothing new):** I scanned our public repository's whole history for leaked keys inside files; our automatic check looks only at file names. It found only a test's fake keys and the two dead Google tokens already on the 7 December list.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. The capitals rule came in both top twos, and the history scan and outside-sources check sat mid-table both ways, so I did those three. Dropped: a rule to stop hunting the fall's cause if counted plays held (the rankings split, and rising plays can hide a loss); re-checking the fall on videos read at the same age (split, and too long); viewers' countries (needs YouTube access shifts lack); trimming the findings record (already under its limit). A second round of six used tonight's evidence, and the spam-lock note topped it both ways. Dropped: testing the extra-brief-plays lead now or setting a test for 7 December (I had already seen the data, so any rule would fit it); a plan for a lock notice (those reach you, not shifts); YouTube's 16 October Shorts bonus pilot (invite-only, for Partner Program members). A third look found only the bet 1 merge check.
- **Security and reliability (checked):** both of yesterday's uploads landed; two very short runs were the normal skips. Bet 1 and its two follow-on fixes still merge cleanly into tonight's live code, and all 1,147 tests pass on the result. Money controls intact ($0.33 this month, forecast $0.78 of $3); no secret committed; workflows unchanged.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label; its sample, review and automatic check all passed), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away, then the verdict-counting fix, then the time-slot logging, before four a day.
- **16 November, the weekly review:** the buried-upload rule set on 13 November, the weekly swings question, and tonight's lead on counted plays. If no field we log explains the fall, I'd stop hunting its cause: a fall of a quarter doesn't change being ~690 times short, and bet 1 is the answer either way.
- **About 18 November:** the new model's 20th upload and its title counts. **20 November:** if bet 1 is still unmerged, update #80, mentioning YouTube's spam-lock test. **23 November:** the capitals read, with tonight's rule.

### Better?
- **Than last shift:** no, not toward revenue. The capitals read can no longer be stretched to explain the fall, and the fatal risk now has a recorded way back.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-13 (19:08) — The fall in plays that get past the opening is not in anything we choose; five suspects ruled out

    Worked (% of the shift): data 55 · gm 25 · reliability 10 · engineering 5 · security 5

**Summary:** Fewer viewers now get past each video's opening (about 40 in 100 before 19 October, 30 since). Tonight's tests show the fall is the same whatever the topic, subreddit, voice or format. That points at the opening itself, which bet 1 changes, or at YouTube. Nothing reached viewers, so the company is no closer to revenue tonight.

### Toward revenue
- **Nothing directly.** Every step that changes the videos still waits on you, bet 1 (#77) first. Plays past the opening are the units YouTube's paid tier counts, so their fall matters to every revenue route. Tonight ruled out the explanations that are ours to choose: the fall happens inside every topic and both subreddits. Bet 1 is the one ready change that touches the opening.

### Done
- **Data (a question answered: no):** does a change in our topic mix explain the fall? I set the rule and saved it before looking. The share fell from 40.6 to 30.0 in 100, and the mix of topics accounts for none of it. It fell inside each topic group. With only two topics common enough to test alone, the read is coarse.
- **Data (a question answered: no):** the same test by subreddit. Our second subreddit's share of uploads doubled over the same weeks, which made it the likeliest cause. It isn't: the share fell inside both (39 to 30, and 43 to 30). The voice mix shifted a little too. By the figures we already hold, that explains about 1 point of the 10, without touching the voice test that is still sealed. The video format was the same in both periods, so it isn't that either.
- **Data (a question answered: too rare to matter):** are reworded repeats of earlier questions buried more often? Only 3 of 219 uploads repeat an earlier question, too few to test and too few to explain the buried uploads. Two are word-for-word repeats from July and August, from before we refused every past title.
- **Reliability (a check, all clear):** the missed-upload alarm waiting for your December bundle would not have raised a false alarm at any of the 129 scheduled shifts since 20 September, even with GitHub starting jobs hours late. It fired only on the one real miss, 6 October. Its closest call was 26.7 hours of its 28-hour window, which I noted so the check is re-run before it lands.
- **Data (a rule set for Monday's review):** whether video length, rank in the candidate list or title style explains the rise in buried uploads. Set before Monday's figures arrive, with a stricter bar because it runs three tests.
- **Engineering (bet 1's path kept clear):** tonight's changes touched files bet 1 also changes. I checked that bet 1 and its two follow-on fixes still merge into the live code cleanly, and that all 1,147 tests pass on the result. So your label still needs nothing else.
- **General management:** the code-findings list was one over its limit for several shifts. It is back at the limit: I moved a finished item's note into the code it describes. All 870 tests pass, and a fresh helper reviewed each change before it merged.
- **General management (your approvals):** I tried again to apply #88's approved text. The tool that runs shifts still refuses to edit those files, so it stays with you; the patch on the issue still applies cleanly. #65 still waits on your "yes" to its corrected sentence. On #88 a shift promised to look for a safe way to let shifts land approved changes to those files. There isn't one: the lock sits outside the tool's permission settings, and the only way past it turns off every permission check for the whole shift. I don't recommend that, so those changes stay one command for you.
- **General management (ranking):** a fresh helper proposed eight ideas, and two others ranked them forwards and reversed. Both orders agreed, and I did all four survivors in that order. Dropped: late-running jobs as a cause of buried uploads (lateness now moves with the calendar, so there is no fair comparison); pinning our build steps to exact versions (only you can land it); counting deleted Reddit posts (it needs Reddit calls); whether closing lines draw comments (no viewer has commented on the last 20 uploads). A second round at 18:57 found only the findings-list fix. It dropped: a note on an old library (live security debt, not a finished item); the sample-video reset hour (dropped 8 November, and it would not close); pre-testing library updates (done 28 October); a risk row for late jobs (already recorded); and the approval guard (a file only you can change). I found the subreddit test myself after that, and two checks that needed only counts: voice and format, above. I also checked whether shifts could safely be allowed to land your approved rule texts (above). Nothing else cleared the bar, so I handed over at 19:08, 23 minutes early.
- **Security and reliability (checked):** this morning's upload landed; the evening one had not yet run by 19:05, which is normal now that GitHub starts jobs hours late. The money controls are intact ($0.33 this month, forecast $0.78 of $3). No secret is in the repository, and the workflows are unchanged.
- AI use: none; no sample video; no Polly.

### Blocked
- **For you, in order:** #77 (one label; its sample, review and today's automatic check all passed), #82 (register the Reddit app by 12 January), #88 (one command), #95 (one label), #90, #65, #80, #59 (five minutes for the two checks that matter), and the shift allowance setting (on #92).

### Next
- **If #77 is labelled:** merge bet 1 straight away. Today's automatic check passed on the sampled version. Then the verdict-counting fix, then the time-slot logging, before four a day.
- **16 November, the weekly review:** read the buried-upload rule set tonight, with the weekly swings question, on that day's figures.
- **About 18 November:** the new model's 20th upload and its counts. **20 November:** if bet 1 is still unmerged, update #80. **23 November:** the capitals test's read, if its lock opens.

### Better?
- **Than last shift:** no, not toward revenue. We now know the fall past the opening isn't in what we pick, which points the fix at the opening itself.
- **Than ~10 shifts ago:** no. Watch time is flat at 11 seconds, and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.
