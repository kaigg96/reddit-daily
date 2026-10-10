"""Pipeline orchestrator. Entry point: python -m src.run

DRY_RUN=1 renders everything locally and prints the would-be upload metadata
without touching YouTube, prev_post.txt, or upload_log.csv (PRD R0.1).
"""

import datetime
import random
import sys

from moviepy import AudioFileClip

from . import config, content, llm, log, sample, screen, thumbnail, tts, video, youtube


def _probe_duration(path):
    clip = AudioFileClip(str(path))
    duration = clip.duration
    clip.close()
    return duration


def upload_text(subreddit, post_title, comments, shortlink, keywords, asker=""):
    """Description and tags naming the post's own subreddit (R4.1). Each
    author is credited by username where known (Reddit's attribution term,
    PLAN C15): the same in both subreddits, so rotation stays the only
    variable between them."""
    def by(name):
        return f" (u/{name})" if name else ""

    description = (
        f"Today's top {subreddit} post{', asked by u/' + asker if asker else ''}: {post_title}\n\n"
        f"Top Comments:\n"
        + "\n".join(f"{i}. {c}{by(getattr(c, 'author', ''))}" for i, c in enumerate(comments, 1))
        + f"\n\n{shortlink}\n#{subreddit} #Reddit #Shorts"
    )
    tags = ([subreddit] + (["Ask Reddit"] if subreddit == "AskReddit" else [])
            + ["Shorts", "Reddit", f"Top {subreddit} Post", f"Trending {subreddit}"]
            + keywords)
    return description, tags


def build_segments(post, outro_text, host, synth, host_voice):
    """The narration in order. With bet 1's host lines (#70): question, setup,
    then each answer followed by its reaction, then the host's vote. Without
    them, today's: question, the answers, the CTA."""
    segments = [synth("title", post.title, kind="title")]
    answers = post.comments[:len(host.reactions)] if host else post.comments
    if host:
        segments.append(synth("setup", host.setup, kind="host", speaker=host_voice))
    for i, comment in enumerate(answers, 1):
        segments.append(synth(f"comment_{i}", comment, kind="comment"))
        if host:
            segments.append(synth(f"reaction_{i}", host.reactions[i - 1], kind="host",
                                  speaker=host_voice))
    # The vote is the host's line, so it takes the host's voice and colour.
    segments.append(synth("outro", outro_text, kind="host" if host else "outro",
                          speaker=host_voice if host else None))
    return segments


def drop_last_answer(segments):
    """R1.7: drop the last answer, and the host's reaction to it with it, since
    a reaction to an answer nobody heard makes no sense. Returns the answer."""
    i = max(i for i, s in enumerate(segments) if s.kind == "comment")
    dropped = segments.pop(i)
    if i < len(segments) and segments[i].kind == "host":
        segments.pop(i)
    return dropped


def own_words_share(segments):
    """Bet 1's done-when (#70): the host's share of the narration's characters,
    as spoken. The question and the answers are Reddit's; the rest is ours."""
    ours = sum(len(s.text) for s in segments if s.kind == "host")
    total = sum(len(s.text) for s in segments)
    return f"{ours / total:.2f}" if total else ""


def check_channel_name():
    """Refuse a real upload without the channel's name.

    The name is a secret, so the public repo does not carry it. Without it the
    watermark and thumbnail would show a placeholder on a live video, which is
    worse than a missed upload."""
    if not config.DRY_RUN and not config.CHANNEL_NAME_SET:
        raise SystemExit("CHANNEL_NAME is not set: refusing to upload a video "
                         "branded with a placeholder. Add the CHANNEL_NAME secret.")


def main():
    rng = random.Random()
    print(f"DRY_RUN={config.DRY_RUN} SAMPLE={config.SAMPLE} "
          f"SILENT_NARRATION={config.SILENT_NARRATION} format={config.FORMAT_VERSION}")
    check_channel_name()

    # --- content ---
    prev_title = ""
    if config.PREV_POST_FILE.exists():
        prev_title = config.PREV_POST_FILE.read_text().strip()
    subreddit_name = content.subreddit_for_run(datetime.datetime.now(datetime.timezone.utc))

    # R4.6: log every non-pass verdict for weekly false-positive audit.
    def record_verdict(post_title, result, action):
        row = {
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "subreddit": subreddit_name,
            "post_title": post_title,
            "action": action,
            # A demoted row's payload is the category we chose not to skip on.
            "category": result.demoted if action == "demoted_post_risk" else result.category,
            "reason": result.reason,
            "source": result.source,
            "dropped_comments": len(result.unsafe),
        }
        if config.DRY_RUN:
            print(f"  [dry run] screen_log row: {row}")
        else:
            log.append_screen_log(row)

    if config.SAMPLE:
        post = sample.POST
    else:
        post = content.select_post(
            content.make_reddit(), prev_title,
            subreddit_name=subreddit_name,
            screener=screen.screen, on_verdict=record_verdict,
            slate_classifier=screen.classify_slate,
            uploaded=log.uploaded_titles(),
        )
    print(f"Selected post: {post.title}")
    print(f"Slate topics (rank order): {post.slate_topics or '(not collected)'}")
    for i, c in enumerate(post.comments, 1):
        print(f"  comment {i}: {c}")

    # --- llm (fail-soft) ---
    # Each of these fails soft, so the run continues either way -- which is
    # exactly why the outcome has to be logged. Title fallbacks ran at ~25% for
    # two weeks in Sept 2026 and were only discoverable by comparing the shipped
    # title back to the Reddit question (PRD §2, TECH_DEBT 2026-09-19).
    # R2.2: one title style per day so both daily uploads share it; logged per upload
    title_style = llm.title_style_for(datetime.date.today())
    # PRD §0 #14: a coin per run, independent of the day's style.
    title_caps = llm.title_caps_arm(rng)

    # One request for all three fields. Each fails soft independently, so a
    # missing CTA doesn't cost us the title -- see llm.get_metadata.
    meta = (sample.METADATA if config.SAMPLE
            else llm.get_metadata(post.title, post.comments, style=title_style,
                                  caps=title_caps))

    keywords_ok = meta.keywords is not None
    keywords = meta.keywords or []

    video_title, title_style, title_ok = llm.resolve_title(
        meta.title, style=title_style, fallback=post.title)
    if not title_ok:
        print("Title generation failed — shipping the Reddit question and "
              "logging no style (it was never applied)")
    # Blank when the arm never applied, as the style is: a raw Reddit question
    # is not evidence about either arm.
    title_caps_logged = "" if not title_ok or config.SAMPLE else int(title_caps)
    print(f"Title style {title_style or '-'}, caps arm {title_caps_logged}: {video_title}")

    # Bet 1 (#70): the host's lines, or today's video if any is missing. The
    # flag is blank while bet 1 is off, as title_caps is when no arm applied.
    host = meta.commentary if config.COMMENTARY else None
    commentary_ok = int(host is not None) if config.COMMENTARY else ""
    if config.COMMENTARY and not host:
        print("Commentary: no usable host lines -- shipping today's reading")
    if host:
        print(f"Commentary setup: {host.setup}")
        for i, line in enumerate(host.reactions, 1):
            print(f"Commentary reaction {i}: {line}")

    # R3.1a: question-specific outro CTA (fail-soft to the generic line)
    cta_ok = meta.cta is not None
    outro_text = (host.verdict if host else meta.cta) or config.OUTRO_TEXT
    print(f"CTA: {outro_text}")

    # --- tts ---
    voice = rng.choice(config.VOICES)
    # R3.2: the host speaks in the voice the narrator is not using.
    host_voice = next(v for v in config.VOICES if v != voice)
    silent = config.SAMPLE or config.SILENT_NARRATION
    polly = None if silent else tts.make_polly()
    print(f"Narrator voice: {voice}" + (f", host voice: {host_voice}" if host else ""))

    def synth(name, text, kind, speaker=None):
        path = config.GEN / f"{name}.mp3"
        if silent:
            marks = sample.synthesize(text, path)
        else:
            marks = tts.synthesize_with_marks(polly, text, speaker or voice, path)
        return video.Segment(kind=kind, text=text, audio_path=str(path), marks=marks)

    segments = build_segments(post, outro_text, host, synth, host_voice)

    # --- duration guard (R1.7): drop the last comment rather than run long ---
    def projected(segs):
        def display(s):
            dur = _probe_duration(s.audio_path)
            return max(dur, config.MIN_COMMENT_DISPLAY) if s.kind == "comment" else dur
        return sum(display(s) for s in segs) + config.INTER_SEGMENT_GAP * (len(segs) - 1)

    if projected(segments) > config.MAX_TOTAL_SECONDS:
        dropped = drop_last_answer(segments)
        print(f"Duration guard: dropped comment '{dropped.text[:40]}...'")
    assert projected(segments) <= 60, "video must never exceed 60s"
    own_words = own_words_share(segments) if host else ""
    if host:
        print(f"Commentary: our own words are {own_words} of the narration")

    # --- assemble + render ---
    result = video.assemble(post.title, segments, rng)
    print(f"Assembled: {result.duration:.1f}s, bg={result.bg_name}, music={result.music_name}")
    video.render(result.video, config.OUT_VIDEO)
    thumbnail.make_thumbnail(post.title, result.bg_frame, config.OUT_THUMBNAIL)
    video.write_srt(result.srt_events, config.OUT_SRT)  # R3.5

    # --- upload metadata (R2.1: no hashtag suffix — Shorts are auto-detected) ---
    full_title = video_title
    description, tags = upload_text(
        post.subreddit, post.title,
        [s.text for s in segments if s.kind == "comment"], post.shortlink, keywords,
        asker=post.author)

    # R3.3: engagement comment posted from the channel account (the CTA doubles as it)
    comment_text = outro_text

    if config.DRY_RUN:
        print("\n=== DRY RUN — nothing uploaded ===")
        print(f"video:       {config.OUT_VIDEO}")
        print(f"thumbnail:   {config.OUT_THUMBNAIL}")
        print(f"captions:    {config.OUT_SRT}")
        print(f"title:       {full_title}")
        print(f"tags:        {tags}")
        print(f"comment:     {comment_text}")
        print(f"description:\n{description}")
        return

    video_id = youtube.upload_video(config.OUT_VIDEO, full_title, description, tags)
    if not video_id:
        sys.exit("Upload failed; not updating prev_post/upload_log.")
    youtube.upload_thumbnail(video_id, config.OUT_THUMBNAIL)
    caption_ok = youtube.upload_caption(video_id, config.OUT_SRT)  # R3.5, fail-soft
    comment_ok = youtube.post_comment(video_id, comment_text)      # R3.3, fail-soft
    print(f"Uploaded: {video_id}")

    config.PREV_POST_FILE.write_text(post.title)
    log.append_upload_log({
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "video_id": video_id,
        "subreddit": post.subreddit,
        "post_title": post.title,
        "video_title": full_title,
        "title_style": title_style,
        "voice": voice,
        "bg_clip": result.bg_name,
        "music_track": result.music_name,
        "format_version": config.FORMAT_VERSION,
        "duration_s": f"{result.duration:.1f}",
        "candidate_rank": post.candidate_rank,
        "topic": post.topic,
        "screen_source": post.screen_source,
        "slate_topics": post.slate_topics,
        "caption_ok": int(bool(caption_ok)),
        "comment_ok": int(bool(comment_ok)),
        "title_ok": int(title_ok),
        "keywords_ok": int(keywords_ok),
        "cta_ok": int(cta_ok),
        "meta_failure": meta.failure,
        "screen_failure": post.screen_failure,
        "title_caps": title_caps_logged,
        "commentary_ok": commentary_ok,
        "own_words_share": own_words,
    })


if __name__ == "__main__":
    main()
