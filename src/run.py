"""Pipeline orchestrator. Entry point: python -m src.run

DRY_RUN=1 renders everything locally and prints the would-be upload metadata
without touching YouTube, prev_post.txt, or upload_log.csv (PRD R0.1).
"""

import datetime
import random
import sys

from moviepy import AudioFileClip

from . import config, content, llm, log, tts, video, youtube


def _probe_duration(path):
    clip = AudioFileClip(str(path))
    duration = clip.duration
    clip.close()
    return duration


def main():
    rng = random.Random()
    print(f"DRY_RUN={config.DRY_RUN} format={config.FORMAT_VERSION}")

    # --- content ---
    prev_title = ""
    if config.PREV_POST_FILE.exists():
        prev_title = config.PREV_POST_FILE.read_text().strip()
    post = content.select_post(content.make_reddit(), prev_title)
    print(f"Selected post: {post.title}")
    for i, c in enumerate(post.comments, 1):
        print(f"  comment {i}: {c}")

    # --- llm (fail-soft) ---
    keywords = llm.get_keywords(post.title, post.comments)
    video_title = llm.sanitize_title(
        llm.get_video_title(post.title, post.comments), fallback=post.title
    )

    # --- tts ---
    voice = rng.choice(config.VOICES)
    polly = tts.make_polly()
    print(f"Narrator voice: {voice}")

    def synth(name, text):
        path = config.GEN / f"{name}.mp3"
        marks = tts.synthesize_with_marks(polly, text, voice, path)
        return video.Segment(kind="", text=text, audio_path=str(path), marks=marks)

    segments = [synth("title", post.title)]
    segments[0].kind = "title"
    for i, comment in enumerate(post.comments, 1):
        seg = synth(f"comment_{i}", comment)
        seg.kind = "comment"
        segments.append(seg)
    outro = synth("outro", config.OUTRO_TEXT)
    outro.kind = "outro"
    segments.append(outro)

    # --- duration guard (R1.7): drop the last comment rather than run long ---
    def projected(segs):
        def display(s):
            dur = _probe_duration(s.audio_path)
            return max(dur, config.MIN_COMMENT_DISPLAY) if s.kind == "comment" else dur
        return sum(display(s) for s in segs) + config.INTER_SEGMENT_GAP * (len(segs) - 1)

    if projected(segments) > config.MAX_TOTAL_SECONDS:
        last_comment = max(i for i, s in enumerate(segments) if s.kind == "comment")
        dropped = segments.pop(last_comment)
        print(f"Duration guard: dropped comment '{dropped.text[:40]}...'")
    assert projected(segments) <= 60, "video must never exceed 60s"

    # --- assemble + render ---
    result = video.assemble(post.title, segments, rng)
    print(f"Assembled: {result.duration:.1f}s, bg={result.bg_name}, music={result.music_name}")
    video.render(result.video, config.OUT_VIDEO)
    video.make_thumbnail(post.title, result.bg_frame, config.OUT_THUMBNAIL)

    # --- upload metadata ---
    full_title = f"{video_title} #shorts #foryou"
    description = (
        f"Today's top AskReddit post: {post.title}\n\n"
        f"Top Comments:\n"
        + "\n".join(f"{i}. {s.text}" for i, s in enumerate(
            (s for s in segments if s.kind == "comment"), 1))
        + f"\n\n{post.shortlink}\n#AskReddit #RedditDaily #shorts #foryou"
    )
    tags = ["AskReddit", "Ask Reddit", "Shorts", "Reddit", "Top AskReddit Post",
            "Trending AskReddit"] + keywords

    if config.DRY_RUN:
        print("\n=== DRY RUN — nothing uploaded ===")
        print(f"video:       {config.OUT_VIDEO}")
        print(f"thumbnail:   {config.OUT_THUMBNAIL}")
        print(f"title:       {full_title}")
        print(f"tags:        {tags}")
        print(f"description:\n{description}")
        return

    video_id = youtube.upload_video(config.OUT_VIDEO, full_title, description, tags)
    if not video_id:
        sys.exit("Upload failed; not updating prev_post/upload_log.")
    youtube.upload_thumbnail(video_id, config.OUT_THUMBNAIL)
    print(f"Video live: https://www.youtube.com/watch?v={video_id}")

    config.PREV_POST_FILE.write_text(post.title)
    log.append_upload_log({
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "video_id": video_id,
        "subreddit": post.subreddit,
        "post_title": post.title,
        "video_title": full_title,
        "title_style": config.TITLE_STYLE,
        "voice": voice,
        "bg_clip": result.bg_name,
        "music_track": result.music_name,
        "format_version": config.FORMAT_VERSION,
        "duration_s": f"{result.duration:.1f}",
    })


if __name__ == "__main__":
    main()
