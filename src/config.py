"""Central configuration. Importing this module loads .env (local dev only)."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_dotenv():
    """Populate os.environ from .env without overriding already-set vars.

    CI sets everything via Actions secrets; this only matters for local runs.
    """
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

DRY_RUN = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")

# --- video geometry / look ---
W, H, FPS = 1080, 1920, 30
BRAND_ORANGE = "#ff5d01"
CHANNEL_NAME = "AskReddit Shorts"
FONT = str(ROOT / "assets" / "fonts" / "Anton-Regular.ttf")

# --- audio mix (voice RMS is ~-25 dBFS; keep music ~9 dB and SFX ~10 dB below) ---
SFX_VOLUME = 0.15
MUSIC_VOLUME_LIBRARY = 0.18   # for normalized tracks dropped into assets/music/
MUSIC_VOLUME_FALLBACK = 0.40  # funk_bg_lower.mp3 is only ~2.5 dB under voice at 1.0

# Keep all text inside the Shorts UI safe area (PRD R1.2)
SAFE_X = 60
CAPTION_WIDTH = W - 2 * SAFE_X

# --- content limits ---
MAX_COMMENT_LENGTH = 150
MAX_TITLE_LENGTH = 90
NUM_COMMENTS = 3
MAX_TOTAL_SECONDS = 45  # R1.7: drop last comment if exceeded
INTER_SEGMENT_GAP = 0.15  # natural breath between segments; music covers it
MIN_COMMENT_DISPLAY = 2.0  # short answers hold on screen this long so they land

# --- pipeline metadata (R0.2) ---
FORMAT_VERSION = "v2"
TITLE_STYLE = "A"  # curiosity-rephrase; B/C variants arrive in Phase 2

VOICES = ["Danielle", "Stephen"]
OUTRO_TEXT = "Like, subscribe, and comment your answer below!"

# --- paths ---
ASSETS = ROOT / "assets"
GEN = ASSETS / "gen"  # per-run outputs, gitignored
BROLL_DIR = ASSETS / "broll"
MUSIC_DIR = ASSETS / "music"
SFX_DIR = ASSETS / "sfx"
FALLBACK_MUSIC = ASSETS / "funk_bg_lower.mp3"  # pre-lowered ~13dB; see CREDITS.md
OUT_VIDEO = GEN / "final_askreddit_video.mp4"
OUT_THUMBNAIL = GEN / "thumbnail.png"
PREV_POST_FILE = ROOT / "prev_post.txt"
UPLOAD_LOG = ROOT / "upload_log.csv"

GEN.mkdir(parents=True, exist_ok=True)
