#!/usr/bin/env python3
"""Discover the currently open Start-Up Chile call from the official CORFO page.

The adapter extracts only fields present on the original government page.
If the page layout changes or key fields disappear, it fails rather than
publishing a guessed deadline or amount.
"""
from __future__ import annotations
import json
import re
import ssl
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

URL = "https://www.corfo.gob.cl/sites/cpp/convocatoria/start-up-chile-growth-13/"
OUT = Path("data/chile-discovery.json")
class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts=[]
    def handle_data(self, data):
        value=" ".join(data.split())
        if value: self.parts.append(value)

def main():
    request=urllib.request.Request(URL,headers={"User-Agent":"GlobalSupportRadar/1.0 (+official public grant discovery)","Accept":"text/html"})
    context=ssl.create_default_context()
    try:
        import certifi
        context=ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    with urllib.request.urlopen(request,timeout=30,context=context) as response:
        html=response.read(4_000_000).decode(response.headers.get_content_charset() or "utf-8",errors="replace")
        final_url=response.geturl()
    parser=TextParser();parser.feed(html)
    text=" ".join(parser.parts)
    def require(pattern, label, flags=re.I):
        match=re.search(pattern,text,flags)
        if not match: raise RuntimeError(f"Could not verify {label} on official CORFO page")
        return match.group(1)
    opening=require(r"Apertura:\s*(\d{2}/\d{2}/\d{4})","opening date")
    closing=require(r"Cierre:\s*(\d{2}/\d{2}/\d{4})","closing date")
    amount=require(r"tope de hasta\s*\$\s*([\d.]+)","maximum co-financing amount")
    if not re.search(r"Postulaciones\s+Abierta",text,re.I):
        raise RuntimeError("Official CORFO page no longer marks this call as open; refusing to publish as open")
    def iso_date(value):
        return datetime.strptime(value,"%d/%m/%Y").date().isoformat()
    start=iso_date(opening); end=iso_date(closing)
    deadline=datetime.fromisoformat(end+"T13:00:00-03:00")
    if deadline <= datetime.now(timezone.utc):
        raise RuntimeError("CORFO application deadline has passed; refusing to publish as open")
    amount_clp=int(amount.replace(".",""))
    record={
      "id":"corfo-startup-chile-growth-13-2026",
      "country_code":"CL","country_en":"Chile","country_hu":"Chile",
      "title":"Start-Up Chile — Growth 13",
      "title_hu":"Start-Up Chile – Growth 13 startupfejlesztési támogatás",
      "category":"business","region":"Todo Chile",
      "status":"open-and-current",
      "opening_date":start,
      "deadline":deadline.isoformat(),
      "amount_max":amount_clp,"currency":"CLP",
      "funding_rate_max_percent":50,
      "funding_rate_female_project_lead_percent":60,
      "eligibility_summary_hu":"18 év feletti chilei vagy külföldi természetes személyek, illetve a kiírásban meghatározott chilei vagy külföldi startupvállalkozások. A Growth kategória fejlettebb, értékesítéssel rendelkező technológiai startupokat céloz; a pontos bevételi és jogi feltételeket az eredeti szabályzat tartalmazza.",
      "eligibility_summary_en":"Chilean or foreign individuals aged 18+ and qualifying Chilean or foreign startup entities. Growth targets more mature technology startups with sales; exact revenue and legal requirements are set out in the official rules.",
      "eligibility_verified":False,
      "amount_verified":True,
      "official_url":final_url,
      "publisher":"Corporación de Fomento de la Producción (CORFO), Government of Chile",
      "verification_status":"official_page_open_status_and_amount_checked",
      "source_checked_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
      "note_hu":"A nyitott státusz, nyitás/zárás és maximális társfinanszírozás a CORFO hivatalos oldaláról származik. A támogatás legfeljebb a projektköltség 50%-a; női projektvezető esetén a hivatalos oldal 60%-ot jelez. A teljes jogosultságot és a saját hozzájárulást a szabályzatban ellenőrizni kell.",
      "note_en":"Open status, opening/closing dates and maximum co-financing are taken from CORFO's official page. Funding covers up to 50% of project cost; the page states 60% for a female project leader. Confirm full eligibility and matching contribution in the rules."
    }
    payload={
      "schema_version":"1.0",
      "updated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
      "country_code":"CL","country_en":"Chile",
      "source":"CORFO official active-call page",
      "source_url":final_url,
      "scope":"Official CORFO call pages checked by the daily discovery adapter. Only calls whose original page explicitly indicates open applications and provides parseable dates are included.",
      "records_count":1,"records":[record]
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Verified one open CORFO call; deadline {deadline.isoformat()}, maximum CLP {amount_clp:,}.")
if __name__=="__main__":
    main()
