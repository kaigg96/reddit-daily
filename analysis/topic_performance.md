# Channel content-performance analysis (PRD R4.3)

Generated 2026-07-20 · 869 videos fetched, 857 analyzed (parsed + ≥7 days old) · age model: log-views slope 0.13

Performance metric: **age-adjusted residual** — how far a video's log-views sit above/below
the channel's own age trend. residual > 0 = overperformed for its age. Raw views are NOT
comparable across months and are shown only for scale.

## Topic performance

| Topic | n | median residual | median views | % overperforming |
|---|---|---|---|---|
| nostalgia | 24 | +0.57 | 75 | 83% |
| dark-morbid | 48 | +0.50 | 70 | 73% |
| humor-absurd | 30 | +0.50 | 68 | 83% |
| other | 410 | +0.26 | 51 | 69% |
| hypotheticals | 23 | +0.25 | 55 | 65% |
| relationships-dating | 69 | +0.22 | 51 | 62% |
| politics-news | 49 | +0.20 | 54 | 55% |
| money-work | 54 | +0.18 | 48 | 61% |
| health-body | 35 | +0.15 | 52 | 60% |
| fame-celebrity | 22 | +0.13 | 42 | 59% |
| life-advice | 85 | +0.12 | 47 | 59% |
| sex-adjacent ⚠️ small n | 8 | -0.07 | 38 | 38% |

## Distinctive terms (top quartile vs bottom quartile)

| In overperformers | In underperformers |
|---|---|
| yourself | interest |
| means | deep |
| sick | reasons |
| silence | reddit what's |
| ruin | looks |
| major | running |
| realizing | automatically |
| lights | jobs |
| stuff | celebrity |
| dating | don't want |
| pick | being able |
| played | career |
| imagine | youtube |
| written | letting |
| military | admit wrong |

## Upload slot

| UTC hour | median residual |
|---|---|
| 00:00 | +0.46 |
| 01:00 | -0.00 |
| 02:00 | -0.04 |
| 03:00 | +0.22 |
| 04:00 | +0.27 |
| 05:00 | -0.05 |
| 06:00 | +0.52 |
| 12:00 | +0.34 |
| 13:00 | -0.02 |
| 14:00 | +0.04 |
| 15:00 | -0.68 |
| 16:00 | -0.04 |
| 17:00 | -0.49 |
| 18:00 | -1.34 |
| 19:00 | -0.11 |
| 20:00 | -1.55 |
| 22:00 | -0.02 |
| 23:00 | -2.75 |

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