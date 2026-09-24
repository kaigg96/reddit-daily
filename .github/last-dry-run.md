# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

_None yet._

## Last request

- **Branch:** `?`
- **When:** 2026-09-24T02:06:52Z
- **Outcome:** not rendered -- no valid request in the queue
