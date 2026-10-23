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

## 2026-10-23 (22:55) — Bet 1's first spoken sample plays, but its host tags praised the answers instead of reacting, so I held it back from you; a reworded prompt shows promise

    Worked (% of the shift): product 40 · reliability 25 · data 15 · gm 15 · security 5

**Summary:** Sample videos now speak on the build machine, and tonight's played end to end. But on tonight's post the host's three tags praised the answers ("Spot on", "Deep insight") instead of reacting to them, the weakness you flagged on 19 October. So I did not ask you to watch it. A reworded prompt fixed that post on a first try, and needs a wider check before you see a new sample.

### Toward revenue
- **Bet 1 is closer, not shipped.** Every route to revenue needs bet 1, and its last gate is you watching a narrated sample. Tonight's sample showed a gap the trials had missed. On personal advice questions ("Why does my friend act like this?"), about one upload in eight, the host grades the answers. Showing you that would have cost you a viewing to repeat your own feedback.

### Done
- **Product (a bet):** the free stand-in voice rendered on the build machine. It passed every check and is now on the release branch, so future samples speak. Your own render command is unchanged by it. The tags were "Direct hit", "Spot on" and "Deep insight", all verdicts. The first answer also only made sense with the post's body, which viewers never see. None of the nine trial posts was a personal advice question; two now are. If you want to see it anyway, the sample stays on tonight's render page for 14 days. It is not an ask.
- **Product (the fix, a bet):** the reworded prompt drops "agreement" from the reactions it invites and names grading as a verdict. On the upload model, one request per post: tonight's post went from 0 of 3 reactions to 2 of 3 ("Wait, what?", "Oof, direct"). A second advice post scored 2 of 3 either way. A direction, not a rate; it stays out of the release until it holds on the other nine posts.
- **Reliability (a fix, built on bet 1):** the swear-word filter now also covers the host's vote and its on-screen tags. They spare "Oh god" and "Hell no" but refuse "Holy shit". This was the gap a review found yesterday where the filter fix meets bet 1. Reviewed; it joins the release after the filter's own render.
- **Data (a research question):** is the flat 12 seconds hiding gains at the opening? Our watch-time figure leaves out most viewers who swipe away early, so I added seconds watched per play start, swipe-aways included, and fixed the rule before reading. Across all uploads it rose from 3.7 to 5.3 seconds. Among longer videos it was flat, and the rule needed both, so **it is not a finding**: the rise may come from the mix of lengths. Reviewed and merged as a diagnostic. It never decides a revert.
- **Data:** bet 1's revert check measures total watch time in a way that runs about 2.5× YouTube's own minutes. Recounted from minutes, no past keep-or-revert decision changes, so no change is proposed.
- **General management:** nothing was ready. A fresh agent proposed eight ideas and six survived. Two rankers, in opposite orders, put the same three on top: the watch-time read and the revert check (done above), then the swear-word gap (done). **Dropped:** whether any Shorts money comes before the Partner Program (the plan already answers it); amending the rule for staying on Reddit (your #60 call covers it); a dependency audit (run: Pillow's known flaws grew, still unreachable as we never open outside images).
- **Process:** three scheduled shifts were skipped from last night to this afternoon because the week's shift allowance ran out a day before Friday's reset. The guard worked as designed, but it is why last night's planned render waited a day.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.68 this month, forecast $0.98 of $3).
- Mostly bets, with one fix. AI use: one sample render (one upload-model request), three upload-model requests for the tag trial; no Polly.

### Blocked
- **For you, in order:** #82 (register our Reddit app, by 12 January; sooner is safer); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks). #77 needs nothing from you until a sample is posted there.

### Next
- **After about 10:17 UTC tomorrow:** render the swear-word filter branch; on a pass naming its commit, merge it into the live branch (no version bump). Then fold the vote-and-tags guard into the release branch.
- **The tag check:** the reworded prompt on the other nine trial posts, upload model. The daily release check and both uploads share its allowance, so about three requests a day fit safely; it spans a few days. If it reacts at least as often as before (14 of 18, 21 October), fold it into the release, render, and post that sample to #77.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Slightly. Samples speak without you, and a tag weakness reaching about one upload in eight was found before shipping, not after.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-22 (16:50) — A swear word reached this morning's title; the filter's gap is fixed and waits for one render. Reddit's own page: register by 12 January; free access still ends in March

    Worked (% of the shift): reliability 40 · legal 25 · strategy 15 · gm 15 · security 5

**Summary:** This morning's upload went out titled with a swear word, because our word filter misses words inside quote marks. The fix is built and reviewed, and goes live after one sample render. Reddit's own registration page shows that registering is not a new request, so 12 January is the real deadline. Free access still ends in March whatever we do, which makes the 5 November source choice the real answer.

### Toward revenue
- **Nothing directly.** The fix protects the channel rather than growing it. The three reads sharpen the 5 November choice of a source after Reddit, the company's one fatal, dated risk.

### Done
- **Reliability (a fix):** this morning's video went out as "Could YOUR Will Start with "Alright Fuckers"?". Our word filter misses a swear word touching a quote mark or Reddit's bold and italic marks, and the AI title then quoted the post. It was 1 of 191 uploads. The filter on answers shares the gap, and so do contractions ("shit's"). Nothing checked the AI's own words either: an emoji title shipped on 1 September. The fix catches all of these: an AI title with a swear word or emoji now falls back to the screened question, and a closing line to our standard one. It leaves "he'll" and "who're" alone. Fresh reviews found three misses and two over-catches; a fourth found nothing more. All are fixed but one, which lives in bet 1's unreleased code and is recorded for when the two meet. On 959 old questions it flags nothing new. It changes which posts and AI lines qualify, not the video. **I recommend leaving the live video as it is:** retitling it would alter one row of two running title tests, and we earn no ad money it could lose. That is yours to overrule.
- **Legal (Reddit):** Reddit's own registration page, read first-hand from an archive copy. It is for "existing apps", so 31 October (the end of *new* requests) does not apply to us. Uploads stop from 12 January if we have not registered. It needs the login of the account that owns our app and a personal Reddit account. In Reddit's words, "remaining public API access will end in March 2027", registered or not. #82 now carries the link and these steps.
- **Legal (Stack Exchange):** its licence fits a Short, on conditions: credit in the description, and the upload left on YouTube's standard licence setting. The cost: anyone could re-upload those videos, even for money, and we could not claim them.
- **Strategy:** 16 Stack Exchange sites, read for free. Not one recent question has three answers short enough to use as written (30 words or fewer). So every such video needs AI shortening, which is what made yesterday's sample read as dry advice.
- **General management:** nothing was ready. A fresh agent proposed eight ideas; five survived its filter. Two rankers, in opposite orders, put the same three on top: the filter, Reddit's page and the licence, all done, plus the fourth (the survey). A second round found the unchecked AI words, done above. **Dropped:** a sample of the "our own questions" show (not finishable in time, and its render queues behind three others). Also closed #74, as you said on #77.
- **Reliability (tonight's render):** the stand-in voice branch merges cleanly, and all its tests pass on its own and with live code.
- **Security:** the standing check is clean. No secrets in the project, no workflow changes, you remain the only collaborator, and the money controls are in place ($0.65 this month, forecast $0.85 of $3).
- Mostly fixing, plus reads. AI use: no Gemini, Polly or Groq; 27 free Stack Exchange requests. Handed over about 15 minutes early: the second round's last idea, titles a stray "<" would make YouTube refuse, has never occurred in 2,300 past texts, so it is recorded rather than built.
- **Process:** one render per 12 hours now queues a live fix behind a sample. Tonight's slot is bet 1's, so the fix waits about a day.

### Blocked
- **For you, in order:** #82 (register; the exact page is on the issue; by 12 January, sooner is safer); #77 (tonight: watch the sample); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- **Tonight, after 20:56 UTC:** as planned, render the stand-in branch and post it to #77.
- **The slot after:** render the filter branch; on a pass naming its commit, merge it into the live branch (no version bump). Then the Stack Exchange sample.
- The 28 October re-raise of #82 can wait: re-raise in early December if it is still open.
- 26 October weekly read, then the opening-reach read once.

### Better?
- **Than last shift:** Slightly. A live gap in what we publish is closed, pending one render, and #82's step is now exact.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. The source decision has firmer facts.
- **Than ~100 shifts ago:** Too early to say.
