#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import time
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data"
OUTPUT_JSON = OUTPUT_DIR / "cities.json"
OUTPUT_JS = OUTPUT_DIR / "cities.js"

NUMBER_RE = re.compile(r"^-?\d[\d,]*(?:\.\d+)?$")

CITY_META = [
    {
        "source_label": "New York, NY, United States",
        "label": "New York, United States",
        "city": "New York",
        "country": "United States",
        "lat": 40.7128,
        "lng": -74.0060,
    },
    {
        "source_label": "Mexico City, Mexico",
        "label": "Mexico City, Mexico",
        "city": "Mexico City",
        "country": "Mexico",
        "lat": 19.4326,
        "lng": -99.1332,
    },
    {
        "source_label": "Sao Paulo, Brazil",
        "label": "Sao Paulo, Brazil",
        "city": "Sao Paulo",
        "country": "Brazil",
        "lat": -23.5558,
        "lng": -46.6396,
    },
    {
        "source_label": "Buenos Aires, Argentina",
        "label": "Buenos Aires, Argentina",
        "city": "Buenos Aires",
        "country": "Argentina",
        "lat": -34.6037,
        "lng": -58.3816,
    },
    {
        "source_label": "London, United Kingdom",
        "label": "London, United Kingdom",
        "city": "London",
        "country": "United Kingdom",
        "lat": 51.5072,
        "lng": -0.1276,
    },
    {
        "source_label": "Paris, France",
        "label": "Paris, France",
        "city": "Paris",
        "country": "France",
        "lat": 48.8566,
        "lng": 2.3522,
    },
    {
        "source_label": "Berlin, Germany",
        "label": "Berlin, Germany",
        "city": "Berlin",
        "country": "Germany",
        "lat": 52.5200,
        "lng": 13.4050,
    },
    {
        "source_label": "Amsterdam, Netherlands",
        "label": "Amsterdam, Netherlands",
        "city": "Amsterdam",
        "country": "Netherlands",
        "lat": 52.3676,
        "lng": 4.9041,
    },
    {
        "source_label": "Istanbul, Turkey",
        "label": "Istanbul, Turkey",
        "city": "Istanbul",
        "country": "Turkey",
        "lat": 41.0082,
        "lng": 28.9784,
    },
    {
        "source_label": "Cairo, Egypt",
        "label": "Cairo, Egypt",
        "city": "Cairo",
        "country": "Egypt",
        "lat": 30.0444,
        "lng": 31.2357,
    },
    {
        "source_label": "Cape Town, South Africa",
        "label": "Cape Town, South Africa",
        "city": "Cape Town",
        "country": "South Africa",
        "lat": -33.9249,
        "lng": 18.4241,
    },
    {
        "source_label": "Dubai, United Arab Emirates",
        "label": "Dubai, United Arab Emirates",
        "city": "Dubai",
        "country": "United Arab Emirates",
        "lat": 25.2048,
        "lng": 55.2708,
    },
    {
        "source_label": "Mumbai, India",
        "label": "Mumbai, India",
        "city": "Mumbai",
        "country": "India",
        "lat": 19.0760,
        "lng": 72.8777,
    },
    {
        "source_label": "Bangkok, Thailand",
        "label": "Bangkok, Thailand",
        "city": "Bangkok",
        "country": "Thailand",
        "lat": 13.7563,
        "lng": 100.5018,
    },
    {
        "source_label": "Singapore, Singapore",
        "label": "Singapore, Singapore",
        "city": "Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lng": 103.8198,
    },
    {
        "source_label": "Seoul, South Korea",
        "label": "Seoul, South Korea",
        "city": "Seoul",
        "country": "South Korea",
        "lat": 37.5665,
        "lng": 126.9780,
    },
    {
        "source_label": "Tokyo, Japan",
        "label": "Tokyo, Japan",
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.6762,
        "lng": 139.6503,
    },
    {
        "source_label": "Sydney, Australia",
        "label": "Sydney, Australia",
        "city": "Sydney",
        "country": "Australia",
        "lat": -33.8688,
        "lng": 151.2093,
    },
    {
        "source_label": "Toronto, Canada",
        "label": "Toronto, Canada",
        "city": "Toronto",
        "country": "Canada",
        "lat": 43.6532,
        "lng": -79.3832,
    },
    {
        "source_label": "Nairobi, Kenya",
        "label": "Nairobi, Kenya",
        "city": "Nairobi",
        "country": "Kenya",
        "lat": -1.2921,
        "lng": 36.8219,
    },
]

SOURCES = {
    "rent": {
        "url": "https://www.numbeo.com/cost-of-living/prices_by_city.jsp?itemId=26&displayCurrency=USD",
        "values_per_row": 1,
        "pick_index": 0,
    },
    "cappuccino": {
        "url": "https://www.numbeo.com/cost-of-living/prices_by_city.jsp?itemId=114&displayCurrency=USD",
        "values_per_row": 1,
        "pick_index": 0,
    },
    "gym": {
        "url": "https://www.numbeo.com/cost-of-living/prices_by_city.jsp?itemId=40&displayCurrency=USD",
        "values_per_row": 1,
        "pick_index": 0,
    },
    "salary": {
        "url": "https://www.numbeo.com/cost-of-living/prices_by_city.jsp?itemId=105&displayCurrency=USD",
        "values_per_row": 1,
        "pick_index": 0,
    },
    "transitPass": {
        "url": "https://www.numbeo.com/cost-of-living/prices_by_city.jsp?itemId=20&displayCurrency=USD",
        "values_per_row": 1,
        "pick_index": 0,
    },
    "crime": {
        "url": "https://www.numbeo.com/crime/rankings_current.jsp",
        "values_per_row": 2,
        "pick_index": 0,
    },
    "pollution": {
        "url": "https://www.numbeo.com/pollution/rankings_current.jsp",
        "values_per_row": 2,
        "pick_index": 0,
    },
    "commute": {
        "url": "https://www.numbeo.com/traffic/rankings_current.jsp",
        "values_per_row": 5,
        "pick_index": 1,
    },
}


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.tokens: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return

        text = " ".join(unescape(data).split())
        if text:
            self.tokens.append(text)


def fetch_html(url: str) -> str:
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
    request = Request(
        url,
        headers={"User-Agent": user_agent},
    )
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception:
        result = subprocess.run(
            ["curl", "-fsSL", "-A", user_agent, url],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout


def extract_tokens(html: str) -> list[str]:
    parser = VisibleTextParser()
    parser.feed(html)
    return parser.tokens


def parse_number(token: str) -> float:
    return float(token.replace(",", ""))


def extract_rows(tokens: list[str], values_per_row: int) -> dict[str, list[float]]:
    start = next((index for index, token in enumerate(tokens) if token == "Rank"), 0)
    end = next(
        (
            index
            for index, token in enumerate(tokens[start:], start)
            if token.startswith("Last Update:")
        ),
        len(tokens),
    )
    city_labels = {item["source_label"] for item in CITY_META}
    rows: dict[str, list[float]] = {}

    for index in range(start, end):
        token = tokens[index]
        if token not in city_labels or token in rows:
            continue

        values: list[float] = []
        for look_ahead in range(index + 1, min(end, index + 12)):
            candidate = tokens[look_ahead]
            if NUMBER_RE.match(candidate):
                values.append(parse_number(candidate))
                if len(values) == values_per_row:
                    rows[token] = values
                    break

    return rows


def build_dataset() -> list[dict]:
    collected: dict[str, dict[str, list[float]]] = {}

    for metric_name, config in SOURCES.items():
        print(f"Fetching {metric_name} from {config['url']}")
        html = fetch_html(config["url"])
        tokens = extract_tokens(html)
        rows = extract_rows(tokens, config["values_per_row"])
        collected[metric_name] = rows
        time.sleep(1.1)

    dataset = []
    for city in CITY_META:
        metrics = {}
        source_label = city["source_label"]

        for metric_name, config in SOURCES.items():
            city_values = collected.get(metric_name, {}).get(source_label)
            if city_values is None:
                raise RuntimeError(
                    f"Missing {metric_name} value for '{source_label}'. "
                    "Adjust the city list or parsing logic."
                )

            metrics[metric_name] = round(city_values[config["pick_index"]], 2)

        dataset.append(
            {
                "label": city["label"],
                "city": city["city"],
                "country": city["country"],
                "lat": city["lat"],
                "lng": city["lng"],
                "metrics": metrics,
            }
        )

    return dataset


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset = build_dataset()

    OUTPUT_JSON.write_text(
        json.dumps(dataset, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    OUTPUT_JS.write_text(
        "window.STATGUESSR_CITIES = "
        + json.dumps(dataset, indent=2, ensure_ascii=True)
        + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_JS}")


if __name__ == "__main__":
    main()
