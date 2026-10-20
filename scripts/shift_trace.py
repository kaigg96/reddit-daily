#!/usr/bin/env python3
"""What a shift did, from the agent's execution output: how it ended, its last
message, and every tool it called, with failures marked.

The action hides its own output because the repo's logs are public, and a shift
cannot read Actions logs anyway. So run 39338110057 (2026-10-19) stopped after
32 turns with no handover and left nothing to find out why. This writes the
trace to the log and to `.github/last-shift-trace.md`, where the next shift can
read it. Secrets are redacted: the values of the job's secret variables, and
anything shaped like a token.

    shift_trace.py <execution-output.json> [--write PATH] [--run-id ID]
"""
import json
import os
import re
import sys

TRACE = ".github/last-shift-trace.md"
SUMMARY_END = "### Tool calls"   # shift_report.py quotes the trace up to here
MAX_CALLS = 80
MAX_FINAL = 2000

# The shift job's secrets. Their values are replaced wherever they appear; the
# step that runs this is given them for that alone.
SECRET_VARS = ("CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY", "GROQ_API_KEY",
               "AWS_READONLY_ACCESS_KEY_ID", "AWS_READONLY_SECRET_ACCESS_KEY",
               "GITHUB_TOKEN", "GH_TOKEN")
# Anything token-shaped that a secret variable would not catch, such as a token
# minted during the run.
TOKEN_SHAPES = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9_\-]{10,}"
    r"|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{30,}|A[SK]IA[0-9A-Z]{16}"
    r"|x-access-token:[^@\s]+|(?<=Bearer )[A-Za-z0-9._\-]{16,}")


def redact(text, env=None):
    env = os.environ if env is None else env
    for name in SECRET_VARS:
        value = env.get(name) or ""
        if len(value) >= 8:
            text = text.replace(value, "***")
    return TOKEN_SHAPES.sub("***", text)


def load(path):
    """The action's messages, in order. It writes a JSON array, one object or
    a stream of objects depending on version (as shift_budget.record)."""
    text = open(path, encoding="utf-8").read()
    try:
        data = json.loads(text)
    except ValueError:
        data = [json.loads(line) for line in text.splitlines() if line.strip().startswith("{")]
    if isinstance(data, dict):
        data = [data]
    return [m for m in data if isinstance(m, dict)]


def _content(message):
    inner = message.get("message")
    content = inner.get("content") if isinstance(inner, dict) else message.get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [b for b in content or [] if isinstance(b, dict)]


def _one_line(text, limit):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _what(name, args):
    """The part of a tool call that says what it did."""
    args = args if isinstance(args, dict) else {}
    for key in ("command", "file_path", "path", "pattern", "url", "query",
                "description", "skill", "prompt"):
        if args.get(key):
            first = str(args[key]).strip().splitlines()[0] if str(args[key]).strip() else ""
            return first
    return ", ".join(sorted(args)) if args else ""


def _result_text(block):
    content = block.get("content")
    if isinstance(content, list):
        content = " ".join(str(c.get("text", "")) for c in content if isinstance(c, dict))
    return str(content or "")


def trace(messages):
    """(ending, final message, [(tool, what, error or "")])."""
    calls, index, final_text = [], {}, ""
    for m in messages:
        kind = m.get("type")
        for block in _content(m):
            if kind == "assistant" and block.get("type") == "text" and block.get("text", "").strip():
                final_text = block["text"]
            elif kind == "assistant" and block.get("type") == "tool_use":
                index[block.get("id")] = len(calls)
                calls.append([block.get("name", "?"), _what(block.get("name"), block.get("input")), ""])
            elif kind == "user" and block.get("type") == "tool_result" and block.get("is_error"):
                i = index.get(block.get("tool_use_id"))
                if i is not None:
                    calls[i][2] = _result_text(block).strip().splitlines()[0] if _result_text(block).strip() else "error"
    results = [m for m in messages if m.get("type") == "result"]
    result = results[-1] if results else {}
    final = str(result.get("result") or final_text)
    if result:
        ending = (f"{result.get('subtype', '?')}, is_error {str(bool(result.get('is_error'))).lower()}, "
                  f"{result.get('num_turns', '?')} turns, "
                  f"{(result.get('duration_ms') or 0) / 60000:.1f} min")
    else:
        ending = "no result message: the agent did not finish (killed, timed out or never started)"
    return ending, final, [tuple(c) for c in calls]


def render(ending, final, calls, run_id="", env=None):
    # Each piece is redacted before it is cut short: a cut through a token
    # leaves a prefix too short for TOKEN_SHAPES to recognise.
    clean = lambda text, limit: _one_line(redact(str(text), env), limit)
    errors = sum(1 for c in calls if c[2])
    out = [f"## Shift trace{f' — run {run_id}' if run_id else ''}", "",
           f"**Ended:** {ending}. **Tool calls:** {len(calls)}, {errors} failed.", "",
           "**Last message:**", ""]
    quoted = redact(final.strip(), env)[:MAX_FINAL] or "(none)"
    out += ["> " + line if line.strip() else ">" for line in quoted.splitlines()]
    shown = calls[-MAX_CALLS:]
    out += ["", SUMMARY_END + (f" (last {len(shown)} of {len(calls)})" if len(shown) < len(calls) else ""), ""]
    start = len(calls) - len(shown) + 1
    for n, (name, what, error) in enumerate(shown, start):
        line = f"{n}. {'✗ ' if error else ''}{name}: {clean(what, 140)}"
        if error:
            line += f" — {clean(error, 140)}"
        out.append(line)
    return redact("\n".join(out) + "\n", env)


def summary(trace_path, run_id=""):
    """The trace's head for the report email, or "" when there is none for
    this run (a stale file from an earlier shift says nothing about this one)."""
    try:
        text = open(trace_path, encoding="utf-8").read()
    except OSError:
        return ""
    if run_id and f"run {run_id}" not in text.split("\n", 1)[0]:
        return ""
    return text.split(SUMMARY_END, 1)[0].strip()


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    path, write, run_id = argv[0], None, os.environ.get("GITHUB_RUN_ID", "")
    if "--write" in argv:
        write = argv[argv.index("--write") + 1]
    if "--run-id" in argv:
        run_id = argv[argv.index("--run-id") + 1]
    try:
        text = render(*trace(load(path)), run_id=run_id)
    except Exception as e:   # never fail the job over its own diagnostics
        text = (f"## Shift trace{f' — run {run_id}' if run_id else ''}\n\n"
                f"**Ended:** unknown: the execution output could not be read ({type(e).__name__}).\n")
    print(text)
    if write:
        with open(write, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
