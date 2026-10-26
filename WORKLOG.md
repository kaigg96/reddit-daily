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

## 2026-10-26 (18:12) — Weekly review: views fell fourfold, inside a pattern of alternating weeks; a background clip that buried videos is retired

    Worked (% of the shift): data 25 · product 15 · gm 15 · legal 10 · strategy 10 · reliability 10 · distribution 5 · market 5 · security 5

**Summary:** The weekly review retired a background clip that hid videos, recorded the second Reddit-replacement sample, and built a check against shock-bait titles (live after its sample video). Views fell fourfold this week, but they have alternated low and high weekly for two months, so a rule set today reads next Monday's figures before anyone acts.

### Toward revenue
- **A small step for viewers.** The retired clip left 6 of its 21 videos at 5 views or fewer, against about 1 in 20 for the other clips. It no longer appears. Its watch time per view was normal, so YouTube was not showing those videos; viewers were not leaving them.
- **The views drop, read carefully.** The Shorts feed sent 363 views this week, against 1,243 to 2,902 in the three weeks before. YouTube's announced cut for "unoriginal" channels would look like this. But the feed has alternated low and high every week since early September, and two-week totals are much steadier. If next Monday is low again (two low weeks running, for the first time), the next shift treats it as a reach cut and tells you that day. Bet 1 (#77) is the response either way. I queued an email to you about this, then withdrew it before it went out once I saw the alternation.
- **A guard on the spam-policy risk, built, not yet live.** YouTube's rules refuse content "designed to shock or surprise viewers"; our instructions to the AI ban such titles, but "Animals' chilling genius will surprise you" went out on 20 October. Titles like that are now refused in code and replaced by the plain Reddit question; questions like "What surprised you most?" still pass. It goes live after a sample video, which the 12-hour limit allows from 22:00 tonight.

### Done
- **Legal and engineering (a fix, from a second round of ideas aimed at the quieter functions):** the title guard above. Of our 199 published titles it would have refused 11, all shock titles. A fresh review found gaps (missed wordings; a word the asker used); all fixed. It combines cleanly with bet 1.
- **Data:** the opening-reach question reads as noise: how many viewers get past a video's opening does not predict its views. Closed. A new question, set before its data: is the weekly alternation real viewers or how YouTube's figures arrive? Read on 16 November.
- **Product (a fix, under a rule set 6 October):** the clip retirement above, after a fresh review (one miscount fixed) and a test video. Not yet due: the title-style test (one video short) and the subreddit test (three short on one side).
- **Strategy:** the "our own questions" sample plays, at 18.8 seconds. Its question was bland again ("What's the best way to relax after a long day?"). Both replacement samples are now recorded for the 5 November review.
- **Reliability:** all 15 uploads since last Monday landed with titles. This afternoon's upload had not started by 18:10: GitHub's queue is running it nearly 6 hours late. It has landed as late as 18:48 before.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.75 this month, forecast $0.88 of $3). The dependency scan shows the same two known libraries (66 advisories), still unreachable.
- **Market:** YouTube still gives no start date for the reach cut, and outside reports say Studio has no page that would show one.
- **Audience:** one viewer comment this week, so the reply pipeline stays parked.
- **General management:** after the review nothing was ready. I proposed nine ideas; two separate rankers, in opposite orders, put the same one first: a two-week column in our views report, so one low week is not misread again. Built, reviewed and merged (a fix; nothing viewers see). I also refreshed the plan's distance to revenue: 757 times short of the Partner Program's views bar (720 last week), 22 subscribers. **Dropped:** recording when YouTube's figures actually run to (the new question says first whether timing is the cause); a tool to read bet 1's host lines (premature until you label it); new background clips (they would wait weeks for bet 1's read); a one-page re-pitch of bet 1 (#77 already asks, and it would spend your attention); checking whether similar channels' views fell this week (the stats site refused us; channel pages show lifetime totals); a missed-upload alert (one miss in 72 days, and shifts check three times a day); drafting the 5 November review now (Monday's figures would redraft it); splitting this week's low by test group (it reads experiments early, on too few videos).
- One change viewers see today (the clip), one waiting on its sample video (the title guard); the rest were reads and records. AI use: none from the upload allowance; no Polly.
- **Process:** I nearly emailed you about a single week's low. The weekly review reads views on a scorecard of three-week groups, and nothing showed the weekly alternation. Our views report now prints a two-week figure beside each week, with a note to read lows against it.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #82 (register our Reddit app by 12 January); #80 (one label, by about 1 November); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **The title guard:** ask for its sample video from 21:58 UTC, and merge it if that passes.
- **2 November snapshot:** the views rule above, first; then the title-style test if it has its eighth video, the subreddit test, and the voice question.
- **If this afternoon's upload has not landed** by the next shift, that is an incident: the next scheduled upload is about 05:00.
- **If #77 is labelled:** merge as this morning's handover says. Bet 1's release still combines cleanly with today's changes (checked this evening).

### Better?
- **Than last shift:** Slightly: one clip that hid videos is gone, and the Reddit replacement decision has both its samples. Nothing larger reached viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds, views had their lowest week on record, and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
