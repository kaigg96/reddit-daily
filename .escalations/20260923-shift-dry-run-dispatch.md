---
title: Approve: let a shift start the dry-run render it was already given permission for
key: shift-dry-run-dispatch
labels: needs-owner,guardrail
raised_at: 2026-09-23T15:54:33+00:00
---

## What happened

The top experiment in the plan — opening each video on the question rather than
on the channel name and a "today's top question" label — is built, tested and
waiting on branch `feature/v7-open-on-hook`. It cannot merge, because the rules
require a dry run producing a playable video first, and **a shift has no way to
get one**:

- A shift holds no Polly credentials (deliberately), so it cannot narrate.
- `shift.yml` grants `actions: write` and says a shift *"dispatches
  run-reddit-video.yml with dry_run"* for exactly this. **That has never
  worked.** The Claude action replaces the `GITHUB_TOKEN` it is given with its
  own app token, which has no Actions permission. Verified this shift: both
  `GITHUB_TOKEN` and `GH_TOKEN` in the session are that app token, and listing
  or dispatching workflow runs returns HTTP 403.

So every change to the video is blocked at the last gate, on every shift. The
previous shift hit the same wall and queued it as "ask the video job for a
render" without knowing the request could not be made.

## The change (two workflow files — I cannot push these myself)

**1. `.github/workflows/shift.yml`** — pass the workflow token under a name
the action does not overwrite. (Setting the action's `github_token` input
instead would be simpler, but pushes made with the workflow token do not
trigger other workflows, so escalations would stop becoming issues.)

```diff
         env:
           GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
           # So the shift can pick up decisions the owner has already made and
           # close them out. Scoped to this repo, and no wider than what the
           # action can already do.
           GITHUB_TOKEN: ${{ github.token }}
+          # The action replaces GITHUB_TOKEN with its own app token, which has
+          # no Actions permission, so `actions: write` above never reached the
+          # session. This name survives. For dispatching dry runs only.
+          DISPATCH_TOKEN: ${{ github.token }}
```

**2. `.github/workflows/run-reddit-video.yml`** — the guard. Without it, a
shift that forgets `-f dry_run=true` would publish and move `prev_post.txt`.
With it, only you can start a real upload by hand; the schedule is untouched.

```diff
     steps:
+    # A shift may dispatch this job to render a sample (dry_run), never to
+    # publish. Only the owner may start a real upload by hand.
+    - name: Refuse a real upload not started by the owner
+      if: ${{ github.event_name == 'workflow_dispatch' && !inputs.dry_run && github.triggering_actor != github.repository_owner }}
+      run: |
+        echo "::error::Only ${{ github.repository_owner }} may start a real upload by hand; automation may only dry-run."
+        exit 1
+
     - name: Checkout Repository
```

It fails closed: anything not started by you is refused unless it is a dry
run. A run started with the workflow token reports `github-actions[bot]` as
its triggering actor. The first dry run a shift starts will confirm that from
the run's metadata, and the shift will report it, so the guard is verified,
not assumed.

## What it costs and what it allows

- A dry run spends one narration (~$0.015 of Polly) and 2–5 of the 20 daily
  Gemini requests. The existing shift limits already cover both: at most one
  dry run per shift, never within an hour of a scheduled upload.
- The token can also start the other workflows (release check, weekly
  analytics). None of them publishes anything.
- **Residual gap:** the guard lives in the workflow file of whatever branch is
  dispatched, and older branches (`integration/preview` and two landed ones)
  predate it. A shift would have to both pick one of those and deliberately
  skip dry-run mode to get past it. If you want this closed structurally,
  move the YouTube secrets into a GitHub environment limited to `main`. That
  is a settings change I cannot make. Don't delete `integration/preview` to
  close the gap: the daily release check stops running if that branch
  disappears.

## If you approve

Apply both diffs (a shift's token is refused on any workflow file) with
`Approved-In:` naming this issue, and label it `approved`. The next shift
starts the dry run on `feature/v7-open-on-hook`, checks the result, and merges
v7 if it passes.

Issue #21 (approved) is waiting for the same reason. Its one line still needs
applying by hand; it is not bundled into this one.

## Recommendation

Approve both edits below: they make the dry-run permission shifts already hold actually usable, and add a guard so a shift can never start a real upload

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*