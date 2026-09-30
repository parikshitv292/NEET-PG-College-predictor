# NEET PG 2025 Seat Predictor

Single-file rank, college and specialty predictor (HTML, Tailwind CDN, vanilla JS) built from the official NEET PG 2025 counselling Round 1, 2 and 3 seat allotment PDFs.

## Run
Open `index.html` in a browser, or enable GitHub Pages (Settings, Pages, Deploy from branch, `main` / root).

## Data pipeline
1. `scripts/parse.py` reads the three PDFs with `pdftotext -bbox` and assigns words to table columns using the fixed column boundaries of each round.
2. `scripts/build.py` normalizes course, institute, state and quota names and computes opening and closing rank per institute, course, quota and seat category for each round, writing `data/allotment-cutoffs.json`.
3. `scripts/template.html` is the app; the JSON replaces the `/*DATA*/null` placeholder to produce `index.html`.

Paths in the scripts point to `/home/claude`; edit them to your local folders. Requires Poppler (`pdftotext`) and Python 3.

## Notes
Cutoffs are allotment-based (last rank allotted in each round). The lists contain no state-quota seats. Chance percentages are a heuristic from one year of data, not a guarantee. Verify against official MCC information before choice filling.
