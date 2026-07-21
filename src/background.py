"""Background layer selection for the timeline (PRD R1.3): real b-roll if
assets/broll/ has clips, otherwise a procedural drifting-glow animation so
the video is never a static frame."""

import math
import random
from pathlib import Path

import numpy as np
from moviepy import ColorClip, VideoClip, VideoFileClip, vfx

from . import config


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
