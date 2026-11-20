#!/usr/bin/env python3
"""Turn the offline beta data-quality audit into a safe, prioritized review queue."""
from __future__ import annotations

import json
from pathlib import Path

from check_beta_data_quality import DATA, audit


def recommendations(report: dict) -> list[dict]:
    """Create deterministic human-review tasks; never change source data."""
    tasks = []
    def add(priority, key, title, detail, count=1):
        if count:
            tasks.append({"priority": priority, "key": key, "title": title,
                          "count": int(count), "detail": detail,
                          "action": "Kézi ellenőrzés; az eredeti rekordot csak igazolt forrás alapján módosítsd."})

    errors = report.get("feed_errors", [])
    add("P0", "feed_errors", "Adatfolyam-hibák javítása",
        "Ellenőrizd a hiányzó, hibás JSON- vagy szerkezetileg érvénytelen feedfájlokat.", len(errors))
    add("P1", "invalid_urls", "Nem megfelelő forrás-URL-ek ellenőrzése",
        "Csak hivatalos, HTTPS-forrásra mutató linket fogadj el.", report.get("invalid_urls", 0))
    add("P1", "missing_urls", "Hiányzó forráshivatkozások pótlása",
        "A rekordot ne tekintsd ellenőrzöttnek hivatalos forrás nélkül.", report.get("missing_urls", 0))
    add("P1", "duplicate_ids", "Duplikált rekordazonosítók felülvizsgálata",
        "Hasonlítsd össze a rekordokat; automatikus törlés nem történik.", report.get("duplicate_ids", 0))
    add("P1", "missing_titles", "Cím nélküli rekordok kiegészítése",
        "A címet az eredeti hivatalos forrásból vedd át.", report.get("missing_titles", 0))
    add("P2", "overdue_deadlines", "Lejárt határidők státuszának ellenőrzése",
        "A lejárt dátum önmagában nem bizonyítja a program lezárását.", report.get("overdue_deadlines", 0))
    add("P2", "stale_feeds", "Elavult adatfolyamok frissítése",
        "A 72 óránál régebbi ellenőrzés újraellenőrzést igényel.", report.get("stale_feeds", 0))
    if not tasks:
        add("P3", "manual_sample", "Mintavételes kézi ellenőrzés",
            "Végezz mintavételes ellenőrzést a hivatalos források és rekordok között.")
    return tasks


def render_markdown(report: dict) -> str:
    tasks = recommendations(report)
    lines = [
        "# Béta adatminőségi javítási teendősor", "",
        f"- Ellenőrzött adatfolyamok: {report.get('feeds_checked', 0)}",
        f"- Ellenőrzött rekordok: {report.get('records_checked', 0)}",
        f"- Figyelmeztetések: {len(report.get('warnings', []))}",
        f"- Feedhibák: {len(report.get('feed_errors', []))}", "",
        "Ez a lista javaslatokat készít. Nem módosít, nem töröl, nem publikál és nem keres meg külső felet.", "",
        "## Prioritás szerinti teendők", ""
    ]
    for task in tasks:
        lines += [f"### {task['priority']} – {task['title']}",
                  f"- Érintett esetek: {task['count']}",
                  f"- Teendő: {task['detail']}",
                  f"- Biztonság: {task['action']}", ""]
    lines += ["## Forrásfigyelmeztetések", ""]
    warnings = report.get("warnings", [])
    lines.extend([f"- {warning}" for warning in warnings] or ["- Nincs rögzített figyelmeztetés."])
    lines += ["", "## Feedhibák", ""]
    lines.extend([f"- {error}" for error in report.get("feed_errors", [])] or ["- Nincs rögzített feedhiba."])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(render_markdown(audit(DATA)))
