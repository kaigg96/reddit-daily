---
title: Confirm: do escalation emails reach you?
key: escalation-path-smoke-test
labels: needs-owner
raised_at: 2026-09-19T22:15:19+00:00
---

## Why this exists

Shifts now run without you. When one hits a decision it may not make — weakening
a guardrail, spending money, rewriting production data, or changing the shift
process itself — it queues a file and this workflow turns it into an issue.

That whole mechanism is only as good as the last hop: **the email actually
reaching you.** An untested notification path is worse than no path, because
work proceeds assuming you were told.

## What to check

1. Did this arrive by email at kaigg@live.ca, or only on GitHub?
2. Is the title clear enough to triage from a phone?

## How it works

- `scripts/escalate.py` queues a file in `.escalations/`
- `.github/workflows/escalations.yml` files it as an issue, then deletes the file
- Uses the built-in `GITHUB_TOKEN` — no SMTP credentials stored anywhere
- Re-raising the same `--key` comments on the open issue instead of duplicating

## Recommendation

If you got an email for this issue, the path works — close it and nothing further is needed. If you only saw it on GitHub, check Settings → Notifications, because a shift that escalates into silence is worse than one that never escalates.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*