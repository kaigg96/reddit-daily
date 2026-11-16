"""Render a play-along episode (the dict `playalong.select` returns) to a
silent 1080x1920 30 fps MP4. Narration comes later.

The shape: the hook (for a pick, the two options as labelled blocks), then the
beat line with the question held over a 3-2-1 countdown, then the reveal
(answer and one comparison). The screen follows the narration's length: the
hook holds for as long as it takes to say, the reveal for as long as the
answer and comparison take, and the reveal never starts before two-thirds of
the whole (`timings`). Narration is not rendered yet, so each length is an
estimate from the line's word count at `sample.WORDS_PER_SECOND`. `turn` is
left for narration; `tomorrow` and `credit` go in the description
(`description(episode)`), not on screen.

Everything drawn goes through `plan(episode)`, a pure function, so a test can
check every string on screen is the episode's own without rendering video.
The live Reddit pipeline is untouched: this only reuses its text and
background helpers.
"""
import random
from pathlib import Path

import numpy as np

from . import config
from .sample import WORDS_PER_SECOND

HOOK_MIN = 3.0                    # the hook alone holds at least 3 s
COUNT_FROM = 3                    # the beat: 3, 2, 1, one per second
REVEAL_MIN = 3.0                  # the reveal holds at least 3 s
LABELS = ("A", "B")
# YouTube's caption and channel name cover the bottom 15% of a Short.
SAFE_BOTTOM = 0.85 * config.H

# style -> (font size, y, colour, width, max lines). On screen: answer and
# ONE comparison. `turn` is left for narration and `tomorrow`/`credit` for the
# description: the reveal holds only as long as its two lines take to say,
# too short to read a third.
STYLES = {
    "hook": (76, 260, "white", 920, 4),
    "option": (104, None, "white", 880, 1),
    "beat": (92, 1150, config.BRAND_ORANGE, config.CAPTION_WIDTH, 1),
    "count": (280, 1240, "white", config.CAPTION_WIDTH, 1),
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


def spoken(text):
    """Estimated seconds to say `text`: its word count at narration pace."""
    return len(text.split()) / WORDS_PER_SECOND


def timings(episode):
    """{"hook_end", "reveal_start", "total"} in seconds, from the narration's
    estimated length. The hook holds for its spoken length (at least
    HOOK_MIN), the countdown follows it, and the reveal holds for the spoken
    answer and comparison (at least REVEAL_MIN). The answer must appear only
    in the last third, which holds when the lead-up is at least twice the
    reveal; so a long reveal holds the question longer, and the reveal then
    starts at exactly two-thirds. (Holding the reveal itself longer would
    pull its start further before two-thirds, not after.)"""
    reveal = max(REVEAL_MIN, spoken(f"{episode['answer']} {episode['comparison']}"))
    reveal_start = max(max(HOOK_MIN, spoken(episode["hook"])) + COUNT_FROM, 2 * reveal)
    return {"hook_end": reveal_start - COUNT_FROM, "reveal_start": reveal_start,
            "total": reveal_start + reveal}


def plan(episode):
    """[(start, end, text, style)] for every piece of text on screen, in
    start order. Text is copied from `episode` unchanged; the only text this
    adds is the countdown digits and the option labels' letters."""
    t = timings(episode)
    hook_end, reveal_start, total = t["hook_end"], t["reveal_start"], t["total"]
    items = [(0.0, reveal_start, episode["hook"], "hook")]
    for label, option, style in zip(LABELS, episode.get("options") or [], OPTION_Y):
        items.append((0.0, reveal_start, f"{label}  {option}", style))
    items.append((hook_end, reveal_start, episode["beat"], "beat"))
    # Each digit ends where the next starts, the last where the reveal does.
    ticks = [hook_end + i for i in range(COUNT_FROM)] + [reveal_start]
    for i in range(COUNT_FROM):
        items.append((ticks[i], ticks[i + 1], str(COUNT_FROM - i), "count"))
    items += [(reveal_start, total, episode["answer"], "answer"),
              (reveal_start, total, episode["comparison"], "comparison")]
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
    total = timings(episode)["total"]
    bg, _ = build_background(total, random.Random(seed))
    video = CompositeVideoClip(bg + _clips(items), size=(config.W, config.H))
    return video.with_duration(total).with_audio(silent_audio(total))


def render(episode, out_path, seed=0):
    """Write the episode to `out_path`. moviepy's temporary audio goes in
    assets/gen/ (gitignored), not the working directory, which is the repo
    root when a script runs this."""
    video = build(episode, seed)
    config.GEN.mkdir(parents=True, exist_ok=True)
    temp_audio = config.GEN / f"{Path(out_path).stem}_TEMP_audio.m4a"
    video.write_videofile(str(out_path), fps=config.FPS, codec="libx264", audio_codec="aac",
                          threads=4, temp_audiofile=str(temp_audio))
    video.close()
    return out_path
