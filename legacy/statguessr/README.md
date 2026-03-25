# StatGuessr

StatGuessr is a lightweight browser game where each round reveals a handful of
city metrics and the player has to click the correct city on the map.

## What is in this version

- 5-round seeded challenges for easy sharing in streams or competitions
- Click-to-guess world map with distance-based scoring
- Clue cards built from rent, cappuccino, gym, crime, commute, pollution, and
  two bonus metrics
- Local city snapshot generated from public Numbeo pages

## Run locally

From the project root:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## Refresh the dataset

The game uses a local snapshot in `data/cities.js`.
To rebuild it from public Numbeo pages:

```bash
python3 tools/fetch_numbeo.py
```

The script also writes a JSON copy to `data/cities.json`.

## Deploy

This project is a static site, so Vercel can deploy it directly from the repo
root with no build step.

```bash
vercel
vercel --prod
```

## Data note

This is a small, local gameplay snapshot sourced from public Numbeo pages for a
demo-sized city list. It is not a bulk mirror of Numbeo data.
