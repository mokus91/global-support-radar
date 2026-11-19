#!/usr/bin/env python3
"""Discover Australian research grants from the official ARC Data Portal API.
This is a research-grants dataset, not a complete list of all Australian benefits or grants.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/au-arc-grants-discovery.json"
API = "https://dataportal.arc.gov.au/NCGP/API/grants"

def pick(obj, *keys):
    for key in keys:
        if key in obj and obj[key] not in (None, ""):
            return obj[key]
    return None

def main():
    records, error, pages = [], None, 0
    try:
        for page in range(1, 6):
            url = f"{API}?page%5Bnumber%5D={page}&page%5Bsize%5D=100"
            req = Request(url, headers={"User-Agent": "GlobalSupportRadar/0.1", "Accept": "application/vnd.api+json, application/json"})
            with urlopen(req, timeout=45) as response:
                payload = json.loads(response.read().decode("utf-8"))
            items = payload.get("data", [])
            if not isinstance(items, list):
                raise ValueError("Unexpected ARC API response: data is not a list")
            pages += 1
            for item in items:
                attrs = item.get("attributes") or {}
                if not isinstance(attrs, dict):
                    attrs = {}
                title = pick(attrs, "grant-title", "grantTitle", "title", "project-title", "projectTitle", "scheme-name", "schemeName")
                if not title:
                    continue
                identifier = pick(attrs, "grant-number", "grantNumber", "grant-id", "grantId", "id") or item.get("id")
                records.append({
                    "id": str(identifier) if identifier is not None else None,
                    "title": str(title),
                    "identifier": str(identifier) if identifier is not None else None,
                    "administering_organisation": pick(attrs, "admin-org-name", "adminOrgName", "administering-organisation", "administeringOrganisation"),
                    "funding_year": pick(attrs, "funding-commencement-year", "fundingCommencementYear", "commencement-year"),
                    "amount": pick(attrs, "grant-value", "grantValue", "funding-amount", "fundingAmount"),
                    "status": pick(attrs, "status", "grant-status", "grantStatus"),
                    "official_url": "https://dataportal.arc.gov.au/RGS/Web/Grants",
                    "source_id": "au-arc-grants",
                    "record_type": "historical-research-grant-discovery",
                    "verification_status": "unverified"
                })
            if len(items) < 100:
                break
    except Exception as exc:
        error = str(exc)[:500]
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "au-arc-grants",
        "source_url": "https://dataportal.arc.gov.au/RGS/Web/Grants",
        "api_url": API,
        "purpose": "Australian Research Council grant records. This dataset covers ARC research funding and is not a complete national register of household benefits or all government grants. Records are not live open calls unless verified separately.",
        "pages_fetched": pages,
        "records_count": len(records),
        "records": records,
        "error": error
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Australian ARC grants: {len(records)} records from {pages} pages; error={error or 'none'}")

if __name__ == "__main__":
    main()
