"""A free stand-in voice for renders that may not use Polly (#77).

A branch render narrates silently, since unmerged code never holds the Polly
keys (dry-run.yml), and the owner cannot judge from a silent sample whether a
first-time viewer follows the video. Kokoro is an open model (Apache-2.0) that
runs offline and reports when each sound is spoken, so the captions and the
host's tags land on the stand-in's own words. Uploads never use it: only a
silent render reaches this module (src/sample.py).

It lives in its own environment under GEN, because Kokoro needs numpy 2 and
the pipeline pins 1.26. Everything it downloads is pinned, and the model files
are checked against their digests before use.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from . import config

# The whole environment, every wheel locked by hash, so neither a release that
# morning nor a substituted file can change what runs beside the job's keys.
LOCK = Path(__file__).with_name("standin_requirements.txt")
RELEASES = "https://github.com/thewh1teagle/kokoro-onnx/releases/download"
FILES = {
    "kokoro-v1.0.int8.onnx": (f"{RELEASES}/model-files-v1.1/kokoro-v1.0.int8.onnx",
                              "ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c"),
    "voices-v1.0.bin": (f"{RELEASES}/model-files-v1.0/voices-v1.0.bin",
                        "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d"),
}
# The pipeline's two Polly voices, and the nearest of Kokoro's American ones.
VOICES = {"Danielle": "af_heart", "Stephen": "am_michael"}
WORKER = Path(__file__).with_name("standin_worker.py")


# Every call shares one deadline, so a stalled install or download leaves the
# render time to finish silently inside dry-run.yml's 900 seconds.
DEADLINE = 300
_state = {"started": None, "broken": None}


def _home():
    return config.GEN / "standin"


def _python():
    return _home() / "venv" / "bin" / "python"


def _left():
    if _state["started"] is None:
        _state["started"] = time.monotonic()
    left = DEADLINE - (time.monotonic() - _state["started"])
    if left <= 5:
        raise TimeoutError(f"the stand-in voice's {DEADLINE}s are spent")
    return left


def _clean_env():
    """Only what pip and the worker need: the job's API keys stay out of
    third-party code."""
    return {k: os.environ[k] for k in ("PATH", "HOME", "TMPDIR", "LANG") if k in os.environ}


def _run(args, **kw):
    try:
        return subprocess.run(args, check=True, capture_output=True, text=True,
                              env=_clean_env(), timeout=_left(), **kw)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{Path(args[0]).name} exited {e.returncode}: "
                           f"{(e.stderr or '').strip()[-300:]}") from None


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ensure():
    """Install the voice once per machine; raise if any part cannot be had.

    The environment counts as installed only once pip has finished with
    exactly today's pins, so a half-built one, or one with old pins, is built
    again rather than narrating silently on every later run."""
    home = _home()
    home.mkdir(parents=True, exist_ok=True)
    marker = home / "installed.txt"
    pins = LOCK.read_text()
    if not (marker.exists() and marker.read_text() == pins and _python().exists()):
        marker.unlink(missing_ok=True)
        shutil.rmtree(home / "venv", ignore_errors=True)
        _run([sys.executable, "-m", "venv", str(home / "venv")])
        _run([str(_python()), "-m", "pip", "install", "-q", "--only-binary=:all:",
              "--require-hashes", "-r", str(LOCK)])
        marker.write_text(pins)
    for name, (url, digest) in FILES.items():
        path = home / name
        if path.exists() and _digest(path) == digest:
            continue
        part = home / f"{name}.part"
        # The timeout bounds each read, not the whole file: a slow but moving
        # download is held to the deadline block by block.
        with urllib.request.urlopen(url, timeout=min(60, _left())) as r, open(part, "wb") as f:
            for block in iter(lambda: r.read(1 << 20), b""):
                _left()
                f.write(block)
        if _digest(part) != digest:
            part.unlink()
            raise RuntimeError(f"{name} does not match its pinned digest")
        part.replace(path)


# A word the voice may say as several (a number, "$", "U.S."), so the counts
# can match while the times sit on the wrong words: such text shares out its
# span by length instead.
PLAIN = re.compile(r"[^\W\d_]+(['’][^\W\d_]+)*")


def word_marks(marks, starts, duration):
    """Polly-shaped marks with the stand-in's times.

    `marks` are the evenly paced ones (src/sample.py), whose byte offsets stay.
    When the voice spoke as many words as the text has, all of them plain,
    each takes its own start. Otherwise the spoken span is shared out by
    length, so the last word still ends with the speech.
    """
    if len(starts) == len(marks) and all(PLAIN.fullmatch(m["w"]) for m in marks):
        return [dict(m, t=s) for m, s in zip(marks, starts)]
    first = starts[0] if starts else 0.0
    span = max(duration - first, 0.0)
    total = sum(len(m["w"]) + 1 for m in marks) or 1
    out, done = [], 0
    for m in marks:
        out.append(dict(m, t=round(first + span * done / total, 3)))
        done += len(m["w"]) + 1
    return out


def synthesize(text, out_path, voice, marks):
    """Speak `text` into `out_path`; return `marks` retimed to the speech.
    After one failure every later call fails at once, so a broken voice costs
    the render one wait, not one per segment."""
    from moviepy import AudioFileClip

    if _state["broken"]:
        raise RuntimeError(f"already failed this run ({_state['broken']})")
    try:
        ensure()
        home = _home()
        wav = Path(out_path).with_suffix(".standin.wav")
        job = {"text": text, "voice": VOICES.get(voice, "af_heart"), "out": str(wav),
               "model": str(home / "kokoro-v1.0.int8.onnx"),
               "voices": str(home / "voices-v1.0.bin")}
        result = json.loads(_run([str(_python()), str(WORKER)], input=json.dumps(job)).stdout)
        clip = AudioFileClip(str(wav))
        clip.write_audiofile(str(out_path), logger=None)
        clip.close()
        wav.unlink()
    except Exception as e:
        _state["broken"] = f"{type(e).__name__}: {e}"[:200]
        raise
    return word_marks(marks, result["starts"], result["duration"])
