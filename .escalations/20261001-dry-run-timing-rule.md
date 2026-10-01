---
title: Let a shift request a sample render outside the Gemini timing window?
key: dry-run-timing-rule
labels: needs-owner,process
raised_at: 2026-10-01T16:35:13+00:00
---

## It has now happened twice

The 2026-09-30 shift (started 12:44, scheduled 09:17) also missed the
rotation sample's window. Two clocks constrain the sample, not one: this timing
rule, and the rotation itself, which draws the new subreddit only in alternating
half-days (after 12:00 UTC on 1 October, before 12:00 on 2 October). Shifts
start hours late, so the overlap keeps closing before anyone reaches it.

Retiring the timing rule removes one clock. A follow-up that would remove the
other: let a dry run pin the subreddit (a `DRY_RUN`-only override passed by
`dry-run.yml`), so a sample proves the new subreddit whenever it is taken.
That needs a workflow edit, so it would come to you as a patch; I would build
it only if you want it.

## Recommendation

Yes — same wording as above; this is the second missed window, so the cost is recurring

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*