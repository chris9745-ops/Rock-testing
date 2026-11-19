# Rockefeller Chargeback UAT status

Static dashboard published to rock-testing.netlify.app.

- `site/index.html`: the page. It reloads `data.json` every minute.
- `site/data.json`: generated from the UAT tracker by `scripts/build_data.py`. It is the only file that changes on a refresh.
- `netlify.toml`: publishes `site/` (no build step) and disables caching of `data.json`.

## Refreshing
1. Export the tracker's `results` and `defects` collections as JSON files into `<dir>/results/` and `<dir>/defects/`.
2. Run `python3 scripts/build_data.py <dir> data`.
3. Commit and push `site/data.json`. Netlify redeploys automatically.

## Tracker v2 (`/v2/`)
- `v2/tracker.html`: the tracker page. The same file is published as the live Claude artifact (shared store, editable) and wrapped into `site/v2/index.html` for Netlify, where it reads `site/v2/data.json` and is read-only.
- Refresh: export the v2 tracker's collections (`meta`, `areas`, `cases`, `testdata`, `results`, `defects`, `activity`) as `<dir>/<collection>/<doc_id>.json`, run `python3 scripts/build_v2.py <dir>`, then commit and push `site/v2/`.
