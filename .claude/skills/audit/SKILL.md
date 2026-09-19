---
name: audit
description: Deep audit of the reddit-digest agentic workflow itself — is the process producing value, are the rules still right, what external guidance should we adopt, and where is it bloating. Run roughly every tenth shift, or when WORKLOG.md shows none recently.
---

# Audit the workflow

**The workflow is a product, and this is its review.** The code has tests and
the channel has metrics; the process has neither unless a shift deliberately
looks. That gap is where agentic systems rot — they optimise what they build
and never ask whether the way they build it still makes sense.

Run every ~10th shift. Findings go in `TECH_DEBT.md`. Changes to `/shift`,
`/pickup` or `CLAUDE.md` are **proposals** — escalate them with
`scripts/escalate.py` rather than self-applying. A workflow that rewrites its
own rules unobserved is the failure this exists to prevent.

Hold it to the same standard as the channel: **evidence over hunches, record
what you rejected, and don't change direction because a shift has a new
opinion.** Process churn is as costly as code churn.

## The evidence to read first

- **`WORKLOG.md`, last ten entries** — what shifts actually did.
- **Closed and open escalation issues** — which decisions really needed a human.
- **`git log`** — what got reverted, re-done, or abandoned on a branch.
- **`scripts/context_budget.py --session`** — what a session spends and on what.

## What to ask

**Is it producing value?** Which of the last ten shifts shipped something that
mattered, and which produced churn? If a shift's output was a refactor nobody
needed or a doc nobody reads, that is a process failure, not a one-off — the
value bar (`/shift` §7) is not working.

**Are we working on the right things?** Is the triage order still right, or is
something important always losing? Is a lane never chosen — and is that correct
(nothing to do there) or a bug (the trigger never fires)?

**Are the gates real or theatre?** Have the merge gates ever *caught* anything?
A gate that has never failed is either protecting well or not testing anything;
the git history tells you which. Equally: has anything reached `main` that the
gates should have stopped?

**Is the authorization boundary right?** Escalations are the data. Too many on
trivia means the boundary is drawn too tight. None at all, over many shifts,
probably means shifts are deciding things they shouldn't.

**Does the handover work?** Could a cold session resume from `WORKLOG.md` and
`PRD.md` §0 alone, or did recent shifts re-derive state that should have been
written down? Re-derivation is the symptom; a thin handover is the cause.

**Are the budgets calibrated?** Context ceilings, the usage reserve, the Gemini
allowance — has any of them blocked useful work, or failed to stop waste?

**Are the rules being followed?** A rule quietly ignored across several shifts
is worse than no rule: it is noise that makes the others easier to ignore.
Either enforce it in code or delete it.

## Then look outward

Re-read [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
and the [skills](https://code.claude.com/docs/en/skills) docs — they change.
Look for community practice worth stealing. For each candidate, decide and
**record the decision either way**, so the next audit doesn't re-litigate it.

Adopted so far: the *"would removing this cause a mistake?"* pruning test;
`CLAUDE.md` for broadly-applicable rules only, with specifics in skills;
hooks and tests in preference to advisory prose.

Not yet tried, and worth a look: `/doctor` for automated `CLAUDE.md` cuts;
subagents to keep exploration out of the main context; `/clear` discipline
between unrelated tasks within a shift.

## Prune

Run `venv/bin/python scripts/context_budget.py`. Re-read `CLAUDE.md` line by
line against the pruning test. Look for **layering**: the same rule stated in
two places will drift — that has already happened here between memory and
`PRD.md`. One rule, one home, pointers everywhere else.

## Finish

Write up what you found, what you changed, what you proposed, and what you
deliberately left alone, in `TECH_DEBT.md`. **"The process is working" is a
valid finding** if the evidence says so — say it and stop, rather than
manufacturing a change to justify the audit.
