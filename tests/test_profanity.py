"""The swear-word filter on post titles and answers (src/content.py).

The library's whole-word check misses a word with a quote mark or *emphasis*
touching it, or a contraction's suffix. On 2026-10-22 a post titled "Can I
legally start my will with 'alright fuckers'?" passed it, and the upload went
out under a title quoting it. These pin that case and the contractions the fix
must leave alone."""

import pytest

from src import content
from tests.test_screen import FakePost

LIVE_2026_10_22 = "Can I legally start my will with 'alright fuckers'?"


@pytest.mark.parametrize("text", [
    LIVE_2026_10_22,
    'Could YOUR Will Start with "Alright Fuckers"?',   # the title it went out under
    "That's some *shit* right there",                  # Reddit's emphasis
    "fuckers' last words",
    "**FUCK** that",
    "What's the most 'f**k it' moment you've had?",    # a censored word, quoted
    "For fuck's sake, what's the worst?",              # contractions hide one too
    "That shit's crazy",
    "That *shit's* crazy, **fuck's** sake",              # emphasis around a contraction
])
def test_a_quoted_or_emphasised_swear_word_is_caught(text):
    assert content._profane(text)


@pytest.mark.parametrize("text", [
    "What's something he'll never admit to his wife?",   # "he ll" reads as "hell"
    "Who're you rooting for this year?",                 # "who re" as "whore"
    "What does your boss think he'll be great at?",      # "he be" as a slur
    "Who'll ring the bell, and who's red?",
    "Don't you think the 80's were better?",
    "What's the **genuinely** best pizza, James' or the dogs'?",
    "Rock 'n' roll at 6 o'clock, ma'am",
    "What did your grandma call 'the good scissors'?",
    'Teachers, what was the "dumbest" excuse you heard?',
])
def test_quotes_and_contractions_alone_are_clean(text):
    assert not content._profane(text)


def test_the_2026_10_22_post_is_passed_over_for_the_next(monkeypatch):
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    clean = "What did your grandma call 'the good scissors'?"

    class Reddit:
        def subreddit(self, name):
            class S:
                def top(self, time_filter, limit):
                    return [FakePost(LIVE_2026_10_22), FakePost(clean)]
            return S()

    post = content.select_post(Reddit(), "")
    assert post.title == clean
    assert post.candidate_rank == 1   # the skipped post never held a rank


# --- the AI's own output ------------------------------------------------------

from src import llm


@pytest.mark.parametrize("text", [
    'Could YOUR Will Start with "Alright Fuckers"?',   # 2026-10-22, as shipped
    "Your Pets' Secret Drama? Tell Us! 🤫",             # 2026-09-01, as shipped
    "What the **f**k** is this?",                       # the emphasis strip would hide it
    "TREASON: When Is a President Too Far? 🇺🇸",        # a flag is two code points
    "Pick 1️⃣ or 2️⃣?",                                   # so is a keycap
])
def test_an_ai_field_with_a_swear_word_or_emoji_falls_back(text):
    assert llm._clean_published(text) is None


def test_a_reddit_answer_with_a_flag_counts_as_emoji_and_plain_marks_do_not():
    from src import content
    assert content._has_emoji("Delete social media 🇺🇸 stop spending")
    for plain in ("Top 10 #1 pick :) <3", "Reddit™ and © marks", ""):
        assert content._has_emoji(plain) is ("™" in plain), plain


def test_a_clean_ai_field_passes_with_its_quotes_stripped():
    assert llm._clean_published('"Would YOU Pay for This?"') == "Would YOU Pay for This?"


def test_a_refused_title_ships_the_screened_question_and_claims_no_style():
    r = llm.resolve_title(llm._clean_published('Could YOUR Will Start with "Alright Fuckers"?'),
                          "B", fallback="Can I legally start my will with a toast?")
    assert r.title == "Can I legally start my will with a toast?"
    assert (r.style, r.ok) == ("", False)


@pytest.mark.parametrize("reaction", ["Oh god", "Hell yes", "Damn, okay"])
def test_the_hosts_reactions_are_not_held_to_the_word_list(reaction):
    """The list holds "god", "hell" and "damn"; a host's wince is not swearing."""
    assert llm._clean_str(reaction) == reaction
