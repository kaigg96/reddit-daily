"""The reply job's YouTube calls (PLAN C10), against a fake Data API resource."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import youtube


class _Req:
    def __init__(self, result):
        self.result = result

    def execute(self):
        return self.result


class _Comments:
    def __init__(self, by_id, pages):
        self.by_id, self.pages, self.inserted = by_id, pages, []

    def list(self, part, id=None, parentId=None, textFormat=None, maxResults=None):
        if id is not None:
            return _Req({"items": [self.by_id[id]] if id in self.by_id else []})
        return _Req(self.pages[0] | {"_page": 0})

    def list_next(self, request, page):
        i = page["_page"] + 1
        return _Req(self.pages[i] | {"_page": i}) if i < len(self.pages) else None

    def insert(self, part, body):
        self.inserted.append(body["snippet"])
        return _Req({})


class _Yt:
    def __init__(self, comments, channel="US"):
        self._comments, self.channel = comments, channel

    def comments(self):
        return self._comments

    def channels(self):
        outer = self

        class _C:
            def list(self, part, mine):
                return _Req({"items": [{"id": outer.channel}]})
        return _C()


def _snip(author, text=""):
    return {"snippet": {"authorChannelId": {"value": author}, "textOriginal": text}}


def test_reply_client_reads_author_and_text_and_none_once_gone():
    c = youtube.ReplyClient(_Yt(_Comments({"c1": _snip("viewer", "hello")}, [{"items": []}])))
    assert c.channel_id() == "US"
    assert c.comment("c1") == ("viewer", "hello")
    assert c.comment("gone") is None


def test_reply_client_finds_our_reply_on_a_later_page():
    pages = [{"items": [_snip("someone")]}, {"items": [_snip("US")]}]
    c = youtube.ReplyClient(_Yt(_Comments({}, pages)))
    assert c.replied("c1", "US") is True
    assert c.replied("c1", "OTHER") is False


def test_reply_client_posts_a_reply_to_the_parent():
    comments = _Comments({}, [{"items": []}])
    c = youtube.ReplyClient(_Yt(comments))
    assert c.post("c1", "Thanks!") is True
    assert comments.inserted == [{"parentId": "c1", "textOriginal": "Thanks!"}]
