# john1hsu.github.io

Landing page for my knowledge-graph sites: **https://john1hsu.github.io/**

Each graph lives in its own repo and publishes its own GitHub Pages site under this domain (for example https://john1hsu.github.io/chess-graph/). This page lists them with live article counts and the latest additions, read from each repo's `graph/index.json`.

`build.py` generates the page and `.github/workflows/pages.yml` deploys it on every push and once an hour, so the counts stay current without commits here. To add a graph, add a row to `GRAPHS` in `build.py`.

Preview locally:

```bash
python3 build.py && python3 -m http.server -d _site 8000
```
