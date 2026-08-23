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

### Considered, not done (with reasoning)

- **Refactoring `analyze_channel.py` onto `insights`.** It duplicates residual/median logic, but it's 292 working lines, run manually a few times a month, and operates on its own dict shape rather than `Video` objects. Rewriting it now is real regression risk against a script that isn't causing problems — the duplication is documented rather than churned. Revisit if it needs changes for another reason.
- **Broad Pass-2 refactor of `src/`.** The module split from Pass 1 is holding up; nothing has rotted. A general sweep would produce diff noise, not value.
- **`scripts/` naming convention** (one-time tools vs CI-invoked vs ad hoc) — still not painful at 6 scripts; still deferred.

### Deferred to a future pass

- `analyze_channel.py` residual/median duplication (above).
- No tests over the rendering path — still correctly covered by the dry-run + frame-extraction ritual, which checks things assertions can't (legibility, timing feel).
- `create_video.ipynb` remains in the repo as deprecated reference; harmless, owner's call.

## Ritual

Run this check-in after each version bump (`FORMAT_VERSION` change in `src/config.py`) or major non-video feature ships (like R4.2). Read the current state fresh — don't assume the last pass's findings still apply — propose tiered findings, get owner scoping, execute, update this file.
