"""Branded thumbnail card (PRD R2.3), rendered with Pillow over a darkened
frame pulled from the video's background — independent of the MoviePy
assembly path in video.py."""

from PIL import Image, ImageDraw, ImageFont

from . import config


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
