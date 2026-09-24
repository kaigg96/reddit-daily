---
title: Approve: make approvals from your phone the last step (pre-trip)
key: pre-trip-autonomy
labels: needs-owner
raised_at: 2026-09-24T02:34:41+00:00
---

You asked on 2026-09-24 for the gaps to be closed before your trip
(Sep 25 – Oct 4), so that approving from your phone is the last step for
everything. This covers the parts that change protected files.

## What changes

1. **Approved workflow changes apply themselves.** Today a shift cannot touch
   workflow files at all, so even an approved one waits for someone at a
   computer (#21 has waited two days). A shift will now attach the exact
   change to its request; when **you** label it `approved`, a workflow applies
   precisely that change. It refuses if anyone but you applied the label, if
   the request was edited after it was raised, or if the change reaches beyond
   workflow files. It can never change the two workflows that enforce
   approvals, and the guard re-checks everything it lands.
2. **Only your label counts as approval.** A shift's access can add labels,
   and nothing checked who did. It has never happened — every approval so far
   is yours — but it has to be closed before item 1 can be trusted.
3. **Every shift report starts with "Waiting on you"**: one line per request
   that needs you, or "Nothing is waiting on you."
4. **Shifts can diagnose a failed upload**, using the new dry-run route to see
   the error they cannot read directly.
5. **The release check strips secrets** from the detail it writes into the
   repository (a gap found while landing #21).

Landing alongside, already approved: the guard fix (#28) and #21.

## One thing only you can do: create the token item 1 uses

Takes about five minutes; best done at a computer before you leave.

1. GitHub → your picture → **Settings → Developer settings → Personal access
   tokens → Fine-grained tokens → Generate new token**.
2. Name: `reddit-daily auto-apply`. Expiration: 90 days or longer.
3. Repository access: **Only select repositories → reddit-daily**.
4. Repository permissions: **Contents → Read and write**, **Workflows → Read
   and write**. Nothing else.
5. Generate it and copy it.
6. The repository → **Settings → Secrets and variables → Actions → New
   repository secret**. Name `APPLY_TOKEN`, paste, save.

Without it everything else still works; approved workflow changes just wait
for you, as they do today.

## What approving means

Label this issue `approved`, then merge the pull request you'll be sent.

## Recommendation

Approve, and create the token — after this, your label is the only thing any change needs from you.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*