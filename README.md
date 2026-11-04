# Did they grow up with the game?

ECON 3916 midterm project, course example. Critics' scores for films based on video games, 1993–2025.

[Open the notebook in Colab](https://colab.research.google.com/github/RyanPiao/econ3916-midterm-example/blob/main/midterm-example-movies.ipynb) · [Report (PDF)](report/midterm-report.pdf)

## Question

Among English-language films based on video games, 1993–2025, are films whose directors were younger when the game came out rated better by critics (the Rotten Tomatoes score), holding the release year and the format (live-action or animated) constant?

## Hypothesis

A director who was young when the game came out is more likely to have grown up playing it, so should make a better film of it: a negative coefficient on the director's age when the game came out (the game's first release year minus the director's birth year).

## Data

| File | Source | What it holds |
|---|---|---|
| `data/films_wikipedia.csv` | [Wikipedia, "List of films based on video games"](https://en.wikipedia.org/wiki/List_of_films_based_on_video_games) | the live-action and animated tables: title, director, release date, Rotten Tomatoes score and review count, budget (each cited to Rotten Tomatoes, Box Office Mojo or The Numbers) |
| `data/directors_wikidata.csv` | [Wikidata](https://www.wikidata.org) | each linked director's date of birth (P569) |
| `data/games_wikipedia.csv` | Wikipedia: each film's infobox "based on" page | the game or series each film is based on, and its first release year |
| `data/second_search.csv` | searched by hand, 2026-11-04 | every gap searched a second time, with its source: 7 values found, 9 confirmed missing |
| `data/rt_spot_check.csv` | Rotten Tomatoes, 2026-11-04 | the 5 most recent films' scores checked against the site |
| `data/fx_usd_per_gbp_fred.csv` | [FRED, DEXUSUK](https://fred.stlouisfed.org/series/DEXUSUK) | dollars per pound, to convert the one budget given in pounds |
| `data/cpi_fred.csv` | [FRED, CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) | CPI-U, monthly, to put budgets in 2024 prices |

All four were downloaded on 2026-11-03 by `get_data.py` (the game years on 2026-11-04, with `python get_data.py --only games`).

## How to run

1. Open the notebook in Colab (link above) and run the cells top to bottom. The cell after Setup downloads the four files in `data/` from this repository.
2. To rebuild `data/` from the original sources instead, run `python get_data.py`. The Wikipedia page changes, so a new download can give slightly different numbers.

Every number in the report is printed by the notebook's last code cell, "Numbers my report quotes".

## Finding

Before any controls, films by directors who were younger when the game came out are rated better: -0.72 points per year of age (95% CI -1.17 to -0.27). Most of that goes with the release year: recent films adapt games their directors met younger, and recent films are rated much better. Holding the year and the format fixed, a director ten years younger when the game came out goes with a score 3.0 points higher (95% CI -1.9 to +7.9, N = 57). The hypothesis is neither supported nor rejected.
