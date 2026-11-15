# E1 · The show after Reddit
Status: active
Function: Strategy, Product management
Deadline: 2027-01-12 (Reddit refuses our requests from that day; cut over by 2027-01-05)
Measure: uploads continue past 12 January, on a show chosen by a comparison, not by default
Rule: T5 writes the choice rule into the experiment ledger before the new show's first upload; T9 applies it by 2026-12-20

## Why now

The owner will not register the Reddit app (2026-11-14, #82), so the show we
upload today ends on 12 January. Every plan this quarter assumed Reddit.
A replacement exists, built and switched off: our own question with three
takes (`src/ownquestions.py`, PLAN C16). Nothing has yet asked whether viewers
watch it.

## The decision

Made in the owner's session on 2026-11-15 by their assistant, on the repo's
records, without watching a video. **The first orchestrating shift should have
a fresh agent argue against it (`ORG.md`, Decide) and may overturn any part on
evidence.**

1. **The eight weeks of Reddit left are a control arm, not a runway.** After
   12 January there is nothing to compare a new show with, and views swing
   27–50% week to week with nothing changed (PRD §4), so a before-and-after
   read will say nothing. Run the new show beside the Reddit one now, one
   upload a day each, and choose on a same-weeks comparison.
2. **Ship bet 1's no-reactions build now, as the Reddit arm's last form, and
   do not hold slots for its own read.** It waited a month; its code carries
   work other items need; and it gives both arms the same closing "pick", so
   the comparison isolates the source. Its verdict will be thin by design
   (about one Reddit upload a day). Auto-revert still guards it.
3. **Three takes written by a model is the fallback that guarantees
   continuity, not yet the show.** The shifts' own market read names the gap:
   the question-led channels that get paid are quizzes, and "a quiz has answers
   to play along with, which ours lacks" (PRD §4, 2026-10-31). A viewer of today's
   show stays for what real people said. A viewer of three machine-written
   stances has no crowd, no stake and no reason to wait for the end. So test
   at least one **play-along** form against it: a question, a beat to guess,
   then a reveal that is true and comes from somewhere real.
4. **Continuity is the floor.** If nothing is decided by 20 December, the
   built show goes to every slot on 5 January. Uploads do not stop.

**Rejected:** bake bet 1 alone for four weeks first (its answer arrives in
mid-December about a format that ends in January, and leaves no time to
compare anything); switch cold on 12 January (no baseline, no fallback); Stack
Exchange (about 1.6 usable questions a day and still a reading, PRD §4).

## Out of scope

Four uploads a day (PRD §0 #4): it stays off until T9, so bet 2's window
(30 November to 27 December) will be read at today's volume. Say that in the
quarter's verdict; it is a consequence of this decision, not a failed lever.
Voice changes (#16). Anything that spends beyond #72's approved narration line.

## Assumptions to check

1. `integration/preview` (`b1190de`, sampled and reviewed 11-13) still merges
   cleanly and its release check passes.
2. The source can alternate by slot in code, as subreddits do
   (`content.subreddit_for_run`), with no change to the upload workflow, which
   only the owner's label can change.
3. A third daily upload, if T8 wants one, is inside #72's approved spend and
   the $3 AWS budget. If `money_check.py` disagrees, it does not happen.
4. One music track on every upload is the trait we share with YouTube's
   example of mass-production (PLAN §4). T2 removes it before a model-written
   show uploads daily.

## Tickets

### T1 · Bet 1's no-reactions build is live as the Reddit arm's last form
Status: ready
Needs: none
Touches: src/ (by merge of `integration/preview`), PRD.md §0 #15 and #13, the experiment ledger
Context: decision 2. The build, its sample and its review are described on #77 (closed). The release check must pass on the day; `FORMAT_VERSION` becomes `v8`. Its pre-committed rule stays as written; add one ledger line that its read is thin by design from T4 on.
Accept:
- [ ] `scripts/validate_release.py` passes for the merged tree, and tests are green
- [ ] the first `v8` upload is in `upload_log.csv` with its host pick as the closing line
- [ ] PRD §0 no longer says #15 waits on a label; the ledger carries the line above
Evidence:

### T2 · More than one music track, with no login needed
Status: ready
Needs: none
Touches: assets/music/, src/video.py, tests/, a licence note beside the tracks
Context: assumption 4. Today's track is from YouTube's Audio Library, which needs the owner's login and may not be shared, so it is sealed. Find at least three more tracks that are public domain or CC0, or make them with our own code as `scripts/make_sfx.py` makes effects. `video._pick_music` already picks at random from the folder. A track changes the video for every arm alike, so it does not disturb the comparison.
Accept:
- [ ] at least four tracks in rotation, each with its source and licence text recorded in the repo
- [ ] no track needs a login, a payment or an attribution we cannot give in the description
- [ ] a test shows the picker never chooses the track of the last upload in `upload_log.csv`
- [ ] if no such track can be found, that is recorded and the ticket is dropped, not left open
Evidence:

### T3 · Every upload records which show it was
Status: ready
Needs: none
Touches: src/log.py, src/run.py, scripts/weekly_analytics.py, src/insights.py, tests/
Context: the log has no column for the source; an own-question upload is known only by an empty `subreddit`. The comparison needs `report.py --compare show=<name>` with ages matched, like every other read (`CLAUDE.md` §6).
Accept:
- [ ] `upload_log.csv` gains a `show` column (`reddit`, `takes`, later others); old rows read as `reddit`
- [ ] `scripts/report.py --at-age 7 --compare show=takes` runs and refuses thin cohorts as it does elsewhere, with a test
- [ ] the append-only log's existing rows are unchanged byte for byte
Evidence:

### T4 · The show alternates by slot, in code
Status: todo
Needs: T3
Touches: src/content.py, src/config.py, src/run.py, tests/
Context: assumption 2. Mirror `content.subreddit_for_run`: one Reddit and one new-show upload a day, each show getting the morning and the evening slot equally over two days. Merged switched off behind a constant, so T5 is one line.
Accept:
- [ ] a test shows that over any 14 days each show gets 14 uploads, 7 in each slot
- [ ] `DRY_RUN=1` produces a playable video for each show
- [ ] with the constant off, behaviour is unchanged (existing tests pass untouched)
Evidence:

### T5 · The three-takes show uploads once a day, under a rule set first
Status: todo
Needs: T1, T2, T4
Touches: src/config.py, the experiment ledger, PRD.md §0, PLAN.md C16
Context: the show is built and merged off (11-15); the switch-on is prepared on `strategy/own-switch-on`, its pre-merge items in TECH_DEBT. Write the choice rule before the first upload: the primary measure (engaged share at 7 days, D9), the gate, the minimum uploads a side, the chance gap `report.py` prints, and the tie rule, which is decision 4.
Accept:
- [ ] the ledger row for the rule is committed before the first `takes` upload's timestamp
- [ ] a `takes` upload is live, labelled as takes, naming nothing of Reddit's
- [ ] the date of the read is in PRD §0
Evidence:

### T6 · We know whether a play-along show has a clean, daily supply
Status: ready
Needs: none
Touches: PRD.md §4
Context: decision 3. One shift at most. A guess needs a true answer that is ours to use. Check first-hand, quoting the terms: statistics published by governments that place them in the public domain, and datasets released under CC0 or CC BY. For each: what a viewer would be asked to guess, how many usable episodes a day, and whether commercial use is allowed. Reddit, and anything scraped against a site's terms, is out.
Accept:
- [ ] PRD §4 records each source read, its licence quoted, and its daily supply
- [ ] three example episodes are written out: question, the beat to guess, the reveal, the credit line
- [ ] a verdict: build T7, or drop the play-along form because no source allows commercial reuse with at least two episodes a day
Evidence:

### T7 · A play-along episode exists as a sample a viewer could follow
Status: todo
Needs: T6
Touches: src/ (a new source beside ownquestions.py), tests/
Context: only if T6 says build. The number or answer in the reveal is copied from the source record by code, never written by a model. Write the viewer's bar before rendering (D14): can someone who has never seen the channel tell what to guess, and is the reveal worth the wait.
Accept:
- [ ] a test fails if the revealed value differs from the source record
- [ ] a free sample render (`SAMPLE=1`) and one narrated dry run are playable
- [ ] a fresh agent, shown the frames and the script but not the bar's author's notes, judges it against the bar; its findings are fixed or recorded
Evidence:

### T8 · The play-along show uploads as its own arm
Status: todo
Needs: T5, T7
Touches: src/content.py, src/config.py, the experiment ledger
Context: three shows cannot each reach a readable count on two uploads a day before 20 December. Decide between a third daily upload (assumption 3) and giving this show half of the takes arm's slots, using the chance gaps `report.py` prints; write the choice and why.
Accept:
- [ ] the arm's rule is in the ledger before its first upload
- [ ] the slot plan gives every arm both slots equally, with a test
Evidence:

### T9 · The 12 January show is chosen
Status: todo
Needs: T5
Touches: the experiment ledger, DECISIONS.md, PRD.md §0, PLAN.md
Context: by 2026-12-20, apply the rule from T5 (and T8 if it ran) exactly as written. A Decide: evidence, the alternative rejected, a fresh agent arguing against it.
Accept:
- [ ] the rule is quoted before any number, and the choice follows from it
- [ ] if the rule cannot tell the shows apart, decision 4 applies and the record says so
Evidence:

### T10 · Uploads no longer need Reddit
Status: todo
Needs: T9
Touches: src/config.py, src/run.py, tests/, README.md
Context: by 2027-01-05, a week clear of the cutoff. `tests/test_reddit_cutoff.py` already proves a refused request cannot cost money or duplicate an upload.
Accept:
- [ ] seven days of uploads with no request to Reddit in any run log
- [ ] descriptions and tags name nothing of Reddit's
- [ ] PLAN C16 is closed and the risk row for Reddit's API leaves PLAN §4
Evidence:

### T11 · The channel stops carrying Reddit's name
Status: todo
Needs: T9
Touches: PLAN.md C12, `.escalations/`
Context: the channel's name uses Reddit's, and from January the show has nothing of Reddit's in it. A rename is a one-way door and needs the owner's login: a dated notice (`escalate.py --notice-days`), then one ask with the exact name and steps. The fate of the 1,041 old readings (C12) is decided with it, also by notice.
Accept:
- [ ] the name's trademark, handle and domain checks are recorded
- [ ] the notice is raised, and the ask can be done from a phone in two minutes
Evidence:
