#!/usr/bin/env python3
"""Replay every shipped title through two versions of the code.

For any change to shipped text this is the gate that works (TECH_DEBT, the
11-05 audit): on 11-04 the unit tests passed while a replay of every logged
title caught the fix's own regressions (F159). It was rebuilt by hand each
time, and twice went wrong the same ways (F175): the cleaner prints its
refusal notice to stdout, which corrupted results written there, and two
identical outputs had to be proven to come from two different trees.

    replay_text.py main integration/preview    # before merging bet 1
    replay_text.py main HEAD --out /tmp/replay # keep both results

Each ref's `src/` is extracted with `git archive` and imported in its own
process, so neither tree can see the other. Results go to a file, never
stdout, and each side prints the file its module loaded from and a hash of
its `src/*.py`. Inputs are `upload_log.csv` on disk: each title as published
goes through `_clean_published` and then `resolve_title`, as `src.llm` treats
a generated one, with the upload's logged style and capitals arm and its
Reddit question as the fallback. Two limits: the shock check sees the
question only (production also passes the top answers, which are not
logged), so a title cleared by an answer's word reads as a fallback on both
sides; and closing lines are not replayed, since only a few are logged
(from 11-04) and bet 1 writes them by another path, the host's vote.
Nothing calls a model or the network. Exits 1 when the two disagree on any
title, which is a list to read, not a failure by itself: an intended fix
changes some; exits 2 when both refs carry the same `src/`.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "upload_log.csv")

# Run inside the extracted tree. Its stdout is the cleaner's, so the results
# go to the file named in argv[3] and only that file is trusted.
CHILD = r"""
import contextlib, glob, hashlib, io, json, os, sys
tree, inputs, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, tree)
with contextlib.redirect_stdout(io.StringIO()):
    from src import llm

def title(row):
    generated = llm._clean_published(row["video_title"])
    if generated is None:
        return "REFUSED: swear word or emoji"
    caps = int(row["title_caps"]) if row["title_caps"] in ("0", "1") else None
    r = llm.resolve_title(generated, row["title_style"] or "A", row["post_title"],
                          caps=caps, source=row["post_title"])
    return r.title if r.ok else "FALLBACK: " + r.title

rows = json.load(open(inputs))
with contextlib.redirect_stdout(io.StringIO()):
    result = {
        "module": llm.__file__,
        "sha256": hashlib.sha256(b"".join(
            open(f, "rb").read() for f in sorted(glob.glob(os.path.join(tree, "src", "*.py"))))
        ).hexdigest(),
        "title": [title(r) for r in rows],
    }
json.dump(result, open(out, "w"))
"""


def shipped_rows(path=LOG):
    with open(path, newline="") as f:
        return [{"video_id": r["video_id"], "video_title": r["video_title"],
                 "post_title": r["post_title"], "title_style": r.get("title_style") or "",
                 "title_caps": r.get("title_caps") or ""}
                for r in csv.DictReader(f) if r.get("video_title")]


def extract(ref, dest):
    """`ref`'s src/ under `dest`, or SystemExit naming a ref git cannot read."""
    shutil.rmtree(dest, ignore_errors=True)  # a reused --out keeps no stale file
    os.makedirs(dest)
    archive = os.path.join(dest, "src.tar")
    try:
        subprocess.run(["git", "archive", "--format=tar", "-o", archive, ref, "src"],
                       cwd=ROOT, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"cannot read {ref!r}: {e.stderr.decode().strip()}")
    with tarfile.open(archive) as t:
        if hasattr(tarfile, "data_filter"):
            t.extractall(dest, filter="data")
        else:
            t.extractall(dest)
    return dest


def replay(ref, rows, workdir):
    tree = extract(ref, os.path.join(workdir, ref.replace("/", "_")))
    inputs = os.path.join(workdir, "inputs.json")
    with open(inputs, "w") as f:
        json.dump(rows, f)
    out = os.path.join(tree, "result.json")
    run = subprocess.run([sys.executable, "-c", CHILD, tree, inputs, out],
                         cwd=tree, capture_output=True, text=True)
    if run.returncode:
        sys.exit(f"{ref}: replay failed\n{run.stderr.strip()}")
    with open(out) as f:
        result = json.load(f)
    if not os.path.realpath(result["module"]).startswith(os.path.realpath(tree)):
        sys.exit(f"{ref}: loaded {result['module']}, not its own tree")
    return result


def compare(rows, a, b):
    """(titles compared, {reason: count} refused by both, every title that
    differs). Titles shipped before a guard existed are refused by both."""
    refused = collections.Counter(
        "fell back to the question" if x.startswith("FALLBACK") else x[len("REFUSED: "):]
        for x, y in zip(a["title"], b["title"])
        if x == y and x.startswith(("REFUSED: ", "FALLBACK: ")))
    diffs = [(r["video_id"], x, y) for r, x, y in zip(rows, a["title"], b["title"]) if x != y]
    return len(rows), dict(refused), diffs


def main(argv=None, log=LOG):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("ref_a")
    p.add_argument("ref_b")
    p.add_argument("--out", help="directory to keep both trees' results in")
    args = p.parse_args(argv)

    rows = shipped_rows(log)
    with tempfile.TemporaryDirectory() as tmp:
        workdir = args.out or tmp
        os.makedirs(workdir, exist_ok=True)
        a = replay(args.ref_a, rows, workdir)
        b = replay(args.ref_b, rows, workdir)
    for ref, r in ((args.ref_a, a), (args.ref_b, b)):
        print(f"{ref}: {os.path.relpath(r['module'], workdir)}, src/ sha256 {r['sha256'][:12]}")
    if a["sha256"] == b["sha256"]:
        print("both refs carry the same src/: the replay compares nothing")
        return 2

    n, refused, diffs = compare(rows, a, b)
    why = ", ".join(f"{k} {v}" for k, v in sorted(refused.items()))
    print(f"titles: {n - len(diffs)} of {n} identical, "
          f"{sum(refused.values())} refused by both{f' ({why})' if why else ''}")
    for vid, x, y in diffs:
        print(f"  {vid}\n    {args.ref_a}: {x}\n    {args.ref_b}: {y}")
    return 1 if diffs else 0

if __name__ == "__main__":
    sys.exit(main())
