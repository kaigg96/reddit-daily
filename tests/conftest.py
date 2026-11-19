"""Shared test setup."""
import pytest

from src import config


@pytest.fixture(autouse=True)
def _gemini_route(monkeypatch):
    """Tests pin Gemini's request shape, so a shell or .env with AI_PROVIDER
    set must not switch them to another route. Groq tests opt in.

    Likewise a shell's GROQ_API_KEY: with GROQ_FALLBACK on, it would send a
    Gemini-failure test on to Groq's rescue. Groq tests set their own key.

    And a shell's GEMINI_API_KEY: a shift's environment holds the real one,
    so a path a test forgets to mock would spend the 20 a day production
    shares (11-18: the takes path did, with SHOW_ALTERNATION on). Without it
    such a call fails fast instead. Tests that need a key set their own."""
    monkeypatch.setattr(config, "AI_PROVIDER", "gemini")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
