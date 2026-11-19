#!/usr/bin/env python3
"""Discover US federal grant opportunities from the official Grants.gov public API."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/us-grants-discovery.json"
URL = "https://api.grants.gov/v1/api/search2"

def fetch_page(start):
    body = {
        "rows": 100,
        "startRecordNum": start,
        "oppStatuses": "posted|forecasted",
        "sortBy": "openDate|desc"
    }
    req = Request(URL, data=json.dumps(body).encode("utf-8"), method="POST",
                  headers={"Content-Type": "application/json", "Accept": "application/json",
                           "User-Agent": "GlobalSupportRadar/0.1"})
    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    error = None
    records = []
    hit_count = 0
    try:
        for page in range(10):
            payload = fetch_page(page * 100)
            if payload.get("errorcode") not in (0, "0", None):
                raise RuntimeError(str(payload.get("msg") or payload.get("errorcode")))
            data = payload.get("data") or {}
            hits = data.get("oppHits") or []
            hit_count = int(data.get("hitCount") or hit_count)
            for item in hits:
                oid = item.get("id")
                if not oid:
                    continue
                records.append({
                    "id": str(oid),
                    "title": item.get("title") or item.get("number") or "Untitled opportunity",
                    "identifier": item.get("number"),
                    "agency": item.get("agencyName") or item.get("agencyCode"),
                    "open_date": item.get("openDate"),
                    "deadline": item.get("closeDate") or None,
                    "status": item.get("oppStatus"),
                    "category_codes": item.get("alnist") or [],
                    "official_url": "https://www.grants.gov/search-results-detail/" + str(oid),
                    "source_id": "us-grants-gov",
                    "record_type": "official-api-discovery-candidate",
                    "verification_status": "unverified"
                })
            if len(hits) < 100 or len(records) >= hit_count:
                break
    except Exception as exc:
        error = str(exc)[:500]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "us-grants-gov",
        "source_url": "https://www.grants.gov/",
        "api_url": URL,
        "purpose": "Posted and forecasted federal funding opportunities returned by the official public Grants.gov API. Records remain unverified until their official detail pages and eligibility are checked.",
        "total_available": hit_count,
        "records_count": len(records),
        "records": records,
        "error": error
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Grants.gov: {len(records)} discovery candidates; error={error or 'none'}")

if __name__ == "__main__":
    main()
