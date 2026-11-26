#!/usr/bin/env python3
"""Build Hungarian support SEO pages from curated official-source records.

This publishes official information starting points, not a claim that a
benefit is currently open or that a visitor is eligible.
"""
from __future__ import annotations
import datetime as dt
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hu-household-support.json"
OUT = ROOT / "countries" / "hu" / "programmes"
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://mokus91.github.io/global-support-radar/"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

CATEGORY = {
    "family": "Családtámogatás",
    "housing": "Lakhatás",
    "social": "Szociális támogatás",
    "energy": "Energia",
    "business": "Vállalkozás",
    "agriculture": "Mezőgazdaság",
    "education": "Oktatás",
    "employment": "Foglalkoztatás",
    "healthcare": "Egészségügy",
    "transport": "Közlekedés",
}

def esc(v):
    return html.escape(str(v or ""), quote=True)

def slug(v):
    s = str(v or "")
    return s if re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,90}", s) else None

def valid_url(v):
    if not isinstance(v, str):
        return None
    p = urlparse(v)
    return v if p.scheme == "https" and p.netloc and not p.username and not p.password else None

def render_record(r, updated):
    rid = slug(r.get("id"))
    title = r.get("title_hu") or "Állami támogatás"
    url = valid_url(r.get("url"))
    if not url:
        url = "https://www.allamkincstar.gov.hu/"
    category = CATEGORY.get(str(r.get("category") or "").lower(), "Állami támogatás")
    summary = r.get("summary_hu") or "A támogatás részletes feltételeit a hivatalos forrás tartalmazza."
    beneficiary = r.get("beneficiary_hu") or "A jogosultságot az adott ellátás hatályos szabályai határozzák meg."
    publisher = r.get("publisher") or "Hivatalos magyar állami tájékoztató"
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "inLanguage": "hu-HU",
        "url": BASE + "countries/hu/programmes/" + rid + "/",
        "dateModified": updated,
        "isPartOf": {"@type": "WebSite", "name": "Global Support Radar", "url": BASE},
        "about": {"@type": "GovernmentService", "name": title, "serviceUrl": url,
                  "provider": {"@type": "GovernmentOrganization", "name": publisher}}
    }
    return f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow,max-image-preview:large">
<title>{esc(title)} – feltételek és igénylés | Global Support Radar</title>
<meta name="description" content="{esc(title)}: hivatalos magyar tájékoztató, jogosulti kör és ügyintézési kiindulópont. Ellenőrizd az aktuális feltételeket az állami forrásnál.">
<link rel="canonical" href="{BASE}countries/hu/programmes/{esc(rid)}/">
<meta property="og:type" content="article"><meta property="og:site_name" content="Global Support Radar">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(summary)}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7022315203746196" crossorigin="anonymous"></script>
<style>
:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.75 system-ui,sans-serif}}
main{{max-width:900px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;text-decoration:none;color:var(--text)}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:20px;margin:18px 0}}
h1{{font-size:clamp(27px,5vw,42px);line-height:1.3}}.muted{{color:var(--muted)}}.badge{{display:inline-block;border-radius:20px;background:#3b3420;color:#ffe2a5;padding:4px 10px;font-size:13px}}
.button{{display:inline-block;background:var(--mint);color:#08251e;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:800}}
footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}">Magyarország</a> · <a href="{BASE}countries/hu/programmes/">Támogatások listája</a></header>
<p class="muted">Magyar állami támogatások és ellátások · {esc(category)}</p>
<h1>{esc(title)}</h1><p><span class="badge">Hivatalos tájékoztató – egyedi jogosultság-ellenőrzés szükséges</span></p>
<section class="panel"><h2>Miről szól?</h2><p>{esc(summary)}</p><h3>Kinek szólhat?</h3><p>{esc(beneficiary)}</p>
<p><strong>Tájékoztató forrás:</strong> {esc(publisher)}</p>
<a class="button" href="{esc(url)}" target="_blank" rel="noopener noreferrer">Hivatalos feltételek és ügyintézés megnyitása ↗</a></section>
<section class="panel"><h2>Igénylés előtt ellenőrizd</h2>
<ol><li>A hivatalos oldalon ellenőrizd, hogy az ellátás jelenleg igényelhető-e, és milyen határidő vonatkozik rád.</li>
<li>Ellenőrizd a személyi, lakóhelyi, családi, jövedelmi vagy egyéb jogosultsági feltételeket – csak az adott programra vonatkozókat.</li>
<li>Nézd meg az aktuális kéreleműrlapot, a csatolandó igazolásokat és a benyújtás módját.</li>
<li>A kérelmet a hivatalos ügyintézési csatornán add be; a Radar nem vesz át kérelmet és nem dönt jogosultságról.</li></ol>
<p><a href="https://www.kormanyhivatalok.hu/csaladtamogatasok" target="_blank" rel="noopener noreferrer">Kormányhivatalok – családtámogatási ügyintézés</a></p></section>
<p class="muted">A nyilvántartás utolsó újraépítése: {esc(updated)}. A forrásoldal az irányadó, nem ez az összefoglaló.</p>
<footer><a href="{BASE}countries/hu/programmes/">Vissza a magyar támogatásokhoz</a> · <a href="{BASE}methodology.html">Adatminőségi módszertan</a> · <a href="{BASE}privacy.html">Adatvédelem</a>
<p>A Global Support Radar független tájékoztató oldal, nem állami szerv. Nem garantál jogosultságot, támogatási összeget vagy kifizetést.</p></footer>
</main></body></html>"""

def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    updated = dt.datetime.now(dt.timezone.utc).date().isoformat()
    records = [r for r in payload.get("records", []) if isinstance(r, dict) and slug(r.get("id")) and r.get("title_hu")]
    OUT.mkdir(parents=True, exist_ok=True)
    cards, urls = [], []
    for r in records:
        rid = slug(r["id"])
        target = OUT / rid / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_record(r, updated), encoding="utf-8")
        page_url = BASE + "countries/hu/programmes/" + rid + "/"
        urls.append(page_url)
        cards.append(f'<li><a href="./{esc(rid)}/">{esc(r.get("title_hu"))}</a><br><small>{esc(CATEGORY.get(str(r.get("category") or "").lower(), "Állami támogatás"))} · {esc(r.get("publisher") or "Hivatalos forrás")}</small></li>')

    grouped = {}
    for r in records:
        grouped.setdefault(CATEGORY.get(str(r.get("category") or "").lower(), "Egyéb támogatás"), []).append(r)
    groups = []
    for name, rows in sorted(grouped.items()):
        groups.append("<h2>" + esc(name) + "</h2><ul>" + "".join(
            f'<li><a href="./{esc(slug(r["id"]))}/">{esc(r.get("title_hu"))}</a></li>' for r in rows
        ) + "</ul>")
    index = f"""<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow"><title>Magyar állami támogatások, családi pótlék és pályázatok | Global Support Radar</title>
<meta name="description" content="Magyarország állami családtámogatásai, családi pótlék, GYES, GYET, lakástámogatás és szociális ellátások hivatalos forrásokkal és igénylési útmutatóval.">
<link rel="canonical" href="{BASE}countries/hu/programmes/">
<meta property="og:title" content="Magyar állami támogatások és ellátások"><meta property="og:description" content="Családi pótlék, GYES, GYET, anyasági támogatás, lakástámogatás és további hivatalos lehetőségek.">
<style>body{{margin:0;background:#0b1220;color:#eef4ff;font:16px/1.7 system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:24px 18px}}a{{color:#64e2b8}}li{{padding:10px;border-bottom:1px solid #31435e}}small,.muted{{color:#b2c1d5}}.panel{{background:#142238;border:1px solid #31435e;border-radius:14px;padding:18px;margin:18px 0}}</style></head><body><main>
<a href="{BASE}">Global Support Radar főoldal</a> · <a href="{BASE}countries/hu/">Magyarország országoldal</a>
<h1>Magyar állami támogatások és ellátások</h1>
<p>Hivatalos tájékoztatók családi pótlék, anyasági támogatás, GYES, GYET, lakástámogatás, energia- és szociális segítség kereséséhez.</p>
<section class="panel"><h2>Hogyan használd?</h2><p>Válaszd ki a támogatást, olvasd el a jogosulti feltételeket, majd a hivatalos állami oldalon ellenőrizd az aktuális összeget, határidőt, szükséges iratokat és a benyújtás módját.</p>
<p><a href="https://www.kormanyhivatalok.hu/csaladtamogatasok" target="_blank" rel="noopener noreferrer">Családtámogatási ügyintézés a kormányhivataloknál</a> · <a href="https://www.kormanyhivatalok.hu/lakastamogatas" target="_blank" rel="noopener noreferrer">Lakástámogatási tájékoztató</a></p></section>
{''.join(groups)}
<p class="muted">Adatfrissítés: {updated}. Ez hivatalos forrásokra mutató tájékoztató jegyzék, nem jogosultsági döntés és nem teljes körű állami nyilvántartás.</p>
<footer><a href="{BASE}methodology.html">Adatminőségi módszertan</a> · <a href="{BASE}privacy.html">Adatvédelem</a></footer>
</main></body></html>"""
    (OUT / "index.html").write_text(index, encoding="utf-8")

    # Add a visible route to the programme directory on the generated HU country page.
    country_page = ROOT / "countries" / "hu" / "index.html"
    if country_page.exists():
        text = country_page.read_text(encoding="utf-8")
        marker = "GSR_HU_PROGRAMME_DIRECTORY"
        if marker not in text:
            block = f'<section class="notice"><h2>Magyar állami támogatások és ellátások</h2><p>Családi pótlék, anyasági támogatás, GYES, GYET, lakhatási és szociális támogatások hivatalos forrásokkal.</p><p><a href="./programmes/">Magyar támogatások és igénylési útmutatók megnyitása →</a></p></section>\n'
            text = text.replace("</main>", block + "<!-- " + marker + " -->\n</main>")
            country_page.write_text(text, encoding="utf-8")

    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    existing = {n.find(f"{{{NS}}}loc").text for n in root.findall(f"{{{NS}}}url") if n.find(f"{{{NS}}}loc") is not None}
    for url in [BASE + "countries/hu/programmes/"] + urls:
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(node, f"{{{NS}}}loc").text = url
        ET.SubElement(node, f"{{{NS}}}lastmod").text = updated
    tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)
    print(f"Built {len(records)} Hungarian official-information pages and updated sitemap.")

if __name__ == "__main__":
    main()
