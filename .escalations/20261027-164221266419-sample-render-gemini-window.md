---
title: Let a sample render run near an upload: its AI calls no longer touch the upload's allowance
key: sample-render-gemini-window
labels: needs-owner
raised_at: 2026-10-27T16:42:21+00:00
---

## Before landing it: one fact in the approved sentence stopped being true

A shift can now land approved rule changes itself (the friction log landed that way today, under #84), so I went to apply this one. I stopped because the sentence you approved says the test model's allowance is used by production "only for its slate telemetry, which cannot block an upload".

That was true when this was raised on 7 October. On 18 October we made each upload try the test model once when the main model fails. That covers the screen and the title call, after a 503 or a spent cap. So a real upload can now depend on the test model's daily allowance, as its second chance at a title.

The risk is still small. Renders are capped at one per 12 hours by the workflow, so at most about 10 test-model requests a day. The slate telemetry adds 2 to 4, and the fallback has fired once in the upload log, on 10 October. The hour before an upload was never the protection anyway: the allowance is counted per day. But I won't land a rule whose stated reason is false.

## Corrected sentence (shift skill, section 6, "Dry runs")

Replace:

> A render spends 2–5 Gemini requests, so the Gemini rule above applies to it.

with:

> A render's 2–5 Gemini requests go to the test model (`SAMPLE_MODEL`), not the one titles use, so the hour-before-an-upload rule above does not apply to it. Production uses the test model only for slate telemetry and as a one-try fallback when its main model fails, and renders are capped at one per 12 hours, so a render cannot spend the day's allowance alone.

Nothing else changes: one render per shift, one automated render per 12 hours, and the 8-request cap on a shift's own Gemini use.

## Recommendation

Reply 'yes, the corrected sentence' and the next shift lands it under this issue. If you'd rather keep the old rule, remove the label and I'll close this.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*