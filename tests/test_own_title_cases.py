"""The own-question show's title check, graded on a fixed case set (PLAN C16).

The show asks its own questions, so a title or closing line that credits
Reddit or real people's answers is false, and one that merely mentions people
is ordinary. Three fresh reviews of word-list fixes (TECH_DEBT, the own-title
item) each found new wordings it got wrong, so these cases grade whatever
check replaces it, word list or the screen judging the title, with no AI
request, through `llm._own_fields`, the entry point every version keeps. A
case today's check gets wrong is a strict xfail: a fix that rights it fails
here until its mark comes off.
"""
import pytest

from src import llm

WRONG_TODAY = pytest.mark.xfail(strict=True, raises=AssertionError,
                                 reason="today's word list gets it wrong")

# (line, refuse?)
CASES = [
    ("Redditors Reveal Their Worst Date", True),
    ("3 People Share Their Biggest Regret", True),
    ("Strangers Reveal Their Weirdest Habit", True),
    ("r/AskReddit Answers This", True),
    pytest.param("/r/tifu's Best Stories", True, marks=WRONG_TODAY),
    pytest.param("Commenters reveal what they'd never do again", True, marks=WRONG_TODAY),
    pytest.param("3 Answers That Changed How I Tip", True, marks=WRONG_TODAY),
    pytest.param("People's Hot Takes on Tipping", True, marks=WRONG_TODAY),
    pytest.param("Hot Takes From Strangers", True, marks=WRONG_TODAY),
    pytest.param("People React To The Worst Wedding Gift", True, marks=WRONG_TODAY),
    pytest.param("A stranger told me something I can't forget", True, marks=WRONG_TODAY),
    ("Should two people split the bill?", False),
    ("How often do people really shower?", False),
    ("Which habit would YOU drop first?", False),
    pytest.param("Why do people say sorry so much?", False, marks=WRONG_TODAY),
    pytest.param("3 People You Meet at Every Wedding", False, marks=WRONG_TODAY),
    pytest.param("What do people say when they mean no?", False, marks=WRONG_TODAY),
]


@pytest.mark.parametrize("line,refuse", CASES)
def test_own_title_check_on_the_fixed_cases(line, refuse):
    assert (llm._own_fields({"title": line})["title"] is None) is refuse
