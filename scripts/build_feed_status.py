#!/usr/bin/env python3
"""Build a transparent status manifest for automated discovery feeds.

The manifest records when this pipeline inspected each local feed file. It does
not claim that the upstream publisher changed its data at that time.
"""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = DATA / "feed-status.json"

FEEDS = [
    ("Japan — JGrants", "jgrants-discovery.json"),
    ("Chile — CORFO / Sercotec", "chile-discovery.json"),
    ("Spain — SNPSAP", "spain-discovery.json"),
    ("France — Aides-territoires", "france-aides-territoires-discovery.json"),
    ("New Zealand — Government Funding Explorer", "nz-funding-explorer-discovery.json"),
    ("EU — Funding & Tenders", "eu-funding-discovery.json"),
    ("EU — open calls", "eu-open-calls-discovery.json"),
    ("EU — CAP Network", "eu-cap-network-discovery.json"),
    ("EU — national agriculture", "eu-national-agriculture-discovery.json"),
    ("EU — national categories", "eu-national-category-discovery.json"),
    ("USA — Grants.gov", "us-grants-discovery.json"),
    ("UK — UKRI", "ukri-discovery.json"),
    ("Australia — ARC", "au-arc-grants-discovery.json"),
    ("Canada — CIHR", "ca-cihr-discovery.json"),
    ("Hungary — open data", "hu-open-data-discovery.json"),
    ("Hungary — grant announcements", "hu-palyazat-announcements.json"),
    ("Hungary — NKFIH current calls", "hu-nkfih-discovery.json"),
    ("Worldwide — portal reachability", "worldwide-portal-health.json"),
]

def count_records(data):
    for key in ("records", "results", "items", "opportunities", "grants"):
        value = data.get(key)
        if isinstance(value, list):
            return len(value)
    return None

def main():
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    entries = []
    for name, filename in FEEDS:
        path = DATA / filename
        entry = {"name": name, "file": filename, "checked_at": now,
                 "status": "missing", "records_count": None,
                 "source_updated_at": None, "note": ""}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                entry["status"] = data.get("fetch_status") or "checked"
                entry["records_count"] = count_records(data)
                for key in ("source_updated_at", "updated_at", "generated_at",
                            "fetched_at", "retrieved_at", "checked_at"):
                    if data.get(key):
                        entry["source_updated_at"] = data[key]
                        break
                if data.get("http_status"):
                    entry["http_status"] = data["http_status"]
                if data.get("query_errors"):
                    entry["note"] = "One or more upstream queries reported errors."
                elif data.get("note"):
                    entry["note"] = str(data["note"])[:240]
                if entry["status"] == "checked" and entry["records_count"] == 0:
                    entry["status"] = "checked-empty"
            except Exception as exc:
                entry["status"] = "invalid-json"
                entry["note"] = type(exc).__name__
        entries.append(entry)
    OUTPUT.write_text(json.dumps({
        "schema_version": "1.0",
        "checked_at": now,
        "note": "checked_at means the automation inspected the local feed file; it is not proof of upstream publication time or that every opportunity is open.",
        "feeds": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Feed status manifest created: {len(entries)} feeds")

if __name__ == "__main__":
    main()
