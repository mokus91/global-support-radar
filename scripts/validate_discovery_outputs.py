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

    print(f"Post-discovery validation passed: {checked_files} feeds and {checked_records} records checked.")


if __name__ == "__main__":
    main()
