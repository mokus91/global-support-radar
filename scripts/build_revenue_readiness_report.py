#!/usr/bin/env python3
"""Generate a conservative revenue-readiness report without exposing financial data."""
import json
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
PIPELINE_PATH = "data/revenue-pipeline.json"
PIPELINE_STATUSES = {"researched", "outreach_approved", "contacted", "replied", "pilot", "paid_customer"}

def summarize_pipeline(root=ROOT):
    """Count verified pipeline states and reject contradictory records."""
    path = root / PIPELINE_PATH
    if not path.is_file():
        return {"state": "MISSING", "counts": {}, "revenue_huf": 0, "errors": ["A bevételi pipeline fájl hiányzik."]}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload["records"]
        if not isinstance(records, list):
            raise ValueError("A records mezőnek listának kell lennie.")
        ids = [item["id"] for item in records]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplikált pipeline azonosító.")
        counts = {status: 0 for status in PIPELINE_STATUSES}
        revenue, errors = 0, []
        for item in records:
            status = item.get("status")
            if status not in PIPELINE_STATUSES:
                errors.append(f"Ismeretlen státusz: {item.get('id', 'ismeretlen')}")
                continue
            counts[status] += 1
            if item.get("contacted") and not item.get("outreach_approved"):
                errors.append(f"Jóváhagyás nélküli kapcsolatfelvétel jelölve: {item['id']}")
            if item.get("reply_received") and not item.get("contacted"):
                errors.append(f"Kapcsolatfelvétel nélküli válasz jelölve: {item['id']}")
            if item.get("paid_customer") and not item.get("pilot"):
                errors.append(f"Pilot nélküli fizető ügyfél jelölve: {item['id']}")
            flags = {
                "outreach_approved": bool(item.get("outreach_approved")),
                "contacted": bool(item.get("contacted")),
                "replied": bool(item.get("reply_received")),
                "pilot": bool(item.get("pilot")),
                "paid_customer": bool(item.get("paid_customer")),
            }
            expected = {
                "researched": (False, False, False, False, False),
                "outreach_approved": (True, False, False, False, False),
                "contacted": (True, True, False, False, False),
                "replied": (True, True, True, False, False),
                "pilot": (True, True, True, True, False),
                "paid_customer": (True, True, True, True, True),
            }[status]
            actual = tuple(flags[key] for key in ("outreach_approved", "contacted", "replied", "pilot", "paid_customer"))
            if actual != expected:
                errors.append(f"Státusz és eseményjelölők ellentmondanak: {item['id']} ({status})")
            amount = item.get("revenue_huf", 0)
            if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
                errors.append(f"Hibás bevételi összeg: {item['id']}")
            elif status == "paid_customer":
                if amount <= 0:
                    errors.append(f"Fizető ügyfélhez pozitív, igazolt bevétel szükséges: {item['id']}")
                else:
                    revenue += amount
            elif amount:
                errors.append(f"Nem fizető ügyfélhez rögzített bevétel: {item['id']}")
        return {"state": "ERROR" if errors else "OK", "counts": counts, "revenue_huf": revenue, "errors": errors}
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return {"state": "ERROR", "counts": {}, "revenue_huf": 0, "errors": [f"Nem feldolgozható pipeline: {exc}"]}

def build_report(now=None, root=ROOT):
    now = now or datetime.now(timezone.utc)
    lines = [
        "# Bevételi készenléti ellenőrzés", "",
        f"Generálva (UTC): {now.strftime('%Y-%m-%d %H:%M')}", "",
        "Ez belső működési ellenőrzés, nem pénzügyi kimutatás és nem bizonyíték bevételre.", "",
        "## Termékeszközök ellenőrzése",
    ]
    for label, relative in REQUIRED.items():
        state = "RENDELKEZÉSRE ÁLL" if (root / relative).is_file() else "HIÁNYZIK"
        lines.append(f"- [{state}] {label}: `{relative}`")
    pipe = summarize_pipeline(root)
    c = pipe["counts"]
    lines += ["", "## Értékesítési pipeline – konzervatív nyilvántartás",
        f"- Pipeline állapot: **{pipe['state']}**",
        f"- Kutatott célpont: {c.get('researched', 0)}",
        f"- Jóváhagyott kapcsolatfelvétel: {c.get('outreach_approved', 0)}",
        f"- Kapcsolatfelvétel megtörtént: {c.get('contacted', 0)}",
        f"- Válasz érkezett: {c.get('replied', 0)}",
        f"- Pilot: {c.get('pilot', 0)}",
        f"- Fizető ügyfél: {c.get('paid_customer', 0)}",
        f"- Pipeline-ban nyilvántartott bevétel: {pipe['revenue_huf']} Ft"]
    lines += [f"- [ELLENŐRZÉSI HIBA] {e}" for e in pipe["errors"]]
    lines += ["", "## Nyitott üzleti és jogi kapuk"] + [f"- [NYITOTT] {x}" for x in BLOCKERS]
    lines += ["", "## Automatizálható következő lépések",
        "- Friss hivatalos forrásadatokból szervezeti riport előállítása.",
        "- Riportminőség és forrásfrissesség automatikus ellenőrzése.",
        "- Célpontlista és személyre szabott bemutatóanyag előkészítése, kiküldés nélkül.",
        "- Minden futás eredményének és hibájának naplózása.", "",
        "## Tulajdonosi jóváhagyást igényel",
        "- Külső megkeresés, ajánlat, szerződés vagy reklám.",
        "- Fizetési szolgáltató, számlázás, tárhelyváltás és bármilyen költség.",
        "- Ügyfélpénz fogadása és a tulajdonosi kifizetés beállítása.", "",
        "## Nyereségszámítás elve",
        "Nyereség = ténylegesen beérkezett, visszatérítésekkel korrigált bevétel - szolgáltatói díjak - működési költségek - adótartalék.",
        "A jelentés nem kér és nem tárol bankszámla-, kártya- vagy belépési adat.", ""]
    return "\n".join(lines)

if __name__ == "__main__":
    print(build_report())
