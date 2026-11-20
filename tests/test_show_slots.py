"""E1 T4: one Reddit and one takes upload a day, the shows trading slots.
E1 T12: from config.TAKES_ONLY_FROM, every slot is takes."""
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


def test_switched_on_by_e1_t5():
    # Off again only with the takes-gate's read (01-04) or a Decide: the
    # ledger row was dated before the first takes upload.
    assert config.SHOW_ALTERNATION is True


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


def test_off_the_subreddit_rotation_is_unchanged(monkeypatch):
    monkeypatch.setattr(config, "SHOW_ALTERNATION", False)
    subs = config.SUBREDDITS
    for line, now in _runs(8):
        day = now.date().toordinal()
        assert content.subreddit_for_run(now, schedule=line) == subs[(day + (now.hour >= 12)) % len(subs)]


@pytest.fixture(params=(2, 4), ids=("two_a_day", "four_a_day"))
def per_day(request, monkeypatch):
    monkeypatch.setattr(config, "UPLOADS_PER_DAY", request.param)
    return request.param


def _scheduled_on(day):
    """(line, slot, now) for each live slot's run scheduled on `day`, on time
    and late. A late run past slot 0 lands at 00:40 the next day; run_slot
    still gives it `day`, and that is the day show_for_run keys on."""
    start = datetime.datetime.combine(day, datetime.time(0, 23), tzinfo=datetime.timezone.utc)
    for line, slot in config.SLOT_CRONS.items():
        if slot not in content.live_slots():
            continue
        on_time = start + datetime.timedelta(hours=6 * slot)
        late = (start + datetime.timedelta(days=1, minutes=17) if slot
                else on_time + datetime.timedelta(hours=5))
        for now in (on_time, late):
            assert content.run_slot(now, line) == (day, slot)
            yield line, slot, now


def test_takes_only_from_is_5_january_the_day_after_the_takes_gate_read():
    # Decision 4: a FAIL at ledger `takes-gate`'s 01-04 read moves this date
    # (here and in config; insights reads config), never the code.
    from src import insights
    assert config.TAKES_ONLY_FROM == datetime.date(2027, 1, 5)
    assert insights.TAKES_GATE_ENDS == config.TAKES_ONLY_FROM.isoformat()


def test_a_run_scheduled_the_day_before_still_alternates(per_day):
    day = config.TAKES_ONLY_FROM - datetime.timedelta(days=1)
    by_slot = collections.defaultdict(set)
    for line, slot, now in _scheduled_on(day):
        by_slot[slot].add(content.show_for_run(now, line))
    # The last slot's late run lands on TAKES_ONLY_FROM by the clock and keeps
    # its scheduled day's show, the same as on time.
    assert all(len(shows) == 1 for shows in by_slot.values())
    order = [by_slot[slot].pop() for slot in content.live_slots()]
    assert set(order) == set(config.SHOWS)
    assert all(a != b for a, b in zip(order, order[1:]))


def test_every_slot_from_takes_only_from_is_takes(per_day):
    for d in range(60):   # past Reddit's 01-12 cutoff
        day = config.TAKES_ONLY_FROM + datetime.timedelta(days=d)
        shows = {content.show_for_run(now, line) for line, _, now in _scheduled_on(day)}
        assert shows == {"takes"}, day
    # A run no cron line names (a manual run) keys on the clock's day.
    manual = datetime.datetime.combine(config.TAKES_ONLY_FROM, datetime.time(9),
                                       tzinfo=datetime.timezone.utc)
    assert content.show_for_run(manual) == "takes"


def test_with_the_date_moved_the_alternation_is_todays_for_28_days(per_day, monkeypatch):
    # A FAIL at the 01-04 read moves the date; until it, nothing changes.
    first = datetime.date(2026, 12, 22)   # 28 days across 01-05 and 01-12
    moved = first + datetime.timedelta(days=28)
    monkeypatch.setattr(config, "TAKES_ONLY_FROM", moved)
    for d in range(28):
        day = first + datetime.timedelta(days=d)
        for line, slot, now in _scheduled_on(day):
            position = content.live_slots().index(slot)
            expected = config.SHOWS[(day.toordinal() + position) % len(config.SHOWS)]
            assert content.show_for_run(now, line) == expected, (day, slot, now)
    assert {content.show_for_run(now, line) for line, _, now in _scheduled_on(moved)} == {"takes"}


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
