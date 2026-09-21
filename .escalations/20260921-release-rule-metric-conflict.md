---
title: The revert rule's first real verdicts: b-roll says revert, but on the metric you don't rank first
key: release-rule-metric-conflict
labels: needs-owner,guardrail
raised_at: 2026-09-21T16:10:35+00:00
---

## What changed

The auto-revert rule now works. It has never produced a verdict on anything we
have shipped — a release applies to every upload after it and none before, so
there was never a same-age group to compare it against (issue #16, which you
approved). The weekly performance data we keep turns out to solve it: it has
ten weekly readings per video, so a July upload can be read at exactly the same
age as a September one. Built and merged today; it needs no account access, so
an unattended session can run it.

Two things it turned up are yours to decide.

## 1. Views on this channel are too noisy to revert on

Measured at a fixed age, with nothing changed, the channel's views move 27–52%
between consecutive batches of uploads. Watch-seconds move 6–15%.

The first version of this check — before I accounted for that — ordered
reverting **both** of the last two things shipped: the current video format
(views down 50%) and the background-video library (down 39%). Both "effects"
sit in the same few weeks and are almost certainly one channel-wide swing, not
two independent regressions. A guardrail that reverts the last two releases on
its first run is not a guardrail.

The check now measures that background movement and requires a drop to exceed
it. That is a refusal, in the same family as the two the rule already had
("too little data", "ages don't match") — I have not touched the rule's
threshold or its teeth.

## 2. The rule reverts on watch-seconds **or** views, and they disagree

The background-video library reads:

- **watch-seconds +22%** — clearly above its 11% noise limit
- **views −39%** — barely above its 38% noise limit

So the rule says revert, on a one-point margin, against a clear gain in the
metric the plan names as primary ("watch-seconds is primary, views is
distribution"). I have not acted on it: reverting that library would also mean
discarding clips you curated, which is your call either way. The tool prints
the disagreement rather than hiding it behind the one-word verdict.

Current verdicts: current format **keep** · background library **revert, with
this conflict** · newest release **no verdict yet** (it becomes judgeable
around 5 October, which happens to match the two-week bake rule).

## Recommendation

Change the rule's trigger to **watch-seconds only**, with views reported
alongside and never used to fire. Reasons: views at a fixed age are five times
noisier than watch-seconds here, the plan already ranks watch-seconds first
precisely because it cannot be gamed, and as written the rule would revert a
change that improved the primary metric by 22%.

Until you say otherwise the rule stands as written, and the background-video
library keeps its revert verdict on the record un-acted-on.

## Recommendation

Make watch-seconds the trigger and views a reported-only signal — but it is your rule, so it stays as written until you say otherwise.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*