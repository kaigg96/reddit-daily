#!/usr/bin/env python3
"""Replay every shipped title and closing line through two versions of the code.

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
its `src/*.py`. Inputs are `upload_log.csv` on disk: the title as published and the
closing line as logged, run through the same steps `src.llm` applies to a
generated one (`_clean_published`, then `_shock_bait` against the Reddit
question for titles, then `sentence_case`). Nothing calls a model or the
network. Exits 1 when the two disagree on any line, which is a list to read,
not a failure by itself: an intended fix changes some.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
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
    cleaned = llm._clean_published(row["video_title"])
    if cleaned is None:
        return "REFUSED: swear word or emoji"
    if llm._shock_bait(cleaned, row["post_title"]):
        return "REFUSED: shock phrase"
    return llm.sentence_case(cleaned)

def cta(row):
    cleaned = llm._clean_published(row["cta"])
    return "REFUSED: swear word or emoji" if cleaned is None else llm.sentence_case(cleaned)

rows = json.load(open(inputs))
with contextlib.redirect_stdout(io.StringIO()):
    result = {
        "module": llm.__file__,
        "sha256": hashlib.sha256(b"".join(
            open(f, "rb").read() for f in sorted(glob.glob(os.path.join(tree, "src", "*.py"))))
        ).hexdigest(),
        "title": [title(r) for r in rows],
        "cta": [cta(r) if r["cta"] else None for r in rows],
    }
json.dump(result, open(out, "w"))
"""


def shipped_rows(path=LOG):
    with open(path, newline="") as f:
        return [{"video_id": r["video_id"], "video_title": r["video_title"],
                 "post_title": r["post_title"], "cta": r.get("cta") or ""}
                for r in csv.DictReader(f) if r.get("video_title")]


def extract(ref, dest):
    """`ref`'s src/ under `dest`, or SystemExit naming a ref git cannot read."""
    os.makedirs(dest, exist_ok=True)
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
    """Per field: (lines compared, {reason: count} refused by both, every line
    that differs). Titles shipped before a guard existed are refused by both."""
    report = {}
    for field in ("title", "cta"):
        pairs = [(r, x, y) for r, x, y in zip(rows, a[field], b[field]) if x is not None]
        refused = collections.Counter(x[len("REFUSED: "):] for _, x, y in pairs
                                      if x == y and x.startswith("REFUSED: "))
        report[field] = (len(pairs), dict(refused),
                         [(r["video_id"], x, y) for r, x, y in pairs if x != y])
    return report


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

    differs = False
    for field, (n, refused, diffs) in compare(rows, a, b).items():
        name = "titles" if field == "title" else "closing lines"
        why = ", ".join(f"{k} {v}" for k, v in sorted(refused.items()))
        print(f"{name}: {n - len(diffs)} of {n} identical, "
              f"{sum(refused.values())} refused by both{f' ({why})' if why else ''}")
        for vid, x, y in diffs:
            differs = True
            print(f"  {vid}\n    {args.ref_a}: {x}\n    {args.ref_b}: {y}")
    return 1 if differs else 0


if __name__ == "__main__":
    sys.exit(main())
