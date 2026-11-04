"""Download step for the movie example (the README's 'how to get the data').

Writes three files into data/ and prints what it saved:
  films_wikipedia.csv  the two English box-office tables on Wikipedia's
                       "List of films based on video games" (live-action, animated)
  directors_wikidata.csv  every director linked in those tables, with the
                       birth date Wikidata holds for them
  cpi_fred.csv         CPIAUCSL, monthly, from FRED
Run once; the notebook reads the saved files, so it does not change when the page does.
"""
import io, json, urllib.parse, urllib.request
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup

UA = {"User-Agent": "ECON3916-midterm-example/1.0 (Northeastern University course)"}
PAGE = "https://en.wikipedia.org/wiki/List_of_films_based_on_video_games"

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()

html = fetch(PAGE.replace("/wiki/", "/w/index.php?title=") + "&action=render").decode()
soup = BeautifulSoup(html, "html.parser")
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
