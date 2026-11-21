#!/usr/bin/env python3
"""Build country landing pages and sitemap from the latest official-source indexes.

All discovered records remain leads unless their source explicitly verifies them.
The generator never labels a portal lead as an open grant.
"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COUNTRIES = ROOT / "countries"
BASE_URL = "https://mokus91.github.io/"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

CATEGORY_LABELS = {
    "all": "Általános támogatások és közszolgáltatások",
    "agriculture": "Mezőgazdaság",
    "business": "Vállalkozás",
    "education": "Oktatás",
    "employment": "Foglalkoztatás",
    "energy": "Energia",
    "family": "Család",
    "healthcare": "Egészségügy",
    "housing": "Lakhatás",
    "social": "Szociális támogatások",
    "transport": "Közlekedés",
    "other": "Egyéb",
}

def load_records(filename: str) -> list[dict]:
    path = DATA / filename
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("records", [])
    return [row for row in rows if isinstance(row, dict)]

def safe_url(value: object) -> str | None:
    value = str(value or "").strip()
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        return None
    return value

def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)

def render_page(code: str, country: str, portal: dict | None, sources: list[dict], generated: str) -> str:
    items = []
    for row in sorted(sources, key=lambda x: (str(x.get("category", "other")), str(x.get("name_hu") or x.get("name_en") or ""))):
        url = safe_url(row.get("url") or row.get("official_url"))
        if not url:
            continue
        title = row.get("name_hu") or row.get("name_en") or row.get("title") or "Hivatalos információs oldal"
        description = row.get("description_hu") or row.get("description_en") or row.get("description") or ""
        category = CATEGORY_LABELS.get(str(row.get("category") or "other"), "Egyéb")
        verification = str(row.get("verification_status") or row.get("status") or "Ellenőrzendő")
        items.append(
            '<article class="source"><div class="tag">' + esc(category) + '</div>'
            '<h2><a rel="noopener noreferrer" target="_blank" href="' + esc(url) + '">' + esc(title) + '</a></h2>'
            '<p>' + esc(description) + '</p><small>Forrásjelölés: ' + esc(verification) + '</small></article>'
        )
    portal_html = ""
    if portal:
        url = safe_url(portal.get("url"))
        if url:
            portal_html = (
                '<section class="notice"><h2>Nemzeti kormányzati portál</h2>'
                '<p>Ez a hivatkozás egy korábbi nemzetközi portáljegyzékből származó kiindulópont. '
                'A forrásjegyzék 2013-as ellenőrzési időszakot jelez; a cím és a támogatási tartalom jelenlegi működése nincs igazolva.</p>'
                '<p><a rel="noopener noreferrer" target="_blank" href="' + esc(url) + '">Kormányzati portál megnyitása</a></p>'
                '<small>Állapot: történeti címtáradat, jelenleg nem ellenőrzött.</small></section>'
            )
    body = "\n".join(items) if items else '<p>Ehhez az országhoz jelenleg nincs külön indexelt, hivatalos támogatási forrás. A nemzeti portál kiindulópontként használható, ha elérhető.</p>'
    return f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(country)} – hivatalos támogatási források | Global Support Radar</title>
<meta name="description" content="{esc(country)} hivatalos állami támogatási, ellátási és finanszírozási forrásainak országoldala. Ellenőrizd az eredeti kiírásokat.">
<link rel="canonical" href="{BASE_URL}countries/{code.lower()}/">
<style>
:root{{color-scheme:light dark}}*{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 system-ui,sans-serif;background:#101827;color:#edf3fb}}
main{{max-width:900px;margin:auto;padding:28px 18px}}a{{color:#77c8ff}}.back{{display:inline-block;margin-bottom:20px}}
h1{{font-size:clamp(2rem,6vw,3rem);line-height:1.15}}.muted{{color:#bdc9d8}}.notice,.source{{background:#1b293c;border:1px solid #34445a;border-radius:14px;padding:18px;margin:18px 0}}
.tag{{display:inline-block;background:#294b68;border-radius:20px;padding:3px 10px;font-size:.8rem}}small{{color:#bdc9d8}}footer{{margin-top:34px;border-top:1px solid #34445a;padding-top:16px}}
</style></head><body><main>
<a class="back" href="../">← Országok áttekintése</a>
<h1>{esc(country)}</h1><p class="muted">Országkód: {esc(code)} · Automatikusan összeállított forrásjegyzék · Frissítve: {esc(generated)}</p>
<p>Az oldal hivatalos állami forrásokhoz vezető hivatkozásokat gyűjt. A felsorolt oldalak nem jelentenek automatikusan nyitott pályázatot, támogatási jogosultságot vagy garantált kifizetést. Mindig az eredeti kiírás az irányadó.</p>
{portal_html}
<section><h2>Országspecifikus források</h2>{body}</section>
<footer><p><a href="{BASE_URL}">Global Support Radar főoldal</a> · <a href="{BASE_URL}methodology.html">Adatminőségi módszertan</a> · <a href="{BASE_URL}free-policy.html">Ingyenes használat</a></p>
<p class="muted">A felfedezett hivatkozásokat rendszeresen újraépítjük. A gépi forrásfelderítés nem helyettesíti az egyedi hivatalos ellenőrzést.</p></footer>
</main></body></html>
"""

def main() -> None:
    portals = load_records("un-national-portals.json")
    official_sources = load_records("worldwide-national-support-sources.json")
    # Some feeds include country-specific official links beyond the curated directory.
    for filename in ("eu-national-agriculture-discovery.json", "eu-national-category-discovery.json"):
        official_sources.extend(load_records(filename))

    countries: dict[str, dict] = {}
    for row in portals:
        code = str(row.get("country_code") or "").upper()
        if re.fullmatch(r"[A-Z]{2}", code):
            countries.setdefault(code, {"name": row.get("country_en") or code, "portal": row, "sources": []})
            if not countries[code].get("portal"):
                countries[code]["portal"] = row
    for row in official_sources:
        code = str(row.get("country_code") or "").upper()
        if not re.fullmatch(r"[A-Z]{2}", code):
            continue
        entry = countries.setdefault(code, {"name": row.get("country_en") or code, "portal": None, "sources": []})
        entry["name"] = entry.get("name") or row.get("country_en") or code
        entry["sources"].append(row)

    generated = datetime.now(timezone.utc).date().isoformat()
    urls = set()
    for code, entry in sorted(countries.items()):
        target = COUNTRIES / code.lower() / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(code, str(entry["name"]), entry.get("portal"), entry["sources"], generated), encoding="utf-8")
        urls.add(f"{BASE_URL}countries/{code.lower()}/")

    sitemap_path = ROOT / "sitemap.xml"
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    existing = {node.find(f"{{{NS}}}loc").text for node in root.findall(f"{{{NS}}}url") if node.find(f"{{{NS}}}loc") is not None}
    for url in sorted(urls):
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(node, f"{{{NS}}}loc").text = url
        ET.SubElement(node, f"{{{NS}}}lastmod").text = generated
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    print(f"Generated {len(countries)} country landing pages and indexed {len(urls)} URLs.")

if __name__ == "__main__":
    main()
