# The viewer bar

How a video is judged before it ships, by someone who cannot watch it. Written
2026-11-15 for E1 T7 and every format change after it (D14: judged as a
viewer; D16: judged by shifts). A shift never sees a video play. What it has
is the script (every word narrated or shown, with timings), the frames
(`sample-frames`), and the numbers after the fact. This bar is written so a
fresh agent given only the script and frames reaches the same verdict a
careful viewer would, most of the time.

## Who the viewer is

Someone who has never seen the channel, mid-scroll, sound on, who gives a
video about **two seconds** before deciding and will leave the moment they
stop caring. They did not choose this video. Nothing is owed to it.

## The five checks, in the order the viewer meets them

Each check is answered **yes or no** with the line or frame that decides it.
"Mostly" is a no. A reviewer who cannot point at the evidence writes "cannot
tell from the script", which is also a no for shipping.

1. **The first two seconds give a reason to stay.** By the end of the first
   spoken sentence, or the first frame's text, the viewer knows what is being
   asked of them and wants the answer. Test: cover everything after the first
   sentence. Does a stranger have a question in their head? A title that
   promises something the first sentence does not deliver fails here.
2. **There is nothing to do but wait for the end.** The video has one line of
   tension that resolves at the end, not before. Test: find the moment the
   viewer has what they came for. If it is before the last third, everything
   after is dead air, however good. A reading of three answers fails this
   when the best answer comes first.
3. **Every second is followable at speaking pace.** Nothing on screen has to
   be read while something different is being said. Text shown stays long
   enough to read twice (about 1.2 s for three words, from the owner's
   watching, 2026-10-19). No number, name or clause needs a second pass.
4. **The reveal is worth the wait.** The end lands something the viewer could
   not have guessed and now cannot unknow, or confirms a guess they made and
   were invested in. Test: would a viewer say the reveal to someone else? If
   the end is a formula ("which one gets your vote?") with nothing before it
   that made them care, it fails.
5. **It is ours, and it is true.** Nothing in it is a plain reading of
   someone else's text; the commentary, the question or the structure is the
   show's own (PLAN §4, YouTube's reused-content rule). Every stated fact
   traces to its source record, copied by code, never by a model, and the
   credit the source asks for is in the description.

## What the bar is not

- Not a style guide. Voice, music and colour are judged by their own tests.
- Not a predictor. A video can pass all five and get 40 views; the feed
  decides reach. The bar is the floor below which no video goes out.
- Not a score. Five yeses ships; any no is fixed or the video is dropped. A
  reviewer tempted to average is reviewing the wrong thing.

## How to apply it

- The reviewer is a fresh agent that did not write the episode or its
  prompt, given the script, the frames, this file, and nothing else: not the
  author's notes, not the show's design (the design says what was intended;
  the bar asks what a stranger gets).
- One verdict per check with its evidence, then the single change that would
  turn the first no into a yes. Findings are fixed or recorded (`CLAUDE.md`
  §7); a video that fails a check twice after fixes is a design problem, not
  a draft problem, and goes back to the epic.
- For a new show, the first **three** samples are judged this way before any
  upload, and the verdicts are kept with the epic's ticket as evidence. For a
  change inside a shipped show, one sample.
- The numbers afterwards are the bar's own test: a show that passes and still
  loses most viewers in the opening (`engaged_share` low, `watch_ratio_25`
  low) means check 1 or 2 is being read wrong. The weekly review notes it,
  and this file changes on that evidence, not on taste.
