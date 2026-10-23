"""Reddit content selection and text cleanup."""

import datetime
import os
import re
import types
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
    screen_source: str = ""   # gemini | groq | gemini_fallback | backstop — which path actually screened this
    screen_failure: str = ""  # why each route missed, main model first ("http_503;fallback_…;groq_…"), blank when it answered; read with screen_source
    slate_topics: str = ""    # R4.4 Step 0.5: every eligible candidate's topic, rank order, "|"-joined; "!<why>" if the call failed
    author: str = ""          # the question's author, for the description's credit ("" if not printable)


class Answer(str):
    """A cleaned comment that remembers its author, so the description can
    credit it (Reddit's attribution term, PLAN C15). Riding on the string
    keeps the name with its text through the screen's drops and the length
    guard, with no parallel list to keep in step; a plain str credits no one."""
    author = ""

    def __new__(cls, text, author=""):
        obj = super().__new__(cls, text)
        obj.author = author
        return obj


# Usernames run words together ("shitlord99"), which the whole-word check
# misses, so names are also searched for list words as substrings. Only words
# of 4+ letters: "len" would catch "Allen". An over-match costs one credit.
_NAME_WORDS = sorted({str(w) for w in profanity.CENSOR_WORDSET
                      if len(str(w)) >= 4 and str(w).isalpha()})


def credit_name(author):
    """A Reddit username we may print, else "". Names are untrusted input:
    deleted accounts and profane names are left uncredited."""
    name = str(getattr(author, "name", "") or "")
    if name in ("", "[deleted]", "[removed]"):
        return ""
    low = name.lower()
    if profanity.contains_profanity(re.sub(r"[_\-\d]+", " ", name)) or any(w in low for w in _NAME_WORDS):
        return ""
    return name


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


def sentence_case(text):
    """The host's vote, as posted in the channel's comment: the AI writes it
    all lower case ("raising my hand for yes. which gets your vote?", the
    2026-10-11 sample), so each sentence's first letter is capitalised when
    its first word is plain lower case, keeping "r/AskReddit" and "iPhone".
    The video's own lines are untouched: its captions are shown in capitals,
    and the host's notes are capitalised in video.note_clips."""
    def cap(m):
        word = m.group(2).rstrip(",;:.!?").replace("'", "").replace("’", "")  # "i'd", "don’t"
        plain = word.isalpha() and word.islower()
        return m.group(1) + (m.group(2)[:1].upper() + m.group(2)[1:] if plain else m.group(2))
    # The stop is looked behind, not matched, so "nope. which?" caps both.
    return re.sub(r"(^|(?<=[.!?])\s+)(\S+)", cap, text)


def _has_emoji(text):
    return any(emoji.is_emoji(ch) for ch in text)


# The library counts a straight quote or * as part of a word, so a quote or
# Reddit's *emphasis* touching a word hides it: "'alright fuckers'" passed,
# and on 2026-10-22 an upload went out titled with it. A contraction hides
# one too ("shit's"). So the text is checked again with edge marks spaced out,
# and each contracted word alone. Marks inside a word stay ("f**k" is a list
# word as written), and words are never split in place: the library reads
# neighbours together, so "he ll" reads "hell" and "he be" a slur.
_EDGE_MARKS = re.compile(r"(?<![A-Za-z*])['\"*]+|['\"*]+(?![A-Za-z*])")
_CONTRACTED = re.compile(r"([A-Za-z*]+)'(?:s|ll|re|ve|d|m|t)\b", re.IGNORECASE)


def _profane(text):
    return (profanity.contains_profanity(text)
            or profanity.contains_profanity(_EDGE_MARKS.sub(" ", text))
            or any(profanity.contains_profanity(m.group(1))
                   for m in _CONTRACTED.finditer(_EDGE_MARKS.sub(" ", text))))


def _comment_pool(post, limit):
    """Top comments passing the basic filters, larger than NUM_COMMENTS so the
    screen (R4.6) can drop individual answers and still backfill."""
    post.comment_sort = "top"
    post.comments.replace_more(limit=0)
    return [
        Answer(clean_text(c.body), credit_name(getattr(c, "author", None)))
        for c in post.comments
        if (
            len(c.body) <= config.MAX_COMMENT_LENGTH
            and c.body not in ("[deleted]", "[removed]")
            and not _has_emoji(c.body)
            and not _profane(c.body)
        )
    ][:limit]


# Bet 1 (#70, PRD R3.2): with commentary on, medical threads are skipped at
# selection. Drafts slipped facts and advice there even under prompt rules, and
# YouTube refuses AI personas advising on health. The screen's health-body
# label catches 1 of 83 uploads, so the title is checked too (2 of 165 by
# keyword). Broad on purpose: a wrong skip costs one candidate, not an upload.
_MEDICAL = re.compile(
    r"\b(doctors?|nurses?|hospitals?|medical|medicine|medications?|illness(es)?|"
    r"diseases?|cancer|symptoms?|diagnos\w*|surger(y|ies)|surgeons?|paramedics?|"
    r"ambulances?|911|chiropract\w*|therap(y|ies|ists?)|pharmac\w*|health)\b", re.I)
_MEDICAL_CAPS = re.compile(r"\b(ER|EMTs?)\b")  # case-folded, "er" is in "were"


def is_medical(title, topic=""):
    """True for a thread the host must not comment on (bet 1, #70)."""
    return (topic == "health-body" or bool(_MEDICAL.search(title))
            or bool(_MEDICAL_CAPS.search(title)))


def _medical_skip(title, on_verdict, why):
    print(f"Commentary: skipping a medical thread ({why}) — {title[:60]}")
    if on_verdict:
        on_verdict(title, types.SimpleNamespace(
            category="medical", reason=why, source="commentary", unsafe=(), demoted=""),
            # Not "skip_*": the weekly digest reads those as the screen's
            # verdicts to audit for false positives, and this is not one.
            "medical_excluded")


def subreddit_for_run(now, subreddits=None, schedule=""):
    """R4.1: the subreddit this run draws from, deterministic per run.

    Morning and evening take consecutive entries and the start moves on a day
    each day, so every subreddit gets both slots over a rotation; indexing on
    runs alone would pin each of two subreddits to one slot, confounding the
    comparison with upload time.

    Both this and llm.title_style_for key on the day number, and the style
    cycle's length is even, so with two subreddits each style position keeps
    one subreddit-to-slot pairing (style A days: NoStupidQuestions in the
    morning; C days: AskReddit). Subreddit-vs-subreddit and style-vs-style
    reads stay balanced; a style comparison *within* one subreddit is
    confounded with slot. At four a day each run takes the next entry, so
    no subreddit runs more than twice in a row."""
    subs = subreddits or config.SUBREDDITS
    day, slot = run_slot(now, schedule)
    live = live_slots()
    position = live.index(slot) if slot in live else slot // 2
    return subs[(day.toordinal() + position) % len(subs)]


def run_slot(now, schedule=""):
    """PRD §0 #4: (day, slot) of this run. The slot is the triggering cron
    line's (config.SLOT_CRONS), and so is the day: the 18:23 run can land
    after midnight, and it still belongs to the day it was scheduled for. A
    run no cron line names (today's '23 0,12' line, a manual run) keeps the
    clock's split: before noon is slot 0, after it slot 2."""
    slot = config.SLOT_CRONS.get(schedule)
    if slot is None:
        if schedule and schedule != config.LEGACY_CRON:
            # A line the code does not know must not fall to the clock: an
            # 06:23 run landing near noon would read as slot 2 and upload.
            raise ValueError(f"cron line {schedule!r} is not in config.SLOT_CRONS")
        return now.date(), (2 if now.hour >= 12 else 0)
    day = now.date()
    if now.hour < 6 * slot:
        day -= datetime.timedelta(days=1)
    return day, slot


def live_slots():
    """The slots that upload. At two a day, the two the schedule has always
    had, so turning four on changes nothing about them."""
    return (0, 1, 2, 3) if config.UPLOADS_PER_DAY == 4 else (0, 2)


def select_post(reddit, prev_title, subreddit_name="AskReddit", screener=None, on_verdict=None,
                slate_classifier=None, uploaded=frozenset()):
    """Pick the first candidate that passes the basic filters and the optional
    suppression screen. `screener(question, comments) -> ScreenResult`;
    `on_verdict(post_title, result, action)` records non-pass outcomes.
    `slate_classifier(titles) -> [topic] | None` labels the eligible slate for
    telemetry only; its answer never influences which post is picked.
    `uploaded` is every title already shipped (log.uploaded_titles): prev_title
    alone stops only a repeat of the last upload. Matching is on the title, so
    a question re-asked weeks later is refused too (one was, 2026-08-20): to a
    viewer it is the same video."""
    subreddit = reddit.subreddit(subreddit_name)
    candidates = []
    for post in subreddit.top(time_filter="day", limit=config.CANDIDATE_LIMIT):
        if post.title in uploaded and post.title != prev_title:
            print(f"Already uploaded, not a candidate: {post.title[:60]}")
        if (
            not post.over_18
            and not _profane(post.title)
            and len(post.title) <= config.MAX_TITLE_LENGTH
            and not _has_emoji(post.title)
            and post.title != prev_title
            and post.title not in uploaded
        ):
            candidates.append(post)

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

    examined = 0
    for rank, post in enumerate(candidates, 1):
        # Before the screen, and outside its cap: a thread skipped on its title
        # spends no request, so it must not cost the run a screened candidate.
        if config.COMMENTARY and is_medical(post.title):
            _medical_skip(post.title, on_verdict, "title")
            continue
        examined += 1
        if examined > config.MAX_SCREENED_CANDIDATES:
            break
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
            if config.COMMENTARY and is_medical("", topic):
                _medical_skip(post.title, on_verdict, "topic")
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
            author=credit_name(getattr(post, "author", None)),
        )

    raise ValueError("No suitable Reddit post found (after filters and screen).")
