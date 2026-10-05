---
title: Quarterly planning, Q4 2026: three draft bets for you to set
key: quarterly-planning-2026-q4
labels: needs-owner
raised_at: 2026-10-05T22:37:03+00:00
---

## Withdrawn: the alternating-tests idea

I tested the proposal against our own data before you spent time on it, and it failed. With nothing changed, uploads split by alternate days within the same weeks differ in watch time by 12%. Consecutive batches differ by 13%. So the noise comes from how few uploads each comparison has, not from the calendar. Alternating would not make our tests sharper, and it would make each one take longer.

What does make tests sharper is more uploads per comparison, which is bet 2's volume step. Please drop the method item from the session. The rest of this issue stands.

## Recommendation

Skip the alternating-tests item; nothing to decide there.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*