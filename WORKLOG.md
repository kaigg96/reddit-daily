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

## 2026-10-25 (22:45) — The Stack Exchange sample shows the host grading advice; the own-questions sample is built for the 5 November choice

    Worked (% of the shift): strategy 40 · engineering 20 · gm 10 · editorial 5 · market 5 · data 5 · finance 5 · reliability 5 · security 5

**Summary:** The Stack Exchange version of the show was rendered tonight. The "our own questions" version is built and reviewed, and renders next shift. So the 5 November review can weigh both replacements for Reddit as planned. Nothing reached viewers; bet 1 still waits on your label on #77.

### Toward revenue
- **Nothing directly.** Reddit's free access, our only source, ends in March, and these two samples are how you will pick a replacement. Tonight's finding bears on it: on Stack Exchange's advice questions the host praised the answers ("Smart move", "Nice framing") instead of reacting to them, as it did on Reddit's advice threads on 23 October. On that show the host would need a different job.

### Done
- **Strategy (the Stack Exchange sample):** brought up to date with bet 1's release, then rendered once, clear of both uploads. It plays (37.5 seconds against our usual ~21), with three shortened workplace answers, dry and all in the first person. The host's tags were praise or labels that the filter's stock list misses. I did not grow that list again: the audit flagged its growth, and this is not live.
- **Strategy and engineering (the "our own questions" sample, a bet):** built on a side branch, never merged. One AI request writes a question and three takes. Each take is labelled "TAKE 1/3" on screen, under the host's note "Three takes. All mine.", so nobody mistakes them for real people's answers. The host reacts to none of its own takes. A fresh review found no blockers and nothing touching live uploads; I fixed its main points (the note now shows even if the AI's other lines fail, a rejected reply gets one free retry instead of wasting the day's render, and takes cannot speak as a character or in the first person). On the free AI models, 7 of 7 trial episodes were usable, all plain stances and all bland ("What is the best way to spend a rainy Sunday?").
- **General management:** nothing was ready. A fresh agent proposed eight ideas and six survived. Two rankers, in opposite orders, put the same three on top: the own-questions sample, the voice cost and the outside checks (all done). **Dropped:** making a refused render request retry itself (a workflow change for a case that has not happened); keeping raw AI replies out of public build logs (it would touch bet 1's release branch while #77 is pending).
- **Finance (a check):** a Stack Exchange video narrates about as many characters as ours (485 against ~455), so no budget change.
- **Market and legal (a check):** Reddit's dates are unchanged; its new $1,000 migration bounty is for apps moved inside Reddit, which ours cannot be. YouTube still gives no start date for cutting reach to unoriginal channels, but says channels that turn original get reach re-evaluated, so bet 1 could win reach back.
- **Data (set ahead):** if bet 1 merges after 6 November, the doubling test (bet 2) keeps its window and bar, and says how many weeks ran at four a day; with fewer than two, four a day gets its own read, set in January.
- **Reliability and security:** this morning's and this afternoon's uploads landed. The standing check is clean: no secrets in the project, no workflow changes, you the only collaborator, money controls in place ($0.73 this month, forecast $0.87 of $3).
- **Editorial (a fix, from a second round aimed at neglected functions):** your music task said "anytime", though it must wait for bet 1's read or it changes two things at once; and adding tracks would replace today's track, not add to it. Both are now in the task. **Dropped:** collecting viewers' countries, ages and search terms weekly (it changes no decision, as found on 14 October); free public-domain music (it would replace today's track mid-read, YouTube's claim system flags such tracks, and nobody here can listen); declaring English audio and auto-dubbing (both change every upload mid-read; dubbing is your setting).
- Mostly bets and checks; no live code changed. AI use: one sample render, seven free-model trial requests; no Polly.
- **Process:** handed over about 30 minutes early. The one ready item, the next sample's render, waits for the 12-hour render limit, and two rounds of ideas left nothing above the bar.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; it must merge by about 30 October to 6 November for bet 2 to run as planned); #82 (register our Reddit app by 12 January); #80 (one label, by about 1 November); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **Render the own-questions sample** after 07:00 UTC (the one render that shift), and record it beside the Stack Exchange one for 5 November.
- **If #77 is labelled:** merge the release branch once that day's release check passes on its current commit.
- The 26 October weekly review, then the opening-reach read once the snapshot lands.
- The 5 November monthly: both samples; the rule bundle as one ask; distribution and finance get their turn.

### Better?
- **Than last shift:** Slightly, for the company: the source decision now has both its samples (one rendered, one ready), and a real finding about the host on advice. Nothing new for viewers.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped. For the Reddit deadline, both replacement candidates are built and one can be watched; ten shifts ago neither existed.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-25 (15:40) — The audit found shifts waiting on you, not short of ideas; #77 now asks only for a label

    Worked (% of the shift): gm 50 · product 10 · finance 10 · engineering 10 · strategy 5 · editorial 5 · reliability 5 · security 5

**Summary:** This shift ran the process audit that comes due every ten shifts. Every shift since 21 October ended early with nothing ready, because what is worth doing waits on you, and nothing has moved on your side since 20 October. The issue that ships bet 1 still asked you to render a video yourself; it now asks only for a label on a sample you can watch in the browser.

### Toward revenue
- **Bet 1's ask is smaller.** #77's title and description asked for a render on your machine, though this morning's comment links a spoken sample you can watch in the browser. Both now lead with that sample; the local render is optional. Editing sends no email.
- **Break-even, priced for the first time.** It had been dropped four times as "needs your subscription price". It does not: on Pro ($20 a month), reaching the Partner Program bar covers our costs at any reported ad rate; on Max ($100 or more), only in the upper half of the reported range, and at the lowest rate it takes three to six times the bar. So the bar is roughly break-even, not profit. For the 5 November review.
- **#77 has a date.** Doubling weekly views (bet 2) is judged over the quarter's last four weeks, from 30 November, and four uploads a day starts only once bet 1 has run 24–31 days. So bet 1 must ship by about 30 October to 6 November for that test to run as planned; each week later costs it one of its four weeks. Four a day fits the voice budget: about $1.80 a month of $3.

### Done
- **General management (the audit):** nine shifts since 21 October ran 26–43 of 60 minutes. All handed over, none had anything ready, and nothing reached viewers. Checks caught real faults before release (two samples held back, a slur created by cutting a line, a blank line that dropped the whole host). There were no reverts and no rule broken. **Found:** (1) two plain-label asks wait (#77, #80) while nothing of yours has moved, so no re-asks, which would only add email; (2) distribution and finance had no time in twenty shifts, monetization and editorial none since 21 October (for 5 November); (3) all nine shifts called themselves better than the last while watch time stayed flat: the self-grading the report's template warns about, so this entry answers for viewers first; (4) six of nine were mostly fixes, many of them word lists for bet 1's tag filter, grown three times. Every decision re-tested (two triggers had fired, on your queue and the ready floor), one compressed, two superseded findings shortened. Rule fixes that need your approval are bundled for one ask at the 5 November review, not sent now: the ready-work floor (3 in the rules, 5 in the code), a false line saying shifts cannot read run logs, and your approved #65 sentence.
- **Product:** #82's title said to register by 31 October; the date that binds us is 12 January. Corrected, no email.
- **Engineering (a fix, live):** the tool that shows where each shift's time went counted two re-dated shifts twice and stopped short of ten shifts back. Fixed in two steps, each reviewed by a fresh agent (no blockers), merged; no video change.
- **Editorial (a check):** the working name "Show of Hands" belongs to an English folk duo active since 1986, with its own YouTube channel, so a rename proposal cannot assume it. Recorded on the brand item.
- **General management (a second round of ideas):** a fresh agent proposed eight, five survived; two rankers, in opposite orders, put the same two first, the date above and the voice cost (both done). Dropped: the content screen's standing check (tomorrow's weekly review), a description line saying what the host adds (it ships only after bet 1 is kept), and a likes test (likes earn nothing, and the counts are thin).
- **Dropped:** which uploads gain subscribers (gains are zero on almost every upload, 21 ever, so nothing can be told apart); the Stack Exchange spoken sample (this afternoon's upload runs about 16:00, inside the hour a render must avoid); a hook that stops a shift ending before its handover (every traced shift since 19 October handed over); deleting four abandoned side branches (unmerged work; recorded instead).
- **Reliability and security:** yesterday's two uploads and this morning's landed; the last six runs succeeded. The standing check is clean: no secrets in the project, no workflow changes, you the only collaborator; money controls in place ($0.73 this month, forecast $0.87 of $3).
- Mostly process and fixes; break-even, the date and the name check are new. AI use: no upload-model, Groq or Polly requests, no render.
- **Process:** shifts cannot edit the rule files (refused again today), so the bundle will reach you as exact text, as #65 did. Handed over about 20 minutes early: the second round's other ideas fell below the bar (above), and the next real item, the Stack Exchange sample, cannot render until this evening.

### Blocked
- **For you, in order:** #77 (watch the sample in its 25 October comment; one label ships bet 1); #82 (register our Reddit app by 12 January; sooner is safer); #80 (one label, by about 1 November); #59 (the account checks); #50 and #65 (your hands, on the rule files).

### Next
- **If #77 is labelled:** merge the release branch once that day's release check passes on its current commit, then update the plans.
- The Stack Exchange spoken sample, in the first render slot clear of an upload (after about 17:30 UTC).
- The 26 October weekly review, then the opening-reach read once the snapshot lands.
- The 5 November monthly: raise the rule bundle as one ask with its exact text; give distribution and finance their turn.
- **About 2 November, if #80 is still unanswered:** the plan you approved turns on four a day after the subreddit read, while #80 asks it to wait for bet 1 (the spam rule's risk is the channel itself). Recommend holding: going ahead is the riskier action, and one label from you starts it.

### Better?
- **Than last shift:** No for viewers; nothing new reached them. Slightly for the company: bet 1's ask is one label, and break-even is known.
- **Than ~10 shifts ago:** No: watch time is flat at 12 seconds and bet 1 has not shipped, though its ask shrank from a session on your machine to one label.
- **Than ~100 shifts ago:** Too early to say.
