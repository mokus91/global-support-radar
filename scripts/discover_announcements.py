#!/usr/bin/env python3
"""Collect potentially relevant items from configured official RSS/Atom feeds.
Nothing is treated as a verified benefit until a human reviews the official notice.
"""
import json, re, hashlib, urllib.request, urllib.error
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"data/official-announcement-feeds.json"
OUT=ROOT/"data/announcement-review-queue.json"
UA="GlobalSupportRadarBot/1.0 (+https://mokus91.github.io/global-support-radar/)"
MAX_ITEMS=500

def text_of(node, names):
    for name in names:
        el=node.find(name)
        if el is not None and el.text:
            return el.text.strip()
        # namespace-insensitive lookup
        for child in node.iter():
            if child.tag.rsplit("}",1)[-1].lower()==name.lower() and child.text:
                return child.text.strip()
    return ""

def parse_date(value):
    if not value: return None
    try:
        dt=parsedate_to_datetime(value)
        if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        try: return datetime.fromisoformat(value.replace("Z","+00:00")).astimezone(timezone.utc).isoformat()
        except Exception: return None

def parse_feed(raw, feed):
    root=ET.fromstring(raw)
    entries=[x for x in root.iter() if x.tag.rsplit("}",1)[-1].lower() in ("item","entry")]
    results=[]
    for entry in entries:
        title=text_of(entry,["title"])
        link=""
        for child in entry:
            if child.tag.rsplit("}",1)[-1].lower()=="link":
                link=child.attrib.get("href") or (child.text or "").strip()
                if link: break
        summary=text_of(entry,["description","summary","content"])
        guid=text_of(entry,["guid","id"]) or link or title
        haystack=(title+" "+summary).lower()
        matched=[k for k in feed_keywords if k in haystack]
        if not title or not link or not matched: continue
        digest=hashlib.sha256((feed["id"]+"|"+guid).encode()).hexdigest()[:20]
        date=text_of(entry,["pubDate","published","updated","date"])
        results.append({
            "candidate_id":digest,"country_code":feed["country_code"],
            "country_name":feed["country_name"],"publisher":feed["publisher"],
            "feed_id":feed["id"],"title":title,"url":link,
            "published_at":parse_date(date),"summary":re.sub(r"\s+"," ",summary)[:1200],
            "matched_keywords":matched,"review_status":"needs_human_review",
            "review_note":"A hír releváns lehet, de támogatási programként, összegként, határidőként vagy jogosultságként még nincs ellenőrizve."
        })
    return results

config=json.loads(CONFIG.read_text(encoding="utf-8"))
feed_keywords=[k.lower() for k in config.get("keywords",[])]
try: old=json.loads(OUT.read_text(encoding="utf-8"))
except Exception: old={"items":[]}
known={x.get("candidate_id"):x for x in old.get("items",[])}
feed_results=[]
errors=[]
for feed in config.get("feeds",[]):
    if not feed.get("enabled",True): continue
    try:
        req=urllib.request.Request(feed["url"],headers={"User-Agent":UA,"Accept":"application/rss+xml, application/atom+xml, application/xml, text/xml"})
        with urllib.request.urlopen(req,timeout=25) as response:
            if response.status>=400: raise RuntimeError("HTTP "+str(response.status))
            raw=response.read(5_000_000)
        found=parse_feed(raw,feed)
        feed_results.append({"feed_id":feed["id"],"country_code":feed["country_code"],"fetched":len(found),"status":"ok"})
        for item in found:
            if item["candidate_id"] not in known:
                known[item["candidate_id"]]=item
    except Exception as exc:
        errors.append({"feed_id":feed["id"],"error":str(exc)[:300]})
        feed_results.append({"feed_id":feed["id"],"country_code":feed["country_code"],"status":"error","error":str(exc)[:300]})
items=list(known.values())
items.sort(key=lambda x:(x.get("published_at") or "",x.get("candidate_id","")),reverse=True)
items=items[:MAX_ITEMS]
report={"generated_at":datetime.now(timezone.utc).isoformat(),"feeds_checked":len(feed_results),"feeds_ok":sum(1 for x in feed_results if x["status"]=="ok"),"new_candidates":sum(1 for x in known if x not in {i.get("candidate_id") for i in old.get("items",[])}),"pending_review":sum(1 for x in items if x.get("review_status")=="needs_human_review"),"feed_results":feed_results,"errors":errors,"items":items}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Feeds checked: {report['feeds_checked']}; successful: {report['feeds_ok']}; pending review: {report['pending_review']}; errors: {len(errors)}")
