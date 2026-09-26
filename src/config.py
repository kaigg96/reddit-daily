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

# SAMPLE=1 renders a fixed post over silent narration (src/sample.py): no
# Reddit, Gemini or Polly call. Always a dry run -- nothing it makes is real.
SAMPLE = os.environ.get("SAMPLE", "").lower() in ("1", "true", "yes")
DRY_RUN = SAMPLE or os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")

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

# --- candidate selection / suppression screen (R4.6) ---
CANDIDATE_LIMIT = 10          # top posts fetched per run
COMMENT_POOL = 8              # screened comments per candidate; NUM_COMMENTS survive
MAX_SCREENED_CANDIDATES = 4   # caps Gemini calls per run (worst case) for free-tier quota
# R4.4 Step 0.5: one batched topic call per run over every eligible candidate,
# logged so the ranker's firing rate is measurable before any selection logic
# ships. It runs on a different model from every other call here because the
# free tier is counted per model (our 429 names the quota
# GenerateRequestsPerDayPerProjectPerModel), so it spends that model's
# allowance, never the one titles and the screen share. $0 either way (#22).
SLATE_MODEL = "gemini-3.5-flash-lite"  # 2.5-flash-lite: 404 for this key since at least 2026-09-25

# --- pipeline metadata (R0.2) ---
FORMAT_VERSION = "v7"  # v7 = opens on the question, not the channel name + format label

# --- AWS Polly cost guard (the only billed service; see CLAUDE.md §1) ---
# Neural is $16/1M chars and every segment is synthesized twice (mp3 + speech
# marks), so characters bill double. A real run spends ~910 billed chars; the
# config caps above put the ceiling at ~1,260. The budget is per-process and
# sized at ~4x a worst-case run: generous for one video, nowhere near enough
# for a batch job. Raise it only for a deliberate, owner-approved bulk run
# (POLLY_CHAR_BUDGET=... in the environment), never to make an error go away.
POLLY_CHAR_BUDGET = int(os.environ.get("POLLY_CHAR_BUDGET", 5000))

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
OUT_SRT = GEN / "captions.srt"
PREV_POST_FILE = ROOT / "prev_post.txt"
UPLOAD_LOG = ROOT / "upload_log.csv"
SCREEN_LOG = ROOT / "analysis" / "screen_log.csv"  # R4.6 audit trail
ANALYTICS_SNAPSHOTS = ROOT / "analysis" / "analytics_snapshots.csv"  # R4.2 weekly series
TRAFFIC_LOG = ROOT / "analysis" / "traffic_sources.csv"  # R4.7 traffic-source series

GEN.mkdir(parents=True, exist_ok=True)
