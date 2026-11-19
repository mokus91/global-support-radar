#!/usr/bin/env python3
"""Discover candidate datasets from the official EU portal; never claim they are verified grants."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/discovery-index.json"
ENDPOINT = "https://data.europa.eu/api/hub/search/search"
QUERIES = [
    "government grants", "public support programmes", "subsidies",
    "housing assistance", "agricultural funding", "business funding",
    "scholarships", "energy efficiency support"
]

def request_eu(query):
    # The documented public Search API supports GET /search with q, filters, page and limit.
    params = urlencode({"q": query, "filters": "dataset", "limit": 50, "page": 0})
    req = urllib.request.Request(
        ENDPOINT + "?" + params,
        headers={"Accept": "application/json", "User-Agent": "GlobalSupportRadar/0.1 (+https://mokus91.github.io/global-support-radar/)"},
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))

def localized(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("en", "hu"):
            if isinstance(value.get(key), str):
                return value[key]
        for item in value.values():
            if isinstance(item, str):
                return item
    if isinstance(value, list) and value:
        return localized(value[0])
    return None

def extract_items(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    # The portal has returned both nested and top-level result envelopes over time.
    for key in ("results", "result", "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            for nested in ("results", "items", "data"):
                if isinstance(value.get(nested), list):
                    return value[nested]
    return []

def main():
    records, errors = [], []
    for query in QUERIES:
        try:
            payload = request_eu(query)
            for item in extract_items(payload):
                if not isinstance(item, dict):
                    continue
                title = localized(item.get("title") or item.get("name")) or "Untitled dataset"
                url = localized(item.get("uri") or item.get("url") or item.get("landing_page") or item.get("landingPage"))
                if not url or urlparse(url).scheme not in ("http", "https"):
                    continue
                records.append({
                    "title": title, "url": url, "query": query,
                    "source_id": "eu-data", "record_type": "dataset-discovery",
                    "verification_status": "unverified"
                })
        except Exception as exc:
            errors.append({"source_id": "eu-data", "query": query, "error": str(exc)[:300]})
    unique = {item["url"]: item for item in records}
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Discovery only. Catalogue datasets are not verified grant or benefit offers.",
        "verified_programmes_count": 0,
        "discovered_datasets_count": len(unique),
        "records": sorted(unique.values(), key=lambda x: x["title"].lower()),
        "errors": errors
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Discovered {len(unique)} catalogue datasets; verified programmes: 0; errors: {len(errors)}")
    if not unique and errors:
        print("WARNING: no catalogue results were returned; inspect API errors above.", file=sys.stderr)

if __name__ == "__main__":
    main()
