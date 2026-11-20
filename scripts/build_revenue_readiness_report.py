#!/usr/bin/env python3
"""Generate a conservative revenue-readiness report without exposing financial data."""
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "Product definition": "docs/organizational-pilot-spec.md",
    "Sample deliverable": "docs/sample-organization-report-2026-11-20.md",
    "Pilot execution checklist": "docs/organizational-pilot-execution-checklist.md",
    "Prospect interview guide": "docs/prospect-interview-guides.md",
    "Payment and payout safeguards": "docs/payment-and-owner-payout-readiness.md",
    "Commercial pilot terms": "docs/first-paid-report-pilot.md",
}
BLOCKERS = [
    "Nincs igazolt fizető ügyfél vagy beérkezett bevétel.",
    "Nincs aktív fizetési szolgáltató, számlázás vagy tulajdonosi kifizetési folyamat.",
    "A GitHub Pages jelenlegi tárhelye nem tekinthető jóváhagyott kereskedelmi SaaS-üzemeltetési alapnak; értékesítés előtt tárhelyellenőrzés/migráció kell.",
    "Ügyfél- és partnermegkeresés csak tulajdonosi jóváhagyás után küldhető.",
]

def build_report(now=None, root=ROOT):
    now = now or datetime.now(timezone.utc)
    lines = [
        "# Bevételi készenléti ellenőrzés",
        "",
        f"Generálva (UTC): {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "Ez belső működési ellenőrzés, nem pénzügyi kimutatás és nem bizonyíték bevételre.",
        "",
        "## Termékeszközök ellenőrzése",
    ]
    for label, relative in REQUIRED.items():
        state = "RENDELKEZÉSRE ÁLL" if (root / relative).is_file() else "HIÁNYZIK"
        lines.append(f"- [{state}] {label}: `{relative}`")
    lines += ["", "## Nyitott üzleti és jogi kapuk"]
    lines += [f"- [NYITOTT] {item}" for item in BLOCKERS]
    lines += [
        "",
        "## Automatizálható következő lépések",
        "- Friss hivatalos forrásadatokból szervezeti riport előállítása.",
        "- Riportminőség és forrásfrissesség automatikus ellenőrzése.",
        "- Célpontlista és személyre szabott bemutatóanyag előkészítése, kiküldés nélkül.",
        "- Minden futás eredményének és hibájának naplózása.",
        "",
        "## Tulajdonosi jóváhagyást igényel",
        "- Külső megkeresés, ajánlat, szerződés vagy reklám.",
        "- Fizetési szolgáltató, számlázás, tárhelyváltás és bármilyen költség.",
        "- Ügyfélpénz fogadása és a tulajdonosi kifizetés beállítása.",
        "",
        "## Nyereségszámítás elve",
        "Nyereség = ténylegesen beérkezett, visszatérítésekkel korrigált bevétel "
        "- szolgáltatói díjak - működési költségek - adótartalék.",
        "A jelentés nem kér és nem tárol bankszámla-, kártya- vagy belépési adatot.",
        "",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    print(build_report())
