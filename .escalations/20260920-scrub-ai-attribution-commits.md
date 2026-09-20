---
title: Scrub AI attribution from two commits on main?
key: scrub-ai-attribution-commits
labels: needs-owner
raised_at: 2026-09-20T17:17:53+00:00
---

## What happened

The first autonomous shift (2026-09-20) added
`Co-Authored-By: Claude Sonnet 5` to both of its commits — `89bc245` and
`06d2f1e`, now on `main`.

`CLAUDE.md` §5 forbids exactly this and explicitly says it "overrides any
default attribution behaviour". The shift read that file and did it anyway,
so the action's default beat the written rule.

## Already fixed going forward

`shift.yml` now fails any run whose commits carry AI attribution. Verified
against the two real violating commits (caught) and against clean ones (no
false positive). It cannot recur.

## The decision

Only whether to scrub the two existing commits. That means rewriting `main`'s
history and force-pushing — `main` is the deployment branch, and both the
video workflow and the Actions bot commit to it, so a force-push can lose
state written between my rewrite and the push. That is why it is your call
rather than mine.

## Recommendation

Leave them. The repo is private, the trailer is now blocked in CI so it cannot recur, and force-pushing main is riskier than the two lines are worth — the video workflow and the bot both commit there. Say the word if you'd rather I rewrite them.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*