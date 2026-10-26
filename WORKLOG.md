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

## 2026-10-26 (09:55) — Bet 1 can go live the day you label it; the own-questions sample renders now, and carries a policy cost

    Worked (% of the shift): engineering 35 · gm 20 · strategy 15 · reliability 10 · legal 10 · data 5 · security 5

**Summary:** Bet 1 was combined with today's live code in a trial copy: no conflicts, and every check passes, so your label on #77 can reach viewers the same day. The "our own questions" sample could not render before 09:54 (one render per 12 hours) and is queued now; YouTube's spam rules weigh against that show.

### Toward revenue
- **Bet 1 can ship the day you label #77.** Every route to revenue needs it, and it must ship by about 30 October to 6 November for the doubling test to run as planned. The release was combined with everything live since it was built, in a copy never pushed: no conflicts, all 857 automated checks pass, and none reached the internet or spent AI requests. Bet 1 itself is unchanged, so the sample you are judging is what ships.
- **A cost on one of the two Reddit replacements.** YouTube's spam page (read today) gives as its example of mass production "the exact same background music and repetitive AI generated imagery across many videos, with each video reading out an AI-generated script". The own-questions show is a wholly AI-written script over our one music track: two of those three traits, where the Reddit and Stack Exchange shows have one. If you pick it on 5 November, it should ship only with more music and a check that its videos differ, as #80 asks of four a day.

### Done
- **Engineering (a check, for bet 1):** the trial above. The only live change it picks up that touches the video is the 24 October rule holding the capitals test's titles to their arm, and it lands where bet 1 writes titles. At merge, the product plan's live-format line becomes v8. A fresh review of the combination found nothing on the upload path, and two faults in how our reporting tool reads bet 1's results. One, already live, would have pointed a later shift at the wrong group of videos for two of bet 1's pre-set checks: fixed, reviewed, merged (a fix; no video change). The other exists only once bet 1 merges: it would count bet 1's on-screen lines over uploads its verdict never reads. Which uploads that count covers is now set in advance, before any bet 1 upload, and its fix is built, reviewed and waiting beside bet 1, to merge right after it.
- **Strategy:** asked for the own-questions render at 08:56; refused, as last night's Stack Exchange render (21:53) holds the slot for 12 hours. Re-queued at 09:54; it renders after this shift.
- **Legal (a check):** the spam-policy reading above, recorded with the source comparison for 5 November.
- **General management:** one item was ready. A fresh agent proposed eight ideas, five survived; two rankers, in opposite orders, put the same one first (the bet 1 trial) and said nothing else cleared the bar. A second round aimed at the functions with no time in twenty shifts (distribution, audience, monetization, finance) found one, the policy cost above. **Dropped:** a one-page comparison of the replacements (mostly written, and the review packet writes it); drafting the rule bundle for 5 November early (nothing gained); the Stack Exchange licence credit on its sample (never published); counting advice-style questions (any change waits weeks for bet 1's read); a warning before a render request is refused (the refusal came in 20 seconds); a traffic-source report (search is flat at 2–3%, which changes nothing).
- **Reliability:** this morning's upload and both of yesterday's landed. This morning the title model failed twice ("overloaded") and the backup model wrote the title, keywords and closing line: the first live rescue by the 18 October fix. The capitals test holds since its 24 October fix (one capitalised word on every such title). GitHub has not yet moved our uploads to its new server image (due by 19 November).
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, money controls in place ($0.74 this month, forecast $0.88 of $3).
- Mostly checks, and one fix to the reporting tool; nothing viewers see changed. AI use: none from the upload allowance (the render after this shift uses the free sample model); no Polly.
- **Process:** last night's handover said to render "after 07:00", but the 12-hour limit held the slot until 09:54. A handover naming a render should give the time the limit allows.

### Blocked
- **For you, in order:** #77 (one label ships bet 1, the same day); #82 (register our Reddit app by 12 January); #80 (one label, by about 1 November); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **Read the own-questions render** (verdict about 10:05) into the source comparison for 5 November. The next automated render is not before about 22:00.
- **Today's weekly snapshot** (it has landed between 11:20 and 13:50 for five weeks): the weekly review, the opening-reach read, and the title-style test, whose sample is now large enough (19 "You…" titles against 8 others reach 7 days old).
- **If #77 is labelled:** merge the release branch (still at its tested commit), then the dose-count fix beside it, set the live format to v8 in the product plan, and close #77.

### Better?
- **Than last shift:** Slightly: bet 1 is shown to merge with today's live code, so a label reaches viewers the same day. Nothing new reached viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. For the Reddit deadline, both replacements are built, one rendered, and one now has a known policy cost.
- **Than ~100 shifts ago:** Too early to say.
