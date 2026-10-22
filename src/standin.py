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
import subprocess
import sys
import urllib.request
from pathlib import Path

from . import config

# The whole environment, pinned as it was first tested (2026-10-22), so a
# release that morning cannot change what the owner hears.
PACKAGES = [
    "kokoro-onnx==0.6.1", "soundfile==0.14.0", "numpy==2.5.4", "onnxruntime==1.31.0",
    "phonemizer==3.4.0", "espeakng-loader==0.2.4", "attrs==26.1.0", "cffi==2.1.1",
    "cloudpickle==3.1.2", "dlinfo==2.0.0", "flatbuffers==25.12.19", "joblib==1.6.0",
    "packaging==26.3", "protobuf==7.36.2", "pycparser==3.11", "typing_extensions==4.16.0",
]
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


def _home():
    return config.GEN / "standin"


def _python():
    return _home() / "venv" / "bin" / "python"


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ensure():
    """Install the voice once per machine; raise if any part cannot be had."""
    home = _home()
    home.mkdir(parents=True, exist_ok=True)
    if not _python().exists():
        subprocess.run([sys.executable, "-m", "venv", str(home / "venv")],
                       check=True, timeout=120)
        subprocess.run([str(_python()), "-m", "pip", "install", "-q", *PACKAGES],
                       check=True, timeout=300)
    for name, (url, digest) in FILES.items():
        path = home / name
        if path.exists() and _digest(path) == digest:
            continue
        urllib.request.urlretrieve(url, path)
        if _digest(path) != digest:
            path.unlink()
            raise RuntimeError(f"{name} does not match its pinned digest")


def word_marks(marks, starts, duration):
    """Polly-shaped marks with the stand-in's times.

    `marks` are the evenly paced ones (src/sample.py), whose byte offsets stay.
    When the voice spoke as many words as the text has, each takes its own
    start. Otherwise (a number read as several words) the spoken span is
    shared out by length, so the last word still ends with the speech.
    """
    if len(starts) == len(marks):
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
    """Speak `text` into `out_path`; return `marks` retimed to the speech."""
    from moviepy import AudioFileClip

    ensure()
    home = _home()
    wav = Path(out_path).with_suffix(".standin.wav")
    job = {"text": text, "voice": VOICES.get(voice, "af_heart"), "out": str(wav),
           "model": str(home / "kokoro-v1.0.int8.onnx"),
           "voices": str(home / "voices-v1.0.bin")}
    done = subprocess.run([str(_python()), str(WORKER)], input=json.dumps(job),
                          capture_output=True, text=True, check=True, timeout=300)
    result = json.loads(done.stdout)
    clip = AudioFileClip(str(wav))
    clip.write_audiofile(str(out_path), logger=None)
    clip.close()
    wav.unlink()
    # The tail of silence the worker adds is not speech.
    return word_marks(marks, result["starts"], result["duration"] - 0.3)
