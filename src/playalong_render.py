"""Render a play-along episode (the dict `playalong.select` returns) to a
silent 1080x1920 30 fps MP4. Narration comes later.

The shape: the hook (for a pick, the two options as labelled blocks), then the
beat line with the question held over a 3-2-1 countdown, then the reveal
(answer and one comparison) for the last 3 s of 9 s, so it starts at
two-thirds. `turn` is left for narration; `tomorrow` and `credit` go in the
description (`description(episode)`), not on screen.

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
TOTAL = REVEAL_START + 3.0        # the video ends 3 s after the reveal
LABELS = ("A", "B")
# YouTube's caption and channel name cover the bottom 15% of a Short.
SAFE_BOTTOM = 0.85 * config.H

# style -> (font size, y, colour, width, max lines). On screen: answer and
# ONE comparison. `turn` is left for narration and `tomorrow`/`credit` for the
# description: the reveal is 3 s, too short to read a third line.
STYLES = {
    "hook": (76, 260, "white", 920, 4),
    "option": (104, None, "white", 880, 1),
    "beat": (92, 1150, config.BRAND_ORANGE, config.CAPTION_WIDTH, 1),
    "count": (280, 1270, "white", config.CAPTION_WIDTH, 1),
    "answer": (210, 520, config.BRAND_ORANGE, config.CAPTION_WIDTH, 1),
    "comparison": (84, 880, "white", config.CAPTION_WIDTH, 2),
}
LINE_H = 1.25                     # a text line's height per point of font size
OPTION_Y = {"option_a": 640, "option_b": 900}
OPTION_BOX_H = 210


def bottom(style):
    """The lowest pixel a style's text can reach."""
    if style in OPTION_Y:
        return OPTION_Y[style] + OPTION_BOX_H
    size, y, _, _, lines = STYLES[style]
    return y + size * LINE_H * lines


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
              (REVEAL_START, TOTAL, episode["comparison"], "comparison")]
    return sorted(items, key=lambda it: it[0])


def description(episode):
    """The text that goes under the video instead of on it."""
    return f"{episode['tomorrow']}\n\n{episode['credit']}"


def _clips(items):
    from moviepy import ColorClip
    from .video import overlay_text

    out = []
    for start, end, text, style in items:
        if style in OPTION_Y:
            size, _, colour, width, _ = STYLES["option"]
            y = OPTION_Y[style]
            box = (ColorClip((width + 80, OPTION_BOX_H), color=(20, 20, 20))
                   .with_opacity(0.7).with_start(start).with_duration(end - start)
                   .with_position(("center", y)))
            out += [box, overlay_text(text, start, end - start, size, y + 20,
                                      color=colour, width=width)]
            continue
        size, y, colour, width, _ = STYLES[style]
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
