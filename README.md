# OECD GHG Earnest and Deceptive Visualizations (A2)

Two static charts from OECD greenhouse gas emissions (1990–2019): an earnest multi-country index chart and a deceptive single-country chart, plus a short write-up.

## Data source

- **Dataset**: OECD Environment Statistics — Greenhouse gas emissions (total CO₂ equivalent, all sectors), 1990–2019.
- **Countries**: United States, United Kingdom, Germany, Japan, Canada.
- **File**: `data/ghg_emissions.csv` (columns: `country`, `year`, `emissions_mt`).

To regenerate the CSV (OECD-aligned embedded data), run:

```bash
py data/fetch_oecd_ghg.py
```

Alternatively, export the same series from [OECD Data Explorer](https://data-explorer.oecd.org/) (Air and GHG emissions → Greenhouse gas emissions Inventories) and save as `data/ghg_emissions.csv`.

## Run instructions

1. Install dependencies: `py -m pip install -r requirements.txt`
2. Generate charts: `py make_charts.py`
3. Outputs: `a2_earnest.png`, `a2_deceptive.png`

## Files

- `make_charts.py` — Builds both visualizations.
- `writeup.md` — Four-paragraph write-up.
- `a2_earnest.png`, `a2_deceptive.png` — Final images (after running `make_charts.py`).
