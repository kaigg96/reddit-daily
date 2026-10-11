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

## 2026-10-11 (00:30) — Shifts ended early because work waited on you; fixed by us. Your three replies are now acted on

    Worked (% of the shift): gm 25 · product 30 · engineering 20 · strategy 10 · distribution 5 · legal 5 · security 5

**Summary:** You told us on #67 to find why shifts end early and fix it ourselves. We did. Work waited on you, and shifts missed replies you had already given: three of your comments (the host, the Groq key, Reddit) sat unread for up to a day. Shifts now see your comments. Asked as one label, bet 2 was approved in 11 minutes (#72). Bet 1's voiced host will not ship, as you asked; its text-only successor is built.

### Toward revenue
- **Not yet, but the queue is honest again.** Your verdict on the host settles the step queued for Monday. Bet 1 (make the format ours) still stands, and its next step is built: one voice, no extra audio spend. Facebook, like YouTube and TikTok, pays nothing for narrated readings, so bet 1 comes first whichever platform earns.

### Done
- **General management (a fix, #67):** found the cause in the record. Every ask you could answer with a label closed, most within a day (12 of 12). Asks needing a session, commands, a login or a listen waited for days, and shifts stopped once all their work waited on those. Worse, the list a shift reads at the start showed only labels and closes, so it missed your comments. The alarm no longer emails you. Each shift now starts with the rows waiting on you and a rule: do every part a shift can, so what reaches you is one label. Your comments now reach the shift. Both changes had fresh reviews, and every fault they found is fixed.
- **Product:** acted on your three replies. The voiced host is recorded as rejected. Bet 1's next step is built behind a switch: the host's setup and reactions as text on screen while the answers are read, and the narrator speaking the vote as today's closing line. One voice, no host audio. A free local sample rendered cleanly, with our own words at 54% of what the viewer gets. Groq: tonight's checks on it passed for titles, but its safety screen skipped one test post Gemini passes, so we are not switching yet. Gemini was overloaded on 3 of the last 5 uploads, so Gemini first, with Groq when it fails, looks like the right shape. Reddit: recorded that we ask before applying to any programme, not now.
- **Strategy:** bet 2 went to you as one label (#72), including four a day's narration spend, and you approved it 11 minutes later. With bets 1 and 2 set by label, the quarter's planning is recorded as held, with no session, and #55 is closed. Bet 3's pilot comes back as its own label once bet 1's next step keeps.
- **Distribution:** Meta's own pages answered what the plan said needed your logged-in read. Facebook's programme is invite-only, paid per 1,000 qualified views. It demonetises accounts that mostly narrate what is on screen.
- **Reliability:** two upload runs could overlap and both pick one post. The fix came with #72 and is live. The daily release check was about to spend up to 8 of production's 20 daily AI requests on the rejected release; it now checks the live code.
- **Legal:** you sealed the music; closed #66. Next upload is the first on the sealed file.
- **General management:** closed 11 old weekly digests so your open issues are only the ones needing you. Code-health passes no longer wait on you (the company's rules give them to Engineering). Three rows that said they waited on you did not; corrected.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: mostly fixing. The improvement is how work reaches you.

### Blocked
- **For you, each one action:** re-label #53 (comments); the account checks (#59). #50 and #65 need your hands: Claude Code protects the skills folder by design, and only a looser mode for the whole shift would open it, which is not worth it.

### Next
- **After tonight's upload:** check its log names the music track, not "none".
- **Bet 1's next step:** the text-only host is built, reviewed (its findings fixed) and switched on in its release. Tomorrow's 08:17 release check reads its lines on the AI that uploads use. Then request its sample after 10:46 (one render per 12 hours) and bring it to you as one label. Since the host is silent, you can judge it from the sample link, with nothing to run.
- **12 October:** read `v7` under its rule, with the buried-upload check beside it.
- **Groq:** build Gemini first with Groq on Gemini's failures; it shares the one render slot with bet 1, so bet 1 goes first.
- **Four a day (approved):** build it switched off, for the subreddit read about 2 November.

### Better?
- **Than last shift:** Yes. Three of your answers had sat unread, and shifts were still waiting on you for them. Now they are acted on, and the cause is fixed in code.
- **Than ~10 shifts ago:** Unclear. Watch time is flat (12.0 seconds), and the first originality step is back to a first sample. But the queue now holds work that changes what we ship.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-10 (22:32) — You approved bet 1, and it is built: a host's commentary, ready to ship after Monday's read

    Worked (% of the shift): product 40 · engineering 25 · editorial 10 · gm 10 · data 5 · legal 5 · security 5

**Summary:** You approved bet 1 on #70, so this shift built it. A host now sets up each question, reacts to the top two answers and casts the show's vote, from the AI request we already make. It is the first change aimed squarely at getting the channel paid, since YouTube does not pay for readings. It is switched off until Monday's read of the current version, and I have asked you to listen to one sample first (#71, about five minutes).

### Toward revenue
- **Yes, the most direct step yet.** YouTube refuses to pay for "readings of other materials". On tonight's sample, with real AI lines on a real post, our own words were 63% of the narration, against none today. Whether that is enough for YouTube's review is unknown until we apply. Without it, the answer is no.

### Done
- **Product (a bet):** built the commentary-led video as you approved it. The host speaks in the voice the narrator is not using, with yellow captions. The answers are still read word for word, the top two in vote order. The host's vote replaces the closing line and is posted as the channel's comment. If any host line is missing or far too long, that upload ships as today's reading, and the log records it. The log also records our own words' share for every upload. Medical threads are skipped when picking the post: that would have skipped 3 of our 168 uploads.
- **Product:** tonight's sample with commentary on passed: a playable video of 29.5 seconds on a real politics thread, a little longer than today's usual 15 to 28. Reading its captions showed two faults. The setup only restated the question ("Reddit weighs in on …"), and one reaction took a side on the issue. The prompt now forbids both. Re-tried with the sample AI on two posts (3 requests on its own allowance): both rules held, but one vote called an answer "the second one". After a rule against that, the vote ran a few words past its limit, so that upload would have been a plain reading. Samples always use the sample AI, so the daily release check will be the first to show what the AI that uploads use does.
- **Engineering:** two fresh reviews. The first found seven real problems, all with commentary on, and all are fixed. The worst two: a fallback upload would still have spoken the host's vote after a plain reading, and an over-long AI line could have cost an upload. The second found three small ones, also fixed. Both confirmed that with commentary off, nothing changes.
- **Engineering:** the daily release check, once this ships, fails if the host's lines are missing and prints them, so a shift can read real host lines every day without a render. Sample verdicts now show them too: that part is merged and live for the next sample.
- **Data:** the reporting tool's release read now prints bet 1's "done" test beside its verdict: how many uploads had our own words at half or more. It never triggers a revert, and it prints nothing for `v7`, so Monday's committed read is unchanged. Reviewed (its crash on a malformed value fixed) and merged.
- **General management:** closed #70. Bet 1 is marked approved in the plan, and the host-storyline experiment is folded into it. Two gaps for the release are recorded: long answers can keep our own words under half, and the length guard's fallback has never fired on a real post.
- **Security:** standing check clean. Narration spend $0.29 this month (forecast $0.90 of $3), money controls in place, no secrets in the project, no workflow change.
- Tonight's upload carried its capitals group (none), and its title obeyed it.
- Fixing against improving: an improvement, the first change to what we ship since the capitals test.

### Blocked
- **For you, newest first:** #71, listening to one sample of bet 1 (two commands, about 2 cents of narration); the four commands on #50; the Groq key and label on #69; the planning session for bets 2 and 3 (#55); asking Reddit (#60); the music script (#66); the account checks (#59); re-running the comments job on #53; pasting #65's sentence.

### Next
- **11 October, 08:17:** the daily release check now tests the commentary release with the AI that uploads use, and prints its host lines. **Its pass is not a go-ahead:** shipping also needs Monday's `v7` read, your listen on #71, and a fresh sample of the release's current commit.
- **12 October:** read `v7` under its rule, with the buried-upload check beside it. If it keeps (or reverts), merge the commentary build and release `v8` once you have listened. The release needs its own sample of the branch's current commit and a release-check pass showing the host lines. If host lines fall back on length there, raise the vote's limit by three words first.
- Then the engaged-view, narrator, dark-morbid and zero-view questions, the clip check and the first subscriber count.
- I handed over about 20 minutes early. Considered and dropped: raising the vote's word limit now (one try on the sample AI; tomorrow's check on the upload AI decides it); merging the switched-off build tonight (its current version has no sample of its own, and the shift's one render is spent); measuring how long real answers run, to size the own-words gap (answers are not logged, and reading them needs YouTube access a shift lacks); narrowing the medical filter's rare idiom matches (a wrong skip costs one candidate, not an upload). The health check's "time unspent" warning went to #67 again: the queue is empty because every next step waits on a dated read or on you.

### Better?
- **Than last shift:** Yes. Bet 1, the change YouTube's own wording says the channel needs to be paid at all, went from a question to a built release.
- **Than ~10 shifts ago:** Yes, though unproven. Then, bet 1 was a draft waiting on your choice of stance. Now it is approved, built and sampled. Watch time is still flat (12.0 seconds).
- **Than ~100 shifts ago:** Too early to say.
