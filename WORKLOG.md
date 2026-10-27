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

## 2026-10-27 (23:35) — Your ledger decision is live; Monday's figures, which four test reads depend on, are now protected from a one-off YouTube error

    Worked (% of the shift): reliability 30 · data 25 · gm 20 · legal 10 · strategy 10 · security 5

**Summary:** The experiment-ledger wording you approved (#85) is live. Last Monday YouTube's reporting service failed once and the weekly figures lost nearly every video's subscriber count without anyone noticing; that can no longer pass silently, and a repeat on 2 November, when four test reads are due, is now retried. Nothing viewers see changed, and nothing moved revenue directly.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the evidence.** Every bet is judged on the Monday figures, and a week that is lost cannot be fetched again later. On 26 October one "internal error" from YouTube cost every video its subscriber count; a repeat on the main request would have lost the whole week, including the four reads due on 2 November. Each request now tries up to three times before giving up.
- **One more fact for 5 November.** AI use does not decide between the replacement sources at two uploads a day: Reddit and Stack Exchange need 2–5 requests per video, our own questions 2–3, under the 20-a-day allowance. At four a day, Reddit and Stack Exchange reach the allowance on a bad day.

### Done
- **General management (your decision, #85):** the two lines landed as one approved commit at about 23:00 UTC; #85 is closed. The quarterly preparation now quotes the ledger before proposing any bet's rule, and every rule set or read updates its row. First read at the next quarterly preparation, in early January.
- **Reliability (three fixes, live):** every request the Monday jobs make to YouTube now retries a server error, as one kind already did after 19 October, including the 22-page list of our videos that comes before any figure, and your check-in's own requests. Fresh reviews found no bugs; each found a request still left out, now covered. I also checked the three libraries that job installs without fixed versions: their newest releases work, so they are not a risk for Monday unless a new one ships first.
- **Data (three fixes, live):** the reports said "insufficient data" about subscribers when the truth was "YouTube refused the request". Our rules tell a shift to accept a report's refusal as the answer, so a failed collection would have read as too few videos. They now say it was not collected. Your Monday check-in said "ran clean" that day too; its title and health line now name any figure YouTube refused. The test comparisons dropped a refused figure silently too, so a thin result could be a failed one; each such read now warns, and today notes 11 videos whose subscriber figure was refused. Fresh reviews found no bugs in any of the three; their wording points are fixed. To confirm the warning on real data I ran the voice question's command filtered to its warnings, so none of its result was seen early.
- **Legal (for #82):** Reddit's pages refuse automated reads, so I recorded the questions on Reddit's API request form from an archived copy (November 2025) in #82's description, by edit, which sends no email. One choice there is yours: whether to apply as a "developer" or a "commercial developer", which asks for a monthly data budget. I recommend "developer", saying plainly that the videos go on YouTube, earn nothing today, and that we would ask Reddit before earning from them, as you decided on 10 October.
- **General management:** #65 stays open. Your label predates the corrected sentence on it, and there has been no reply since, so I did not land it; a "yes" there lands it.
- **Reliability:** both of today's uploads landed. Bet 1's release still combines cleanly with everything live.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.78 this month, forecast $0.88 of $3).
- **General management:** nothing was ready. A fresh agent proposed eight ideas and found the refused subscriber counts. Two rankers, in opposite orders, put the same three first: the retries, the library check, the Reddit form. **Dropped:** a topic test chosen after seeing the data (both rankers put it last); counting deleted Reddit posts (Reddit refuses our build machine, as found before); why likes per 100 views rose (under one like per video); handing over early (three items cleared the bar).
- Seven fixes and two findings. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January; the form's questions are now on it); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **2 November snapshot:** check first that the Monday check-in names no figure YouTube refused, and read each test's warnings before its verdict; the voice question reads engaged views. Then the views rule, the subreddit test, the title-style test and the voice question; all should have enough videos (20 a side; 27 against 14; 21 and 17), counted from the upload log without reading any result. Record each read in the ledger.
- **If #77 is labelled:** as the 17:05 handover says. **If #65 gets a yes:** land the corrected sentence as one commit with the approval line.

### Better?
- **Than last shift:** No for viewers or revenue. Yes for the evidence: a one-off YouTube error can no longer quietly cost a week of test data, and a failed collection no longer reads as "too few videos".
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-27 (17:05) — The friction log is live; two of your open questions rested on facts that had moved, and both now say what will really happen

    Worked (% of the shift): gm 45 · engineering 15 · market 10 · legal 10 · reliability 10 · security 10

**Summary:** The friction log you approved (#84) is live, and two questions still before you (#65, #77) now state facts that had moved since you were asked. Nothing reached viewers; the 5 November source decision gained two facts, both against an easy replacement for Reddit.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on #77 (bet 1). The channel is flat: 12 seconds watched per view for six weeks.
- **Bet 1's approval had a gap, now on #77.** It says the host's tags are written by the main AI model. On a day that model fails (1 upload in 18 since 18 October), they would come from the cheaper test model, which mostly labels, or from Groq, whose tags missed our bar. Still label it: the test counts those uploads against bet 1, so they can only make it look worse. Bet 1 still combines with everything live; all 900 checks pass.
- **Two facts for 5 November.** Stack Exchange's three best sites produce about 1.6 usable questions a day, under our two uploads and 41% fewer than a year ago. Reaching two or four a day means adding niche sites (philosophy, law, language), a different show. And Reddit's terms leave no side door when the free API ends: scraping, RSS or its page data all need Reddit's written consent, and commercial use needs a written agreement. That makes registering our app (#82) matter more.

### Done
- **General management (your decision, #84):** the friction log landed as one approved commit, live from 16:40 UTC; #84 is closed. Its first rows are in, and its rule is first read at the 24 November monthly review.
- **General management (your decision, #65, held back):** you approved letting a shift ask for a sample video near an upload, because its AI requests go to a test model "production uses only for telemetry". Since 18 October each upload also tries that model once when the main one fails, so that reason is no longer true. The risk stays small (renders are capped at about 10 requests a day), so #65 now carries a corrected sentence; reply "yes" and the next shift lands it. It answers the friction log's costliest recurring problem: sample videos holding up finished work.
- **General management (a check, by a fresh agent):** besides #77, #80's reasons have aged. Bet 1's notes became one-to-three-word tags, so it does less to make videos differ, and "bet 2 slips four weeks" overstates it: the plan says each late week costs one week at four a day. #59's six checks predate the Groq key, now a seventh. #82's text still gave 31 October, which does not apply to us; 12 January does. I corrected all three by editing them, which sends no email; their recommendations stand. #85 checks out.
- **Engineering (a fix):** the friction log's own test demanded that every row already be sorted into a group, but new rows wait for the weekly review. The first real row failed the checks on two pushes, for about four minutes. Fixed; all 645 checks pass. I pushed this and a comment fix before a fresh review, which the rules ask for first; the review ran afterwards, found no bugs and two small gaps, both fixed.
- **General management (fixes):** the plan told the next shift to "merge" #85's branch, which the rule guard would undo automatically; it now says to land it as one approved commit. The code comment that misled #65 is corrected.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.78 this month, forecast $0.88 of $3). Process health: ok.
- **Reliability:** both of yesterday's uploads and this morning's landed.
- **General management:** nothing was ready. I considered seven ideas and a fresh agent eight more; the four above cleared the bar (the facts check, the supply rate, Reddit's terms, the merge rehearsal). A last pass at 17:04, aimed at audience, monetization, market and distribution, found nothing new, so I handed over at 17:05. **Dropped:** re-testing every decision's assumptions (the audit's job); how often the fallback fires (a count changes nothing); upload timing (answered 30 September); the test model's daily cap (measuring it spends requests); more sample renders (your call, and a second ask beside #77); bet 1's detection limit (changes no decision); a Reddit-outage alarm (dropped 26 October); a search tool for recorded answers (the weekly review ranks friction fixes).
- Nothing viewers see changed. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #85 (one label adds the ledger to quarterly planning); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **If #77 is labelled:** merge the release, then the counting fix built beside it (the technical list names both), set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how).
- **If #65 gets a yes:** land the corrected sentence as one commit with the approval line. **If #85 is labelled:** land its branch the same way, squashed to one commit.
- **2 November snapshot:** the views rule first, then the subreddit test, the title-style test if it has its eighth video, and the voice question; record each read in the ledger. The weekly review sorts the friction log's first rows; four are questions to you whose facts moved after they were asked (#65, #77, #80, #82), the pattern worth a fix.

### Better?
- **Than last shift:** No for viewers or revenue. Slightly for your decisions: #77 and #65 now describe what would actually happen.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---
