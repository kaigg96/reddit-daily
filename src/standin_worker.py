"""Speak one text with Kokoro and print when each word starts (src/standin.py).

Runs in the stand-in voice's own environment, never the pipeline's: Kokoro
needs numpy 2 and the pipeline pins 1.26, so this file imports nothing from
src/. Reads {"text", "voice", "out", "model", "voices"} as JSON on stdin,
writes a WAV to "out", and prints {"starts": [...], "duration": s}: one start
per spoken group of phonemes, which matches the text's words when nothing (a
number, an abbreviation) was spoken as several.
"""
import json
import sys
import unicodedata


def word_starts(timings):
    """When each space-separated group of phonemes starts, skipping groups
    with no speech sound in them (a dash read as a pause), as Polly gives no
    mark for those."""
    starts, group = [], []
    for t in [*timings, None]:
        if t is None or t.phoneme == " ":
            if any(unicodedata.category(c).startswith("L") for p in group for c in p.phoneme):
                starts.append(round(float(group[0].start), 3))
            group = []
        else:
            group.append(t)
    return starts


def main():
    import soundfile as sf
    from kokoro_onnx import Kokoro

    job = json.load(sys.stdin)
    kokoro = Kokoro(job["model"], job["voices"])
    audio, rate, timings = kokoro.create_timed(job["text"], voice=job["voice"])
    sf.write(job["out"], audio, rate)
    json.dump({"starts": word_starts(timings), "duration": len(audio) / rate}, sys.stdout)


if __name__ == "__main__":
    main()
