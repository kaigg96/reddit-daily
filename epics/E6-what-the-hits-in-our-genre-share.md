# E6 · What the hits in our genre have in common
Status: proposed
Function: Market intelligence (with Product management)
Deadline: before E3 T2 sets Q1's bets (2026-12-20)
Measure: what exists when done: a dated table of comparable quiz and play-along Shorts channels' top videos against each channel's own median, and the hypotheses it hands Product (ORG.md: "hypotheses supplied that changed a decision")
Rule: it worked if at least one of its hypotheses becomes a pre-committed test in the owned show by 2027-02-28, or it records that none survived a fresh challenge. Written before any channel is read.

## Why now

E3 names the gap: "The paid channels in our genre have what we lack: a few
videos that reach hundreds of thousands. Q1 cannot be a march toward a bar.
It is a search for a format that reaches." Our own data cannot show what
makes a hit: "Nothing we log makes hits" (PRD §4, 2026-10-07). The only
market scan of comparable channels (2026-10-05) used "search-snippet figures,
approximate", and it compared channels, not their best videos. PLAN §1
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
