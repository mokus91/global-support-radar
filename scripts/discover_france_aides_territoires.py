#!/usr/bin/env python3
"""Import current catalogue entries from the official Aides-territoires API."""
from __future__ import annotations
import json, ssl, time, socket, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

BASE="https://aides-territoires.beta.gouv.fr"
START=BASE+"/api/aids/"
OUT=Path("data/france-aides-territoires-discovery.json")
MAX_PAGES=40

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"GlobalSupportRadar/1.0","Accept":"application/json"})
    ctx=ssl.create_default_context()
    try:
        import certifi
        ctx=ssl.create_default_context(cafile=certifi.where())
    except ImportError: pass
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25,context=ctx) as r:
                return json.loads(r.read(8_000_000).decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403, 429, 500, 502, 503, 504):
                return {"_api_error": exc.code, "_api_error_reason": str(exc.reason), "_api_error_kind": "http"}
            raise
        except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError, ConnectionError) as exc:
            if attempt == 2:
                return {"_api_error": None, "_api_error_reason": str(exc), "_api_error_kind": "network"}
            time.sleep(2 ** attempt)
    return {"_api_error": None, "_api_error_reason": "Unknown network failure", "_api_error_kind": "network"}

def first(row,*keys):
    for k in keys:
        if row.get(k) not in (None,"",[],{}): return row[k]
    return None

def eligibility_flags(row):
    """Presence of eligibility text is not proof that eligibility was verified."""
    return {
        "eligibility_verified": False,
        "eligibility_text_available": bool(first(row, "eligibility", "eligibility_description")),
    }


def categories(row):
    text=" ".join(str(x) for x in [row.get("name"),row.get("description"),row.get("perimeter"),*(row.get("tags") or []),*(row.get("aid_types") or [])] if x).lower()
    rules=[
      ("housing",("logement","habitat","rénovation énergétique","hébergement")),
      ("family",("famille","enfance","jeunesse","parentalité")),
      ("agriculture",("agriculture","agricole","rural","exploitant")),
      ("business",("entreprise","économie","commerce","artisan","innovation")),
      ("education",("éducation","formation","enseignement","école","université")),
      ("healthcare",("santé","médical","soin","sanitaire")),
      ("energy",("énergie","énergétique","solaire","renouvelable","climat")),
      ("employment",("emploi","insertion professionnelle","recrutement")),
      ("social_support",("social","inclusion","précarité","solidarité","handicap")),
      ("transport",("mobilité","transport","vélo","déplacement"))
    ]
    found=[c for c,words in rules if any(w in text for w in words)]
    return found or ["all"]

def main():
    url=START; records=[]; seen=set(); pages=0
    while url and pages<MAX_PAGES:
        payload=get_json(url)
        if payload.get("_api_error") is not None or payload.get("_api_error_kind"):
            restricted = payload.get("_api_error_kind") == "http"
            # Preserve the last successful snapshot during an upstream outage.
            # Its original generated_at remains unchanged so freshness checks do
            # not mistake old opportunities for newly fetched data.
            previous = {}
            if OUT.exists():
                try:
                    previous = json.loads(OUT.read_text(encoding="utf-8"))
                    if not isinstance(previous, dict):
                        previous = {}
                except (OSError, json.JSONDecodeError):
                    previous = {}
            previous_records = previous.get("records", [])
            if not isinstance(previous_records, list):
                previous_records = []
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            output={
                "schema_version":"1.0",
                "generated_at":previous.get("generated_at") or now,
                "checked_at":now,
                "country_code":"FR",
                "source":"Aides-territoires official public API",
                "source_url":START,
                "pages_checked":pages,
                "records_count":len(previous_records),
                "records":previous_records,
                "fetch_status":"temporarily-restricted" if restricted else "temporarily-unavailable",
                "http_status":payload.get("_api_error"),
                "error":payload.get("_api_error_reason"),
                "stale_snapshot_preserved":bool(previous_records),
                "scope":"The official API could not be queried successfully. Previously collected records are retained as a stale snapshot, not treated as newly verified. No current grant or application status is inferred; use the official catalogue directly."
            }
            OUT.parent.mkdir(parents=True,exist_ok=True)
            OUT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
            print("Aides-territoires API " + ("temporarily restricted" if restricted else "temporarily unavailable") + f"; preserved {len(previous_records)} records from the last successful snapshot.")
            return
        rows=payload.get("results",[])
        if not isinstance(rows,list): raise RuntimeError("Unexpected API response: results is not a list")
        for row in rows:
            if not isinstance(row,dict): continue
            rid=str(row.get("id") or row.get("url") or "")
            if not rid or rid in seen: continue
            seen.add(rid)
            detail=row.get("url") or ""
            records.append({
              "id":rid,"country_code":"FR","title_original":first(row,"name","title") or "Aide publique",
              "publisher":", ".join(row.get("backers",[])) if isinstance(row.get("backers"),list) else first(row,"backers"),
              "description_original":first(row,"description","summary"),
              "eligibility_original":first(row,"eligibility","eligibility_description"),
              "geographic_scope_original":first(row,"perimeter","territory","geographic_scope"),
              "targeted_audiences_original":row.get("targeted_audiences") or [],
              "aid_types_original":row.get("aid_types") or [],"tags_original":row.get("tags") or [],
              "categories":categories(row),"official_url":urljoin(BASE,detail) if detail else BASE+"/",
              "origin_url":first(row,"origin_url","source_url"),
              "application_url":first(row,"application_url","mobilization_url"),
              "deadline":first(row,"application_deadline","end_date","deadline"),
              "status":"listed-active-in-official-catalogue","deadline_verified":False,
              **eligibility_flags(row),
              "source_api":START,
              "note_hu":"Az Aides-territoires aktív katalógusában szereplő támogatás. Ez nem bizonyítja, hogy a jelentkezés jelenleg nyitott. A határidőt és jogosultságot az eredeti kiírásban ellenőrizd.",
              "note_en":"Listed in the Aides-territoires active catalogue. This does not prove applications are currently open or that an applicant is eligible. Eligibility text presence is informational only; verify the actual criteria and deadlines on the original notice."
            })
        pages+=1
        nxt=payload.get("next")
        url=urljoin(BASE,nxt) if nxt else None
    if not pages: raise RuntimeError("Aides-territoires API returned no pages")
    output={"schema_version":"1.0","generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),"country_code":"FR","source":"Aides-territoires official public API","source_url":START,"pages_checked":pages,"records_count":len(records),"records":records,"fetch_status":"ok","scope":"Paginated active-aids catalogue. The API does not establish current application deadlines; no open-call status is inferred."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Imported {len(records)} catalogue records from {pages} API pages.")
if __name__=="__main__": main()
