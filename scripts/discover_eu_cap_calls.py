#!/usr/bin/env python3
"""Discover featured agriculture and rural-development calls from the official EU CAP Network.
Records are leads only: the original call page must be checked for eligibility and current status.
"""
import json, re, ssl
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/eu-cap-network-discovery.json"
SOURCE = "https://eu-cap-network.ec.europa.eu/eip-agri-innovation-cooperation-funding/funding-opportunities_en"

class CallsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_featured = False
        self.in_intro = False
        self.tag = None
        self.current = None
        self.anchor_href = None
        self.anchor_text = []
        self.records = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h2", "h3"):
            self.tag = tag
            self.text_buffer = []
        elif tag == "p" and self.in_featured:
            self.tag = "p"
            self.text_buffer = []
        elif tag == "a" and self.in_featured:
            self.anchor_href = attrs.get("href")
            self.anchor_text = []
    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.tag in ("h2", "h3", "p"):
            self.text_buffer.append(text)
        if self.anchor_href is not None:
            self.anchor_text.append(text)
    def handle_endtag(self, tag):
        if tag == "h2":
            heading = " ".join(getattr(self, "text_buffer", [])).lower()
            self.in_featured = "featured calls" in heading
            if "introduction" in heading:
                self.in_featured = False
            self.tag = None
        elif tag == "h3" and self.in_featured:
            title = " ".join(getattr(self, "text_buffer", []))
            if title:
                self.current = {"title": title, "description": [], "official_url": SOURCE}
                self.records.append(self.current)
            self.tag = None
        elif tag == "p" and self.in_featured:
            value = " ".join(getattr(self, "text_buffer", []))
            if value and self.current:
                self.current["description"].append(value)
            self.tag = None
        elif tag == "a" and self.in_featured:
            if self.current and self.anchor_href:
                from urllib.parse import urljoin
                href = urljoin(SOURCE, self.anchor_href)
                # Keep the first useful call-specific link, not generic navigation.
                if self.current["official_url"] == SOURCE and href.startswith("https://"):
                    self.current["official_url"] = href
                    self.current["link_text"] = " ".join(self.anchor_text)
            self.anchor_href = None
            self.anchor_text = []

def main():
    req = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (compatible; GlobalSupportRadar/1.0)"})
    try:
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        context = ssl.create_default_context()
    with urlopen(req, timeout=45, context=context) as response:
        html = response.read().decode("utf-8", "replace")
    parser = CallsParser()
    parser.feed(html)
    records = []
    today = date.today()
    for raw in parser.records:
        description = " ".join(raw.get("description", []))
        if not raw.get("title") or raw["official_url"] == SOURCE:
            continue
        match = re.search(r"Deadline:\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", description, re.I)
        deadline = None
        status = "unverified"
        if match:
            try:
                deadline_date = datetime.strptime(" ".join(match.groups()), "%d %B %Y").date()
                deadline = deadline_date.isoformat()
                if deadline_date < today:
                    continue
                status = "deadline-in-future-unverified"
            except ValueError:
                pass
        elif "expected to be published" in description.lower():
            status = "planned-announcement-not-open"
        else:
            status = "unverified-directory-lead"
        records.append({
            "id": re.sub(r"[^a-z0-9]+", "-", raw["title"].lower()).strip("-"),
            "title": raw["title"],
            "description": description,
            "official_url": raw["official_url"],
            "deadline": deadline,
            "country_code": "EU",
            "categories": ["agriculture", "business"],
            "source_id": "eu-cap-network",
            "record_type": "agriculture-funding-discovery-candidate",
            "verification_status": "unverified",
            "status": status,
            "last_discovered_at": datetime.now(timezone.utc).isoformat()
        })
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-cap-network",
        "source_url": SOURCE,
        "purpose": "Featured agriculture and rural innovation funding leads from the official EU CAP Network. Expired dated calls are excluded; all records require manual verification on the original call page.",
        "records_count": len(records),
        "records": records
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"EU CAP Network: saved {len(records)} agriculture funding leads.")
if __name__ == "__main__":
    main()
