"""The play-along selector (src/playalong.py): every value shown is a source
record's, and the five rules each refuse what they should."""
import copy
import csv
import json

import pytest

from src import playalong

GAS, PEOPLE, FLOORS = playalong.candidates()


def _with(candidate, i=None, **changes):
    """A copy of `candidate`, with `changes` made to record `i` (all if None)."""
    c = copy.deepcopy(candidate)
    for j, r in enumerate(c["records"]):
        if i is None or i == j:
            r.update(changes)
    return c


def _reason(candidate, prev_template="", shipped=()):
    episode, why = playalong.select(candidate, prev_template, shipped)
    assert episode is None
    return why


def test_the_worked_examples_make_two_episodes_and_one_rule2_rejection(capsys):
    episodes, rejects = playalong.select_day(playalong.candidates(), "", [])
    assert [e["answer"] for e in episodes] == ["$1.04", "D.C."]
    assert rejects == {"rule2": 1}
    out = capsys.readouterr().out
    # The first casualty: 163 against 102 floors is x1.6, under x2.
    assert "rejected how_many: rule2: ×1.6 from its anchor, under ×2" in out
    assert "2 of 3 candidates made episodes; rejected 1 (33%): rule2 1" in out
    json.dumps(episodes)   # the renderer copies them as JSON


def test_the_revealed_values_are_the_source_records():
    """Pinned to the records as fetched 2026-11-16 (the brief's 2026-11-15
    values): a value or comparison drifting from the record fails here."""
    (gas, people), _ = playalong.select_day(playalong.candidates(), "", [])
    assert gas["hook"] == "Gas is $4.45 a gallon this October. What did it cost in 1990?"
    assert (gas["answer"], gas["comparison"], gas["options"]) == ("$1.04", "÷4.3", None)
    assert gas["source"] == {"name": "U.S. Bureau of Labor Statistics", "id": "APU000074714",
                             "value": 1.042, "fetched": "2026-11-16"}
    assert gas["credit"] == "Source: U.S. Bureau of Labor Statistics, series APU000074714."
    assert people["hook"] == "More people: Wyoming, or Washington, D.C.?"
    assert people["options"] == ["Wyoming", "Washington, D.C."]
    assert people["answer"] == "D.C."
    assert people["comparison"] == "D.C. 702,250 · Wyoming 587,618 (114,632 more)"
    assert people["source"]["value"] == 702250
    assert people["credit"] == "Source: U.S. Census Bureau, Vintage 2024 population estimates."
    assert [e["beat"] for e in (gas, people)] == ["Say your number.", "Pick one."]


def test_the_episode_matches_the_raw_files_it_was_read_from():
    raw = json.loads((playalong.ASSETS / "bls_APU000074714.json").read_text())
    month = {(d["year"], d["period"]): float(d["value"])
             for d in raw["Results"]["series"][0]["data"]}
    with open(playalong.ASSETS / "census_NST-EST2024-ALLDATA.csv", newline="") as f:
        pop = {r["NAME"]: int(r["POPESTIMATE2024"]) for r in csv.DictReader(f)}
    (gas, people), _ = playalong.select_day(playalong.candidates(), "", [])
    then, now = month[("1990", "M01")], month[("2026", "M10")]
    assert gas["answer"] == f"${then:.2f}" and f"${now:.2f}" in gas["hook"]
    assert gas["comparison"] == f"÷{now / then:.1f}"
    dc, wy = pop["District of Columbia"], pop["Wyoming"]
    assert people["comparison"] == f"D.C. {dc:,} · Wyoming {wy:,} ({dc - wy:,} more)"


def test_every_number_is_copied_from_the_record_by_code():
    """Change a record and the episode follows it: nothing is typed in."""
    episode, _ = playalong.select(_with(GAS, 1, value=0.991))
    assert (episode["answer"], episode["comparison"]) == ("$0.99", "÷4.5")
    assert episode["source"]["value"] == 0.991
    episode, _ = playalong.select(_with(PEOPLE, 1, value=600_000))
    assert episode["comparison"] == "D.C. 600,000 · Wyoming 587,618 (12,382 more)"


def test_values_are_shown_as_their_quantity_reads():
    assert playalong._fmt({"quantity": "price", "value": 4.454}) == "$4.45"
    assert playalong._fmt({"quantity": "population", "value": 702250}) == "702,250"
    assert playalong._fmt({"quantity": "date", "value": 1931}) == "1931"


def test_rule1_only_everyday_quantities_per_shape():
    assert _reason(_with(GAS, quantity="gdp")).startswith("rule1:")
    # Floors are everyday for how-many, not for a price question.
    assert _reason(_with(GAS, quantity="floors")).startswith("rule1:")
    assert _reason({"template": "trivia", "records": GAS["records"]}).startswith("rule1:")


def test_rule2_a_number_question_states_a_far_enough_anchor():
    assert _reason({"template": "how_many", "records": FLOORS["records"][1:]}) == \
        "rule2: a number question with no anchor"
    assert _reason(_with(FLOORS, 0, value=None)) == "rule2: a number question with no anchor"
    # 163 floors against 102 is x1.6: a stranger guesses it.
    assert _reason(FLOORS) == "rule2: ×1.6 from its anchor, under ×2"
    assert _reason(_with(GAS, 1, value=3.0)).startswith("rule2: ×1.5")
    assert _reason(_with(GAS, 1, value=0)).startswith("rule2: a value that is not")
    assert _reason(_with(GAS, 1, value="1.04")).startswith("rule2: a value that is not")
    # x2 or more ships, either way round (the answer above the anchor too).
    assert playalong.select(_with(FLOORS, 0, value=81, provenance="fetched"))[0]["answer"] == "163"


def test_rule2_a_pick_ships_only_when_a_city_beats_a_state():
    # The state wins: most would have picked it, so no surprise.
    assert _reason(_with(PEOPLE, 1, value=500_000)).startswith("rule2: no contrast")
    # Two states: no coded contrast says which most would pick.
    assert _reason(_with(PEOPLE, 1, kind="state")).startswith("rule2: no contrast")


def test_rule3_one_fact_one_unit_one_comparison():
    three = copy.deepcopy(GAS)
    three["records"].append(copy.deepcopy(GAS["records"][1]))
    assert _reason(three).startswith("rule3:")
    assert _reason(_with(GAS, 1, unit="litre")).startswith("rule3:")
    assert _reason(_with(GAS, 1, id="APU000072610")).startswith("rule3:")
    assert _reason(_with(PEOPLE, 1, source="Somewhere else")).startswith("rule3:")


def test_rule4_never_the_same_shape_or_a_shipped_subject():
    assert _reason(GAS, prev_template="price_then").startswith("rule4: the same shape")
    assert playalong.select(GAS, prev_template="bigger_of_two")[0]
    shipped = ["What is the best thing about living in Wyoming?"]
    assert _reason(PEOPLE, shipped=shipped).startswith("rule4: the subject has shipped")
    # A day's run: the second price question follows the first.
    episodes, rejects = playalong.select_day([GAS, copy.deepcopy(GAS)], "", [])
    assert len(episodes) == 1 and rejects == {"rule4": 1}


def test_rule4_reads_the_real_upload_log_when_given_none(capsys):
    episodes, _ = playalong.select_day(playalong.candidates(), "")
    assert len(episodes) == 2   # no shipped title names gas, Wyoming or D.C.


@pytest.mark.parametrize("change", [
    {"category": "poverty"}, {"category": "illness"}, {"category": "disaster"},
    {"category": "earthquakes"}, {"category": "weather extremes"},
    {"subject": "Deaths in Wyoming"}, {"subject": "Crime in D.C."}])
def test_rule5_nothing_that_invites_contempt(change):
    assert _reason(_with(PEOPLE, 0, **change)).startswith("rule5:")


def test_rule5_reads_the_candidates_category_too():
    assert _reason({**PEOPLE, "category": "homelessness"}).startswith("rule5:")


def test_a_hand_entered_value_never_ships():
    """Wikidata holds no floor count for the Empire State Building (fetched
    2026-11-16); the brief's 102 is entered by hand and marked so."""
    anchor = FLOORS["records"][0]
    assert anchor["provenance"] == "entered" and anchor["value"] == 102
    assert _reason(_with(FLOORS, 0, value=81)) == "unsourced: Q9188 P1101 was not fetched from its source"


def test_check_turn_refuses_a_number_the_records_do_not_hold():
    (gas, people), _ = playalong.select_day(playalong.candidates(), "", [])
    for episode in (gas, people):
        assert playalong.check_turn(episode["turn"], episode) == ""
    assert playalong.check_turn("Back in 1990 it was $1.04, now $4.45.", gas) == ""
    assert playalong.check_turn("That is 4.3 times less.", gas) == ""
    assert playalong.check_turn("Gas was $2 a gallon.", gas) == "2"
    assert playalong.check_turn("It costs four times as much.", gas) == "four"
    assert playalong.check_turn("Prices doubled, then twice again.", gas) == "twice"
    assert playalong.check_turn("Over a million people.", people) == "million"
    assert playalong.check_turn(
        "Seven hundred two thousand two hundred fifty people.", people) == ""
    assert playalong.check_turn("Seven hundred thousand people.", people) == "seven hundred thousand"
