# john1hsu.github.io

Landing page for my knowledge-graph sites, quiz apps and world history: **https://john1hsu.github.io/**

Each graph, each quiz bank and the history lives in its own repo and publishes its own GitHub Pages site under this domain (for example https://john1hsu.github.io/chess-graph/ or https://john1hsu.github.io/aws-quiz-bank/). The page has three sections:

- **Quizzes**: the swipe-to-answer true/false apps, with live question counts read from each quiz bank's `index/questions.json`. Each quiz takes the accent color of the graph it draws from and links back to it.
- **History**: [world-history](https://john1hsu.github.io/world-history/), a daily chronicle of the world in dactylic hexameter, with live book, chapter and verse counts from its `index.json` and the first verse of the newest chapter.
- **Graphs**: the knowledge graphs, with live article counts and the latest additions read from each repo's `graph/index.json`. A graph with a quiz gets a "Practice quiz" link.

`build.py` generates the page and `.github/workflows/pages.yml` deploys it on every push and once an hour, so the counts stay current without commits here. To add a graph, add a row to `GRAPHS` in `build.py`; to add a quiz bank, add a row to `QUIZZES` naming the graph it draws from.

Preview locally:

```bash
python3 build.py && python3 -m http.server -d _site 8000
```
