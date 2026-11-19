#!/usr/bin/env python3
"""Discover Hungarian current calls from the official NKFIH listing page."""
from __future__ import annotations
import html, json, re, urllib.error, urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

SOURCE_URL = "https://nkfih.gov.hu/palyazoknak/palyazatok/aktualis-felhivasok"
OUT = Path("data/hu-nkfih-discovery.json")
ALLOWED_HOSTS = {"nkfih.gov.hu", "www.nkfih.gov.hu"}
MONTHS = {"január":"01","február":"02","március":"03","április":"04","május":"05","június":"06","július":"07","augusztus":"08","szeptember":"09","október":"10","november":"11","december":"12"}

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.current=None
    def handle_starttag(self, tag, attrs):
        if tag.lower()=="a":
            href=dict(attrs).get("href","")
            if href:self.current={"href":href,"text":[]}
    def handle_data(self,data):
        if self.current is not None and data.strip():self.current["text"].append(data.strip())
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self.current is not None:
            self.current["text"]=" ".join(self.current["text"])
            self.links.append(self.current)
            self.current=None

def parse_deadline(text):
    pattern=r"(20\d{2})\.\s*("+"|".join(MONTHS)+r")\s+(\d{1,2})\."
    match=re.search(pattern,text,re.I)
    if not match:return None
    return f"{match.group(1)}-{MONTHS[match.group(2).lower()]}-{int(match.group(3)):02d}"

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    previous={}
    if OUT.exists():
        try:previous=json.loads(OUT.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError):pass
    now=datetime.now(timezone.utc).isoformat()
    request=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"GlobalSupportRadar/1.0","Accept":"text/html"})
    try:
        with urllib.request.urlopen(request,timeout=20) as response:
            page=response.read().decode(response.headers.get_content_charset() or "utf-8",errors="replace")
        parser=LinkCollector()
        parser.feed(page)
        records=[]
        seen=set()
        for item in parser.links:
            text=re.sub(r"\s+"," ",html.unescape(item["text"])).strip()
            href=urljoin(SOURCE_URL,item["href"])
            parsed=urlparse(href)
            if parsed.scheme!="https" or parsed.hostname not in ALLOWED_HOSTS or not text:continue
            candidate=bool(re.search(r"20\d{2}\.\s*(?:"+"|".join(MONTHS)+r")",text,re.I) or re.search(r"GINOP|EUREKA|WIDERA|TÉT|NETWORKING|IPARJOG|KFI",text,re.I) or re.search(r"\bM(?:F|Ft)|\bEUR\b",text))
            if not candidate or href in seen:continue
            seen.add(href)
            deadline=parse_deadline(text)
            title=re.split(r"\s+20\d{2}\.\s*(?:"+"|".join(MONTHS)+r")",text,maxsplit=1,flags=re.I)[0].strip() or text
            amount_match=re.search(r"(\d[\d\s,.]*\s*(?:MFt|M Ft|millió Ft|EUR|Ft))",text,re.I)
            amount=amount_match.group(1).strip() if amount_match else None
            records.append({
              "id":"nkfih-"+str(len(records)+1),"title":title[:350],"title_hu":title[:350],
              "summary":"Az NKFIH hivatalos aktuális felhíváslistáján szereplő pályázat. A részletes beadási feltételeket és a nyitott státuszt a felhívás oldalán kell ellenőrizni.",
              "official_url":href,"deadline":deadline,"amount":amount,
              "currency":"HUF" if amount and "Ft" in amount else ("EUR" if amount and "EUR" in amount else None),
              "country":"HU","source_id":"hu-nkfih","status":"listed-on-official-current-calls-page",
              "record_type":"official-listing-candidate","verification_status":"official-listing-detail-not-yet-verified"
            })
        if not records and "Aktuális pályázati felhívások" not in page:
            raise ValueError("Unexpected NKFIH response: current-calls page marker not found")
        payload={"generated_at":now,"source_id":"hu-nkfih","source_url":SOURCE_URL,"fetch_status":"checked" if records else "checked-empty","record_type":"official-current-calls-listing-candidates","records_count":len(records),"records":records,"note":"Official listing candidates only; confirm current application status, eligibility and deadline on each detailed call page."}
    except (urllib.error.URLError,TimeoutError,OSError,ValueError) as exc:
        old=previous.get("records",[])
        payload={"generated_at":now,"source_id":"hu-nkfih","source_url":SOURCE_URL,"fetch_status":"temporarily-unavailable","record_type":"official-current-calls-listing-candidates","records_count":len(old),"records":old,"note":"Latest fetch failed; previous successful snapshot is preserved and may be stale.","error":str(exc)[:300],"last_successful_fetch":previous.get("generated_at")}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"NKFIH current calls: {payload['fetch_status']}; candidates: {payload['records_count']}")

if __name__=="__main__":main()
