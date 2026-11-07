"""Shuffle tag_trial.py runs into one blind sheet for a fresh scorer.

    venv/bin/python scripts/tag_trial.py --model upload --gemini-model gemini-3.6-flash --posts 2,4,9 > a.jsonl
    venv/bin/python scripts/tag_trial.py --model upload --gemini-model gemini-3.8-flash --posts 2,4,9 > b.jsonl
    venv/bin/python scripts/tag_sheet.py a.jsonl b.jsonl --key key.json > sheet.md

Each reaction is shown beside its question and the answer it follows, in a
shuffled order that names no model; the key maps each row back. Hand the
scorer the sheet alone (PRD §4, 11-07: the successor's tag trial). Spends no
request.
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.tag_trial import POSTS


def read_rows(paths):
    """One row per reaction from tag_trial's JSON lines; other output is skipped."""
    rows = []
    for path in paths:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                r = json.loads(line)
                if "post" not in r:
                    continue
                question, answers = POSTS[r["post"] - 1]
                for i, tag in enumerate(r.get("reactions") or []):
                    rows.append({"model": r.get("model") or path, "post": r["post"],
                                 "answer": i + 1, "question": question,
                                 "answer_text": answers[i], "tag": tag or "(none)"})
    return rows


def build(rows, seed):
    """(sheet text, key): the sheet carries no model, the key carries it by row number."""
    order = list(range(len(rows)))
    random.Random(seed).shuffle(order)
    lines, key = [], {"seed": seed, "rows": {}}
    for n, i in enumerate(order, 1):
        r = rows[i]
        lines.append(f"{n}. Q: {r['question']}\n   Answer: {r['answer_text']}\n   Tag: {r['tag']}")
        key["rows"][n] = {k: r[k] for k in ("model", "post", "answer", "tag")}
    return "\n\n".join(lines) + "\n", key


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="tag_trial.py output, one file per run")
    ap.add_argument("--key", required=True, help="where the model-per-row key is written")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)
    rows = read_rows(args.runs)
    if not rows:
        raise SystemExit("no reactions found in " + ", ".join(args.runs))
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10**6)
    text, key = build(rows, seed)
    with open(args.key, "w") as f:
        json.dump(key, f, indent=1, ensure_ascii=False)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
