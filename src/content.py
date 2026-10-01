"""Reddit content selection and text cleanup."""

import os
import re
from dataclasses import dataclass

import emoji
import praw
from better_profanity import profanity

from . import config

profanity.load_censor_words()


@dataclass
class PostContent:
    subreddit: str
    title: str
    comments: list  # cleaned comment strings
    shortlink: str
    candidate_rank: int = 1   # 1 = Reddit's own top-ranked eligible post
    topic: str = ""           # R4.3 taxonomy, from the screen call (free)
    screen_source: str = ""   # gemini | backstop — which path actually screened this
    screen_failure: str = ""  # why the screen fell back, blank when Gemini answered
    slate_topics: str = ""    # R4.4 Step 0.5: every eligible candidate's topic, rank order, "|"-joined; "!<why>" if the call failed


def make_reddit():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )


def clean_text(text):
    """Normalize reddit markup for TTS/captions: [a](b) links, *em*, `code`, newlines."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("*", "").replace("`", "").replace("~~", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _has_emoji(text):
    return any(emoji.is_emoji(ch) for ch in text)


def _comment_pool(post, limit):
    """Top comments passing the basic filters, larger than NUM_COMMENTS so the
    screen (R4.6) can drop individual answers and still backfill."""
    post.comment_sort = "top"
    post.comments.replace_more(limit=0)
    return [
        clean_text(c.body)
        for c in post.comments
        if (
            len(c.body) <= config.MAX_COMMENT_LENGTH
            and c.body not in ("[deleted]", "[removed]")
            and not _has_emoji(c.body)
            and not profanity.contains_profanity(c.body)
        )
    ][:limit]


def subreddit_for_run(now, subreddits=None):
    """R4.1: the subreddit this run draws from, deterministic per run.

    Morning and evening take consecutive entries and the start moves on a day
    each day, so every subreddit gets both slots over a rotation; indexing on
    runs alone would pin each of two subreddits to one slot, confounding the
    comparison with upload time."""
    subs = subreddits or config.SUBREDDITS
    return subs[(now.toordinal() + (now.hour >= 12)) % len(subs)]


def select_post(reddit, prev_title, subreddit_name="AskReddit", screener=None, on_verdict=None,
                slate_classifier=None):
    """Pick the first candidate that passes the basic filters and the optional
    suppression screen. `screener(question, comments) -> ScreenResult`;
    `on_verdict(post_title, result, action)` records non-pass outcomes.
    `slate_classifier(titles) -> [topic] | None` labels the eligible slate for
    telemetry only; its answer never influences which post is picked."""
    subreddit = reddit.subreddit(subreddit_name)
    candidates = [
        post
        for post in subreddit.top(time_filter="day", limit=config.CANDIDATE_LIMIT)
        if (
            not post.over_18
            and not profanity.contains_profanity(post.title)
            and len(post.title) <= config.MAX_TITLE_LENGTH
            and not _has_emoji(post.title)
            and post.title != prev_title
        )
    ]

    # R4.4 Step 0.5. Rank here is position in `candidates`, the same basis as
    # candidate_rank, so slate[candidate_rank - 1] is the selected post and its
    # agreement with the screen's topic comes free.
    slate_topics = ""
    if slate_classifier and candidates:
        try:
            slate = slate_classifier([p.title for p in candidates])
        except Exception as e:  # telemetry must never cost an upload
            print(f"Slate: classifier raised {type(e).__name__} (not logged this run)")
            # "!" + why, so a failed call is told apart from one that never ran
            slate_topics = "!" + getattr(e, "kind", type(e).__name__)
            slate = None
        if slate:
            slate_topics = "|".join(t or "?" for t in slate)

    for rank, post in enumerate(candidates[: config.MAX_SCREENED_CANDIDATES], 1):
        pool = _comment_pool(post, config.COMMENT_POOL)
        if len(pool) < config.NUM_COMMENTS:
            continue

        topic = screen_source = screen_failure = ""
        if screener:
            result = screener(post.title, pool)
            topic, screen_source = result.topic, result.source
            screen_failure = result.failure
            if result.verdict == "skip_post":
                print(f"Screen: skipping post ({result.category}) — {post.title[:60]}")
                if on_verdict:
                    on_verdict(post.title, result, "skip_post")
                continue

            # Answer-level category raised against the post: not a skip, but
            # recorded so the audit can see what the old taxonomy would have cost.
            if result.demoted and on_verdict:
                on_verdict(post.title, result, "demoted_post_risk")

            if result.unsafe:
                kept = [c for i, c in enumerate(pool) if i not in result.unsafe]
                if len(kept) < config.NUM_COMMENTS:
                    print(f"Screen: too few safe comments — {post.title[:60]}")
                    if on_verdict:
                        on_verdict(post.title, result, "skip_insufficient_comments")
                    continue
                print(f"Screen: dropped {len(result.unsafe)} comment(s) ({result.category})")
                if on_verdict:
                    on_verdict(post.title, result, "drop_comments")
                pool = kept

        if rank > 1:
            print(f"Selected candidate rank {rank} (earlier candidates filtered/screened out)")
        return PostContent(
            subreddit=subreddit_name,
            title=post.title,
            comments=pool[: config.NUM_COMMENTS],
            shortlink=post.shortlink,
            candidate_rank=rank,
            topic=topic,
            screen_source=screen_source,
            screen_failure=screen_failure,
            slate_topics=slate_topics,
        )

    raise ValueError("No suitable Reddit post found (after filters and screen).")
