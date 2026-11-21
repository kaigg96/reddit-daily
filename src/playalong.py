"""A play-along episode: one question with a true, sourced answer a stranger
can guess at before they know it. The viewer commits, then sees whether they
were right. First slice: the selector, with no renderer yet.

No model writes a number. `select` frames a candidate (two source records) as
an episode, and every value shown or spoken is copied from a record by code.
`turn`, the one clause a model will later write, is a fixed line per shape
here, and `check_turn` refuses any turn stating a number the episode does not
hold. The records are public files fetched once and committed
(`assets/playalong/`, with where and when in `sources.json`): this module makes
no network call and no model call.
"""
import csv
import json
import re
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal

from . import config, insights, ownquestions

ASSETS = config.ROOT / "assets" / "playalong"

PRICE_THEN, BIGGER, HOW_MANY = "price_then", "bigger_of_two", "how_many"
TEMPLATES = (PRICE_THEN, BIGGER, HOW_MANY)
BEAT = {PRICE_THEN: "Say your number.", BIGGER: "Pick one.", HOW_MANY: "Guess."}
# The clause a model will write later; fixed per shape in this slice, and
# free of numbers, so `check_turn` passes it whatever the records hold.
TURN = {PRICE_THEN: "Prices creep up so slowly you never feel the climb.",
        BIGGER: "A city can outgrow a whole state.",
        HOW_MANY: "Height adds up faster than you think."}
TOMORROW = "Back tomorrow with another to guess."

# Rule 1, guessable not knowable: the everyday quantities a stranger has a
# feel for, per shape. Anything else is trivia nobody can guess at.
ALLOWED = {PRICE_THEN: {"price"}, BIGGER: {"population"},
           HOW_MANY: {"floors", "height", "date"}}
# Rule 2: a number question's answer is at least this far from its anchor,
# and a pick's two values this far apart (the viewer bar's "twice as far").
MIN_DISTANCE = 2.0
# A ratio shown as "1.0×" says nothing changed ("11.0×" is fine).
NO_CHANGE = re.compile(r"(?<![\d.])1\.0×")
# Rule 2 for a pick, on top of the distance, the coded contrast "a city beats
# a state": the answer ships only when it is the place most would not pick.
CITY_KINDS = {"city", "district"}
# Rule 5, nothing that invites contempt (or grief): checked against every
# record's subject and category, the candidate's category and the hook.
DENY = re.compile(
    r"\b(pover\w*|poor|homeless\w*|ill|illness\w*|disease\w*|cancer|sick\w*|"
    r"disaster\w*|earthquake\w*|quake\w*|hurricane\w*|tornado\w*|flood\w*|"
    r"wildfire\w*|drought\w*|storm\w*|heat ?waves?|weather|death\w*|dead|died|"
    r"mortality|fatal\w*|crime\w*|criminal\w*|murder\w*|homicide\w*|kill\w*|"
    r"prison\w*|overdose\w*|suicide\w*|war|wars|famine\w*)\b", re.I)

# The spoken names the source files lack. `hook` is how a question names one
# unit of the series, written out so its case survives (never lowercased).
SERIES = {"APU000074714": {"subject": "Gas", "hook": "a gallon of regular gas",
                           "quantity": "price", "unit": "gallon", "category": "fuel"},
          # T7's less familiar price (11-16): sold by the pound, its 1990 price unknown.
          "APU0000703112": {"subject": "Ground beef", "hook": "a pound of ground beef",
                            "quantity": "price", "unit": "pound", "category": "food"}}
GAS_SERIES, BEEF_SERIES = "APU000074714", "APU0000703112"


def _price(subject, hook, unit="pound", category="food"):
    return {"subject": subject, "hook": hook, "quantity": "price", "unit": unit,
            "category": category}


# T13's supply (11-21): BLS average prices with a January 1990 month and a
# 2026 one, named as BLS names the item. Gas is left out as too well known.
SUPPLY_SERIES = {
    "APU0000703112": SERIES[BEEF_SERIES],
    "APU0000701111": _price("White flour", "a pound of all-purpose white flour"),
    "APU0000701312": _price("White rice", "a pound of uncooked long-grain white rice"),
    "APU0000702111": _price("White bread", "a pound of white pan bread"),
    "APU0000702421": _price("Chocolate chip cookies", "a pound of chocolate chip cookies"),
    "APU0000703111": _price("Ground chuck", "a pound of ground chuck"),
    "APU0000703213": _price("Chuck roast", "a pound of boneless chuck roast"),
    "APU0000703311": _price("Round roast", "a pound of boneless round roast"),
    "APU0000703511": _price("Round steak", "a pound of boneless round steak"),
    "APU0000703613": _price("Sirloin steak", "a pound of boneless sirloin steak"),
    "APU0000704111": _price("Bacon", "a pound of sliced bacon"),
    "APU0000706111": _price("Whole chicken", "a pound of fresh whole chicken"),
    "APU0000710411": _price("Ice cream", "a half gallon of ice cream", "half gallon"),
    "APU0000711311": _price("Navel oranges", "a pound of navel oranges"),
    "APU0000711412": _price("Grapefruit", "a pound of grapefruit"),
    "APU0000712112": _price("White potatoes", "a pound of white potatoes"),
    "APU0000712211": _price("Iceberg lettuce", "a pound of iceberg lettuce"),
    "APU0000713111": _price("Frozen orange juice", "16 ounces of frozen orange juice concentrate",
                            "16 ounces"),
    "APU0000715211": _price("Sugar", "a pound of white sugar"),
    "APU0000717311": _price("Coffee", "a pound of ground coffee"),
    "APU0000718311": _price("Potato chips", "16 ounces of potato chips", "16 ounces"),
    "APU000072610": _price("Electricity", "a kilowatt-hour of electricity", "kilowatt-hour",
                           "energy"),
    "APU000072620": _price("Piped gas", "a therm of piped utility gas", "therm", "energy"),
    "APU000072511": _price("Heating oil", "a gallon of No. 2 heating oil", "gallon", "energy"),
}
SERIES.update(SUPPLY_SERIES)
# Census Vintage 2024 places (SUMLEV 162, name and state as the file has them)
# and the small states they can beat at x2.
SUPPLY_CITIES = {("New York city", "New York"): "New York City",
                 ("Los Angeles city", "California"): "Los Angeles",
                 ("Chicago city", "Illinois"): "Chicago",
                 ("Houston city", "Texas"): "Houston",
                 ("Phoenix city", "Arizona"): "Phoenix",
                 ("Philadelphia city", "Pennsylvania"): "Philadelphia",
                 ("San Antonio city", "Texas"): "San Antonio",
                 ("San Diego city", "California"): "San Diego",
                 ("Dallas city", "Texas"): "Dallas"}
SUPPLY_STATES = ("Wyoming", "Vermont", "Alaska", "North Dakota", "South Dakota", "Delaware",
                 "Rhode Island", "Montana", "Maine", "New Hampshire", "Hawaii")
# Well-known buildings with a Wikidata floor count (P1101), named by their
# fetched English label.
SUPPLY_BUILDINGS = (
    "Q12495", "Q18547", "Q494895", "Q189476", "Q1077308", "Q29294", "Q317034", "Q83101",
    "Q80852", "Q546221", "Q94193", "Q83063", "Q80813", "Q4255374", "Q271695", "Q18640924",
    "Q11274", "Q270407", "Q35525", "Q39054", "Q11208", "Q54109", "Q220728", "Q167566",
    "Q191161", "Q673223", "Q207870", "Q461371", "Q745964", "Q739612", "Q19104", "Q22041180",
    "Q836531", "Q189883", "Q188190", "Q478926", "Q91274", "Q677555", "Q750444", "Q656743",
    "Q336246", "Q542783")
PLACES = {"District of Columbia": {"subject": "Washington, D.C.", "short": "D.C.",
                                   "kind": "district"}}
BUILDINGS = {"Q12495": "the Burj Khalifa", "Q9188": "the Empire State Building"}
BLS = "U.S. Bureau of Labor Statistics"
CENSUS = "U.S. Census Bureau"
WIKIDATA = "Wikidata"


def _manifest():
    return json.loads((ASSETS / "sources.json").read_text())


def bls_records(path=ASSETS / "bls_APU000074714.json"):
    """One record per month in a BLS API reply (average price series)."""
    fetched = _manifest()[path.name]["fetched"]
    out = []
    for series in json.loads(path.read_text())["Results"]["series"]:
        sid, meta = series["seriesID"], SERIES[series["seriesID"]]
        for d in series["data"]:
            out.append({"source": BLS, "id": sid, "subject": meta["subject"],
                        "short": meta["subject"], "hook": meta["hook"], "kind": "series",
                        "quantity": meta["quantity"], "unit": meta["unit"],
                        "value": float(d["value"]), "period": f"{d['year']}-{d['period'][1:]}",
                        "month": d["periodName"], "category": meta["category"],
                        "fetched": fetched, "provenance": "fetched",
                        "credit": f"Source: {BLS}, series {sid}."})
    return out


def census_records(path=ASSETS / "census_NST-EST2024-ALLDATA.csv"):
    """One record per state-level row of the Vintage 2024 estimates (SUMLEV
    040: the 50 states and D.C.)."""
    fetched = _manifest()[path.name]["fetched"]
    out = []
    with open(path, newline="", encoding="latin-1") as f:
        for r in csv.DictReader(f):
            if r["SUMLEV"] != "040":
                continue
            place = PLACES.get(r["NAME"], {"subject": r["NAME"], "short": r["NAME"],
                                           "kind": "state"})
            out.append({"source": CENSUS, "id": f"NST-EST2024 POPESTIMATE2024 {r['NAME']}",
                        "subject": place["subject"], "short": place["short"],
                        "kind": place["kind"], "quantity": "population", "unit": "people",
                        "value": int(r["POPESTIMATE2024"]), "period": "2024",
                        "category": "population", "fetched": fetched, "provenance": "fetched",
                        "credit": f"Source: {CENSUS}, Vintage 2024 population estimates."})
    return out


def wikidata_records(path=ASSETS / "wikidata_P1101.json"):
    """One floor count (P1101) per item. A preferred claim beats a normal
    one, a deprecated one is never read. An item with no claim falls back to a
    value `sources.json` says was entered by hand, marked so: it never ships."""
    entry = _manifest()[path.name]
    out = []
    for qid, data in json.loads(path.read_text()).items():
        claims = data.get("claims", {}).get("P1101", [])
        best = ([c for c in claims if c["rank"] == "preferred"]
                or [c for c in claims if c["rank"] == "normal"])
        if best:
            value, provenance = float(best[0]["mainsnak"]["datavalue"]["value"]["amount"]), "fetched"
        elif "P1101" in entry.get("entered", {}).get(qid, {}):
            value, provenance = entry["entered"][qid]["P1101"], "entered"
        else:
            continue
        value = int(value) if float(value).is_integer() else value
        name = BUILDINGS.get(qid) or data.get("label") or qid
        out.append({"source": WIKIDATA, "id": f"{qid} P1101", "subject": name,
                    "short": name, "kind": "building", "quantity": "floors", "unit": "floors",
                    "value": value, "period": "", "category": "buildings",
                    "fetched": entry["fetched"], "provenance": provenance,
                    "credit": f"Data: Wikidata (CC0), {qid} P1101."})
    return out


def candidates(price=GAS_SERIES):
    """The three worked examples, from the committed records: a price then and
    now (gas unless `price` names another BLS series on file), D.C. against
    Wyoming, the Burj Khalifa against the Empire State."""
    gas = {r["period"]: r for r in bls_records(ASSETS / f"bls_{price}.json")}
    people = {r["short"]: r for r in census_records()}
    floors = {r["id"].split()[0]: r for r in wikidata_records()}
    return [{"template": PRICE_THEN, "records": [gas["2026-10"], gas["1990-01"]]},
            {"template": BIGGER, "records": [people["Wyoming"], people["D.C."]]},
            {"template": HOW_MANY, "records": [floors["Q9188"], floors["Q12495"]]}]


def _ambiguous(path):
    """The items whose floor count Wikidata gives twice over, two normal
    claims that disagree and none preferred (Willis Tower: 108 and 110)."""
    out = set()
    for qid, data in json.loads(path.read_text()).items():
        claims = data.get("claims", {}).get("P1101", [])
        if not any(c["rank"] == "preferred" for c in claims) and len(
                {c["mainsnak"]["datavalue"]["value"]["amount"] for c in claims
                 if c["rank"] == "normal"}) > 1:
            out.add(qid)
    return out


def _supply_pool():
    """{template: [candidate, ...]} from the committed supply files only."""
    prices = []
    for r in bls_records(ASSETS / "bls_AP_supply.json"):
        prices.append(r)
    by_id = {}
    for r in prices:
        by_id.setdefault(r["id"], []).append(r)
    price = [{"template": PRICE_THEN, "records": sorted(rs, key=lambda r: r["period"], reverse=True)}
             for rs in by_id.values() if len(rs) == 2]
    people = census_places()
    cities = sorted((r for r in people if r["kind"] == "city"), key=lambda r: r["value"])
    states = sorted((r for r in people if r["kind"] == "state"), key=lambda r: r["value"])
    picks = []
    for city in cities:   # the smallest city takes the smallest state it beats x2
        state = next((s for s in states if city["value"] >= MIN_DISTANCE * s["value"]), None)
        if state:
            states.remove(state)
            picks.append({"template": BIGGER, "records": [state, city]})
    path = ASSETS / "wikidata_P1101_landmarks.json"
    floors = [r for r in wikidata_records(path) if r["id"].split()[0] not in _ambiguous(path)]
    floors.sort(key=lambda r: r["value"], reverse=True)
    half = len(floors) // 2
    tall, low = floors[:half], floors[half:]
    how = []
    for i, (t, s) in enumerate(zip(tall, low)):
        how.append({"template": HOW_MANY, "records": [s, t] if i % 2 else [t, s]})
    return {PRICE_THEN: price, BIGGER: picks, HOW_MANY: how}


def supply():
    """The play-along arm's candidates in shipping order, built only from the
    committed fetched files (T13). Each passes `select` after the ones before
    it with nothing shipped: the next always takes another shape (rule 4),
    the shape with the most left first, so two shapes alternate to the end.
    A candidate no order can ship (a rule-1, -2 or -5 refusal, a rewording of
    an earlier hook) is left out."""
    pool = {k: list(v) for k, v in _supply_pool().items()}
    out, prev, shipped = [], "", []
    while True:
        for template in sorted((t for t in TEMPLATES if t != prev and pool[t]),
                               key=lambda t: (-len(pool[t]), TEMPLATES.index(t))):
            pick = next((c for c in pool[template] if select(c, prev, shipped)[0]), None)
            if pick:
                break
        else:
            return out
        pool[template].remove(pick)
        out.append(pick)
        prev = template
        shipped.append(select(pick)[0]["hook"])


def census_places(path=ASSETS / "census_SUB-EST2024.csv"):
    """The Vintage 2024 city and town file's rows: a city (SUMLEV 162) under
    its spoken name, a state (040) under its own."""
    fetched = _manifest()[path.name]["fetched"]
    out = []
    with open(path, newline="", encoding="latin-1") as f:
        for r in csv.DictReader(f):
            if r["SUMLEV"] == "162":
                name, kind = SUPPLY_CITIES.get((r["NAME"], r["STNAME"])), "city"
                if not name:
                    continue
                rid = f"SUB-EST2024 POPESTIMATE2024 {r['NAME']}, {r['STNAME']}"
            elif r["SUMLEV"] == "040":
                name, kind, rid = r["NAME"], "state", f"SUB-EST2024 POPESTIMATE2024 {r['NAME']}"
            else:
                continue
            out.append({"source": CENSUS, "id": rid, "subject": name, "short": name,
                        "kind": kind, "quantity": "population", "unit": "people",
                        "value": int(r["POPESTIMATE2024"]), "period": "2024",
                        "category": "population", "fetched": fetched, "provenance": "fetched",
                        "credit": f"Source: {CENSUS}, Vintage 2024 population estimates."})
    return out


def _half_up(v, decimals):
    """`v` rounded half up, as a reader rounds: the float 6.755 is stored a
    hair under, so round() and an f-string gave $6.75 where the record's
    $6.755 is $6.76 (fifth judging, 11-17: check 5's "true")."""
    return Decimal(str(v)).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP)


def _fmt(record):
    """A record's value as shown and spoken, copied by code."""
    v = record["value"]
    if record["quantity"] == "price":
        return f"${_half_up(v, 2):,.2f}"
    if record["quantity"] == "date":
        return str(int(v))   # a year, never "1,931"
    return f"{v:,}" if float(v).is_integer() else f"{_half_up(v, 1):,.1f}"


def _cap(text):
    return text[:1].upper() + text[1:]


def _distance(a, b):
    lo, hi = sorted((float(a), float(b)))
    return hi / lo if lo > 0 else float("inf")


def _credit(records):
    if records[-1]["source"] == WIKIDATA:   # answer first, as the brief's line
        ids = [r["id"] for r in reversed(records)]
        return f"Data: Wikidata (CC0), {'; '.join(ids)}."
    return " ".join(dict.fromkeys(r["credit"] for r in records))


def _frame(template, records):
    """The episode, every value copied from `records` by code."""
    if template == PRICE_THEN:
        anchor, then = records
        r = anchor["value"] / then["value"]
        when = f"{then['month']} {then['period'][:4]}"
        named = anchor.get("hook") or f"a {anchor['unit']} of {anchor['subject']}"
        # The anchor's month with its year: "this October" is wrong once the
        # year turns, and the show starts in January (T13's review, 11-21).
        hook = (f"What did {named} cost in {when}? "
                f"In {anchor['month']} {anchor['period'][:4]} it was {_fmt(anchor)}.")
        answer, ans_rec, options = _fmt(then), then, None
        more = f"{r:.1f}× more now" if r >= 1 else f"{1 / r:.1f}× less now"
        # Under the answer it reads "$1.04 / in Jan 1990 / 4.3× more now".
        comparison = f"in {then['month'][:3]} {then['period'][:4]}\n{more}"
    elif template == HOW_MANY:
        anchor, ans_rec = records
        hook = (f"{_cap(anchor['subject'])} has {_fmt(anchor)} {anchor['unit']}. "
                f"{_cap(ans_rec['subject'])}?")
        answer, options = _fmt(ans_rec), None
        comparison = f"{_fmt(ans_rec)} vs {_fmt(anchor)}"
    else:
        a, b = records
        ans_rec, other = (a, b) if a["value"] > b["value"] else (b, a)
        hook = f"More people: {a['subject']}, or {b['subject']}?"
        options, answer = [a["subject"], b["subject"]], ans_rec["short"]
        # One line per name, so no line splits a name from its number.
        comparison = f"{ans_rec['short']} {_fmt(ans_rec)}\n{other['short']} {_fmt(other)}"
    return {"hook": hook, "beat": BEAT[template], "options": options, "answer": answer,
            "comparison": comparison, "turn": TURN[template], "tomorrow": TOMORROW,
            "source": {"name": ans_rec["source"], "id": ans_rec["id"],
                       "value": ans_rec["value"], "fetched": ans_rec["fetched"]},
            "credit": _credit(records)}


def _repeats_subject(records, hook, shipped):
    """The shipped title that names one of the subjects, or rewords the hook
    (`ownquestions.near_repeat`, R13's words and bar), else ""."""
    for title in shipped:
        words = insights.question_words(title)
        for r in records:
            subject = insights.question_words(r["subject"])
            if subject and subject <= words:
                return title
    # The rewording check sees only the question, never the show's frame: the
    # words a hook keeps whatever its subjects are ("cost", "january", "1990",
    # the month, the unit "pound") are every price hook's, so two prices on
    # different items read as rewordings of each other (T13, 11-21). The frame
    # is derived per hook: its words less its records' subject words, and the
    # same words are dropped from each shipped title.
    subjects = frozenset().union(*(insights.question_words(r["subject"]) for r in records))
    frame = insights.question_words(hook) - subjects
    core = " ".join(sorted(insights.question_words(hook) - frame))
    titles = {" ".join(sorted(insights.question_words(t) - frame)): t for t in shipped}
    near = ownquestions.near_repeat(core, list(titles))
    return titles.get(near, "") if near else ""


def select(candidate, prev_template="", shipped=()):
    """(episode, "") for a candidate that passes the five rules, else
    (None, "ruleN: why")."""
    template, records = candidate.get("template"), list(candidate.get("records") or [])
    # 1. Guessable, not knowable.
    if template not in TEMPLATES:
        return None, f"rule1: no such shape {template!r}"
    off = [r.get("quantity") for r in records if r.get("quantity") not in ALLOWED[template]]
    if off:
        return None, f"rule1: {off[0]!r} is not an everyday quantity for {template}"
    # A name that holds its own number gives the answer away ("Landmark 81").
    told = [r["subject"] for r in records if isinstance(r.get("value"), (int, float))
            and float(r["value"]).is_integer()
            and str(int(r["value"])) in re.findall(r"\d+", r.get("subject") or "")]
    if told:
        return None, f"rule1: {told[0]!r} names its own number"
    # 2. A surprising distance, from a stated anchor. The viewer bar's "twice
    # as far" governs every shape: a pick's two values too.
    if template in (PRICE_THEN, HOW_MANY):
        if len(records) < 2 or records[0].get("value") in (None, ""):
            return None, "rule2: a number question with no anchor"
    elif len(records) < 2:
        return None, "rule2: a pick needs two options"
    if not all(isinstance(r.get("value"), (int, float)) and r["value"] > 0
               for r in records[:2]):
        return None, "rule2: a value that is not a positive number has no distance"
    d = _distance(records[0]["value"], records[1]["value"])
    if d < MIN_DISTANCE:
        between = "from its anchor" if template != BIGGER else "between its two options"
        return None, f"rule2: ×{d:.1f} {between}, under ×{MIN_DISTANCE:g}"
    if template == BIGGER:
        win, lose = sorted(records[:2], key=lambda r: r["value"], reverse=True)
        if not (win.get("kind") in CITY_KINDS and lose.get("kind") == "state"):
            return None, (f"rule2: no contrast says most would not pick {win['short']}"
                          f" ({win.get('kind')} beats {lose.get('kind')})")
    # 3. One fact, one unit, one comparison.
    if len(records) != 2:
        return None, f"rule3: {len(records)} records, not one comparison of two"
    if len({r["quantity"] for r in records}) != 1 or len({r["unit"] for r in records}) != 1:
        return None, "rule3: two quantities or two units"
    if len({r["source"] for r in records}) != 1 or (
            template == PRICE_THEN and len({r["id"] for r in records}) != 1):
        return None, "rule3: the two values are not one fact from one source"
    episode = _frame(template, records)
    if template != BIGGER and _fmt(records[0]) not in episode["hook"]:
        return None, "rule2: the hook does not state its anchor"
    if NO_CHANGE.search(episode["comparison"]):
        return None, "rule2: the comparison would read 1.0×, no change at all"
    # 4. Fresh shape.
    if template == prev_template:
        return None, f"rule4: the same shape as the previous episode ({template})"
    near = _repeats_subject(records, episode["hook"], shipped)
    if near:
        return None, f"rule4: the subject has shipped ({near[:60]})"
    # 5. Nothing that invites contempt.
    texts = [candidate.get("category") or "", episode["hook"]] + [
        f"{r.get('subject', '')} {r.get('category', '')}" for r in records]
    bad = next((m.group(0) for t in texts for m in [DENY.search(t)] if m), "")
    if bad:
        return None, f"rule5: {bad!r} invites contempt"
    # A hand-entered value is not a source record, whatever its credit says.
    entered = [r["id"] for r in records if r.get("provenance") != "fetched"]
    if entered:
        return None, f"unsourced: {entered[0]} was not fetched from its source"
    bad = check_turn(episode["turn"], episode)
    if bad:
        return None, f"turn: states {bad!r}, which the records do not hold"
    return episode, ""


def select_day(cands, prev_template="", shipped=None):
    """(episodes, rejects by rule) over a day's candidates, in order: each
    episode is the next to ship, so the next must take another shape. Prints
    each reject's reason and the day's reject rate."""
    if shipped is None:
        from . import log   # read only: the titles already uploaded
        shipped = log.uploaded_titles()
    shipped = list(shipped)
    episodes, rejects = [], Counter()
    for c in cands:
        episode, why = select(c, prev_template, shipped)
        if episode:
            episodes.append(episode)
            prev_template = c["template"]
            shipped.append(episode["hook"])
        else:
            rejects[why.split(":")[0]] += 1
            print(f"Play-along: rejected {c.get('template')}: {why}")
    n = len(cands)
    by_rule = ", ".join(f"{k} {v}" for k, v in sorted(rejects.items())) or "none"
    print(f"Play-along: {len(episodes)} of {n} candidates made episodes; rejected "
          f"{n - len(episodes)} ({(n - len(episodes)) / n if n else 0:.0%}): {by_rule}")
    return episodes, rejects


_ONES = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
_TENS = {w: 10 * i for i, w in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety".split(), start=2)}
_SCALES = {"hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000,
           "trillion": 1_000_000_000_000}
_WORDS = {"dozen": 12, "twice": 2, "double": 2, "triple": 3, "half": 0.5}
# Quantities stated without a value the records could hold ("prices
# quadrupled", "thousands more", "a quarter of", "½"): a turn using one is
# refused outright, since no record can confirm it. "Quarter" and "fifth" in
# a name ("the French Quarter") are refused too: the safe side.
_VAGUE = re.compile(r"\b(?:hundreds|thousands|millions|billions|trillions?|dozens|thrice|"
                    r"doubl(?:ed|es|ing)|tripl(?:ed|es|ing)|"
                    r"(?:quadr|quint|sext|sept|oct)upl(?:e|ed|es|ing)|halv(?:e|ed|es|ing)|"
                    r"(?:two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|many)fold|"
                    r"quarters?|thirds?|fifths?|sixths?|sevenths?|eighths?|ninths?|tenths?)\b"
                    r"|[¼-¾⅐-⅞]")
_DIGITS = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _numbers(text):
    """Every number `text` states: (as written, value), digits and words."""
    out = [(m.group(0), float(m.group(0).replace(",", ""))) for m in _DIGITS.finditer(text)]
    total = current = 0
    said = []

    def flush():
        if said:
            out.append((" ".join(said), float(total + current)))
        said.clear()
        return 0, 0

    for w in re.findall(r"[a-z]+", text.lower()) + [""]:
        small = _ONES.get(w, _TENS.get(w))
        if small is not None:
            # "sixty three" is one number; "three seven" and "twenty thirty"
            # are two.
            if current % 100 and not (said[-1] in _TENS and small < 10):
                total, current = flush()
            said.append(w)
            current += small
        elif w in _SCALES:
            said.append(w)
            current = (current or 1) * _SCALES[w]
            if _SCALES[w] >= 1000:
                total, current = total + current, 0
        elif w == "and" and said and said[-1] in _SCALES:
            continue   # "one hundred and sixty"
        else:
            total, current = flush()
            if w in _WORDS:
                out.append((w, float(_WORDS[w])))
    return out


def _held(value, written, allowed):
    decimals = len(written.split(".")[1]) if "." in written and written[0].isdigit() else 0
    return any(float(_half_up(a, decimals)) == value if decimals else a == value for a in allowed)


def check_turn(turn, episode):
    """The first number `turn` states that the episode does not hold, else "".
    The episode holds only what code copied from its records: the numbers in
    its hook, options, answer, comparison and source value."""
    shown = " ".join([episode["hook"], " ".join(episode.get("options") or []),
                      episode["answer"], episode["comparison"]])
    allowed = {v for _, v in _numbers(shown)}
    value = episode["source"]["value"]
    if isinstance(value, (int, float)):
        allowed.add(float(value))
    vague = _VAGUE.search((turn or "").lower())
    if vague:
        return vague.group(0)
    for written, v in _numbers(turn or ""):
        if not _held(v, written, allowed):
            return written
    return ""
