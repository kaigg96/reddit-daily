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

- **No automated tests exist.** Not urgent for the rendering path (correctly verified by the existing dry-run + frame-extraction ritual — genuinely visual/audio correctness that needs eyes, not assertions). But `weekly_digest.py`'s date/threshold arithmetic (cadence windows, unlogged-video buffers) and `analyze_channel.py`'s stats (age-adjusted residuals, distinctive terms) are pure, deterministic, and have already needed two manual recalibrations this week from eyeballing — exactly the class of bug a small `pytest` suite over just those functions would catch for free. Owner scoped this pass to Tier 1+2 (cleanup + structure) and left testing for later; worth revisiting at the next check-in.
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

- **A shift ended after 2 minutes with no handover (run 39338110057,
  2026-10-19; the first in 40+ runs).** 32 turns, no commits, no error; same
  Claude Code (2.1.280) and action as the passing runs, and the budget gate
  returns GO in CI. Cause unknown: the transcript was hidden. Likeliest, it
  found every queue item waiting on the owner and ended without §10's entry.
  **Visibility (owner, 2026-10-20):** `scripts/shift_trace.py` writes how a
  shift ended (with an error result's reasons), its last message and its tool
  calls, redacted, to `.github/last-shift-trace.md`; the emailed report now says
  when a shift wrote no handover, with the trace's head. The workflow step that
  runs it is the owner's to approve (its escalation, 2026-10-20). Not new, from
  its review: a WORKLOG commit someone else pushes during a shift counts as that
  shift's handover, in the workflow's check and the report alike. **Closes
  when** the step is live and ten more shifts pass, or a repeat is root-caused
  from its trace.
- **The owner's machine cannot run bet 1's build, and only it can narrate a
  sample (2026-10-19).** Its `venv` is Python 3.10; CI runs 3.12, and
  `src/llm.py` on `integration/preview` uses an f-string with nested quotes
  (3.12+), so `DRY_RUN=1 venv/bin/python -m src.run` fails to import there
  (that f-string rewritten for 3.10 on `product/host-tags`, 2026-10-20).
  That night's renders used a throwaway 3.12 venv. Its git (2.37) also fails
  `test_check_docs`'s two merge-tree tests (`--write-tree` needs 2.38;
  skipped below 2.38 since 2026-10-20). It
  matters because CI samples are silent (branch code never holds the Polly
  keys) and the owner judges format changes with narration (#77): a narrated
  sample is a local run. Also: there is no way to re-render from saved
  narration, so each timing tweak costs a Polly run (CLAUDE.md §1 asks for
  reuse). **Closes when** the venv is rebuilt on 3.12 (`/usr/local/bin/python3.12`
  is installed) and a render can reuse the last run's narration. Both are
  built on `product/host-tags` (2026-10-20): it imports on 3.10, and
  `REUSE_NARRATION=1` on a dry run buys each line once; closes when it merges.
  Re-checked 10-21 on `46548ae` under 3.10: 656 tests pass and a `SAMPLE=1`
  render plays; `google-api-core` warns it will drop 3.10, so rebuild anyway.

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
  fallbacks in 180 uploads.

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
  twice, fixed). Merge it after `v8`, before the switch, on tests and review:
  no sample reaches it (a dry run returns before the log), and `prev_post.txt`
  is written first, so a fault there cannot repeat an upload. **At the switch, keep
  `MAX_SCREENED_CANDIDATES` at 4:** PRD §2's cut to 2 was the free route for
  Gemini's worst case, which `v8`'s Groq fallback now answers, so the cut
  would cost screen depth for nothing (10-13). Raise `CANDIDATE_LIMIT` as §4 says. The delay is not rising: weekly median 4.3–4.6h (W36–W38),
  5.5h (W40), 5.9h (W41), then 4.6h over W42's 14 uploads (10-19; 6.5h was its
  first 3), so the median run still lands before the next slot; the worst
  (8.9h) does not. Runs are safe (`run_slot` takes
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
  `run.py`'s source, not the written row). It and `product/vote-comment-caps`
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
  on `meta_source` once any appear; 3 `test_llm` tests fail with `DRY_RUN=1`
  in the shell (on `main` too; fixed on `reliability/run-slot-log`, after `v8`). **Switch on in `src/config.py`, never a
  workflow or repo variable:** the release check re-runs only when code
  changes. Some log lines still say "Gemini" whichever route answered.
  **Since 10-18 the metadata call tries Gemini's second model before Groq**,
  as the screen has since 10-09: two 503s 30s apart cost the 16:02 upload
  its title, keywords and CTA (third since 10-01, all 503s). Its answer logs
  a `meta_failure` beside fields logged ok and counts as `gemini` in
  `title_writer`; the release check switches it off. Both bet 1 branches
  conflicted with it in `get_metadata`'s failure branch and are pre-resolved
  (`integration/preview`, `integration/two-answer-meta-fallback`): the second
  model first, given the main call's reply schema.

- **Audit 2026-10-21: bet 1 waits on a render only the owner's machine can
  make; otherwise the process is working.** 10 shifts since 10-17, 2–56 of 60
  minutes (mean 38). Nothing reached viewers; 10 merges, all measurement or
  reliability. Bet 1's craft moved under D14 (notes became tags, upload-model
  reactions, the setup gate), each reviewed fresh. Reviews caught real defects
  (R3's age guard, a tag-trial test of the wrong thing); the release check
  passed daily; no reverts. Distribution and finance got no time, with nothing
  ready: fine while the 11-05 monthly runs. **Found:** (1) #77's body went
  stale a second time (it described notes, and said a label alone ships while
  its 10-21 comment asked for a render): rewritten 10-21. The fix that ends it
  is the re-raise below. (2) D13's "owner absent" line was stale and seeded a
  ship-unless-they-object candidate; re-reviewed. (3) `backlog_status.py
  --dropped` lists only drops, so the generator re-proposed done work (bet 2's
  start date, answered 10-17 and 10-19) and a ranker put it first. Fixed: `--dropped`
  also lists each entry's Done openings (reviewed). Left: a shift that re-stamps
  its time and rewords its headline still lists twice (10-18 08:45/08:50). (4) Narrated branch samples
  (main's code narrating the branch's script) would take the owner's hands off
  the critical path, but touch secrets handling: for the 11-05 review, not an
  ask beside #77. Decisions: D13 re-reviewed; the rest unchanged. Outward look
  not repeated (done 10-13). **Carried, pending #50:** a re-raise that changes
  the ask replaces the body (built on `process/reraise-replaces-ask`, the filer
  as a patch in `.github/pending/` with the weekly install's pin below; raise
  with `--patch` when #77 settles, then merge); the shift skill's false "cannot
  read Actions logs" (`gh run view <id> --log` works); a Stop hook refusing to
  stop before the handover is pushed. **Before `v8` merges:** read Groq-written
  uploads apart (`--by meta_source`; titles `--within title_writer!=groq`).
  **Closes when** #50 lands and the bundle is raised, or the next audit.

- **The weekly snapshot job installs its libraries unpinned (2026-10-14).**
  `weekly-analytics.yml` names three Google packages in `pip install`; every
  other workflow reads `requirements.txt`, and `test_requirements.py` reads
  only the requirements files. A broken release on a Monday loses that week's
  snapshot for good (no backfill). Not raised alone: unlikely, and the owner's
  queue is the binding limit. Patch and test built 10-18 (the bundle above).
  **Closes when** the next workflow patch to the
  owner carries `pip install -r requirements.txt` there, with a test that
  fails any workflow `pip install` naming a package.

- **C15's name credits drop silently (2026-10-06).** `content.credit_name`
  leaves out deleted, profane and over-matched names: the substring check
  (list words of 4+ letters) also catches "hell" in Michelle and "rape" in
  Grape, by design, since a missed credit beats printing a slur. Nothing
  records how often it fires. If the
  attribution term ever turns on it, add an upload-log column (asker credited,
  answers credited of shown) through a sample run, then tune the word floor.

**Retention — open items must close, not accumulate** (cap: 25, checked by
`scripts/context_budget.py`). Every item resolves one of three ways: **fixed**
(delete it, or leave one line in the pass that fixed it), **promoted** to
`PRD.md` §0's backlog if it is really product work, or **deleted with
reasoning** if it stopped mattering. Past the cap, close before adding —
a list nobody can read is the same as no list.

- **Pillow is ageing out.** (Python moved to 3.12 on 2026-10-07, #63; the
  next upload ran on it and README follows. requests 2.33.1 merged 2026-09-30.)
  `pip-audit` finds published advisories against **Pillow 10.4.0** (33+).
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
  **The runner image moves (2026-10-19):** `ubuntu-latest` becomes 26.04
  between 10-19 and 11-19 (GitHub changelog, 09-17). Checked: no workflow
  installs a system package or calls a system tool; `setup-python` has 3.12
  for 26.04; ffmpeg and fonts ship with the repo's packages and assets. If
  an upload fails in that window, suspect the image first; the fix is
  `runs-on: ubuntu-24.04`, a workflow patch for the owner.

- **`analysis/analytics_snapshots.csv` has mixed line endings** — ~6,600 CRLF
  rows and ~890 LF, because it is appended from both CI (`autocrlf` off) and
  local runs (`autocrlf=input`, which normalizes on add). Harmless to parse,
  but every weekly diff is noisier than it needs to be. Noticed 2026-09-07
  while shipping R4.7, which pinned LF on the *new* `traffic_sources.csv`.
  Both writers are now pinned, so it will not worsen. **Normalizing the
  existing rows is deliberately deferred:** it is a ~7,500-line mechanical diff
  on a production data file, and worth doing on its own rather than buried in a
  feature commit. Owner's call.

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
