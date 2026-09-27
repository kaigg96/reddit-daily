"""R4.4 Step 0.5: the slate is labelled for telemetry and can never cost an upload.

The ranker R4.4 would build fires only when the top candidate's topic is weak
and one just below it is strong. How often that happens decides how long its
bake takes, and the upload log's one topic per upload cannot say. So every run
now labels the whole eligible slate in ONE request, on a model whose free
allowance is separate from the one titles and the screen share.
"""

import json

import pytest

from src import config, content, llm, screen

TITLES = ["What job looks easy but is brutal?",
          "What did every 90s kid own?",
          "What is the creepiest thing you have seen at night?"]


class FakePost:
    def __init__(self, title):
        self.title = title
        self.over_18 = False
        self.shortlink = f"https://redd.it/{title[:6]}"


class FakeReddit:
    def __init__(self, titles):
        self.titles = titles

    def subreddit(self, name):
        titles = self.titles

        class S:
            def top(self, time_filter, limit):
                return [FakePost(t) for t in titles]
        return S()


@pytest.fixture
def selection(monkeypatch):
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)


# --- the call -----------------------------------------------------------------

def test_one_request_on_the_slate_model_for_the_whole_slate(monkeypatch):
    calls = []

    def fake(prompt, thinking_budget=0, model=llm.MODEL):
        calls.append((prompt, model))
        return json.dumps(["money-work", "nostalgia", "dark-morbid"])

    monkeypatch.setattr(screen.llm, "_generate", fake)
    assert screen.classify_slate(TITLES) == ["money-work", "nostalgia", "dark-morbid"]
    assert len(calls) == 1
    assert calls[0][1] == config.SLATE_MODEL != llm.MODEL
    assert all(t in calls[0][0] for t in TITLES)


def test_unknown_labels_are_blanked_not_trusted(monkeypatch):
    monkeypatch.setattr(screen.llm, "_generate",
                        lambda *a, **k: '```json\n["Money-Work", "sports", "nostalgia"]\n```')
    assert screen.classify_slate(TITLES) == ["money-work", "", "nostalgia"]


@pytest.mark.parametrize("reply, kind", [('["money-work"]', "shape 1/3"),
                                         ("no json", "shape"), ('{"a": 1}', "shape")])
def test_a_wrong_shape_logs_why_rather_than_misaligned_ranks(monkeypatch, reply, kind):
    monkeypatch.setattr(screen.llm, "_generate", lambda *a, **k: reply)
    with pytest.raises(screen.SlateFailed) as e:
        screen.classify_slate(TITLES)
    assert e.value.kind == kind


def test_a_failed_call_is_not_retried_and_names_only_type_and_status(monkeypatch, capsys):
    calls = []

    class HTTPError(Exception):
        response = type("R", (), {"status_code": 429})()

    def boom(*a, **k):
        calls.append(1)
        raise HTTPError("429 for url ...?key=secret")

    monkeypatch.setattr(screen.llm, "_generate", boom)
    with pytest.raises(screen.SlateFailed) as e:
        screen.classify_slate(TITLES)
    assert e.value.kind == "HTTPError 429"
    assert len(calls) == 1
    assert "secret" not in capsys.readouterr().out and e.value.__cause__ is None


def test_the_model_reaches_the_url(monkeypatch):
    seen = []

    class R:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "[]"}]}}]}

    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: seen.append((url, kw)) or R())
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    llm._generate("x", model="some-other-model")
    llm._generate("x")
    assert "/models/some-other-model:generateContent" in seen[0][0]
    assert f"/models/{llm.MODEL}:generateContent" in seen[1][0]


def test_the_key_travels_in_a_header_never_the_url(monkeypatch):
    """An HTTPError quotes the URL, so a key in it lands in every log."""
    seen = []

    class R:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "[]"}]}}]}

    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: seen.append((url, kw)) or R())
    monkeypatch.setenv("GEMINI_API_KEY", "sekrit")
    llm._generate("x")
    url, kw = seen[0]
    assert "sekrit" not in url and kw["headers"]["x-goog-api-key"] == "sekrit"


# --- selection ----------------------------------------------------------------

def test_slate_is_logged_in_rank_order_and_never_changes_the_pick(selection):
    post = content.select_post(FakeReddit(TITLES), "",
                               slate_classifier=lambda t: ["money-work", "", "nostalgia"])
    assert post.title == TITLES[0] and post.candidate_rank == 1
    assert post.slate_topics == "money-work|?|nostalgia"


def test_a_classifier_that_raises_costs_only_the_column(selection):
    def boom(titles):
        raise RuntimeError("anything")

    post = content.select_post(FakeReddit(TITLES), "", slate_classifier=boom)
    assert post.title == TITLES[0] and post.slate_topics == "!RuntimeError"


def test_a_failed_slate_logs_why(selection):
    def failed(titles):
        raise screen.SlateFailed("Timeout")

    post = content.select_post(FakeReddit(TITLES), "", slate_classifier=failed)
    assert post.title == TITLES[0] and post.slate_topics == "!Timeout"


def test_slate_ranks_match_candidate_rank_after_filters(selection):
    """Rank is position among ELIGIBLE candidates, the same basis as
    candidate_rank, so slate[candidate_rank - 1] is the selected post."""
    seen = []
    content.select_post(FakeReddit(["yesterday's question"] + TITLES), "yesterday's question",
                        slate_classifier=lambda t: seen.append(t) or ["x"] * len(t))
    assert seen == [TITLES]


def test_no_classifier_means_no_column(selection):
    assert content.select_post(FakeReddit(TITLES), "").slate_topics == ""


def test_thinking_budget_goes_only_to_models_that_accept_it(monkeypatch):
    """Gemini 3.x returns 400 on thinkingBudget; 2.5 needs it to stay fast."""
    bodies = []

    class R:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "[]"}]}}]}

    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: bodies.append(kw["json"]) or R())
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    llm._generate("x", model="gemini-2.5-flash")
    llm._generate("x", model="gemini-3.5-flash-lite")
    assert bodies[0]["generationConfig"]["thinkingConfig"]["thinkingBudget"] == 0
    assert "generationConfig" not in bodies[1]


# --- R4.1 subreddit rotation ---------------------------------------------------

def _runs(days):
    import datetime
    start = datetime.datetime(2026, 10, 5, 5, tzinfo=datetime.timezone.utc)
    for d in range(days):
        for hour in (5, 17):
            yield (hour, start.replace(hour=hour) + datetime.timedelta(days=d))


def test_rotation_gives_every_subreddit_both_slots():
    subs = ["AskReddit", "NoStupidQuestions"]
    seen = {(s, h): 0 for s in subs for h in (5, 17)}
    for hour, now in _runs(6):
        seen[(content.subreddit_for_run(now, subs), hour)] += 1
    assert set(seen.values()) == {3}


def test_rotation_never_repeats_a_subreddit_within_a_day():
    subs = ["AskReddit", "NoStupidQuestions", "AskUK"]
    picks = [content.subreddit_for_run(now, subs) for _, now in _runs(3)]
    assert all(picks[i] != picks[i + 1] for i in range(0, len(picks), 2))
    assert {picks.count(s) for s in subs} == {2}


def test_askreddit_stays_in_the_list_as_the_baseline():
    assert config.SUBREDDITS[0] == "AskReddit"


def test_upload_text_for_askreddit_is_unchanged_by_rotation():
    from src.run import upload_text
    desc, tags = upload_text("AskReddit", "Q?", ["a", "b"], "https://redd.it/x", ["k"])
    assert desc == ("Today's top AskReddit post: Q?\n\nTop Comments:\n1. a\n2. b"
                    "\n\nhttps://redd.it/x\n#AskReddit #Reddit #Shorts")
    assert tags == ["AskReddit", "Ask Reddit", "Shorts", "Reddit", "Top AskReddit Post",
                    "Trending AskReddit", "k"]


def test_upload_text_names_the_posts_own_subreddit():
    from src.run import upload_text
    desc, tags = upload_text("NoStupidQuestions", "Q?", ["a"], "https://redd.it/x", [])
    assert "AskReddit" not in desc and "AskReddit" not in " ".join(tags)
    assert desc.startswith("Today's top NoStupidQuestions post") and "#NoStupidQuestions" in desc
