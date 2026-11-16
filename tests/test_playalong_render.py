"""The play-along render plan (src/playalong_render.py): timings, order, and
that every revealed string is the episode's own."""
import copy

import pytest

from src import playalong, playalong_render as pr

EPISODES, _ = playalong.select_day(playalong.candidates(), "", [])


def _by_style(items, style):
    return [it for it in items if it[3] == style]


@pytest.mark.parametrize("episode", EPISODES, ids=lambda e: e["beat"])
def test_the_plan_runs_12_to_15_seconds_and_ends_on_the_reveal(episode):
    items = pr.plan(episode)
    assert items[0][0] == 0.0
    total = max(end for _, end, _, _ in items)
    assert 12.0 <= total <= 15.0
    for start, end, _, _ in items:
        assert 0.0 <= start < end <= total
    (answer,) = _by_style(items, "answer")
    # The reveal is last: it holds to the end and starts after the hook and
    # the countdown are gone.
    assert answer[1] == total
    assert all(end <= answer[0] for _, end, _, style in items
               if style in ("hook", "option_a", "option_b", "beat", "count"))
    assert 4.0 <= total - answer[0]
    (tomorrow,) = _by_style(items, "tomorrow")
    assert tomorrow[1] == total and 0.5 <= total - tomorrow[0] <= 1.5


@pytest.mark.parametrize("episode", EPISODES, ids=lambda e: e["beat"])
def test_the_countdown_shows_3_2_1_one_per_second(episode):
    counts = _by_style(pr.plan(episode), "count")
    assert [t for _, _, t, _ in counts] == ["3", "2", "1"]
    for (s1, e1, _, _), (s2, _, _, _) in zip(counts, counts[1:]):
        assert e1 == s2 and e1 - s1 == pytest.approx(1.0)
    (beat,) = _by_style(pr.plan(episode), "beat")
    assert beat[2] == episode["beat"]
    assert (beat[0], beat[1]) == (counts[0][0], counts[-1][1])
    (hook,) = _by_style(pr.plan(episode), "hook")
    assert hook[2] == episode["hook"] and hook[1] >= counts[-1][1]   # question held


@pytest.mark.parametrize("episode", EPISODES, ids=lambda e: e["beat"])
def test_the_revealed_text_is_the_episodes_own(episode):
    items = pr.plan(episode)
    for field in ("answer", "comparison", "turn", "tomorrow", "credit"):
        (it,) = _by_style(items, field)
        assert it[2] == episode[field]


def test_an_altered_answer_shows_on_screen_as_altered():
    episode = copy.deepcopy(EPISODES[0])
    original = pr.plan(episode)
    episode["answer"], episode["comparison"] = "$9.99", "×2.0"
    (answer,) = _by_style(pr.plan(episode), "answer")
    (comparison,) = _by_style(pr.plan(episode), "comparison")
    assert answer[2] == "$9.99" and comparison[2] == "×2.0"
    assert _by_style(original, "answer")[0][2] == EPISODES[0]["answer"] != "$9.99"


def test_a_pick_shows_its_two_options_as_labelled_blocks():
    pick = next(e for e in EPISODES if e["options"])
    blocks = _by_style(pr.plan(pick), "option_a") + _by_style(pr.plan(pick), "option_b")
    assert [t for _, _, t, _ in blocks] == [f"A  {pick['options'][0]}",
                                           f"B  {pick['options'][1]}"]
    number = next(e for e in EPISODES if not e["options"])
    assert not _by_style(pr.plan(number), "option_a")
