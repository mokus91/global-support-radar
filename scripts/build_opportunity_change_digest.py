#!/usr/bin/env python3
"""Render a human-readable, cautious digest from the opportunity change log."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

EU_CALL_STATUS = {
    "31094501": "Előzetesen meghirdetett (Forthcoming)",
    "31094502": "Nyitott (Open)",
    "31094503": "Lezárt (Closed)",
}
IMPORTANT_FIELDS = {
    "status": "Státusz", "application_status": "Jelentkezési státusz",
    "call_status": "Felhívás státusza", "deadline": "Határidő",
    "acceptance_end": "Benyújtás vége", "application_deadline": "Pályázati határidő",
    "amount_maximum": "Maximális támogatás", "total_call_budget": "Teljes keret",
    "amount_currency": "Pénznem", "eligibility_status": "Jogosultsági státusz",
}

def display_value(field: str, value: Any) -> str:
    if field in {"status", "application_status", "call_status"}:
        return EU_CALL_STATUS.get(str(value), str(value))
    return str(value)

def build_digest(payload: dict[str, Any]) -> str:
    events = payload.get("events", [])
    if not isinstance(events, list):
        events = []
    lines = [
        "# Támogatási lehetőségek változásfigyelője", "",
        f"**Adatpillanatkép:** {payload.get('generated_at', 'ismeretlen')}",
        f"**Események:** {len(events)}", "",
        "> Ez a lista adatforrás-pillanatképek közötti eltéréseket mutat. A változás nem bizonyítja,",
        "> hogy a felhívás még nyitott vagy hogy bárki jogosult rá. Minden esetben ellenőrizd a hivatalos kiírást.", "",
    ]
    if not events:
        lines.extend(["Nincs rögzített változás az aktuális összehasonlításban.", ""])
    for event in events:
        if not isinstance(event, dict):
            continue
        kind = event.get("type", "unknown")
        title = event.get("title") or event.get("key") or "Cím nélkül"
        feed = event.get("feed") or "ismeretlen adatforrás"
        lines.extend([f"## {title}", "", f"- **Esemény:** {kind}", f"- **Adatforrás:** {feed}"])
        if kind == "changed":
            before, after = event.get("before") or {}, event.get("after") or {}
            changed = []
            for field, label in IMPORTANT_FIELDS.items():
                old, new = before.get(field), after.get(field)
                if old != new and (old not in (None, "") or new not in (None, "")):
                    old_text = display_value(field, old) if old is not None else "nincs adat"
                    new_text = display_value(field, new) if new is not None else "nincs adat"
                    changed.append(f"  - {label}: **{old_text}** → **{new_text}**")
            lines.extend(changed or ["- A figyelt mezőkben nem látható értelmezhető változás."])
        elif kind == "removed_from_feed":
            lines.append("- **Figyelmeztetés:** eltűnt az adatforrás pillanatképéből; ez önmagában nem jelenti a felhívás lezárását.")
        elif kind == "new":
            lines.append("- Új rekord jelent meg a figyelt adatforrásban; a nyitottságot és feltételeket ellenőrizni kell.")
        lines.extend(["- **Ellenőrzés:** a kiíró hivatalos oldalán szükséges.", ""])
    lines.extend([
        "## Értelmezési szabályok", "",
        "- A Forthcoming, Open és Closed címkék az EU Funding & Tenders Portal státuszkódjainak feloldásai.",
        "- Az ismeretlen státuszkódokat változatlanul mutatjuk; nem találgatunk.",
        "- Az adatforrásból eltűnt rekordot nem minősítjük automatikusan lezártnak.",
        "- Ez a digest belső ellenőrzési segédlet, nem ügyfélnek küldött értesítés.", "",
    ])
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/opportunity-changes.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/opportunity-change-digest.md"))
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Change log must be a JSON object")
    digest = build_digest(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(digest, encoding="utf-8")
    print(f"Change digest written: {args.output}")

if __name__ == "__main__":
    main()
