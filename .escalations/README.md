# Escalation queue

Files here become GitHub issues on push to `main`, which emails the owner
(they watch the repo). One file per message.

**Don't write these by hand** — use the helper, which gets the frontmatter and
the dedupe key right:

```sh
venv/bin/python scripts/escalate.py \
    --title "Turn on 2-step verification for the channel's Google account" \
    --key account-security-2step \
    --recommend "Yes — five minutes, and it is the channel's only protection" <<'EOF'
## What is needed
Only your login can do this.
EOF
```

Then commit and push. [`.github/workflows/escalations.yml`](../.github/workflows/escalations.yml)
files the issue and deletes the file.

`--key` dedupes: re-raising the same key comments on the open issue rather than
opening a second one. Name it after the *decision*, not the day.

## What belongs here

Since 2026-11-14 (D16) the owner is the last resort, so very little
(`CLAUDE.md` §4). Three kinds of message, and the helper's own help says how
each is raised:

- **A notice** (`--notice-days 7` or more): a one-way door that costs no
  money, such as deleting production data or published videos, or renaming
  the channel. It goes ahead on its date unless the owner objects.
- **A workflow change** (`--patch`): a shift cannot push workflow files. It
  applies itself after 3 days unless the owner objects, or waits for their
  label if it touches the money checks or a file holding paid or upload keys.
- **An ask** (neither flag): only what the owner's login alone can do.

**Never** for spending money: that is not asked for, it does not happen. And
**not** for a product, strategy or process decision, which is the shift's own
to make and record. Status, findings and ideas go in `WORKLOG.md`,
`TECH_DEBT.md` and `PRD.md` §0.

The issue history is also the record of *which* things kept needing a human
— the evidence for whether the autonomy boundary sits in the right place.
