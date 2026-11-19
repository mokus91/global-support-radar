#!/usr/bin/env python3
"""Expand the worldwide country navigator to all UN Member States.

Missing countries receive only a historical UN DESA government-portal lead.
UN DESA says these URLs were last assessed in April-August 2013; they are
never represented as verified grant portals or current benefit listings.
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UN_FILE = ROOT / "data/un-national-portals.json"
OUTPUT = ROOT / "data/worldwide-national-support-sources.json"

def main():
    directory = json.loads(OUTPUT.read_text(encoding="utf-8"))
    un_data = json.loads(UN_FILE.read_text(encoding="utf-8"))
    records = directory.setdefault("records", [])
    existing = {item.get("country_code") for item in records}
    added = 0
    for portal in un_data.get("records", []):
        code = portal.get("country_code")
        url = portal.get("url", "")
        if not code or code in existing or not url.startswith("https://"):
            continue
        records.append({
            "id": f"un-historical-portal-{code.lower()}",
            "country_code": code,
            "country_en": portal.get("country_en", code),
            "category": "all",
            "name_hu": f"{portal.get('country_en', code)} – történelmi ENSZ-kormányzati portálhivatkozás",
            "name_en": f"{portal.get('country_en', code)} — historical UN government portal lead",
            "url": url,
            "publisher": "United Nations Department of Economic and Social Affairs (UN DESA)",
            "kind": "historical-national-government-portal",
            "description_hu": "Történelmi országos kormányzati portálhivatkozás az ENSZ DESA 2013-as jegyzékéből. A hivatkozás jelenlegi működése, támogatási tartalma és jogosultsági információi nincsenek ellenőrizve. Kérjük, kezeld kiindulópontként, ne aktuális pályázatként.",
            "description_en": "Historical national government portal lead from the UN DESA directory. The current URL, support-programme coverage and eligibility information have not been verified. Treat this as a starting point, not as a current grant listing.",
            "verification_status": "not-currently-verified",
            "status": "historical-directory-lead",
            "last_assessed_by_source": portal.get("last_assessed_by_source", "2013-04/2013-08"),
            "source_url": portal.get("source_url", "https://ekap.desa.un.org/Resources")
        })
        existing.add(code)
        added += 1
    directory["updated_at"] = date.today().isoformat()
    directory["scope"] = (
        "Country-specific official support finders plus historical UN DESA national government portal leads. "
        "Dedicated source links are curated for selected countries. Missing-country links are historical "
        "directory leads last assessed by UN DESA in April-August 2013; they are not verified support finders, "
        "current grant listings or proof of eligibility."
    )
    directory["records_count"] = len(records)
    OUTPUT.write_text(json.dumps(directory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    countries = len({item.get("country_code") for item in records})
    print(f"Added {added} historical country portal leads; {len(records)} links now cover {countries} country codes.")

if __name__ == "__main__":
    main()
