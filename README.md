# Do younger directors make better video-game movies?

ECON 3916 midterm project, course example. Critics' scores for films based on video games, 1993–2025.

[Open the notebook in Colab](https://colab.research.google.com/github/RyanPiao/econ3916-midterm-example/blob/main/midterm-example-movies.ipynb) · [Report (PDF)](report/midterm-report.pdf)

## Question

Among English-language films based on video games, 1993–2025, are films by younger directors rated better by critics (the Rotten Tomatoes score), holding the release year and the format (live-action or animated) constant?

## Hypothesis

Younger directors are more likely to have grown up playing the game they adapt, so they should make better films: a negative coefficient on the director's age.

## Data

| File | Source | What it holds |
|---|---|---|
| `data/films_wikipedia.csv` | [Wikipedia, "List of films based on video games"](https://en.wikipedia.org/wiki/List_of_films_based_on_video_games) | the live-action and animated tables: title, director, release date, Rotten Tomatoes score and review count, budget (each cited to Rotten Tomatoes, Box Office Mojo or The Numbers) |
| `data/directors_wikidata.csv` | [Wikidata](https://www.wikidata.org) | each linked director's date of birth (P569) |
| `data/cpi_fred.csv` | [FRED, CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) | CPI-U, monthly, to put budgets in 2024 prices |

All three were downloaded on 2026-11-03 by `get_data.py`.

## How to run

1. Open the notebook in Colab (link above) and run the cells top to bottom. The cell after Setup downloads the three files in `data/` from this repository.
2. To rebuild `data/` from the original sources instead, run `python get_data.py`. The Wikipedia page changes, so a new download can give slightly different numbers.

Every number in the report is printed by the notebook's last code cell, "Numbers my report quotes".

## Finding

A director ten years younger goes with a critics' score 1.7 points higher (95% CI -4.6 to +8.1 points, N = 53). That is the sign the hypothesis predicts, but the data cannot rule out no association. The release year matters far more: each later year goes with 1.21 points more. The estimate is a conditional association; age is only a stand-in for having played the game.
