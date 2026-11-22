#!/usr/bin/env python3
"""Validate Global Support Radar catalogue integrity without changing benefit facts."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "data/worldwide-national-support-sources.json"
TAXONOMY = ROOT / "data/global-support-taxonomy.json"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
COUNTRY_RE = re.compile(r"^(?:[A-Z]{2}|EU|GLOBAL)$")

def load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

def main():
    data = load(CATALOGUE)
    taxonomy = load(TAXONOMY)
    records = data.get("records")
    if not isinstance(records, list):
        raise SystemExit("ERROR: catalogue.records must be a list")
    errors, warnings = [], []
    seen_ids = set()
    for index, row in enumerate(records, 1):
        if not isinstance(row, dict):
            errors.append(f"Record #{index}: expected an object")
            continue
        rid = row.get("id", f"#{index}")
        for key in ("id", "country_code", "country_en", "name_en", "url", "publisher", "kind", "category"):
            if not row.get(key):
                errors.append(f"{rid}: missing required field '{key}'")
        if row.get("id"):
            if not ID_RE.fullmatch(str(row["id"])):
                errors.append(f"{rid}: invalid id format")
            if rid in seen_ids:
                errors.append(f"{rid}: duplicate id")
            seen_ids.add(rid)
        code = str(row.get("country_code", ""))
        if code and not COUNTRY_RE.fullmatch(code):
            errors.append(f"{rid}: invalid country code '{code}'")
        url = row.get("url", "")
        parsed = urlparse(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{rid}: URL must be a valid HTTPS address")
        if row.get("verification_status") in (None, ""):
            warnings.append(f"{rid}: verification_status is not recorded")
        if row.get("kind") in ("benefits-finder", "grant-directory", "government-service-portal") and row.get("verification_status") == "verified-programme":
            warnings.append(f"{rid}: portal/finder is marked as a verified individual programme; review classification")
    if not isinstance(taxonomy.get("support_categories"), list) or not taxonomy["support_categories"]:
        errors.append("Taxonomy has no support_categories list")
    if errors:
        print("CATALOGUE VALIDATION FAILED")
        for error in errors:
            print("ERROR:", error)
        for warning in warnings:
            print("WARNING:", warning)
        return 1
    print(f"Catalogue validation passed: {len(records)} records, {len(seen_ids)} unique IDs, {len(taxonomy.get('regions', {}))} regions, {len(taxonomy.get('support_categories', []))} categories.")
    if warnings:
        print(f"Warnings: {len(warnings)} (non-blocking)")
        for warning in warnings[:30]:
            print("WARNING:", warning)
    return 0

if __name__ == "__main__":
    sys.exit(main())
