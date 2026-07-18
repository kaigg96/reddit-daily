"""Normalize downloaded b-roll clips for the pipeline (PRD R1.3).

Takes any downloaded video, crops/scales to 1080x1920 vertical, strips audio,
caps length, and compresses to a repo-friendly size. Run once per new clip:

    venv/bin/python scripts/prep_broll.py ~/Downloads/clip.mp4 kinetic_sand

Output lands in assets/broll/<name>.mp4. Remember to add the source URL to
assets/CREDITS.md.
"""

import subprocess
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "broll"
MAX_SECONDS = 30


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, name = sys.argv[1], sys.argv[2]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{name}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", src,
            "-t", str(MAX_SECONDS),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,"
                   "crop=1080:1920,fps=30",
            "-c:v", "libx264", "-crf", "27", "-preset", "slow",
            "-an", "-movflags", "+faststart",
            str(out),
        ],
        check=True,
    )
    size_mb = out.stat().st_size / 1e6
    print(f"wrote {out} ({size_mb:.1f} MB)")
    if size_mb > 25:
        print("WARNING: over the 25 MB per-file budget (PRD constraint 8); "
              "trim the clip or raise CRF.")


if __name__ == "__main__":
    main()
