#!/usr/bin/env python3
"""Create a conservative change log for official opportunity feeds."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TRACKED = [
    "jgrants-discovery.json", "chile-discovery.json", "spain-discovery.json",
    "france-aides-territoires-discovery.json", "nz-funding-explorer-discovery.json",
    "eu-funding-discovery.json", "eu-open-calls-discovery.json",
    "eu-cap-network-discovery.json", "us-grants-discovery.json", "ukri-discovery.json",
    "au-arc-grants-discovery.json", "ca-cihr-discovery.json",
    "hu-palyazat-announcements.json", "hu-nkfih-discovery.json",
]
OUTPUT = DATA / "opportunity-changes.json"
FIELDS = ("status", "application_status", "call_status", "deadline", "acceptance_end",
          "application_deadline", "amount_maximum", "total_call_budget", "amount_currency",
          "eligibility_status", "title", "title_original", "title_en")

def load_previous(filename):
    try:
        raw = subprocess.run(["git", "show", f"HEAD:data/{filename}"], cwd=ROOT,
                             check=True, capture_output=True, text=True).stdout
        data = json.loads(raw)
        return data.get("records", []) if isinstance(data, dict) else []
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []

def key_for(row):
    for field in ("id", "identifier", "grant_id", "opportunity_id"):
        value = row.get(field)
        if value not in (None, ""):
            return "id:" + str(value).strip().lower()
    url = row.get("official_url") or row.get("application_url") or row.get("url")
    title = row.get("title_original") or row.get("title") or row.get("title_en") or ""
    normalized_url = str(url or "").strip().split("#")[0].rstrip("/").lower()
    normalized_title = " ".join(str(title).split()).casefold()
    # Keep deadlines out of identity: a changed deadline must be detected as an update,
    # not misreported as one removed record plus one new record.
    if not normalized_title and not normalized_url:
        return None
    identity = "|".join((normalized_url, normalized_title))
    return "fallback:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()

def signature(row):
    return {field: row.get(field) for field in FIELDS if row.get(field) not in (None, "", [], {})}

def load_feed_status():
    try:
        manifest = json.loads((DATA / "feed-status.json").read_text(encoding="utf-8"))
        return {item.get("file"): item for item in manifest.get("feeds", [])
                if isinstance(item, dict) and item.get("file")}
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}

def allow_removal_events(filename, status_by_file):
    """Avoid treating missing records as removals from incomplete feeds."""
    status = status_by_file.get(filename, {})
    if status.get("status") == "temporarily-unavailable":
        return False
    # ARC is deliberately capped at 40 pages. Reaching the cap means this
    # snapshot is partial and cannot support reliable removal detection.
    if filename == "au-arc-grants-discovery.json" and status.get("pages_fetched", 0) >= 40:
        return False
    return True

def main():
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    events = []
    status_by_file = load_feed_status()
    for filename in TRACKED:
        path = DATA / filename
        if not path.exists():
            continue
        try:
            current_data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        current_rows = current_data.get("records", []) if isinstance(current_data, dict) else []
        previous_rows = load_previous(filename)
        old = {key_for(row): row for row in previous_rows if isinstance(row, dict) and key_for(row)}
        new = {key_for(row): row for row in current_rows if isinstance(row, dict) and key_for(row)}
        for key, row in new.items():
            before = old.get(key)
            if before is None:
                events.append({"type": "new", "feed": filename, "key": key,
                               "title": row.get("title") or row.get("title_original") or row.get("title_en") or key,
                               "detected_at": now})
            elif signature(before) != signature(row):
                events.append({"type": "changed", "feed": filename, "key": key,
                               "title": row.get("title") or row.get("title_original") or row.get("title_en") or key,
                               "before": signature(before), "after": signature(row), "detected_at": now})
        if allow_removal_events(filename, status_by_file):
            for key, row in old.items():
                if key not in new:
                    events.append({"type": "removed_from_feed", "feed": filename, "key": key,
                                   "title": row.get("title") or row.get("title_original") or row.get("title_en") or key,
                                   "detected_at": now,
                                   "note": "No longer present in this feed; this does not prove the opportunity is closed."})
    # Keep the newest events only; absence is never labelled as confirmed closure.
    events = events[-500:]
    OUTPUT.write_text(json.dumps({"schema_version": "1.0", "generated_at": now,
        "events_count": len(events), "events": events,
        "note": "Changes are detected by comparing repository snapshots. Removals are suppressed for unavailable feeds and capped ARC snapshots; removed records are not assumed closed. Always confirm status at the official source."},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Opportunity change log created: {len(events)} events")

if __name__ == "__main__":
    main()
