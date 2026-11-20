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
    "verification_tiers": {"verified_open": 0, "api_window_candidate": 0, "official_listing_candidate": 0, "unverified": 0, "other": 0},
    "feed_summary": [],
    "source_status_summary": [],
    "review_queue_count": 0,
    "review_queue": [],
    "non_opportunity_records": 0,
    "historical_archive_records": 0,
    "diagnostic_records_checked": 0,
    "diagnostic_missing_urls": 0,
    "feed_errors": [],
    "notes": [
        "Schema-aware audit: title_original and coofficial_title are accepted title fields for international feeds.",
        "Portal reachability diagnostics, dataset catalogue entries and historical award archives are not counted as current grant opportunities.",
        "Unverified status is an information flag, not automatically a data error.",
        "No source opportunity records are modified by this audit."
    ]
}

TITLE_FIELDS = ("title", "title_hu", "title_original", "coofficial_title")
URL_FIELDS = ("official_url", "url", "source_url", "final_url")
AMOUNT_FIELDS = ("amount_maximum", "amount_max", "budget", "total_call_budget", "award_ceiling", "estimated_funding")
ELIGIBILITY_FIELDS = ("eligibility", "eligible_applicants", "beneficiary", "target_group", "applicant_type")

status_observations = {}

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
    feed_counts = {"file": filename, "records": 0, "unverified": 0, "api_window_candidates": 0, "official_listing_candidates": 0, "historical_archive_records": 0}
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

        # Historical award archives are not current application opportunities.
        if str(record.get("record_type") or "").startswith("historical-"):
            report["historical_archive_records"] += 1
            feed_counts["historical_archive_records"] += 1
            continue

        # Dataset catalogue metadata is useful discovery material but is not a grant call.
        if record.get("record_type") == "dataset-discovery":
            report["non_opportunity_records"] += 1
            continue

        report["records_checked"] += 1
        feed_counts["records"] += 1

        # Build a human-readable review queue from the best-documented candidates.
        # A score indicates available information, not confirmation that a call is open.
        title = next((record.get(k) for k in TITLE_FIELDS if record.get(k)), None)
        url = next((record.get(k) for k in URL_FIELDS if record.get(k)), None)
        deadline_value = next((record.get(k) for k in ("deadline", "acceptance_end", "application_deadline", "close_date", "closeDate") if record.get(k)), None)
        amount_value = next((record.get(k) for k in AMOUNT_FIELDS if record.get(k) not in (None, "", [], {})), None)
        eligibility_value = next((record.get(k) for k in ELIGIBILITY_FIELDS if record.get(k) not in (None, "", [], {})), None)
        source_status_value = record.get("status") or record.get("status_code") or record.get("application_window_status") or record.get("opportunityStatus")
        if source_status_value not in (None, "", [], {}):
            status_key = str(source_status_value).strip()[:120]
            status_observations[(filename, status_key)] = status_observations.get((filename, status_key), 0) + 1
        missing_details = []
        score = 0
        if title:
            score += 2
        else:
            missing_details.append("title")
        if url:
            score += 2
        else:
            missing_details.append("official_url")
        if deadline_value:
            score += 2
        else:
            missing_details.append("deadline")
        if amount_value is not None:
            score += 1
        else:
            missing_details.append("funding_amount")
        if eligibility_value is not None:
            score += 2
        else:
            missing_details.append("eligibility")
        if source_status_value not in (None, "", [], {}):
            score += 1
        else:
            missing_details.append("source_status")
        deadline_state = "unknown"
        if deadline_value:
            try:
                deadline_day = dt.date.fromisoformat(str(deadline_value)[:10])
                deadline_state = "expired" if deadline_day < today else "upcoming"
            except ValueError:
                deadline_state = "unparsed"
        if title or url:
            report["review_queue"].append({
                "source_file": filename,
                "id": str(record.get("id") or ""),
                "title": str(title or "Untitled")[:240],
                "official_url": str(url or ""),
                "deadline": str(deadline_value or ""),
                "deadline_state": deadline_state,
                "source_status": str(source_status_value or "")[:100],
                "score": score,
                "missing_details": missing_details
            })

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

        status = str(record.get("verification_status") or "").strip().lower()
        record_state = str(record.get("status") or "").strip().lower()
        record_type = str(record.get("record_type") or "").strip().lower()
        combined = status + " " + record_state + " " + record_type
        is_unverified = "unverified" in status or "not-yet-verified" in status
        if is_unverified:
            report["unverified_status"] += 1
            feed_counts["unverified"] += 1

        # Discovery candidates remain candidates; this is not an open-status claim.
        if "official_api_live_acceptance_candidate" in status or "official-api-window-current" in status:
            report["verification_tiers"]["api_window_candidate"] += 1
            feed_counts["api_window_candidates"] += 1
        elif any(token in combined for token in ("candidate", "official-listing", "rss-discovery")):
            report["verification_tiers"]["official_listing_candidate"] += 1
            feed_counts["official_listing_candidates"] += 1
        elif (
            status in {"official_page_open_status_and_amount_checked", "official-page-open-status-and-amount-checked"}
            and record_state in {"open-and-current", "verified-open"}
        ) or ("verified" in status and "unverified" not in status and record_state not in {"closed", "withdrawn", "expired"}):
            report["verification_tiers"]["verified_open"] += 1
        elif is_unverified:
            report["verification_tiers"]["unverified"] += 1
        else:
            report["verification_tiers"]["other"] += 1

        deadline = next((record.get(k) for k in ("deadline", "acceptance_end", "application_deadline", "close_date", "closeDate") if record.get(k)), None)
        if deadline:
            try:
                day = dt.date.fromisoformat(str(deadline)[:10])
                if day < today:
                    report["expired_deadlines"] += 1
            except ValueError:
                report["feed_errors"].append(f"{filename}: invalid deadline format")

    report["feed_summary"].append(feed_counts)

report["source_status_summary"] = [
    {"source_file": source_file, "source_status": source_status, "records": count}
    for (source_file, source_status), count in sorted(status_observations.items(), key=lambda item: (item[0][0], item[0][1].lower()))
]
report["feed_errors"] = report["feed_errors"][:100]
report["review_queue"].sort(key=lambda item: ({"upcoming": 0, "unknown": 1, "unparsed": 2, "expired": 3}.get(item["deadline_state"], 4), -item["score"], item["deadline"] or "9999", item["source_file"], item["id"]))
report["review_queue"] = report["review_queue"][:50]
report["review_queue_count"] = len(report["review_queue"])
(DATA / "quality-report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({k: v for k, v in report.items() if k != "notes"}, ensure_ascii=False, indent=2))
