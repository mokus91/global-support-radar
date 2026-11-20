#!/usr/bin/env python3
"""Discover public EU Funding & Tenders call records; all results remain unverified."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import time

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
    for attempt in range(3):
        try:
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(3 * (attempt + 1))
    raise RuntimeError("EU Funding & Tenders API retry loop exhausted")

def first(meta, key, default=None):
    value = (meta or {}).get(key)
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default

def classify_opportunity_type(title, identifier="", record_type=""):
    """Conservative heuristic: separate clear service/contract notices, not grant calls mentioning procurement."""
    text = " ".join(str(value or "") for value in (title, identifier, record_type)).lower()
    explicit_contract_markers = (
        "service request", "contract notice", "contract award",
        "procurement procedure", "tender notice", "invitation to tender",
        "works contract", "supplies contract", "open tender for", "open tender:"
    )
    if any(marker in text for marker in explicit_contract_markers):
        return "procurement_candidate"
    # 'Procurement' can describe the subject of a grant. A call for proposals
    # remains a funding candidate unless an explicit contract marker exists.
    return "funding_candidate"

def main():
    error = None
    payload = {}
    pages_fetched = 0
    pagination_complete = False
    max_pages = 100
    try:
        payload = {"results": [], "totalResults": 0}
        for page in range(1, max_pages + 1):
            part = collect(page)
            pages_fetched += 1
            payload["results"].extend(part.get("results", []))
            payload["totalResults"] = part.get("totalResults", payload["totalResults"])
            if len(part.get("results", [])) < 100 or len(payload["results"]) >= int(payload["totalResults"] or 0):
                pagination_complete = True
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
        title = first(meta, "callTitle") or item.get("summary") or first(meta, "title") or "Untitled call"
        identifier = first(meta, "identifier") or ""
        opportunity_type = classify_opportunity_type(title, identifier, first(meta, "type"))
        candidates.append({
            "id": ref,
            "title": title,
            "opportunity_type": opportunity_type,
            "classification_basis": "title_identifier_keyword_heuristic; verify original notice",
            "official_url": item.get("url") or first(meta, "url") or ("https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/" + str(ref)),
            "identifier": first(meta, "identifier"),
            "programme": first(meta, "frameworkProgramme"),
            "start_date": first(meta, "startDate"),
            "deadline": first(meta, "deadlineDate") or first(meta, "closingDate"),
            "budget": first(meta, "budget"),
            "source_language": item.get("language") or first(meta, "language") or "en",
            "source_id": "eu-funding",
            "record_type": "current-deadline-discovery-candidate",
            "verification_status": "unverified",
            "status": first(meta, "status"),
            "status_code": first(meta, "status"),
            "portal_status_interpretation": "open-or-forthcoming-filter-result; not individually verified",
            "last_discovered_at": datetime.now(timezone.utc).isoformat()
        })
    # Always order dated opportunities by the nearest upcoming deadline; undated
    # records remain discoverable but are placed after dated records.
    candidates.sort(key=lambda row: (
        1 if not row.get("deadline") else 0,
        str(row.get("deadline") or "9999-12-31"),
        str(row.get("id") or "")
    ))
    candidate_output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-funding",
        "source_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
        "purpose": "Candidates returned by the official portal status filters, sorted by nearest upcoming deadline first; past closing dates are excluded where parseable. Records remain unverified; check the original call page before relying on status or eligibility.",
        "expired_deadline_records_excluded": expired_excluded,
        "status_filters": ["31094501", "31094502"],
        "sort_field": "deadlineDate",
        "sort_order": "ASC",
        "pages_fetched": pages_fetched,
        "maximum_pages": max_pages,
        "pagination_complete": pagination_complete,
        "records_count": len(candidates),
        "records": candidates,
        "error": error
    }
    (ROOT / "data/eu-open-calls-discovery.json").write_text(
        json.dumps(candidate_output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # Keep the audit file compact. The raw API response can exceed GitHub's
    # 100 MB per-file limit and is not needed by the website; the curated
    # candidate feed above contains the fields used by the frontend.
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-funding",
        "source_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
        "purpose": "Compact audit summary of the official API discovery run. The curated candidate feed is stored separately in eu-open-calls-discovery.json. Raw API payloads are intentionally not committed.",
        "verification_status": "unverified",
        "pages_fetched": pages_fetched,
        "maximum_pages": max_pages,
        "pagination_complete": pagination_complete,
        "sort_field": "deadlineDate",
        "sort_order": "ASC",
        "page_size": 100,
        "records_received": len(payload.get("results", [])),
        "total_results_reported": payload.get("totalResults", 0),
        "candidate_records": len(candidates),
        "expired_deadline_records_excluded": expired_excluded,
        "error": error
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if error:
        print("EU Funding & Tenders discovery failed: " + error)
    else:
        print(f"EU Funding & Tenders API response saved; {len(candidates)} current-deadline candidates; excluded {expired_excluded} past-deadline records (all remaining candidates unverified).")

if __name__ == "__main__":
    main()
