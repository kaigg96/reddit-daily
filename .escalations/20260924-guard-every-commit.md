---
title: Approve: make the process guard check every commit, not just the last
key: guard-every-commit
labels: needs-owner
raised_at: 2026-09-24T01:53:00+00:00
---

You asked for this fix on 2026-09-24. It changes the process guard itself,
which is a protected file, so it needs your label to land.

## What was wrong

The guard that stops shifts from changing their own rules only ever looked at
the **last commit** of each push. That failed both ways:

- **It could let an unapproved change through.** If a shift changed a skill and
  then made any other commit on top, the guard saw only the second commit.
- **It undid approved changes.** Work merged with GitHub's normal "merge
  commit" button was reverted even though you had approved it, because the
  merge commit itself carries no approval note. We have been working around
  that by using "Rebase and merge".

Two smaller holes in the same guard:

- A **new** rules file added without approval was left in place instead of
  being removed.
- A carefully named file could have run commands inside the guard's own clean-up
  step.

## What the fix does

Branch: `fix/guard-every-commit`

The guard now checks **every commit** in a push. Any commit that changes a
protected file must name an issue you have labelled `approved`. Merges are
judged only on what they change themselves, so approved work merged with a
merge commit passes, while a change slipped in during a merge is still
caught. The clean-up removes unapproved new files, and file names can no
longer be treated as commands.

## How it was checked

The guard's own code was run against 11 real scenarios, including both
failures above and a hostile file name. Pointed at the **old** guard, the same
tests fail on exactly the two main bugs — so they are testing the real
problem, not passing by accident.

One related gap, not fixed here: the automatic checks that run on every push
do not run the test suite. These tests run daily in the release check and in
working sessions, but they do not block a push. Making them do so would be a
separate change.

## What approving means

Label this issue `approved`. I then attach its number to the change and open
it for you to merge. This one is independent of the #27 dry-run change and
they can land in either order.

## Recommendation

Approve — closes a hole that let unapproved rule changes through, and stops approved changes being wrongly undone.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*