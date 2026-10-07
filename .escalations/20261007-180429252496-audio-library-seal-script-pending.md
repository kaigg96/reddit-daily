---
title: The music fix is half done: please run the sealing script (about two minutes)
key: audio-library-seal-script-pending
labels: needs-owner,security
raised_at: 2026-10-07T18:04:29+00:00
---

## Where it stands

You approved #64, and its workflow half landed at 13:38 UTC today, which closed the issue. The other half is yours alone: `scripts/seal_assets.sh`. It encrypts the track, stores the key as a secret and removes the plain file. It has not run yet. `assets/funk_bg_lower.mp3` is still in the public project in plain form, so the licence problem #64 described is still live.

Nothing is broken meanwhile. With no sealed file present, the new unsealing step does nothing and uploads keep their music.

## What to do

From the repo root, on an up-to-date `main`, with `gh` logged in as an admin of the repo:

    bash scripts/seal_assets.sh

Then push. The script refuses to run twice, so a second run cannot lose the key. Afterwards a shift will check that the next upload's log names the track rather than "none".

As #64 said, git history still holds the plain file; rewriting history is a separate decision.

## Recommendation

Run scripts/seal_assets.sh once from an up-to-date main on your machine, then check the next upload's log names the track.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*