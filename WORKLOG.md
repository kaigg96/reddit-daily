# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PLAN.md](PLAN.md) (the company), [PRD.md](PRD.md) §0 (the product) and
[TECH_DEBT.md](TECH_DEBT.md) (code health).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

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

## 2026-10-07 (17:50) — Nothing we track predicts a hit, so more uploads is the one views lever with evidence

    Worked (% of the shift): data 50 · gm 20 · engineering 15 · reliability 5 · legal 5 · security 5

**Summary:** Nothing was ready, so I tested three questions our own numbers could answer. None of the things we track (title style, topic, voice, background, time of day, question length) predicts which uploads become the hits that earn most views, and September's fall in views isn't explained by anything we track. No video changed. The company is no nearer revenue, but it now has evidence that more uploads per day is the lever for views.

### Toward revenue
- **Nothing directly.** Every step that would change what we ship waits on you (the planning session, #55) or on data arriving 12 October.
- **More uploads per day now has evidence behind it.** The top tenth of uploads earn 42% of views. None of the six things we track predicts which uploads land there, so every upload is a similar lottery ticket and more tickets is the lever. That item stays behind the subreddit test, as planned. The title style we now favour lifts the typical upload's views but does not make more hits.
- **Views per upload fell by about a third in September** (about 250 down to about 150 at a week old). It happened in both daily slots and with both voices. The retired background clip and that month's failed titles each explain only a sliver, and nothing else we track explains the rest, so I am not proposing a fix. Bet 2's starting point of 8,300 views a week stands: no fix already made will lift it for free. The week to 5 October gained the most views of any week on record, so the dip may already be passing; the 12 October figures will say.
- **Nearly every view toward YouTube's bar comes from new uploads.** The 800-odd older videos earn under 1% of views, about 3 a day. So the bar rises or falls with what we publish now, another point for more uploads per day.

### Done
- **Data:** the three reads above, plus one more: the share of plays that get past the opening (the views YouTube's payout bar counts) does not vary with anything we track either. So the favoured title style's lead carries over in full to the views that count. A finding.
- **Engineering:** the reporting tool can now read the weekly trend inside one group or with one group left out, test which groups produce hits, and split views between old and new videos. Fresh reviews caught a real bug before merging (a misspelt filter silently kept everything) and two smaller ones. One also caught a misleading reading I had already written down: "the drop is all one voice" was an artefact of how many videos each voice read. Both fixed. The tool also explains itself now instead of crashing when asked for a report that needs YouTube access a shift doesn't have.
- **General management:** the shift rules forbid a sample video within an hour of an upload because its AI requests used to share the upload's allowance. They no longer do (since 25 September a sample uses a separate test model). This evening the rule stopped the finished vote feature getting its sample, so I asked you to drop it (#65, one sentence). Shifts cannot edit their own rules.
- **Legal:** the music fix you approved (#64) closed when its workflow half landed, but the plain music file is still public: your two-minute script has not run. Nothing breaks meanwhile. I raised a reminder (#66) so the closed issue doesn't read as done.
- **Reliability and security:** yesterday's two uploads and this morning's landed; money controls are clean ($0.21 this month); no secrets in the project; the only workflow changes are the two you approved (#63, #64).
- Fixing against improving: two fixes (the filter bug, the crash); the rest was research.

### Blocked
- **For you, in order of what they unblock:** the planning session (#55); asking Reddit (#60); running the music script (#66, about two minutes); Gemini's paid tier (#62); the account checks (#59); the sample-video rule (#65, new); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Ask for the vote feature's sample video, and merge it on a pass. Under today's rule that means a shift after 07:00 UTC and not within an hour of an upload, so tomorrow late morning. If you approve #65, any shift can ask. For planning: if the vote starts 13 October, its first read lands about 9 November (it is judged on AskReddit uploads alone, which now come one a day, and needs 20 of them a week old).
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, and the first subscriber count.
- After you run the music script (#66): check the next upload's log names the track, not "none".
- Tonight's upload, the first from NoStupidQuestions, had not run by hand-over: check it landed with a generated title. If its log shows a quota refusal, the daily allowance is tighter than we think: this afternoon's release check also hit one, with little spent since the reset.

### Better?
- **Than last shift:** Unclear. We know more (hits look like luck, and September's drop has no cause we could undo), but nothing we ship changed.
- **Than ~10 shifts ago:** Somewhat. The views lever is now evidenced, not assumed, and the tests admit what they cannot see. Views per upload are lower than in August.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-07 (10:15) — Bet 1's first step is built, switched off, and can start in mid-October; our project shares a music file it shouldn't

    Worked (% of the shift): product 35 · legal 25 · data 15 · editorial 10 · gm 10 · security 5

**Summary:** No video changed, but bet 1 got closer. I drafted three house voices for you to choose from and built the cheapest first step, switched off until you do: the host's vote replaces the closing line, adding no length or AI request, and it can start in mid-October rather than November. I also found our public project shares a music file YouTube's terms forbid sharing, and readied a two-minute fix for you.

### Toward revenue
- **Bet 1 can start three weeks sooner.** Its first step (the reaction beat) was queued behind the subreddit test, which reads around 2 November. Both running tests split each day's uploads between their sides, so a change to every video biases neither. Once you set the stance, bet 1 can follow v7's read on 12 October, judged on AskReddit uploads only.
- **Three house voices, tried on this week's real answers** (on the planning issue): a "show of hands" host who votes for one answer and asks the viewer to vote, a skeptic, and a warm "noticer". I recommend the show of hands, with its rule in one sentence of yours. It can replace the closing line every video already speaks ("comment your answer"), so bet 1's first step would add no length, no AI request and almost no narration cost. YouTube asks for the creator's own perspective, so the stance has to be yours.
- **The fallback source does not fit as is.** If Reddit says no, Stack Exchange is the fallback. None of its 95 popular questions across six sites had three answers short enough for our format; the typical answer is seven times too long. It could only feed a show where we condense answers in our own words. That is a rebuild, one more reason to ask Reddit early.

### Done
- **Legal:** since the project went public on 5 October, anyone can download the one YouTube Audio Library track in every upload. Its terms, as quoted by several guides, forbid offering the files apart from videos. I wrote the fix: the music is stored encrypted and unlocked only while rendering. It is yours to apply: a label, then one script on your machine. A fresh review caught two bugs first. A fix.
- **Product:** the topic ranker's go/no-go count came due: it would change 5 uploads in 20. A ranker that touches one upload in four cannot show up in our test unless each change gains about 50%, and the best topic edge we have measured is 12%. Parked, with the condition that reopens it. The safety screen's weekly check is clean: no post skipped this week, four answers dropped.
- **Product:** built bet 1's first step, switched off: one setting, empty until you choose, turns the closing line into the host's vote, written from your rule. While empty, what the AI is asked is unchanged to the letter, so no video changes. I tried it on this week's five posts on the test model's own allowance (examples on the planning issue): four good votes, and one claim about autism, which a new instruction fixed. It waits for its sample run (the next opens at 11:36). Switching it on is a release. A bet.
- **Data:** v7's videos run 3 seconds longer than any earlier version's, though v7 changed only on-screen text. Longer videos earn more watch time, so most of v7's +25% early lead is length; within long videos it is +8%, inside normal swings. Before the 12 October read I recorded that v7 gets credit only for gains that hold among same-length videos, and the release check now prints that comparison itself whenever a release changes video length. It can also read a release inside AskReddit alone, as bet 1's read requires. The keep-or-revert rule itself stands, with your total-watch-time check (#39).
- **Data:** from Monday, the weekly statistics also record how many subscribers each upload won. Subscribers are half of YouTube's bar, and until now no test could say which videos earn them. A refusal costs only that column. Checking that, I fixed a hidden fault: one refused figure would have stopped every age-matched report. A fix. Your Monday email will also flag any upload that went out without music.
- **General management:** landed the fresh-review merge step you approved (#61) and closed it. This morning's upload ran on the new Python and credited every Reddit user by name, so both of yesterday's changes are confirmed live; trackers updated.
- **Security:** standing check clean: $0.20 spent this month, no secrets in the project, no unapproved workflow change.
- Fixing against improving: three fixes (the music licence, the length reading, the hidden fault); the rest improved bet 1's path and the plan's evidence.

### Blocked
- **For you, in order of what they unblock:** the planning session (#55; it gates bet 1, and now has three voices to pick from); asking Reddit (#60); the music fix (#64, new; a label and a two-minute script); Gemini's paid tier (#62); the account checks (#59, about 15 minutes); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Tonight: check the first NoStupidQuestions upload lands with a title.
- After 11:36: request the sample run for the switched-off vote, and merge it on a pass. Both its fresh reviews are done and clean.
- 12 October: read v7 under its rule, with the same-length read beside it; then the engaged-view, narrator and dark-morbid questions and the first subscriber count.
- Also on 12 October: last week's snapshot shows more uploads stuck at zero views (5.6% against 2.4%). One week is weather by the tool's own rule; read it with the clip rule and act only if it repeats.
- Once you apply the music fix and run the script: confirm the next upload's log shows the track, not "none".
- If you choose the vote: switch it on as the next version after v7's read, with a real sample. If you choose another voice: build the reaction beat to its spec, now current.
- Considered and not taken: tracing why v7's posts run longer (it would not change the 12 October reading), and preparing Gemini's paid tier (nothing to prepare until you decide).

### Better?
- **Than last shift:** Slightly. Bet 1's start moved from November to mid-October, pending your stance, and a licence breach has a ready fix. Nothing we ship changed.
- **Than ~10 shifts ago:** Somewhat. The legal ground and the fallback are known first-hand, and our tests now admit what they cannot detect. Views and watch time are flat.
- **Than ~100 shifts ago:** Too early to say.
