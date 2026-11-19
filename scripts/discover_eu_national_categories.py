#!/usr/bin/env python3
"""Discover category-specific links on official EU national funding portals.

Only same-host HTTPS links are retained. Every result is an unverified lead,
never a claim that a programme is open or that a visitor is eligible.
"""
from __future__ import annotations
import json
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/europe-national-portals.json"
OUTPUT = ROOT / "data/eu-national-category-discovery.json"
TIMEOUT = 18
MAX_PER_PORTAL_CATEGORY = 12
HEADERS = {"User-Agent": "GlobalSupportRadar/1.0 (official public funding link discovery)"}
KEYWORDS = {
    "business": ("business", "entrepreneur", "enterprise", "sme", "startup", "unternehmen", "unternehmer", "entreprise", "ondernem", "företag", "yritys", "podnik", "przedsi", "firm", "v podnik", "vállalkoz"),
    "housing": ("housing", "house", "home renovation", "renovation", "wohn", "logement", "habitat", "woning", "bostad", "asuminen", "bydlen", "lakhat", "energetikai korszer"),
    "energy": ("energy", "renewable", "efficiency", "energie", "énergie", "energía", "energia", "energieeffizienz", "energetycz", "energiatehok", "energiahat"),
    "education": ("education", "training", "skills", "scholarship", "school", "bildung", "formation", "éducation", "educación", "istruzione", "koulutus", "oktatás", "szakképz"),
    "employment": ("employment", "jobs", "labour", "workforce", "unemployment", "beschäft", "emploi", "empleo", "lavoro", "werk", "arbete", "työll", "foglalkoztat"),
    "transport": ("transport", "mobility", "vehicle", "rail", "road", "verkehr", "mobilité", "transporte", "trasport", "közleked", "mobilit"),
}
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.current = {"href": dict(attrs).get("href", ""), "text": ""}
    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += " " + data
    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.current is not None:
            self.links.append(self.current)
            self.current = None

def host(url):
    value = (urlparse(url).hostname or "").lower()
    return value[4:] if value.startswith("www.") else value

def fetch(url):
    context = ssl.create_default_context()
    try:
        import certifi
        context.load_verify_locations(certifi.where())
    except Exception:
        pass
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=TIMEOUT, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.geturl(), response.read(2_500_000).decode(charset, errors="replace")

def main():
    directory = json.loads(INPUT.read_text(encoding="utf-8"))
    records, checked, failures = [], 0, []
    for portal in directory.get("records", []):
        try:
            final_url, html = fetch(portal["url"])
            checked += 1
            parser = LinkParser()
            parser.feed(html)
            seen = {category: set() for category in KEYWORDS}
            for item in parser.links:
                label = re.sub(r"\s+", " ", item["text"]).strip()
                href = (item["href"] or "").strip()
                if not href or href.startswith(("#", "mailto:", "javascript:")):
                    continue
                target = urljoin(final_url, href)
                if urlparse(target).scheme != "https" or host(target) != host(final_url):
                    continue
                haystack = (label + " " + target).casefold()
                for category, words in KEYWORDS.items():
                    if len(seen[category]) >= MAX_PER_PORTAL_CATEGORY:
                        continue
                    if not any(word in haystack for word in words) or target in seen[category]:
                        continue
                    seen[category].add(target)
                    records.append({
                        "id": f"eu-{portal['country_code'].lower()}-{category}-{len(seen[category])}",
                        "country_code": portal["country_code"],
                        "country_en": portal["country_en"],
                        "country_hu": portal["country_hu"],
                        "category": category,
                        "title": label or target,
                        "official_url": target,
                        "portal_url": final_url,
                        "publisher": "Official national EU funding portal",
                        "verification_status": "unverified",
                        "status": "unverified-directory-lead",
                        "description": f"{category.title()}-related link discovered on the official national EU funding portal. Confirm the programme, opening status, deadline and eligibility on the linked page."
                    })
    except Exception as exc:
        failures.append({"country_code": portal.get("country_code"), "error": str(exc)[:220]})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_id": "eu-national-funding-portals",
        "source_url": directory.get("source_index_url"),
        "scope": "Category-related links discovered on 27 official EU national shared-management funding portals. Results are unverified leads, not confirmed open calls.",
        "portals_total": len(directory.get("records", [])),
        "portals_checked": checked,
        "records_count": len(records),
        "records": records,
        "fetch_failures": failures
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {checked}/{payload['portals_total']} portals; found {len(records)} unverified category links; failures: {len(failures)}")

if __name__ == "__main__":
    main()
