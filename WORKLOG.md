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

## 2026-10-30 (23:25) — The release check was spending 6 of our uploads' 20 daily AI requests re-checking a release that had not changed; fixed

    Worked (% of the shift): reliability 40 · gm 40 · legal 10 · editorial 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. The daily check of the next release had re-run every afternoon since 25 October on a release that had not changed, using 6 of the 20 free AI requests our uploads share. It now runs only when the release changes, or weekly, as designed.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting what we publish.** Each upload's title, closing line and safety screen draw on that allowance of 20 a day. The check took 6 of them a few hours before each evening upload. Running out cost an upload its title on 20 September. It also matters for four uploads a day: our plan says four fits the allowance, but it never counted this.

### Done
- **Reliability (fix, live):** a fresh agent's round of ideas found it, and the build log confirmed it. The build machine knows the release only by its remote name, so the check could never tell that nothing had changed. Fixed and tested. A fresh review found no defects; its one test gap is closed. Merged 23:12. The release's sample tags now print when it changes or weekly, not daily.
- **General management (fix, live):** the check that catches the plan calling finished work "pending" could never fire, for the same reason and because it looked for old branch names. A fresh review then found that fixing it would have woken a second fault: it read the start of each paragraph, not the words beside the work it names. Both fixed and tested; today it finds nothing stale.
- **Legal (check):** the stock-footage licence bars reselling clips on stock or wallpaper sites and selling unaltered copies. Keeping our five clips in our public project is neither. Recorded beside the credits.
- **Editorial (check):** this evening's upload asked about Patrick Stewart's death. Major outlets confirm he died on 28 October, so we did not spread a false claim.
- **General management:** no shift ran on 29 or 30 October. The weekly shift allowance was spent by the evening of the 28th (228 units over 15 shifts, against a ceiling near 200), so five shifts were skipped. It also tripped a day early the week before (210). Nothing was lost, since everything waits on you. But the breaker meant to catch a runaway shift now sets the weekly pace, as the average shift rose from about 11 units to 15. Recorded for the 5 November review, so this shift stopped once nothing above the bar was left rather than spend a later shift's allowance.
- **General management:** nothing was ready. A fresh agent proposed eight ideas from the data. Two rankers, in opposite orders, put the release check first and the licence second. **Dropped:** counting AI requests per day (the logs do not print them, and the fix removes the uncounted share); logging why a title was refused (bet 1's release rewrites that code, so it is in the technical list for after it); updating our Reddit library (its new version adds nothing for Reddit's API change); a shorter list of dropped ideas, and compressing the findings section (both already proposals for the 5 November review); recording the Claude plan (it changes no decision).
- **Reliability:** all five uploads since the last shift landed. On the 29th one shipped the Reddit question as its title, as designed, after the shock-phrase guard refused the AI's.
- **Security:** the standing check is clean: no secrets in the project, no workflow changes, money controls in place ($0.87 this month, forecast $0.90 of $3).
- **Product:** bet 1 is still ready the day you label it: tonight's live code and the release combine with no conflicts, and all 942 checks pass.
- Two fixes live, three checks. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; bet 2's window for it opened today and closes about 6 November); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **Tomorrow's release check (about 13:00–15:00 UTC):** its build log should say it skipped, as already validated. If it ran, read why.
- **2 November snapshot:** as the 28 October (17:44) handover says: refused figures first, then the views rule, the subreddit test, the title-style test and the voice question, each with its fairness check and rule as written. The zero-view guardrail: a second breach is a decision's revisit trigger.
- **If #77 is labelled:** merge the release, then the counting fix, set the live format to v8 in the product plan, and close #77.
- **5 November monthly:** the audit's proposals, plus the weekly shift breaker now setting the pace.
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. Yes for the uploads' margin: 6 of 20 daily AI requests are back.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-10-28 (17:44) — The process audit: unchanged since 25 October, the company waits on bet 1; a gap that could have leaked a token into a public file is closed

    Worked (% of the shift): gm 45 · security 15 · reliability 15 · legal 10 · engineering 10 · editorial 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly. Bet 1 still waits on your label (#77). The process audit came due and found the same picture as three days ago: shifts keep the system safe while the one change that matters waits on you. It also found and closed a gap that could have put a working token into a public file.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Bet 1 is ready the day you label it.** Today's live code, the release and the counting fix built beside it combine with no conflicts, and all 936 checks pass.

### Done
- **General management (the audit, due after about ten shifts):** eight shifts since 25 October ran 26 to 61 minutes of 60 (38 on average, as before). Six of eight were fixes, and the two changes viewers saw were protective. Of the last audit's findings, the self-grading is fixed (these reports now answer "No for viewers" first); the rest stand because they wait on bet 1 or on you. New: the product plan's findings section has nearly doubled in ten days and nothing caps it; these reports run about 1,000 words, so only the last two survive for the next shift; six ideas were dropped twice by different shifts; and a recommendation to you went in before its premise was checked (below). Every decision was re-tested and dated; one, settled in the rules, was cut to a line. Proposals go to the 5 November review, not to you now.
- **Security (fix, live):** a helper agent printed the build machine's settings, keys included, into its own working notes. Nothing left the session: the build page hides agent output, and the record each shift commits lists only the shift's own steps. But checking that record showed one token, the machine's own GitHub token, would only have been partly blanked if a shift had ever printed it. Fixed, tested, reviewed and live. No key needs changing.
- **Reliability (check):** a networking component under YouTube's libraries updated at 10:21 this morning, and Monday's job and every upload install it fresh. It only drops a distrusted certificate Google does not use; every Google service we call works on it, and every check passes on Monday's exact versions.
- **Legal and editorial (question closed):** 12 old videos repeat another word for word. I first recorded them as worth removing; a second check found them already private since at least 12 October, so I corrected it within the hour. Other repeated questions read different answers. Nothing to do.
- **General management (your decisions):** our rule on slow answers came due. On 27 October you approved two process items within hours and passed over #77 and #80, so the delay is in asks needing a judgement or a watch, not absence. No re-ask. The tool listing your open questions now says when you last acted, so this check takes one line (reviewed, live).
- **General management:** nothing was ready. Two rounds of ideas, ranked in opposite orders, gave the library check and the duplicate count. **Dropped:** bet 1's "no tags on fallback days" option before you ask (the rankers split); removing YouTube's text from an old file (5 November decides); filling 82 missing topics and a list of 2 November's rules (change no decision); tying approvals to their issue (your workflow file). A second round sought anything that changes what we ship or earn without disturbing the running tests or needing you: playlists, descriptions, the language setting, more music, a new source. Each failed on a recorded finding, the tests, or you: only #77 changes what we ship.
- **Security:** the standing check is clean; money controls in place ($0.79 this month of $3).
- **Reliability:** this morning's upload landed. The safety screen skipped 1 post in two months, far under its review line. This afternoon's upload had not started by the handover.
- Two fixes live, one audit, two checks, one closed question. AI use: none from the upload allowance; no Polly; no render.

### Blocked
- **For you, in order:** #77 (one label ships bet 1; by about 30 October to 6 November for bet 2 to run as planned); #65 (a "yes" lands the corrected sentence); #82 (register our Reddit app by 12 January); #80 (four a day waits for bet 1 until you answer); #59 (the account checks); #50 (your hands, on a workflow file).

### Next
- **This afternoon's upload** is the first on today's code and on this morning's library update: check its log row, and that the run shows no warning.
- **2 November snapshot:** first check that the Monday check-in names no figure YouTube refused, and read each test's warnings before its verdict. Then the views rule, the subreddit test, the title-style test and the voice question (it reads engaged views); each should have enough videos. Before the voice read, run the fairness check its rule names, counting only the uploads that read will see. Apply each rule as written and record each read in the ledger. Read the scorecard's zero-view guardrail again: a second breach is a decision's revisit trigger.
- **If #77 is labelled:** merge the release, then the counting fix (both rehearsed today), set the live format to v8 in the product plan, and close #77. If you ask for no tags on fallback days, build that first (the technical list says how).
- **5 November monthly:** the audit's proposals (the technical list): compress and cap the findings section, a length cap for these reports, one decision ready to retire into the rules, with the bundle carried from 25 October.
- **7 November:** if #77 is still open, render a fresh sample before the current one expires on the 8th.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: one token can no longer leak through the shift record.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
