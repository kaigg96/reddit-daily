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

## 2026-10-08 (17:53) — You asked for another way to keep Reddit posts out of AI training: one is found, free, and built switched off

    Worked (% of the shift): engineering 35 · legal 25 · data 20 · gm 15 · security 5

**Summary:** You turned down paying for Gemini (#62) and asked for another solution; the morning shift missed that. Groq's free tier bans training on what we send, in its contract, and it is built into the code switched off; your ten minutes on #68 is all it needs. It brings no revenue directly, but it removes one way our use of Reddit breaks Reddit's terms. It also lifts the 20-a-day AI limit that has shaped half our plans.

### Toward revenue
- **Nothing directly.** The Reddit risk stands until Reddit answers (#60), but this takes away the part we can fix ourselves. And Groq allows about 100 of our requests a day against Gemini's 20. That limit ruled out the topic ranker reading every candidate post, and four uploads a day has to fit inside it.

### Done
- **Legal:** read each provider's own terms. Groq bans training on inputs by contract, even on the free tier. Cloudflare's free tier does not train either, and is a fallback at about 60–75 requests a day. GitHub's free models were retired in July, and Cerebras offers only a 30-day trial. Google's no-training terms need a billing account, unless the account holder is in the UK, the EEA or Switzerland. If that is you, say so on #68: nothing may need to change, and it also answers TikTok's country rule.
- **Engineering:** tried an open AI model running on our own GitHub machine, so no text leaves it. It took 7 to 53 seconds a call and got the safety screen's five standing cases right. Its titles were clearly weaker, so it is a fallback, not the answer. Then built the Groq route into the code, switched off: until a shift flips it, every request is unchanged, and a key alone changes nothing. It stays on a branch: a sample video was barred so near the evening upload. A fresh review is running; its findings go to the next shift. A bet.
- **Engineering:** the safety screen's daily check only uses questions that are written into the screen's own instructions, so passing it shows memory, not judgement. On the branch, two new questions now run whenever we test a different AI. A fix.
- **Data:** the channel's scorecard stops counting videos you made private as "buried". This matters now: the scorecard's one red flag is exactly that count (2.4% to 5.6%). From 12 October it is read on the same terms as every other report. Reviewed, merged. A fix.
- **General management:** recorded your #62 decision under the standing ruling against new costs (it still holds), and corrected the risk register. The three items you approved (#65, #53, #50) still each need a step from you (unchanged since the morning).
- **Security:** standing check clean. $0.21 spent on narration this month (forecast $0.96 of $3), money controls in place, no secrets in the project, no workflow change.
- Fixing against improving: two fixes, one bet (the Groq route). Nothing changed in a video: every change to what we ship waits on you or on 12 October.

### Blocked
- **For you, in order of what they unblock:** the planning session and the vote's one sentence (#55); asking Reddit (#60); the Groq account and key, or telling us you are in the UK, EEA or Switzerland (#68, about ten minutes); running the music script (#66); pasting the sample-video sentence (#65); the account checks (#59); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- Check tonight's upload. It had not run at hand-over (yesterday's ran at 18:58). It is the repeat guard's first live run: the post must not be one we have uploaded before.
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, the first subscriber count, and the scorecard with private videos excluded.
- When you answer #68: act on the review's findings, attach the workflow change for your label, run the screen check on Groq, take a sample video, and switch it on only if the screen does as well as Gemini.
- A slip of mine cost about 8 minutes: a wait loop matched its own command and never ended. Nothing else was affected.

### Better?
- **Than last shift:** Slightly. A decision of yours that had gone unseen became a ready, priced answer, and the only free AI route that fixes the training problem is built.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a first step and a rule to read it by, and the AI limit that kept forcing workarounds now has a free way out. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.

## 2026-10-08 (11:00) — A bug that would have repeated uploads at four a day is fixed, so that test can start once you approve it

    Worked (% of the shift): data 40 · reliability 35 · gm 15 · security 10

**Summary:** The four-a-day test is our one views lever with evidence. It would have uploaded the same Reddit post twice most days, and that is now fixed in the live code. From 12 October shifts can also tell buried uploads from private ones without YouTube access. Neither changes a video, so the company is no nearer revenue today, but the step toward it has one obstacle fewer.

### Toward revenue
- **Four a day no longer needs a fix first.** The pipeline remembered only the last upload. At four a day one subreddit is drawn four times in a row, so a post still at the top of Reddit's daily list would have gone out again two runs later. This already happened once, on 20 July, when an extra run came between two scheduled ones. Every run now skips any question we have ever uploaded. Starting four a day still waits on you, in the planning session (#55), because it adds narration spend.
- **Supply does not hold four a day back.** AskReddit alone leaves 4 to 8 usable posts in its daily top ten (6 typically), so one subreddit can feed four uploads a day. On its thinnest days the fourth run would have one post left, so the four-a-day change should also widen the list each run reads. That costs nothing.

### Done
- **Reliability:** the repeat fix above, now in the live code. A fresh review found nothing blocking, and I fixed its two small gaps. It also found that two video runs can still overlap if a manual run lands during a late scheduled one, which this guard cannot see. That is rare at two a day. The fix is one line in a workflow file only you can apply, so it goes with the four-a-day change rather than as a separate ask now. A fix.
- **Data:** the weekly statistics now record whether each video is public or private. This costs no extra request: it comes back with a call the job already makes. From 12 October the zero-view report runs without access to YouTube, and the release reads stop counting your private videos as buried. So last week's rise in uploads stuck at zero views (5.6% against 2.4%) can be read properly then. Two fixes, each reviewed.
- **Data:** the safety screen's weekly check passes. It skipped 4 of roughly 90 posts since late August (4%, well under the 15% at which we would loosen it), the last on 12 September. None looks wrong: two medical-horror questions, one about bar violence, one flirt question.
- **General management:** you approved letting a sample video run near an upload (#65), but shifts cannot edit their own rules file, and automatic apply only covers workflow files. I left a note on the issue: it needs you to paste the one sentence. Separately, the health check raised an issue (#67: shifts using about half their time). I added why: all three stopped because nearly everything that would change what we ship waits on you or on the 12 October numbers. The fix is the planning session, not longer shifts. I also deleted a leftover work branch whose changes you applied on 6 October, so it no longer looks like unfinished work.
- **Security:** standing check clean: $0.21 spent on narration this month (forecast $0.96 of the $3 budget), money controls in place, no secrets in the project, no workflow change since the music fix you approved.
- Fixing against improving: all fixes this shift. They clear the way for a bet (four a day) and for the 12 October reads. Nothing new was tried on the channel, because every change to what we ship waits on you.

### Blocked
- **For you, in order of what they unblock:** the planning session and the vote's one sentence (#55); asking Reddit (#60); running the music script (#66, about two minutes); pasting the sample-video sentence you approved (#65); Gemini's paid tier (#62); the account checks (#59); re-running the comments change (#53); the auto-apply patch (#50).

### Next
- 12 October: read v7 under its rule; then the engaged-view, narrator, dark-morbid and zero-view questions, and the first subscriber count. Check that snapshot carries the new privacy column; the zero-view question can then be read offline.
- Check tonight's upload landed and is not a question we have uploaded before (the repeat fix's first live run).
- When four a day is approved: widen the list each run reads, and bring you the one-line overlap fix as a ready-made patch.
- I handed over about 35 minutes early because nothing else cleared the bar. Considered and not taken: a search for a properly licensed source of short crowd answers in case Reddit says no (it would most likely confirm Stack Exchange again, already on record; worth redoing once Reddit answers you); getting four a day's workflow change ready now (it waits on the subreddit read until about 2 November, and a ready-made change could go stale by then); the topic ranker's rule (it rests on the dark-morbid read due 12 October); a trademark check on the working name (waits on bet 1, as planned).

### Better?
- **Than last shift:** Slightly. The volume test lost a hidden blocker, and the 12 October reads gained a missing piece. No video changed.
- **Than ~10 shifts ago:** Somewhat. Both views bets have a ready first step and a rule that can read it, and the second now has a safe pipeline. Views per upload are still below August's.
- **Than ~100 shifts ago:** Too early to say.
