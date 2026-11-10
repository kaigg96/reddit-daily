"""Shuffle tag_trial.py runs into one blind sheet for a fresh scorer.

    venv/bin/python scripts/tag_trial.py --model upload --gemini-model gemini-3.6-flash --posts 2,4,9 > a.jsonl
    venv/bin/python scripts/tag_trial.py --model upload --gemini-model gemini-3.8-flash --posts 2,4,9 > b.jsonl
    venv/bin/python scripts/tag_sheet.py a.jsonl b.jsonl --key key.json > sheet.md
    venv/bin/python scripts/tag_sheet.py run.jsonl --with-shipped --key key.json \
        --sheet-path /tmp/sheet.md --scorer-prompt /tmp/prompt.txt > /tmp/sheet.md

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

# The shipped nine (3.6-flash, 11-08, PRD §4): every stage sheet carries them,
# so each scorer's strictness reads beside the arm (blind: 4, 2 and 1 of 9).
SHIPPED_11_08 = {2: ["Goodbye free time", "Endless billable hours", "Fancy catering though"],
                 4: ["Housing market hits", "Tuition pays coddling", "Tale old time"],
                 9: ["Liquid gold baby", "That hurt inside", "Classic perk right"]}
# Stage 1's scorer prompt, word for word (11-10): later stages score the same
# way, so their counts compare. Give a fresh agent this and the sheet only.
SCORER_PROMPT = """You are a blind scorer. Read the file {sheet} and nothing else (do not open any other file, key, or repo document). It has {n} numbered rows. Each row is a question asked on a Q&A show, one answer to it, and a short on-screen "tag": the show host's 1–3 word reaction, shown at the end of that answer.

Score each tag against this strict bar:
- PASS (a reaction) only if it reacts to how the answer lands: a laugh, a wince, doubt, surprise, sympathy. It sounds like a person's spontaneous response.
- FAIL (a label) if it labels, names, categorises or sums up the answer's content (e.g. "Retail monopoly", "Per day cost", "Classic perk"), even if accurate or witty-sounding.
- FAIL if it would not make sense to a viewer who heard only that answer.
- FAIL if, on a political answer, it agrees or takes a side rather than reacting to the delivery.
Be strict: when it is between reaction and label, it is a label. Judge each row on its own.

Output exactly one line per row, in order, as `N. PASS|FAIL — reason in under 10 words`, then a final line `TOTAL PASS: n of {n}`. Nothing else."""


def shipped_rows():
    """SHIPPED_11_08 as rows, so a sheet carries them without a typed file."""
    rows = []
    for post, tags in SHIPPED_11_08.items():
        question, answers = POSTS[post - 1]
        for i, tag in enumerate(tags):
            rows.append({"model": "shipped-11-08", "run": "shipped-11-08", "post": post,
                         "answer": i + 1, "question": question,
                         "answer_text": answers[i], "tag": tag})
    return rows


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
                    # The run's file too: two arms on one model (a wording, a
                    # thinking level) share the model, so only it tells them apart.
                    rows.append({"model": r.get("model") or path, "run": path, "post": r["post"],
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
        key["rows"][n] = {k: r[k] for k in ("model", "run", "post", "answer", "tag")}
    return "\n\n".join(lines) + "\n", key


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="tag_trial.py output, one file per run")
    ap.add_argument("--key", required=True, help="where the model-per-row key is written")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--with-shipped", action="store_true",
                    help="add the shipped nine (SHIPPED_11_08), as every stage sheet does")
    ap.add_argument("--scorer-prompt", default=None,
                    help="also write SCORER_PROMPT for this sheet to this path")
    ap.add_argument("--sheet-path", default="sheet.md",
                    help="where the sheet will be saved, named in the scorer prompt")
    args = ap.parse_args(argv)
    rows = (shipped_rows() if args.with_shipped else []) + read_rows(args.runs)
    if not rows:
        raise SystemExit("no reactions found in " + ", ".join(args.runs))
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10**6)
    text, key = build(rows, seed)
    with open(args.key, "w") as f:
        json.dump(key, f, indent=1, ensure_ascii=False)
    if args.scorer_prompt:
        with open(args.scorer_prompt, "w") as f:
            f.write(SCORER_PROMPT.format(sheet=args.sheet_path, n=len(rows)) + "\n")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
