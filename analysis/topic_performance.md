# Channel content-performance analysis (PRD R4.3)

Generated 2026-07-21 · 891 videos fetched, 877 analyzed (parsed + ≥7 days old) · age model: log-views slope 0.10

Performance metric: **age-adjusted residual** — how far a video's log-views sit above/below
the channel's own age trend. residual > 0 = overperformed for its age. Raw views are NOT
comparable across months and are shown only for scale.

## Topic performance

| Topic | n | median residual | median views | % overperforming |
|---|---|---|---|---|
| humor-absurd | 33 | +0.58 | 69 | 88% |
| dark-morbid | 59 | +0.57 | 69 | 73% |
| nostalgia | 29 | +0.57 | 70 | 86% |
| health-body | 43 | +0.40 | 60 | 65% |
| hypotheticals | 28 | +0.39 | 55 | 68% |
| politics-news | 56 | +0.32 | 54 | 61% |
| other | 355 | +0.27 | 48 | 67% |
| relationships-dating | 80 | +0.25 | 50 | 62% |
| money-work | 63 | +0.22 | 47 | 63% |
| life-advice | 95 | +0.22 | 47 | 67% |
| fame-celebrity | 25 | +0.16 | 42 | 64% |
| sex-adjacent | 11 | +0.01 | 38 | 64% |

## Distinctive terms (top quartile vs bottom quartile)

| In overperformers | In underperformers |
|---|---|
| more than | self |
| asking | deep |
| yourself | thighs |
| major | mad |
| sick | about women |
| means | land |
| party | model |
| realizing | automatically |
| silence | reasons |
| lights | late |
| imagine | rate like |
| played | looks |
| pick | credit card |
| walk | beast |
| ruin | jobs |

## Upload slot

| UTC hour | median residual |
|---|---|
| 00:00 | +0.55 |
| 01:00 | -0.04 |
| 02:00 | -0.01 |
| 03:00 | +0.30 |
| 04:00 | +0.31 |
| 05:00 | +0.02 |
| 06:00 | +0.63 |
| 12:00 | +0.42 |
| 13:00 | -0.01 |
| 14:00 | +0.06 |
| 15:00 | -0.66 |
| 16:00 | -0.18 |
| 17:00 | -0.47 |
| 18:00 | -2.35 |
| 19:00 | -3.73 |
| 20:00 | -2.35 |
| 22:00 | +0.07 |
| 23:00 | -3.05 |

## Caveats (read before acting)

- **Single snapshot.** Views are lifetime totals adjusted by a fitted age curve, not true
  views@7d. The weekly snapshotting in R4.2 will fix this going forward.
- **Correlation ≠ causation.** Topic buckets with few videos (⚠️) are noise-prone.
- **Suppression vs. interest is not separable** from this data — but both imply the same
  action for weak topics.
- **Upload-slot medians are era-confounded**: posting times changed over the channel's life,
  so slot differences partly encode channel age/maturity. Don't reschedule from this table.
- Nearly all analyzed videos are pre-v2 format; re-run after v2 accumulates data.
- Proposed `BLOCKED_TOPICS` candidates require owner approval before any gate ships (R4.4).