#!/usr/bin/env python3
"""Schema-aware quality audit; never rewrites source opportunity records."""
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
    "feeds_checked": 0,
    "records_checked": 0,
    "expired_deadlines": 0,
    "missing_urls": 0,
    "invalid_urls": 0,
    "duplicate_ids": 0,
    "missing_titles": 0,
    "unverified_status": 0,
    "non_opportunity_records": 0,
    "diagnostic_records_checked": 0,
    "diagnostic_missing_urls": 0,
    "feed_errors": [],
    "notes": [
        "Schema-aware audit: title_original and coofficial_title are accepted title fields for international feeds.",
        "Portal reachability diagnostics and dataset catalogue entries are not counted as grant opportunities.",
        "Unverified status is an information flag, not automatically a data error.",
        "No source opportunity records are modified by this audit."
    ]
}

TITLE_FIELDS = ("title", "title_hu", "title_original", "coofficial_title")
URL_FIELDS = ("official_url", "url", "source_url", "final_url")

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

    # This file describes portal connectivity, not grant opportunities.
    is_diagnostic_feed = filename == "worldwide-portal-health.json"
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            report["feed_errors"].append(f"{filename}: non-object record")
            continue

        if is_diagnostic_feed:
            report["diagnostic_records_checked"] += 1
            diagnostic_url = next((record.get(k) for k in URL_FIELDS if record.get(k)), None)
            if not diagnostic_url:
                report["diagnostic_missing_urls"] += 1
            else:
                parsed = urlparse(str(diagnostic_url))
                if parsed.scheme not in ("https", "http") or not parsed.netloc:
                    report["feed_errors"].append(f"{filename}: malformed diagnostic URL")
            continue

        # Dataset catalogue metadata is useful discovery material but is not a grant call.
        if record.get("record_type") == "dataset-discovery":
            report["non_opportunity_records"] += 1
            continue

        report["records_checked"] += 1
        rid = record.get("id")
        if rid:
            if rid in seen:
                report["duplicate_ids"] += 1
            seen.add(rid)

        if not any(record.get(k) for k in TITLE_FIELDS):
            report["missing_titles"] += 1

        url = next((record.get(k) for k in URL_FIELDS if record.get(k)), None)
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
(DATA / "quality-report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({k: v for k, v in report.items() if k != "notes"}, ensure_ascii=False, indent=2))
