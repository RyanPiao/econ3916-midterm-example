"""Download step for the movie example (the README's 'how to get the data').

Writes three files into data/ and prints what it saved:
  films_wikipedia.csv  the two English box-office tables on Wikipedia's
                       "List of films based on video games" (live-action, animated)
  directors_wikidata.csv  every director linked in those tables, with the
                       birth date Wikidata holds for them
  cpi_fred.csv         CPIAUCSL, monthly, from FRED
  games_wikipedia.csv  for each film, the game or series its Wikipedia infobox says it is
                       "based on", and that page's first release year
Run once; the notebook reads the saved files, so it does not change when the page does.
    python get_data.py               # all four files
    python get_data.py --only games  # just games_wikipedia.csv
"""
import io, json, re, sys, urllib.parse, urllib.request
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup

UA = {"User-Agent": "ECON3916-midterm-example/1.0 (Northeastern University course)"}
PAGE = "https://en.wikipedia.org/wiki/List_of_films_based_on_video_games"

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()

# ---- games_wikipedia.csv: when did the game come out?
YEAR = r"\b(19[7-9]\d|20[0-2]\d)\b"

def wikitext(titles):
    out = {}
    for i in range(0, len(titles), 40):
        q = urllib.parse.urlencode({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                                    "titles": "|".join(titles[i:i + 40]), "redirects": 1, "format": "json", "formatversion": 2})
        j = json.loads(fetch("https://en.wikipedia.org/w/api.php?" + q))
        red = {r["from"]: r["to"] for r in j["query"].get("redirects", [])}
        norm = {r["from"]: r["to"] for r in j["query"].get("normalized", [])}
        pages = {p["title"]: p["revisions"][0]["slots"]["main"]["content"] for p in j["query"]["pages"] if "revisions" in p}
        for t in titles[i:i + 40]:
            k = norm.get(t, t)
            out[t] = pages.get(red.get(k, k), "")
    return out

def first_year(wt):
    # a franchise page: "origin = ''[[Game]]'' (1996)" or "years = 1996-present"; a game page: its release block
    for name in ["origin", "first_release_date", "first release date", "first_release", "first release", "years"]:
        m = re.search(r"\n\s*\|\s*" + name + r"\s*=([^\n]*)", wt, re.I)
        if m and re.search(YEAR, m.group(1)):
            return min(int(y) for y in re.findall(YEAR, m.group(1)))
    for name in ["released", "release", "launch date", "launched"]:
        m = re.search(r"\n\s*\|\s*" + name + r"\s*=", wt, re.I)
        if m:
            block = re.split(r"\n\s*\|\s*(genre|mode|modes|platform|platforms|director|producer|designer)\s*=", wt[m.end():m.end() + 700])[0]
            ys = [int(y) for y in re.findall(YEAR, block)]
            if ys:
                return min(ys)
    return None

def get_games(soup):
    rows = []
    for t in soup.find_all("table"):
        if "Worldwide box office" not in t.find("tr").get_text():
            continue
        if t.find_previous(["h2", "h3", "h4"]).get_text(strip=True) not in ("Live-action", "Animated"):
            continue
        # read_html handles the merged (rowspan) cells; the first cell of each row is the title, with its link
        dates = pd.read_html(io.StringIO(str(t)))[0]["Release date"].astype(str)
        trs = [row for row in t.find_all("tr")[1:] if row.find_all(["th", "td"])]
        assert len(trs) == len(dates), (len(trs), len(dates))
        for row, d in zip(trs, dates):
            a = row.find_all(["th", "td"])[0].find("a")
            y = re.search(r"(19|20)\d\d", d)
            rows.append({"title": row.find_all(["th", "td"])[0].get_text(" ", strip=True), "year": int(y.group()) if y else None,
                         "film_page": urllib.parse.unquote(a["href"].split("/wiki/")[1]).replace("_", " ") if a else None})
    films_wt = wikitext([r["film_page"] for r in rows if r["film_page"]])
    based = {}
    for r in rows:
        m = re.search(r"\n\s*\|\s*based[_ ]on\s*=(.*?)(?=\n\s*\|\s*[a-z_ ]+\s*=)", films_wt.get(r["film_page"], ""), re.S | re.I)
        based[r["title"], r["year"]] = re.findall(r"\[\[([^\]|#]+)", m.group(1)) if m else []
    src_wt = wikitext(sorted({l for v in based.values() for l in v}))
    for r in rows:
        found = [(l, first_year(src_wt.get(l, ""))) for l in based[r["title"], r["year"]]]
        found = [(l, y) for l, y in found if y]
        r["source_page"] = found[0][0] if found else None
        r["game_year"] = min(y for _, y in found) if found else None
    out = pd.DataFrame(rows)
    out["retrieved"] = date.today().isoformat()
    out.to_csv("data/games_wikipedia.csv", index=False)
    print("games", out.shape, "with a year:", out["game_year"].notna().sum())


html = fetch(PAGE.replace("/wiki/", "/w/index.php?title=") + "&action=render").decode()
soup = BeautifulSoup(html, "html.parser")
if "--only" in sys.argv and "games" in sys.argv:
    get_games(soup)
    sys.exit()
tables, links = [], {}
for t in soup.find_all("table"):
    if "Worldwide box office" not in t.find("tr").get_text():
        continue
    fmt = t.find_previous(["h2", "h3", "h4"]).get_text(strip=True)
    if fmt not in ("Live-action", "Animated"):
        continue                                   # the Japanese table has other columns
    df = pd.read_html(io.StringIO(str(t)))[0]
    df.insert(0, "format", fmt.lower())
    tables.append(df)
    for row in t.find_all("tr")[1:]:
        cells = row.find_all(["th", "td"])
        if len(cells) > 1:
            for a in cells[1].find_all("a"):
                href = a.get("href", "")
                if "/wiki/" in href and "redlink" not in href:
                    links[a.get_text(strip=True)] = urllib.parse.unquote(href.split("/wiki/")[1]).replace("_", " ")
films = pd.concat(tables, ignore_index=True)
films["retrieved"] = date.today().isoformat()
films.to_csv("data/films_wikipedia.csv", index=False)

rows, titles = [], sorted(set(links.values()))
for i in range(0, len(titles), 45):
    q = urllib.parse.urlencode({"action": "wbgetentities", "sites": "enwiki", "titles": "|".join(titles[i:i + 45]),
                                "props": "claims|sitelinks", "sitefilter": "enwiki", "format": "json", "redirects": "yes"})
    for qid, e in json.loads(fetch("https://www.wikidata.org/w/api.php?" + q))["entities"].items():
        if "sitelinks" not in e:
            continue
        c = e.get("claims", {}).get("P569")
        born = c[0]["mainsnak"]["datavalue"]["value"]["time"][1:11] if c and "datavalue" in c[0]["mainsnak"] else None
        rows.append({"wikipedia_title": e["sitelinks"]["enwiki"]["title"], "wikidata_id": qid, "born": born})
births = pd.DataFrame(rows)
names = pd.DataFrame([{"director": k, "wikipedia_title": v} for k, v in links.items()])
# a redirect (e.g. "Dwight Little") comes back under its target's title, so match on both
directors = names.merge(births, on="wikipedia_title", how="left")
directors.to_csv("data/directors_wikidata.csv", index=False)

open("data/cpi_fred.csv", "wb").write(fetch("https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"))
print("films", films.shape, "| directors", directors.shape, "with a birth date:", directors.born.notna().sum())
get_games(soup)
