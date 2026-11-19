#!/usr/bin/env python3
"""Discover Hungarian research and innovation grant news from the official NKFIH RSS feed.

RSS entries are news/discovery candidates only. They are never marked as open calls
without checking the original opportunity page.
"""
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

FEED_URL = "https://rss.nkfih.gov.hu/hirek-180603?rss=1"
SOURCE_URL = "https://nkfih.gov.hu/palyazoknak/palyazatok/aktualis-felhivasok"
OUT = Path("data/hu-nkfih-discovery.json")
ALLOWED_HOSTS = {"nkfih.gov.hu", "www.nkfih.gov.hu"}


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.parts.append(value)


def clean(value, limit=900):
    parser = TextOnly()
    parser.feed(html.unescape(value or ""))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:limit]


def main():
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "hu-nkfih",
        "source_url": SOURCE_URL,
        "feed_url": FEED_URL,
        "feed_status": "unknown",
        "record_type": "official-grant-news-discovery",
        "records_count": 0,
        "records": [],
        "errors": []
    }
    try:
        request = urllib.request.Request(FEED_URL, headers={
            "User-Agent": "GlobalSupportRadar/1.0 (+https://mokus91.github.io/global-support-radar/)",
            "Accept": "application/rss+xml, application/xml, text/xml"
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        root = ET.fromstring(raw)
        items = root.findall(".//item")
        if not items:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = root.findall(".//atom:entry", ns)
        for item in items:
            title = clean(item.findtext("title") or "")
            link = (item.findtext("link") or "").strip()
            if not link:
                link_node = item.find("{http://www.w3.org/2005/Atom}link")
                link = (link_node.attrib.get("href", "") if link_node is not None else "").strip()
            parsed = urlparse(link)
            if not title or parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
                continue
            description = item.findtext("description") or item.findtext("summary") or ""
            published = item.findtext("pubDate") or item.findtext("published") or item.findtext("updated")
            output["records"].append({
                "title": title,
                "official_url": link,
                "published_at": clean(published or "", 80) or None,
                "summary": clean(description),
                "source_id": "hu-nkfih",
                "record_type": "grant-news-candidate",
                "verification_status": "unverified"
            })
        output["feed_status"] = "responding"
    except Exception as exc:
        output["feed_status"] = "unavailable-or-invalid"
        output["errors"].append(str(exc))
    output["records_count"] = len(output["records"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Official NKFIH RSS status: {output['feed_status']}; candidate items: {len(output['records'])}")


if __name__ == "__main__":
    main()
