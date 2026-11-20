#!/usr/bin/env python3
"""Discover agriculture-related links on official EU national funding portals.

This is a link-discovery adapter only. It never marks a result as an open call.
"""
from __future__ import annotations
import json
import os
import re
import ssl
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/europe-national-portals.json"
OUTPUT = ROOT / "data/eu-national-agriculture-discovery.json"
KEYWORDS = (
    "agri", "agric", "farm", "rural", "cap", "eafrd", "feader", "pdr",
    "landbouw", "agrar", "landwirtschaft", "agricultura", "agricolt",
    "jordbruk", "zem", "mezogaz", "mezőgaz", "rolnict", "rolnic",
    "poľnohospod", "poljopriv", "kmetij", "jord", "maatalous",
    "agro", "rural development", "vidékfejleszt"
)
MAX_LINKS_PER_PORTAL = 20
TIMEOUT = 12
HEADERS = {"User-Agent": "GlobalSupportRadar/1.0 (+official public funding link discovery)"}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs = dict(attrs)
            self.current = {"href": attrs.get("href", ""), "text": ""}
    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += " " + data
    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.current is not None:
            self.links.append(self.current)
            self.current = None

def fetch(url):
    request = Request(url, headers=HEADERS)
    context = ssl.create_default_context()
    try:
        import certifi
        context.load_verify_locations(certifi.where())
    except Exception:
        pass
    last_error = None
    for attempt in range(2):
        try:
            with urlopen(request, timeout=TIMEOUT, context=context) as response:
                raw = response.read(2_500_000)
                charset = response.headers.get_content_charset() or "utf-8"
                return response.geturl(), raw.decode(charset, errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code < 500 and exc.code != 429 or attempt == 1:
                raise
            last_error = exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if attempt == 1:
                raise
            last_error = exc
        time.sleep(1 * (attempt + 1))
    raise RuntimeError(f"Official portal request failed after retries: {last_error}")

def normalized_host(url):
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host

def main():
    directory = json.loads(INPUT.read_text(encoding="utf-8"))
    records, checked, failures = [], 0, []
    def scan_portal(portal):
        local_records = []
        try:
            final_url, html = fetch(portal["url"])
            parser = LinkParser()
            parser.feed(html)
            source_host = normalized_host(final_url)
            found = set()
            for item in parser.links:
                label = re.sub(r"\s+", " ", item["text"]).strip()
                href = (item["href"] or "").strip()
                if not href or href.startswith(("#", "mailto:", "javascript:")):
                    continue
                target = urljoin(final_url, href)
                parsed = urlparse(target)
                if parsed.scheme != "https" or normalized_host(target) != source_host:
                    continue
                haystack = (label + " " + target).casefold()
                if not any(word in haystack for word in KEYWORDS) or target in found:
                    continue
                found.add(target)
                local_records.append({
                    "id": f"national-agri-{portal['country_code'].lower()}-{len(found)}",
                    "country_code": portal["country_code"],
                    "country_en": portal["country_en"],
                    "country_hu": portal["country_hu"],
                    "title": label or target,
                    "official_url": target,
                    "portal_url": final_url,
                    "publisher": "Official national EU funding portal",
                    "category": "agriculture",
                    "record_type": "national-agriculture-link-discovery",
                    "verification_status": "unverified",
                    "status": "unverified-directory-lead",
                    "description": "Agriculture-related link discovered on the country official EU funding portal. Confirm the current call, eligibility and deadline on the linked page."
                })
                if len(found) >= MAX_LINKS_PER_PORTAL:
                    break
            return portal, True, local_records, None
        except Exception as exc:
            return portal, False, local_records, str(exc)[:220]

    portals = directory.get("records", [])
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(scan_portal, portals))
    for portal, ok, found_records, error in results:
        if ok:
            checked += 1
            records.extend(found_records)
        else:
            failures.append({"country_code": portal.get("country_code"), "error": error})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_id": "eu-national-funding-portals",
        "source_url": directory.get("source_index_url"),
        "scope": "Agriculture-related links discovered on the 27 official EU national shared-management funding portals. Results are unverified leads, not confirmed open calls.",
        "portals_total": len(directory.get("records", [])),
        "portals_checked": checked,
        "records_count": len(records),
        "records": records,
        "fetch_failures": failures
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {checked}/{payload['portals_total']} portals; found {len(records)} unverified agriculture links; failures: {len(failures)}")

if __name__ == "__main__":
    main()
