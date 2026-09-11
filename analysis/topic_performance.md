# Channel content-performance analysis (PRD R4.3)

Generated 2026-09-11 · 993 videos fetched, 979 analyzed (parsed + ≥7 days old) · age model: log-views slope -0.24

Performance metric: **age-adjusted residual** — how far a video's log-views sit above/below
the channel's own age trend. residual > 0 = overperformed for its age. Raw views are NOT
comparable across months and are shown only for scale.

## Topic performance

| Topic | n | median residual | median views | % overperforming |
|---|---|---|---|---|
| nostalgia | 38 | +0.62 | 75.0 | 82% |
| dark-morbid | 71 | +0.60 | 69 | 66% |
| humor-absurd | 38 | +0.58 | 72.0 | 74% |
| hypotheticals | 33 | +0.43 | 55 | 79% |
| relationships-dating | 96 | +0.35 | 54.0 | 59% |
| politics-news | 74 | +0.33 | 54.0 | 64% |
| health-body | 53 | +0.32 | 53 | 62% |
| money-work | 90 | +0.18 | 49.5 | 60% |
| other | 153 | +0.18 | 58 | 60% |
| fame-celebrity | 36 | +0.14 | 45.5 | 56% |
| life-advice | 121 | +0.11 | 47 | 55% |
| sex-adjacent | 13 | -0.30 | 37 | 31% |

## Does the topic prior survive the format change? (R4.4 gate)

The table above pools eras. R4.4 would seed a ranker from these priors, but they
were measured almost entirely on pre-overhaul v1 content, and v1->v4 moved median
views ~6x (PRD §4 Review 2). Below, residuals are refit **within** each era, so the
era's own level is removed and only the topic ordering is compared.

| Topic | v1 n | v1 residual | current n | current residual |
|---|---|---|---|---|
| nostalgia | 32 | +0.61 | 6 | +0.89 |
| humor-absurd ⚠️ | 35 | +0.59 | 3 | +0.47 |
| dark-morbid | 64 | +0.54 | 7 | +0.45 |
| hypotheticals | 33 | +0.38 | — | — |
| relationships-dating | 89 | +0.30 | 7 | +0.11 |
| politics-news | 68 | +0.29 | 6 | +0.42 |
| other | 130 | +0.29 | 23 | +0.73 |
| health-body ⚠️ | 49 | +0.28 | 4 | -0.01 |
| money-work | 72 | +0.24 | 18 | -0.19 |
| life-advice | 107 | +0.19 | 14 | -0.89 |
| fame-celebrity | 29 | +0.10 | 7 | +0.06 |
| sex-adjacent ⚠️ | 12 | +0.02 | 1 | -4.88 |

**Spearman rho = +0.79** across 10 shared buckets (buckets with n<3 in either era excluded): the prior TRANSFERS — the ranker may seed from the v1 table.

Read the rho, not the individual current-era medians — per-bucket n is small,
but the ordering across ~10 buckets is far more robust than any one median.


## Distinctive terms (top quartile vs bottom quartile)

| In overperformers | In underperformers |
|---|---|
| asking | reddit what's |
| died | jobs |
| means | thighs |
| ruin | minutes |
| imagine | rate like |
| silence | about women |
| more than | divorce |
| telling | myself |
| stuff | related |
| lights | deep |
| bring | cleaning |
| walk | mad |
| stage | land |
| stole | future |
| teeth | model |

## Upload slot

| UTC hour | median residual |
|---|---|
| 00:00 | +0.64 |
| 01:00 | -0.27 |
| 02:00 | -0.29 |
| 03:00 | +0.83 |
| 04:00 | +0.41 |
| 05:00 | +0.15 |
| 06:00 | +0.83 |
| 07:00 | -3.73 |
| 09:00 | +0.37 |
| 11:00 | -0.70 |
| 12:00 | +0.44 |
| 13:00 | -0.18 |
| 14:00 | -0.24 |
| 15:00 | -0.22 |
| 16:00 | -0.08 |
| 17:00 | -0.70 |
| 18:00 | -1.61 |
| 19:00 | -2.98 |
| 20:00 | -2.15 |
| 21:00 | -1.41 |
| 22:00 | +0.15 |
| 23:00 | -2.83 |

## Caveats (read before acting)

- **Single snapshot.** Views are lifetime totals adjusted by a fitted age curve, not true
  views@7d. The weekly snapshotting in R4.2 will fix this going forward.
- **Correlation ≠ causation.** Topic buckets with few videos (⚠️) are noise-prone.
- **Suppression vs. interest is not separable** from this data — but both imply the same
  action for weak topics.
- **Upload-slot medians are era-confounded**: posting times changed over the channel's life,
  so slot differences partly encode channel age/maturity. Don't reschedule from this table.
- The pooled topic table is still dominated by pre-v2 videos; for anything that
  drives selection, read the era-comparison section rather than the pooled table.
- Proposed `BLOCKED_TOPICS` candidates require owner approval before any gate ships (R4.4).