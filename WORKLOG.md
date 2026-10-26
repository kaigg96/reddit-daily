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
