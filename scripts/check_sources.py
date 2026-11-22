#!/usr/bin/env python3
"""Daily URL, page-change and catalogue review monitoring. Never edits benefit facts."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import pathlib
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/worldwide-national-support-sources.json"
OUTPUT = ROOT / "data/source-health-report.json"
UTC = dt.timezone.utc
now = dt.datetime.now(UTC)
data = json.loads(SOURCE.read_text(encoding="utf-8"))
records = data.get("records", [])
if not isinstance(records, list):
    raise SystemExit("Invalid catalogue: 'records' must be a list.")
try:
    previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
    previous_by_id = {x.get("id"): x for x in previous.get("results", [])}
except Exception:
    previous_by_id = {}

def request_url(url, method):
    req = urllib.request.Request(url, headers={
        "User-Agent": "GlobalSupportRadar/1.0 (+https://mokus91.github.io/global-support-radar/)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Range": "bytes=0-65535"
    }, method=method)
    with urllib.request.urlopen(req, timeout=25) as response:
        body = response.read(65536) if method == "GET" else b""
        return response.status, response.geturl(), body, response.headers.get("ETag"), response.headers.get("Last-Modified")

def check(record):
    url = record.get("url", "")
    item = {"id": record.get("id"), "country_code": record.get("country_code"),
            "name_en": record.get("name_en"), "url": url}
    previous_item = previous_by_id.get(record.get("id"), {})
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        item.update(status="invalid_url", http_status=None, error="Missing or invalid HTTP(S) URL.")
    else:
        last_error = None
        for attempt in range(2):
            try:
                try:
                    status, final_url, _, etag, modified = request_url(url, "HEAD")
                except urllib.error.HTTPError as exc:
                    if exc.code not in (400, 403, 405, 406, 501): raise
                    status, final_url, _, etag, modified = request_url(url, "GET")
                # Retrieve a bounded page sample to detect content changes, not to infer benefit facts.
                try:
                    get_status, final_url, body, get_etag, get_modified = request_url(url, "GET")
                    status = get_status
                    etag = get_etag or etag
                    modified = get_modified or modified
                    digest = hashlib.sha256(body).hexdigest() if body else None
                    old_digest = previous_item.get("content_sample_sha256")
                    item.update(content_sample_sha256=digest,
                                page_change=("changed" if old_digest and digest and old_digest != digest
                                             else "unchanged" if old_digest and digest
                                             else "baseline_created" if digest else "not_available"),
                                page_sample_bytes=len(body))
                except Exception as content_exc:
                    item.update(page_change="not_available", content_check_error=str(content_exc)[:180])
                item.update(status="reachable", http_status=status, final_url=final_url,
                            etag=etag, last_modified=modified)
                last_error = None
                break
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in (400, 403, 405, 406, 501):
                    try:
                        status, final_url, body, etag, modified = request_url(url, "GET")
                        digest = hashlib.sha256(body).hexdigest() if body else None
                        old_digest = previous_item.get("content_sample_sha256")
                        item.update(status="reachable", http_status=status, final_url=final_url,
                                    etag=etag, last_modified=modified, content_sample_sha256=digest,
                                    page_change=("changed" if old_digest and digest and old_digest != digest
                                                 else "unchanged" if old_digest and digest
                                                 else "baseline_created" if digest else "not_available"),
                                    page_sample_bytes=len(body))
                        last_error = None
                        break
                    except Exception as get_exc:
                        last_error = get_exc
            except Exception as exc:
                last_error = exc
            if attempt == 0: time.sleep(1.5)
        if last_error is not None:
            code = getattr(last_error, "code", None)
            item.update(status="http_error" if code else "check_failed",
                        http_status=code, error=str(last_error)[:240],
                        page_change="not_available")

    item["checked_at"] = now.isoformat()
    last_checked = record.get("last_checked") or record.get("amounts_checked")
    if not last_checked:
        item.update(content_freshness="not_recorded", last_content_check=None)
    else:
        try:
            last_date = dt.date.fromisoformat(str(last_checked)[:10])
            age = (now.date() - last_date).days
            item.update(content_freshness="review_due" if age > 45 else "recently_checked",
                        last_content_check=str(last_checked)[:10], content_age_days=age)
        except ValueError:
            item.update(content_freshness="invalid_date", last_content_check=str(last_checked))
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, records))

report = {
    "generated_at": now.isoformat(),
    "checked_records": len(results),
    "reachable": sum(x["status"] == "reachable" for x in results),
    "http_errors": sum(x["status"] == "http_error" for x in results),
    "check_failed": sum(x["status"] in ("check_failed", "invalid_url") for x in results),
    "page_changed": sum(x.get("page_change") == "changed" for x in results),
    "page_baseline_created": sum(x.get("page_change") == "baseline_created" for x in results),
    "content_review_due": sum(x["content_freshness"] in ("review_due", "not_recorded", "invalid_date") for x in results),
    "important_note": "Daily checks test URL availability and compare a bounded 64 KB page sample with the previous run. A detected page change is only a review signal. It does not verify programme status, amounts, deadlines, eligibility or application rules. Benefit facts are never auto-edited.",
    "results": results
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Checked {checked_records}: {reachable} reachable, {http_errors} HTTP errors, {check_failed} check failures; {page_changed} page samples changed; {content_review_due} content reviews due.".format(**report))
