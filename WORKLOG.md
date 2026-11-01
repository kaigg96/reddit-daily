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

## 2026-11-01 (17:45) — Election week could have failed an upload outright; the fix waits only for its sample. A lasting upload alarm is built, and this morning's #86 ask is very likely not needed

    Worked (% of the shift): reliability 40 · editorial 30 · gm 20 · market 5 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Two upload risks in the unwatched days around the election are now covered or ready: a run that finds no usable question, and a missed upload whose run never started, which no email reports.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the uploads.** Around results day, Reddit's top questions may nearly all be about the election, which we skip. Today such a day fails the run and loses that upload. The fix is built and reviewed. It needs one sample video, which the rules allow from tomorrow at 11:17.

### Done
- **Editorial (fix, ready):** when the election skip leaves none of the day's top 10 questions usable, or our safety check rejects the few that are left, the run now reads the day's top 30 instead of failing. The same filters and the same cap on AI checks apply. An ordinary day is unchanged. NoStupidQuestions sometimes has only 2 usable questions out of 10 even without the skip. Its first review found no fault and two gaps, both now fixed. Uploads that came from the deeper list are marked, so they cannot blur a running test. 713 checks pass.
- **Reliability (built, for the monthly):** a check in the shift job, which runs on your schedule three times a day even when the shift allowance is spent. If fewer than 2 uploads landed in 28 hours, or a scheduled upload run failed, it fails that job, so GitHub emails you. Replayed over the 95 shift runs since 20 September, it raised no false alarm and caught the one real miss, on 5 October. A fresh review found two gaps, both fixed. It is on main but does nothing until your label adds one step to the shift job. To save you a separate email, that step joins the single proposal the monthly review brings you.
- **Reliability (correction, by edit, no email):** this morning's #86 said a failed upload emails no one. That is very likely wrong. GitHub's documentation sends the email to whoever changed the schedule, and GitHub still names you on every scheduled upload run since 11 October. The automatic approver pushes with a personal token, so to GitHub the change was yours. I cannot see who gets the emails, so this is not proof. #86 now says no action is needed.
- **Market (checked):** Reddit stops its public RSS feeds on 13 November. We read Reddit through its registered API, not RSS, so this does not touch us. No new YouTube monetization rule since July turned up.
- **Editorial (answered):** the election skip reads titles only. In 993 past videos, 5 had an election word only in an answer, and none of those was about when or how to vote. So answers need no screening.
- **General management:** nothing was ready. A fresh agent proposed 8 ideas and I added one. Two rankers, reading them in opposite orders, both put the election fallback and the lasting alarm first and second. Dropped: re-checking Monday's libraries (none has a new release since 28 October); a security audit of our libraries (six days after the last one); a check on quoted review dates (no effect on any decision); fixing a comment about the clock change (no shift starts in that hour); tallying hype-word titles (the wider guard waits for bet 1's release, so a count now changes nothing).
- **Reliability, security:** this morning's upload landed; this evening's had not started when I handed over (it usually starts between 17:15 and 18:30). No workflow changed. Money controls are in place ($0.89 this month, forecast $0.90 of $3).
- AI use: none from the upload allowance; no Polly; no sample video (the 12-hour cap).

### Blocked
- **For you, in order:** #77 (one label ships bet 1); #82 (register by 12 January; check the app's name first); #86 (very likely not needed: close it); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Tomorrow's 11:17 shift, first thing:** request the election fallback's sample video and merge it on a pass, before the polls close on 3 November. It is the only ready item.
- **The weekly, then the November monthly:** the monthly's bundled proposal now also carries the upload alarm's one-step change.
- **Once the alarm's step lands:** check that the shift job printed "uploads ok", then close the technical-list item.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: a results-day upload no longer fails once the fix merges, and a lasting alarm is one label away.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.

---

## 2026-11-01 (10:27) — A failed upload has emailed no one since 11 October, and two clicks of yours fix it; election week's fuller skip is live

    Worked (% of the shift): reliability 30 · editorial 20 · gm 20 · legal 15 · data 10 · security 5

**Summary:** Nothing viewers see changed and nothing moved revenue directly; bet 1 still waits on #77. Since 11 October a failed upload would have emailed no one, which matters most when the shift allowance runs out around 4 November; #86 asks you for the two clicks that fix it. Election week's skip now also catches questions about polls, live from today.

### Toward revenue
- **Nothing directly.** Everything viewers would see still waits on bet 1 (#77). The channel is flat at 12 seconds watched per view.
- **Protecting the uploads and their source.** A failed upload reaches you again once #86 is done. Reddit's terms bar its name from our app's name, so #82 now says to check that before you register.

### Done
- **Reliability (found, for you):** GitHub emails a scheduled job's failures to whoever last changed its schedule. On 11 October our automatic approver applied your four-a-day approval, so the last editor is now a bot, and the upload job has no alert of its own. Nothing has failed since; the last failure, on 5 October, did reach you. Shifts are the only other check, and none runs once the weekly allowance is spent (29–30 October, and again about 4 November). #86 gives the fix: in the Actions tab, disable the upload job and enable it again straight away. A later approved schedule change would repeat it; that is recorded.
- **Editorial (fix, live):** election week's skip now also catches "polls" and "electoral", and logs each post it skips. A fresh review found no fault, and all 707 checks pass. Across 211 past uploads it would skip nothing more than before. Its sample passed; it is live from this evening's upload.
- **Editorial (check):** this morning's upload, on makeup, makes no claim about voting.
- **Legal (for you, no email):** Reddit's developer terms (section 5.3) forbid its name "in the name of your App". We cannot see our app's name, and this project's own name is reddit-daily. #82 now tells you to check the name before you register, and to rename the app if it says "reddit". I edited the issue, so no email.
- **Data (recorded before any read):** bet 2 starts from 8,300 views over four weeks, the lowest of the 11 four-week stretches since July; the middle one is 11,212. So its bar of 16,600 is about one and a half times a typical stretch, not double. It is in the test ledger, so December's read cannot overstate a pass.
- **General management:** nothing was ready. A fresh agent proposed 8 ideas; two rankers, reading them in opposite orders, both put the failure emails first, then the Reddit name check and a read-only key. Dropped: a read-only key for Monday's figures (both jobs can reach every secret, so it closes nothing); what the new country figures would change (at 757 times short, nothing); a plan for bet 1 missing 6 November (the monthly's, after the date); whether long shifts produce less (too big, and your call). One shift's cost row was missing (31 October, 16:05): its run stopped after 18 minutes with no usage figures. That is 1 of the last 60 runs, so the weekly count is one shift short.
- **Reliability, security:** all uploads since the last shift landed. No workflow changed; money controls in place ($0.89 this month, forecast $0.90 of $3).
- AI use: none from the upload allowance; no Polly; one sample render, on the test model's allowance.

### Blocked
- **For you, in order:** #86 (two clicks, about a minute); #77 (one label ships bet 1; bet 2's window closes about 6 November); #82 (register by 12 January; check the app's name first); #65 (a "yes" lands the corrected sentence); #80 (four a day waits for bet 1); #59 (six account checks).

### Next
- **Election week:** the full skip is live, so the daily voting check ends; the skip lapses by itself after 10 November.
- **2 November, the weekly; then the November monthly; if #77 is labelled; 7 November:** all as the 31 October (22:29) entry says.
- **Once #86 is done:** close it, and the item in the technical list.

### Better?
- **Than last shift:** No for viewers or revenue. A little for safety: once #86 is done, a failed upload reaches you again, and your Reddit registration will not use a name Reddit's terms forbid.
- **Than ~10 shifts ago:** No for viewers: watch time is flat at 12 seconds and bet 1 has not shipped.
- **Than ~100 shifts ago:** Too early to say.
