#!/usr/bin/env python3
"""Discover Canadian health research funding opportunities from the official CIHR RSS feed."""
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ca-cihr-discovery.json"
FEED = "https://www.researchnet-recherchenet.ca/rnr16/fodRss.do?type=ALL&chanTyp=ALL&lang=E"

def clean(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\\s+", " ", value).strip()

def main():
    records, error = [], None
    try:
        req = Request(FEED, headers={"User-Agent": "GlobalSupportRadar/0.1", "Accept": "application/rss+xml, application/xml, text/xml"})
        with urlopen(req, timeout=45) as response:
            root = ET.fromstring(response.read())
        for item in root.findall(".//item"):
            title = clean(item.findtext("title"))
            link = clean(item.findtext("link"))
            if not title or not link:
                continue
            if not (link.startswith("https://www.researchnet-recherchenet.ca/") or link.startswith("https://cihr-irsc.gc.ca/")):
                continue
            records.append({
                "title": title,
                "official_url": link,
                "summary": clean(item.findtext("description")),
                "published_at": clean(item.findtext("pubDate")),
                "source_id": "ca-cihr",
                "record_type": "official-rss-discovery-candidate",
                "verification_status": "unverified"
            })
    except Exception as exc:
        error = str(exc)[:500]
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "ca-cihr",
        "source_url": "https://cihr-irsc.gc.ca/e/193.html",
        "feed_url": FEED,
        "records_count": len(records),
        "records": records,
        "error": error
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CIHR RSS: {len(records)} candidates; error={error or 'none'}")

if __name__ == "__main__":
    main()
