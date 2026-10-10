"""Video assembly: single continuous timeline, no gap clips (PRD R1.1),
word-timed karaoke captions (R1.2), header + progress badge (R1.5), SFX +
music (R1.6). Background generation lives in background.py, the thumbnail
card in thumbnail.py — both independent concerns from this timeline."""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    TextClip,
    afx,
)

from . import config
from .background import build_background


@dataclass
class Segment:
    kind: str  # 'title' | 'comment' | 'host' | 'outro'
    text: str
    audio_path: str
    marks: list  # from tts.synthesize_with_marks


@dataclass
class WordGroup:
    start: float
    end: float
    text: str


# ---------------------------------------------------------------- captions


def group_words(marks, text, audio_duration, max_words=3, gap_split=0.6):
    """Chunk word marks into 1-3 word caption groups.

    New group on: max_words reached, a >gap_split pause, or sentence-ending
    punctuation (detected via the mark's byte offset into the utf-8 text,
    since Polly's 'value' excludes trailing punctuation).
    """
    if not marks:
        return [WordGroup(0.0, audio_duration, text)]

    text_bytes = text.encode("utf-8")

    def ends_sentence(mark):
        nxt = text_bytes[mark["end_offset"]: mark["end_offset"] + 1]
        return nxt in (b".", b"!", b"?", b",", b";", b":")

    raw_groups, current = [], []
    for i, mark in enumerate(marks):
        current.append(mark)
        next_mark = marks[i + 1] if i + 1 < len(marks) else None
        pause = next_mark and (next_mark["t"] - mark["t"]) > gap_split
        if len(current) == max_words or ends_sentence(mark) or pause or next_mark is None:
            raw_groups.append(current)
            current = []

    groups = []
    for i, g in enumerate(raw_groups):
        start = g[0]["t"]
        end = raw_groups[i + 1][0]["t"] if i + 1 < len(raw_groups) else audio_duration
        groups.append(WordGroup(start, end, " ".join(m["w"] for m in g)))
    return groups


def _text_clip(text, font_size, color="white", stroke_frac=0.075, width=config.CAPTION_WIDTH):
    stroke = max(2, int(font_size * stroke_frac))
    # margin keeps the stroke from clipping at the rendered image edge
    return TextClip(
        font=config.FONT,
        text=text,
        font_size=font_size,
        color=color,
        stroke_color="black",
        stroke_width=stroke,
        method="caption",
        size=(width, None),
        text_align="center",
        margin=(stroke * 4, stroke * 4),
    )


def caption_clips(groups, seg_start, font_size, y, color="white"):
    clips = []
    for g in groups:
        clip = (
            _text_clip(g.text.upper(), font_size, color=color)
            .with_start(seg_start + g.start)
            .with_duration(max(0.15, g.end - g.start))
            .with_position(("center", y))
        )
        clips.append(clip)
    return clips


def overlay_text(text, start, duration, font_size, y, color="white", width=config.CAPTION_WIDTH):
    return (
        _text_clip(text, font_size, color=color, width=width)
        .with_start(start)
        .with_duration(duration)
        .with_position(("center", y))
    )


# ---------------------------------------------------------------- audio


def _pick_music(duration, rng):
    """Returns (music AudioClip or None, track name). Library tracks get scaled
    down; the legacy fallback file is already ~13dB lower than source."""
    library = sorted(Path(config.MUSIC_DIR).glob("*.mp3"))
    if library:
        path, volume = rng.choice(library), config.MUSIC_VOLUME_LIBRARY
    elif config.FALLBACK_MUSIC.exists():
        path, volume = config.FALLBACK_MUSIC, config.MUSIC_VOLUME_FALLBACK
    else:
        return None, "none"

    music = AudioFileClip(str(path))
    if music.duration < duration:
        music = music.with_effects([afx.AudioLoop(duration=duration)])
    else:
        music = music.subclipped(0, duration)
    return music.with_volume_scaled(volume), path.name


# ---------------------------------------------------------------- assembly


@dataclass
class AssemblyResult:
    video: object
    duration: float
    bg_name: str
    music_name: str
    bg_frame: np.ndarray = field(repr=False, default=None)
    srt_events: list = field(default_factory=list)  # (start_s, end_s, text)


def _truncate(text, limit):
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _srt_ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((t % 1) * 1000):03d}"


def write_srt(events, path):
    """R3.5: subtitle track from the same word-group timings as the on-screen
    captions (original case, not the uppercased on-screen form)."""
    blocks = [
        f"{i}\n{_srt_ts(start)} --> {_srt_ts(end)}\n{text}\n"
        for i, (start, end, text) in enumerate(events, 1)
    ]
    Path(path).write_text("\n".join(blocks))


def assemble(question, segments, rng):
    t = 0.0
    audio_clips, overlays, sfx_times, srt_events = [], [], [], []
    n_answers = sum(1 for s in segments if s.kind == "comment")
    answer_i = 0

    for seg in segments:
        audio = AudioFileClip(seg.audio_path)
        dur = audio.duration
        audio_clips.append(audio.with_start(t))

        # Short answers stay up past the end of their narration; captions and
        # badge span display_dur while the audio keeps its own timing.
        display_dur = dur
        if seg.kind == "comment":
            display_dur = max(dur, config.MIN_COMMENT_DISPLAY)
        groups = group_words(seg.marks, seg.text, display_dur)
        srt_events += [(t + g.start, t + g.end, g.text) for g in groups]  # R3.5

        if seg.kind == "title":
            overlays += caption_clips(groups, t, font_size=130, y=640)
        elif seg.kind == "comment":
            answer_i += 1
            sfx_times.append(t)
            overlays.append(
                overlay_text(f"ANSWER {answer_i}/{n_answers}", t, display_dur, 56, 330, color=config.BRAND_ORANGE)
            )
            overlays += caption_clips(groups, t, font_size=112, y=700)
        elif seg.kind == "host":  # bet 1 (#70): the host's own words
            overlays += caption_clips(groups, t, font_size=100, y=700,
                                      color=config.HOST_CAPTION_COLOR)
        else:  # outro
            overlays += caption_clips(groups, t, font_size=100, y=700)

        t += display_dur + config.INTER_SEGMENT_GAP

    total = t - config.INTER_SEGMENT_GAP + 0.35  # small tail so the last word breathes

    # v7: the question is pinned from the first frame to the last. The opening
    # second is where the Shorts feed (~97% of views) decides, so it shows the
    # hook rather than the channel name and a format label; the watermark below
    # still brands every frame. Only the ANSWER n/N badge swaps per answer.
    # Truncated only past the length selection already rejects: an opening that
    # cut the question's last word would be showing the hook without its point.
    overlays.append(
        overlay_text(_truncate(question, config.MAX_TITLE_LENGTH), 0, total, 44, 120, width=920)
    )

    # R3.4: persistent brand watermark, all frames, low in the safe area.
    overlays.append(
        _text_clip(config.CHANNEL_NAME, 34)
        .with_opacity(0.55)
        .with_start(0)
        .with_duration(total)
        .with_position(("center", 1500))
    )

    bg_clips, bg_name = build_background(total, rng)
    video = CompositeVideoClip(bg_clips + overlays, size=(config.W, config.H)).with_duration(total)

    sfx_files = sorted(Path(config.SFX_DIR).glob("*.mp3"))
    sfx_clips = []
    if sfx_files:
        for ts in sfx_times:
            sfx = AudioFileClip(str(rng.choice(sfx_files))).with_volume_scaled(config.SFX_VOLUME)
            sfx_clips.append(sfx.with_start(max(0.0, ts - 0.08)))

    music, music_name = _pick_music(total, rng)
    mix = audio_clips + sfx_clips + ([music] if music else [])
    video = video.with_audio(CompositeAudioClip(mix).with_duration(total))

    return AssemblyResult(
        video=video,
        duration=total,
        bg_name=bg_name,
        music_name=music_name,
        bg_frame=bg_clips[0].get_frame(min(1.0, total / 2)),
        srt_events=srt_events,
    )


def render(video, out_path):
    video.write_videofile(
        str(out_path), fps=config.FPS, codec="libx264", audio_codec="aac", threads=4
    )
