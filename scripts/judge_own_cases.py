#!/usr/bin/env python3
"""One request: does the own-question show's title judge right the fixed
cases (PLAN C16; TECH_DEBT's own-title item)? The last check before
`SOURCE=own` can turn on: the unit tests prove the plumbing with the judge
mocked, never its model.

    judge_own_cases.py                            # the sample model
    judge_own_cases.py --model gemini-3.6-flash   # the uploads' model

Spends ONE Gemini request, never retried: only after the 07:00 UTC reset and
an hour clear of a scheduled run (CLAUDE.md §1). The sample model has its own
allowance, so the default leaves the uploads' untouched; it is also the
judge's fallback. The cases go in one batch in the judge's own words
(`llm._OWN_JUDGE`), so the request is the judge's but for how many lines it
reads. Exits 1 unless every case is right, 2 when no usable reply came.
"""
import argparse
import json
import re
import sys

sys.path.insert(0, ".")
from src import llm  # noqa: E402
from tests.test_own_title_cases import CASES  # noqa: E402


def prompt():
    lines = "\n".join(f"{i}: {json.dumps(line, ensure_ascii=False)}"
                      for i, (line, _) in enumerate(CASES, 1))
    shape = ", ".join(f'"{i}": "yes" or "no"' for i in range(1, len(CASES) + 1))
    return llm._OWN_JUDGE.format(lines=lines, shape=shape)


def grade(raw):
    """[(right, said, line)] per case, by the judge's own rule (anything but
    a plain "no" refuses); None when the reply is not a JSON object."""
    match = re.search(r"\{.*\}", raw or "", re.S)
    try:
        verdict = json.loads(match.group(0)) if match else None
    except ValueError:
        verdict = None
    if not isinstance(verdict, dict):
        return None
    rows = []
    for i, (line, refuse) in enumerate(CASES, 1):
        said = str(verdict.get(str(i), "")).strip().lower()
        rows.append(((said != "no") == refuse, said or "-", line))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model", default=llm.SAMPLE_MODEL)
    args = ap.parse_args(argv)
    if llm.provider() != "gemini":   # it would answer on Groq, under Gemini's name
        print("AI_PROVIDER routes to Groq: unset it to grade a Gemini model")
        return 2
    try:
        raw = llm._generate(prompt(), model=args.model)
    except Exception as e:   # noqa: BLE001
        # The label only: an HTTPError's message can embed the keyed URL.
        print(f"no answer from {args.model}: {llm._failure_kind(e)}")
        return 2
    rows = grade(raw)
    if rows is None:
        print(f"{args.model} replied without a JSON object")
        return 2
    for right, said, line in rows:
        print(f"{'ok   ' if right else 'WRONG'} {said:<5} {line}")
    wrong = sum(not right for right, _, _ in rows)
    print(f"{len(rows) - wrong} of {len(rows)} right on {args.model}")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
