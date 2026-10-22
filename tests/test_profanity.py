"""The swear-word filter on post titles and answers (src/content.py).

The library's whole-word check misses a word with a quote mark or *emphasis*
touching it. On 2026-10-22 a post titled "Can I legally start my will with
'alright fuckers'?" passed it, and the upload went out under a title quoting
it. These pin that case and the contractions the fix must leave alone."""

import pytest

from src import content
from tests.test_screen import FakePost

LIVE_2026_10_22 = "Can I legally start my will with 'alright fuckers'?"


@pytest.mark.parametrize("text", [
    LIVE_2026_10_22,
    'Could YOUR Will Start with "Alright Fuckers"?',   # the title it went out under
    "That's some *shit* right there",                  # Reddit's emphasis
    "I said `shit` out loud",
    "fuckers' last words",
    "**FUCK** that",
])
def test_a_quoted_or_emphasised_swear_word_is_caught(text):
    assert content._profane(text)


@pytest.mark.parametrize("text", [
    "What's something he'll never admit to his wife?",   # "ll" is a list word once split
    "Who're you rooting for this year?",                 # so is "re"
    "Don't you think the 80's were better?",
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
