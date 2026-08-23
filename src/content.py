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


def select_post(reddit, prev_title, subreddit_name="AskReddit", screener=None, on_verdict=None):
    """Pick the first candidate that passes the basic filters and the optional
    suppression screen. `screener(question, comments) -> ScreenResult`;
    `on_verdict(post_title, result, action)` records non-pass outcomes."""
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

    for post in candidates[: config.MAX_SCREENED_CANDIDATES]:
        pool = _comment_pool(post, config.COMMENT_POOL)
        if len(pool) < config.NUM_COMMENTS:
            continue

        if screener:
            result = screener(post.title, pool)
            if result.verdict == "skip_post":
                print(f"Screen: skipping post ({result.category}) — {post.title[:60]}")
                if on_verdict:
                    on_verdict(post.title, result, "skip_post")
                continue

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

        return PostContent(
            subreddit=subreddit_name,
            title=post.title,
            comments=pool[: config.NUM_COMMENTS],
            shortlink=post.shortlink,
        )

    raise ValueError("No suitable Reddit post found (after filters and screen).")
