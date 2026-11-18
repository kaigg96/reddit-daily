# E5 · Where viewers leave an episode
Status: dropped: filter 11-18, the five retention points already show where viewers leave (steepest between 25% and 50%, 11-16 medians), #15 has its Where read set in advance, and the segments it would log belong to the Reddit show that ends 01-12
Function: Data (with Product management)
Deadline: none; most useful before E1 T9 reads the shows (2026-12-20)
Measure: average % viewed (the scorecard guardrail now BREACHED, 55.3 to 46.4). Done when every upload's segments are on record, joined to its retention points, and one command names the segment where viewers leave
Rule: it worked if, within four weeks of the record starting, one product change is chosen because of its output (a Decide citing it), or its output says plainly that no segment stands out beyond chance. Written before any segment is read.

## Why now

`report.py --scorecard` (2026-11-18): avg_view_pct is BREACHED, 55.3 to
46.4, and plays past the opening per 100 fell from 43.8 to 33.3, while views
rose. The 11-16 weekly review found "no logged field explains burial". We
collect retention points (`watch_ratio_*`, PRD §0) but not what was on
screen at each point. Friction group G25 (4 rows): "What an upload said
(narration, closing line) lives only in run logs". F257: "the upload log
keeps titles and closing lines but not the three answers". So each read of
"where do they leave" starts with digging through logs, and that dig is
coarse: #15's rule maps 25% to "the setup" and 50/75% to "the notes".

## The decision

At upload, write each segment's text and its start and end second (hook,
question, countdown, reveal, closing line) into a per-upload record.
`report.py` then maps the retention points onto those segments, median
across uploads of a show. Rejected: rebuilding the record afterwards from
run logs, which expire and need a login-free path each time (G25). Also
rejected: estimating timings from the MP4, which is slower and drifts once
screens follow the narration (E1 T7).

## Scorecard number it moves

Average % viewed, through the product changes it points to. It is a
diagnostic, never a trigger.

## Riskiest assumption and its cheapest test

That our retention points are fine enough to tell segments apart. On a
23-second video each 10% step is about 2.3s, and segments run 3–6s. The
cheapest test: take one recent upload whose run log is still readable and
place its segment times onto its `watch_ratio_*` row by hand. Half a shift,
no API calls. **Run already? No.** Not in `--dropped` or PRD §4, which has
only "Retention points leave out viewers who swipe away" (10-20). Those
viewers are read through engaged share.

## First slice that ships alone

The record, written by the upload itself, with a test and a dry run showing
it filled in. No analysis yet. One shift.

## Cost in shifts

About three: the record (1), the join and report command with tests (1),
the first read and its Decide or "nothing stands out" (1).

## Out of scope

Collecting new YouTube metrics. Reading a blind test's fields before their
due date (G29). Any Gemini call. Any change to `prev_post.txt` during
development.

## Assumptions

1. The record can go in new `upload_log.csv` columns written by the upload
   itself. If it needs its own file, the workflow must commit that file,
   which is an `escalate.py --patch` that applies after 3 days.
2. The weekly snapshot keeps the per-upload retention points for videos
   under 30 days old (PRD §0). Older videos do not need them.
3. Both shows' segment names can be the same five, so one command reads
   both arms.
