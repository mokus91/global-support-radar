#!/usr/bin/env python3
from __future__ import annotations
import argparse,html,json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data/worldwide-national-support-sources.json"; SITEMAP=ROOT/"sitemap.xml"
BASE="https://mokus91.github.io/global-support-radar/"; NS="http://www.sitemaps.org/schemas/sitemap/0.9"; ET.register_namespace("",NS)
CFG={
"fi":("FI","fi","Suomi","Avustukset, tuet ja julkinen rahoitus Suomessa","Viralliset suomalaiset lähteet perhe-etuuksista, yritystuista, maataloudesta, sosiaaliturvasta ja energiasta.","Huomio: linkki ei tarkoita, että haku on avoinna tai että olet automaattisesti oikeutettu tukeen. Tarkista ehdot ja määräajat vastuulliselta viranomaiselta."),
"da":("DK","da","Danmark","Tilskud, ydelser og offentlig støtte i Danmark","Officielle danske kilder om familieydelser, boligstøtte, erhvervsstøtte, landbrug og energi.","Bemærk: et link betyder ikke, at en ordning er åben, eller at du automatisk er berettiget. Kontrollér betingelser og frister hos myndigheden."),
"no":("NO","no","Norge","Tilskudd, ytelser og offentlig støtte i Norge","Offisielle norske kilder om familieytelser, sosialhjelp, boligstøtte, næringsliv, landbruk og arbeid.","Merk: en lenke betyr ikke at en ordning er åpen eller at du automatisk har rett til støtte. Kontroller vilkår og frister hos myndigheten."),
"ie":("IE","en-IE","Ireland","Government grants, benefits and support in Ireland","Official Irish sources for family payments, social welfare, business grants, agriculture and energy supports.","A link does not mean a scheme is currently open or that you automatically qualify. Check eligibility and deadlines with the responsible authority.")
}
LABELS={
"fi":{"all":"Kaikki avustukset ja rahoitus","family":"Perheet ja lapset","social":"Sosiaaliturva","housing":"Asuminen","energy":"Energia ja ympäristö","business":"Yritykset ja yrittäjyys","agriculture":"Maatalous ja maaseudun kehittäminen","education":"Koulutus ja tutkimus","employment":"Työ ja työllisyys","healthcare":"Terveydenhuolto","transport":"Liikenne"},
"da":{"all":"Alle tilskud og finansieringsmuligheder","family":"Familie og børn","social":"Sociale ydelser","housing":"Bolig","energy":"Energi og miljø","business":"Virksomheder og iværksættere","agriculture":"Landbrug og udvikling af landdistrikter","education":"Uddannelse og forskning","employment":"Arbejde og beskæftigelse","healthcare":"Sundhed","transport":"Transport"},
"no":{"all":"Alle tilskudd og finansieringsordninger","family":"Familie og barn","social":"Sosiale ytelser","housing":"Bolig","energy":"Energi og miljø","business":"Bedrifter og gründere","agriculture":"Landbruk og bygdeutvikling","education":"Utdanning og forskning","employment":"Arbeid og sysselsetting","healthcare":"Helse","transport":"Transport"},
"ie":{"all":"All grants and funding","family":"Families and children","social":"Social welfare","housing":"Housing","energy":"Energy and environment","business":"Businesses and entrepreneurs","agriculture":"Agriculture and rural development","education":"Education and research","employment":"Work and employment","healthcare":"Healthcare","transport":"Transport"}
}
def esc(x): return html.escape(str(x or ""),quote=True)
def main():
 p=argparse.ArgumentParser();p.add_argument("country",choices=CFG);a=p.parse_args()
 cc,lang,country,title,desc,notice=CFG[a.country]; data=json.loads(DATA.read_text(encoding="utf-8"))
 rows=[r for r in data.get("records",[]) if r.get("country_code")==cc and urlparse(str(r.get("url",""))).scheme=="https" and urlparse(str(r.get("url",""))).netloc]
 groups={}
 for r in rows: groups.setdefault(r.get("category","all"),[]).append(r)
 sections=[]
 for cat,items in sorted(groups.items(),key=lambda z:LABELS[a.country].get(z[0],z[0])):
  cards=[]
  for r in sorted(items,key=lambda x:x.get("name_"+a.country) or x.get("name_en") or ""):
   name=r.get("name_"+a.country) or r.get("name_en") or "Official public information"; description=r.get("description_"+a.country) or r.get("description_en") or "Official information."
   cards.append(f'<article class="card"><h3><a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">{esc(name)} ↗</a></h3><p>{esc(description)}</p><small>{esc(r.get("publisher","Public authority"))} · {esc(r.get("verification_status","official source"))}</small></article>')
  sections.append(f'<section><h2>{esc(LABELS[a.country].get(cat,"Other support"))}</h2>{"".join(cards)}</section>')
 today=datetime.now(timezone.utc).date().isoformat();url=BASE+f"countries/{a.country}/"
 page=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Global Support Radar</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":{json.dumps(title,ensure_ascii=False)},"inLanguage":"{lang}","url":"{url}","dateModified":"{today}","isPartOf":{{"@type":"WebSite","name":"Global Support Radar","url":"{BASE}"}}}}</script><style>:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 system-ui,sans-serif}}main{{max-width:960px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;color:var(--text);text-decoration:none}}h1{{font-size:clamp(28px,5vw,44px);line-height:1.2}}.lead,small{{color:var(--muted)}}.notice,.card{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:18px;margin:16px 0}}footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}</style></head><body><main><header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}countries/">All countries</a> · <a href="{BASE}">Home</a></header><p class="lead">{esc(country)} · Official sources · Updated: {today}</p><h1>{esc(title)}</h1><p class="lead">{esc(desc)}</p><div class="notice"><strong>Important:</strong> {esc(notice)}</div>{"".join(sections)}<footer><a href="{BASE}methodology.html">Methodology and data quality</a> · <a href="{BASE}privacy.html">Privacy</a><p>Global Support Radar is an independent information service, not a government agency.</p></footer></main></body></html>'''
 out=ROOT/"countries"/a.country/"index.html";out.parent.mkdir(parents=True,exist_ok=True);out.write_text(page,encoding="utf-8")
 tree=ET.parse(SITEMAP);root=tree.getroot();existing={n.find(f"{{{NS}}}loc").text for n in root.findall(f"{{{NS}}}url") if n.find(f"{{{NS}}}loc") is not None}
 if url not in existing:
  node=ET.SubElement(root,f"{{{NS}}}url");ET.SubElement(node,f"{{{NS}}}loc").text=url;ET.SubElement(node,f"{{{NS}}}lastmod").text=today
 tree.write(SITEMAP,encoding="utf-8",xml_declaration=True);print(f"Built {country} page with {len(rows)} official source links.")
if __name__=="__main__":main()
