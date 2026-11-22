#!/usr/bin/env python3
"""Check whether catalogue source URLs respond; this does NOT verify benefit facts or eligibility."""
import concurrent.futures
import datetime
import json
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/worldwide-national-support-sources.json"
OUTPUT = ROOT / "data/source-health-report.json"
data = json.loads(SOURCE.read_text(encoding="utf-8"))
records = data.get("records", [])

def check(record):
    url = record.get("url", "")
    item = {"id": record.get("id"), "country_code": record.get("country_code"),
            "name_en": record.get("name_en"), "url": url}
    if not url.startswith("https://") and not url.startswith("http://"):
        item.update(status="invalid_url", http_status=None, checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
        return item
    request = urllib.request.Request(url, headers={"User-Agent": "GlobalSupportRadarSourceChecker/1.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=18) as response:
            item.update(status="reachable", http_status=response.status, final_url=response.geturl())
    except urllib.error.HTTPError as exc:
        # Some government sites reject HEAD; retry with a small GET request.
        if exc.code in (403, 405, 501):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "GlobalSupportRadarSourceChecker/1.0", "Range": "bytes=0-1023"})
                with urllib.request.urlopen(req, timeout=18) as response:
                    item.update(status="reachable", http_status=response.status, final_url=response.geturl())
            except Exception as retry_exc:
                item.update(status="check_failed", http_status=getattr(retry_exc, "code", None), error=str(retry_exc)[:240])
        else:
            item.update(status="http_error", http_status=exc.code, error=str(exc)[:240])
    except Exception as exc:
        item.update(status="check_failed", http_status=None, error=str(exc)[:240])
    item["checked_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, records))
report = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "checked_records": len(results),
    "reachable": sum(x["status"] == "reachable" for x in results),
    "http_errors": sum(x["status"] == "http_error" for x in results),
    "check_failed": sum(x["status"] in ("check_failed", "invalid_url") for x in results),
    "important_note": "A reachable URL only means the server responded. It does not verify that a programme is open, that amounts are current, or that eligibility rules are unchanged.",
    "results": results
}
OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Checked {len(results)} sources: {report['reachable']} reachable, {report['http_errors']} HTTP errors, {report['check_failed']} check failures.")
