#!/usr/bin/env python3
"""Validate generated discovery feeds after all source adapters have run."""
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ALLOWED_COUNTRY_CODES = {"EU", "UN", "INTL", "GLOBAL"}


def parse_timestamp(value, label):
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{label}: timestamp must be a non-empty ISO 8601 string")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(f"{label}: invalid ISO 8601 timestamp: {value}") from exc


def validate_https(value, label):
    if not isinstance(value, str) or not value:
        return
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise SystemExit(f"{label}: expected a safe HTTPS URL, got {value!r}")


def validate_date(value, label):
    if value in (None, ""):
        return
    if not isinstance(value, str):
        raise SystemExit(f"{label}: date must be a string")
    try:
        if "T" in value or " " in value:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"{label}: invalid ISO date/time: {value!r}") from exc


def main():
    files = sorted(DATA.glob("*discovery.json"))
    checked_files = 0
    checked_records = 0
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.name}: invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
        if not isinstance(payload, dict):
            raise SystemExit(f"{path.name}: root must be a JSON object")

        timestamp = payload.get("generated_at") or payload.get("updated_at")
        if timestamp:
            parse_timestamp(timestamp, path.name)

        source_url = payload.get("source_url")
        if source_url:
            validate_https(source_url, f"{path.name} source_url")

        records = payload.get("records", [])
        if not isinstance(records, list):
            raise SystemExit(f"{path.name}: records must be a list")
        declared_count = payload.get("records_count")
        if declared_count is not None and declared_count != len(records):
            raise SystemExit(
                f"{path.name}: records_count={declared_count} but records contains {len(records)} items"
            )

        for index, row in enumerate(records):
            label = f"{path.name} record {index + 1}"
            if not isinstance(row, dict):
                raise SystemExit(f"{label}: record must be an object")
            for key in ("official_url", "application_url", "legal_bases_url", "url"):
                if row.get(key):
                    validate_https(row[key], f"{label} {key}")
            for key in ("deadline", "deadline_date", "start_date", "opening_date", "acceptance_start", "acceptance_end"):
                validate_date(row.get(key), f"{label} {key}")
            country = row.get("country_code")
            if country and not (
                re.fullmatch(r"[A-Z]{2}", str(country)) or country in ALLOWED_COUNTRY_CODES
            ):
                raise SystemExit(f"{label}: invalid country_code {country!r}")
            for key in ("amount_maximum", "amount_max", "total_call_budget", "maximum_amount_jpy"):
                amount = row.get(key)
                if amount is not None and (
                    not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0
                ):
                    raise SystemExit(f"{label}: {key} must be a non-negative number")

        checked_files += 1
        checked_records += len(records)

    # Validate the status manifest separately: it is operational metadata, not an opportunity feed.
    status_path = DATA / "feed-status.json"
    if status_path.exists():
        try:
            manifest = json.loads(status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"feed-status.json: invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
        if not isinstance(manifest, dict) or not isinstance(manifest.get("feeds"), list):
            raise SystemExit("feed-status.json: root must contain a feeds list")
        parse_timestamp(manifest.get("checked_at"), "feed-status.json checked_at")
        seen_files = set()
        allowed_statuses = {"checked", "checked-empty", "temporarily-unavailable", "missing", "invalid-json"}
        allowed_freshness = {"fresh", "aging", "stale", "unknown"}
        for index, feed in enumerate(manifest["feeds"]):
            label = f"feed-status.json feed {index + 1}"
            if not isinstance(feed, dict):
                raise SystemExit(f"{label}: entry must be an object")
            filename = feed.get("file")
            if not isinstance(filename, str) or not filename.endswith(".json") or "/" in filename or "\\\\" in filename:
                raise SystemExit(f"{label}: file must be a simple JSON filename")
            if filename in seen_files:
                raise SystemExit(f"{label}: duplicate feed filename {filename!r}")
            seen_files.add(filename)
            parse_timestamp(feed.get("checked_at"), f"{label} checked_at")
            if feed.get("status") not in allowed_statuses:
                raise SystemExit(f"{label}: unsupported status {feed.get('status')!r}")
            count = feed.get("records_count")
            if count is not None and (not isinstance(count, int) or isinstance(count, bool) or count < 0):
                raise SystemExit(f"{label}: records_count must be a non-negative integer or null")
            freshness = feed.get("freshness")
            if freshness is not None and freshness not in allowed_freshness:
                raise SystemExit(f"{label}: unsupported freshness {freshness!r}")
            age = feed.get("feed_age_hours")
            if age is not None and (not isinstance(age, (int, float)) or isinstance(age, bool) or age < 0):
                raise SystemExit(f"{label}: feed_age_hours must be a non-negative number")

    print(f"Post-discovery validation passed: {checked_files} feeds and {checked_records} records checked.")


if __name__ == "__main__":
    main()
