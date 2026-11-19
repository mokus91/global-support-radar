#!/usr/bin/env python3
"""Discover public EU Funding & Tenders call records; all results remain unverified."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/eu-funding-discovery.json"
URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA&text=*&pageSize=100&pageNumber={page}&sortBy=deadlineDate&orderBy=ASC"
QUERY = {"bool": {"must": [
    {"terms": {"type": ["1", "2", "8"]}},
    {"terms": {"status": ["31094501", "31094502"]}}
]}}

def multipart(parts):
    boundary = "----GSR" + uuid.uuid4().hex
    chunks = []
    for name, value, content_type in parts:
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n'.encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            value.encode("utf-8"), b"\r\n"
        ])
    chunks.append(f"--{boundary}--\r\n".encode())
    return boundary, b"".join(chunks)

def collect(page=1):
    parts = [
        ("query", json.dumps(QUERY), "application/json"),
        ("languages", json.dumps(["en"]), "application/json"),
        ("displayLanguage", "en", "text/plain")
    ]
    boundary, body = multipart(parts)
    req = Request(URL.format(page=page), data=body, method="POST", headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; GlobalSupportRadar/0.1)",
        "Referer": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/"
    })
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))

def first(meta, key, default=None):
    value = (meta or {}).get(key)
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default

def main():
    error = None
    payload = {}
    try:
        payload = {"results": [], "totalResults": 0}
        for page in range(1, 21):
            part = collect(page)
            payload["results"].extend(part.get("results", []))
            payload["totalResults"] = part.get("totalResults", payload["totalResults"])
            if len(part.get("results", [])) < 100 or len(payload["results"]) >= payload["totalResults"]:
                break
    except Exception as exc:
        error = str(exc)[:500]
    # Keep only official portal open/forthcoming status candidates.
    # They remain discovery candidates until each call page is individually checked.
    candidates = []
    expired_excluded = 0
    seen = set()
    today = datetime.now(timezone.utc).date()
    for item in payload.get("results", []):
        meta = item.get("metadata") or {}
        ref = item.get("reference") or first(meta, "REFERENCE")
        if not ref or ref in seen:
            continue
        seen.add(ref)
        deadline_value = first(meta, "deadlineDate") or first(meta, "closingDate")
        if deadline_value:
            try:
                deadline_date = datetime.fromisoformat(str(deadline_value).replace("Z", "+00:00")).date()
                if deadline_date < today:
                    expired_excluded += 1
                    continue
            except ValueError:
                pass
        candidates.append({
            "id": ref,
            "title": first(meta, "callTitle") or item.get("summary") or first(meta, "title") or "Untitled call",
            "official_url": item.get("url") or first(meta, "url"),
            "identifier": first(meta, "identifier"),
            "programme": first(meta, "frameworkProgramme"),
            "start_date": first(meta, "startDate"),
            "deadline": first(meta, "deadlineDate") or first(meta, "closingDate"),
            "budget": first(meta, "budget"),
            "source_language": item.get("language") or first(meta, "language") or "en",
            "source_id": "eu-funding",
            "record_type": "current-deadline-discovery-candidate",
            "verification_status": "unverified",
            "status_code": first(meta, "status"),
            "last_discovered_at": datetime.now(timezone.utc).isoformat()
        })
    candidate_output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-funding",
        "source_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
        "purpose": "Candidates returned by the official portal OPEN/FORTHCOMING status filters, with past closing dates excluded where parseable. Records remain unverified; check the original call page before relying on status or eligibility.",
        "expired_deadline_records_excluded": expired_excluded,
        "status_filters": ["31094501", "31094502"],
        "records_count": len(candidates),
        "records": candidates,
        "error": error
    }
    (ROOT / "data/eu-open-calls-discovery.json").write_text(
        json.dumps(candidate_output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # Preserve the raw official API response for audit and future field mapping.
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-funding",
        "source_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
        "purpose": "Official call discovery only. Every result requires individual page verification before publication.",
        "verification_status": "unverified",
        "error": error,
        "response": payload
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if error:
        print("EU Funding & Tenders discovery failed: " + error)
    else:
        print(f"EU Funding & Tenders API response saved; {len(candidates)} current-deadline candidates; excluded {expired_excluded} past-deadline records (all remaining candidates unverified).")

if __name__ == "__main__":
    main()
