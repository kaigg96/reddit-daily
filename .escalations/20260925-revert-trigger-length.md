---
title: Judge a length-changing release on total watch time too?
key: revert-trigger-length
labels: needs-owner,guardrail
raised_at: 2026-09-25T02:58:36+00:00
---

## What happened

The revert rule you set (#18) triggers on watch-seconds only. This shift found watch-seconds rises with video length alone: videos over ~20s hold 11.0 vs 9.0 seconds (+22%, ~58 uploads each, read at the same age). But they draw fewer views, so **total watch time per upload is flat** (+3% at 7 days, -13% at 14 days).

So a release that only makes videos longer would read "keep", and one that only shortens them would read "revert", with no real change in how much the channel is watched. The b-roll switch was one: it lengthened videos 1.8s at a common age, so part of its +22% keep was length (keep still stands).

## What is already done

The release check now prints each cohort's median length and flags a shift of 1s or more. v5 and v6 did not shift. v7 changes only what is on screen, so it should not shift either.

## The decision

Whether a flagged length shift should also require total watch time to hold. It tightens the rule for one case and loosens nothing. Views stay never a trigger on their own.

## Recommendation

Yes, narrowly: keep watch-seconds as the trigger, but when the release check flags a video-length shift of 1s or more, require total watch time (views x watch-seconds) not to drop before keeping. Changes nothing for v7 unless its length moves.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*