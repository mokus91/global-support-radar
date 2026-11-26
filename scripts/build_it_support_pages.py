#!/usr/bin/env python3
"""Build an Italian-language directory of official national support portals."""
from __future__ import annotations
import html,json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"worldwide-national-support-sources.json"
OUT=ROOT/"countries"/"it"/"index.html"
SITEMAP=ROOT/"sitemap.xml"
BASE="https://mokus91.github.io/global-support-radar/"
NS="http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("",NS)
LABELS={"all":"Incentivi e finanziamenti","family":"Famiglia e figli","social":"Prestazioni sociali","housing":"Casa e abitazione","energy":"Energia e ambiente","business":"Imprese e nuove attività","agriculture":"Agricoltura e sviluppo rurale","education":"Istruzione e ricerca","employment":"Lavoro e occupazione","healthcare":"Salute","transport":"Trasporti"}
def esc(v):return html.escape(str(v or ""),quote=True)
def valid(v):
 p=urlparse(str(v or ""));return str(v) if p.scheme=="https" and p.netloc and not p.username and not p.password else None
def main():
 data=json.loads(DATA.read_text(encoding="utf-8"))
 rows=[r for r in data.get("records",[]) if r.get("country_code")=="IT" and valid(r.get("url"))]
 groups={}
 for r in rows:groups.setdefault(r.get("category","all"),[]).append(r)
 sections=[]
 for key,items in sorted(groups.items(),key=lambda x:LABELS.get(x[0],x[0])):
  cards=[]
  for r in sorted(items,key=lambda x:x.get("name_it") or x.get("name_en") or ""):
   title=r.get("name_it") or r.get("name_en") or "Portale informativo ufficiale"
   desc=r.get("description_it") or r.get("description_en") or "Informazioni ufficiali e indicazioni sulle misure disponibili."
   cards.append(f'<article class="card"><h3><a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a></h3><p>{esc(desc)}</p><small>Ente: {esc(r.get("publisher","Ente pubblico"))} · Stato fonte: {esc(r.get("verification_status","da verificare"))}</small></article>')
  sections.append(f'<section><h2>{esc(LABELS.get(key,"Altre agevolazioni"))}</h2>{"".join(cards)}</section>')
 today=datetime.now(timezone.utc).date().isoformat()
 page=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Contributi, bonus e agevolazioni statali in Italia | Global Support Radar</title>
<meta name="description" content="Trova portali ufficiali italiani per contributi, bonus famiglia, prestazioni INPS, incentivi alle imprese, agricoltura, lavoro ed energia.">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}countries/it/">
<meta property="og:type" content="website"><meta property="og:title" content="Contributi e agevolazioni in Italia"><meta property="og:description" content="Fonti ufficiali per bonus, incentivi e prestazioni pubbliche italiane.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Contributi e agevolazioni in Italia","inLanguage":"it-IT","url":"{BASE}countries/it/","dateModified":"{today}","isPartOf":{{"@type":"WebSite","name":"Global Support Radar","url":"{BASE}"}}}}</script>
<style>:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;color:var(--text);text-decoration:none}}h1{{font-size:clamp(28px,5vw,44px);line-height:1.2}}.lead,.muted,small{{color:var(--muted)}}.notice,.card{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:18px;margin:16px 0}}.card h3{{margin:0 0 8px}}footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}</style></head><body><main>
<header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}countries/">Tutti i paesi</a> · <a href="{BASE}">Home</a></header>
<p class="muted">Italia · Fonti ufficiali · Aggiornato: {today}</p>
<h1>Contributi, bonus e agevolazioni statali in Italia</h1>
<p class="lead">Consulta le fonti pubbliche ufficiali per incentivi alle imprese, sostegni alle famiglie, prestazioni sociali, agricoltura, lavoro, casa ed energia.</p>
<div class="notice"><strong>Attenzione:</strong> Questa pagina raccoglie portali informativi ufficiali. La presenza di un collegamento non significa che un bando sia aperto o che tu abbia diritto al beneficio. Verifica requisiti, scadenze, fondi disponibili e modalità di domanda presso l'ente competente. Un finanziamento agevolato può essere un prestito da restituire, non un contributo a fondo perduto.</div>
{"".join(sections)}
<p class="muted">Le fonti sono punti di accesso alla ricerca; le condizioni definitive sono quelle pubblicate dall'amministrazione responsabile.</p>
<footer><a href="{BASE}methodology.html">Metodo e qualità dei dati</a> · <a href="{BASE}privacy.html">Privacy</a><p>Global Support Radar è un servizio informativo indipendente, non un ente pubblico.</p></footer>
</main></body></html>'''
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(page,encoding="utf-8")
 tree=ET.parse(SITEMAP);root=tree.getroot()
 existing={n.find(f"{{{NS}}}loc").text for n in root.findall(f"{{{NS}}}url") if n.find(f"{{{NS}}}loc") is not None}
 url=BASE+"countries/it/"
 if url not in existing:
  node=ET.SubElement(root,f"{{{NS}}}url");ET.SubElement(node,f"{{{NS}}}loc").text=url;ET.SubElement(node,f"{{{NS}}}lastmod").text=today
 tree.write(SITEMAP,encoding="utf-8",xml_declaration=True)
 print(f"Built Italian country page with {len(rows)} official portal links.")
if __name__=="__main__":main()
