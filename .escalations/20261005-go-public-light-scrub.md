---
title: Approve: prepare the repo to go public, and four shifts a day
key: go-public-light-scrub
labels: needs-owner
raised_at: 2026-10-05T21:46:48+00:00
---

## What this is

The light-touch plan we agreed on 5 October, on branch `public/light-scrub`. It touches protected files (workflows, skills, `ORG.md`), so it needs your label.

## What changes

- **Unmerged code never holds the Polly keys.** Sample videos of a branch use the real Reddit post but silent narration. Only the main code, which production already runs, gets the keys. A test pins this.
- **Obvious links to the channel are removed.** The channel's name now comes from a secret, and a real upload refuses to start without it. The upload log line and the Monday digest no longer post YouTube links, and the docs say "the channel".
- **Four shifts a day** (03:17, 09:17, 15:17 and 21:17 UTC). The Actions-minutes guard stands down while the repo is public, and returns if it is ever private again.
- **A shift carries on with the queue after a review**, and a burst of pushes runs one guardrail check instead of one per push.

All 317 tests pass, every guardrail step passes locally, and a free sample video renders and plays.

## Before I land it, please

1. **Add the repository secret `CHANNEL_NAME`**, set to the channel's display name exactly as it appears today. Without it, the next real upload stops rather than publish a placeholder watermark.
2. **Consider raising the repository variable `SHIFT_WEEKLY_QUOTA_BUDGET`** (default 120). Four shifts a day at today's cost of about 4.3 units each is about 120 a week, so the guard would start skipping shifts late in the week. I suggest 200, then check your weekly usage after a few days.

## After it lands

Switch the repo to public (Settings, General, Danger zone). Optionally, under Actions settings, require approval for workflows from outside contributors.

## Recommendation

Approve after adding the CHANNEL_NAME secret. I land it once both are in place; then you switch the repo to public.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*