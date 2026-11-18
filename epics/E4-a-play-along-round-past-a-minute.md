# E4 · A play-along round that runs past a minute
Status: dropped: filter 11-18, cannot start before E1's arms are read in February, a release would read length rather than the round (PRD §4 10-07: v7's lead was mostly length), and its arithmetic fails: three 16.9 s episodes are ~50 s, not past a minute, at 1.5-2x the Polly characters
Function: Product management (with Monetization)
Deadline: none; it starts once E1 T9 has chosen the show (by 2026-12-20), and only if the play-along show is chosen or kept as an arm
Measure: median watch-seconds per upload at 7 days (the scorecard's success line), with engaged share beside it
Rule: keep the round if median watch-seconds rises beyond the detection limit `report.py --release` prints, at 7 days on at least 20 uploads, and engaged share does not fall beyond its printed chance gap; otherwise revert to the single question. Average % viewed is reported and never a trigger, because a longer video lowers it by construction. Views never trigger (#18).

## Why now

Watch time is falling: `report.py --trajectory` says FALLING, 12.0s to 10.5s
over six weeks, and `--scorecard` gives a verdict of WORSE. The one lever the
record says grows watch time is length: "Watch time grows with length up to
~31s; past that it is unmeasured" (PRD §4, 2026-10-05), and "a 60-second
format would need its own measured test on YouTube before any TikTok pilot".
TikTok's Creator Rewards is the nearest route on views (`--routes`: about 7x
short) and pays only for originals over a minute (PLAN §1). Today a
play-along episode asks one question and runs about as long as a reading.

## The decision

An episode becomes a round of three questions on one theme ("Prices in 1990:
ground beef, gas, a stamp"). It keeps each question's narration, countdown
and reveal, with a running score the viewer keeps in their head. Rejected:
stretching one question with a longer countdown, which adds dead time
rather than content. Also rejected: longer Reddit readings, because that show
ends on 12 January and more reading means more Polly.

## Scorecard number it moves

Median watch-seconds at 7 days. The round also meets the one-minute length
condition of the TikTok route, which E3 T4's second feed would need.

## Riskiest assumption and its cheapest test

That viewers keep watching past ~31s on a quiz, so watch-seconds rise
instead of the extra questions going unwatched. No upload has run past 31.5s
(PRD §4), so our data cannot answer it. The cheapest test is the release
itself: about 20 uploads read with `--release`. **Run already? No.** Not
in `backlog_status.py --dropped` or PRD §4 beyond the 31s line.

## First slice that ships alone

The round builder, switched off: a three-question episode renders as a free,
silent sample (`scripts/playalong_sample.py`). A test shows its narration
fits under `POLLY_CHAR_BUDGET` (5,000 characters, `src/config.py`) and its
screens follow the narration's timing. One shift. Nothing is uploaded.

## Cost in shifts

About four: the builder and sample (1), a fresh judge's viewing and the
release with its rule in the ledger (1), the bake's checks (1), the read (1).

## Out of scope

Posting to TikTok (E3 T4). Any rise in the Polly line or the per-run budget.
Changing the takes show's length. A round in more than one show at once
(one variable per release).

## Assumptions

1. Three questions' narration is no more characters than one of today's
   Reddit episodes, so the monthly Polly forecast ($0.78 of $3) does not
   rise. Check it against the mp3s and text in `assets/gen/` before building.
2. The play-along sources (E1 T6) supply three questions on one theme a day
   without repeats.
3. A Short can run up to three minutes, and a 60–75s one stays in the Shorts
   feed. Check YouTube's current help page before the release.
4. E3's comparison reads arms as bundles. If E1 T9 is still reading arms
   side by side, the round waits until that read is in, so it is not a
   second variable inside it.
