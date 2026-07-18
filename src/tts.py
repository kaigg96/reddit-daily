"""AWS Polly synthesis with word-level speech marks (PRD R1.2).

Timings come from a second synthesize_speech call with OutputFormat='json' —
Polly cannot return audio and marks in one call, but identical Text/Voice/Engine
means the timings line up with the mp3.
"""

import json
import os

import boto3


def make_polly():
    return boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_POLLY_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_POLLY_SECRET_ACCESS_KEY"),
        region_name="us-west-2",
    )


def synthesize_with_marks(polly, text, voice_id, out_path):
    """Write mp3 to out_path; return word marks [{'t': sec, 'w': word, 'end_offset': int}]."""
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
