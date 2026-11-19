#!/usr/bin/env python3
"""Tell the owner something by queueing a GitHub issue.

Shifts run without the owner, and since D16 (2026-11-14) the owner is the last
resort: a shift decides product, strategy and its own process. Three things
still go through here. The `escalations` workflow turns each file into a GitHub
issue on push, and GitHub emails the owner because they watch the repo.

1. **A notice** (`--notice-days N`, at least 7): a one-way door that costs no
   money, such as deleting production data or old videos, or renaming the
   channel. It says what happens and on which date. Go ahead on that date
   unless the owner replied, closed the issue or labelled it `objection`
   (`escalations.py notices`).
2. **A workflow change** (`--patch`): a shift cannot push workflow files. The
   change applies itself after 3 days of notice with no objection, or at once
   on the owner's `approved` label. A change to the money checks, or to a file
   holding a key a shift does not hold, waits for the label.
3. **An ask** (neither flag): only when nothing can move without the owner,
   because it needs their login or their accounts. Spending money is never an
   ask: it does not happen (`CLAUDE.md` §1, §4).

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
import importlib.util
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".escalations"

# A shift cannot push workflow files. With --patch it attaches the exact change
# instead, and .github/workflows/apply-approved.yml applies it: after
# NOTICE_DAYS with no objection, or at once on the owner's `approved` label.
# What a notice may do is written once, in notice_check.py, which that job
# runs; this imports the same rules to word the issue.
PATCH_MARKER = "<!-- apply-patch -->"
MAX_PATCH = 30000


def checker():
    """The notice rules, from the one file that holds them."""
    path = ROOT / ".github" / "workflows" / "notice_check.py"
    spec = importlib.util.spec_from_file_location("notice_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_CHECK = checker()
ENFORCERS = _CHECK.LOCKED
NOTICE_DAYS = _CHECK.NOTICE_DAYS
MONEY_CHECKS = _CHECK.MONEY_CHECKS
SHIFT_HOLDS = set(_CHECK.SHIFT_HOLDS)

# A one-way door that costs no money gets a dated notice, never a silent act.
MIN_NOTICE_DAYS = 7
NOTICE_DATE = "<!-- notice-date: {} -->"      # read by escalations.py notices
OBJECT = "reply here, close this issue or label it `objection`"


def label_only(inner, repo=ROOT):
    """Why this change waits for the owner's label instead of applying itself
    after notice, or None. A forecast for the issue's wording, from the same
    rules (notice_check.py) on each file's content before the change and on
    the lines the change adds; the job that applies it decides, on what git
    stages."""
    why = []
    for section in re.split(r"(?m)^(?=diff --git )", inner):
        m = re.match(r"diff --git a/(\S+) b/(\S+)", section)
        if not m:
            continue
        for p in sorted({m.group(1), m.group(2)}):
            if p in MONEY_CHECKS:
                why.append(f"`{p}` is the money checks")
                continue
            if p in ENFORCERS:
                why.append(f"`{p}` never changes this way")
                continue
            before = subprocess.run(["git", "show", f"HEAD:{p}"], cwd=repo,
                                    capture_output=True, text=True).stdout
            added = "\n".join(l[1:] for l in section.splitlines()
                              if l.startswith("+") and not l.startswith("+++"))
            why += (_CHECK.reasons(before, p) if before else [])
            why += _CHECK.reasons(added, p, raw_only=True)
    return "; ".join(dict.fromkeys(why)) or None


def day(date):
    return f"{date.day} {date:%B %Y}"


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


def patch_section(inner, sha,
                  how="Applied automatically, exactly as shown, when you label this `approved`."):
    return ["## The exact change", "", how, "",
            PATCH_MARKER, "`````diff", inner, "`````", f"patch-sha256: {sha}", ""]


def slugify(value):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")[:60]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True, help="Decision-shaped, e.g. 'Raise X?'")
    ap.add_argument("--key", help="Stable dedupe handle (default: slug of title)")
    ap.add_argument("--labels",
                    help="Comma-separated (default: notice for a notice, else needs-owner)")
    ap.add_argument("--notice-days", type=int,
                    help=f"A notice, not an ask: it goes ahead after this many days "
                         f"(at least {MIN_NOTICE_DAYS}) unless the owner objects")
    ap.add_argument("--recommend", help="Your recommendation — always give one")
    ap.add_argument("--body-file", help="Read body from a file instead of stdin")
    ap.add_argument("--patch", help="A workflow change to apply after notice, or on the "
                                    "owner's label (git diff output; workflow files only)")
    args = ap.parse_args()
    patch = validate_patch(pathlib.Path(args.patch).read_text(), repo=ROOT) if args.patch else None
    if args.notice_days is not None and patch:
        sys.exit("escalate: a --patch sets its own notice; drop --notice-days")
    if args.notice_days is not None and args.notice_days < MIN_NOTICE_DAYS:
        sys.exit(f"escalate: a notice runs at least {MIN_NOTICE_DAYS} days")

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

    # What kind of message this is decides its label, its first lines and its
    # last: a notice must never read as a question the owner has to answer.
    waits = label_only(patch[0], repo=ROOT) if patch else None
    notice = (patch and not waits) or args.notice_days is not None
    lead = []
    if args.notice_days is not None:
        due = now + datetime.timedelta(days=args.notice_days)
        lead = [NOTICE_DATE.format(due.date().isoformat()), "",
                f"**A notice, not a question.** This goes ahead on or after **{day(due)}** "
                f"unless you {OBJECT}. Nothing is needed from you otherwise.", ""]
    if patch and not waits:
        due = now + datetime.timedelta(days=NOTICE_DAYS)
        how = (f"**A notice, not a question.** This applies itself, exactly as shown, on or "
               f"after **{day(due)}** unless you {OBJECT}. Your `approved` label applies it "
               "at once. Nothing is needed from you otherwise.")
    elif patch:
        how = ("Applied automatically, exactly as shown, when you label this `approved`. "
               f"It does not apply itself after notice, because {waits}.")

    # The applying job and `escalations.py notices` both find a notice by its
    # label, so a notice always carries it, whatever else was asked for.
    labels = [l.strip() for l in (args.labels or "").split(",") if l.strip()]
    if notice and "notice" not in labels:
        labels.append("notice")
    elif not labels:
        labels.append("needs-owner")
    parts = [
        "---",
        f"title: {args.title}",
        f"key: {key}",
        f"labels: {','.join(labels)}",
        f"raised_at: {now.isoformat(timespec='seconds')}",
        "---",
        "",
        *lead,
        body,
        "",
    ]
    if patch:
        parts += patch_section(*patch, how)
    if args.recommend:
        parts += ["## Recommendation", "", args.recommend, ""]
    parts += [
        "---",
        "",
        "*A notice from a `/shift` run. Nothing is needed from you unless you object.*"
        if notice else
        "*Raised automatically by a `/shift` run, which could not go on without you. "
        "Close this issue once decided.*",
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
    if patch and waits:
        print(f"this change waits for the owner's label: {waits}")
    if patch:
        print("do NOT commit the workflow edit itself (it cannot be pushed): "
              "`git checkout -- .github/workflows/` to drop it")


if __name__ == "__main__":
    main()
