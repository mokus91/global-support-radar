#!/usr/bin/env python3
"""Discover Hungarian open-data catalogue records related to public support.
This is dataset metadata discovery only; it does not identify active grant calls.
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://t.data.gov.hu/api/3/action/package_search"
QUERIES = ["támogatás", "pályázat", "agrártámogatás", "lakhatási támogatás",
           "vállalkozásfejlesztés", "ösztöndíj", "energiahatékonyság"]
OUT = Path("data/hu-open-data-discovery.json")


def fetch(query):
    params = urllib.parse.urlencode({"q": query, "rows": 50, "start": 0})
    req = urllib.request.Request(API + "?" + params, headers={
        "User-Agent": "GlobalSupportRadar/1.0 (public-interest dataset discovery)",
        "Accept": "application/json"
    })
    with urllib.request.urlopen(req, timeout=35) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("success") is not True:
        raise RuntimeError("CKAN API returned success=false")
    result = payload.get("result") or {}
    return result.get("results") or []


def main():
    records, errors = {}, []
    for query in QUERIES:
        try:
            for item in fetch(query):
                key = item.get("id") or item.get("name") or item.get("title")
                if not key:
                    continue
                records[key] = {
                    "id": key,
                    "title": item.get("title") or item.get("name") or "Untitled dataset",
                    "name": item.get("name"),
                    "url": item.get("url") or item.get("portal_url"),
                    "metadata_created": item.get("metadata_created"),
                    "metadata_modified": item.get("metadata_modified"),
                    "organization": (item.get("organization") or {}).get("title"),
                    "license_id": item.get("license_id"),
                    "notes": item.get("notes"),
                    "tags": [t.get("name") for t in item.get("tags", []) if t.get("name")],
                    "source_id": "hu-national-open-data",
                    "record_type": "dataset-discovery",
                    "verification_status": "unverified"
                }
        except Exception as exc:
            errors.append({"query": query, "error": str(exc)})
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "https://t.data.gov.hu/",
        "api": API,
        "record_type": "open-data-dataset-discovery-not-grant-listings",
        "query_count": len(QUERIES),
        "result_count": len(records),
        "errors": errors,
        "records": list(records.values())
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} dataset metadata records; {len(errors)} query errors.")
    if errors and not records:
        raise RuntimeError("No CKAN query succeeded; see output JSON for details.")


if __name__ == "__main__":
    main()
