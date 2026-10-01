---
title: Let a shift request a sample render outside the Gemini timing window?
key: dry-run-timing-rule
labels: needs-owner,process
raised_at: 2026-10-01T16:33:47+00:00
---

## What happened

On 2026-10-01 the subreddit-rotation sample video was due "after 12:00 UTC, not
within an hour of the evening upload". No shift ran in that window; the 16:30
shift found the evening run already due (queued since 12:23, lands 16:30–18:10)
and, following the shift skill §6, did not request it. The build loses a day.

## Why the rule no longer protects anything real

The skill says a render "spends 2–5 Gemini requests, so the Gemini rule above
applies to it." Since 2026-09-25 every Gemini call under `DRY_RUN` goes to the
sample model (`gemini-3.5-flash-lite`, `src/llm.py` SAMPLE_MODEL), which has its
own free-tier quota. Production's only call on that model is the slate
classifier (`config.SLATE_MODEL`) — telemetry that never influences the upload.
So the worst case of a render next to a live run is one missing slate value,
not a lost title or screen.

## Proposed wording (shift skill §6, Polly bullet, final sentence)

> A render's 2–5 Gemini requests go to the sample model, whose only production
> use is the slate telemetry call, so the timing rule above does not apply to
> it — request whenever ready.

The skill file is write-protected from shifts, so this needs your edit or an
approval that a shift can act on.

## Recommendation

Yes — replace the shift skill's last sentence of the Polly bullet in §6 with the wording below; the one-render-per-12-hours cap and one-per-shift limit stay

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*