#!/usr/bin/env python3
"""Discover US federal grant opportunities from the official Grants.gov public API."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/us-grants-discovery.json"
URL = "https://api.grants.gov/v1/api/search2"

def fetch_page(start):
    body = {
        "rows": 100,
        "startRecordNum": start,
        "oppStatuses": "posted|forecasted",
    }
    req = Request(URL, data=json.dumps(body).encode("utf-8"), method="POST",
                  headers={"Content-Type": "application/json", "Accept": "application/json",
                           "User-Agent": "GlobalSupportRadar/0.1"})
    last_error = None
    for attempt in range(4):
        try:
            with urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Grants.gov API page {start} failed after 4 attempts: {last_error}")

def main():
    error = None
    records = []
    hit_count = 0
    try:
        for page in range(20):
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
                    "start_date": item.get("openDate") or None,
                    "deadline": item.get("closeDate") or None,
                    "country_code": "US",
                    "source_language": "en",
                    "status": item.get("oppStatus"),
                    "application_window_status": "forecasted" if str(item.get("oppStatus") or "").lower() == "forecasted" else "posted_status_requires_detail_page_check",
                    "eligibility_verified": False,
                    "amount_verified": False,
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
        "purpose": "Posted and forecasted federal funding opportunities returned by the official public Grants.gov API. Forecasted items are not presented as currently open application windows. Posted status, deadlines, funding amounts and eligibility must be checked on each official detail page; the API search result alone does not verify applicant eligibility.",
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
