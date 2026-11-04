# Do older directors make bigger hits?

ECON 3916 midterm project, course example. Box office for films based on video games, 1993–2025.

[Open the notebook in Colab](https://colab.research.google.com/github/RyanPiao/econ3916-midterm-example/blob/main/midterm-example-movies.ipynb) · [Report (PDF)](report/midterm-report.pdf)

## Question

Among English-language films based on video games, 1993–2025, do films by older directors earn more at the worldwide box office, holding the release year and the format (live-action or animated) constant?

## Data

| File | Source | What it holds |
|---|---|---|
| `data/films_wikipedia.csv` | [Wikipedia, "List of films based on video games"](https://en.wikipedia.org/wiki/List_of_films_based_on_video_games) | the live-action and animated tables: title, director, release date, budget, worldwide gross (each figure cites Box Office Mojo or The Numbers) |
| `data/directors_wikidata.csv` | [Wikidata](https://www.wikidata.org) | each linked director's date of birth (P569) |
| `data/cpi_fred.csv` | [FRED, CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) | CPI-U, monthly, to put dollars in 2024 prices |

All three were downloaded on 2026-11-03 by `get_data.py`.

## How to run

1. Open the notebook in Colab (link above) and run the cells top to bottom. The cell after Setup downloads the three files in `data/` from this repository.
2. To rebuild `data/` from the original sources instead, run `python get_data.py`. The Wikipedia page changes, so a new download can give slightly different numbers.

Every number in the report is printed by the notebook's last code cell, "Numbers my report quotes".

## Finding

A director one year older goes with a 2.4% higher worldwide gross (95% CI -3.0% to +8.0%, N = 51). The data cannot rule out no association, and the estimate is a conditional association, not the effect of experience: franchise sequels, which go to experienced directors, are not in the model.
