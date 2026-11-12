#!/usr/bin/env python3
"""Build the landing page for John's knowledge-graph sites.

Usage:
  python3 build.py              # fetches each graph's index.json from GitHub, writes _site/
  python3 build.py out_dir      # writes somewhere else
  GRAPHS_LOCAL=/path python3 build.py   # read <path>/<repo>/graph/index.json instead (offline preview)

Each graph repo publishes its own GitHub Pages site at https://john1hsu.github.io/<repo>/.
This page lists them with live counts. The Pages workflow rebuilds it hourly, so the counts
stay current without touching this repo.
"""
from __future__ import annotations

import html
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = "john1hsu"
HERE = Path(__file__).resolve().parent

# repo, title, blurb, accent (light, dark), article path prefix inside the site
GRAPHS = [
    ("salesforce-knowledge-graph", "Salesforce",
     "Features, APIs, limits, products and certifications, each checked against the current release.",
     ("#075A8C", "#7CC0EC"), "articles/"),
    ("aws-graph", "AWS",
     "Services, quotas, pricing models and architecture patterns, re-verified after every re:Invent.",
     ("#B35C00", "#F2B266"), "articles/"),
    ("ai-knowledge-graph", "Artificial Intelligence",
     "From ML foundations and AI history to transformers, agents, safety and governance.",
     ("#4B3FA6", "#ADA4F2"), "articles/"),
    ("business-knowledge-graph", "Business",
     "Strategy, finance, accounting, marketing, operations and management, with the evidence behind each idea.",
     ("#7A3B12", "#EDB389"), "articles/"),
    ("communication-graph", "Communication",
     "Evidence-checked techniques for listening, writing, presenting, feedback, meetings and hard conversations.",
     ("#0C6A62", "#6FCFC2"), "a/"),
    ("critical-thinking-graph", "Critical Thinking",
     "Logic, argument, fallacies, cognitive biases, evidence and better decisions.",
     ("#2444A0", "#8DA8F2"), "a/"),
    ("wisdom-graph", "Wisdom",
     "Practices, virtues and teachings for judging, deciding and living well, from research and the great traditions.",
     ("#8A5A12", "#E0B261"), "a/"),
    ("usa-graph", "United States",
     "Land, Native nations, history, the Constitution, government, rights, people, economy and culture of the U.S.",
     ("#A3242F", "#F0939A"), "a/"),
    ("chess-graph", "Chess",
     "Openings, strategy, tactics, endgames, history, players and computer chess.",
     ("#2F6B4F", "#86C9A4"), "articles/"),
]

e = lambda s: html.escape(str(s), quote=True)  # noqa: E731


def load_index(repo: str) -> list[dict] | None:
    local = os.environ.get("GRAPHS_LOCAL")
    try:
        if local:
            return json.loads((Path(local) / repo / "graph" / "index.json").read_text(encoding="utf-8"))
        url = f"https://raw.githubusercontent.com/{OWNER}/{repo}/main/graph/index.json"
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as ex:  # a missing graph shouldn't take the whole page down
        print(f"warning: {repo}: {ex}", file=sys.stderr)
        return None


def slug(node_id: str) -> str:
    return node_id.split(":", 1)[1]


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "_site"
    out.mkdir(parents=True, exist_ok=True)

    cards, recent, accents = [], [], []
    tot_articles = tot_sources = 0
    for i, (repo, title, blurb, (light, dark), prefix) in enumerate(GRAPHS):
        site = f"https://{OWNER}.github.io/{repo}/"
        accents.append(f".g{i}{{--gc:{light}}}"
                       f"@media (prefers-color-scheme: dark){{.g{i}{{--gc:{dark}}}}}")
        idx = load_index(repo)
        if idx:
            n = len(idx)
            areas = len({a.get("domain") for a in idx if a.get("domain")})
            srcs = len({u for a in idx for u in a.get("source_urls") or []})
            last = max((str(a.get("created", "")) for a in idx), default="")
            tot_articles += n
            tot_sources += srcs
            for a in idx:
                recent.append((str(a.get("created", "")), a["title"], f"{site}{prefix}{slug(a['id'])}.html", title, i))
            meta = "".join(f'<span><b>{k}</b> {w if k == 1 else w + "s"}</span>'
                           for k, w in [(n, "article"), (areas, "area"), (srcs, "source")])
            when = f'<p class="when">Last addition {e(last)}</p>' if last else ""
        else:
            meta, when = '<span>Counts unavailable right now</span>', ""
        cards.append(f"""
<li class="card g{i}">
  <a class="cover" href="{site}" aria-label="{e(title)} knowledge graph"></a>
  <h3>{e(title)}</h3>
  <p class="blurb">{e(blurb)}</p>
  <p class="meta">{meta}</p>
  {when}
  <p class="links"><a href="{site}">Open site</a><a href="https://github.com/{OWNER}/{repo}">Source</a></p>
</li>""")

    recent.sort(key=lambda r: (r[0], r[1]), reverse=True)
    recent_li = "".join(
        f'<li class="g{i}"><a href="{e(u)}">{e(t)}</a><span>{e(g)} · {e(d)}</span></li>'
        for d, t, u, g, i in recent[:10])
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    css = (HERE / "style.css").read_text(encoding="utf-8") + "\n" + "\n".join(accents)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Knowledge Graphs</title>
<meta name="description" content="Cited, cross-linked knowledge graphs on Salesforce, AWS, AI, business, communication, critical thinking, wisdom, the United States and chess, each growing by one researched article an hour.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400..800&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<style>{css}</style>
</head>
<body>
<header class="masthead">
  <span class="wordmark">john1hsu</span>
  <nav aria-label="Site"><a href="https://github.com/{OWNER}">GitHub</a></nav>
</header>
<main>
  <section class="hero">
    <h1>Knowledge graphs</h1>
    <p class="lede">Nine cited, cross-linked maps of the things I work on and study. Each grows by one researched article an hour, and every claim links to the source behind it.</p>
    <p class="stat">{tot_articles} articles · {tot_sources} cited sources · {len(GRAPHS)} graphs</p>
  </section>
  <section aria-labelledby="graphs-h">
    <h2 id="graphs-h" class="visually-hidden">Graphs</h2>
    <ul class="cards">{"".join(cards)}</ul>
  </section>
  <section class="recent" aria-labelledby="recent-h">
    <h2 id="recent-h">Recently added</h2>
    <ul>{recent_li}</ul>
  </section>
</main>
<footer class="colophon"><p>Counts refreshed {built}. Built from <a href="https://github.com/{OWNER}/{OWNER}.github.io">{OWNER}/{OWNER}.github.io</a>.</p></footer>
</body>
</html>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / "icon.svg").write_text((HERE / "icon.svg").read_text(encoding="utf-8"), encoding="utf-8")
    (out / ".nojekyll").write_text("")
    print(f"Landing page written to {out} ({tot_articles} articles across {len(GRAPHS)} graphs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
