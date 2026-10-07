---
title: Let a sample render run near an upload: its AI calls no longer touch the upload's allowance
key: sample-render-gemini-window
labels: needs-owner,process
raised_at: 2026-10-07T18:00:38+00:00
---

## What happened

This evening's shift had a finished branch waiting only for its sample video (the host's vote, built switched off), and could not ask for it. The shift rules forbid any AI request within an hour of a scheduled upload, and say a sample video's requests count under that rule.

That was true when it was written. Since 25 September a sample video sends every AI request to a separate test model with its own daily allowance (`SAMPLE_MODEL` in `src/llm.py`, `SLATE_MODEL` in `src/screen.py`). Production uses that model only for its topic-telemetry call, which by design cannot hold up an upload. So a sample video cannot cost a real upload its title, which is the reason the rule gives.

Because GitHub starts our scheduled jobs hours late, shifts often land near an upload, as this one did (started 17:49 UTC; the evening upload usually runs 18:00–18:30). The rule then blocks a render for no protection.

## The change (shift skill, section 6, "Dry runs")

Replace:

> A render spends 2–5 Gemini requests, so the Gemini rule above applies to it.

with:

> A render's 2–5 Gemini requests go to the test model (`SAMPLE_MODEL`), whose allowance production uses only for its slate telemetry, which cannot block an upload: the Gemini rule above does not apply to it.

Unchanged: one render per shift, one automated render per 12 hours (enforced in the workflow), and the 8-request cap for a shift's own Gemini use.

A shift cannot make this edit: skill files are write-protected from it. Label `approved` and apply it, or reply with changes.

## Recommendation

Approve the one-sentence change below to the shift rules. It only lets a shift ask for a sample video at any hour; it spends nothing new.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*