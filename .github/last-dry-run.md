# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render


- **Branch:** `legal/credit-reddit-users`
- **Commit:** `4e2d547`
- **When:** 2026-10-06T23:36:44Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 30.1 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37547106464)

What it picked:

```
Screen: dropped 1 comment(s) (unsafe_comments)
Selected post: How did that kid at your high school die?
Slate topics (rank order): dark-morbid|relationships-dating|other|dark-morbid|humor-absurd
Title style B: Do you remember how that kid from your high school died?
Today's top AskReddit post, asked by u/IM_HODLING: How did that kid at your high school die?
```

## Last request

- **Branch:** `product/house-vote-dormant`
- **When:** 2026-10-07T10:41:16Z
- **Outcome:** not rendered -- one automated render per 12 hours; the last was 2026-10-06T23:36:01Z
