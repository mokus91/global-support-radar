#!/usr/bin/env python3
"""Read-only readiness report for the Global Support Radar advertising inventory."""
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "advertising-inventory.json"
OUTPUT = ROOT / "advertising-readiness-report.md"


def build_report(data):
    inventory = data.get("inventory", [])
    advertisers = data.get("advertisers", [])
    events = data.get("revenue_events", [])
    errors = []
    for item in inventory:
        if item.get("enabled") and not item.get("owner_approved"):
            errors.append(f"{item.get('id')}: enabled without owner approval")
        if item.get("enabled") and item.get("status") != "active":
            errors.append(f"{item.get('id')}: enabled but status is not active")
        if item.get("external_code_present") and not item.get("owner_approved"):
            errors.append(f"{item.get('id')}: external code present without owner approval")
        if item.get("enabled") and item.get("sponsor_id") not in {a.get("id") for a in advertisers}:
            errors.append(f"{item.get('id')}: enabled without a registered advertiser")
    for advertiser in advertisers:
        if advertiser.get("contacted") and not advertiser.get("outreach_approved"):
            errors.append(f"{advertiser.get('id')}: contacted without outreach approval")
    verified_revenue = 0
    for event in events:
        amount = event.get("amount_huf", 0)
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
            errors.append(f"{event.get('id')}: invalid revenue amount")
            continue
        if event.get("received") and event.get("receipt_reference"):
            verified_revenue += amount
    active_slots = sum(1 for item in inventory if item.get("enabled") and item.get("status") == "active")
    lines = [
        "# Hirdetési készenléti jelentés",
        "",
        f"Jelentés dátuma: {date.today().isoformat()}",
        "",
        "## Összesítés",
        f"- Nyilvántartott hirdetési hely: {len(inventory)}",
        f"- Aktív hirdetési hely: {active_slots}",
        f"- Nyilvántartott hirdető: {len(advertisers)}",
        f"- Igazoltan beérkezett bevétel: {verified_revenue:,} Ft".replace(",", " "),
        f"- Ellenőrzési hiba: {len(errors)}",
        "",
        "## Hirdetési helyek",
    ]
    for item in inventory:
        lines.append(f"- {item.get('name', item.get('id'))}: {item.get('status', 'ismeretlen')} (bekapcsolva: {'igen' if item.get('enabled') else 'nem'})")
    lines.extend(["", "## Kapuk és hibák"])
    if errors:
        lines.extend(f"- HIBA: {error}" for error in errors)
    else:
        lines.append("- Nincs észlelt szabálysértés a nyilvántartásban.")
    lines.extend([
        "",
        "## Korlátok",
        "- Ez a jelentés csak a helyi nyilvántartásból dolgozik; nem ellenőriz külső szerződést, bankszámlát vagy hirdetői fiókot.",
        "- A bevétel csak beérkezett összeg és bizonylathivatkozás együttes megléte esetén számít igazoltnak.",
        "- A jelentés nem kapcsol be hirdetést, nem keres meg partnert, nem fizet és nem vállal költséget.",
        ""
    ])
    return "\n".join(lines), errors


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    report, errors = build_report(data)
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Report written: {OUTPUT}")
    print(f"Validation errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
