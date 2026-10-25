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

## 2026-10-25 (08:25) — Bet 1's spoken sample met the bar and is on #77; one label from you ships it

    Worked (% of the shift): product 30 · data 25 · gm 20 · strategy 10 · engineering 5 · reliability 5 · security 5

**Summary:** Bet 1's spoken sample, whose three host tags all react ("Oof", "No way", "Uh oh"), is on #77, so one label from you ships it. A check of how its first two weeks could go wrong found three ways its verdict would have been misread, all fixed before any upload.

### Toward revenue
- **Bet 1 is one label from shipping.** Every route to revenue needs it, and this is the first sample since your 19 October feedback whose tags meet your bar.
- **The revenue gap is sharper.** At four a day every upload would need about 75,000 plays, about 70 times our best ever, so no hit rate closes it: the gap is each video's reach. For the 5 November review.

### Done
- **Product (bet 1, the sample):** rendered on the build machine in the free stand-in voice, with tags from the model real uploads use: 30 seconds, no faults, each tag in the pause after its answer. The opening tag ("My money's on…") was not a reaction, so it was left out as designed. Our own words are 17% of what is read (long answers); reported, never a gate. Posted to #77 with frames, the video, and this morning's upload of the same post.
- **Product (a measurement, set before it ships):** bet 1's answer to YouTube's spam rule (#80) is that the host makes each video different, but stock tags like "Oof" could repeat across videos. Fixed now: a tag on 5 or more of the first 20 uploads means a check against recent uploads' tags comes next. The three samples so far repeat none.
- **Strategy and data (a correction):** the record said each upload needs about 28,000 views at four a day, counting plays; the bar counts engaged views (37% of plays), so it is about 75,000. Corrected in both plans.
- **Data (a pre-mortem of bet 1's first two weeks: one fix, live, and three corrections):** a fresh agent assumed bet 1's read went wrong and found four causes, all confirmed. (1) The Monday report and the shifts' command would have judged bet 1 across both subreddits, though its rule reads AskReddit only and the mix shifts with it (70% before, about half after). Both now read AskReddit, with a test against misspelling; reviewed twice, no blockers, live, no video change. (2) Bet 1's videos run ~2 seconds longer by design, which alone would trip its two warning signs; both now allow for length, worked out from the old version's data alone. (3) Own words' share no longer sets the next step (your 19 October call). (4) The live tags get read by eye at the 6th upload, not first at the 20th.
- **Data (a research question, "cannot tell"):** do some topics keep more viewers past the opening? Only one topic has 8 uploads at a common age, so the report refuses; that is the answer.
- **General management:** nothing was ready. A fresh agent proposed eight ideas; two failed the filters (upload hour, already read as the time slot; counting deleted Reddit sources, which Reddit refuses our build machine). Two rankers, in opposite orders, put the same two first: the per-upload need (done) and a Partner Program readiness list (dropped: those gates bite only when we apply, about 720 times away). Third on both, the topic read (done). A second round, the pre-mortem above, found the rest. **Dropped:** a within-day pairing test (answered 5 October); a scan for paid text-only channels (done 18 October); generated music (your task, and AI music needs disclosure); the prompt trial without "agreement" (changing the prompt now would change what you are judging on #77).
- **Reliability and security:** both uploads landed today. The standing check is clean (no secrets, no workflow changes, you the only collaborator); money controls in place ($0.71 this month, forecast $0.86 of $3).
- Mostly fixes and measurement; the sample is the bet. AI use: one sample render, clear of both uploads; no Polly.
- **Process:** the "08:17" release check runs at 12:40–13:45 (GitHub starts every schedule here 4–5 hours late), so a morning shift cannot read it first, as the last handover asked; the render went ahead without it. The answer-length tool ran its whole collection when asked for usage, appending rows; reverted and fixed (reviewed). Handed over ~20 minutes early: what was left fell below the bar (a tool listing live tags, which one planned command does).

### Blocked
- **For you, in order:** #77 (watch the sample; one label ships bet 1); #82 (register our Reddit app, by 12 January); #80 (one label, by about 1 November); #50 (four commands, which unblocks #65); #59 (the account checks).

### Next
- **If #77 is labelled:** merge the release branch once that day's release check passes on its current commit, then update the plans. The next upload is the first of the new version.
- **If you comment instead:** fix it and render again (next slot ~20:30).
- The Stack Exchange spoken sample, in a free render slot.
- 26 October weekly read, then the opening-reach read.
- The audit comes due at about ten shifts since 21 October; this was the ninth.

### Better?
- **Than last shift:** Yes. A sample whose tags meet your bar is in front of you, where last shift's was still being filtered, and bet 1's verdict can no longer be read on the wrong cut.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped, though it now waits on one label, not your machine.
- **Than ~100 shifts ago:** Too early to say.
