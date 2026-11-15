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

**Challenged 2026-11-15 by a fresh agent, as asked; amended.** *Kept:*
decision 2, as the ledger's `v7s-before-bet1` (set 11-14) already accepts
cutting v7s's read, and decision 4. *Struck:* "auto-revert still guards it".
From T4 on, v8's AskReddit cut gains about one upload every two days, so its
20 may come after T9 (ledger `#15-thin`). *Decision 1, amended:* the 20
December read cannot decide. Takes start no sooner than T1–T4 (~11-20); the
14 December snapshot, the last before T9, sees uploads to ~12-07 at 7 days,
about 17 a side, under the 20 `RELEASE_MIN_UPLOADS` requires, and at 15 a side
the chance gap is 23% on watch-seconds and 35% on engaged share. So T9 will
refuse and decision 4 applies: takes take every slot on 5 January unless T5's
gate shows it failing. The takes arm before then is a shakedown, not the
choice. **The choice of show moves past the cutover:** takes against the
play-along form (if T7 passes its bar) and Stack Exchange (1.6 a day fills
one arm; real people's answers; a sample branch exists; costs: answers cut to
length, and share-alike lets anyone re-upload us), one upload a day each in
the same weeks, its rule written before the first upload, read in February.
*Rejected:* keeping 20 December as the deciding read (it cannot reach its own
minimum), and a third daily upload to hurry it (still too late). *Decision 3*
rests on one market read about who gets paid, not on our data; T7's viewer
bar is its test, and it takes no upload slot before the cutover.

## The play-along episode (design, 2026-11-15, for T7)

Written in the owner's session with Fable, on T6's supply read. The first
shift on T7 may amend it on evidence; the viewer bar (`process/viewer-bar.md`)
is the test, and this design is not shown to the agent applying it.

**What it is.** One question with a true, sourced answer that a stranger can
have an opinion about before they know it. The viewer is asked to commit (a
guess, a pick, a count) and then shown whether they were right. Everything
else serves that one beat. It is a quiz the way a bar bet is a quiz: the fun
is in being wrong about something you were sure of.

**Shape, about 15–22 seconds.**
1. **The hook (≤ 3 s, spoken and on screen):** the question, in the viewer's
   terms, with the thing to commit to. "Gas is $4.45 today. What did it cost
   in 1990?" Never a preamble, never the show's name, never "today we".
2. **The beat (2–4 s):** the invitation and the room to take it. One line:
   "Say your number." The screen holds the question and, for a pick, the two
   options. Music carries it; narration stops. This pause is the show. It is
   also where a viewer who does not care leaves, which is fine.
3. **The reveal (3–5 s):** the answer, as a number or a name, large, with the
   one comparison that makes it land: "$1.04. A quarter of today." The
   comparison is computed from the record (a ratio, a difference, a rank),
   never written freehand.
4. **The turn (2–4 s):** one spoken line that gives the answer meaning or
   points at the next guess: "Same gallon, same country. Thirty-six years."
   Then the question for tomorrow, in five words, as the closing line and the
   pinned comment. No "like and subscribe" (PRD §5 no. 9): the reason to come
   back is the next question.

**What makes it ours (check 5).** The question's framing, the pairing, the
comparison and the turn are the show's; the fact is the source's and is
credited in the description exactly as the source asks. No model writes a
number: `select` fetches the record, `render` copies it, and a test fails if
the shown value differs from the record (T7's first acceptance line).

**Choosing the question (the selector's rules).**
- **Guessable, not knowable.** A stranger can form a guess from everyday
  sense (prices, sizes, populations, heights, dates) but would not know the
  answer. Skip anything that needs expertise or that most people know.
- **A surprising distance.** For a number, the answer differs from the
  obvious guess by at least ×2 or ÷2 (prices over time, sizes across places);
  for a pick, the losing option is the one most people would choose, judged
  by a simple proxy the code can compute (the more populous, the more famous
  by Wikidata sitelinks). The selector rejects the rest; the shift logs the
  reject rate so the pool's size is known.
- **One fact, one unit, one comparison.** No episode needs two numbers to
  land. Units in the viewer's own terms (a gallon, a floor, a person).
- **Fresh shape.** Never the same template two days running (price-then,
  bigger-of-two, how-many) and never the same subject as any shipped title
  (the own-questions repeat check applies).
- **Nothing that invites contempt.** No question whose fun is someone else's
  poverty, illness or disaster (USGS quakes and weather extremes are out of
  the main rotation for this reason, not for supply).

**Series identity.** The closing line's "tomorrow" is the only series device
until the brand is settled (C12, T11). The watermark carries the channel's
name. A recurring sting or a host persona waits for the February read.

**The three samples.** T6's three episodes, in this shape, rendered free
(`SAMPLE=1`) and judged by a fresh agent against the bar before any narrated
render is bought. Two fails on the same check means the shape changes, not
the episode.

**Worked examples** (T6's three episodes in the shape; values as fetched
11-15, comparisons computed from the records). The script is what is spoken;
[screen] is what is shown.

1. *Hook:* "Gas is four forty-five a gallon today. What did it cost in 1990?"
   [screen: "$4.45 today · 1990: ?"] *Beat:* "Say your number." [screen holds
   3 s] *Reveal:* "One dollar four." [screen: "$1.04"] "Less than a quarter
   of today." [screen: "÷4.3"] *Turn:* "Same gallon, same country.
   Thirty-six years." *Tomorrow:* "Tomorrow: a dozen eggs, 1980."
   Credit: "Source: U.S. Bureau of Labor Statistics, series APU000074714."
2. *Hook:* "More people: Wyoming, or Washington, D.C.?" [screen: the two
   names] *Beat:* "Pick one." [screen holds 3 s] *Reveal:* "D.C."
   [screen: "D.C. 702,250 · Wyoming 587,618"] "By about a hundred and
   fifteen thousand." *Turn:* "A whole state, outnumbered by one city that
   isn't in one." *Tomorrow:* "Tomorrow: Vermont or Alaska?"
   Credit: "Source: U.S. Census Bureau, Vintage 2024 population estimates."
3. *Hook:* "How many floors does the Burj Khalifa have?" [screen: the
   name, "? floors"] *Beat:* "Guess." [screen holds 3 s] *Reveal:* "A
   hundred and sixty-three." [screen: "163"] "Sixty-one more than the
   Empire State Building." [screen: "163 vs 102"] *Turn:* "And it's
   been the tallest since 2010." *Tomorrow:* "Tomorrow: the longest
   bridge you can drive on." Credit: "Data: Wikidata (CC0), Q12495 P1101;
   Q9188 P1101."

The comparison in each is a second record or a ratio, never prose a model
invented; the "turn" is the one line the model may write, and it states no
number the records do not hold.

**Schema the renderer takes** (one JSON per episode, produced by `select`):
`{"hook": str, "beat": str, "options": [str, str] | null, "answer": str,
"comparison": str, "turn": str, "tomorrow": str, "source": {"name": str,
"id": str, "value": number | str, "fetched": date}, "credit": str}`.

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
Status: blocked: the 11-16 08:17 release check on `b74fc92` (carries `main` and T3; 1,335 pass); merge on a PASS naming it
Needs: none
Touches: src/ (by merge of `integration/preview`), PRD.md §0 #15 and #13, the experiment ledger
Context: decision 2. The build, its sample and its review are described on #77 (closed). The release check must pass on the day; `FORMAT_VERSION` becomes `v8`. Its pre-committed rule stays as written; add one ledger line that its read is thin by design from T4 on.
Accept:
- [ ] `scripts/validate_release.py` passes for the merged tree, and tests are green
- [ ] the first `v8` upload is in `upload_log.csv` with its host pick as the closing line
- [x] PRD §0 no longer says #15 waits on a label; the ledger carries the line above
Evidence: 11-15: `main` merged into `integration/preview` cleanly (`403fc90`), then T3 (`b74fc92`); 1,335 pass. The release check could not run the same evening (the 19:00 upload's hour). Ledger `#15-thin`.

### T2 · More than one music track, with no login needed
Status: review: `product/e1-t2-music` (`e1f8b5d`), unmerged; left: a listen, a fresh look at `e1f8b5d`, and its own `FORMAT_VERSION` timed against v8's read (one variable per release)
Needs: none
Touches: assets/music/, src/video.py, tests/, a licence note beside the tracks
Context: assumption 4. Today's track is from YouTube's Audio Library, which needs the owner's login and may not be shared, so it is sealed. Find at least three more tracks that are public domain or CC0, or make them with our own code as `scripts/make_sfx.py` makes effects. `video._pick_music` already picks at random from the folder. A track changes the video for every arm alike, so it does not disturb the comparison.
Accept:
- [ ] at least four tracks in rotation, each with its source and licence text recorded in the repo
- [ ] no track needs a login, a payment or an attribution we cannot give in the description
- [ ] a test shows the picker never chooses the track of the last upload in `upload_log.csv`
- [ ] if no such track can be found, that is recorded and the ticket is dropped, not left open
Evidence: 11-15, implementer: four FreePD tracks (Advertime, City Sunshine, Fresh Focus, Funshine), cut to 60 s at the funk track's level; FreePD closed in 2025, so the files and its "CC0 1.0 Universal Public Domain Dedication" statement come from Internet Archive copies, URLs in `assets/music/LICENSES.md`; `log.last_music_track()` bars the last upload's track; 1,065 pass. Orchestrator 11-15: fresh review, nothing blocking, names match the log so the no-repeat rule works, the archived licence quotes verified verbatim, four 0.96 MB files. Its finding to fix before merge: a funk bed that fails to unseal in CI now drops out of rotation silently, where it used to log `none` and the digest flagged it (`weekly_digest.py`; the comment in `run-reddit-video.yml` goes stale too). Free sample (`SAMPLE=1`, silent) on the branch: 24.3 s, `freepd_funshine.mp3`, decodes clean, bed alone at −37 dB mean. No one has listened. Fixed in `e1f8b5d` (1,066 pass): the weekly digest flags a sealed track that no upload used all week. The workflow's unseal comment still says "none"; raise its one-line patch (`escalate.py --patch`) at the merge.

### T3 · Every upload records which show it was
Status: review: on `integration/preview` (`b74fc92`), lands with T1
Needs: none
Touches: src/log.py, src/run.py, scripts/weekly_analytics.py, src/insights.py, tests/
Context: the log has no column for the source; an own-question upload is known only by an empty `subreddit`. The comparison needs `report.py --compare show=<name>` with ages matched, like every other read (`CLAUDE.md` §6).
Accept:
- [ ] `upload_log.csv` gains a `show` column (`reddit`, `takes`, later others); old rows read as `reddit`
- [ ] `scripts/report.py --at-age 7 --compare show=takes` runs and refuses thin cohorts as it does elsewhere, with a test
- [ ] the append-only log's existing rows are unchanged byte for byte
Evidence: 11-15, `b849e94` (`data/e1-t3-show-column`): `config.SHOW` from `SOURCE`; blank reads as `reddit` in `insights._with_derived_dimensions`; 2 new tests. `--at-age 7 --compare show=takes` refuses (n=0 against 206). The committed log is untouched, but the first live run after the merge re-writes it through `_migrate_header`, padding old rows with blank cells, as every column added since 10-09 did (bet 1 adds four anyway): values kept, bytes not. Fresh review: nothing blocking; minor, the ledger-floor counter reads raw `show`, harmless while no ledger row coins on it.

### T4 · The show alternates by slot, in code
Status: review: `product/e1-t4-show-slots` (`4730afa`, on the release), unmerged; left: the dry runs and the title-style pairing (below)
Needs: T3
Touches: src/content.py, src/config.py, src/run.py, tests/
Context: assumption 2. Mirror `content.subreddit_for_run`: one Reddit and one new-show upload a day, each show getting the morning and the evening slot equally over two days. Merged switched off behind a constant, so T5 is one line.
Accept:
- [ ] a test shows that over any 14 days each show gets 14 uploads, 7 in each slot
- [ ] `DRY_RUN=1` produces a playable video for each show
- [ ] with the constant off, behaviour is unchanged (existing tests pass untouched)
Evidence: 11-15, implementer, not yet re-checked: `content.show_for_run` takes the old subreddit key, so shows swap slots daily; with `SHOW_ALTERNATION` on, subreddits move on `day // 2 + position // 2`, so the Reddit arm still draws every subreddit in both slots (a trap: on one key, Reddit's slot would always draw the same subreddit and starve bet 1's AskReddit read). `config.use_show` sets SOURCE, SHOW, FORMAT_VERSION and ANSWER_LABEL per run. 1,350 pass. Unchecked: how `title_style_for`, keyed on the day, pairs with subreddits once it is on. Fresh review 11-15: nothing blocking; switched off, production is unchanged (a pure extraction, `run.py`'s new step skipped); switched on, no module keeps a stale copy. Minor: the first startup line prints the import-time format before `use_show` runs.

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
Status: done
Needs: none
Touches: PRD.md §4
Context: decision 3. One shift at most. A guess needs a true answer that is ours to use. Check first-hand, quoting the terms: statistics published by governments that place them in the public domain, and datasets released under CC0 or CC BY. For each: what a viewer would be asked to guess, how many usable episodes a day, and whether commercial use is allowed. Reddit, and anything scraped against a site's terms, is out.
Accept:
- [ ] PRD §4 records each source read, its licence quoted, and its daily supply
- [ ] three example episodes are written out: question, the beat to guess, the reveal, the credit line
- [x] a verdict: build T7, or drop the play-along form because no source allows commercial reuse with at least two episodes a day
Evidence: 11-15, `07482b2` on `main`: PRD §4 "Play-along supply". BLS, Census, USGS, NWS public domain; Wikidata CC0; OGL and OWID terms quoted; ~740 candidates (BLS ~200, Wikidata ~490, Census ~50); three episodes; verdict build T7.

### T7 · A play-along episode exists as a sample a viewer could follow
Status: ready
Needs: T6
Touches: src/ (a new source beside ownquestions.py: `select` fetches a record and frames it, `render` copies it), tests/, assets/gen/ (samples)
Context: T6 said build; "The play-along episode" above is the design, and `process/viewer-bar.md` is the test. The agent judging a sample is given the script, the frames and the bar only, never the design. Start with BLS prices and Census pairs, whose records are files that need no key; Wikidata second. The number or answer in the reveal is copied from the source record by code, never written by a model.
Accept:
- [ ] a test fails if the revealed value or the comparison differs from what the source record gives
- [ ] the selector applies the rules above (guessable, surprising distance, one fact, fresh shape, nothing contemptuous) with a test per rule, and logs its reject rate on a day's candidates
- [ ] the three T6 episodes render free (`SAMPLE=1`) in the shape above, and a fresh agent judges each against the bar; every check is a yes, or the fail and the fix are recorded here
- [ ] one narrated dry run of the best is playable, with the credit in its description
Evidence:

### T8 · The play-along show uploads as its own arm
Status: todo
Needs: T5, T7
Touches: src/content.py, src/config.py, the experiment ledger
Context: amended 11-15 (the challenge, above): this arm runs after the cutover, against takes and perhaps Stack Exchange, read in February. Three shows cannot each reach a readable count on two uploads a day before 20 December. Decide between a third daily upload (assumption 3) and giving this show half of the takes arm's slots, using the chance gaps `report.py` prints; write the choice and why.
Accept:
- [ ] the arm's rule is in the ledger before its first upload
- [ ] the slot plan gives every arm both slots equally, with a test
Evidence:

### T9 · The 12 January show is chosen
Status: todo
Needs: T5
Touches: the experiment ledger, DECISIONS.md, PRD.md §0, PLAN.md
Context: amended 11-15: expect T5's rule to refuse at ~17 a side, so decision 4 applies unless its gate fails. By 2026-12-20, apply the rule from T5 (and T8 if it ran) exactly as written. A Decide: evidence, the alternative rejected, a fresh agent arguing against it.
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
