#!/usr/bin/env python3
"""Probe the official Hungarian Pályázati Portal announcements RSS feed.

The feed has been reported as unavailable by independent feed monitoring.
This adapter never falls back to third-party copies and never invents entries.
If the official feed responds, items are stored as unverified announcements
for later checking against their original official pages.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

FEED_URL = "https://www.palyazat.gov.hu/rssfeed.php?type=kozlemenyek"
OUT = Path("data/hu-palyazat-announcements.json")


def main():
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "hu-palyazat-gov",
        "source_url": "https://www.palyazat.gov.hu/",
        "feed_url": FEED_URL,
        "feed_status": "unknown",
        "record_type": "official-announcement-discovery",
        "records": [],
        "errors": []
    }
    try:
        req = urllib.request.Request(FEED_URL, headers={
            "User-Agent": "GlobalSupportRadar/1.0 (+https://mokus91.github.io/global-support-radar/)",
            "Accept": "application/rss+xml, application/xml, text/xml"
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
        root = ET.fromstring(raw)
        channel = root.find("channel")
        if channel is None:
            raise ValueError("RSS XML has no channel element")
        for item in channel.findall("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if not title or not link or not link.startswith("https://www.palyazat.gov.hu/"):
                continue
            output["records"].append({
                "title": title,
                "official_url": link,
                "published_at": (item.findtext("pubDate") or "").strip() or None,
                "summary": (item.findtext("description") or "").strip() or None,
                "source_id": "hu-palyazat-gov",
                "record_type": "announcement-candidate",
                "verification_status": "unverified"
            })
        output["feed_status"] = "responding"
    except Exception as exc:
        output["feed_status"] = "unavailable-or-invalid"
        output["errors"].append(str(exc))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Official Palyazat.gov.hu feed status: {output['feed_status']}; candidate items: {len(output['records'])}")
    # A failed feed probe is recorded, not treated as a workflow failure.


if __name__ == "__main__":
    main()
