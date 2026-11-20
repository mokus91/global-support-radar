#!/usr/bin/env python3
"""Read-only beta data-quality report for feeds listed in data/feed-status.json.

This check is deliberately offline: it never calls external URLs and never edits
or deletes source records. Warnings are review signals, not closure decisions.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
URL_FIELDS = ("official_url", "url", "source_url", "final_url")
DEADLINE_FIELDS = ("deadline", "acceptance_end", "application_deadline", "close_date", "closeDate")
TITLE_FIELDS = ("title", "title_hu", "title_original", "coofficial_title")


def parse_timestamp(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def valid_https_url(value):
    parsed = urlparse(str(value or ""))
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password


def audit(data_dir: Path, now: dt.datetime | None = None, stale_after_hours: int = 72):
    now = now or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    manifest_path = data_dir / "feed-status.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    feeds = manifest.get("feeds")
    if not isinstance(feeds, list):
        raise ValueError("feed-status.json: feeds must be a list")

    report = {
        "generated_at": now.astimezone(dt.timezone.utc).isoformat(),
        "feeds_checked": 0,
        "records_checked": 0,
        "duplicate_ids": 0,
        "missing_titles": 0,
        "missing_urls": 0,
        "invalid_urls": 0,
        "stale_feeds": 0,
        "overdue_deadlines": 0,
        "feed_errors": [],
        "warnings": [],
    }
    seen_files = set()
    for feed in feeds:
        filename = feed.get("file") if isinstance(feed, dict) else None
        if not isinstance(filename, str) or Path(filename).name != filename or not filename.endswith(".json"):
            report["feed_errors"].append("Manifest contains an unsafe feed filename")
            continue
        if filename in seen_files:
            report["feed_errors"].append(f"{filename}: duplicate manifest entry")
            continue
        seen_files.add(filename)
        path = data_dir / filename
        if not path.is_file():
            report["feed_errors"].append(f"{filename}: file missing")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            report["feed_errors"].append(f"{filename}: cannot read valid JSON ({exc})")
            continue
        if not isinstance(payload, dict):
            report["feed_errors"].append(f"{filename}: top-level JSON must be an object")
            continue
        records = payload.get("records", [])
        if not isinstance(records, list):
            report["feed_errors"].append(f"{filename}: records must be a list")
            continue
        report["feeds_checked"] += 1
        declared = feed.get("records_count")
        if isinstance(declared, int) and declared != len(records) and feed.get("status") in {"checked", "checked-empty"}:
            report["warnings"].append(f"{filename}: manifest count {declared} differs from file count {len(records)}")

        checked_at = parse_timestamp(feed.get("checked_at"))
        if checked_at is None:
            report["warnings"].append(f"{filename}: missing or invalid timezone-aware checked_at")
        else:
            age = (now.astimezone(dt.timezone.utc) - checked_at.astimezone(dt.timezone.utc)).total_seconds() / 3600
            if age < -1:
                report["warnings"].append(f"{filename}: checked_at is more than one hour in the future")
            elif age > stale_after_hours:
                report["stale_feeds"] += 1
                report["warnings"].append(f"{filename}: feed check is stale ({age:.1f} hours)")
        if feed.get("status") == "temporarily-unavailable":
            report["warnings"].append(f"{filename}: upstream temporarily unavailable; retained data needs caution")
        elif feed.get("status") in {"missing", "invalid-json"}:
            report["warnings"].append(f"{filename}: manifest status is {feed.get('status')}")

        ids = set()
        for index, row in enumerate(records):
            if not isinstance(row, dict):
                report["feed_errors"].append(f"{filename}: record {index} is not an object")
                continue
            report["records_checked"] += 1
            record_id = row.get("id") or row.get("identifier")
            if record_id:
                key = str(record_id)
                if key in ids:
                    report["duplicate_ids"] += 1
                    report["warnings"].append(f"{filename}: duplicate record ID {key}")
                ids.add(key)
            if not any(row.get(field) for field in TITLE_FIELDS):
                report["missing_titles"] += 1
            url = next((row.get(field) for field in URL_FIELDS if row.get(field)), None)
            if not url:
                report["missing_urls"] += 1
            elif not valid_https_url(url):
                report["invalid_urls"] += 1
            deadline = next((row.get(field) for field in DEADLINE_FIELDS if row.get(field)), None)
            if deadline:
                try:
                    day = dt.date.fromisoformat(str(deadline)[:10])
                except ValueError:
                    report["warnings"].append(f"{filename}: unparseable deadline on record {record_id or index}")
                else:
                    status = str(row.get("status") or row.get("application_status") or "").lower()
                    if day < now.date() and status not in {"closed", "expired", "withdrawn", "cancelled", "canceled"}:
                        report["overdue_deadlines"] += 1
    if report["duplicate_ids"]:
        report["warnings"].append(f"Duplicate IDs found: {report['duplicate_ids']}")
    if report["missing_urls"]:
        report["warnings"].append(f"Records without a source URL: {report['missing_urls']}")
    if report["invalid_urls"]:
        report["warnings"].append(f"Records with a non-HTTPS or malformed source URL: {report['invalid_urls']}")
    if report["missing_titles"]:
        report["warnings"].append(f"Records without a recognized title: {report['missing_titles']}")
    if report["overdue_deadlines"]:
        report["warnings"].append(f"Past deadlines requiring status review: {report['overdue_deadlines']}")
    return report


def main():
    report = audit(DATA)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["feed_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
