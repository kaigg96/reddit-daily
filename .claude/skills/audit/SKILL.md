---
name: audit
description: Deep audit of the reddit-digest agentic workflow itself — is the process producing value, are the rules still right, what external guidance should we adopt, and where is it bloating. A project-management task that comes due once about ten shifts of evidence have accumulated; check WORKLOG.md for when one last ran.
---

# Audit the workflow

**The workflow is a product, and this is its review.** The code has tests and
the channel has metrics; the process has neither unless a shift deliberately
looks. That gap is where agentic systems rot — they optimise what they build
and never ask whether the way they build it still makes sense.

This is the biggest task in the project-management lane, not a separate
rotation. It comes due once roughly ten shifts of evidence exist, because every
question below reads a *series* — one shift cannot tell you whether the process
is working. Findings go in `TECH_DEBT.md`.

**Changes to `CLAUDE.md` or any skill are proposals, and this is enforced, not
advised.** `.github/workflows/protect-process.yml` reverts a protected file
changed on `main` without approval and tells the owner. The path:

1. Make the change **on a branch** — branches are unrestricted.
2. `scripts/escalate.py` to raise it, with the reasoning and your recommendation.
3. The owner labels that issue `approved`.
4. Land it with `Approved-In: #N` in the commit message. CI checks the issue
   really exists and really carries the label — the trailer alone proves nothing.

A workflow that rewrites its own rules unobserved is the failure this prevents,
and prose was never going to stop it.

Hold it to the same standard as the channel: **evidence over hunches, record
what you rejected, and don't change direction because a shift has a new
opinion.** Process churn is as costly as code churn.

## The evidence to read first

- **`DECISIONS.md`** — every process decision and the assumptions under it.
- **`WORKLOG.md`, last ten entries** — what shifts actually did.
- **Closed and open escalation issues** — which decisions really needed a human.
- **`git log`** — what got reverted, re-done, or abandoned on a branch.
- `scripts/context_budget.py --session --allocation` — what a session spent,
  and planned vs actual per lane.

## Re-test the decisions

Walk `DECISIONS.md` and, for each assumption, ask **is this still true?** A
false assumption means the decision is due for re-litigation — not necessarily
reversal. Record the re-review inline with a date, *including* "still holds":
an unreviewed decision and a reviewed-and-confirmed one look identical
otherwise.

This is the file's reason to exist. D1 is there as the worked example — a
decision whose primary assumption became false within two hours and stood
unexamined until the owner happened to ask.

## What to ask

**Are slices being finished or filled?** `--allocation` shows planned vs
actual. Landing under plan is fine — slices are ceilings. *Every* lane under
plan on *every* shift means we are not finding valuable work, which is a
process finding. Consistently over means the allocation is wrong.

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

Run `venv/bin/python scripts/context_budget.py`. It reports three things:
words in the always-loaded and startup docs, and **open-item counts in the
append-only ones** — `WORKLOG.md`, `DECISIONS.md`, `TECH_DEBT.md`. The second
is the one that creeps, because those files cost nothing per session and so
nobody notices them growing.

Enforce closure. An open item resolves — fixed, promoted to `PRD.md` §0's
backlog, or deleted with reasoning. A superseded decision compresses to a line;
one confirmed stable across three audits graduates into the rules and leaves a
stub. **"Still open" is not a resolution**, and a list nobody can read is the
same as no list.

**`PRD.md` is the largest document and only §0 is budgeted**, so check it by
hand: cancelled and superseded requirements in §6, and retracted findings in
§4, should compress to a line plus a pointer to git history. Full text of a
decision we no longer act on is cost without benefit.

Look for **layering**: the same rule stated in two places will drift — that has
already happened here between memory and `PRD.md`. One rule, one home.

## Finish

Write up what you found, what you changed, what you proposed, and what you
deliberately left alone, in `TECH_DEBT.md`. **"The process is working" is a
valid finding** if the evidence says so — say it and stop, rather than
manufacturing a change to justify the audit.
