"""No tracked file holds a credential. The repo is public, and every shift
commits; the standing check "secrets never committed" was a reading by eye.
On 2026-11-06 a history scan found two Google refresh tokens in a 2025
notebook's saved output (dead, and the client secret was never committed),
which no check had seen."""
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.shift_trace import CREDENTIAL_SHAPES

CREDENTIAL = re.compile(CREDENTIAL_SHAPES)
# Fixtures made up to prove the redactor catches each shape.
FAKE_BY_DESIGN = {"tests/test_shift_trace.py"}
BINARY = (".mp4", ".mp3", ".wav", ".png", ".jpg", ".jpeg", ".gif", ".ttf",
          ".otf", ".enc", ".pyc", ".zip", ".gz")


def _tracked():
    r = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        pytest.skip("not a git checkout")
    return [f for f in r.stdout.split("\0") if f]


def test_no_tracked_file_holds_a_credential():
    found = []
    for path in _tracked():
        if path in FAKE_BY_DESIGN or path.lower().endswith(BINARY):
            continue
        try:
            with open(os.path.join(ROOT, path), encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except OSError:   # deleted in the working tree, or a submodule
            continue
        for m in CREDENTIAL.finditer(text):
            found.append(f"{path}: {m.group()[:8]}…")
    assert not found, "credential-shaped values are committed:\n" + "\n".join(found)


# Built at run time, so this file never holds the shapes it scans for.
@pytest.mark.parametrize("prefix, body", [
    ("1//0", "6" + "Fake-" * 8),
    ("GOCSPX", "-" + "Fake_" * 5),
    ("-----BEGIN RSA PRIVATE", " KEY-----"),
    ("AK", "IA" + "FAKE" * 4),
])
def test_each_shape_is_recognised(prefix, body):
    assert CREDENTIAL.search(prefix + body)
