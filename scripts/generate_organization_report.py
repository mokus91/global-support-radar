#!/usr/bin/env python3
"""Build a cautious organization monitoring report from local discovery JSON files.

Only explicitly open records are presented as verified-open. Official registry
window matches are separated as candidates. Discovery-only/unverified records
are never promoted into either section.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

OPEN_STATUSES = {"open-and-current", "open", "official-page-checked-open"}
CANDIDATE_STATUSES = {"official-api-window-current", "official-registry-window-current"}
CLOSED_STATUSES = {"closed", "expired", "withdrawn"}


def load_records(data_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(data_dir.glob("*-discovery.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"WARNING: skipped {path.name}: {exc}")
            continue
        if not isinstance(payload, dict):
            print(f"WARNING: skipped {path.name}: top-level JSON must be an object")
            continue
        items = payload.get("records", [])
        if not isinstance(items, list):
            print(f"WARNING: skipped records in {path.name}: expected a list")
            continue
        checked_at = payload.get("updated_at") or payload.get("generated_at") or ""
        for item in items:
            if isinstance(item, dict):
                record = dict(item)
                record["_dataset"] = path.name
                record["_dataset_checked_at"] = checked_at
                records.append(record)
    return records


def classify(record: dict[str, Any], today: date) -> str:
    # Consider both fields: a closed signal must override an open signal.
    statuses = {
        str(record.get(key) or "").strip().lower()
        for key in ("status", "verification_status")
    }
    statuses.discard("")
    if statuses & CLOSED_STATUSES:
        return "exclude"

    deadline = record.get("deadline")
    if deadline not in (None, ""):
        try:
            parsed_deadline = date.fromisoformat(str(deadline)[:10])
        except (TypeError, ValueError):
            return "exclude"
        if parsed_deadline < today:
            return "exclude"

    if statuses & OPEN_STATUSES:
        return "verified"
    if statuses & CANDIDATE_STATUSES:
        return "candidate"
    return "exclude"


def title_of(record: dict[str, Any]) -> str:
    return str(record.get("title_hu") or record.get("title") or
               record.get("title_original") or record.get("name") or "Cím nélkül")


def official_url_of(record: dict[str, Any]) -> str:
    candidate = record.get("official_url") or record.get("url") or ""
    if not isinstance(candidate, str):
        return ""
    parsed = urlparse(candidate.strip())
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        return ""
    return candidate.strip()


def amount_of(record: dict[str, Any]) -> str:
    amount = record.get("amount_max")
    if amount in (None, ""):
        amount = record.get("total_call_budget")
    if amount in (None, ""):
        return "nincs megadva"
    currency = record.get("currency") or record.get("amount_currency") or ""
    return f"{amount} {currency}".strip()


def _values(record: dict[str, Any], keys: tuple[str, ...]) -> set[str]:
    values: set[str] = set()
    for key in keys:
        value = record.get(key)
        if isinstance(value, list):
            values.update(str(part).strip().casefold() for part in value if part not in (None, ""))
        elif value not in (None, ""):
            values.add(str(value).strip().casefold())
    return values


def filter_records(
    records: list[dict[str, Any]],
    country: str | None = None,
    category: str | None = None,
) -> list[dict[str, Any]]:
    """Filter by exact country/category aliases; matching is case-insensitive."""
    result = records
    if country:
        wanted = country.strip().casefold()
        country_keys = ("country_code", "country", "country_hu", "country_en", "country_name", "country_name_hu")
        result = [r for r in result if wanted in _values(r, country_keys)]
    if category:
        wanted = category.strip().casefold()
        category_keys = ("category", "categories", "category_hu", "category_en", "topic", "topics")
        result = [r for r in result if wanted in _values(r, category_keys)]
    return result


def render(records: list[dict[str, Any]], today: date) -> str:
    verified, candidates = [], []
    for record in records:
        bucket = classify(record, today)
        if bucket == "verified":
            verified.append(record)
        elif bucket == "candidate":
            candidates.append(record)

    lines = [
        "# Szervezeti támogatásfigyelő riport",
        "",
        f"**Generálás dátuma:** {today.isoformat()}",
        "**Adatforrás:** a repository data/*-discovery.json fájljai",
        "**Módszer:** automatikus státuszszűrés; nem teljes körű piaci vagy jogosultsági vizsgálat.",
        "",
        "> A riport csak a forrásadatok pillanatképét tükrözi. Minden határidőt, feltételt és",
        "> beadási lehetőséget az eredeti kiírói oldalon kell újraellenőrizni.",
        "",
        "## Vezetői összefoglaló",
        "",
        f"- Kifejezetten nyitottként jelölt rekord: **{len(verified)}**.",
        f"- Hivatalos nyilvántartás időablaka alapján ellenőrzendő jelölt: **{len(candidates)}**.",
        f"- Discovery/unverified rekordok nem kerülnek ajánlatként a riportba.",
        "",
    ]

    def add_section(heading: str, items: list[dict[str, Any]], candidate: bool) -> None:
        lines.extend([f"## {heading}", ""])
        if not items:
            lines.extend(["Nincs megfelelő rekord az aktuális helyi adatfájlokban.", ""])
            return
        for item in sorted(items, key=lambda x: (str(x.get("country_code", "")), title_of(x))):
            country = item.get("country_hu") or item.get("country_en") or item.get("country_code") or "Ismeretlen ország"
            url = official_url_of(item)
            status_text = (
                "Nyitottként jelzett a forrásadapterben; az egyéni jogosultság nincs igazolva."
                if not candidate else
                "Nyilvántartási időablak-jelölt; a tényleges nyitottságot és feltételeket ellenőrizni kell."
            )
            categories = item.get("categories")
            if not isinstance(categories, list):
                categories = []
            category = item.get("category") or ", ".join(str(x) for x in categories) or "nincs megadva"
            lines.extend([
                f"### {country} – {title_of(item)}",
                "",
                f"- **Státusz:** {status_text}",
                f"- **Kategória:** {category}",
                f"- **Határidő:** {item.get('deadline') or 'nincs megadva'}",
                f"- **Összeg/keret:** {amount_of(item)}",
                f"- **Forrásellenőrzés:** {item.get('source_checked_at') or item.get('_dataset_checked_at') or 'nincs időbélyeg'}",
                f"- **Adatfájl:** {item.get('_dataset', 'nincs megadva')}",
                f"- **Hivatalos forrás:** {url if url else 'nincs megadva vagy nem biztonságos URL'}",
                "",
            ])

    add_section("Kifejezetten nyitottként jelzett lehetőségek", verified, False)
    add_section("Ellenőrzendő nyilvántartási jelöltek", candidates, True)
    lines.extend([
        "## Korlátok",
        "",
        "- A rekord státusza nem bizonyítja a szervezet vagy személy jogosultságát.",
        "- A teljes pályázati keret nem azonos az egy pályázónak járó összeggel.",
        "- A lejárt, lezárt és visszavont rekordok nem jelennek meg nyitott lehetőségként.",
        "- A hibás határidővel vagy nem HTTPS forráslinkkel rendelkező rekord nem minősül ellenőrzöttnek.",
        "- Az ismeretlen vagy discovery-only státuszú adatok nem kerülnek be a találati listákba.",
        "- A riport tájékoztató jellegű; nem jogi, adózási vagy pályázatírási tanács.",
        "",
    ])
    return "\n".join(lines)


def self_test() -> None:
    today = date(2026, 11, 20)
    assert classify({"status": "open-and-current", "deadline": "2026-11-24"}, today) == "verified"
    assert classify({"status": "official-api-window-current", "deadline": "2026-12-01"}, today) == "candidate"
    assert classify({"status": "official-api-window-current", "deadline": "2026-11-19"}, today) == "exclude"
    assert classify({"verification_status": "unverified"}, today) == "exclude"
    assert classify({"status": "closed"}, today) == "exclude"
    assert classify({"status": "open", "verification_status": "withdrawn"}, today) == "exclude"
    assert classify({"status": "open", "deadline": "not-a-date"}, today) == "exclude"
    sample = [
        {"country_code": "HU", "categories": ["business", "energy"]},
        {"country_hu": "Magyarország", "category": "Agriculture"},
        {"country_code": "ES", "category": "business-growth"},
    ]
    assert len(filter_records(sample, country="hu")) == 1
    assert len(filter_records(sample, country="MAGYARORSZÁG")) == 1
    assert len(filter_records(sample, category="BUSINESS")) == 1
    assert len(filter_records(sample, category="business-growth")) == 1
    assert len(filter_records(sample)) == 3
    print("Self-test: 12 checks passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("reports/organization-report-latest.md"))
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--country", help="Exact country code or country name (case-insensitive)")
    parser.add_argument("--category", help="Exact category/topic label (case-insensitive)")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    today = datetime.now(timezone.utc).date()
    records = filter_records(load_records(args.data_dir), country=args.country, category=args.category)
    report = render(records, today)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Report written: {args.output}")


if __name__ == "__main__":
    main()
