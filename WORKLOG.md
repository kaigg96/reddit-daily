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

## 2026-10-09 (00:00) — The free AI route that keeps Reddit posts out of training is now in the live code, switched off: your key and one label turn it on

    Worked (% of the shift): engineering 45 · market 15 · product 15 · gm 10 · security 10 · reliability 5

**Summary:** The free AI route that keeps Reddit posts out of training (#68) is now in the live code, switched off and checked, so your ten minutes on #68 and #69 leave no building to do. Outside evidence also says one host line per video is unlikely to be enough originality for YouTube, which matters for bet 1; neither brings revenue directly.

### Toward revenue
- **Nothing directly.** Two things moved. Once you add the key, Groq takes away the AI-training part of the Reddit-terms problem and lifts the 20-a-day AI limit. And bet 1 now has YouTube's own wording on what originality earns money, which bears on how big that bet has to be.

### Done
- **Engineering:** finished the steps that had to come before switching to Groq, then merged it into the live code, switched off. If it is switched on without its key, calls fall back to Gemini rather than costing the upload its title. The upload log now records which AI answered. Groq's per-minute limit gets one short wait. A sample video passed. A fresh review found nothing blocking, and its fixes went in. The sample's title call failed on Gemini's side, a model overload like one that hit tonight's upload, so the error message now says why. A bet, built ahead of your answer.
- **Engineering:** the workflow change that gives the Groq key to the four jobs that make AI calls, and strips it from their saved logs, is #69, waiting on your label. #68 now points to it.
- **Product:** set the rule for switching to Groq before anyone can flip it. It changes the spoken closing line and which post runs, so it ships as its own version. Revert if watch time falls beyond the usual limit, or if titles fail on 4 or more of its first 20 uploads (Gemini: 3 of the last 30).
- **Market intelligence (this function's first work):** YouTube's policy page, read first-hand, allows "reaction videos where you comment". It refuses videos that "feel interchangeable", and "templated storylines … with minimal or no … commentary". It says nothing against synthetic voices. One Reddit-stories channel that used human voice actors was still demonetized in May 2026. So one quip per video, or a fixed opening and closing around the readings, is unlikely to pass alone; commentary would need to fill most of each video. My recommendation is on #55, and the host-storyline plan now carries the caveat.
- **Security:** the safety screen's two new test questions, which it had never seen, both got the right answer on Gemini (2 requests). That is the first sign the screen generalizes. Standing check clean: $0.21 spent on narration this month (forecast $0.96 of $3), money controls in place, no secrets in the project, no workflow change. The dependency warnings are unchanged, and they sit in the image library, which only reads our own files.
- **General management:** the product tracker had grown past its size limit; it is now shorter than at the start of the shift.
- Fixing against improving: mostly improving (the Groq route, its switch rule, the market read). Three small fixes rode along.

### Blocked
- **For you, in order of what they unblock:** the planning session and the vote's one sentence (#55); asking Reddit (#60); the Groq key and the label on #69, about ten minutes together, or telling us you are in the UK, EEA or Switzerland (#68); the music script (#66); the sample-video sentence (#65); the account checks (#59); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Check this morning's upload landed and is not a repeat.
- When the Groq key and #69 land: run the screen check on Groq and take a sample. Then switch on as its own version, by changing the code's default, never a workflow setting, under the rule above.
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, the first subscriber count, and the scorecard with private videos excluded.
- The workflow audit comes due in a shift or two (eight shifts since the last one).
- I handed over about 35 minutes early because nothing else cleared the bar. Considered and dropped: posting-time research (answered 30 September); title failures (none since the 4 October fix); a safety check in the upload step that practically cannot fire and would need its own sample; a draft to Reddit (one is on #60 already); closing old digest issues (your email channel); pre-building the Groq switch (two lines, and it cannot be checked without the key).
- Process: a background reviewer reads the shared working copy, so switching branches while it runs can show it the wrong code. It coped this time; next time, give it its own copy.

### Better?
- **Than last shift:** Yes, slightly. The Groq route went from a branch to the live code, so switching it on needs only your ten minutes, and bet 1 has outside evidence on how big it must be.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a first step and a rule, and the AI-limit and AI-training problems have a free fix merged and waiting on a key. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-08 (17:53) — You asked for another way to keep Reddit posts out of AI training: one is found, free, and built switched off

    Worked (% of the shift): engineering 35 · legal 25 · data 20 · gm 15 · security 5

**Summary:** You turned down paying for Gemini (#62) and asked for another solution; the morning shift missed that. Groq's free tier bans training on what we send, in its contract, and it is built into the code switched off; your ten minutes on #68 is all it needs. It brings no revenue directly, but it removes one way our use of Reddit breaks Reddit's terms. It also lifts the 20-a-day AI limit that has shaped half our plans.

### Toward revenue
- **Nothing directly.** The Reddit risk stands until Reddit answers (#60), but this takes away the part we can fix ourselves. And Groq allows about 100 of our requests a day against Gemini's 20. That limit ruled out the topic ranker reading every candidate post, and four uploads a day has to fit inside it.

### Done
- **Legal:** read each provider's own terms. Groq bans training on inputs by contract, even on the free tier. Cloudflare's free tier does not train either, and is a fallback at about 60–75 requests a day. GitHub's free models were retired in July, and Cerebras offers only a 30-day trial. Google's no-training terms need a billing account, unless the account holder is in the UK, the EEA or Switzerland. If that is you, say so on #68: nothing may need to change, and it also answers TikTok's country rule.
- **Engineering:** tried an open AI model running on our own GitHub machine, so no text leaves it. It took 7 to 53 seconds a call and got the safety screen's five standing cases right. Its titles were clearly weaker, so it is a fallback, not the answer. Then built the Groq route into the code, switched off: until a shift flips it, every request is unchanged, and a key alone changes nothing. It stays on a branch: a sample video was barred so near the evening upload. A fresh review found nothing blocking; I made its quick fixes, and the rest wait for the switch-on. A bet.
- **Engineering:** the safety screen's daily check only uses questions that are written into the screen's own instructions, so passing it shows memory, not judgement. On the branch, two new questions now run whenever we test a different AI. A fix.
- **Data:** the channel's scorecard stops counting videos you made private as "buried". This matters now: the scorecard's one red flag is exactly that count (2.4% to 5.6%). From 12 October it is read on the same terms as every other report. Reviewed, merged. A fix.
- **General management:** recorded your #62 decision under the standing ruling against new costs (it still holds), and corrected the risk register. Fixed the tracker check that read "spending" as "pending" and so flagged a closed issue as still open. The three items you approved (#65, #53, #50) still each need a step from you (unchanged since the morning).
- **Security:** standing check clean. $0.21 spent on narration this month (forecast $0.96 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: three fixes, one bet (the Groq route). Nothing changed in a video: every change to what we ship waits on you or on 12 October.

### Blocked
- **For you, in order of what they unblock:** the planning session and the vote's one sentence (#55); asking Reddit (#60); the Groq account and key, or telling us you are in the UK, EEA or Switzerland (#68, about ten minutes); running the music script (#66); pasting the sample-video sentence (#65); the account checks (#59); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Check tonight's upload. It had not run at hand-over (yesterday's ran at 18:58). It is the repeat guard's first live run: the post must not be one we have uploaded before.
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, the first subscriber count, and the scorecard with private videos excluded.
- When you answer #68: attach the workflow change for your label, run the screen check on Groq, take a sample video, and switch it on only if the screen does as well as Gemini.
- A slip of mine cost about 8 minutes: a wait loop matched its own command and never ended. Nothing else was affected.

### Better?
- **Than last shift:** Slightly. A decision of yours that had gone unseen became a ready, priced answer, and the only free AI route that fixes the training problem is built.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a first step and a rule to read it by, and the AI limit that kept forcing workarounds now has a free way out. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.
