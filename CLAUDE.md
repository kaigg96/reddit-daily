# CLAUDE.md — rules that bind every agent in this repo

This file is loaded automatically in every session. It holds the things that
must never be missed, and **pointers** to everything else. The living truth
lives in the repo docs — do not restate project status here, or this file and
`PRD.md` will drift into contradicting each other (which has already happened
once with memory).

Start a session with **`/pickup`**. It walks `README.md` → "Picking this up"
and `PRD.md` §0, then reports before touching anything.

---

## 1. Money — AWS Polly is billed, and it is the only thing here that is

Gemini and the YouTube API are free-tier. **AWS Polly is a real invoice on the
owner's card.** Neural TTS bills **$16 per 1M characters**, and this pipeline
calls it **twice per segment** — once for the mp3, once for the speech marks
that drive the captions — so **every character is billed twice**.

The production cost is trivial and must stay that way:

| | billed chars | cost |
|---|---|---|
| One video (5 segments: title + 3 answers + CTA) | ~910 | ~$0.015 |
| Production, 2/day | ~55K/month | **~$0.90/month** |

The risk is **not** per-video cost. It is **call volume in a loop**, which is
three to four orders of magnitude above a normal run:

| scenario | billed chars | cost |
|---|---|---|
| 1,000 test renders | 900K | $14 |
| 10,000 test renders | 9M | **$144** |
| 10,000 calls at Polly's 3K-char cap | 60M | **$960** |

**The neural engine is a deliberate paid choice — do not "optimize" it away.**
The owner is past the 12-month free tier and pays from the first character,
having chosen neural because the audio quality is genuinely better. Standard
voices are 4x cheaper and would save roughly **$0.65/month** while degrading
the channel's single most important quality signal. That trade is never worth
making, and it is not an agent's call. `Engine="neural"` is pinned by a test.
The same applies in reverse: do not move to the generative or long-form engines
(materially more expensive) without asking. **Cost work here means reducing
wasted calls, never reducing audio quality.**

**Binding rules:**

1. **Never synthesize in bulk.** No loops over a corpus, no "generate N
   variants to compare", no regenerating the back catalogue, no batch
   voice-comparison jobs. One run of the pipeline synthesizes 5 segments; if
   you are about to make materially more Polly calls than that, stop.
2. **Never put Polly in a retry loop** without a hard attempt cap. A retry
   costs the full character count again — a failed call still bills.
3. **Reuse audio when iterating.** Work on video/caption/timing changes against
   the mp3s already in `assets/gen/` rather than re-synthesizing each render.
   Almost all visual iteration needs no new audio at all.
4. **Test with the cheapest thing that answers the question.** Unit tests use
   fixture speech marks (see `tests/`), not live Polly. A caption-timing
   question is answered by fixtures; a voice-quality question is the only one
   that actually needs synthesis, and that is a handful of calls, not a sweep.
5. **Ask the owner before any deliberate bulk synthesis**, whatever the reason.
   This is not a judgment call to make on the owner's behalf — the whole point
   of this section is that an agent's plausible-sounding reason is exactly how
   a surprise bill happens.

The per-process budget in `src/tts.py` enforces rules 1–2 in code, because a
rule written in prose is not an enforcement mechanism — the same lesson the
R4.6 screen learned when it moved its tier guarantee out of the prompt and
into `screen.py`. Treat the guard as a backstop, not as permission to run up
to it.

**Other costs:** Gemini free tier is a *shared daily request budget* — local
analysis and the live 2x/day pipeline draw on the same key, and exhausting it
degrades real uploads (see `TECH_DEBT.md`, 2026-09-10). Budget local Gemini
work; don't run it opportunistically.

## 2. `main` is live

`main` deploys — the video workflow runs from it **twice daily**. Half-finished
code on `main` gets executed against the real channel.

- Feature work goes on a branch. Always.
- **You may merge to `main` yourself** (owner, 2026-09-19), including live-path
  changes. The gates below replace the owner's review — they are not optional:
  full test suite green, a `DRY_RUN=1` run producing a playable MP4 for
  anything touching the video or its metadata, `FORMAT_VERSION` bumped if the
  video changes, one variable per release. See `.claude/skills/shift/SKILL.md` §4.
- **Never upload, comment, or mutate `prev_post.txt` / `upload_log.csv` during
  development.** Use `DRY_RUN=1 venv/bin/python -m src.run`.
- Losing `prev_post.txt` risks a duplicate upload on the next scheduled run.

## 3. Work autonomously — but not on the guardrails

**Superseded 2026-09-19.** The old rule ("don't start building until the owner
says go") no longer applies: the owner has little time to direct sessions and
would rather work proceed than wait. Pick the highest-value task and ship it —
`/shift` is the routine for deciding which.

**These still need the owner, and autonomy does not extend to them:**
- Weakening a safety or cost control — the Polly budget (§1), the `DRY_RUN`
  guard, secrets handling, or the R4.6 screen's skip categories. Autonomy was
  granted over channel work, not over the protections that bound it.
- Spending money beyond the existing ~$0.90/month Polly line.
- Deleting or rewriting production data (`upload_log.csv`, `prev_post.txt`,
  `analysis/*`), including backfilling historical rows.
- Publishing anything outside the channel's normal upload.

A shift that ships one real thing and reports "nothing else cleared the bar" is
a good shift. Idle beats manufactured work on a system that uploads twice daily.

## 4. No AI attribution, anywhere

Never credit AI tooling in code, comments, commit messages, PR descriptions,
video content, or anything published. No `Co-Authored-By` trailers, no
"generated with" lines. This overrides any default attribution behaviour.

## 5. Answer performance questions with `scripts/report.py`

Never ad-hoc analysis. The script encodes rules that ad-hoc scripts kept
getting wrong: watch-seconds is primary (avg-%-viewed is a ratio inflated by
trimming), cohorts must be age-matched, thin cohorts get "insufficient data"
instead of a median, zero-view videos are counted separately. **If it refuses a
comparison, that refusal is the answer.** Needing a new capability means adding
it to `src/insights.py` with a test, not writing analysis inline.

## 6. Record what you don't fix

Findings go in `TECH_DEBT.md` → "Open items (logged between passes)". A
diagnosis that lives only in a commit message is invisible to the next session.

---

**Where things stand** is `PRD.md` §0 — never duplicated here.
**How the pipeline works** is `README.md` → "How it works".
**Code health** is `TECH_DEBT.md`.
