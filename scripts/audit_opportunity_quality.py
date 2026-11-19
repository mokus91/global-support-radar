#!/usr/bin/env python3
"""Audit published opportunity feeds without changing source records."""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
manifest = json.loads((DATA / "feed-status.json").read_text(encoding="utf-8"))
today = dt.datetime.now(dt.timezone.utc).date()
report = {
    "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "feeds_checked": 0, "records_checked": 0, "expired_deadlines": 0,
    "missing_urls": 0, "invalid_urls": 0, "duplicate_ids": 0,
    "missing_titles": 0, "unverified_status": 0, "feed_errors": [],
    "notes": [
        "Automated structural checks only; an expired date or reachable URL does not establish legal programme status or eligibility.",
        "No opportunity records are modified by this audit."
    ]
}
for feed in manifest.get("feeds", []):
    filename = feed.get("file", "")
    if not filename or Path(filename).name != filename or not filename.endswith(".json"):
        report["feed_errors"].append("Unsafe feed filename in manifest")
        continue
    path = DATA / filename
    if not path.is_file():
        report["feed_errors"].append(f"{filename}: file missing")
        continue
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        report["feed_errors"].append(f"{filename}: invalid JSON")
        continue
    records = payload.get("records", [])
    if not isinstance(records, list):
        report["feed_errors"].append(f"{filename}: records is not a list")
        continue
    report["feeds_checked"] += 1
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            report["feed_errors"].append(f"{filename}: non-object record")
            continue
        report["records_checked"] += 1
        rid = record.get("id")
        if rid:
            if rid in seen:
                report["duplicate_ids"] += 1
            seen.add(rid)
        if not (record.get("title") or record.get("title_hu")):
            report["missing_titles"] += 1
        url = record.get("official_url") or record.get("url") or record.get("source_url")
        if not url:
            report["missing_urls"] += 1
        else:
            parsed = urlparse(str(url))
            if parsed.scheme != "https" or not parsed.netloc:
                report["invalid_urls"] += 1
        status = str(record.get("verification_status") or "").lower()
        if status and any(word in status for word in ("unverified", "not-yet-verified", "candidate")):
            report["unverified_status"] += 1
        deadline = record.get("deadline")
        if deadline:
            try:
                day = dt.date.fromisoformat(str(deadline)[:10])
                if day < today:
                    report["expired_deadlines"] += 1
            except ValueError:
                report["feed_errors"].append(f"{filename}: invalid deadline format")
report["feed_errors"] = report["feed_errors"][:100]
(DATA / "quality-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k != "notes"}, ensure_ascii=False, indent=2))
