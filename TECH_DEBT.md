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
- **`median` consolidated** to one implementation; `analytics.median` now delegates to `insights.median`.
- **`requirements-dev.txt`** added so pytest stays out of the CI runtime install.

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

- **The Gemini free-tier daily cap is 20 requests, not the few hundred everyone
  assumed — and production needs 8–14 of them.** Measured directly 2026-09-19
  from the 429 body:
  `quotaId=GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue=20`.
  Per run the pipeline spends 1–4 on the R4.6 screen (`MAX_SCREENED_CANDIDATES`),
  plus one each for keywords, title and CTA = **4–7 per run, 8–14 per day**, so
  **production alone is 40–70% of the cap** with no headroom on a bad day.
  **PRD §2's "comfortably inside the free tier at 2 runs/day" is false** and has
  been corrected. Consequences worth deciding on:
  - **Any local Gemini work competes directly with live uploads.** The
    2026-09-10 note below guessed at this; it is now measured, and it is worse
    than that note assumed. A single replay run (5–8 calls) is a third of the
    day's budget.
  - **The cheapest structural fix is fewer requests, not fewer tokens** — the
    quota counts *requests*. `get_keywords` + `get_video_title` + `get_cta` are
    three calls against the same post and could be one, taking a run from 4–7
    to 2–5. Not done here: it changes prompt behaviour on the live path and
    wants its own review.
  - This also retroactively supports the v6 branch's "never retry a 429"
    decision — at 20/day a retry is a meaningful fraction of the budget.
  - Reset is midnight Pacific ≈ 07:00 UTC, which falls **between** the two
    scheduled runs (~04:50 and ~16:45 UTC). So the early run is the one exposed
    to a budget already spent the previous day.
- **Gemini failures are invisible in `upload_log.csv` for three of the four
  call sites.** `screen_source` (v6 branch) covers the screen, but a failed
  keyword, title or CTA call is only inferable — and only for the title, by
  comparing `video_title` to `post_title`. That inference is how the regression
  above was found at all, and it is fragile. Worth `title_ok` / `cta_ok` /
  `keywords_ok` columns on the established `caption_ok`/`comment_ok` pattern.
  Noticed 2026-09-19.
- **`title_style` is logged on uploads whose title was never generated**,
  contaminating the R2.2 A/B/C experiment: 10 of 127 rows (8% lifetime, but
  **23% of the last 30**) claim a style that was never applied, because the run
  fell back to the raw Reddit question. Per-cohort the mislabel rate is A 7% /
  B 12% / C 5%, i.e. unevenly spread, so it biases the comparison rather than
  just adding noise. The style should be logged blank when generation failed,
  which also makes `report.py --compare` correct automatically (it already
  excludes rows where the field is unset). Noticed 2026-09-19.
- **Generated titles can contain emoji, while Reddit posts containing emoji are
  filtered out at selection.** `sanitize_title` strips quotes and whitespace but
  not emoji, so the pipeline rejects emoji in source content and then adds its
  own: 1 of 127 shipped titles (`Your Pets' Secret Drama? Tell Us! 🤫`), and the
  model volunteered one in 2 of 4 test generations on 2026-09-19. Low impact and
  arguably fine on YouTube, but it is an inconsistency someone should decide on
  rather than discover. Noticed 2026-09-19.

- **`est_minutes_watched` contradicts `avg_view_duration_s` in
  `analysis/analytics_snapshots.csv`.** Example: `8pEemfuXl74` — 55 views at a
  reported 30s average view duration is ~27 minutes watched, but the row logs
  `1`. This holds broadly: of 727 videos with ≥10 views in the latest snapshot,
  686 are off by more than 2× and the column clusters at 0–3 regardless of
  views. **Not decision-affecting** — `report.py` and `insights.py` judge on
  views and watch-seconds, and the traffic CSV's minutes come from a separate
  query — so the column is effectively decorative today. Worth either fixing or
  dropping before anything starts reading it. Noticed 2026-09-09 during the
  R4.6 audit.
- **The SRT track fails to upload roughly half the time.** The `caption_ok`
  telemetry added 2026-09-07 has 5 rows and 2 are `0`; `comment_ok` is 5/5.
  The telemetry did its job — this was invisible before. Deliberately not
  chased: R4.7 measured the search surface at 1.3% of views, so the SRT is an
  accessibility nicety, not a growth lever. Revisit only if the failure rate
  holds over a larger sample and the fix is cheap. Noticed 2026-09-09.
- ~~**Scheduled runs now land ~4h25m after their cron slot**~~ — the two stale
  doc claims were corrected 2026-09-19 (workflow cron comment, and PRD §1/§4's
  "00:00 and 12:00 UTC"). The drift itself remains deliberately unchased; the
  original note is kept below for the reasoning. **Scheduled runs land ~4h25m
  after their cron slot**, up from ~40–90 min
  in July (actual publish ~04:48 / ~16:45 UTC against a `23 0,12` cron). This
  is GitHub Actions queue delay, not a bug in the job — but it is *drifting*,
  which means publish time is an uncontrolled variable moving underneath every
  cohort comparison. Already instrumented: `median_publish_drift` in
  `weekly_digest.py` alerts above 120 min, so the 2026-09-14 digest will fire
  it. **Two docs are now factually wrong** and want a one-line fix each: the
  `run-reddit-video.yml` cron comment still claims "actual publish lands ~10
  min later; acceptable", and README/PRD still describe the slots as 00:00 and
  12:00 UTC. Noticed 2026-09-09.
- **FIXED 2026-09-19 — `load_videos` silently dropped every 0-view upload.**
  Recorded here because the *class* of bug matters more than the fix: the
  Analytics API returns no row at all for a video with exactly 0 views, and
  `load_videos` did `if not s: continue`. So the uploads that vanished from
  every median, every `--by` grouping and the zero-view count were precisely
  the worst performers — and among them **both surviving confirmed-suppression
  cases** (`VDH3pSafyE0`, `_0MNAf8AzNg`), i.e. the entire evidence base for
  R4.6's skip categories was invisible to the tool the PRD tells you to verify
  it with. Measured effect on the live channel: zero-view uploads **1 → 4**,
  cohort **118 → 121**; headline medians unchanged. A missing row is now read
  as a genuine zero, except for non-public videos, which are excluded and
  counted in a printed note. Non-public vs cold-spell vs isolated was already
  encoded in `classify_zero_views` — it just had never been carried into the
  join. Worth remembering that `--zeros` was right all along while the overview
  was wrong: two paths over the same question disagreed for weeks and nothing
  flagged it.

- **The Gemini free-tier daily budget is smaller than the pipeline assumes, and
  is shared between production and any local analysis.** On 2026-09-10 an R4.3
  re-run exhausted it within ~90 minutes of the 07:00 UTC reset, which means the
  16:45 UTC video run that day very likely executed with no Gemini at all:
  keyword-backstop screening, and Reddit's own title instead of a generated one.
  Nothing breaks — every path fails soft — but the upload is materially worse
  and nothing in the logs said so at the time. PRD §2 says usage is "comfortably
  inside the free tier at 2 runs/day", which is true for production alone and
  false as soon as anything else shares the key. Worth deciding on: (a)
  `screen_source` (v6 branch) will start showing how often production actually
  loses Gemini; (b) local analysis should run right after a reset **and** be
  budgeted rather than run opportunistically; (c) retry policy must treat a
  repeated 429 as a stop signal rather than a reason to try harder —
  `analyze_channel` now does, and `src/screen.py`'s widened retry is unverified
  under quota pressure. Noticed 2026-09-10.
- **`analysis/analytics_snapshots.csv` has mixed line endings** — ~6,600 CRLF
  rows and ~890 LF, because it is appended from both CI (`autocrlf` off) and
  local runs (`autocrlf=input`, which normalizes on add). Harmless to parse,
  but every weekly diff is noisier than it needs to be. Noticed 2026-09-07
  while shipping R4.7, which pinned LF on the *new* `traffic_sources.csv`.
  Both writers are now pinned, so it will not worsen. **Normalizing the
  existing rows is deliberately deferred:** it is a ~7,500-line mechanical diff
  on a production data file, and worth doing on its own rather than buried in a
  feature commit. Owner's call.
- **Digest surfaces `channel_7d` traffic, README says decide on `logged_uploads`.**
  Both are correct for their purpose (7d is the drift series, logged_uploads is
  the current-format cohort), but a reader skimming the digest could take the
  weekly number as the decision number. Revisit if the two ever diverge much.

