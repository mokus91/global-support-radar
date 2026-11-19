#!/usr/bin/env python3
"""Snapshot New Zealand's official Business.govt.nz Funding Explorer.

Only programme names and their official links are extracted. The page does not
publish a single authoritative open/closed status for every programme, so this
adapter deliberately does not infer application status, deadlines or amounts.
"""
from __future__ import annotations
import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "nz-funding-explorer-discovery.json"
URL = "https://www.business.govt.nz/browse-our-resource-library/funding-explorer"
TITLES = {
    "ai advisory pilot": "AI Advisory Pilot",
    "aspire nz seed fund": "Aspire NZ Seed Fund",
    "deep tech incubator programme": "Deep Tech Incubator Programme",
    "international growth fund": "International Growth Fund",
    "low emissions heavy vehicles fund": "Low Emissions Heavy Vehicles Fund",
    "management capability development fund": "Management Capability Development Fund",
    "maori agribusiness funds": "Māori Agribusiness funds",
    "maori development fund": "Māori Development Fund",
    "new to r&d grant": "New to R&D Grant",
    "preseed accelerator fund": "PreSeed Accelerator Fund",
    "primary sector growth fund": "Primary Sector Growth Fund",
    "r&d career grant": "R&D Career Grant",
    "r&d experience grant": "R&D Experience Grant",
    "waste minimisation fund": "Waste Minimisation Fund",
    "wood processing growth fund": "Wood Processing Growth Fund",
}

def norm(value):
    value = value.casefold().replace("&amp;", "&")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.active = [href, []]

    def handle_data(self, data):
        if self.active is not None:
            self.active[1].append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.active is not None:
            self.links.append((self.active[0], " ".join(self.active[1])))
            self.active = None

def main():
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "GlobalSupportRadar/1.0 (official public funding directory monitor)"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")

    parser = Links()
    parser.feed(html)
    found = {}
    for href, text in parser.links:
        title = TITLES.get(norm(text))
        if not title:
            continue
        full = urljoin(URL, href)
        if urlparse(full).scheme == "https":
            found[title] = full

    count_match = re.search(r"Showing\s+(\d+)\s+of\s+(\d+)", html, re.I)
    catalogue_count = int(count_match.group(2)) if count_match else None

    records = [{
        "id": "nz-funding-" + re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-"),
        "title": title,
        "country_code": "NZ",
        "categories": ["business"],
        "official_url": link,
        "publisher": "New Zealand Government — Business.govt.nz",
        "status": "listed-in-official-government-directory",
        "application_status_verified": False,
        "deadline_verified": False,
        "amount_verified": False,
        "eligibility_verified": False,
        "note_hu": "Hivatalos Funding Explorer-listázás. A nyitott jelentkezés, határidő, összeg és jogosultság nincs automatikusan igazolva; ellenőrizd az eredeti programoldalt.",
        "note_en": "Listed in the official Funding Explorer. Open status, deadline, amount and eligibility are not automatically verified; check the original programme page."
    } for title, link in sorted(found.items())]

    output = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "country_code": "NZ",
        "source": "New Zealand Government — Business.govt.nz Funding Explorer",
        "source_url": URL,
        "records_count": len(records),
        "records": records,
        "catalogue_count_reported_by_page": catalogue_count,
        "fetch_status": "ok" if records else ("checked-empty" if catalogue_count == 0 else "parser-no-matches"),
        "scope": "Official directory snapshot only. No open status, deadlines, grant amounts or eligibility are inferred.",
        "note": "The official page currently reports zero listed funding options." if catalogue_count == 0 else (
            "No programme links were extracted; the catalogue may be client-rendered or its structure may have changed."
            if not records else ""
        )
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"New Zealand Funding Explorer: extracted {len(records)} programme links; page catalogue count: {catalogue_count}.")

if __name__ == "__main__":
    main()
