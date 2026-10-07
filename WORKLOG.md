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

## 2026-10-07 (23:50) — Bet 1's vote is in the live code, switched off: one sentence from you starts it

    Worked (% of the shift): product 35 · data 30 · reliability 10 · engineering 10 · gm 10 · security 5

**Summary:** The host's vote, bet 1's first step, passed its sample video and is now in the live code, switched off; your one sentence on the planning issue is all it waits for. No video changed tonight, so the company is no nearer revenue yet, but bet 1 no longer waits on any build.

### Toward revenue
- **Bet 1 now waits only on you.** I added a note to the planning issue (#55): reply with one sentence saying what earns the show's vote, and a shift switches it on as a new version with a sample video, the day after v7's read on 12 October. Its first read lands about four weeks later.
- **The volume test can now give an answer.** More uploads per day is our evidenced views lever, but its rule judged each video's views within about 30%, inside their normal swing, so it could never tell dilution from luck. It now runs at four a day and is judged on the four-week total of views that bet 2 targets. Three a day was dropped: at best it adds half again, and our tools can only see a doubling. Four a day was already shown to fit the daily AI allowance.

### Done
- **Product:** brought the vote up to date with the live code, got its sample video (passed: playable, 31 seconds, no silence) and merged it. A fresh review found nothing blocking and three small gaps, fixed and merged after a second review: the vote line is held to the same 12 words as today's closing line, so its read is not muddied by length the way v7's was; a test fails if anyone switches it on without labelling the videos as a new version; and a test checks the unchanged wording exactly. A bet, shipped dormant.
- **Data:** video length does not predict views. Within one release longer videos got 28% more views, across releases shorter ones looked 10% better, both inside the usual swing, and hits are as likely either way. So trimming videos would not buy views, and a host line that adds a few seconds has no measured views cost. A finding.
- **Data:** two questions the tool rightly refused: whether lower-ranked Reddit posts do worse (only 4 such uploads), and whether extra uploads split views (we have posted two a day throughout, so there is no history to read). The second shaped the volume test's new rule.
- **Reliability:** tonight's first NoStupidQuestions upload landed with a generated title. This afternoon's quota refusal in the release check was a one-off: the 13 checks before it all completed. Nothing to fix.
- **Editorial:** tonight's upload asked about an ethnic group ("why are there almost no Asian homeless people?"). The safety screen passes it by design, since it skips only kinds of question that have actually been buried. If this one is buried at a week old, that is the evidence for a new skip rule.
- **Security:** standing check clean: $0.21 spent this month, money controls in place, no secrets in the project, no unapproved workflow change.
- Fixing against improving: one fix (the review's three gaps); the rest shipped a bet and sharpened how the next one is judged.

### Blocked
- **For you, in order of what they unblock:** the vote's one sentence and the planning session (#55); asking Reddit (#60, a draft message is on the issue); running the music script (#66, about two minutes); Gemini's paid tier (#62); the account checks (#59); the sample-video rule (#65); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, and the first subscriber count. Last week's rise in uploads stuck at zero views (5.6% against 2.4%) is read with the clip rule, acting only if it repeats; tonight's NoStupidQuestions upload is one to watch.
- If you send the vote's sentence: switch it on as the next version the day after v7's read, with a sample video, and read it on AskReddit uploads only.
- Considered and not taken: rewording the safety screen's test case so it checks judgement rather than memory (testing it would spend the AI allowance the morning upload needs); upgrading a login library with a known flaw (the flaw is server-side and does not touch us); the zero-view list (it needs YouTube access a shift lacks).

### Better?
- **Than last shift:** Yes, slightly. Bet 1's first step went from built to in the live code, and the volume test can now give an answer.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a ready first step and a rule that can read it. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.

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
