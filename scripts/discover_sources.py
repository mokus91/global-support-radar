#!/usr/bin/env python3
"""Discover potentially relevant public datasets; never labels them as verified grants."""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "data/source-registry.json").read_text(encoding="utf-8"))
OUT = ROOT / "data/discovery-index.json"
ENDPOINT = "https://data.europa.eu/api/hub/search/search"
QUERIES = ["government grants", "public support programmes", "subsidies", "housing assistance", "agricultural funding", "business funding"]

def request_eu(query):
    body = json.dumps({"q": query, "filters": ["dataset"], "limit": 25, "page": 0}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type":"application/json", "Accept":"application/json", "User-Agent":"GlobalSupportRadar/0.1 (public-source discovery)"}, method="POST")
    with urllib.request.urlopen(req, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))

def pick(obj, *keys):
    for key in keys:
        value = obj.get(key)
        if value:
            return value
    return None

def main():
    records, errors = [], []
    for query in QUERIES:
        try:
            payload = request_eu(query)
            items = payload.get("result", {}).get("results") or payload.get("results") or []
            if isinstance(items, dict):
                items = items.get("results", [])
            for item in items:
                title = pick(item, "title", "name") or "Untitled dataset"
                if isinstance(title, dict):
                    title = next(iter(title.values()), "Untitled dataset")
                url = pick(item, "uri", "url", "landing_page", "landingPage")
                if isinstance(url, list):
                    url = url[0] if url else None
                if isinstance(url, dict):
                    url = next(iter(url.values()), None)
                if not url or urlparse(str(url)).scheme not in ("http", "https"):
                    continue
                records.append({"title": str(title), "url": str(url), "query": query, "source_id": "eu-data", "record_type": "dataset-discovery", "verification_status": "unverified"})
        except Exception as exc:
            errors.append({"source_id":"eu-data", "query":query, "error":str(exc)[:300]})
    unique = {}
    for item in records:
        unique[item["url"]] = item
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Discovery only. These are catalogue datasets, not verified grant or benefit offers.",
        "verified_programmes_count": 0,
        "discovered_datasets_count": len(unique),
        "records": sorted(unique.values(), key=lambda x: x["title"].lower()),
        "errors": errors
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Discovered {len(unique)} catalogue datasets; verified programmes: 0; errors: {len(errors)}")
    # A failed source is recorded but does not destroy the last known output.
    if not unique and errors and not OUT.exists():
        sys.exit(1)

if __name__ == "__main__":
    main()
