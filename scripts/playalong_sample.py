"""Render every play-along episode the day's selector makes, from the
committed records, to assets/gen/playalong_<template>.mp4 (gitignored), with
three PNG frames each (hook, mid-countdown, reveal). Local only: no model,
no TTS, no network, no upload.

    venv/bin/python scripts/playalong_sample.py [--price APU0000703112 | --supply] [--narrate]

`--supply` renders the first episode of each template `playalong.supply()`
ships instead, the set the viewer bar judges before the arm goes live (E1 T15).

`--narrate` reads it with the sample voice (STAND_IN_VOICE=1 for the free
stand-in; else silence of the estimated length; never Polly) and times the
screens and stills from what was said.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import config, playalong, playalong_render as pr  # noqa: E402


def frames(episode, said=None):
    """When to grab each still: mid-hook, mid-countdown, mid-reveal."""
    t = pr.timings(episode, said)
    return {"hook": t["hook_end"] / 2, "countdown": t["count_start"] + pr.COUNT_FROM / 2,
            "reveal": (t["reveal_start"] + t["total"]) / 2}


FFMPEG = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()


def probe(path):
    """Size, frame rate, duration and audio streams: ffprobe when installed,
    else the stream report of the ffmpeg moviepy bundles (no ffprobe there)."""
    if not shutil.which("ffprobe"):
        from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos
        i = ffmpeg_parse_infos(str(path))
        w, h = i["video_size"]
        return (f"{w}x{h} {i['video_fps']:g} fps {i['duration']:.2f}s "
                f"audio streams: {int(i['audio_found'])} (ffmpeg -i; no ffprobe on PATH)")
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True)
    info = json.loads(out.stdout)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    audio = [s for s in info["streams"] if s["codec_type"] == "audio"]
    return (f"{video['width']}x{video['height']} {video['r_frame_rate']} fps "
            f"{float(info['format']['duration']):.2f}s audio streams: {len(audio)}")


def main():
    config.GEN.mkdir(parents=True, exist_ok=True)
    # `--price APU0000703112` renders another BLS series on file (ground beef).
    price = sys.argv[sys.argv.index("--price") + 1] if "--price" in sys.argv else playalong.GAS_SERIES
    cands = playalong.supply() if "--supply" in sys.argv else playalong.candidates(price)
    episodes, _ = playalong.select_day(cands, shipped=[] if "--supply" in sys.argv else None)
    by_hook = {playalong._frame(c["template"], c["records"])["hook"]: c["template"]
               for c in cands}
    done = set()
    for episode in episodes:
        template = by_hook[episode["hook"]]
        if template in done:   # one file per template: the first of each
            continue
        done.add(template)
        out = config.GEN / f"playalong_{template}.mp4"
        narration = pr.narrate(episode, "Danielle") if "--narrate" in sys.argv else None
        said = None
        if narration:
            from moviepy import AudioFileClip
            said = {k: AudioFileClip(str(p)).duration for k, p in narration.items()}
            print(f"  said: {pr.script(episode)} {said}")
        pr.render(episode, out, narration=narration)
        print(f"{out}: {probe(out)}")
        for start, end, text, style in pr.plan(episode, said):
            print(f"  {start:4.1f} - {end:4.1f} | {style}: {text!r}")
        print("  description: " + pr.description(episode).replace("\n", " / "))
        for name, t in frames(episode, said).items():
            png = config.GEN / f"playalong_{template}_{name}.png"
            subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(out),
                            "-frames:v", "1", str(png)], check=True)
            print(f"  frame {name} @ {t:.1f}s: {png}")


if __name__ == "__main__":
    main()
