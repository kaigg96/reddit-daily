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

## 2026-10-27 (09:55) — Both process items you queued last night are built and wait only on your labels; our test record shows "keep" rarely meant "it worked"

    Worked (% of the shift): gm 40 · data 35 · legal 15 · security 5 · reliability 5

**Summary:** The friction log is built and reviewed, and lands when you label #84. The experiment ledger is live: of 7 changes we kept, only 1 measured a gain beyond what its test could tell from noise. Nothing viewers see changed, and nothing moved revenue directly.

### Toward revenue
- **Nothing directly.** Every change that viewers would see still waits on #77 or #80. The channel is flat, so I say plainly that no work today changed what we ship.
- **What the ledger shows, for judging bets.** Of 7 keeps, 1 measured a gain bigger than its test's limit: the background-clip library, +22% against 11%. The product plan already declines to credit opening on the question (+20%), because its lead was mostly longer videos. One keep was inside its limit, and four had no limit recorded. The only "revert" a rule ever gave was overruled by a rule written the next day. So a "keep" has meant "no harm seen", not "it worked". Bet 1's own read can detect a change of about 12% in watch time per view, and views would need about 55%.
- **The 5 November source decision has two more facts.** Stack Exchange's terms bar nothing about running its posts through AI. Opinion polls are a possible third source: Pew's terms allow commercial reuse with credit, and YouGov's do not. A poll gives the crowd's answer as percentages, not quotable answers, so it would be a different show. It is a lead, with no sample.

### Done
- **General management (built to your spec):** the friction log. A shift logs what made each finished item hard, the weekly review groups the entries, and your rule judges it at the first monthly read. Three silent shifts in a row email you. A fresh review found two real bugs and some weaker spots; all fixed, and 637 checks pass. It lands the day you label #84.
- **Data (a bet on the process):** the experiment ledger and a report that reads it. It holds 60 test rules from the product plan and history: when each was set, due and read, and what it found. Of 39 reads, only 9 had a due date (8 on time). Three releases were judged by rules written after they shipped. A fresh review caught that I had credited opening on the question, which the plan says not to; fixed before it went live. **#85** asks you to approve two lines that make the quarterly planning read it and keep it current.
- **Legal (for the 5 November review):** the terms reads above, from archived copies where the live pages gave a script nothing.
- **Reliability:** both of yesterday's uploads and this morning's landed. Bet 1's release still combines cleanly with everything live, and all 870 checks pass together.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, money controls in place ($0.75 this month, forecast $0.88 of $3).
- **General management:** with nothing else ready, a fresh agent proposed six ideas; the two that cleared the bar are the terms reads above. **Dropped:** a trial giving the Stack Exchange host another job (over 20 minutes, and the last two rewordings made things worse); fixing the own-questions show's bland questions (the same, and it shares two of three spam-policy traits); stripping angle brackets from titles (never seen in about 2,300 titles, and it touches code bet 1's release changes); naming bet 3's pilot route (changes nothing until bet 1 keeps). A second round at 09:30 found nothing above the bar: closing two engaged-share rules (never a trigger), the voice read's limit (dropped yesterday), the title test's eighth video (the 2 November read checks it), the reach-cut measure's timing (overlaps a drop, pays off only if fragile), and Christmas inside bet 2's window (no December history to judge it). So I handed over at 09:35 with nothing ready.
- One release merged (the ledger, analysis only); nothing viewers see changed. AI use: none from the upload allowance; no Polly; no render.
- **Process:** I switched the shared copy of the project to another branch while a reviewer was reading the friction-log branch. I switched back within a minute and moved my other work to separate copies. Using separate copies from the start avoids this. I wrote both proposals' rule wording on branches with a script; nothing reaches the rules without your label.

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #84 (one label lands the friction log); #85 (one label adds the ledger to quarterly planning); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **If #84 is labelled:** merge the friction-log branch with the approval line, setting its start time in the same commit (the plan's row says how). **If #85:** merge its proposal branch the same way.
- **2 November snapshot:** the views rule first, then the subreddit test, the title-style test if it has its eighth video, and the voice question. Record each read in the ledger too.
- **If #77 is labelled:** as the last handover says.

### Better?
- **Than last shift:** Unclear for revenue. The process can now see its own record, and it says our "keeps" were mostly not evidence of a gain. That matters before bet 2 is judged.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-26 (23:38) — The guard against shock-bait titles is live; Snapchat and X priced, and neither pays for a reading

    Worked (% of the shift): reliability 25 · gm 25 · monetization 15 · data 15 · security 10 · product 5 · legal 5

**Summary:** The check that refuses shock-bait titles passed its sample video and is live from tomorrow morning's upload. Snapchat's and X's creator programmes are now priced: both pay only for original work, so bet 1 (#77, waiting on your label) still comes first on every route.

### Toward revenue
- **A spam-policy risk is now handled in code.** YouTube refuses content "designed to shock or surprise viewers". A title like "Animals' chilling genius will surprise you" is now replaced by the plain Reddit question before upload. Questions such as "What surprised you most?" still pass. Protection, not growth.
- **Two more routes priced, and neither is nearer.** Snapchat invites creators with 50,000 followers and 15,000 hours watched a month. At our YouTube rate we would have about 37 hours, roughly 400 times short. It also asks for "original" videos of 30 seconds or more; ours run about 21. X now pays only Premium subscribers with 500 verified followers and half a million verified views in 90 days. It excludes "content reuploaded from other platforms". Neither pays for a reading.
- **Bet 1 can still ship the day you label #77.** Combined with tonight's change, all 862 automated checks pass, and its titles go through the new guard.

### Done
- **Reliability and legal (a fix):** the title guard's sample video passed (23 seconds, playable), and the guard merged. Its title, "The most brutal betrayal stories EVER told on Reddit", passed the guard, as it should. Videos look the same.
- **Monetization (a bet-3 read):** the pricing above, now in the company plan; Snapchat's from its own help page, X's from a 3 September report quoting its page, which refused us.
- **Reliability:** both of today's uploads landed (the afternoon one at 18:46, after GitHub's usual queue delay).
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.75 this month, forecast $0.88 of $3).
- **General management:** after the merge nothing was ready. A fresh agent proposed eight ideas and six survived its filter. Two rankers, in opposite orders, ranked the route pricing third both ways; their top pick, a break-even per upload, would repeat the plan's 25 October figure. **Dropped:** whether shock titles were buried more (11 titles, and the answer changes nothing now that the guard is live); a likes measure for bet 1 (it already exists); rewriting the upload description beside bet 1 (the product plan puts it after bet 1); pricing video production for paying clients (speculative, no evidence). A second round, aimed at the 2 and 5 November decisions, found the two rule fixes below. **Dropped from it:** pinning how the tests count uploads (both counts pass by 2 November); bet 2's targets in the views report (its baseline completes on 2 November); one combined email about #77, #80 and #82 (another email); a re-raise date for #82 (escalations already re-raise); the voice read (complete as written); the account-security risk (only your checks move it). A third round, on what could break an upload in the next two weeks, found nothing not already covered (model shutdowns, login expiry, tag lengths, Reddit access, the clock change).
- **Data (a fix, before any bet 1 upload):** bet 1's verdict is now read on AskReddit uploads for as long as two subreddits rotate. The old wording tied it to the subreddit test, which is read on 2 November, before bet 1 can be. Today's format ran on AskReddit alone until 7 October, so a read across both subreddits would credit bet 1 with the mix.
- **Product (a default while #80 is open):** four uploads a day now waits for bet 1 until you answer #80, which recommends exactly that. The plan held both that proposal and "four a day first if bet 1 is late", and the 2 November read could have set off either. Waiting is reversible and spends nothing; to start four a day on time anyway, say so on #80.
- One fix that reached the live pipeline (the guard), two rule fixes and one read for bet 3; nothing viewers see changed. AI use: one sample render (its own allowance); no Polly, no upload-model requests.
- **Process:** the first request for the sample video reached GitHub but got a server error, and no render started. A second request started it within seconds; if no render starts within a minute, request again.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #82 (register our Reddit app by 12 January); #80 (no longer urgent: four a day waits for your answer); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **If #77 is labelled:** merge the release, then the counting fix built beside it (the technical list names both), set the live format to v8 in the product plan, and close #77. Both still combine cleanly with everything live (checked tonight). The next render slot opens at 11:14 UTC on 27 October.
- **2 November snapshot:** the views rule first: if the week is low again (two low weeks running), treat it as YouTube's reach cut and tell you that day. Then the title-style test if it has its eighth video, the subreddit test, and the voice question.

### Better?
- **Than last shift:** Slightly: a policy risk that leaked once is now refused in code, and bet 3's route list is complete for the platforms that pay creators. Nothing changes what viewers watch.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds, and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
