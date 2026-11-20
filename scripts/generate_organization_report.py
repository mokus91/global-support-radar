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
        items = payload.get("records", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict):
                record = dict(item)
                record["_dataset"] = path.name
                record["_dataset_checked_at"] = (
                    payload.get("updated_at") or payload.get("generated_at") or ""
                )
                records.append(record)
    return records


def classify(record: dict[str, Any], today: date) -> str:
    status = str(record.get("status") or record.get("verification_status") or "").lower()
    if status in CLOSED_STATUSES:
        return "exclude"
    deadline = record.get("deadline")
    if deadline:
        try:
            if date.fromisoformat(str(deadline)[:10]) < today:
                return "exclude"
        except ValueError:
            pass
    if status in OPEN_STATUSES:
        return "verified"
    if status in CANDIDATE_STATUSES:
        return "candidate"
    return "exclude"


def title_of(record: dict[str, Any]) -> str:
    return str(record.get("title_hu") or record.get("title") or
               record.get("title_original") or record.get("name") or "Cím nélkül")


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
            url = item.get("official_url") or item.get("url") or ""
            status_text = (
                "Nyitottként jelzett a forrásadapterben; az egyéni jogosultság nincs igazolva."
                if not candidate else
                "Nyilvántartási időablak-jelölt; a tényleges nyitottságot és feltételeket ellenőrizni kell."
            )
            lines.extend([
                f"### {country} – {title_of(item)}",
                "",
                f"- **Státusz:** {status_text}",
                f"- **Kategória:** {item.get('category') or ', '.join(item.get('categories', [])) or 'nincs megadva'}",
                f"- **Határidő:** {item.get('deadline') or 'nincs megadva'}",
                f"- **Összeg/keret:** {item.get('amount_max') or item.get('total_call_budget') or 'nincs megadva'} {item.get('currency') or item.get('amount_currency') or ''}".rstrip(),
                f"- **Forrásellenőrzés:** {item.get('source_checked_at') or item.get('_dataset_checked_at') or 'nincs időbélyeg'}",
                f"- **Adatfájl:** {item.get('_dataset')}",
                f"- **Hivatalos forrás:** {url if url else 'nincs megadva'}",
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
    print("Self-test: 5 checks passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("reports/organization-report-latest.md"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    today = datetime.now(timezone.utc).date()
    report = render(load_records(args.data_dir), today)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Report written: {args.output}")


if __name__ == "__main__":
    main()
