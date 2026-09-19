# Escalation queue

Files here become GitHub issues on push to `main`, which emails the owner
(they watch the repo). One file per decision.

**Don't write these by hand** — use the helper, which gets the frontmatter and
the dedupe key right:

```sh
venv/bin/python scripts/escalate.py \
    --title "Raise the Polly character budget?" \
    --key polly-budget-raise \
    --recommend "No — find out what is making the extra calls first" <<'EOF'
## What happened
A shift hit PollyBudgetExceeded during a routine render.

## Why this is yours
Raising the budget weakens a cost control (CLAUDE.md §1).
EOF
```

Then commit and push. [`.github/workflows/escalations.yml`](../.github/workflows/escalations.yml)
files the issue and deletes the file.

`--key` dedupes: re-raising the same key comments on the open issue rather than
opening a second one. Name it after the *decision*, not the day.

## What belongs here

Only what a shift genuinely may not decide (`CLAUDE.md` §3):

- Weakening a safety or cost control — the Polly budget, the `DRY_RUN` guard,
  secrets handling, the R4.6 screen's skip categories.
- Spending beyond the current ~$0.90/month Polly line.
- Deleting or rewriting production data, including historical backfills.
- Publishing anything outside the channel's normal upload.
- A proposed change to the shift process itself — it must not rewrite its own
  rules unobserved.

**Not** for status, findings or ideas. Those go in `WORKLOG.md`, `TECH_DEBT.md`
and `PRD.md` §0. An escalation asks a question; if there is no decision for the
owner to make, it does not belong here.

The issue history is also the record of *which* decisions kept needing a human
— the evidence for whether the autonomy boundary sits in the right place.
