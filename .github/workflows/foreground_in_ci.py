"""Refuse background work in an unattended shift (PreToolUse hook).

On 2026-11-04 the 10:54 shift started its idea generator and a timer in the
background, said it would rank the ideas when they came back, and ended its
turn. In CI an ended turn ends the job, so nothing came back: the shift left
no handover after 5 of its 60 minutes. Foreground agents sent in one message
still run side by side, so refusing the background loses nothing.

Loaded only by shift.yml (`--settings shift-settings.json`), so an interactive
session, which does hear back from its background work, is untouched. Exit 2
refuses the call and shows the model the reason.
"""
import json
import sys

AGENT_TOOLS = {"Agent", "Task"}


def refusal(call):
    """Why `call` must not run here, or None."""
    tool, args = call.get("tool_name"), call.get("tool_input") or {}
    if tool in AGENT_TOOLS and args.get("run_in_background") is not False:
        return ("In an unattended shift a background agent never reports back: "
                "ending the turn ends the job first. Send it again with "
                "run_in_background: false; several in one message still run in parallel.")
    if tool == "Bash" and args.get("run_in_background"):
        return ("In an unattended shift a background command never reports back: "
                "ending the turn ends the job first. Run it in the foreground.")
    return None


def main(stdin):
    try:
        call = json.load(stdin)
    except ValueError:
        return 0  # an unreadable call is not this hook's to block
    reason = refusal(call)
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin))
