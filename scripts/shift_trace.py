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

# Secrets the agent itself holds, so giving them to this step exposes nothing
# new; their values are replaced wherever they appear. The subscription token
# is deliberately not among them: the agent cannot read it, this script runs
# from a tree the agent could have edited, and its shape (sk-ant-) is caught.
SECRET_VARS = ("GEMINI_API_KEY", "GROQ_API_KEY", "AWS_READONLY_ACCESS_KEY_ID",
               "AWS_READONLY_SECRET_ACCESS_KEY", "GITHUB_TOKEN", "GH_TOKEN")
# Anything token-shaped that a secret variable would not catch, such as a token
# minted during the run or the job's OIDC request token.
TOKEN_SHAPES = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9_\-]{10,}"
    r"|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{30,}|A[SK]IA[0-9A-Z]{16}"
    r"|x-access-token:[^@\s]+|(?i:(?<=bearer )\S{16,})|(?i:authorization: *basic +\S+)"
    r"|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]*")
# An AWS account id in an ARN: money_check.py prints only its last four digits.
ARN_ACCOUNT = re.compile(r"(arn:aws:[^:\s]*:[^:\s]*:)\d{12}")


def redact(text, env=None):
    env = os.environ if env is None else env
    for name in SECRET_VARS:
        value = (env.get(name) or "").strip()
        if len(value) >= 8:
            text = text.replace(value, "***")
    return ARN_ACCOUNT.sub(r"\1***", TOKEN_SHAPES.sub("***", text))


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


def _error_line(text):
    """The line that says what failed. A failed Bash result opens with
    "Exit code N", which alone says nothing, so the next line comes with it."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return "error"
    if re.fullmatch(r"Exit code \d+", lines[0]) and len(lines) > 1:
        return f"{lines[0]}: {lines[1]}"
    return lines[0]


def _ended(result):
    """How the run ended, with the reason an error result carries in `errors`
    (error_max_turns, error_during_execution carry no `result` text)."""
    if not result:
        return "no result message: the agent did not finish (killed, timed out or never started)"
    out = (f"{result.get('subtype', '?')}, is_error {str(bool(result.get('is_error'))).lower()}, "
           f"{result.get('num_turns', '?')} turns, {(result.get('duration_ms') or 0) / 60000:.1f} min")
    if result.get("stop_reason"):
        out += f", stop {result['stop_reason']}"
    errors = result.get("errors")
    if errors:
        out += "; errors: " + "; ".join(_one_line(e, 200) for e in (errors if isinstance(errors, list) else [errors]))
    denied = result.get("permission_denials")
    if denied:
        names = sorted({str(d.get("tool_name", "?")) if isinstance(d, dict) else str(d) for d in denied})
        out += f"; {len(denied)} permission denial(s): {', '.join(names)}"
    return out


def trace(messages):
    """(ending, final message, [(tool, what, error or "")], helper (calls, failed)).

    Helper agents' messages (a `parent_tool_use_id`) are counted, not listed:
    the trace is the shift's own account, and its last words are its own."""
    calls, index, final_text, helper = [], {}, "", [0, 0]
    helper_ids = set()
    for m in messages:
        kind, own = m.get("type"), not m.get("parent_tool_use_id")
        for block in _content(m):
            if kind == "assistant" and block.get("type") == "text" and block.get("text", "").strip():
                if own:
                    final_text = block["text"]
            elif kind == "assistant" and block.get("type") == "tool_use":
                if own:
                    index[block.get("id")] = len(calls)
                    calls.append([block.get("name", "?"), _what(block.get("name"), block.get("input")), ""])
                else:
                    helper[0] += 1
                    helper_ids.add(block.get("id"))
            elif kind == "user" and block.get("type") == "tool_result" and block.get("is_error"):
                i = index.get(block.get("tool_use_id"))
                if i is not None:
                    calls[i][2] = _error_line(_result_text(block))
                elif block.get("tool_use_id") in helper_ids:
                    helper[1] += 1
    results = [m for m in messages if m.get("type") == "result"]
    result = results[-1] if results else {}
    final = str(result.get("result") or final_text)
    return _ended(result), final, [tuple(c) for c in calls], tuple(helper)


def render(ending, final, calls, helper=(0, 0), run_id="", env=None):
    # Each piece is redacted before it is cut short: a cut through a token
    # leaves a prefix too short for TOKEN_SHAPES to recognise.
    clean = lambda text, limit: _one_line(redact(str(text), env), limit)
    errors = sum(1 for c in calls if c[2])
    helpers = f" Helper agents made {helper[0]} more, {helper[1]} failed." if helper[0] else ""
    out = [f"## Shift trace{f' — run {run_id}' if run_id else ''}", "",
           f"**Ended:** {clean(ending, 600)}. **Tool calls:** {len(calls)}, {errors} failed.{helpers}", "",
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
    head = f"## Shift trace{f' — run {run_id}' if run_id else ''}\n\n"
    try:
        text = render(*trace(load(path)), run_id=run_id)
    except FileNotFoundError:
        # The action writes the file when the agent returns; a job killed or
        # cancelled first leaves none.
        text = head + ("**Ended:** no execution output: the agent did not finish "
                       "(killed, cancelled or timed out before it returned).\n")
    except Exception as e:   # never fail the job over its own diagnostics
        text = head + f"**Ended:** unknown: the execution output could not be read ({type(e).__name__}).\n"
    print(text)
    if write:
        with open(write, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
