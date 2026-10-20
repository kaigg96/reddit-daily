"""Bet 1's text-only host (PRD R3.2, after #71): our lines are shown, never
spoken, so a first-time viewer can tell them from Reddit's words."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config, video


def test_a_segment_has_no_note_unless_given_one():
    assert video.Segment(kind="comment", text="x", audio_path="a.mp3", marks=[]).note == ""


def test_a_note_comes_in_partway_and_runs_to_the_next_segment():
    start, span = video.note_window(10.0, 4.0)
    assert 10.0 < start < 14.0
    assert abs((start + span) - (14.0 + config.INTER_SEGMENT_GAP)) < 1e-9


def test_notes_sit_between_the_captions_and_the_watermark():
    assert 700 < config.NOTE_Y < 1500 - config.NOTE_FONT_SIZE * 2


def test_a_note_sits_on_a_see_through_band_of_its_own_size_and_time():
    band, note = video.note_clips("Bold pick.", 3.0, 2.0)
    assert band.size == note.size
    assert (band.start, band.duration) == (note.start, note.duration) == (3.0, 2.0)
    assert band.pos(0) == note.pos(0)
    assert 0 < config.NOTE_BAND_OPACITY < 1


# --- the narration, text-only (HOST_TEXT) -------------------------------------

import pytest

from src import llm, run
from tests.test_commentary import HOST, POST_ANSWERS, _Post, _synth, _too_long_until


@pytest.fixture
def text_host(monkeypatch):
    """The mechanics below count nothing, so they reuse the two-answer
    fixtures; what ships, three answers, is pinned at the end of this file.
    They are the sentence-long notes' (HOST_TAGS off); the tags have their own
    section below."""
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", False)
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)


def _segments():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    return host, run.build_segments(_Post, host.verdict, host, _synth, "Stephen")


def test_the_host_is_shown_never_heard(text_host):
    _, segs = _segments()
    assert [s.kind for s in segs] == ["title", "comment", "comment", "vote"]
    assert [s.note for s in segs] == [HOST["setup"], *HOST["reactions"], ""]
    assert all(s.speaker is None for s in segs)        # one voice: the narrator's
    assert segs[-1].text == HOST["cta"]                # the vote, spoken as a CTA


def test_the_guard_drops_an_answer_with_its_note(text_host):
    host, segs = _segments()
    outro = run.fit_to_length(segs, _too_long_until(3), host, _synth)
    assert [s.text for s in segs][1:2] == [POST_ANSWERS[0]] and len(segs) == 3
    assert HOST["reactions"][1] not in [s.note for s in segs]
    assert outro == config.OUTRO_TEXT == segs[-1].text  # the vote may name it


def test_own_words_count_the_notes_and_the_vote():
    segs = [video.Segment("title", "a" * 20, "", [], note="b" * 10),
            video.Segment("comment", "c" * 20, "", [], note="d" * 10),
            video.Segment("vote", "e" * 20, "", [])]
    assert run.own_words_share(segs) == "0.500"


def test_every_text_edit_matches_the_voiced_ask():
    # A reworded voiced ask would silently leave a text host told to "speak".
    for old, _ in llm._TEXT_EDITS:
        assert old in llm._COMMENTARY_ASK, old


def test_a_text_host_is_told_it_is_read_and_must_not_quote(text_host):
    ask = llm._commentary_ask(2)
    assert "never spoken" in ask and "Never\n     repeat the answer's own words" in ask
    assert "heard" not in ask and "spoken words" not in ask


def test_a_voiced_host_keeps_its_ask(monkeypatch):
    monkeypatch.setattr(config, "HOST_TEXT", False)
    assert llm._commentary_ask(2) == llm._COMMENTARY_ASK.format(n=2)


def test_a_text_reaction_has_a_tighter_cap(text_host):
    assert not llm._within_cap(" ".join(["word"] * 13), "reaction")   # four lines
    assert llm._within_cap(" ".join(["word"] * 12), "reaction")


def test_a_lower_case_note_is_shown_with_its_capital():
    _, note = video.note_clips("looking past the paycheck to find real charm.", 0.0, 1.0)
    assert " ".join(note.text.split()) == "Looking past the paycheck to find real charm."
    for kept in ("YouTube knows.", "r/AskReddit agrees.", "iPhone people, again."):
        _, note = video.note_clips(kept, 0.0, 1.0)
        assert " ".join(note.text.split()) == kept


def test_the_posted_vote_starts_each_sentence_with_a_capital():
    from src import content
    vote = ("raising my hand for yes youll be fine because floor camping builds character."
            " which gets your vote?")
    assert content.sentence_case(vote) == (
        "Raising my hand for yes youll be fine because floor camping builds character."
        " Which gets your vote?")
    assert content.sentence_case("honestly, no.  why would it?") == "Honestly, no.  Why would it?"
    # Review, 2026-10-11: a one-word sentence must not swallow the next one's
    # stop, and a contraction is still a plain word.
    assert content.sentence_case("nope. sorry. which?") == "Nope. Sorry. Which?"
    assert content.sentence_case("i'd pick it. don’t you?") == "I'd pick it. Don’t you?"
    for kept in ("iPhone people, again. YouTube knows.", "r/AskReddit agrees. 3 votes so far!",
                 "Raising my hand for yes. Which gets your vote?", ""):
        assert content.sentence_case(kept) == kept


def test_the_comment_posts_the_vote_capitalised():
    import inspect
    from src import run
    assert "comment_text = content.sentence_case(outro_text)" in inspect.getsource(run.main)


# --- one long line drops alone (sample of 2026-10-13 lost its whole host) -----

def _text_metadata(monkeypatch, **lines):
    import json
    from tests.test_commentary import _metadata
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", False)        # as text_host
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)
    return _metadata(monkeypatch, json.dumps({**HOST, **lines}))[0].commentary


def test_a_long_reaction_drops_only_its_own_note(monkeypatch):
    host = _text_metadata(monkeypatch, reactions=[HOST["reactions"][0], "word " * 13])
    assert host == (HOST["setup"], [HOST["reactions"][0], ""], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert [s.note for s in segs] == [HOST["setup"], HOST["reactions"][0], "", ""]


def test_a_long_vote_leaves_the_generic_line_and_keeps_the_notes(monkeypatch):
    host = _text_metadata(monkeypatch, cta="word " * 19)
    assert host.setup == HOST["setup"] and host.reactions == HOST["reactions"]
    assert run.closing_line(None, host) is None          # so today's line closes
    segs = run.build_segments(_Post, config.OUTRO_TEXT, host, _synth, "Stephen")
    assert segs[-1].kind == "outro"                     # not counted as our words
    notes = sum(len(n) for n in [HOST["setup"], *HOST["reactions"]])
    total = sum(len(s.text) + len(s.note) for s in segs)
    assert run.own_words_share(segs) == f"{notes / total:.3f}"


def test_with_no_note_left_the_upload_is_todays_reading(monkeypatch):
    assert _text_metadata(monkeypatch, setup="word " * 13,
                          reactions=["word " * 13, "word " * 13]) is None


def test_a_voiced_host_still_falls_back_whole(monkeypatch):
    host = _text_metadata(monkeypatch)
    assert host is not None
    monkeypatch.setattr(config, "HOST_TEXT", False)
    from tests.test_commentary import _metadata
    import json
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, "reactions": ["ok", "word " * 19]}))
    assert meta.commentary is None


def test_the_log_counts_the_host_lines_actually_shown(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)
    whole = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    assert run.host_lines_shown(run.build_segments(_Post, whole.verdict, whole, _synth, "S")) == 4
    host = _text_metadata(monkeypatch, reactions=[HOST["reactions"][0], "word " * 13])
    assert run.host_lines_shown(run.build_segments(_Post, host.verdict, host, _synth, "S")) == 3


def test_a_long_setup_drops_alone(monkeypatch):
    host = _text_metadata(monkeypatch, setup="word " * 13)
    assert host == ("", HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert segs[0].note == "" and [s.note for s in segs[1:3]] == HOST["reactions"]


def test_the_guard_does_not_pay_twice_for_a_generic_close(monkeypatch):
    host = _text_metadata(monkeypatch, cta="word " * 19)
    segs = run.build_segments(_Post, config.OUTRO_TEXT, host, _synth, "Stephen")
    calls = []
    outro = run.fit_to_length(segs, _too_long_until(3), host,
                              lambda *a, **k: calls.append(a) or _synth(*a, **k))
    assert calls == [] and outro == config.OUTRO_TEXT == segs[-1].text


def test_the_upload_log_carries_the_host_line_count():
    import inspect
    from src import log
    assert log.FIELDS[-1] == "host_lines"
    assert '"host_lines": host_lines' in inspect.getsource(run.main)


def test_a_voiced_host_counts_its_spoken_lines(monkeypatch):
    monkeypatch.setattr(config, "HOST_TEXT", False)
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert run.host_lines_shown(segs) == 4
    run.fit_to_length(segs, _too_long_until(3), host, _synth)
    assert run.host_lines_shown(segs) == 1     # setup, last answer and its line, the vote


@pytest.mark.parametrize("junk", ["...", "🔥🔥", "So true 😂"])
def test_a_placeholder_or_emoji_note_drops_alone(monkeypatch, junk):
    host = _text_metadata(monkeypatch, reactions=[junk, HOST["reactions"][1]])
    assert host == (HOST["setup"], ["", HOST["reactions"][1]], HOST["cta"])


def test_the_sample_setup_fits_the_text_cap():
    from src import sample
    assert llm._within_cap(sample.METADATA.commentary.setup, "setup")


def test_a_trademark_sign_is_text_not_an_emoji(monkeypatch):
    host = _text_metadata(monkeypatch, reactions=["Reddit™ users loved this.", HOST["reactions"][1]])
    assert host.reactions[0] == "Reddit™ users loved this."


# --- what ships: three answers (2026-10-14) -----------------------------------
# Two answers made room for the voiced host's spoken lines (#70). Notes take no
# time, and two answers would cut the median video from 23.3s to ~17.2s, where
# uploads hold 25% less watch time (PRD §4), so the text host reads all three.

THREE = [*HOST["reactions"], "Twenty five small bosses, zero breaks."]


def test_the_text_host_reads_all_three_answers():
    assert config.HOST_TEXT and config.COMMENTARY_ANSWERS == config.NUM_COMMENTS == 3


def test_the_call_asks_for_a_reaction_to_each_of_the_three(monkeypatch):
    import json
    from tests.test_commentary import _metadata
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TAGS", False)   # THREE are sentence-long notes
    meta, prompt = _metadata(monkeypatch, json.dumps({**HOST, "reactions": THREE}))
    assert "exactly 3 lines" in prompt and '"reactions": ["...", "...", "..."]' in prompt
    assert all(f'{i}. "{a}"' in prompt for i, a in enumerate(POST_ANSWERS, 1))
    assert meta.commentary == llm.Commentary(HOST["setup"], THREE, HOST["cta"])


def test_three_answers_each_carry_their_note(text_host, monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 3)
    host = llm.Commentary(HOST["setup"], THREE, HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert [s.kind for s in segs] == ["title", "comment", "comment", "comment", "vote"]
    assert [s.text for s in segs[1:4]] == POST_ANSWERS
    assert [s.note for s in segs] == [HOST["setup"], *THREE, ""]
    assert run.host_lines_shown(segs) == 5


def test_the_free_sample_has_a_note_for_every_answer_it_reads():
    from src import sample
    host = sample.METADATA.commentary
    assert len(host.reactions) == len(sample.POST.comments[:config.COMMENTARY_ANSWERS])
    assert all(llm._usable(r, "reaction") for r in host.reactions)


# --- tags (HOST_TAGS, #77, 2026-10-19) ----------------------------------------
# The owner, on a narrated render: a sentence shown mid-answer cannot be read
# while the answer is heard. So each note is a tag of 1-3 words, shown on its
# segment's last spoken words and held through a longer pause.

TAGS = {"setup": "Harder than it looks.", "reactions": ["Smiling is cardio.", "Boredom, then chaos."]}


@pytest.fixture
def tag_host(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    monkeypatch.setattr(config, "COMMENTARY_ANSWERS", 2)


def test_the_tags_ship():
    assert config.HOST_TEXT and config.HOST_TAGS


def test_every_tag_edit_matches_the_text_ask(monkeypatch):
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", False)
    ask = llm._commentary_ask(2)
    for old, _ in llm._TAG_EDITS:
        assert old.format(n=2) in ask, old


def test_a_tag_host_is_asked_for_tags(tag_host):
    ask = llm._commentary_ask(2)
    assert ask.count("1 to 3 words") == 2 and "never a sentence" in ask and "at a glance" in ask
    assert "AT MOST 10 words" not in ask and "two seconds" not in ask
    assert "never spoken" in ask and "Never\n     repeat the answer's own words" in ask
    assert "exactly 2 lines" in ask


def test_a_tag_is_four_words_at_most_and_the_vote_keeps_its_cap(tag_host):
    assert llm._within_cap("Fair point, honestly, yes.", "reaction")
    assert not llm._within_cap("Fair point, honestly, yes, really.", "reaction")
    assert not llm._within_cap("Everyone thinks they could do these.", "setup")
    assert llm._within_cap(" ".join(["word"] * 18), "cta")


@pytest.mark.parametrize("line, ok", [("Thatescalatedquickly.", False),
                                      ("Characteristically bold.", True),
                                      ("Bank statement? Checkmate.", True)])
def test_words_run_together_drop(tag_host, line, ok):
    assert llm._usable(line, "reaction") is ok


def test_tags_survive_the_metadata_call_and_a_sentence_drops_alone(tag_host, monkeypatch):
    import json
    from tests.test_commentary import _metadata
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, **TAGS}))
    assert meta.commentary == (TAGS["setup"], TAGS["reactions"], HOST["cta"])
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, **TAGS,
                                                 "reactions": [TAGS["reactions"][0], HOST["reactions"][1]]}))
    assert meta.commentary == (TAGS["setup"], [TAGS["reactions"][0], ""], HOST["cta"])


def test_a_tag_comes_in_on_the_last_words_and_holds_through_the_pause(tag_host):
    start, span = video.tag_window(10.0, 3.0, 3.0)
    assert abs(start - (13.0 - config.TAG_LEAD_IN)) < 1e-9
    assert abs((start + span) - (13.0 + config.TAG_PAUSE)) < 1e-9
    # A short answer holds on screen past its narration; its tag still comes
    # in on the last words and stays until the next segment starts.
    start, span = video.tag_window(10.0, 1.2, config.MIN_COMMENT_DISPLAY)
    assert abs(start - (11.2 - config.TAG_LEAD_IN)) < 1e-9
    assert abs((start + span) - (10.0 + config.MIN_COMMENT_DISPLAY + config.TAG_PAUSE)) < 1e-9


def test_only_a_segment_with_a_tag_gets_the_longer_pause(tag_host, monkeypatch):
    tagged = video.Segment("comment", "x", "", [], note="Oof.")
    plain = video.Segment("comment", "x", "", [])
    assert video.gap_after(tagged) == config.TAG_PAUSE > config.INTER_SEGMENT_GAP
    assert video.gap_after(plain) == config.INTER_SEGMENT_GAP
    monkeypatch.setattr(config, "HOST_TAGS", False)
    assert video.gap_after(tagged) == config.INTER_SEGMENT_GAP


def test_the_duration_guard_counts_the_pauses_the_video_will_have():
    import inspect
    assert "video.gap_after(s) for s in segs[:-1]" in inspect.getsource(run.main)
