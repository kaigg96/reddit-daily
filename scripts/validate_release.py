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
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

MAX_REQUESTS = 8  # screen replay (5) + metadata (1), with headroom for one retry

SUMMARY = []


def note(line):
    print(line)
    SUMMARY.append(line)


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
