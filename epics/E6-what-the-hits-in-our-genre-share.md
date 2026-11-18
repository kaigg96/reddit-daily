# E6 · What the hits in our genre have in common
Status: approved (filter 11-18, the one of five; waits for an active slot, at most two)
Function: Market intelligence (with Product management)
Deadline: before E3 T2 sets Q1's bets (2026-12-20)
Measure: what exists when done: a dated table of comparable quiz and play-along Shorts channels' top videos against each channel's own median, and the hypotheses it hands Product (ORG.md: "hypotheses supplied that changed a decision")
Rule: it worked if at least one of its hypotheses enters an arm's design at E3 T2 by 2026-12-20, or the record says none survived a fresh challenge. E3 forbids a per-lever read in Q1, so no hypothesis is tested on its own. Written before any channel is read (amended by the filter, 11-18).

## Why now

E3 names the gap: "The paid channels in our genre have what we lack: a few
videos that reach hundreds of thousands. Q1 cannot be a march toward a bar.
It is a search for a format that reaches." Our own data cannot show what
makes a hit: "Nothing we log makes hits" (PRD §4, 2026-10-07). Three scans
of comparable channels ran (10-05 on search-snippet figures, 10-18 on about
185 Reddit channels, 10-31 on 15 quiz channels, 6 of them paid), and none
compared a channel's top videos with its own median. PLAN §1
rates Market intelligence "Thin". `--routes`: the 500 tier is about 209x
short on engaged views, so the tail is the only way there.

## The decision

Study the tail, not the average. For each of 5–8 channels running a
question or play-along Short, compare their top ten videos with that
channel's median: length, the number of questions, the topic, the title's
shape, the upload date. From that, write at most three hypotheses the owned
show can test. Rejected: copying a winning channel's format, which YouTube's
originality and template rules penalise (PLAN §4). Also rejected: a paid
analytics tool (money).

## Scorecard number it moves

None directly. It chooses which test moves engaged views per upload in the
owned show (E3's measure).

## Riskiest assumption and its cheapest test

That per-video public figures (views, length, date) for other channels'
Shorts can be read with no login, no paid tool and no Gemini. The cheapest
test: one fetch of one channel's public pages or feed with curl and a
browser user agent. G17 says outside sites refuse the fetch tool but accept
that. Ten minutes. **Run already? No.** The 10-05 scan read search snippets,
not per-video figures. Nothing similar is in `--dropped`.

## First slice that ships alone

The table for five channels, read by hand, in PRD §4 as a dated finding with
its sources. One shift.

## Cost in shifts

About two: the table (1), the hypotheses with a fresh agent arguing against
each (1).

## Out of scope

Reuploading, quoting or clipping anyone's video. Contacting creators. Any
model API to classify videos (about 50–80 rows, done by hand). Watching
video content, which a shift cannot do: only what pages state is used.

## Assumptions

1. Channel feeds list only recent uploads, so a channel's older hits may
   need its public video list instead. The test above checks which works.
2. Five to eight comparable channels exist in English. The 10-05 and 10-31
   findings name candidates.
3. View counts on public pages are rounded. Comparing each channel's top
   videos with its own median stays valid at that precision.

## The filter (2026-11-18)

Approved, the only one of five (E4, E5, E7 and E8 cut). First both ways in
the opposite-order ranking: the only proposal aimed at the reach gap E3
names (`--routes`: the 500 tier is ~209x short), it feeds a decision made
either way (E3 T2, 12-20), it costs about two shifts with no Gemini, Polly or
owner, and it is reversible. Start from the 10-31 list of paid quiz channels.
Its riskiest assumption is half-tested: the 10-18 and 10-31 scans read
channel pages without a login. What remains is whether video IDs and view
counts are on the page: one curl of one paid channel's `/shorts` page with a
browser user agent (G17), then one video page for length and date.
