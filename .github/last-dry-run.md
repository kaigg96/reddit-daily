# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/host-three-answers`
- **Commit:** `2e26595`
- **When:** 2026-10-17T14:27:52Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 33.0 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/39040582950)

Failed soft (the video still passed):

```
Selected post: What animals have humans made a significant, but failed, attempt at domesticating?
tags:        ['NoStupidQuestions', 'Shorts', 'Reddit', 'Top NoStupidQuestions Post', 'Trending NoStupidQuestions', 'failed domestications', 'animals humans tried to domesticate', 'domesticated foxes experiment', 'squirrels as pets history', 'did cats domesticate us', 'unsuccessful animal breeding', 'colonial america pets', 'why foxes cant be pets', 'wild animal attempts', 'reddit failed domestications']
Today's top NoStupidQuestions post, asked by u/-chibcha-: What animals have humans made a significant, but failed, attempt at domesticating?
```

What it picked:

```
Selected post: What animals have humans made a significant, but failed, attempt at domesticating?
Slate topics (rank order): other|relationships-dating|dark-morbid|politics-news|humor-absurd
Title style C, caps arm 1: 3 Animals We TRIED To Tame
Commentary setup: Nature always finds a way to ruin human plans.
Commentary reaction 1: Accidental dogs do not count as a successful harvest.
Commentary reaction 2: Rabies cabinets sound like a terrible colonial trend.
Commentary reaction 3: Truth has rarely been spoken so lazily.
CTA: I raise my hand for cats domesticating us because it is too true. Which gets your vote?
Commentary: our own words are 0.434 of the narration, 5 host line(s) shown
Assembled: 33.0s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/-chibcha-: What animals have humans made a significant, but failed, attempt at domesticating?
```

## Last request

- **Branch:** `product/host-three-answers`
- **When:** 2026-10-17T14:27:52Z
- **Outcome:** rendered -- see above
