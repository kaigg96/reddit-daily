---
title: Approve: shifts refill their own work, so they stop ending early
key: ready-work-floor
labels: needs-owner
raised_at: 2026-09-25T02:19:03+00:00
---

You asked whether we'd found a durable fix for shifts ending early, or only
handed them one more problem. We hadn't: seeding a problem refills the queue
once. This is the fix at the source.

## What was wrong

- **The backlog couldn't tell ready work from blocked work.** Changes waiting
  on a sample video still counted as work to do.
- **Shifts only looked for new work when the feature list was empty**, and
  blocked items kept it from ever looking empty.
- **The alarm for unused time couldn't see it.** It compared percentages that
  always add up, so an 8-minute shift looked fully used.

This would have kept happening by design. One experiment runs at a time and
takes about two weeks to judge, so new features are usually waiting.

## The change

- **Every backlog item says whether it can be worked on now**, or what it is
  waiting on.
- **When fewer than 3 items are ready, a shift's first job is finding more.**
  Questions the channel's own data can answer are always available, with no
  sample video or spending needed.
- **A shift that stops early has to say what it considered and why it fell
  short.** It is never to pad.
- **The alarm now measures real minutes, and each report shows minutes used and
  ready work left.** If shifts keep stopping early, it tells you.

## Checked

- The ready-work count caught a formatting mistake of mine on its first run.
- Pointed at the real record of past shifts, the alarm flags the two short ones.
- 226 tests pass.

## What approving means

Label this `approved`. Everything is written and tested. The rules for shifts
are the part that needs your approval; once approved, it lands tonight if I'm
still here, otherwise the next shift lands it from branch
`feature/ready-work-floor`.

## Recommendation

Approve — this fixes why shifts end early, rather than giving them one more task.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*