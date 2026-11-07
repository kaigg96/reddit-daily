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

## 2026-11-07 (10:08) — The replacement for our title-writing AI is half-tested: it writes well but is slow as Google ships it, so tomorrow's test runs it at its lowest thinking setting

    Worked (% of the shift): reliability 60 · product 10 · market 10 · gm 10 · data 5 · security 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label. This shift tested Google's suggested replacement for the AI that writes our titles and runs our safety screen, which Google swaps out on 1 December; tomorrow's shift finishes the test.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds.
- **When to switch against bet 1 is now a real choice, set out for the next shift.** For switching first: bet 1's host lines run on the new model from 1 December whatever we do, so reading bet 1 wholly on today's model measures a setup that ends that day. Against: if the switch ships as its own version, bet 1's fair comparison needs about 20 days of it first, because our reporting tool otherwise mixes in all older versions. If that holds bet 1 past mid-November, bet 2 suffers, so the next shift weighs it with the test result.
- **The 1 December swap may not be silent.** Our calls send settings the replacement model refused in September, so every call might fail and fall to the backup, using twice the requests. Switching first avoids it either way.

### Done
- **Reliability (tested, half done):** Google's suggested successor, Gemini 3.8 Flash, works on our free key and has no shutdown date. It wrote a good title, keywords and closing line, but took 34 of the 60 seconds allowed, because it thinks at length unless told not to. It refuses "off", so "low" is the nearest. The safety-screen test ran past 7 minutes and I stopped it unread. I built two test branches at "low", one on today's code and one on bet 1's; all tests pass on both. Not yet live.
- **AI use, over the cap:** probably over a shift's 8 requests, up to 13, all on the candidate model, whose allowance uploads do not use. The test tool's retries caused it; the next item fixes that.
- **Reliability (built, live):** the safety-screen test now shows each case's requests and time as it finishes, and stops one request past its five cases. Before, a slow model could spend 10 requests unseen. A fresh review found that once the cap cut off later cases, the release check would have called a real wrong answer "inconclusive". Fixed before merging.
- **Market intelligence (read):** Google's pages make 3.6 Flash the backup candidate, and the only migration change that touches us is the thinking setting, now handled.
- **Reliability (checked):** all three uploads since the last shift landed; this morning's used the Reddit question as its title, because the shock-bait guard refused the AI's, as designed. The samples your asks link are kept permanently.
- **Security (checked):** no secret in the repository, no workflow change since 20 October, money controls intact ($0.17 this month, forecast $0.76 of $3).
- **General management (ranking):** with nothing ready, a fresh helper proposed five ideas. The three I took corrected claims I had written earlier today, which tomorrow's timing decision would rely on: the 20-day point above, the 1 December failure risk, and the test ledger's bar for title fallbacks. The ledger had dropped "shock refusals aside", so it would have tripped at today's normal rate (3 of the last 30). Dropped: a new risk row for AI model changes (the plan's row and the 7 December re-read already cover it).
- **Data (rule set before the read):** the capitals test's check without its 11 flawed uploads will hold about 25 in one group, under the main read's 30. Set now, from counts only: it is read at that size against its own chance margin, and a narrow lead there extends the test once.
- All fixes and checks, apart from the forced model test. None changes what we ship yet.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your reply to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **8 November, after 07:00:** finish the successor test within 7 requests: the safety screen on one branch, the title check on both, timing every call. Any call over about 20 seconds, or an unexercised case, means trying 3.6 Flash instead. Then, on a later day's allowance, check its host lines over bet 1 against your bar, and decide the switch date.
- **9 November weekly, and later dates:** as set in the last handover; the switch done by 30 November.

### Better?
- **Than last shift:** no for viewers. The forced model switch is half-tested with a working setting, and the test can no longer overspend unseen.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---

## 2026-11-07 (00:20) — Google silently swaps our title-writing AI on 1 December; choosing its successor first is now ready work

    Worked (% of the shift): gm 35 · security 30 · reliability 20 · strategy 10 · data 5

**Summary:** Nothing viewers see changed, and the company is no closer to revenue: bet 1 (#77) still waits on your label, and the 6 November date it asked for has passed. This shift found that Google will quietly replace the AI model that writes our titles and runs our safety screen on 1 December, inside both bets' test windows, so the next shift picks and tests a successor first. It also found two dead login tokens in the public history and made the build fail on any committed credential.

### Toward revenue
- **Nothing directly.** Watch time is flat at 12 seconds; every change that would move it waits on bet 1.
- **Bet 2's fallback is now dated.** If bet 1 has not merged by 20 November, bet 2 is expected to miss at two uploads a day. That day a shift updates #80: four a day before bet 1 then becomes bet 2's only route, against the spam-policy risk #80 describes. The choice stays yours, and the 25 October rule for judging bet 2 stands as written.

### Done
- **Reliability (found, ready for the next shift):** Google's model page says that from 1 December every request to the model that writes our titles, closing lines and host tags, and runs the safety screen, goes to a cheaper model instead. That is the one our sample videos use, which mostly labelled where ours reacted. Nothing would show it: the calls still succeed. It falls inside bet 2's judging window and inside bet 1's test, so a switch nobody chose would muddy both. Rule set tonight, before any test: we switch to a successor we choose before 1 December, as its own version, judged by the rule already set for the other model switch. Testing candidates needs AI requests, so it waits for the 07:00 reset. No cost. Our other two models carry no such notice.
- **Reliability (built, live):** until then, each upload's log now says when Google answers from a different model than the one we asked for, so a reroute can't pass unseen. A fresh review found no bugs. It still combines cleanly with bet 1.
- **Security (found, no harm):** a search of the full history found two YouTube login tokens printed into a notebook's saved output in February–March 2025. Both expired within 7 days, because Google's testing mode capped them at a week; the login in use dates from 19 July 2026 or later. Neither works without the matching client secret, which was never committed. No action needed from you.
- **Security (built, live):** the tests now fail if any committed file holds a credential: GitHub, AWS, Google, Groq or Anthropic keys, Google login tokens and secrets, or private keys. The tool that cleans each shift's public record now also removes Google login tokens and whole private keys. A fresh review found it removed only a private key's first line, plus two smaller faults; all were fixed before merging. It catches a leak after it is public, not before.
- **Security (checked):** library advisories unchanged since 26 October (the image library's fix is still blocked by the video library). No workflow change since 20 October. Money controls intact ($0.15 this month, forecast $0.71 of $3).
- **General management (built, live):** the start-of-shift tracker check now also trial-merges the two branches that must land right after bet 1. On 6 November one had silently stopped merging. Both merge cleanly today. A fresh review found a test gap and two small faults; all fixed before merging.
- **Product (checked):** bet 1's release and its two follow-on branches still combine with tonight's code, new credential check included, and all 1,040 tests pass together. Your label can still merge it.
- **General management (closed):** I withdrew #86. Its own correction had found it unnecessary, and its one lasting piece is in #89, so you have one ask fewer.
- **Reliability (checked):** both 6 November uploads landed, the evening one on GitHub's new build machines, so their switch, due by 19 November, is done and harmless. The morning one went out without its separate caption track, which YouTube refused (the first since 22 September; 7 in September). The words are burned into the video, so viewers saw no difference; I built no retry.
- **General management (ranking):** nothing was ready. A fresh helper proposed eight ideas; two rankers reading in opposite orders put the same two first: withdrawing #86, and bet 2's dated step. Dropped:
  - a caption retry (one refusal in 45 days, and refusals like it usually repeat)
  - asking for viewers' answers in our comment (it would disturb the capitals test and bet 1's vote)
  - starting the replacement source early (dated 14 December; your label and #90 set its lead time)
  - a search-traffic measure (search brings under 2% of views)
  - re-reading YouTube's policy pages (read 3 November)
- A second round, aimed at money, audience, distribution, editorial, market, legal and finance, found nothing in those. On the security side it found that the plain music track, sealed on 10 October, can still be downloaded from the public history; no one ever took the history decision its sealing deferred. I added it, with the dead tokens, to the history question already set for the 7 December monthly, so it costs you no new ask. No viewer names, Reddit usernames beyond the public credits, or account numbers are kept in the repository.
- All of this was fixes and checks. None changes what we ship, because everything that would waits on bet 1.
- AI use: none from the upload allowance, no Polly, no sample video. No helper was left running at hand-over.

### Blocked
- **For you, in order:** #77 (bet 1, by about 13–20 November for bet 2), #82, #89, #90, #91, #92, #93, #88, #65 (your reply to its corrected sentence), #80, #59. You last acted on 27 October.

### Next
- **Next shift, after 07:00:** pick the successor model and test it (the safety-screen replay and the release check), within the shift's AI allowance. Timing the switch against the capitals read (23 November) and bet 1 is the decision to make with the result.
- **On your #77 label:** the title check, the usual gates, merge, then the two follow-on branches; the start-of-shift check says whether they still merge.
- **9 November weekly:** as set: the friction fixes, the zero-view re-read by subreddit, the two dropped friction items. Also, for you through that review: the technical-debt list's cap counts 12 old history notes as open items, so it reads full at 13 real ones. You set that cap on 19 September; the review should propose counting only open items, rather than a shift changing it.
- **Later dates:** 10 November, Reddit's terms. 16 November, the view-swing read. 17 November, redraft the viewer replies if #89 is unlabelled. 20 November, bet 2's step above if bet 1 is unmerged. 23 November, the capitals and voice reads. 30 November, the model switch done at the latest.

### Better?
- **Than last shift:** no for viewers. A silent model swap that would have muddied both bets is now known 24 days ahead, and a committed credential now fails the build.
- **Than ~10 shifts ago:** no: watch time is flat at 12 seconds and bet 1 hasn't shipped.
- **Than ~100 shifts ago:** too early to say.

---
