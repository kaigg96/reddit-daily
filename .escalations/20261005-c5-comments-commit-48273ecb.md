---
title: Apply a one-line patch so the weekly job saves viewer comments
key: c5-comments-commit-48273ecb
labels: needs-owner
raised_at: 2026-10-05T22:13:17+00:00
---

## Your approval did not land

The job that applies approved changes started at 21:06 UTC, during GitHub's Actions outage, never got a machine, and was cancelled after 15 minutes with no steps run. Nothing was applied. The weekly job's file is unchanged and this issue's text is untouched, so the change you approved is still the one that will apply.

A shift cannot retry it: its token can read Actions runs but not re-run them, and the job only acts on your label. Either of these finishes it:

- Re-run run 37373796810 (Actions tab → "Apply an approved workflow change" → Re-run all jobs), or
- remove the `approved` label and add it again.

Nothing is lost until the next weekly statistics run on 12 October, which would collect the comments and then throw them away.

## Recommendation

Re-run the failed job from the Actions tab (one click), or remove and re-add the approved label. The change itself is unchanged.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*