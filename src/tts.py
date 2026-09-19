"""AWS Polly synthesis with word-level speech marks (PRD R1.2).

Timings come from a second synthesize_speech call with OutputFormat='json' —
Polly cannot return audio and marks in one call, but identical Text/Voice/Engine
means the timings line up with the mp3.

Polly is the only service here that bills the owner (PRD §5, CLAUDE.md §1), and
that second call means every character is paid for twice. The per-process
budget below is the enforcement for "never synthesize in bulk": a real run
spends ~910 billed characters, so a batch job trips the guard long before it
reaches a surprising invoice.
"""

import json
import os

import boto3

from . import config


class PollyBudgetExceeded(Exception):
    """Raised instead of billing for a call that would break the char budget.

    Deliberately not caught anywhere: a run that would overspend should stop,
    not fail soft and keep going. If you hit this in normal pipeline work it is
    a bug (a retry loop, a duplicated synth pass), not a budget that is too
    small — check the call count before raising POLLY_CHAR_BUDGET.

    Inherits from Exception rather than RuntimeError on purpose: a retry loop
    written as `except RuntimeError: continue` would otherwise swallow the one
    signal telling it to stop. The budget itself is the real guarantee — once
    exhausted it refuses every later call, so spend stays bounded even against
    a caller that catches everything — but the exception should not be easy to
    swallow by accident.
    """


_spent = 0  # billed characters this process; both calls per segment count


def spent_chars():
    """Billed characters used so far in this process (for logging/tests)."""
    return _spent


def reset_budget():
    """Test helper — production runs are one video per process."""
    global _spent
    _spent = 0


def _charge(text, calls):
    """Account for `calls` synthesis passes over `text`, or refuse."""
    global _spent
    cost = len(text) * calls
    if _spent + cost > config.POLLY_CHAR_BUDGET:
        raise PollyBudgetExceeded(
            f"Polly budget exhausted: {_spent} billed chars used, this call adds "
            f"{cost}, budget is {config.POLLY_CHAR_BUDGET}. A normal video costs "
            f"~910. If this is a bulk job, it needs owner approval first "
            f"(CLAUDE.md §1); if it isn't, something is calling Polly in a loop."
        )
    _spent += cost


def make_polly():
    return boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_POLLY_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_POLLY_SECRET_ACCESS_KEY"),
        region_name="us-west-2",
    )


def synthesize_with_marks(polly, text, voice_id, out_path):
    """Write mp3 to out_path; return word marks [{'t': sec, 'w': word, 'end_offset': int}]."""
    # Charged up front for both passes: a failed call still bills, so the guard
    # has to hold even when the second request never returns.
    _charge(text, calls=2)

    audio = polly.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural"
    )
    with open(out_path, "wb") as f:
        f.write(audio["AudioStream"].read())

    marks_resp = polly.synthesize_speech(
        Text=text,
        OutputFormat="json",
        SpeechMarkTypes=["word"],
        VoiceId=voice_id,
        Engine="neural",
    )
    marks = []
    for line in marks_resp["AudioStream"].read().decode("utf-8").splitlines():
        if not line.strip():
            continue
        m = json.loads(line)
        if m.get("type") == "word":
            marks.append({"t": m["time"] / 1000.0, "w": m["value"], "end_offset": m["end"]})
    return marks
