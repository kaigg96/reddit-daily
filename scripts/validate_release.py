#!/usr/bin/env python3
"""Run the Gemini-dependent release gates unattended, in CI.

Two checks gate the pending release and both need live Gemini, which is capped
at 20 requests/day shared with production (PRD §2). That makes them awkward to
run by hand: the window opens at the 07:00 UTC reset, and whoever is awake then
is the constraint. CI has the same secrets and no such constraint, so the gates
run here instead.

    venv/bin/python scripts/validate_release.py

Exits 0 if every gate passes, 1 otherwise, and writes a Markdown verdict to
$GITHUB_STEP_SUMMARY when present. Costs at most MAX_REQUESTS Gemini calls.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

MAX_REQUESTS = 8  # screen replay (5) + metadata (1), with headroom for one retry

# What the gates actually exercise. A commit touching nothing here cannot
# change their verdict, so it must not trigger a re-run -- see should_validate.
GATED_PATHS = ("src", "scripts", "tests", "requirements.txt")

# A PASS expires even with no code change, because the model can drift.
MAX_VERDICT_AGE_DAYS = 7

SUMMARY = []


def note(line):
    print(line)
    SUMMARY.append(line)


def parse_verdict(text):
    """Pull `(commit, passed, when)` out of a last-release-validation.md."""
    text = text or ""
    commit = re.search(r"^- \*\*Commit:\*\* `([^`]+)`", text, re.M)
    passed = re.search(r"^- \*\*Verdict:\*\*.*\bPASS\b", text, re.M)
    when = re.search(r"^- \*\*When:\*\* (\S+)", text, re.M)
    stamp = None
    if when:
        try:
            stamp = datetime.datetime.strptime(when.group(1), "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            stamp = None
    return (commit.group(1) if commit else None), bool(passed), stamp


def should_validate(verdict_text, target_sha, gated_code_changed, now=None,
                    max_age_days=MAX_VERDICT_AGE_DAYS):
    """Do the Gemini gates need to run, or does the last PASS still apply?

    They cost 6 of the 20 daily requests, shared with live uploads, so the
    answer has to be "no" whenever nothing they test has moved.

    **Comparing shas cannot decide this.** Recording a verdict commits to
    `main`, so the next run's HEAD is always at least one commit past the sha
    just validated, and the sha-equality check this replaces could therefore
    never match again — it spent 6 requests every morning to re-learn the same
    answer, and the 2026-09-20 05:01 upload shipped with a raw Reddit question
    as its title because the budget was gone. Compare the code the gates
    actually exercise instead, so doc, WORKLOG and verdict-record commits are
    correctly free.

    Code is not the only thing that can move, though: `gemini-2.5-flash` can
    change behaviour under a pinned name with no commit of ours, and only a
    re-run catches that. So a PASS also expires after `max_age_days` — weekly
    drift detection costs 6 requests a week instead of 42.
    """
    prev_sha, passed, when = parse_verdict(verdict_text)
    if not prev_sha:
        return True, "no previous verdict recorded"
    if not passed:
        # Commonest cause of a FAIL is an exhausted quota, not bad output.
        return True, f"last verdict ({prev_sha}) was a FAIL — retrying"

    age = None
    if when is not None:
        age = ((now or datetime.datetime.utcnow()) - when).days
    if age is None or age >= max_age_days:
        shown = "undated" if age is None else f"{age}d old"
        return True, f"last PASS is {shown} — re-checking for model drift"

    if prev_sha == target_sha:
        return False, f"{target_sha} already validated and passed ({age}d ago)"
    if gated_code_changed(prev_sha):
        return True, f"gated code changed since {prev_sha}"
    return False, f"nothing the gates exercise changed since {prev_sha} ({age}d ago)"


def _git_gated_code_changed(target_ref):
    """`gated_code_changed` backed by the real repo, failing toward validating."""
    def changed(prev_sha):
        found = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{prev_sha}^{{commit}}"],
            cwd=ROOT, capture_output=True)
        if found.returncode != 0:
            return True  # can't resolve it, so can't prove it is still valid
        diff = subprocess.run(
            ["git", "diff", "--quiet", prev_sha, target_ref, "--", *GATED_PATHS],
            cwd=ROOT, capture_output=True)
        # 0 = identical, 1 = differs, >1 = git failed (treat as differing).
        return diff.returncode != 0
    return changed


def should_run_cli(args):
    """`--should-run`: decide, print `proceed=` for the workflow, spend nothing."""
    try:
        with open(os.path.join(ROOT, args.verdict_file)) as f:
            verdict_text = f.read()
    except OSError:
        verdict_text = ""

    target_sha = subprocess.run(["git", "rev-parse", "--short", args.target],
                                cwd=ROOT, capture_output=True, text=True).stdout.strip()
    proceed, why = should_validate(verdict_text, target_sha,
                                   _git_gated_code_changed(args.target))

    print(f"{'validating' if proceed else 'skipping'}: {why}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"proceed={'true' if proceed else 'false'}\n")
            f.write(f"reason={why}\n")
    return 0


def check_metadata():
    """One request: does the merged title+keywords+CTA prompt still work?

    Merging three focused prompts into one multi-task prompt can degrade each
    task, and unit tests can only cover the parsing half — the prompt half only
    shows up live.
    """
    from src import llm

    note("### Gate 1 — merged metadata prompt\n")
    q = "What hobby has become too expensive for the average person?"
    comments = ["Photography. Lenses cost more than my car did.",
                "Warhammer. The plastic crack is genuinely brutal now.",
                "Skiing. A lift ticket is close to two hundred dollars."]
    meta = llm.get_metadata(q, comments, style="A")

    ok = True
    for field, value in (("title", meta.title), ("keywords", meta.keywords),
                         ("cta", meta.cta)):
        if value is None:
            note(f"- ❌ `{field}` came back empty")
            ok = False
        else:
            shown = value if isinstance(value, str) else ", ".join(value[:5])
            note(f"- ✅ `{field}`: {str(shown)[:90]}")

    # A title longer than YouTube's limit, or one that is just the question
    # echoed back, means the prompt is producing junk even though it "worked".
    if meta.title:
        if len(meta.title) > 100:
            note(f"- ❌ title is {len(meta.title)} chars (YouTube caps at 100)")
            ok = False
        if meta.title.strip().lower() == q.strip().lower():
            note("- ❌ title is the question echoed back, not a rewrite")
            ok = False
    if meta.keywords is not None and len(meta.keywords) < 3:
        note(f"- ⚠️ only {len(meta.keywords)} keywords (expected ~10)")
    note("")
    return ok


def check_screen():
    """Five requests: does the R4.6 screen still reach the right verdicts?

    Validates `named_wrongdoing` (open since 2026-09-09) and, since thinking is
    now disabled for every Gemini call, whether the screen's JSON risk verdicts
    survive without reasoning tokens. The screen is the one genuine judgment
    task in the pipeline, so this is the check most worth running.
    """
    note("### Gate 2 — R4.6 screen replay\n")
    proc = subprocess.run([sys.executable, "scripts/replay_screen.py"],
                          cwd=ROOT, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    note("```\n" + out.strip()[-1800:] + "\n```")

    # The replay exits 0 when nothing *failed*, but cases that fell through to
    # the keyword backstop are inconclusive rather than passing — treating them
    # as a pass is exactly how the 2026-09-19 run looked green while proving
    # almost nothing.
    if "inconclusive" in out:
        note("\n- ❌ some cases fell through to the backstop — not a verdict. "
             "Usually means Gemini was unreachable or the quota was spent.")
        return False
    if proc.returncode != 0:
        note("\n- ❌ replay reported a wrong verdict")
        return False
    note("\n- ✅ every case reached the expected verdict via Gemini")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--should-run", action="store_true",
                    help="only decide whether the gates need to run; spends no quota")
    ap.add_argument("--target", default="origin/main", help="ref under test")
    ap.add_argument("--verdict-file", default=".github/last-release-validation.md")
    args = ap.parse_args()

    if args.should_run:
        return should_run_cli(args)

    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not set", file=sys.stderr)
        return 1

    note(f"## Release validation\n\nBudget: at most {MAX_REQUESTS} Gemini "
         f"requests of the 20/day cap shared with production.\n")

    results = {"metadata": check_metadata(), "screen": check_screen()}
    passed = all(results.values())

    note("\n### Verdict\n")
    note(f"**{'PASS — release gates clear' if passed else 'FAIL — do not merge'}**\n")
    for name, ok in results.items():
        note(f"- {name}: {'pass' if ok else 'FAIL'}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            with open(summary_path, "a") as f:
                f.write("\n".join(SUMMARY) + "\n")
        except OSError:
            pass
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
