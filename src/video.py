"""Video assembly: single continuous timeline, no gap clips (PRD R1.1),
word-timed karaoke captions (R1.2), motion background (R1.3), readability
layer (R1.4), header + progress badge (R1.5), SFX + music (R1.6)."""

import math
import random
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
    VideoFileClip,
    afx,
    vfx,
)

from . import config


@dataclass
class Segment:
    kind: str  # 'title' | 'comment' | 'outro'
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


def caption_clips(groups, seg_start, font_size, y):
    clips = []
    for g in groups:
        clip = (
            _text_clip(g.text.upper(), font_size)
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


# ---------------------------------------------------------------- background


def _procedural_frame_function(rng):
    """Dark drifting-glow background: never a static frame (PRD R1.3 fallback).

    Computed at half resolution and pixel-doubled; the glows are smooth enough
    that the upscale is invisible after encoding.
    """
    w2, h2 = config.W // 2, config.H // 2
    xx, yy = np.meshgrid(np.linspace(0, 1, w2), np.linspace(0, 1, h2))

    base_top = np.array([14, 14, 20], dtype=np.float32)
    base_bot = np.array([30, 24, 44], dtype=np.float32)
    base = base_top[None, None, :] + yy[:, :, None] * (base_bot - base_top)[None, None, :]

    cx, cy = (xx - 0.5), (yy - 0.5)
    vignette = (1.0 - 0.35 * (cx * cx + cy * cy) / 0.5)[:, :, None]

    orbs = []
    palette = [
        (np.array([255, 93, 1], dtype=np.float32), 0.55),   # brand orange
        (np.array([255, 150, 40], dtype=np.float32), 0.35),
        (np.array([90, 70, 220], dtype=np.float32), 0.45),  # violet accent
    ]
    for color, alpha in palette:
        orbs.append({
            "color": color, "alpha": alpha,
            "sigma": rng.uniform(0.16, 0.24),
            "ax": rng.uniform(0.25, 0.42), "ay": rng.uniform(0.20, 0.35),
            "tx": rng.uniform(9, 16), "ty": rng.uniform(11, 19),
            "px": rng.uniform(0, 2 * math.pi), "py": rng.uniform(0, 2 * math.pi),
        })

    dither = np.random.default_rng(0).uniform(-1.5, 1.5, (h2, w2, 1)).astype(np.float32)

    def frame_function(t):
        frame = base.copy()
        for o in orbs:
            ox = 0.5 + o["ax"] * math.sin(2 * math.pi * t / o["tx"] + o["px"])
            oy = 0.5 + o["ay"] * math.sin(2 * math.pi * t / o["ty"] + o["py"])
            d2 = (xx - ox) ** 2 + ((yy - oy) * (config.H / config.W)) ** 2
            glow = np.exp(-d2 / (2 * o["sigma"] ** 2)).astype(np.float32)
            frame += glow[:, :, None] * o["color"][None, None, :] * o["alpha"]
        frame = np.clip(frame * vignette + dither, 0, 255).astype(np.uint8)
        return np.repeat(np.repeat(frame, 2, axis=0), 2, axis=1)

    return frame_function


def build_background(duration, rng):
    """Returns (list of background layer clips, bg_name for the upload log)."""
    broll_files = sorted(Path(config.BROLL_DIR).glob("*.mp4"))
    if broll_files:
        path = rng.choice(broll_files)
        clip = VideoFileClip(str(path)).without_audio()
        if clip.duration >= duration + 0.5:
            start = rng.uniform(0, clip.duration - duration - 0.5)
            clip = clip.subclipped(start, start + duration)
        else:
            clip = clip.with_effects([vfx.Loop(duration=duration)])
        scale = max(config.W / clip.w, config.H / clip.h)
        clip = clip.resized(scale).cropped(
            x_center=clip.w * scale / 2, y_center=clip.h * scale / 2,
            width=config.W, height=config.H,
        )
        # scrim so white captions survive bright footage (R1.4)
        scrim = (
            ColorClip((config.W, config.H), color=(0, 0, 0))
            .with_opacity(0.35)
            .with_duration(duration)
        )
        return [clip.with_duration(duration), scrim], path.name

    seed = rng.randint(0, 2**31)
    frame_fn = _procedural_frame_function(random.Random(seed))
    clip = VideoClip(frame_function=frame_fn, duration=duration)
    return [clip], f"procedural:{seed}"


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


def _truncate(text, limit=80):
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def assemble(question, segments, rng):
    t = 0.0
    audio_clips, overlays, sfx_times = [], [], []
    n_answers = sum(1 for s in segments if s.kind == "comment")
    answer_i = 0
    first_comment_start = None

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

        if seg.kind == "title":
            overlays.append(overlay_text(config.CHANNEL_NAME, t, display_dur, 46, 120, color=config.BRAND_ORANGE))
            overlays.append(overlay_text("TODAY'S TOP QUESTION", t, display_dur, 58, 200))
            overlays += caption_clips(groups, t, font_size=130, y=640)
        elif seg.kind == "comment":
            answer_i += 1
            sfx_times.append(t)
            if first_comment_start is None:
                first_comment_start = t
            overlays.append(
                overlay_text(f"ANSWER {answer_i}/{n_answers}", t, display_dur, 56, 330, color=config.BRAND_ORANGE)
            )
            overlays += caption_clips(groups, t, font_size=112, y=700)
        else:  # outro
            overlays += caption_clips(groups, t, font_size=100, y=700)

        t += display_dur + config.INTER_SEGMENT_GAP

    total = t - config.INTER_SEGMENT_GAP + 0.35  # small tail so the last word breathes

    # The question stays pinned from the first answer to the end of the video;
    # only the ANSWER n/N badge swaps per answer.
    if first_comment_start is not None:
        overlays.append(
            overlay_text(_truncate(question), first_comment_start,
                         total - first_comment_start, 44, 120, width=920)
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
    )


def render(video, out_path):
    video.write_videofile(
        str(out_path), fps=config.FPS, codec="libx264", audio_codec="aac", threads=4
    )


# ---------------------------------------------------------------- thumbnail


def make_thumbnail(question, bg_frame, out_path):
    """Full-question card over a darkened background frame. Kept minimal so the
    channel-page browse surface doesn't regress vs. the old static title card."""
    img = Image.fromarray(bg_frame).convert("RGB")
    img = Image.eval(img, lambda px: int(px * 0.55))
    draw = ImageDraw.Draw(img)

    tag_font = ImageFont.truetype(config.FONT, 60)
    q_font = ImageFont.truetype(config.FONT, 110)

    def wrap(text, font, max_width):
        lines, line = [], ""
        for word in text.split():
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    draw.text(
        (config.W / 2, 340), config.CHANNEL_NAME, font=tag_font, fill=config.BRAND_ORANGE,
        anchor="mm", stroke_width=4, stroke_fill="black",
    )
    y = 480
    for line in wrap(question, q_font, config.W - 140):
        draw.text(
            (config.W / 2, y), line, font=q_font, fill="white",
            anchor="ma", stroke_width=8, stroke_fill="black",
        )
        y += 135

    img.save(out_path, format="PNG")
