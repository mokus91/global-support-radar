#!/usr/bin/env python3
"""Read-only weekly availability check for curated revenue and infrastructure sources."""
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "revenue-opportunities.json"
TIMEOUT = 15
UA = "GlobalSupportRadar-LinkMonitor/1.0 (+https://mokus91.github.io/global-support-radar/)"

def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-1023"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return {"status": response.status, "final_url": response.geturl(), "state": "reachable"}
    except urllib.error.HTTPError as exc:
        # Authentication/anti-bot/forbidden responses do not prove a dead page.
        state = "reachable_restricted" if exc.code in (401, 403, 429) else "http_error"
        return {"status": exc.code, "final_url": exc.geturl(), "state": state}
    except Exception as exc:
        return {"status": None, "final_url": url, "state": "check_failed", "detail": str(exc)[:180]}

def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    lines = [
        "# Global Support Radar – bevételi és költségmentes forrásfigyelő",
        "",
        f"Futtatás ideje (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "Ez a jelentés csak a megadott hivatalos oldalak HTTP-elérhetőségét vizsgálja. Nem ellenőrzi a programok elfogadási feltételeit, nem jelent partnerjóváhagyást és nem ígér bevételt.",
        "",
        "| Lehetőség | Állapot | HTTP | Ellenőrzött oldal |",
        "|---|---|---:|---|",
    ]
    failures = 0
    for item in data.get("opportunities", []):
        result = check(item["check_url"])
        if result["state"] in ("http_error", "check_failed"):
            failures += 1
        status = result["state"]
        http = result["status"] if result["status"] is not None else "—"
        url = result["final_url"].replace("|", "%7C")
        lines.append(f"| {item['name']} | {status} | {http} | {url} |")
    lines += [
        "",
        f"Vizsgált források: {len(data.get('opportunities', []))}",
        f"HTTP-hiba vagy ellenőrzési hiba: {failures}",
        "",
        "## Költségvédelmi szabály",
        "- Nincs fizetős API, előfizetés, reklámvásárlás vagy automatikus megrendelés.",
        "- A linkfigyelés nem tölt le teljes weboldalakat, nem küld űrlapot és nem lép be fiókba.",
        "- Egy 403/429 válasz korlátozás lehet, nem bizonyítja, hogy az oldal megszűnt.",
        "- Bevételi lehetőség csak tulajdonosi ellenőrzés és jóváhagyás után aktiválható.",
        "",
    ]
    report = "\n".join(lines)
    out = ROOT / "revenue-opportunity-watch.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    # HTTP errors are reported but do not fail the whole monitor: some sites block bots.
    return 0

if __name__ == "__main__":
    sys.exit(main())
