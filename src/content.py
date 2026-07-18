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


def select_post(reddit, prev_title, subreddit_name="AskReddit"):
    subreddit = reddit.subreddit(subreddit_name)
    top_post = next(
        (
            post
            for post in subreddit.top(time_filter="day", limit=10)
            if (
                not post.over_18
                and not profanity.contains_profanity(post.title)
                and len(post.title) <= config.MAX_TITLE_LENGTH
                and not _has_emoji(post.title)
                and post.title != prev_title
            )
        ),
        None,
    )
    if not top_post:
        raise ValueError("No suitable Reddit post found.")

    top_post.comment_sort = "top"
    top_post.comments.replace_more(limit=0)
    comments = [
        clean_text(c.body)
        for c in top_post.comments
        if (
            len(c.body) <= config.MAX_COMMENT_LENGTH
            and c.body not in ("[deleted]", "[removed]")
            and not _has_emoji(c.body)
            and not profanity.contains_profanity(c.body)
        )
    ][: config.NUM_COMMENTS]

    if len(comments) < config.NUM_COMMENTS:
        raise ValueError("Not enough valid comments found for video creation.")

    return PostContent(
        subreddit=subreddit_name,
        title=top_post.title,
        comments=comments,
        shortlink=top_post.shortlink,
    )
