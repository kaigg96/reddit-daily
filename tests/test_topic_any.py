"""`topic_any`: the logged topic, else the labelling pass's (insights._TOPICS_CACHE)."""
from src import insights


def test_topic_any_fills_older_uploads_from_the_labelling_pass(monkeypatch):
    """82 logged uploads predate the screen's topic; the labelling pass's cache
    labels most of them. `topic` itself stays as logged, so pre-committed reads
    on it keep their population."""
    monkeypatch.setattr(insights, "_cached_topics",
                        lambda: {"Old question?": "nostalgia", "New question?": "other"})
    derive = lambda **row: insights._with_derived_dimensions(row)
    old = derive(post_title="Old question?", topic="")
    assert (old["topic"], old["topic_any"]) == ("", "nostalgia")
    new = derive(post_title="New question?", topic="dark-morbid")
    assert (new["topic"], new["topic_any"]) == ("dark-morbid", "dark-morbid")
    assert derive(post_title="Never labelled?", topic="")["topic_any"] == ""
    assert derive(topic="")["topic_any"] == ""


def test_the_topics_cache_is_read_from_the_repository():
    """The real cache loads, so --by topic_any is not silently empty."""
    insights._cached_topics.cache_clear()
    assert len(insights._cached_topics()) > 700
