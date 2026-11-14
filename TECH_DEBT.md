# Tech debt & code health

Tracks the recurring code-quality check-in the owner asked for after every
project version: read through the codebase, find the highest-leverage
non-functional improvements (structure, duplication, fundamentals), fix what's
approved, defer the rest with reasoning. This is a companion to
[PRD.md](PRD.md) — PRD.md tracks *feature* requirements and their status;
this file tracks *code health* independent of any feature phase.

## Pass 1 — 2026-07-21 (after v3 + R4.2 shipped)

### Addressed

**Dead code/assets removed:**
- `assets/question.mp3`, `assets/top_responses.mp3` — unused since R1.1 removed the "announcer" segments (dead air elimination).
- `audio_adjustment.ipynb` — one-time notebook, its job (lowering `funk_bg.mp3`, generating the now-deleted announcer clips) is done; was gitignored, never committed.
- iCloud sync-conflict duplicate files (`scripts/analyze_channel 2.py`, `analysis/*` " 2" copies) — byte-identical junk from the repo living in an iCloud-synced folder.

**Duplication removed — new `src/analytics.py`:**
- `median()` was copy-pasted verbatim in three scripts (`analyze_channel.py`, `weekly_analytics.py`, `weekly_digest.py`). Now one function.
- Three separate implementations of "paginate the channel's uploads playlist" (one via raw REST + API key, two via OAuth client, each with slightly different pagination loop code) consolidated into `list_uploaded_videos()` + `fetch_video_details()`.
- `analyze_channel.py` migrated off its standalone API-key auth path onto the same OAuth client the other two reporting scripts already used — this was the right call when written (R4.3 shipped before the Phase 3 OAuth re-auth existed), but became a redundant second auth mechanism once that re-auth landed. Removed the hardcoded `CHANNEL_ID` constant along with it; the channel is now always resolved live via `channels().list(mine=True)`, the same as everywhere else.

**Structural split — `src/video.py` (351 lines, three unrelated concerns) →**
- `src/video.py` — timeline assembly, captions, MoviePy rendering.
- `src/background.py` — procedural drifting-glow generator + b-roll/procedural selection.
- `src/thumbnail.py` — Pillow-based thumbnail card (shares no code with the MoviePy path; different library entirely).

**Correctness/clarity fix:**
- `src/run.py`: `Segment` objects were constructed with `kind=""` and mutated right after (`segments[0].kind = "title"`). `synth()` now takes `kind` directly — removes the two-step construction.

**Docs synced** to match: README's pipeline walkthrough and OAuth section (which had gone stale — it still listed the already-completed OAuth re-auth as an open task), PRD.md's R4.3 entries and OQ-4.

### Considered, not done (with reasoning)

- **Pulling caption font-sizes/y-positions in `video.py`/`thumbnail.py` into `config.py`.** These are single-call-site layout values; indirecting them through a config lookup would make the call sites *less* readable, not more. `config.py` already correctly holds values that are genuinely reused across call sites (`BRAND_ORANGE`, `CAPTION_WIDTH`, etc.) — that's the right bar, not "every literal."
- **Type hints / mypy / ruff.** Legitimate for a team codebase; disproportionate process overhead for a solo-maintained project at this size. Revisit if the codebase or contributor count grows.
- **Deleting `create_video.ipynb`.** Harmless either way — kept "for reference" per the owner's earlier call, not a code-health issue. Owner's call whenever.
- **Promoting `weekly_analytics.py`/`weekly_digest.py` into a `src/analytics/` subpackage** (run via `python -m`, mirroring `src/run.py`) instead of staying in `scripts/` importing from a shared module. Considered as the structurally "purer" option; owner chose to keep `scripts/` as-is (no workflow YAML changes, no command-muscle-memory churn) with the new `src/analytics.py` doing the actual DRY work. Revisit if `scripts/` accumulates more CI-invoked entries and the asymmetry starts to grate.

### Deferred to a future pass

- ~~**No automated tests exist.**~~ *Closed in Pass 2* (`tests/test_insights.py`; 669 tests on 2026-10-28). Not urgent for the rendering path (correctly verified by the existing dry-run + frame-extraction ritual — genuinely visual/audio correctness that needs eyes, not assertions). But `weekly_digest.py`'s date/threshold arithmetic (cadence windows, unlogged-video buffers) and `analyze_channel.py`'s stats (age-adjusted residuals, distinctive terms) are pure, deterministic, and have already needed two manual recalibrations this week from eyeballing — exactly the class of bug a small `pytest` suite over just those functions would catch for free. Owner scoped this pass to Tier 1+2 (cleanup + structure) and left testing for later; worth revisiting at the next check-in.
- `scripts/` still mixes true one-time tools (`make_sfx.py`, `prep_broll.py`) with recurring CI-invoked scripts (`weekly_analytics.py`, `weekly_digest.py`) and an ad hoc-but-substantial one (`analyze_channel.py`), with no naming/directory convention distinguishing them. Not painful yet at 5 scripts; reconsider if the directory keeps growing.

## Pass 2 — 2026-08-23 (after v4 + v5 + b-roll + Step 0 telemetry)

### The finding that drove this pass

The code was healthy (~2,000 lines, cleanly separated). **The analysis layer was not.** Four wrong conclusions reached a decision in two weeks, all from ad-hoc analysis written inline and thrown away:

1. *"Length is the retention lever"* — nearly built R1.8/R1.9; caught by the owner, not by us.
2. *"B-roll lifts retention 65% vs 48%"* — pure age artifact.
3. *"Production quality didn't move retention"* (July) — age-confounded; retracted.
4. Digest zero-view alert — 12 false positives, on track to become ignorable noise.

Root cause: decisions were driven by throwaway scripts, so nothing was reproducible, and the rules we kept learning (age-match, watch-seconds primary, n-gating) lived only as prose in the PRD. The code was reliable; the thing steering the code was not.

### Addressed

- **New `src/insights.py`** — the single place "did X work?" is answered. Encodes the hard-won rules as *defaults* rather than reminders: watch-seconds is the default metric (avg-%-viewed is a ratio we can game by trimming), cohorts must be age-matched or the verdict is withheld, cohorts below `MIN_COHORT=8` report "insufficient data" instead of a median, and zero-view videos are counted separately rather than averaged in (they're suppression events, not weak performance). Also provides age-adjusted residuals for cases where cohorts genuinely can't be age-matched.
- **New `tests/test_insights.py` (12 tests)** — clears the testing item deferred in Pass 1. Each test pins a mistake that actually happened: the b-roll age confound, the thin-cohort median, the avg-% illusion, zero-view contamination. Run: `venv/bin/python -m pytest tests/`.
- **New `scripts/report.py`** — CLI over the module (`--by`, `--compare`, `--metric`). Verified against live data: it reproduces the real numbers *and* refuses to call the b-roll comparison, flagging 6d vs 22d median ages — the exact error that previously slipped through.
- **Derived `background_type`** dimension (broll/procedural), since raw `bg_clip` is per-file and too granular to group on.
- **`median` consolidated** to one implementation (`analytics.median` delegates to `insights.median`), and `requirements-dev.txt` added so pytest stays out of the CI runtime install.

### Workspace cleanup (same pass, 2026-08-23)

The v2 refactor moved runtime output to `assets/gen/` and replaced the static background with procedural/b-roll, but the v1 originals were never removed. Deleted ~2.1 MB of orphans: a crashed-render MoviePy temp at the repo root, `assets/comment_{1,2,3}.mp3`, `assets/title_audio.mp3`, `assets/final_askreddit_video.mp4`, `__pycache__` dirs, plus (tracked, recoverable from history) `assets/bg.png`, `assets/bg.jpg`, `assets/thumbnail.png`. Owner-approved second round removed `assets/hook_audio.mp3` (v1 fixed outro audio — superseded by the per-run synthesized CTA), `create_video.ipynb` (deprecated v1 notebook), and `praw.ini` (unused; auth is via `REDDIT_*` env vars).

Docs were corrected to match reality rather than just tidied: R1.3's fallback spec described a Ken Burns pan over `bg.png` that **was never implemented** (procedural glow shipped instead), §2 was relabelled as the historical v1 baseline rather than "current system", the CREDITS row for deleted art was removed, and `.gitignore` rules for files that no longer exist were dropped.

Lesson for future passes: deleting the *files* is the easy half — the stale **claims** in docs are what actually mislead later.

### Considered, not done (with reasoning)

- **Refactoring `analyze_channel.py` onto `insights`.** It duplicates residual/median logic, but it's 292 working lines, run manually a few times a month, and operates on its own dict shape rather than `Video` objects. Rewriting it now is real regression risk against a script that isn't causing problems — the duplication is documented rather than churned. Revisit if it needs changes for another reason.
- **Broad Pass-2 refactor of `src/`.** The module split from Pass 1 is holding up; nothing has rotted. A general sweep would produce diff noise, not value.
- **`scripts/` naming convention** (one-time tools vs CI-invoked vs ad hoc) — still not painful at 6 scripts; still deferred.

### Deferred to a future pass

- `analyze_channel.py` residual/median duplication (above).
- No tests over the rendering path — still correctly covered by the dry-run + frame-extraction ritual, which checks things assertions can't (legibility, timing feel).
- `create_video.ipynb` remains in the repo as deprecated reference; harmless, owner's call.

## Pass 3 — 2026-09-19 — scoped by Engineering 2026-10-11 (ORG.md: Act; it waited three weeks on the owner)

Tier 1 item 1 lands with `v8`: the release branch extracts the guard as `run.fit_to_length`, with tests. Item 2 stays deferred until `analyze_channel.py` next needs a change (Pass 2's call; R4.4, the gate it fed, is parked).

Read fresh, per the ritual. `src/` is ~2,000 lines and the Pass-1 module split is
still holding; nothing has rotted structurally. Two findings are worth acting on,
and they are the same shape as the two real bugs found today — **logic that no
test can reach, and two implementations of one question that quietly disagree.**

### Tier 1 — recommend doing

1. **`run.py:main()` is 152 lines and effectively untestable, and the R1.7
   duration guard inside it has zero tests.** That guard decides whether to drop
   an answer from the video, i.e. it changes what ships. It is the last
   substantial piece of pure logic with no coverage. Today's `title_style` bug
   lived in the same function and could only be tested after extracting
   `llm.resolve_title` — the same move works here. `main()` is 2x the next
   longest function in `src/` (`video.assemble`, 79).
   *Proposed:* extract the guard to a pure `plan_segments(segments, budget)`
   returning the kept segments plus what was dropped, and test it — including
   the case below.

2. **Two implementations of `age_adjusted_residuals` that disagree.**
   `src/insights.py:184` and `scripts/analyze_channel.py:231` answer the same
   question differently: insights **excludes** zero-view videos and clamps age,
   analyze_channel **includes** them, and their `MIN_AGE_DAYS` are 3 vs 7.
   Measured on the live channel: slope **−0.185 vs −0.212, a 14% difference**,
   driven by 41 zero-view videos. Neither is obviously wrong, but the project
   has a *stated* rule that zeros are counted separately rather than averaged in
   — insights follows it, analyze_channel does not, and nothing documents the
   divergence. It matters because **the R4.4 gate was cleared using
   analyze_channel's implementation** while `report.py` uses the other, so that
   evidence is not reproducible through the sanctioned tool. (R4.4's own
   sensitivity note already brackets the age model at +0.66 to +0.79, so this
   does not overturn the gate — it means the number depends on which
   implementation you ask.)
   *Proposed:* analyze_channel calls `insights.age_adjusted_residuals`, with the
   zero-view decision made once, explicitly, and written down.

### Tier 2 — worth doing, lower urgency

3. **A bare `assert` sits in the upload path** (`run.py`, `assert projected(...) <= 60`).
   If it ever fires, the run dies and the slot is lost — the opposite of the
   fail-soft posture everywhere else in the pipeline. It is also stripped under
   `python -O`. Should drop another answer or truncate, not raise.
4. **`_probe_duration` spawns ~10 ffprobe subprocesses per run** — `projected()`
   is called twice and re-probes every segment each time, though the durations
   are already known when the audio is synthesized. Pure waste, easily cached.
5. **`analyze_channel.py` has grown 292 → 517 lines** during the R4.4 work. Pass 2
   deferred refactoring it as "292 working lines, not causing problems"; at 517
   lines carrying the duplicated statistics in finding 2, that reasoning is
   weaker than it was.

### Tier 3 — deliberately deferred (unchanged)

- `scripts/` naming convention (one-time tools vs CI-invoked) — 7 scripts, still
  not painful.
- Normalizing `analytics_snapshots.csv` line endings — still a ~7,500-line
  mechanical diff on a production data file; owner's call, and it cannot worsen
  now that both writers pin LF.
- Type hints / mypy / ruff — unchanged reasoning from Pass 1.

## Ritual

Run this check-in after each version bump (`FORMAT_VERSION` change in `src/config.py`) or major non-video feature ships (like R4.2). Read the current state fresh — don't assume the last pass's findings still apply — propose tiered findings, scope them (Engineering's call, ORG.md; never the owner's), execute, update this file.

## Open items (logged between passes)

Findings that surface during feature work, recorded here so they survive past
the commit message they were noticed in. Not a formal pass; fold into the next one.

- **Bet 1's text-only host (2026-10-11, branch `product/text-host`, behind
  `HOST_TEXT`).** The voiced build was rejected (#71). A local `SAMPLE=1`
  render with `HOST_TEXT` on: playable, 19.9 s, own words 0.540, one voice.
  Before its sample: (1) yellow notes on a busy clip (orange smoke) read but
  not crisply; a dark band behind them would help. (2) The fixture's reaction
  repeated its answer's words, duplicating the caption: fixed on the branch,
  where the text-mode ask says lines are shown, forbids quoting the answer
  and caps setup and reactions at 10 words (12 with slack: four lines would
  meet the watermark). Reviewed, findings fixed, `v8`, switched on. The dark
  band (55%, behind each note) landed 2026-10-11, reviewed. Left (cosmetic):
  notes are not in the SRT caption track; the band is full width behind a
  short note; a rare three-line caption's bottom pixels reach the band's top.
  The 10-11 sample's notes came back all lower case; `note_clips` now
  capitalises a plain lower-case first word (0a0712c, reviewed). Re-sampled
  on `907d6ad` (10-11 22:59): PASS. Its vote, posted as the comment, came
  back lower case: fixed on `product/vote-comment-caps`, to land after `v8`.
  The 10-13 sample of the whole stack (`reliability/groq-switch` `74c81a7`)
  played, but one line past its cap dropped all four (own words 0.000), 1 of
  4 samples; the log does not say which line. `product/host-line-fallback`
  drops only the long line in text mode. The overrun was `SAMPLE_MODEL`'s;
  `MODEL`'s votes fit in all six text-host release checks to 10-16 (12–15
  words, cap 18), but on one fixed post, so production's rate is unmeasured:
  read `host_lines` after `v8`. A full-branch
  review (10-13) found no blockers; left: the setup note shows for 65% of the
  question's audio, so under 2 s on a short question (`video.py` ~107). Keep it
  up to the first answer, after the owner's label, since it changes the look.
  Host lines now also drop on emoji (the font lacks them). `emoji` and
  `better-profanity` (which filters posts and comments) are pinned since
  10-13, and `test_requirements.py` fails any unpinned line. The final
  branch, with those pins merged in, sampled PASS on `0fbc37c` (10-13
  23:22): all four lines shown, notes capitalised, own words 0.439. By 10-14
  afternoon it no longer merged: main's reporting work conflicted in
  `tests/test_insights.py` (both sides appended tests; kept both). Brought
  current, it sampled PASS on `79a3873` (10-14 16:08, own words 0.661);
  `check_docs.py` now flags such a conflict at shift start. **Three answers
  (#77, 10-14 night):** `product/host-three-answers` (`e20a53e`, on top of it;
  565 tests; a fresh review found no bugs). Left by that review: a style C
  title promising "3 Answers" ships over two if the duration guard drops one
  (as in `v7`; the guard has not fired on a `v7` upload, peak 31.5 s of 45);
  the voiced host (`HOST_TEXT=False`, rejected) would now speak three
  reactions, and its tests pin two. Brought current with main, it sampled
  PASS on `b9bc23b` (10-16 22:12): 29.7 s, own words 0.347 on a long-answer
  thread (34 of our words to 64 of Reddit's); a sample-model line ran past
  its cap again, this time the vote, which fell back to the outro. Read
  `host_lines` after `v8` (its dose rule, PRD #15): the count includes the
  vote, so a fallen-back vote already reads as "some". **10-17:** its
  release check failed, the reply unparseable (#78). Live, prompt-only JSON
  also gave a trailing comma (sample model) and four reactions for three
  (`MODEL`), each costing every host line; the metadata call now sends a
  `responseSchema` (exact keys, one reaction per answer) and forgives a
  trailing comma, logged (`2e26595`, reviewed; live on both models: valid,
  three reactions). Groq's fallback sends no schema, and needs none: 12 free
  calls on `2e26595`'s prompt (six posts, styles A/B/C, both caps arms,
  10-17 21:33) all parsed with three reactions; one vote overran its cap, so
  its closing line would ship. Left: a repair records no `meta_failure`, so only stdout
  counts it; the prompt lists `comments[:3]` while the schema follows
  `COMMENTARY_ANSWERS` (harmless at 3). The screen's JSON is unchanged: 3
  fallbacks in 180 uploads. **The verdict-tag filter (`_VERDICT`, 10-24)**
  reads stock forms only; left by its third review: "Nobody's right" and
  "Truth..." drop, "Oof, truth", "Ur right" and "Bulletproof" (a 10-22 render)
  ship, as do probes ("Solid point", "Can't argue", "Best answer"). Widen only
  on a tag seen in a release check or render. **Whole-branch review (10-24, on
  `a05b300`): no blockers**; its fixes (an empty line drops alone, flag emoji in
  tags) are on the branch, as is the same fix for titles, the vote and answers
  (`content._has_emoji`; 2 of ~1,000 past videos' text, one an answer shown on
  screen), so `main` misses flags until `v8`. Left: `_excerpt` prints an
  unparseable reply raw to the public log, where `_clean_published` never
  echoes a refused field. **Merge rehearsed 10-26** (local, over `main`
  `5e96eb2`): no conflicts, 857 pass, no network. **Title replay:**
  `scripts/replay_text.py main integration/preview`, re-run before the
  merge (11-06: 220 of 220 titles identical through `_clean_published`,
  `_shock_bait` and `sentence_case`; 13 refused by both, all shipped before
  their guard); closing lines have three logged rows, and
  host lines none, so neither is replayable yet. Brought current with `main`
  the same night (`f046eba`): clean, 1,013 pass; the CTA is cased by
  `main`'s 11-04 fix and the vote comment by `vote-comment-caps`, so #14's
  no-capitals arm keeps capitals after the merge. **Two sentence-case rules (11-05).** The
  vote comment's `content.sentence_case` (per sentence, any text) left "i"
  and capped after "vs.", "u.s." and "...", bugs 003c9bb fixed in
  `llm.sentence_case`: they disagreed on 19 of 420 lower-cased logged texts.
  Fixed on the release (`5a44db0`, two reviews): now 5, all words starting
  with a mark ("#shorts"), left alone by design. Left: two functions remain. Its review's one gap: the
  dose and own-words lines under `--release v8` (`render_host_lines`,
  `report.py` ~233) count every `v8` row, any age or subreddit, while the
  verdict reads AskReddit at 7 days, so "all lines on N of M" can name
  uploads the verdict never read. Own words do so by design (#70's
  done-when is every upload); the dose does not (PRD §4, pre-committed
  10-26). **Built on `data/v8-dose-verdict-uploads`** (off `integration/preview`,
  reviewed, its fixes in; 859 pass over `main`): the verdict's first 20 by date
  (`insights.dose_ids`; a test drives `report.release()`). Merge it right
  after `v8`. **Rehearsed again 11-13** over `main` `ae729f3`: `v8`, this
  branch and `reliability/run-slot-log` merge cleanly, 1,141 pass. **Fallback tags (10-27, disclosed on #77):** when `MODEL`
  fails, the metadata reply, host tags included, comes from `FALLBACK_MODEL`
  (the sample model, which mostly labels), then Groq (`GROQ_FALLBACK = True` on
  the branch, off on `main`; no Groq model met §4's bar). 1 of 18 uploads
  since 10-18 took that path (10-26 05:05, `meta_failure=http_503`). The
  release check sets `FALLBACK_MODEL = None`, so it never sees it. If the
  owner asks on #77, drop host tags when the route is not `gemini`.
  **Whole-release review (11-13, `b1190de`, main merged in; sampled PASS on
  that commit): no blockers.** Left: a thread skipped as medical by its screen
  topic spends one of the 4 screened slots (`content.py` ~317), rightly, as
  its screen request was spent; so a day of such threads plus R4.6 skips can
  end a run with no post (no upload, no state touched; ~1 in 400 runs if
  skips were independent, against ~1 in 1,200 from R4.6 alone). Any fix spends
  Gemini (`MAX_SCREENED_CANDIDATES`): act only if a run ends with no post. A
  length-guard drop while the vote shows synthesizes the stock line as a sixth
  Polly call (~94 characters, `run.py` ~120). Each branch render spends one
  `MODEL` request (`METADATA_ON_UPLOAD_MODEL`), so #65's sentence needs
  rewording before it lands (noted on its body). Once `v8` merges, the shift skill's
  §6 line that a branch renders "over silent narration" is false (Kokoro
  stand-in, `STAND_IN_VOICE`): for the monthly's bundle of skill changes. With reactions off, the ask and
  schema still request three (tokens only).

- **Four a day, built off (2026-10-11, PRD §0 #4).** Left by its review, for
  the switch to four ((1), the digest's two-slot drift, fixed 2026-10-11):
  (2) a run queued behind another
  cancels a pending one in the `reddit-video` group, so an off-slot run could
  cancel a waiting live one (needs a ~6h pile-up; none in 99 scheduled runs
  08-27 to 10-13, the closest two 3.5h apart); (3) after the patch, a
  12:23 run landing after midnight takes the previous day's style, and an
  00:23 one landing after noon the morning subreddit (11.6h+ delays; 3.0–7.4h
  seen over 81 runs to 10-11, then 9.4h on 10-12's 06:23 run, which exited
  as an off slot should); (4) the digest counts days by publish date, so an 18:23 run landing
  after midnight reads as a missed day, and drift over 6h reads as small.
  (3) and (4) cannot be fixed from publish times: at four a day slots are 6h
  apart and delays reach 9.4h, so any carry-over rule either hides a real miss
  or raises a false one (10-13). Log each run's slot in the upload log, through
  a sample after `v8`: **built 10-13 on `reliability/run-slot-log`**, stacked
  on `v8` (`run_slot`; the digest counts each upload for its scheduled day and
  times its delay from that slot; older rows keep the estimate; reviewed
  twice, fixed; brought current with `v8` (`b1190de`) 11-13, `e37d656`: clean,
  1,139 pass).
  Merge it after `v8`, before the switch, on tests and review:
  no sample reaches it (a dry run returns before the log), and `prev_post.txt`
  is written first, so a fault there cannot repeat an upload. **At the switch, keep
  `MAX_SCREENED_CANDIDATES` at 4:** PRD §2's cut to 2 was the free route for
  Gemini's worst case, which `v8`'s Groq fallback now answers, so the cut
  would cost screen depth for nothing (10-13). Raise `CANDIDATE_LIMIT` as §4 says. The delay is rising again (upload times against their slot, 11-05): weekly
  median 4.3–4.8h (W36–W39), 5.5–5.9h (W40–W41), 4.6–4.7h (W42–W43), 5.7h (W44),
  then 6.7h with all 7 of W45's uploads over 6h (worst 9.5h), so at four a day the
  median run now lands after the next slot is due. **Every cron here is as late
  (11-12, scheduled runs' start against their cron, weekly medians W40→W46):**
  shifts 4.6→7.4h, the release check 6.6→8.3h, the weekly job 6.3→8.7h, all
  rising from W43. So it is GitHub's scheduler, not the upload workflow; no
  edit to its cron fixes it, and only a trigger outside GitHub's schedule would
  (a token: the owner's). Runs are safe (`run_slot` takes
  the day from the cron line); the digest is what misreads. **If #4 goes
  before `v8`** (PRD #4, 10-19), both answers above are `v8`'s: main has
  `GROQ_FALLBACK = False` and no slot log. So switch the fallback on alone
  (a sample, no bump) and move `run-slot-log` off `v8` first, or cut
  `MAX_SCREENED_CANDIDATES` to 2. **Closes when** the switch goes to four.

- **The Groq route is merged switched off; key and patch are in (#68, #69,
  2026-10-10).** `config.AI_PROVIDER == "groq"` sends every AI call to Groq.
  **First replay on Groq (2026-10-11, run with no Gemini key, so nothing
  touched Gemini's quota):** titles pass; the screen went 6/7, skipping as
  `named_wrongdoing` the Epstein-files question that `_PROMPT` itself lists as
  must-pass. A second run that evening skipped the same case (6/7 again), so
  Groq's model follows the prompt's calibration less well, consistently.
  **Fixed on a branch (10-12):** one Groq-only line before the question
  (`_GROQ_CHECK`) took the case to 6 of 6 and the replay to 7/7 twice;
  `reliability/groq-screen-calibration`, to land with the switch. Reviewed:
  no bugs, two test gaps fixed. Its risk, that "closely paraphrases" passes a
  real `named_wrongdoing` rewording, was probed: two rewordings skipped, and
  one is now a Groq-only replay case. The owner leaves Gemini's role to us (#68) and suspects it titles
  better. Gemini failed on 3 of the last 5 uploads (503s), when the screen
  falls to the keyword backstop. So the likely build is Gemini first, Groq on
  a Gemini 429/5xx (stricter than the backstop, which errs safe), with the
  log's source naming the route that answered. **Merged off 2026-10-11** for
  the screen only, after both Gemini models and before the backstop
  (`config.GROQ_FALLBACK`, `screen_source=groq_fallback`); the metadata
  call got the same that evening (`llm.groq_rescue`, one switch for both).
  The upload log has no metadata source column: a Groq answer shows as a
  non-blank `meta_failure` beside any field logged ok. Nothing reads that,
  so once switched on, Groq's titles count in the style and caps reads
  (#10, #14) unmarked (review, 2026-10-11). A `meta_source` column is built
  on `data/meta-source-column`, on top of `product/text-host`: land it after
  `v8` and before the switch (reviewed 10-11, no faults; its test reads
  `run.py`'s source, not the written row). **10-30:** land with it why a
  title was refused: a shock phrase, a swear word or emoji, and a reply that
  cleans to nothing all log `title_ok` 0 with `meta_failure` blank, so #13's
  "shock refusals aside" cannot be counted (10-29 06:06 is one). Not built
  now: `v8` rewrites that code. It and `product/vote-comment-caps`
  (the vote posted as the comment, capitalised; reviewed, fixed) merge
  cleanly over `v8` and `main` together, tests green (re-checked 10-12
  over that morning's `main`: 523 pass). Its review's two logging gaps closed
  2026-10-11: a missed Groq try and its parse failures now end
  `screen_failure` as `;groq_<kind>`. Up to four screens run back to
  back: at 8K tokens a minute a second 429 inside one retry falls to the
  backstop (`…;groq_http_429`). **Switched on, pre-built on
  `reliability/groq-switch` (10-12):** with it on, a shell's `GROQ_API_KEY`
  sent six Gemini-failure tests to Groq's rescue, so the tests' shared
  fixture now clears it. Reviewed: no bugs. Its two risks: the rescue never
  waited out Groq's per-minute cap, so on a Gemini-spent day the title and
  `v8`'s host lines could fall back (fixed on the branch: one printed wait of ≤60s, reviewed);
  and Groq had never written `v8`'s host lines (the release gates routed to
  Groq, no Gemini key, pass: setup, both reactions, screen 8/8). Left: the
  rescue fires on any Gemini exception, not only 429/5xx (harmless);
  `title_caps` is logged for Groq titles, so #10 and #14's reads must filter
  on `meta_source` once any appear. **Switch on in `src/config.py`, never a
  workflow or repo variable:** the release check re-runs only when code
  changes. Some log lines still say "Gemini" whichever route answered.
  **Since 10-18 the metadata call tries Gemini's second model before Groq**,
  as the screen has since 10-09: two 503s 30s apart cost the 16:02 upload
  its title, keywords and CTA (third since 10-01, all 503s). Its answer logs
  a `meta_failure` beside fields logged ok and counts as `gemini` in
  `title_writer`; the release check switches it off. First live rescue
  10-26 05:05: two 503s, then all three fields ok. Bet 1's branch
  conflicted with it in `get_metadata`'s failure branch and is pre-resolved
  (`integration/preview`): the second model first, given the main call's
  reply schema. (The two-answer branch's copy is moot: #74 closed 10-22.)
  **11-14:** PRD #13's tag condition assumes per-answer reactions. If #77
  ships without them (its ask), the host's lines are the setup note and the
  vote, which no Groq trial has read (`tag_trial.py --model groq` reads them
  on `integration/preview`). Set that bar before #13 is next, not now: a
  trial ahead of bet 1's read would be stale by the time it is used.

- **Audit 2026-11-12: working at the margin; the owner's selective answers
  decide what ships (last act 11-10 15:24).** 16 shifts since 11-05 (one
  killed 11-08; two 11-06 slots never ran). 8 began with nothing ready; mean
  38 of 60 minutes, five handed over 16–25 minutes early. ~40 fixes, checks
  or tooling to ~8 bets (~15 internal tooling); one change reached viewers,
  the forced `v7s` switch (11-08). Time: gm 25%, reliability and data 18%
  each, product and strategy 10%; distribution, monetization, finance 0
  (nothing of theirs ready; the 11-03 monthly gave them their turn). "Than
  ~10 shifts ago": No in 16 of 16 (29 running). Scorecard WORSE (zero-rate
  14.7%, from 17.6%, breached; watch-seconds 12.0 → 10.0 s), trajectory FLAT
  (11.0 s): they agree, as every step that changes what we ship waits on
  #77/#90. **Cause found, fixed (finding 3 of both earlier audits):** ~7
  dropped ideas came back because `--dropped` matched only bold labels and
  every entry since 11-04 writes plain "Dropped:", so the generator saw
  nothing after 11-03; one re-stamped shift also listed twice (`6fc8b29`).
  `--allocation` had the same re-stamp fault and merged two 11-07 shifts on a
  stock summary opening; fixed too (11-07 00:35's draft, which
  also changed its split, still lists twice). Reopen if a generator
  re-proposes a drop `--dropped` lists. **Gates:** fresh reviews caught ~50
  defects across 16 changes (9 clean); 3 dry runs and 3 release checks
  passed and caught nothing, a third window. Viewer-facing faults again
  surfaced only by reading published output (11-07 lower-cased title, 11-11
  `v7s` title claims, now a scheduled check). Main's tests broke twice for
  2–4 minutes on pushes without a test run (F240, F255). 0 reverts, 0
  attribution trailers, 1 protected change (`Approved-In: #91`).
  **Escalations:** none opened (11-05's hold); the owner answered five
  label-only asks on 11-10 and passed over the five needing a watch, a
  direction call or hands (#59, #77, #80, #82, #90). Tight on files (#88,
  #65 approved, awaiting hands), not decisions. **Decisions** (inline): D13,
  D11, D5 false; D4 worse (PRD §4 15,317 → 20,714 words in a week); D2, D8,
  D9 (amended, #91), D12 strained; D6, D14 hold a third audit: graduation
  candidates. **Outward (docs 11-12):** the `attribution` setting turns off
  the harness's credit-line request at source: raised with its patch
  (`attribution-setting-off`). A Stop hook in `shift-settings.json` could
  hold a shift to its hand-over time: held, as early hand-overs are
  supply-bound and the owner's standing instruction covers the rest. `--bare`
  may become `-p`'s default and would skip CLAUDE.md, skills and hooks:
  check the trace at the action's next pin bump. `/doctor prompt-audit` now
  exists (11-05 said not), untested under `-p`. Rejected: `--max-budget-usd`
  (a capped run ends with no handover); skill frontmatter (nothing to gain).
  **11-05's held proposals, resolved:** the env switch dropped (moot since
  #93); the title-replay gate dropped as a rule (one command since 11-06,
  used when text code changed; reopen if a shipped-text change merges
  without it); PRD §4's budget touched no protected file, so a shift
  added it (11-12, set at 20,714 so it only shrinks; compressing it is
  next); a per-entry WORKLOG cap was ranked last twice and dropped; the re-raise patch held
  to the 12-07 monthly while five asks are unanswered. **Left alone:** the
  shift cadence (#92 declined), the owner's queue.

- **The weekly snapshot job installs its libraries unpinned (2026-10-14).**
  `weekly-analytics.yml` names three Google packages in `pip install`; every
  other workflow reads `requirements.txt`, and `test_requirements.py` reads
  only the requirements files. A broken release on a Monday loses that week's
  snapshot for good (no backfill). **10-28:** httplib2, under all three and
  unpinned in `requirements.txt` too, shipped 0.32.1 that morning (drops a
  distrusted Comodo root, not Google's); with the job's newest three, TLS to
  every Google host and all tests pass. Not raised alone: unlikely, and the owner's
  queue is the binding limit. Patch and test built 10-18 (the bundle above).
  **Closes when** the next workflow patch to the
  owner carries `pip install -r requirements.txt` there, with a test that
  fails any workflow `pip install` naming a package.

- **#14's arms are held in code (arm 0 10-16, arm 1 10-24); left by the
  second's review:** the source includes the top comments, so one in capitals
  exempts common words ("YOU") and either arm can still leak; "OMG" is not an
  acronym; arm 1 keeps the first capitals word, not the meant one ("WHAT would
  you do?"). Rare, and a leak dilutes, never inflates (PRD #14). **Closes
  when** #14 is read (~11-23).
- **The own-question title check drops ordinary titles (merged off 2026-11-12,
  PLAN C16; left by the merge's fresh review).** `llm._OWN_BANNED` matches
  "people say/tell/explain…" anywhere, so "Why do people say sorry so much?" or
  "3 People You Meet at Every Wedding" falls back to the question itself, which
  carries the same words, logging `title_ok=False` and costing #10's and #14's
  arms that run. It misses "/r/tifu", "Redditors reveal", "3 Answers That…" and
  "Commenters reveal". Live path untouched (`SOURCE=reddit`). Fixing it changes
  the commit, so it needed a second render the 12-hour limit refused.
  **Fixed in part on `strategy/own-title-check` (11-12, 875 pass, unmerged):**
  three rounds, each reviewed fresh, and each review found new wordings. Its
  third leaves: "People's Hot Takes", "Hot Takes From Strangers", "People React
  To…" and singular "A stranger told me" pass (as on `main`); spelled counts
  newly drop "Should two people split the bill?"; "How often/What do people
  say…" drop. A word list keeps leaking, so before switch-on weigh a different
  check, not a fourth round. Not the screen call: it runs inside `select_post`,
  before `get_metadata` writes the title (`run.py`; checked 11-14). **Chosen
  (11-14): a second call, not a field in the metadata reply.** On our own
  channel the writing model ignores its own instructions where a separate
  check does not: three prompt fixes left bet 1's tags as labels (#77), while
  the separate R4.6 screen passes its replay. A miss misleads viewers about whose
  takes they are; a false refusal only ships the question as the title. So: the
  list keeps Reddit's names alone (`reddit`, `r/…`); one request after
  `get_metadata` asks the upload model whether the title or closing line
  presents the takes as real people's, and a yes, a failure or an unreadable
  reply refuses that field (fail closed). Cost +1 a run: a typical own run then
  spends 4 (write and screen in `ownquestions.select_post`, the title, this), 8 of 20
  at two a day and 16 at four, where a worst day passes 20 and #13's Groq
  route must carry it, as for Reddit's (PRD §4). Test plan: the 17
  cases below drive the call mocked; before switch-on one batched request
  judges all 17 on the sample model, and must right every case. **Built 11-14**
  (`llm._own_judged`, merged off, after the list). Left before switch-on: narrow the
  list to Reddit's names and move the 17 cases onto the judge; log a judge refusal
  in `failure`, which today reads as an empty title (mind `validate_release.py`'s
  reading of it). Rescued as the metadata call is since 11-14. **Graded
  from 11-12** by `tests/test_own_title_cases.py`: 17 fixed cases, 10 wrong on
  `main` (strict xfails, so the fix branch must lift the ones it rights). **Closes
  when** fixed with tests, before `SOURCE=own` turns on.

**Retention — open items must close, not accumulate** (cap: 13 under this heading, checked by
`scripts/context_budget.py`). Every item resolves one of three ways: **fixed**
(delete it, or leave one line in the pass that fixed it), **promoted** to
`PRD.md` §0's backlog if it is really product work, or **deleted with
reasoning** if it stopped mattering. Past the cap, close before adding —
a list nobody can read is the same as no list.

- **Pillow is ageing out.** (Python moved to 3.12 on 2026-10-07, #63; the
  next upload ran on it and README follows. requests 2.33.1 merged 2026-09-30.)
  `pip-audit` finds published advisories against **Pillow 10.4.0** (33+; 66
  rows on 10-26, unchanged 11-06 and 11-10, fixes now at 13.0.0; oauthlib's now PYSEC-2026-4114).
  Exposure is low: Pillow only ever decodes our own fonts, b-roll and
  generated frames, never an untrusted image.
  **Pillow is blocked by moviepy 2.1.2, which requires `pillow<11.0`** (pip
  flags 12.3.0 incompatible; found 2026-09-30). A seeded `SAMPLE=1` render on
  12.3.0 completed, but the pin means `pip install -r` would not resolve, so
  the fix is a moviepy upgrade first — a render change, after `v7`'s read.
  Even the latest moviepy (2.2.1) caps `pillow<12.0`, so 11.3.0 is the
  reachable ceiling; re-run `pip-audit` on it before assuming it clears all.
  **The moviepy upgrade buys no security (2026-09-30):** moviepy 2.2.1 +
  pillow 11.3.0 resolves and passes 273/273, but `pip-audit` finds **35**
  Pillow advisories on 11.3.0 (33 on 10.4.0). Every fix is ≥12.1.1, above
  moviepy's cap, so clearing Pillow means overriding the pin (the seeded
  12.3.0 render above completed), not upgrading moviepy. Also new since
  09-27: **oauthlib 3.2.2, CVE-2026-49265** (server-side PKCE timing leak).
  Exposure nil: only `regen_refresh_token.py` imports it, as a client.
  4.0.0 resolves cleanly and passes 273/273; fold into the next dependency
  release rather than spend a sample on it. **Is the Pillow override
  pixel-identical? Not proven (2026-10-01).** Patching `random.Random` to
  `Random(7)` pins clip and voice; `SAMPLE=1` under 10.4.0 vs 12.3.0
  (`pip install --target`, `PYTHONPATH`): thumbnail and audio identical, but
  **185 of 735 video frames** differ by `framemd5`. Control (10.4.0 twice):
  0 differ, so the render is deterministic and **the override is a video
  change** — its own release with a real sample, after `v7`'s read.
  **The runner image moved:** the 11-06 23:17 upload run ran on
  `ubuntu-26.04` and succeeded, so the move is done (it was due 10-19 to
  11-19). If a later upload fails on the image, the fix is
  `runs-on: ubuntu-24.04`, a workflow patch for the owner.

- **Google's daily reset is 08:00 UTC from November to March (found 2026-11-08).**
  The free tier clears at midnight Pacific time (`src/llm.py`'s 429 note), so
  08:00 UTC since US daylight time ended on 1 November, and 07:00 again from
  8 March. The shift skill (§6, "only after the 07:00 UTC reset") and
  `dry-run.yml`'s gate (`-lt 7`, pinned by `scripts/dry_run.py`'s `RESET_HOUR`
  and `tests/test_dry_run.py`) say 07:00 all year, so Gemini work or a render
  between 07:00 and 08:00 UTC in winter spends the day the uploads already
  used. Low exposure: shifts start 03:17, 11:17 and 19:17. Fix: take the hour
  from `America/Los_Angeles` in `dry_run.py` and the workflow (a patch for the
  owner) and the skill's sentence (`Approved-In`). Until then, plan Gemini work
  after 08:00 UTC in winter; PRD §0's host-line row says so.

- **An `Approved-In: #N` trailer is not bound to what it approves.** The guard
  checks that the cited issue is approved by the owner, not that the commit is
  the change that issue described — so any commit can cite any approved issue,
  including one approved for something else. A squash merge carrying several
  trailers is judged on the first alone. Auto-apply does not share this: it
  lands only the exact diff fingerprinted in the issue. Nothing suggests reuse
  has happened, and self-approval is closed (#31: only the owner's label
  counts). Options, cheapest first: refuse a cited issue that is closed, so an
  approval cannot outlive the work it approved; require every cited issue to be
  approved; move protected-file changes to the fingerprinted route. Found
  2026-09-24.
- **Swear-word gaps the filter fix left (merged 2026-10-24).** The fix for
  "'alright fuckers'" reaching a live title (2026-10-22, `IjN6hj2etcs`) is on
  `main` (dry run PASS at `58e0b2b`): `_profane` spaces out edge marks and
  checks each contracted word, and `llm._clean_published` makes a title, CTA
  or keyword with a swear word or emoji fall back. Bet 1's vote and tags get
  the same guard on `integration/preview` (from `reliability/profanity-on-v8`),
  so it ships with `v8`. Left from four reviews, not built: stretched spellings
  ("Fuuuck", "sh!t") pass every list, as the library does not fold repeats
  (folding would newly flag 0 of 1,417 logged titles and lines); a swearing
  vote in voiced mode (dormant) is untested; the library reads a curly "he’ll"
  as "hell" (fails safe, rare); YouTube's API refuses "<" and ">" in a title
  or description and nothing strips them, which would fail the upload and
  retry the same post (0 of ~2,300 past titles and answers). Live video left
  as is (retitling would alter a row of #10 and #14). **Closes when** `v8`
  ships and none of these has occurred in its first 20 uploads.

- **The repo keeps YouTube API text past YouTube's 30-day limit (found
  2026-10-24, Legal).** `analysis/channel_videos.csv` (`scripts/analyze_channel.py`,
  a one-off, last run 09-11) holds 993 uploads' titles, questions and
  answers as read from the Data API, public in this repo and its history.
  YouTube's developer policy III.E.4 lets a client keep non-statistics API
  data 30 days, then refresh or delete it; statistics may stay. The text is
  our own published videos', so the risk is low, but an API-terms breach puts
  at risk the access every upload needs. `analysis/topics_cache.json` holds
  ~1,000 question titles (from Reddit, not the API). Not fixed: dropping the
  text columns rewrites production data (CLAUDE.md §4), and history is the
  owner's. **Recommend** at the 12-07 monthly (the 11-03 monthly, which
  replaced the 11-05 review, held it with five asks open): keep IDs and
  statistics, drop the text columns at HEAD, leave history. **History also
  holds** the plain Audio Library track (`73beb1c`, 2025-01-18; sealed at HEAD
  10-10, whose script defers history to "a separate decision", never taken)
  and two dead Google login tokens (a 2025 notebook's output; 11-06). Put
  them in the same history question there. **Closes when** decided there.

- **A failed upload run emails no one (found 2026-11-01, Reliability).**
  GitHub sends a scheduled workflow's failure email to the last editor of its
  `schedule` lines. `apply-approved.yml` commits as `github-actions[bot]`, and
  its e3f5854 (10-11, #73) edited `run-reddit-video.yml`'s, so the bot gets
  them; the job has no alert of its own. The other scheduled workflows are
  the owner's. Fix is the owner's (disable, then re-enable the workflow):
  #86. Any later approved patch touching a
  `cron:` line repeats this, so its escalation must say so; `apply-approved.yml`
  is owner-only, so no guard in code. **11-01 evening: premise very likely false.** GitHub's docs make the cron's
  changer the runs' `actor` and the email's recipient; every scheduled upload
  run since e3f5854 names the owner, as `APPLY_TOKEN` (needed to push
  workflow files) is a personal token. #86 withdrawn 11-06 (its lasting piece is in #89). The lasting fix needs no
  GitHub rule: `scripts/upload_watch.py` (merged, reviewed) fails the shift
  job, whose schedule is the owner's, on under 2 uploads in 28 h or a failed
  scheduled run; its workflow patch is `upload-watch.patch` on
  `reliability/upload-watch-patch`, for the monthly's bundle (a new issue,
  as auto-apply refuses an edited one). **11-10:** #89 was refused (the owner's
  words were about replies), so the patch did not land; held so #77 and #82
  are read first. **11-13 replay** (`problems()` at all 129 scheduled shift
  starts 09-20 to 11-13, the late-cron weeks included): alarms only at 10-06's
  two, the real miss. Closest otherwise: 26.7 h of 28 (11-02 20:46), so a
  shift landing just before an evening upload about 1.3 h later than any yet
  would false-alarm; re-run the replay before the patch lands. **Closes when**
  it lands as its own ask, or is deleted with reasoning at the 12-07 monthly.
