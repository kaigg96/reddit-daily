"""Render a play-along episode (the dict `playalong.select` returns) to a
silent 1080x1920 30 fps MP4. Narration comes later.

The shape: the hook (for a pick, the two options as labelled blocks), then the
beat line with the question held over a 3-2-1 countdown, then the reveal to
the end (answer, comparison, turn), with `tomorrow` over the last second.

Everything drawn goes through `plan(episode)`, a pure function, so a test can
check every string on screen is the episode's own without rendering video.
The live Reddit pipeline is untouched: this only reuses its text and
background helpers.
"""
import random

import numpy as np

from . import config

HOOK_END = 3.0                    # hook alone, 0-3 s
COUNT_FROM = 3                    # the beat: 3, 2, 1, one per second
REVEAL_START = HOOK_END + COUNT_FROM
TOTAL = 12.5                      # reveal 6.5 s, the last 1.2 s with tomorrow
TOMORROW_START = TOTAL - 1.2
LABELS = ("A", "B")

# style -> (font size, y, colour, width)
STYLES = {
    "hook": (76, 260, "white", 920),
    "option": (104, None, "white", 880),
    "beat": (92, 1180, config.BRAND_ORANGE, config.CAPTION_WIDTH),
    "count": (340, 1300, "white", config.CAPTION_WIDTH),
    "answer": (210, 520, config.BRAND_ORANGE, config.CAPTION_WIDTH),
    "comparison": (78, 880, "white", config.CAPTION_WIDTH),
    "turn": (58, 1200, "white", 900),
    "tomorrow": (60, 1460, config.BRAND_ORANGE, 900),
    "credit": (30, 1720, "white", 900),
}
OPTION_Y = {"option_a": 640, "option_b": 900}
OPTION_BOX_H = 210


def plan(episode):
    """[(start, end, text, style)] for every piece of text on screen, in
    start order. Text is copied from `episode` unchanged; the only text this
    adds is the countdown digits and the option labels' letters."""
    items = [(0.0, REVEAL_START, episode["hook"], "hook")]
    for label, option, style in zip(LABELS, episode.get("options") or [], OPTION_Y):
        items.append((0.0, REVEAL_START, f"{label}  {option}", style))
    items.append((HOOK_END, REVEAL_START, episode["beat"], "beat"))
    for i in range(COUNT_FROM):
        start = HOOK_END + i
        items.append((start, start + 1.0, str(COUNT_FROM - i), "count"))
    items += [(REVEAL_START, TOTAL, episode["answer"], "answer"),
              (REVEAL_START, TOTAL, episode["comparison"], "comparison"),
              (REVEAL_START, TOTAL, episode["turn"], "turn"),
              (REVEAL_START, TOTAL, episode["credit"], "credit"),
              (TOMORROW_START, TOTAL, episode["tomorrow"], "tomorrow")]
    return sorted(items, key=lambda it: it[0])


def _clips(items):
    from moviepy import ColorClip
    from .video import overlay_text

    out = []
    for start, end, text, style in items:
        if style in OPTION_Y:
            size, _, colour, width = STYLES["option"]
            y = OPTION_Y[style]
            box = (ColorClip((width + 80, OPTION_BOX_H), color=(20, 20, 20))
                   .with_opacity(0.7).with_start(start).with_duration(end - start)
                   .with_position(("center", y)))
            out += [box, overlay_text(text, start, end - start, size, y + 20,
                                      color=colour, width=width)]
            continue
        size, y, colour, width = STYLES[style]
        out.append(overlay_text(text, start, end - start, size, y, color=colour, width=width))
    return out


def silent_audio(duration, fps=44100):
    from moviepy.audio.AudioClip import AudioArrayClip
    return AudioArrayClip(np.zeros((int(duration * fps), 2)), fps=fps)


def build(episode, seed=0):
    """The episode as a moviepy clip: background, the plan's text, silence."""
    from moviepy import CompositeVideoClip
    from .background import build_background

    items = plan(episode)
    total = max(end for _, end, _, _ in items)
    bg, _ = build_background(total, random.Random(seed))
    video = CompositeVideoClip(bg + _clips(items), size=(config.W, config.H))
    return video.with_duration(total).with_audio(silent_audio(total))


def render(episode, out_path, seed=0):
    from .video import render as write
    video = build(episode, seed)
    write(video, out_path)
    video.close()
    return out_path
