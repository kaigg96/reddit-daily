"""Shared test setup."""
import pytest

from src import config


@pytest.fixture(autouse=True)
def _gemini_route(monkeypatch):
    """Tests pin Gemini's request shape, so a shell or .env with AI_PROVIDER
    set must not switch them to another route. Groq tests opt in."""
    monkeypatch.setattr(config, "AI_PROVIDER", "gemini")
