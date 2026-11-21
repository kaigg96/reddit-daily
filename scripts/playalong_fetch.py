"""Fetch the play-along supply's public files once, trim each to what is used,
and record it in assets/playalong/sources.json (E1 T13). Free sources only:
BLS's keyless API v1 (two POSTs of 25 series), the Census Vintage 2024 city
and town file, and Wikidata's wbgetentities (CC0). No model, no voice.

    venv/bin/python scripts/playalong_fetch.py
"""
import csv
import datetime
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import playalong  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
BLS_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
CENSUS_URL = ("https://www2.census.gov/programs-surveys/popest/datasets/"
              "2020-2024/cities/totals/sub-est2024.csv")
WIKIDATA_URL = "https://www.wikidata.org/w/api.php"
BLS_FILE, CENSUS_FILE, WIKIDATA_FILE = (
    "bls_AP_supply.json", "census_SUB-EST2024.csv", "wikidata_P1101_landmarks.json")


def _get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_bls():
    """January 1990 and the latest month of each supply series."""
    ids = [s for s in playalong.SUPPLY_SERIES]
    by_id = {}
    for year in ("1990", "2026"):
        body = json.dumps({"seriesid": ids, "startyear": year, "endyear": year}).encode()
        reply = json.loads(_get(BLS_URL, body, {"Content-Type": "application/json"}))
        assert reply["status"] == "REQUEST_SUCCEEDED", reply
        for s in reply["Results"]["series"]:
            by_id.setdefault(s["seriesID"], []).extend(s["data"])
    series = []
    for sid in ids:
        data = by_id.get(sid, [])
        jan = [d for d in data if d["year"] == "1990" and d["period"] == "M01"]
        recent = sorted((d for d in data if d["year"] == "2026" and d["period"] != "M13"),
                        key=lambda d: d["period"], reverse=True)
        if jan and recent:
            series.append({"seriesID": sid, "data": [recent[0], jan[0]]})
    out = {"status": "REQUEST_SUCCEEDED", "Results": {"series": series}}
    return out, ("POST " + BLS_URL + " " + json.dumps(
        {"seriesid": ids, "startyear": "1990", "endyear": "1990"}) + "; the same for 2026")


def fetch_census():
    text = _get(CENSUS_URL).decode("latin-1")
    keep = set(playalong.SUPPLY_CITIES) | set(playalong.SUPPLY_STATES)
    cols = ["SUMLEV", "STATE", "PLACE", "NAME", "STNAME", "POPESTIMATE2024"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, cols, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in csv.DictReader(io.StringIO(text)):
        if (r["SUMLEV"] == "162" and (r["NAME"], r["STNAME"]) in playalong.SUPPLY_CITIES) or \
                (r["SUMLEV"] == "040" and r["NAME"] in playalong.SUPPLY_STATES):
            w.writerow(r)
    return buf.getvalue(), CENSUS_URL


def fetch_wikidata():
    ids = list(playalong.SUPPLY_BUILDINGS)
    params = {"action": "wbgetentities", "ids": "|".join(ids), "props": "labels|claims",
              "languages": "en", "format": "json"}
    reply = json.loads(_get(WIKIDATA_URL + "?" + urllib.parse.urlencode(params)))
    out = {}
    for qid in ids:
        e = reply["entities"][qid]
        claims = [{"mainsnak": {"property": "P1101",
                                "datavalue": c["mainsnak"].get("datavalue")},
                   "rank": c["rank"], "id": c["id"]}
                  for c in e.get("claims", {}).get("P1101", [])
                  if c["mainsnak"].get("datavalue")]
        out[qid] = {"label": e.get("labels", {}).get("en", {}).get("value", ""),
                    "claims": {"P1101": claims}}
    return out, (WIKIDATA_URL + "?action=wbgetentities&ids=" + "|".join(ids)
                 + "&props=labels|claims&languages=en&format=json")


def main():
    today = datetime.date.today().isoformat()
    manifest = json.loads((playalong.ASSETS / "sources.json").read_text())
    bls, bls_url = fetch_bls()
    (playalong.ASSETS / BLS_FILE).write_text(json.dumps(bls, indent=1) + "\n")
    manifest[BLS_FILE] = {"fetched": today, "url": bls_url,
                          "note": "Trimmed to each series' January 1990 and latest 2026 month."}
    census, census_url = fetch_census()
    (playalong.ASSETS / CENSUS_FILE).write_text(census)
    manifest[CENSUS_FILE] = {"fetched": today, "url": census_url,
                             "note": "Trimmed to six columns and the city (162) and state "
                                     "(040) rows used."}
    wd, wd_url = fetch_wikidata()
    (playalong.ASSETS / WIKIDATA_FILE).write_text(json.dumps(wd, indent=1, ensure_ascii=False) + "\n")
    manifest[WIKIDATA_FILE] = {"fetched": today, "url": wd_url,
                               "note": "Trimmed to each item's English label and P1101 claims."}
    (playalong.ASSETS / "sources.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"{len(bls['Results']['series'])} series, {census.count(chr(10)) - 1} census rows, "
          f"{len(wd)} buildings")


if __name__ == "__main__":
    main()
