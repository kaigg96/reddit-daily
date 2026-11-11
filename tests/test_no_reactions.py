"""Bet 1 without its per-answer reactions (#77, 2026-11-11): the setup note
and the vote stay, and no answer carries a tag, shown or spoken."""
import pytest

from src import config, insights, llm, run, video
from tests.test_commentary import HOST, POST_ANSWERS, _Post, _synth


@pytest.fixture
def no_reactions(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    monkeypatch.setattr(config, "HOST_REACTIONS", False)
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)


def test_this_build_ships_without_reactions():
    assert not config.HOST_REACTIONS and config.HOST_TEXT


def test_only_the_setup_and_the_vote_remain(no_reactions):
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert [s.kind for s in segs] == ["title", "comment", "comment", "vote"]
    assert [s.note for s in segs] == [HOST["setup"], "", "", ""]
    assert not any(r in [s.text for s in segs] for r in HOST["reactions"])   # never voiced
    assert all(s.speaker is None for s in segs) and segs[-1].text == HOST["cta"]
    assert [s.text for s in segs][1:3] == POST_ANSWERS[:2]
    assert run.host_lines_shown(segs) == 2
    # no tag, so each answer keeps the ordinary gap rather than a tag's pause
    assert all(video.gap_after(s) == config.INTER_SEGMENT_GAP for s in segs[1:3])


def test_the_dose_counts_setup_and_vote_as_whole(no_reactions):
    rows = [{"format_version": "v8", "host_lines": n} for n in ("2", "1", "0", "2")]
    assert insights.render_host_lines(rows, "v8").endswith(
        "all 2 on 2 of 4 uploads, some on 1, none on 1")
