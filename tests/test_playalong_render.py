"""The play-along render plan (src/playalong_render.py): timings, order, and
that every revealed string is the episode's own."""
import copy
from pathlib import Path

import pytest

from src import config, playalong, playalong_render as pr, sample

# What select_day builds from the fixtures (the gas question alone: the
# Wyoming vs D.C. pick is under x2), plus a pick that clears x2, built here.
EPISODES, _ = playalong.select_day(playalong.candidates(), "", [])
_PICK = copy.deepcopy(playalong.candidates()[1])
_PICK["records"][1]["value"] = 1_200_000
PICK, _ = playalong.select(_PICK)
ALL = EPISODES + [PICK]


def _by_style(items, style):
    return [it for it in items if it[3] == style]


def _start(items, style):
    (it,) = _by_style(items, style)
    return it[0]


def _words(n):
    return " ".join(["word"] * n)


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_the_plan_runs_for_the_narrations_length_and_reveals_in_the_last_third(episode):
    items = pr.plan(episode)
    assert items[0][0] == 0.0
    total = max(end for _, end, _, _ in items)
    assert total == pr.timings(episode)["total"]
    for start, end, _, _ in items:
        assert 0.0 <= start < end <= total
    (answer,) = _by_style(items, "answer")
    # The reveal is last: it holds to the end, starts after the hook and the
    # countdown are gone, at or after two-thirds, and holds as long as the
    # answer and comparison take to say (3 s at least).
    assert answer[1] == total
    assert all(end <= answer[0] for _, end, _, style in items
               if style in ("hook", "option_a", "option_b", "beat", "count"))
    assert answer[0] >= total * 2 / 3 - 1e-9
    said = pr.spoken(f"{episode['answer']} {episode['comparison']}")
    assert total - answer[0] == pytest.approx(max(3.0, said))


def _plain(episode):
    """A copy whose answer and comparison are plain words, so a test's
    timings follow its word counts alone."""
    episode = copy.deepcopy(episode)
    episode["answer"], episode["comparison"] = "A", _words(3)
    return episode


def test_a_number_counts_as_the_words_it_is_read_as():
    # Third judging (11-16): "nineteen ninety", "six seventy-five" ran past
    # the hook's estimate when each counted as one word.
    assert [pr._said(t) for t in ["1990?", "$6.75.", "$1.56", "4.3×", "Jan", "702,250"]] == \
        [2, 2, 2, 4, 1, 3]
    assert pr.spoken("in Jan 1990") == pytest.approx(4 / sample.WORDS_PER_SECOND)


def test_the_closing_line_is_in_the_description_not_spoken_over_the_reveal():
    episode = EPISODES[0]
    assert episode["turn"] in pr.description(episode)
    assert all(text != episode["turn"] for _, _, text, _ in pr.plan(episode))


def test_every_fixture_episode_reveals_at_or_after_two_thirds():
    assert EPISODES   # the fixtures still make at least one episode
    for episode in EPISODES:
        t = pr.timings(episode)
        assert _start(pr.plan(episode), "answer") == t["reveal_start"]
        assert t["reveal_start"] >= t["total"] * 2 / 3 - 1e-9


def test_a_long_hook_pushes_the_beat_and_reveal_later_by_its_estimate():
    short, long = _plain(EPISODES[0]), _plain(EPISODES[0])
    short["hook"], long["hook"] = _words(4), _words(27)
    estimate = 27 / sample.WORDS_PER_SECOND          # 10 s at narration pace
    long_plan, short_plan = pr.plan(long), pr.plan(short)
    assert _start(long_plan, "beat") == pytest.approx(estimate)
    assert _start(long_plan, "answer") == pytest.approx(estimate + 3)
    assert _start(long_plan, "answer") - _start(short_plan, "answer") == \
        pytest.approx(estimate - 3.0)
    (hook,) = _by_style(long_plan, "hook")
    assert hook[1] == _start(long_plan, "answer")    # the question holds to the reveal


def test_a_short_hook_keeps_3_seconds():
    episode = _plain(EPISODES[0])
    episode["hook"] = _words(4)                      # 1.5 s to say
    items = pr.plan(episode)
    assert _start(items, "beat") == 3.0 and _start(items, "answer") == 6.0
    assert pr.timings(episode)["total"] == 9.0


def test_a_long_reveal_holds_the_question_so_the_reveal_starts_at_two_thirds():
    """A reveal longer than half the lead-up would start before two-thirds.
    Holding the reveal longer only makes that worse, so the question holds
    longer instead and the reveal starts at exactly two-thirds."""
    episode = _plain(EPISODES[0])
    episode["hook"], episode["comparison"] = _words(4), _words(26)   # 27 words revealed
    t = pr.timings(episode)
    assert t["total"] - t["reveal_start"] == pytest.approx(27 / sample.WORDS_PER_SECOND)
    assert t["reveal_start"] == pytest.approx(t["total"] * 2 / 3)
    # The beat follows the hook's 3 s; the 3-2-1 leads into the reveal.
    assert t["hook_end"] == 3.0 and t["count_start"] == t["reveal_start"] - pr.COUNT_FROM


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_no_text_reaches_the_bottom_15_percent(episode):
    for _, _, _, style in pr.plan(episode):
        assert pr.bottom(style) <= 0.85 * 1920, style


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_the_reveal_shows_the_answer_and_one_comparison_only(episode):
    items = pr.plan(episode)
    shown = {t for _, _, t, _ in items}
    for field in ("tomorrow", "credit", "turn"):
        assert episode[field] not in shown
        assert not _by_style(items, field)
    revealed = [it for it in items if it[0] >= pr.timings(episode)["reveal_start"]]
    assert [s for _, _, _, s in revealed] == ["answer", "comparison"]
    description = pr.description(episode)
    assert episode["tomorrow"] in description and episode["credit"] in description


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_every_on_screen_string_is_an_episode_field_or_a_label(episode):
    allowed = {episode["hook"], episode["beat"], episode["answer"], episode["comparison"],
               "3", "2", "1"}
    allowed |= {f"{label}  {o}" for label, o in zip(pr.LABELS, episode["options"] or [])}
    for _, _, text, _ in pr.plan(episode):
        assert text in allowed


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_the_countdown_shows_3_2_1_one_per_second(episode):
    counts = _by_style(pr.plan(episode), "count")
    assert [t for _, _, t, _ in counts] == ["3", "2", "1"]
    for (s1, e1, _, _), (s2, _, _, _) in zip(counts, counts[1:]):
        assert e1 == s2 and e1 - s1 == pytest.approx(1.0)
    (beat,) = _by_style(pr.plan(episode), "beat")
    assert beat[2] == episode["beat"]
    # The beat line shows from the hook's end, the digits lead into the reveal.
    t = pr.timings(episode)
    assert (beat[0], beat[1]) == (t["hook_end"], counts[-1][1])
    assert beat[0] <= counts[0][0] == t["count_start"]
    (hook,) = _by_style(pr.plan(episode), "hook")
    assert hook[2] == episode["hook"] and hook[1] >= counts[-1][1]   # question held


@pytest.mark.parametrize("episode", ALL, ids=lambda e: e["beat"])
def test_the_revealed_text_is_the_episodes_own(episode):
    items = pr.plan(episode)
    for field in ("answer", "comparison"):
        (it,) = _by_style(items, field)
        assert it[2] == episode[field]


def test_an_altered_answer_shows_on_screen_as_altered():
    episode = copy.deepcopy(EPISODES[0])
    original = pr.plan(episode)
    episode["answer"], episode["comparison"] = "$9.99", "2.0× more now"
    (answer,) = _by_style(pr.plan(episode), "answer")
    (comparison,) = _by_style(pr.plan(episode), "comparison")
    assert answer[2] == "$9.99" and comparison[2] == "2.0× more now"
    assert _by_style(original, "answer")[0][2] == EPISODES[0]["answer"] != "$9.99"


def test_a_pick_shows_its_two_options_as_labelled_blocks():
    pick = next(e for e in ALL if e["options"])
    blocks = _by_style(pr.plan(pick), "option_a") + _by_style(pr.plan(pick), "option_b")
    assert [t for _, _, t, _ in blocks] == [f"A  {pick['options'][0]}",
                                           f"B  {pick['options'][1]}"]
    number = next(e for e in ALL if not e["options"])
    assert not _by_style(pr.plan(number), "option_a")


def test_render_writes_moviepys_temp_audio_under_assets_gen(monkeypatch, tmp_path):
    """Not the working directory, which is the repo root when a script runs."""
    written = {}

    class Clip:
        def write_videofile(self, path, **kw):
            written.update(kw, path=path)

        def close(self):
            pass

    monkeypatch.setattr(pr, "build", lambda episode, seed=0, narration=None: Clip())
    pr.render(EPISODES[0], tmp_path / "sample.mp4")
    assert written["path"] == str(tmp_path / "sample.mp4")
    assert Path(written["temp_audiofile"]).parent == config.GEN
