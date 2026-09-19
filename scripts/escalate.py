#!/usr/bin/env python3
"""Raise something to the owner by queueing a GitHub issue.

Shifts run without the owner. When one hits a decision that is genuinely not
its to make — weakening a guardrail, spending money, rewriting production data,
or a proposed change to the shift process itself — it writes an escalation
here. The `escalations` workflow turns each file into a GitHub issue on push,
and GitHub emails the owner because they watch the repo. No new secrets: the
workflow uses the built-in GITHUB_TOKEN.

Issues are the right medium rather than a bare email: they persist, they can be
discussed and closed, and they accumulate a record of which decisions actually
needed a human — which is the data that tells us whether the autonomy boundary
is drawn in the right place.

    venv/bin/python scripts/escalate.py \\
        --title "Raise the Polly character budget?" \\
        --key polly-budget-raise \\
        --labels needs-owner,guardrail \\
        --recommend "No — investigate the call count first" <<'EOF'
    ## What happened
    ...
    EOF

`--key` is a stable dedupe handle: re-running with the same key comments on the
open issue instead of opening a second one. Use one that describes the
*decision*, not the day it came up.
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".escalations"


def slugify(value):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")[:60]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True, help="Decision-shaped, e.g. 'Raise X?'")
    ap.add_argument("--key", help="Stable dedupe handle (default: slug of title)")
    ap.add_argument("--labels", default="needs-owner",
                    help="Comma-separated (default: needs-owner)")
    ap.add_argument("--recommend", help="Your recommendation — always give one")
    ap.add_argument("--body-file", help="Read body from a file instead of stdin")
    args = ap.parse_args()

    body = (pathlib.Path(args.body_file).read_text() if args.body_file
            else sys.stdin.read()).strip()
    if not body:
        sys.exit("escalate: empty body — say what you need and why")

    key = slugify(args.key or args.title)
    now = datetime.datetime.now(datetime.timezone.utc)

    parts = [
        "---",
        f"title: {args.title}",
        f"key: {key}",
        f"labels: {args.labels}",
        f"raised_at: {now.isoformat(timespec='seconds')}",
        "---",
        "",
        body,
        "",
    ]
    if args.recommend:
        parts += ["## Recommendation", "", args.recommend, ""]
    parts += [
        "---",
        "",
        "*Raised automatically by a `/shift` run — it could not make this call "
        "itself. Close this issue once decided; if the decision changes a "
        "standing rule, it belongs in `CLAUDE.md` too.*",
    ]

    QUEUE.mkdir(exist_ok=True)
    path = QUEUE / f"{now:%Y%m%d}-{key}.md"
    path.write_text("\n".join(parts))
    print(f"queued {path.relative_to(ROOT)}")
    print("commit and push it — the escalations workflow files the issue")


if __name__ == "__main__":
    main()
