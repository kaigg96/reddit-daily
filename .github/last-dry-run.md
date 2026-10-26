# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render


- **Branch:** `strategy/se-sample`
- **Commit:** `f597d0b`
- **When:** 2026-10-25T21:54:13Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 37.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40237322778)

Failed soft (the video still passed):

```
Slate topics (rank order): (not collected)
```

What it picked:

```
Selected post: How can I deal with a colleague who repeatedly asks for revisions?
Slate topics (rank order): (not collected)
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (4 words)
Commentary setup, as written: "Here we go again"
Commentary: dropped only the line(s) named above
Title style B, caps arm 0: Dealing with endless revisions from a colleague?
Commentary setup: (dropped)
Commentary reaction 1: Smart move
Commentary reaction 2: Nice framing
Commentary reaction 3: Adjust mindset
CTA: I'm raising my hand for 'budgeting extra time for refinements.' Which one gets your vote?
Commentary: our own words are 0.240 of the narration, 4 host line(s) shown
Assembled: 37.6s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top Workplace post, asked by u/Grain Train: How can I deal with a colleague who repeatedly asks for revisions?
```

## Last request

- **Branch:** `strategy/own-questions-sample`
- **When:** 2026-10-26T08:56:40Z
- **Outcome:** not rendered -- one automated render per 12 hours; the last was 2026-10-25T21:53:38Z
