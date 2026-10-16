"""PRD §0 #14's no-capitals arm, held in code (llm.drop_emphasis_caps)."""
from src import llm


def test_the_no_capitals_arm_drops_emphasis_capitals():
    """PRD §0 #14: the arm shipped "What's YOUR unforgetable deathbed
    confession?" on 10-16; the prompt alone did not hold it."""
    cases = {
        "What's YOUR unforgetable deathbed confession?":
            "What's your unforgetable deathbed confession?",
        "YOU won't guess this one": "You won't guess this one",
        "Is it real rest? REALLY?": "Is it real rest? Really?",
        "3 Answers: How YOU'D Feel If US Drops Support":
            "3 Answers: How You'd Feel If US Drops Support",
        "Is Baby Formula REALLY Necessary?": "Is Baby Formula Really Necessary?",
        "What NOT to say to an ICU nurse": "What not to say to an ICU nurse",
        "Your FBI file, in one line": "Your FBI file, in one line",
    }
    source = "Nurses in the ICU, what's the worst thing a visitor said?"
    for generated, shipped in cases.items():
        r = llm.resolve_title(generated, style="B", fallback="Raw?", caps=False,
                              source=source)
        assert (r.title, r.style, r.ok) == (shipped, "B", True), generated


def test_the_capitals_arm_and_an_unset_arm_keep_the_title_as_written():
    """Only arm 0 is held to no capitals; arm 1 asks for one, and a caller
    with no arm (the release check, old callers) changes nothing."""
    for caps in (True, None):
        r = llm.resolve_title("Who's REALLY to blame?", style="B", fallback="Raw?",
                              caps=caps)
        assert r.title == "Who's REALLY to blame?"


def test_a_failed_title_ships_the_reddit_question_untouched_in_either_arm():
    r = llm.resolve_title("", style="B", fallback="AITA for saying NO?", caps=False)
    assert (r.title, r.style, r.ok) == ("AITA for saying NO?", "", False)


def test_the_no_capitals_arm_keeps_acronyms_its_review_found():
    """The fresh review's cases (10-16): acronyms off the list, plurals in the
    source, a curly apostrophe, a title that opens on a number."""
    cases = {
        ("Did YOU learn CPR in school?", ""): "Did you learn CPR in school?",
        ("Ever driven an SUV? WHY?", "Do you hate SUVs?"): "Ever driven an SUV? Why?",
        ("What World War II fact SHOCKED you?", ""): "What World War II fact shocked you?",
        ("DON’T do this at work", ""): "Don’t do this at work",
        ("3 ANSWERS: what would you do?", ""): "3 Answers: what would you do?",
    }
    for (generated, source), shipped in cases.items():
        r = llm.resolve_title(generated, style="C", fallback="Raw?", caps=False,
                              source=source)
        assert r.title == shipped, generated


def test_proper_nouns_do_not_make_a_title_title_case():
    r = llm.resolve_title("Your WiFi. Their Teens. Who's REALLY to blame?", style="B",
                          fallback="Raw?", caps=False)
    assert r.title == "Your WiFi. Their Teens. Who's really to blame?"
