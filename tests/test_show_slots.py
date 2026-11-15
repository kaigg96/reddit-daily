"""E1 T4: one Reddit and one takes upload a day, the shows trading slots."""
import collections
import datetime

import pytest

from src import config, content

LINES = (("23 0 * * *", 0), ("23 12 * * *", 12))


def _runs(days, start_day=0):
    start = datetime.datetime(2026, 11, 1, 0, 30, tzinfo=datetime.timezone.utc)
    for d in range(start_day, start_day + days):
        for line, hour in LINES:
            yield line, start.replace(hour=hour) + datetime.timedelta(days=d)


@pytest.fixture
def alternating(monkeypatch):
    monkeypatch.setattr(config, "SHOW_ALTERNATION", True)
    for name in ("SOURCE", "SHOW", "FORMAT_VERSION", "ANSWER_LABEL"):
        monkeypatch.setattr(config, name, getattr(config, name))


def test_built_switched_off():
    assert config.SHOW_ALTERNATION is False


@pytest.mark.parametrize("offset", range(0, 7))
def test_over_any_14_days_each_show_gets_14_uploads_7_per_slot(alternating, offset):
    seen = collections.Counter()
    for line, now in _runs(14, offset):
        seen[(content.show_for_run(now, line), line)] += 1
    assert sorted(seen) == sorted((s, line) for s in config.SHOWS for line, _ in LINES)
    assert set(seen.values()) == {7}


def test_one_show_each_slot_every_day(alternating):
    runs = list(_runs(10))
    for i in range(0, len(runs), 2):
        shows = {content.show_for_run(now, line) for line, now in runs[i:i + 2]}
        assert shows == set(config.SHOWS)


def test_over_28_days_the_reddit_arm_draws_every_subreddit_in_every_slot(alternating):
    seen = collections.Counter()
    for line, now in _runs(28):
        if content.show_for_run(now, line) == "reddit":
            seen[(content.subreddit_for_run(now, schedule=line), line)] += 1
    assert set(seen) == {(s, line) for s in config.SUBREDDITS for line, _ in LINES}
    assert len(set(seen.values())) == 1   # and evenly


def test_with_three_subreddits_the_reddit_arm_still_covers_every_slot(alternating):
    subs = ["AskReddit", "NoStupidQuestions", "AskUK"]
    seen = set()
    for line, now in _runs(12):
        if content.show_for_run(now, line) == "reddit":
            seen.add((content.subreddit_for_run(now, subs, schedule=line), line))
    assert seen == {(s, line) for s in subs for line, _ in LINES}


def test_use_show_sets_everything_that_follows_the_show(alternating):
    config.use_show("takes")
    assert (config.SOURCE, config.SHOW, config.FORMAT_VERSION) == (
        "own", "takes", config.OWN_FORMAT_VERSION)
    assert config.ANSWER_LABEL == ("ANSWER" if config.SAMPLE else "TAKE")
    config.use_show("reddit")
    assert (config.SOURCE, config.SHOW, config.FORMAT_VERSION, config.ANSWER_LABEL) == (
        "reddit", "reddit", config.REDDIT_FORMAT_VERSION, "ANSWER")
    with pytest.raises(ValueError):
        config.use_show("own")


def test_off_the_subreddit_rotation_is_unchanged():
    subs = config.SUBREDDITS
    for line, now in _runs(8):
        day = now.date().toordinal()
        assert content.subreddit_for_run(now, schedule=line) == subs[(day + (now.hour >= 12)) % len(subs)]


class _Stop(Exception):
    pass


@pytest.mark.parametrize("show", config.SHOWS)
def test_a_run_takes_its_show_before_the_content_step(monkeypatch, tmp_path, alternating, show):
    from src import run
    monkeypatch.setattr(config, "PREV_POST_FILE", tmp_path / "prev_post.txt")
    monkeypatch.setattr(run, "check_channel_name", lambda: None)
    monkeypatch.setattr(content, "run_slot", lambda now, schedule="": (now.date(), 0))
    monkeypatch.setattr(content, "show_for_run", lambda now, schedule="": show)
    state = {}

    def stop(now, schedule=""):
        state.update(source=config.SOURCE, show=config.SHOW, fmt=config.FORMAT_VERSION)
        raise _Stop
    monkeypatch.setattr(content, "subreddit_for_run", stop)
    with pytest.raises(_Stop):
        run.main()
    takes = show == "takes"
    assert state == {"source": "own" if takes else "reddit", "show": show,
                     "fmt": config.OWN_FORMAT_VERSION if takes else config.REDDIT_FORMAT_VERSION}
