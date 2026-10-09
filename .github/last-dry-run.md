# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/screen-fallback-model`
- **Commit:** `d9c1e3e`
- **When:** 2026-10-09T17:38:14Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 30.4 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37967266997)

What it picked:

```
Selected post: Arab and Middle Eastern dudes in the U.S. - who are you talking to all the time?
Slate topics (rank order): humor-absurd|hypotheticals|politics-news|sex-adjacent
Title style B: Who are you talking to on the phone all day?
Today's top NoStupidQuestions post, asked by u/GrizzleTusk: Arab and Middle Eastern dudes in the U.S. - who are you talking to all the time?
```

## Last request

- **Branch:** `reliability/screen-fallback-model`
- **When:** 2026-10-09T17:38:14Z
- **Outcome:** rendered -- see above
