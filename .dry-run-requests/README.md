# Dry-run requests

Files here ask `.github/workflows/dry-run.yml` to render a branch. Don't write
them by hand — use `venv/bin/python scripts/dry_run.py request <branch>`, then
commit and push. The job renders the most recent request, clears the queue, and
writes the verdict to `.github/last-dry-run.md`.
