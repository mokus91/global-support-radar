#!/usr/bin/env python3
"""Build country-coded records from the UN DESA national portal directory seed."""
import csv, json
from pathlib import Path
import pycountry

ROOT = Path(__file__).resolve().parents[1]
seed = ROOT / "data/un-national-portals-seed.tsv"
out = ROOT / "data/un-national-portals.json"
ALIASES = {
    "Congo": "CG", "Niger": "NE", "Nigeria": "NG", "Democratic People's Republic of Korea": "KP",
    "Democratic Republic of the Congo": "CD", "Iran (Islamic Republic of)": "IR",
    "Lao People's Democratic Republic": "LA", "Micronesia (Federated States of)": "FM",
    "Republic of Korea": "KR", "Republic of Moldova": "MD",
    "Russian Federation": "RU", "Syrian Arab Republic": "SY", "Turkey": "TR",
    "United Republic of Tanzania": "TZ",
    "United Kingdom of Great Britain and Northern Ireland": "GB",
    "United States of America": "US", "Venezuela, Bolivarian Republic of": "VE",
    "Viet Nam": "VN", "Bolivia": "BO", "Côte d'Ivoire": "CI",
    "Cabo Verde": "CV", "Eswatini": "SZ", "Gambia": "GM",
    "North Macedonia": "MK", "Sao Tome and Principe": "ST",
}
records = []
with seed.open(encoding="utf-8") as fh:
    for row in csv.reader(fh, delimiter="\t"):
        if not row or len(row) < 2:
            continue
        name, host = row[0].strip(), row[1].strip()
        code = ALIASES.get(name)
        if not code:
            try:
                code = pycountry.countries.search_fuzzy(name)[0].alpha_2
            except LookupError as exc:
                raise SystemExit(f"Could not map country to ISO code: {name}") from exc
        records.append({
            "country_code": code,
            "country_en": name,
            "url": "https://" + host.rstrip("/"),
            "publisher": "United Nations Department of Economic and Social Affairs",
            "source_url": "https://ekap.desa.un.org/Resources",
            "kind": "national-government-portal-directory-lead",
            "status": "historical-directory-lead",
            "verification_status": "not-currently-verified",
            "last_assessed_by_source": "2013-04/2013-08",
            "coverage": "National e-government / public services portal; support programme coverage not confirmed"
        })
codes = [r["country_code"] for r in records]
if len(records) != 193 or len(set(codes)) != len(codes):
    raise SystemExit(f"Expected 193 unique UN Member State records; got {len(records)} records / {len(set(codes))} codes")
payload = {
    "schema_version": "1.0",
    "updated_at": "2026-11-19",
    "publisher": "United Nations Department of Economic and Social Affairs",
    "source_url": "https://ekap.desa.un.org/Resources",
    "scope": "National e-government portal directory for 193 UN Member States. These are starting points, not verified grant or benefit listings.",
    "freshness_warning": "UN DESA states that government website URLs were last assessed during April–August 2013. Verify each portal before relying on it.",
    "records_count": len(records),
    "records": sorted(records, key=lambda r: r["country_en"].casefold())
}
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(records)} unique country portal leads to {out}")
