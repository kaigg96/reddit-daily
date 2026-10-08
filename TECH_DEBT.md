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

## Pass 3 — 2026-09-19 (proposed; at the pending `v6` bump) — **awaiting owner scoping**

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

Run this check-in after each version bump (`FORMAT_VERSION` change in `src/config.py`) or major non-video feature ships (like R4.2). Read the current state fresh — don't assume the last pass's findings still apply — propose tiered findings, get owner scoping, execute, update this file.

## Open items (logged between passes)

Findings that surface during feature work, recorded here so they survive past
the commit message they were noticed in. Not a formal pass; fold into the next one.

- **The Groq route is built off; four things precede switching it on
  (2026-10-08, #68).** `engineering/groq-route` sends every AI call to Groq
  when `config.AI_PROVIDER == "groq"`. Before flipping: a workflow patch giving
  `GROQ_API_KEY` to the video, dry-run, release and shift jobs, including
  each secret-stripping list (S1–S5 today); `generate_retrying` never retries
  a 429, right for Gemini's daily cap but not Groq's per-minute one (8K
  tokens/min), which a short wait clears; `screen_source` and the metadata
  source still say `gemini` whatever answered; `validate_release.py`
  refuses to run without `GEMINI_API_KEY`; a missing `GROQ_API_KEY` is
  caught, so uploads would silently ship raw titles on the keyword backstop
  (check the key before the call). The replay's two unseen wordings run only
  on groq, so their expected verdicts are untested. Reviewed 2026-10-08:
  nothing blocking; its quick fixes are on the branch.

- **Two video runs can overlap (found 2026-10-08).** `run-reddit-video.yml`
  has no `concurrency:` group, so a manual run during a late scheduled one
  checks out the same `prev_post.txt` and `upload_log.csv`: neither repeat
  guard (the 2026-10-08 upload-log one included) sees the other's pick, and
  the second push's rebase likely conflicts on the log. Rare at two a day;
  likelier at four (PRD #4, whose build should carry the one-line fix as an
  owner-applied workflow patch).

- **The public repo distributes a YouTube Audio Library track (found
  2026-10-07).** `assets/funk_bg_lower.mp3`, the only music in every upload,
  has been downloadable from the repo since it went public on 2026-10-05. The
  Audio Library terms (behind YouTube Studio's login; quoted by secondary
  sources) say "You may not make available, distribute or perform the music
  files from this library separately from videos". The Pexels clips are fine:
  its licence bars only stock and wallpaper platforms and selling unaltered
  copies. The fix needs a secret and a workflow line: the patch on #64
  (applied 2026-10-07) and `scripts/seal_assets.sh`, the owner's to run (#66,
  pending). Until then, **do not add tracks to `assets/music/` in plain
  form**: the PRD owner task to add Audio Library tracks would widen it.

- **One in-prompt example does not generalize the R4.6 screen's judgment
  categories.** The 2026-09-20 morning fix restored reasoning tokens for the
  screen after they were caught passing a `sexual_suggestive` question with
  thinking off. A same-day replay, with reasoning already restored, still
  missed a live paraphrase of the identical shape ("...dangerously flirty?")
  while correctly catching the literal in-prompt example ("...excellent in
  bed?"). Fixed by adding the paraphrase as a second calibration example
  (`src/screen.py`), pinned by a deterministic test. The generalisable part:
  reasoning tokens buy consistency on cases the model has already seen the
  shape of; they don't buy category generalization. Any future screen category
  should ship with **two** differently-worded examples, not one, and the
  standing audit (`analysis/screen_log.csv`) is the only thing that would
  catch a shape the taxonomy has zero examples of. `scripts/replay_screen.py`'s
  FLIRT case is now a memorization check, not a generalization check, since its
  question is also in the prompt — swap in a fresh paraphrase before trusting
  a pass on it as proof the category holds.

- **C15's name credits drop silently (2026-10-06).** `content.credit_name`
  leaves out deleted, profane and over-matched names: the substring check
  (list words of 4+ letters) also catches "hell" in Michelle and "rape" in
  Grape, by design, since a missed credit beats printing a slur. Nothing
  records how often it fires, and shifts cannot read Actions logs. If the
  attribution term ever turns on it, add an upload-log column (asker credited,
  answers credited of shown) through a sample run, then tune the word floor.

**Retention — open items must close, not accumulate** (cap: 25, checked by
`scripts/context_budget.py`). Every item resolves one of three ways: **fixed**
(delete it, or leave one line in the pass that fixed it), **promoted** to
`PRD.md` §0's backlog if it is really product work, or **deleted with
reasoning** if it stopped mattering. Past the cap, close before adding —
a list nobody can read is the same as no list.

- **Nothing enforces the Gemini daily total — only the per-consumer caps, and
  they sum to more than the cap.** The free tier is 20 requests/day, measured
  2026-09-19 from the 429 body
  (`quotaId=GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue=20`).
  Since the three metadata calls merged into `get_metadata`, production spends
  **2–5 per run, 4–10 per day**. But the release gate allows itself 8, a shift
  allows itself 8, and production takes up to 10 — **26 against a cap of 20,
  with no shared ledger**, so each consumer can stay inside its own limit and
  still starve the next one. Reset is midnight Pacific ≈ 07:00 UTC, which falls
  **between** the two scheduled runs (~05:00 and ~16:15 UTC), and the early run
  is last in that window, so it is always the one that starves — as it did on
  2026-09-20 (`title_ok=0 keywords_ok=0 cta_ok=0`, raw Reddit question shipped
  as the title). The dead skip in `validate-release.yml` that made this bite
  daily is fixed (2026-09-20); the unbounded total is not. **It recurred
  2026-09-24 05:03** (same all-three-zero shape, screen still `gemini`): 2 of
  the 9 `v6` uploads so far, both morning runs. The fix this item named for a
  recurrence is now due: have the gate and the dry run read the window's
  spend from a committed counter before starting, rather than trusting three
  independent caps. First, confirm the cause: the ok-flags cannot tell a 429
  from a timeout, so this diagnosis rests on timing. **Merged 2026-09-25:** the
  upload log's `meta_failure` column now records the reason (`http_429`,
  `timeout`, ...); the next all-three-zero morning row confirms or kills it.
  Also retroactively supports v6's "never retry a 429" — at 20/day a retry is
  a meaningful fraction of the budget. **2026-10-01 06:09: the screen fell to
  the keyword backstop** (`screen_source=backstop`, first since that column
  began 09-09) while the title call succeeded, so not a whole-window 429.
  **Merged 2026-10-01 (evening):** the upload log's `screen_failure` column now
  records why (`http_503`, `timeout`, `no_json`, ...) — built before a
  second occurrence, since waiting would lose that one's reason. The backstop's regex matches
  **0 of the 4** questions Gemini has skipped (`analysis/screen_log.csv`), so
  a backstop run is unscreened at post level. At ~1 in 44 runs × ~6% skips
  that is ~0.1% of runs — act only if the backstop rate rises. (A reply with
  no JSON used to pass as `gemini`, skipping even the backstop; 0 of 22 rows
  showed it. Since 2026-10-01 it falls to the backstop as `no_json`.)
  **2026-10-01 18:29: the title call failed with `http_503`**, the first
  reason recorded since the column began; title, keywords and CTA all fell
  back. The screen retried a 503 once, the metadata call never did. **Merged
  2026-10-02:** both go through `llm.generate_retrying` (503 or timeout once,
  never a 429). The 10-02 14:46 release check hit a 503 the retry did not
  clear, so a 503 that outlasts ~4s still falls back.
  **2026-10-04 06:04: `http_503` again, not `http_429`** — the shared window
  fitted; a second 503 outlasted the 4s retry and the upload lost its title.
  **Merged 2026-10-04:** a 503 now waits 30s (`_OVERLOAD_WAIT`) before its
  one retry. Another `http_503` row means 30s is not enough either; then
  consider the retry going to a model with its own allowance.
- **`est_minutes_watched` contradicts `avg_view_duration_s` in
  `analysis/analytics_snapshots.csv`.** Example: `8pEemfuXl74` — 55 views at a
  reported 30s average view duration is ~27 minutes watched, but the row logs
  `1`. This holds broadly: of 727 videos with ≥10 views in the latest snapshot,
  686 are off by more than 2× and the column clusters at 0–3 regardless of
  views. **Not decision-affecting** — `report.py` and `insights.py` judge on
  views and watch-seconds, and the traffic CSV's minutes come from a separate
  query — so the column is effectively decorative today. Worth either fixing or
  dropping before anything starts reading it. Noticed 2026-09-09 during the
  R4.6 audit. **2026-09-29: do not drop it — it may be the engaged count.** On
  the 2026-09-28 snapshot (555 videos ≥50 views), `est_minutes × 60 / (views ×
  avg_view_duration_s)` has quartiles 0.14 / 0.18 / 0.24: a steady fraction,
  not noise, never above 1 (max 0.94), median 0.176–0.180 on every snapshot
  since 2026-08-24. By publish month: 0.60 for the two videos from 2025-03
  (before YouTube's 2025-03-31 Shorts view change), 0.13–0.23 from 2025-04 to
  2026-06, then **0.36–0.40 since the 2026-07 v2 overhaul**, as if v2
  doubled the share of plays past the opening that watch-seconds called flat.
  It splits on v2's release day: 0.17 (n=16, 2026-06-01..07-17) vs 0.43
  (n=21, 07-18..07-31).
  Ad hoc and not age-matched: a lead for #8, not a finding. If `averageViewDuration` is per engaged view while `views` counts
  every play, `est_minutes × 60 / avg_view_duration_s` *is* `engagedViews`.
  **Tested 2026-10-05 (`report.py --engaged-check`): no match.** Implied/actual
  median 1.26, 13% of 830 rows within 10%, so this is not the engaged count and
  #8 has no backfill. The column is decorative again: fix or drop.
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

- **`analysis/analytics_snapshots.csv` has mixed line endings** — ~6,600 CRLF
  rows and ~890 LF, because it is appended from both CI (`autocrlf` off) and
  local runs (`autocrlf=input`, which normalizes on add). Harmless to parse,
  but every weekly diff is noisier than it needs to be. Noticed 2026-09-07
  while shipping R4.7, which pinned LF on the *new* `traffic_sources.csv`.
  Both writers are now pinned, so it will not worsen. **Normalizing the
  existing rows is deliberately deferred:** it is a ~7,500-line mechanical diff
  on a production data file, and worth doing on its own rather than buried in a
  feature commit. Owner's call.

- **The weekly shift breaker is ~2x looser on Opus 5.5, not the ~20% first
  estimated.** First Opus 5.5 shift (2026-09-23): 0.044 quota units per turn,
  against 0.059–0.098 on the three Opus 5 shifts. List prices fell 20%, but
  cache reads — most of a long session's cost — fell 60% ($0.50 → $0.20/MTok).
  So `SHIFT_WEEKLY_QUOTA_BUDGET=120` now permits roughly twice the real work it
  did when set. Whether that matters depends on how the subscription meters
  Opus 5.5, which units cannot show: compare the console's weekly % after a
  shift with a pre-5.5 one. If a shift still costs a similar share, lower the
  ceiling to ~60. One data point so far — confirm over a few shifts.

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
