#!/usr/bin/env python3
"""Generate a conservative, evidence-based improvement backlog from current project reports.

This script proposes work only. It never edits application code, source records,
workflow permissions, secrets, or deployment settings.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str) -> dict:
    path = DATA / name
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def main() -> None:
    quality = load("quality-report.json")
    manifest = load("feed-status.json")
    tiers = quality.get("application_state_tiers") or {}
    health = quality.get("feed_health_summary") or manifest.get("feeds") or []
    tasks: list[tuple[str, str, str]] = []

    if int(tiers.get("needs_verification", 0) or 0) > 0:
        tasks.append((
            "Magas prioritás — pályázati feltételek ellenőrzése",
            f"{tiers.get('needs_verification')} rekord további ellenőrzést igényel.",
            "Az eredeti hivatalos oldalról külön ellenőrizni a nyitottságot, jogosultságot, összeget és határidőt; csak bizonyítékkal módosítani a státuszt."
        ))
    unavailable = [f for f in health if f.get("status") == "temporarily-unavailable"]
    for feed in unavailable:
        tasks.append((
            f"Adatforrás-helyreállítás — {feed.get('name', feed.get('file', 'ismeretlen forrás'))}",
            f"Technikai állapot: átmenetileg nem elérhető; HTTP {feed.get('http_status')}.",
            "Ellenőrizni az API-hozzáférést, hitelesítési követelményeket és a hivatalos alternatív feedet. Üres adatként ne kezeljük."
        ))
    stale = [f for f in health if f.get("freshness") == "stale"]
    for feed in stale:
        tasks.append((
            f"Adatfrissítés — {feed.get('name', feed.get('file', 'ismeretlen forrás'))}",
            "A forrás frissességi jelzése elavult.",
            "A lekérési folyamat és az időbélyegek ellenőrzése."
        ))
    if int(quality.get("missing_urls", 0) or 0) or int(quality.get("invalid_urls", 0) or 0):
        tasks.append((
            "Hivatkozások javítása",
            f"Hiányzó URL: {quality.get('missing_urls', 0)}; hibás URL: {quality.get('invalid_urls', 0)}.",
            "Az eredeti közzétevőnél ellenőrizni a hivatkozásokat; találgatott URL-t ne írjunk be."
        ))
    if not tasks:
        tasks.append((
            "Következő fejlesztési kör",
            "A jelenlegi jelentések nem jeleztek automatikus backlog-tételt.",
            "Új hivatalos adatforrások feltérképezése és célzott regressziós tesztek hozzáadása."
        ))

    print("# Global Support Radar — automatikus fejlesztési javaslatok")
    print()
    print("Ez egy mérőszámokból képzett javaslatlista, nem automatikus kódmódosítás.")
    print()
    print(f"- Vizsgált rekordok: {quality.get('records_checked', 'n/a')}")
    print(f"- Igazoltan nyitott: {tiers.get('verified_open', 'n/a')}")
    print(f"- További ellenőrzést igényel: {tiers.get('needs_verification', 'n/a')}")
    print(f"- Adatforrások: {quality.get('feeds_checked', 'n/a')}")
    print()
    for index, (title, evidence, action) in enumerate(tasks, 1):
        print(f"## {index}. {title}")
        print(f"- Bizonyíték: {evidence}")
        print(f"- Javasolt lépés: {action}")
        print()
    print("## Kötelező biztonsági korlátok")
    print("- A program nem írhatja át önállóan a saját forráskódját vagy a kiadott adatokat.")
    print("- Minden kódmódosítás külön tesztelendő, felülvizsgálandó és visszaállítható.")
    print("- Nem kerülhet titok, személyes adat vagy jogosultságmódosítás automatikus folyamatba.")
    print("- Nyitott támogatást csak hivatalos, ellenőrizhető bizonyíték alapján szabad jelezni.")


if __name__ == "__main__":
    main()
