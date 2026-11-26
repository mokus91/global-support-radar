#!/usr/bin/env python3
"""Build a German-language index of official German public support portals.

Portal records are information starting points, not proof that a grant is open.
"""
from __future__ import annotations
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "worldwide-national-support-sources.json"
OUT = ROOT / "countries" / "de" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://mokus91.github.io/global-support-radar/"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
LABELS = {
 "all":"Allgemeine Förderprogramme",
 "family":"Familie und Kinder",
 "housing":"Wohnen und Bauen",
 "social":"Soziale Unterstützung",
 "energy":"Energie und Klimaschutz",
 "business":"Unternehmen und Gründung",
 "agriculture":"Landwirtschaft und ländliche Räume",
 "education":"Bildung und Forschung",
 "employment":"Arbeit und Beschäftigung",
 "healthcare":"Gesundheit",
 "transport":"Verkehr",
}
def esc(v): return html.escape(str(v or ""), quote=True)
def safe_url(v):
 p=urlparse(str(v or ""))
 return str(v) if p.scheme=="https" and p.netloc and not p.username and not p.password else None

def main():
 payload=json.loads(DATA.read_text(encoding="utf-8"))
 rows=[r for r in payload.get("records",[]) if r.get("country_code")=="DE" and safe_url(r.get("url"))]
 groups={}
 for r in rows:
  groups.setdefault(r.get("category","all"),[]).append(r)
 sections=[]
 for key,items in sorted(groups.items(),key=lambda x: LABELS.get(x[0],x[0])):
  cards=[]
  for r in sorted(items,key=lambda x:x.get("name_de") or x.get("name_en") or ""):
   title=r.get("name_de") or r.get("name_en") or "Offizielle Informationsseite"
   desc=r.get("description_de") or r.get("description_en") or "Offizielle Informationen und Hinweise zum jeweiligen Förderbereich."
   cards.append(f'<article class="card"><h3><a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a></h3><p>{esc(desc)}</p><small>Herausgeber: {esc(r.get("publisher","Offizielle Stelle"))} · Quellenstatus: {esc(r.get("verification_status","zu prüfen"))}</small></article>')
  sections.append(f'<section><h2>{esc(LABELS.get(key,"Weitere Förderbereiche"))}</h2>{"".join(cards)}</section>')
 today=datetime.now(timezone.utc).date().isoformat()
 page=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Staatliche Förderungen in Deutschland: Zuschüsse, Familienleistungen und Hilfen | Global Support Radar</title>
<meta name="description" content="Offizielle Förderprogramme und staatliche Hilfen in Deutschland finden: Förderdatenbank, Familienleistungen, Wohnen, Energie, Unternehmen, Landwirtschaft und Arbeit.">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{BASE}countries/de/">
<meta property="og:type" content="website"><meta property="og:title" content="Staatliche Förderungen in Deutschland"><meta property="og:description" content="Offizielle deutsche Förder- und Leistungsportale nach Themen geordnet.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Staatliche Förderungen in Deutschland","inLanguage":"de-DE","url":"{BASE}countries/de/","dateModified":"{today}","isPartOf":{{"@type":"WebSite","name":"Global Support Radar","url":"{BASE}"}}}}</script>
<style>
:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;color:var(--text);text-decoration:none}}h1{{font-size:clamp(28px,5vw,44px);line-height:1.2}}.lead,.muted,small{{color:var(--muted)}}.notice,.card{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:18px;margin:16px 0}}.card h3{{margin:0 0 8px}}footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}countries/">Alle Länder</a> · <a href="{BASE}">Startseite</a></header>
<p class="muted">Deutschland · Offizielle Informationsquellen · Aktualisiert: {today}</p>
<h1>Staatliche Förderungen und Sozialleistungen in Deutschland</h1>
<p class="lead">Finde offizielle Anlaufstellen für Zuschüsse, Förderprogramme, Familienleistungen, Wohnen, Energie, Unternehmensförderung, Landwirtschaft und Arbeit.</p>
<div class="notice"><strong>Wichtig:</strong> Diese Seite verlinkt auf staatliche und öffentliche Informationsportale. Ein Eintrag bedeutet nicht, dass ein Programm aktuell geöffnet ist oder dass du anspruchsberechtigt bist. Prüfe Fristen, Förderbedingungen, verfügbare Mittel und den Antrag direkt bei der zuständigen Stelle. Kredite sind nicht dasselbe wie Zuschüsse.</div>
{"".join(sections)}
<p class="muted">Die verlinkten Portale werden als offizielle Recherche-Einstiege geführt. Die Förderdatenbank des Bundes enthält Programme von Bund, Ländern und EU; die Förderzentrale bildet ausgewählte Programme ab und wird schrittweise erweitert.</p>
<footer><a href="{BASE}methodology.html">Methodik und Datenqualität</a> · <a href="{BASE}privacy.html">Datenschutz</a><p>Global Support Radar ist ein unabhängiges Informationsangebot und keine Behörde. Maßgeblich sind ausschließlich die Angaben der zuständigen Förderstelle.</p></footer>
</main></body></html>'''
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(page,encoding="utf-8")
 tree=ET.parse(SITEMAP); root=tree.getroot()
 existing={n.find(f"{{{NS}}}loc").text for n in root.findall(f"{{{NS}}}url") if n.find(f"{{{NS}}}loc") is not None}
 url=BASE+"countries/de/"
 if url not in existing:
  node=ET.SubElement(root,f"{{{NS}}}url"); ET.SubElement(node,f"{{{NS}}}loc").text=url; ET.SubElement(node,f"{{{NS}}}lastmod").text=today
 tree.write(SITEMAP,encoding="utf-8",xml_declaration=True)
 print(f"Built German country page with {len(rows)} official portal links.")

if __name__=="__main__": main()
