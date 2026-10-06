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
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".escalations"

# A shift cannot push workflow files. With --patch it attaches the exact change
# instead, and .github/workflows/apply-approved.yml applies it once the owner
# labels the issue `approved`. These must match that workflow exactly.
PATCH_MARKER = "<!-- apply-patch -->"
ENFORCERS = (".github/workflows/protect-process.yml", ".github/workflows/apply-approved.yml")
MAX_PATCH = 30000


def validate_patch(text, repo=ROOT):
    """(inner text, sha256) of a patch auto-apply will accept, or exit saying why."""
    inner = text.rstrip("\n")
    if not inner.strip():
        sys.exit("escalate: the patch is empty")
    if len(inner) > MAX_PATCH:
        sys.exit(f"escalate: the patch is over {MAX_PATCH} characters -- split it")
    paths = set(re.findall(r"^diff --git a/(\S+) b/(\S+)", inner, re.M))
    paths = {p for pair in paths for p in pair}
    if not paths:
        sys.exit("escalate: not a git patch -- make it with `git diff -- .github/workflows/`")
    bad = sorted(p for p in paths if not p.startswith(".github/workflows/") or p in ENFORCERS)
    if bad:
        sys.exit("escalate: --patch is for workflow files only, and never "
                 f"{' or '.join(ENFORCERS)}; this touches {', '.join(bad)}")
    # Against the index, so a shift that still has the edit in its working tree
    # is not told the change "already exists".
    check = subprocess.run(["git", "apply", "--check", "--cached", "-"], input=inner + "\n",
                           cwd=repo, capture_output=True, text=True)
    if check.returncode != 0:
        sys.exit("escalate: the patch does not apply to the current workflow files: "
                 + check.stderr.strip())
    return inner, hashlib.sha256((inner + "\n").encode()).hexdigest()


def patch_section(inner, sha):
    return ["## The exact change", "",
            "Applied automatically, exactly as shown, when you label this `approved`.", "",
            PATCH_MARKER, "`````diff", inner, "`````", f"patch-sha256: {sha}", ""]


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
    ap.add_argument("--patch", help="A workflow change to apply once the owner "
                                    "approves (git diff output; workflow files only)")
    args = ap.parse_args()
    patch = validate_patch(pathlib.Path(args.patch).read_text()) if args.patch else None

    body = (pathlib.Path(args.body_file).read_text() if args.body_file
            else sys.stdin.read()).strip()
    if not body:
        sys.exit("escalate: empty body — say what you need and why")

    key = slugify(args.key or args.title)
    if patch:
        # One issue per distinct change: re-raising the same key would land as
        # a comment, and auto-apply only ever reads the issue body.
        key = f"{key[:51]}-{patch[1][:8]}"
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
    if patch:
        parts += patch_section(*patch)
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
    # One file per message, even for the same key on the same day: a day-only
    # name let a second comment overwrite an unfiled first one, and collide
    # with the filer's deletion of a filed one (a modify/delete rebase conflict
    # whose wrong resolution drops the message, 2026-10-06). The filer reads
    # the key from the front matter, so the name carries no meaning.
    path = QUEUE / f"{now:%Y%m%d-%H%M%S%f}-{key}.md"
    path.write_text("\n".join(parts))
    print(f"queued {path.relative_to(ROOT)}")
    print("commit and push it — the escalations workflow files the issue")
    if patch:
        print("do NOT commit the workflow edit itself (it cannot be pushed): "
              "`git checkout -- .github/workflows/` to drop it")


if __name__ == "__main__":
    main()
