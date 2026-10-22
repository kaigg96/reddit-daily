"""Speak one text with Kokoro and print when each word starts (src/standin.py).

Runs in the stand-in voice's own environment, never the pipeline's: Kokoro
needs numpy 2 and the pipeline pins 1.26, so this file imports nothing from
src/. Reads {"text", "voice", "out", "model", "voices"} as JSON on stdin,
writes a WAV to "out", and prints {"starts": [...], "duration": s}: one start
per space-separated group of phonemes, which matches the text's words when
nothing (a number, an abbreviation) was spoken as several.
"""
import json
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

TAIL = 0.3   # as the silent stand-in: a breath after the last word


def main():
    job = json.load(sys.stdin)
    kokoro = Kokoro(job["model"], job["voices"])
    audio, rate, timings = kokoro.create_timed(job["text"], voice=job["voice"])
    starts, in_word = [], False
    for t in timings:
        if t.phoneme == " ":
            in_word = False
        elif not in_word:
            starts.append(round(float(t.start), 3))
            in_word = True
    audio = np.concatenate([audio, np.zeros(int(TAIL * rate), dtype=audio.dtype)])
    sf.write(job["out"], audio, rate)
    json.dump({"starts": starts, "duration": len(audio) / rate}, sys.stdout)


if __name__ == "__main__":
    main()
