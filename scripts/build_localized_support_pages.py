#!/usr/bin/env python3
"""Build localized country support directories from official-source records."""
from __future__ import annotations
import argparse, html, json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"worldwide-national-support-sources.json"
SITEMAP=ROOT/"sitemap.xml"
BASE="https://mokus91.github.io/global-support-radar/"
NS="http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("",NS)
CONFIG={
 "nl":("NL","Nederland","Subsidies, toeslagen en overheidssteun in Nederland","Vind officiële Nederlandse regelingen voor gezinnen, ondernemers, landbouw, werk, sociale zekerheid en energie.","Let op: deze pagina verzamelt officiële informatiebronnen. Een vermelding betekent niet dat een regeling momenteel openstaat of dat u automatisch in aanmerking komt. Controleer voorwaarden, aanvraagtermijnen en budget bij de verantwoordelijke instantie."),
 "pl":("PL","Polska","Dotacje, świadczenia i wsparcie publiczne w Polsce","Oficjalne polskie źródła dotyczące świadczeń rodzinnych, pomocy społecznej, dotacji dla firm, rolnictwa i zatrudnienia.","Uwaga: strona gromadzi oficjalne źródła informacji. Obecność linku nie oznacza, że nabór jest otwarty ani że użytkownik spełnia warunki. Sprawdź kryteria, terminy i dostępność środków w odpowiedniej instytucji."),
 "de":("AT","Österreich","Förderungen, Beihilfen und staatliche Unterstützung in Österreich","Offizielle österreichische Quellen zu Familienleistungen, Sozialhilfe, Unternehmensförderung, Landwirtschaft, Arbeit und Energie.","Hinweis: Diese Seite sammelt offizielle Informationsquellen. Ein Link bedeutet nicht, dass eine Förderung derzeit beantragt werden kann oder dass Sie anspruchsberechtigt sind. Prüfen Sie Voraussetzungen, Fristen und Budget bei der zuständigen Stelle."),
 "sv":("SE","Sverige","Bidrag, ersättningar och offentligt stöd i Sverige","Officiella svenska källor om familjestöd, socialförsäkring, företagsfinansiering, jordbruk, arbete och energi.","Observera: sidan samlar officiella informationskällor. En länk betyder inte att ett stöd är öppet för ansökan eller att du automatiskt har rätt till det. Kontrollera villkor, ansökningstider och budget hos ansvarig myndighet.")
}
LABELS={
 "nl":{"all":"Alle regelingen en financiering","family":"Gezinnen en kinderen","social":"Sociale uitkeringen","housing":"Wonen","energy":"Energie en milieu","business":"Ondernemers en bedrijven","agriculture":"Landbouw en plattelandsontwikkeling","education":"Onderwijs en onderzoek","employment":"Werk en werkgelegenheid","healthcare":"Gezondheid","transport":"Vervoer"},
 "pl":{"all":"Wszystkie dotacje i finansowanie","family":"Rodzina i dzieci","social":"Świadczenia społeczne","housing":"Mieszkanie","energy":"Energia i środowisko","business":"Firmy i przedsiębiorcy","agriculture":"Rolnictwo i rozwój obszarów wiejskich","education":"Edukacja i badania","employment":"Praca i zatrudnienie","healthcare":"Zdrowie","transport":"Transport"},
 "de":{"all":"Alle Förderungen und Finanzierungen","family":"Familie und Kinder","social":"Sozialleistungen","housing":"Wohnen","energy":"Energie und Umwelt","business":"Unternehmen und Gründung","agriculture":"Landwirtschaft und ländliche Entwicklung","education":"Bildung und Forschung","employment":"Arbeit und Beschäftigung","healthcare":"Gesundheit","transport":"Verkehr"},
 "sv":{"all":"Alla stöd och finansieringsmöjligheter","family":"Familj och barn","social":"Socialförsäkring och bidrag","housing":"Boende","energy":"Energi och miljö","business":"Företag och entreprenörer","agriculture":"Jordbruk och landsbygdsutveckling","education":"Utbildning och forskning","employment":"Arbete och sysselsättning","healthcare":"Hälsa","transport":"Transport"}
}
def esc(v): return html.escape(str(v or ""),quote=True)
def safe_url(v):
 p=urlparse(str(v or ""))
 return str(v) if p.scheme=="https" and p.netloc and not p.username and not p.password else None
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("language",choices=CONFIG)
 a=ap.parse_args()
 cc,country,title,description,notice=CONFIG[a.language]
 rows=[r for r in json.loads(DATA.read_text(encoding="utf-8")).get("records",[]) if r.get("country_code")==cc and safe_url(r.get("url"))]
 groups={}
 for r in rows: groups.setdefault(r.get("category","all"),[]).append(r)
 sections=[]
 for key,items in sorted(groups.items(),key=lambda x:LABELS[a.language].get(x[0],x[0])):
  cards=[]
  for r in sorted(items,key=lambda x:x.get("name_"+a.language) or x.get("name_en") or ""):
   name=r.get("name_"+a.language) or r.get("name_en") or "Official public information"
   desc=r.get("description_"+a.language) or r.get("description_en") or "Official information and guidance about available measures."
   cards.append(f'<article class="card"><h3><a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">{esc(name)} ↗</a></h3><p>{esc(desc)}</p><small>Authority: {esc(r.get("publisher","Public authority"))} · Source status: {esc(r.get("verification_status","check required"))}</small></article>')
  sections.append(f'<section><h2>{esc(LABELS[a.language].get(key,"Other support"))}</h2>{"".join(cards)}</section>')
 today=datetime.now(timezone.utc).date().isoformat()
 url=BASE+f"countries/{a.language}/"
 page=f'''<!doctype html><html lang="{a.language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Global Support Radar</title><meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":{json.dumps(title,ensure_ascii=False)},"inLanguage":"{a.language}","url":"{url}","dateModified":"{today}","isPartOf":{{"@type":"WebSite","name":"Global Support Radar","url":"{BASE}"}}}}</script>
<style>:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;color:var(--text);text-decoration:none}}h1{{font-size:clamp(28px,5vw,44px);line-height:1.2}}.lead,small{{color:var(--muted)}}.notice,.card{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:18px;margin:16px 0}}.card h3{{margin:0 0 8px}}footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}</style></head><body><main>
<header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}countries/">All countries</a> · <a href="{BASE}">Home</a></header>
<p class="lead">{esc(country)} · Official sources · Updated: {today}</p><h1>{esc(title)}</h1><p class="lead">{esc(description)}</p>
<div class="notice"><strong>Important:</strong> {esc(notice)}</div>
{"".join(sections)}
<p class="lead">The definitive conditions are those published by the responsible public authority.</p>
<footer><a href="{BASE}methodology.html">Methodology and data quality</a> · <a href="{BASE}privacy.html">Privacy</a><p>Global Support Radar is an independent information service, not a government agency.</p></footer>
</main></body></html>'''
 out=ROOT/"countries"/a.language/"index.html";out.parent.mkdir(parents=True,exist_ok=True);out.write_text(page,encoding="utf-8")
 tree=ET.parse(SITEMAP);root=tree.getroot()
 existing={n.find(f"{{{NS}}}loc").text for n in root.findall(f"{{{NS}}}url") if n.find(f"{{{NS}}}loc") is not None}
 if url not in existing:
  node=ET.SubElement(root,f"{{{NS}}}url");ET.SubElement(node,f"{{{NS}}}loc").text=url;ET.SubElement(node,f"{{{NS}}}lastmod").text=today
 tree.write(SITEMAP,encoding="utf-8",xml_declaration=True)
 print(f"Built {country} ({cc}) localized country page with {len(rows)} official portal links.")
if __name__=="__main__": main()
