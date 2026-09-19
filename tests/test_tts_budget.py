"""Tests for the Polly spend guard (PRD §5, CLAUDE.md §1).

Polly is the only service that bills the owner, and the failure mode we're
guarding against isn't a bug in the pipeline — it's an agent or a script
deciding that a batch of synthesis is a reasonable way to test something. These
tests pin the guard that makes that stop rather than succeed.
"""

import json

import pytest

from src import config, tts


class FakeStream:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return self._payload


class FakePolly:
    """Records calls so a test can count what would have been billed."""

    def __init__(self):
        self.calls = []

    def synthesize_speech(self, **kw):
        self.calls.append(kw)
        if kw.get("OutputFormat") == "json":
            marks = [{"time": 0, "type": "word", "start": 0, "end": 4, "value": "word"}]
            return {"AudioStream": FakeStream(
                "\n".join(json.dumps(m) for m in marks).encode("utf-8"))}
        return {"AudioStream": FakeStream(b"fake-mp3")}


@pytest.fixture(autouse=True)
def fresh_budget():
    tts.reset_budget()
    yield
    tts.reset_budget()


def synth(polly, text, tmp_path, name="out.mp3"):
    return tts.synthesize_with_marks(polly, text, "Danielle", tmp_path / name)


def test_a_normal_video_fits_the_budget_with_room(tmp_path):
    """Five segments at the config ceiling must not trip the guard.

    If this fails the guard is too tight and would break live uploads — that is
    the one way a cost control can do more damage than the cost.
    """
    polly = FakePolly()
    segments = ["t" * config.MAX_TITLE_LENGTH]
    segments += ["c" * config.MAX_COMMENT_LENGTH] * config.NUM_COMMENTS
    segments += ["o" * 90]  # CTA; the generic OUTRO_TEXT is shorter than this
    for i, text in enumerate(segments):
        synth(polly, text, tmp_path, f"seg{i}.mp3")

    assert len(polly.calls) == 2 * len(segments)
    assert tts.spent_chars() <= config.POLLY_CHAR_BUDGET
    # Meaningful headroom, not a coincidence of the current caps.
    assert tts.spent_chars() < config.POLLY_CHAR_BUDGET * 0.75


def test_every_character_is_charged_twice(tmp_path):
    """The speech-mark call is why cost is double the visible text."""
    polly = FakePolly()
    synth(polly, "x" * 100, tmp_path)
    assert tts.spent_chars() == 200


def test_bulk_synthesis_is_refused_rather_than_billed(tmp_path):
    """The scenario this whole guard exists for: a loop over a corpus."""
    polly = FakePolly()
    with pytest.raises(tts.PollyBudgetExceeded):
        for i in range(1000):
            synth(polly, "a" * 150, tmp_path, f"bulk{i}.mp3")

    # It stopped early, and the call count proves the spend was bounded.
    assert len(polly.calls) < 40
    assert tts.spent_chars() <= config.POLLY_CHAR_BUDGET


def test_the_refused_call_never_reaches_polly(tmp_path):
    """A call that would break the budget must not bill at all.

    Charging up front matters because a failed or half-completed synthesis is
    still billed by AWS — the guard cannot rely on the request succeeding.
    """
    polly = FakePolly()
    synth(polly, "a" * (config.POLLY_CHAR_BUDGET // 2), tmp_path)
    calls_before = len(polly.calls)

    with pytest.raises(tts.PollyBudgetExceeded):
        synth(polly, "b" * config.POLLY_CHAR_BUDGET, tmp_path, "over.mp3")

    assert len(polly.calls) == calls_before


def test_an_uncapped_retry_loop_trips_the_guard(tmp_path):
    """Retrying a failed synthesis re-bills the full character count."""
    class FlakyPolly(FakePolly):
        def synthesize_speech(self, **kw):
            super().synthesize_speech(**kw)
            raise RuntimeError("transient")

    polly = FlakyPolly()
    attempts = 0
    with pytest.raises(tts.PollyBudgetExceeded):
        for _ in range(500):
            attempts += 1
            try:
                synth(polly, "c" * 150, tmp_path)
            except RuntimeError:
                continue  # the naive retry this test is about

    assert attempts < 30


def test_the_stop_signal_is_not_swallowed_by_a_broad_retry_handler(tmp_path):
    """`except RuntimeError` must not eat the budget error.

    This is why PollyBudgetExceeded is not a RuntimeError: the first draft of
    the guard made it one, and this exact loop then retried straight through
    it — the guard raised, the handler swallowed it, the loop continued.
    """
    assert not issubclass(tts.PollyBudgetExceeded, RuntimeError)


def test_spend_stays_bounded_even_if_the_caller_catches_everything(tmp_path):
    """The budget, not the exception, is the real guarantee.

    A caller with a bare `except Exception` can swallow the stop signal. It
    still cannot spend, because an exhausted budget refuses every later call
    before it reaches Polly.
    """
    polly = FakePolly()
    for _ in range(1000):
        try:
            synth(polly, "e" * 150, tmp_path)
        except Exception:
            continue  # the worst-behaved caller we can expect

    assert tts.spent_chars() <= config.POLLY_CHAR_BUDGET
    assert len(polly.calls) < 40


def test_budget_is_raisable_for_an_approved_bulk_run(tmp_path, monkeypatch):
    """The escape hatch exists, but it has to be taken deliberately."""
    polly = FakePolly()
    monkeypatch.setattr(config, "POLLY_CHAR_BUDGET", 100_000)
    for i in range(50):
        synth(polly, "d" * 150, tmp_path, f"ok{i}.mp3")
    assert len(polly.calls) == 100
