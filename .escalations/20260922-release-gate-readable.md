---
title: Approve one line so a failed release gate explains itself
key: release-gate-readable
labels: needs-owner,guardrail
raised_at: 2026-09-22T14:16:46+00:00
---

## What happened

The release gate has recorded **FAIL on every run since it was created** —
2026-09-20, -21 and -22 — and has never once passed. Today I re-ran both gates
live against `main`: gate 1 passes, gate 2 is 5/5. **The code is fine and the
gate is wrong about it.**

One cause is now fixed and merged (`c984ebf`): `get_metadata` fails soft, so a
spent Gemini quota and a degraded prompt both arrived as three empty fields,
and the gate called both "do not merge". It now tells them apart, the way the
screen gate already did.

But I could not confirm that is what actually happened on any of the three
days, because **the reason exists only in an Actions log a shift's token
cannot read** (HTTP 403). The verdict file exists precisely so a cold session
learns the outcome without spending quota — and on the FAIL path, the only
path where the reason matters, it hands the reader a link they have no key
for. That has now cost three shifts running: 2026-09-20 re-ran the gates
locally to find out (8 of 20 daily Gemini requests), 2026-09-21 could not
afford to at all, and today's found healthy gates and still cannot close
issue #20.

## What I am asking for

One line in `.github/workflows/validate-release.yml`. The content it appends
is already on `main` and tested — `validate_release.py` writes the detail to a
gitignored scratch file, capped at 1500 characters. Until this line lands, it
is written and thrown away.

```diff
             echo "[Full output](.../actions/runs/${{ github.run_id }})"
           } > .github/last-release-validation.md
 
+          # Why it ruled that way, not just how.
+          cat .github/last-release-detail.md 2>/dev/null >> .github/last-release-validation.md \
+            || echo "_(the gates recorded no detail)_" >> .github/last-release-validation.md
+
           git config --global user.name "github-actions[bot]"
```

It grants no new permission, spends nothing, and cannot fail the run — a
missing file falls back to a placeholder (verified). It is deliberately one
line with the content in a script, so a future shift can change what the
detail says without asking you again.

## Two process notes, since they cost this shift real time

1. **A branch was the wrong instruction.** The rules say to propose a workflow
   change on a branch and escalate. I cannot push one: the shift's token is
   refused with *"refusing to allow a GitHub App to create or update workflow
   ... without `workflows` permission"*. So the patch is inline above rather
   than reviewable as a branch. Worth either granting that scope or changing
   the rule to say "inline the patch".
2. **This fix was already approved-adjacent and got lost.** It was recorded in
   `TECH_DEBT.md` as "bundle into #14's approval rather than raising a third
   ask". #14 was approved and closed, its other half was done — and this half
   silently died with the issue. Stacking a request behind someone else's
   approval does not survive that approval being closed.

## To apply

Cherry-pick the one hunk, or commit it with a trailer naming this issue:
`Approved-In: #<this issue>` (required by `protect-process.yml`, which
otherwise reverts it).

## Recommendation

Approve. It adds no permission and no cost; it moves detail the gate already produces into the file shifts already read.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*