"""One-time generator for transition SFX (PRD R1.6).

Synthesizes short "whoosh" sounds from white noise pushed through a
time-varying state-variable bandpass filter, so the committed SFX are
original works with no licensing concerns. Outputs land in assets/sfx/
and are committed; this script is not run in CI.

Usage: venv/bin/python scripts/make_sfx.py
"""

import math
from pathlib import Path

import numpy as np
from pydub import AudioSegment

SR = 44100
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "sfx"


def whoosh(duration_s, f_start, f_end, q=1.6, gain=0.7, seed=0):
    """Noise through a bandpass whose center frequency sweeps f_start->f_end."""
    n = int(SR * duration_s)
    rng = np.random.default_rng(seed)
    noise = rng.uniform(-1.0, 1.0, n)

    # Exponential frequency sweep sounds more natural than linear
    sweep = f_start * (f_end / f_start) ** (np.arange(n) / n)

    low = band = 0.0
    out = np.empty(n)
    for i in range(n):
        f_coef = 2.0 * math.sin(math.pi * sweep[i] / SR)
        low += f_coef * band
        high = noise[i] - low - q * band
        band += f_coef * high
        out[i] = band

    # sin^2 fade envelope: quick rise, longer tail
    attack = int(n * 0.35)
    env = np.ones(n)
    env[:attack] = np.sin(np.linspace(0, math.pi / 2, attack)) ** 2
    env[attack:] = np.cos(np.linspace(0, math.pi / 2, n - attack)) ** 2
    out *= env

    out *= gain / max(1e-9, np.abs(out).max())
    return out


def export(samples, name):
    pcm = (samples * 32767).astype(np.int16)
    seg = AudioSegment(pcm.tobytes(), frame_rate=SR, sample_width=2, channels=1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.mp3"
    seg.export(path, format="mp3", bitrate="128k")
    print(f"wrote {path} ({seg.duration_seconds:.2f}s)")


if __name__ == "__main__":
    export(whoosh(0.32, 250, 2600, seed=1), "whoosh_up")
    export(whoosh(0.30, 2200, 320, seed=2), "whoosh_down")
    export(whoosh(0.38, 420, 1400, q=1.2, gain=0.55, seed=3), "whoosh_soft")
