"""The own-question show's title check, graded on a fixed case set (PLAN C16).

The show asks its own questions, so a title or closing line that credits
Reddit or real people's answers is false, and one that merely mentions people
is ordinary. Three fresh reviews of word-list fixes (TECH_DEBT, the own-title
item) each found new wordings it got wrong, so since 11-14 the list keeps
Reddit's names alone and a separate request judges the rest (`llm._own_judged`).
These cases grade the list and the judge's plumbing with no AI request: the
list refuses Reddit's names and nothing else, and every other line reaches the
judge, whose verdict alone decides. Whether the judge's model rights them is
graded before switch-on by one batched request on the sample model.
"""
import pytest

from src import llm

# (line, refuse?) -- a line naming Reddit is the list's; every other, the judge's.
CASES = [
    ("Redditors Reveal Their Worst Date", True),
    ("3 People Share Their Biggest Regret", True),
    ("Strangers Reveal Their Weirdest Habit", True),
    ("r/AskReddit Answers This", True),
    ("/r/tifu's Best Stories", True),
    ("Commenters reveal what they'd never do again", True),
    ("3 Answers That Changed How I Tip", True),
    ("People's Hot Takes on Tipping", True),
    ("Hot Takes From Strangers", True),
    ("People React To The Worst Wedding Gift", True),
    ("A stranger told me something I can't forget", True),
    ("Should two people split the bill?", False),
    ("How often do people really shower?", False),
    ("Which habit would YOU drop first?", False),
    ("Why do people say sorry so much?", False),
    ("3 People You Meet at Every Wedding", False),
    ("What do people say when they mean no?", False),
]
NAMED = {"Redditors Reveal Their Worst Date", "r/AskReddit Answers This",
         "/r/tifu's Best Stories"}


@pytest.mark.parametrize("line,refuse", CASES)
def test_the_list_refuses_reddits_names_and_nothing_else(line, refuse):
    assert (llm._own_fields({"title": line})["title"] is None) is (line in NAMED)


@pytest.mark.parametrize("line,refuse", CASES)
def test_every_other_case_reaches_the_judge_whose_verdict_decides(monkeypatch, line, refuse):
    asked = []

    def judge(prompt, tries=2, **kw):
        asked.append(prompt)
        return '{"title": "%s"}' % ("yes" if refuse else "no")
    monkeypatch.setattr(llm, "generate_retrying", judge)
    out, label = llm._own_judged(llm._own_fields({"title": line}))
    assert (out["title"] is None) is refuse
    if line in NAMED:
        assert not asked and label == ""
    else:
        assert len(asked) == 1 and line in asked[0]
        assert label == ("own_judge_title" if refuse else "")
