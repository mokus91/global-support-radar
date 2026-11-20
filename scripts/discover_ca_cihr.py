#!/usr/bin/env python3
"""Discover Canadian health-research funding notices from official CIHR pages.

The ResearchNet RSS endpoint may be unavailable in some hosted runners. In that
case, the CIHR public upcoming-opportunities page is used as a transparent
fallback. Notices are never promoted to verified-open opportunities here.
"""
from __future__ import annotations

import json
import re
import ssl
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

import certifi

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ca-cihr-discovery.json"
RSS_URL = "https://www.researchnet-recherchenet.ca/rnr16/fodRss.do?type=ALL&chanTyp=ALL&lang=E"
UPCOMING_URL = "https://cihr-irsc.gc.ca/e/51605.html"
OFFICIAL_HOSTS = {"cihr-irsc.gc.ca", "www.researchnet-recherchenet.ca"}
KEYWORDS = ("funding opportunity", "funding opportunities", "grant", "fellowship", "award", "research chair")


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()


def official_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() in OFFICIAL_HOSTS


def fetch(url: str, timeout: int = 30) -> bytes:
    request = Request(url, headers={
        "User-Agent": "GlobalSupportRadar/0.2 (+https://mokus91.github.io/global-support-radar/)",
        "Accept": "text/html,application/rss+xml,application/xml,text/xml",
    })
    errors = []
    for context in (ssl.create_default_context(), ssl.create_default_context(cafile=certifi.where())):
        try:
            with urlopen(request, timeout=timeout, context=context) as response:
                return response.read()
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors)[:450])


class OpportunityPageParser(HTMLParser):
    """Collect opportunity links while retaining the page's section label."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.heading_level = 0
        self.heading_parts: list[str] = []
        self.section = ""
        self.anchor_href: str | None = None
        self.anchor_parts: list[str] = []
        self.links: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h1", "h2", "h3"):
            self.heading_level = int(tag[1])
            self.heading_parts = []
        elif tag == "a" and attrs.get("href"):
            self.anchor_href = attrs["href"]
            self.anchor_parts = []

    def handle_data(self, data):
        if self.heading_level:
            self.heading_parts.append(data)
        if self.anchor_href is not None:
            self.anchor_parts.append(data)

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3") and self.heading_level == int(tag[1]):
            heading = clean(" ".join(self.heading_parts))
            if heading:
                self.section = heading
            self.heading_level = 0
            self.heading_parts = []
        elif tag == "a" and self.anchor_href is not None:
            title = clean(" ".join(self.anchor_parts))
            href = self.anchor_href
            self.links.append((title, href, self.section))
            self.anchor_href = None
            self.anchor_parts = []


def parse_upcoming_html(html: str) -> list[dict]:
    parser = OpportunityPageParser()
    parser.feed(html)
    records = []
    seen = set()
    for title, href, section in parser.links:
        title = clean(title)
        url = urljoin(UPCOMING_URL, href)
        if not title or not official_url(url):
            continue
        if not any(word in title.lower() for word in KEYWORDS):
            continue
        # The source page has separate upcoming and already-published sections.
        section_lower = section.lower()
        if "published" in section_lower:
            record_type = "official-published-listing-candidate"
            source_status = "official-listing-not-verified-open"
        else:
            record_type = "official-upcoming-announcement"
            source_status = "planned-announcement-not-open"
        key = (title.lower(), url)
        if key in seen:
            continue
        seen.add(key)
        records.append({
            "title": title,
            "official_url": url,
            "summary": "Official CIHR page listing. Check the linked notice and ResearchNet for current dates and application status.",
            "source_id": "ca-cihr",
            "record_type": record_type,
            "source_section": section or "CIHR opportunities page (section not detected)",
            "source_status": source_status,
            "verification_status": "unverified",
            "eligibility_verified": False,
            "amount_verified": False,
            "open_status_verified": False,
        })
    return records


def parse_rss(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    records = []
    for item in root.findall(".//item"):
        title = clean(item.findtext("title") or "")
        link = clean(item.findtext("link") or "")
        if not title or not official_url(link):
            continue
        records.append({
            "title": title,
            "official_url": link,
            "summary": clean(item.findtext("description") or ""),
            "published_at": clean(item.findtext("pubDate") or ""),
            "source_id": "ca-cihr",
            "record_type": "official-rss-discovery-candidate",
            "source_status": "rss-listing-not-verified-open",
            "verification_status": "unverified",
            "eligibility_verified": False,
            "amount_verified": False,
            "open_status_verified": False,
        })
    return records


def main():
    records: list[dict] = []
    source_errors: dict[str, str] = {}
    try:
        records.extend(parse_rss(fetch(RSS_URL, timeout=25)))
    except Exception as exc:
        source_errors["researchnet_rss"] = str(exc)[:450]

    try:
        records.extend(parse_upcoming_html(fetch(UPCOMING_URL, timeout=25).decode("utf-8", errors="replace")))
    except Exception as exc:
        source_errors["cihr_upcoming_page"] = str(exc)[:450]

    deduplicated = []
    seen = set()
    for record in records:
        key = (record["title"].casefold(), record["official_url"])
        if key not in seen:
            seen.add(key)
            deduplicated.append(record)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "ca-cihr",
        "source_url": UPCOMING_URL,
        "feed_url": RSS_URL,
        "records_count": len(deduplicated),
        "records": deduplicated,
        "source_errors": source_errors,
        "error": "; ".join(f"{key}: {value}" for key, value in source_errors.items())[:500] if not deduplicated and source_errors else None,
        "note": "CIHR notices are discovery candidates only. Upcoming announcements are not open calls; verify the linked official notice and ResearchNet before applying."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CIHR: {len(deduplicated)} official candidates; source errors={len(source_errors)}")


if __name__ == "__main__":
    main()
