---
title: Give approved process-file changes a way to land without your hand edit?
key: process-file-landing-path
labels: needs-owner,process
raised_at: 2026-10-02T16:00:00+00:00
---

## What happened

On 2026-10-02 you approved #44 (retire the sample-timing rule in the shift
skill). The shift could not apply it: the session is refused write access to
`.claude/skills/`, and `apply-approved.yml` only applies patches to
`.github/workflows/` (`escalate.py --patch` refuses anything else). So the
decision is in force but the skill text still states the old rule, and every
later shift reads the old rule until you edit it by hand.

The 2026-10-01 shift hit the same wall from the other side: it could not even
put proposed wording on a branch, so the wording went into the issue body.

## Why it matters

`CLAUDE.md` §4 says a skill or `CLAUDE.md` change lands "only with
Approved-In: #N". Today that path exists for workflow files alone. For the
process files themselves, approval leaves a hand edit owed to you, and the
gap between decision and text is where shifts follow a rule you already
retired.

## Proposal

Let `escalate.py --patch` accept `.claude/skills/**` and `CLAUDE.md` as well as
workflow files, and let `apply-approved.yml` apply them under the same checks:
your label, the unedited issue, the sha256 fingerprint, and never
`protect-process.yml` or `apply-approved.yml`. The commit carries
`Approved-In: #N` as it does today, so `protect-process.yml` keeps it.

This touches `apply-approved.yml`, which only you land, so it cannot come as a
patch. If you approve it, the edit to `escalate.py` and a test can follow
from a shift; the workflow line is yours.

## Recommendation

Yes — extend auto-apply to the skill files and CLAUDE.md, keeping the fingerprint check and the exclusion of the two enforcing workflows. If you would rather keep those files hand-landed, say so and shifts will stop proposing wording they cannot apply.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*