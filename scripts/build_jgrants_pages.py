#!/usr/bin/env python3
"""Build Japanese-language SEO pages for current JGrants discovery records.

Records are discovery candidates from Japan's official JGrants API, not
independently verified awards. Expired records are excluded from the public
current-opportunity index. The source JSON is never modified.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "jgrants-discovery.json"
OUT = ROOT / "countries" / "jp" / "programmes"
BASE = "https://mokus91.github.io/global-support-radar/"
SITEMAP = ROOT / "sitemap.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

CATEGORY_JA = {
    "agriculture": "農業・林業・漁業",
    "family": "子育て・家族",
    "education": "教育・奨学金",
    "employment": "雇用・人材",
    "energy": "エネルギー・環境",
    "healthcare": "医療・福祉",
    "housing": "住宅・住まい",
    "social_support": "生活・社会支援",
    "transport": "交通・物流",
    "business": "中小企業・事業者",
}

def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)

def parse_date(value: object):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)

def safe_id(value: object) -> str | None:
    value = str(value or "")
    return value if re.fullmatch(r"[A-Za-z0-9_-]{3,100}", value) else None

def render(record: dict, generated: str) -> str:
    title = record.get("title_original") or "公的支援制度"
    url = record.get("official_url") or record.get("url")
    if not isinstance(url, str) or not url.startswith("https://"):
        url = "https://www.jgrants-portal.go.jp/"
    start = record.get("acceptance_start") or ""
    end = record.get("acceptance_end") or ""
    categories = [CATEGORY_JA.get(str(c), str(c)) for c in (record.get("categories") or [])]
    amount = record.get("maximum_amount_jpy") or record.get("amount_maximum")
    amount_text = f"{int(amount):,} 円" if isinstance(amount, (int, float)) and amount > 0 else "公式APIに上限額の掲載なし"
    return f"""<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow,max-image-preview:large">
<title>{esc(title)} | 日本の補助金・助成金 | Global Support Radar</title>
<meta name="description" content="{esc(title)}の公募情報。受付期間、対象分野、公式JGrants情報へのリンクを確認できます。申請条件は必ず公式ページでご確認ください。">
<link rel="canonical" href="{BASE}countries/jp/programmes/{esc(record['id'])}/">
<meta property="og:type" content="article"><meta property="og:site_name" content="Global Support Radar">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="日本の政府補助金・助成金情報。公式JGrantsページで最新条件をご確認ください。">
<script type="application/ld+json">{json.dumps({
 "@context":"https://schema.org","@type":"WebPage","name":title,
 "inLanguage":"ja","url":BASE+"countries/jp/programmes/"+str(record["id"])+"/",
 "isPartOf":{"@type":"WebSite","name":"Global Support Radar","url":BASE},
 "dateModified":generated,"about":{"@type":"GovernmentService","name":title,
 "serviceUrl":url,"provider":{"@type":"GovernmentOrganization","name":"Japan Digital Agency — JGrants"}}
}, ensure_ascii=False)}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7022315203746196" crossorigin="anonymous"></script>
<style>
:root{{color-scheme:dark;--bg:#0b1220;--panel:#142238;--text:#eef4ff;--muted:#b2c1d5;--line:#31435e;--mint:#64e2b8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.75 system-ui,-apple-system,"Noto Sans",sans-serif}}
main{{max-width:900px;margin:auto;padding:26px 18px 60px}}a{{color:var(--mint)}}.brand{{font-weight:850;text-decoration:none;color:var(--text)}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:20px;margin:18px 0}}
h1{{font-size:clamp(27px,5vw,42px);line-height:1.3}}.muted{{color:var(--muted)}}.badge{{display:inline-block;border-radius:20px;background:#3b3420;color:#ffe2a5;padding:4px 10px;font-size:13px}}
dt{{color:var(--muted);font-size:13px}}dd{{margin:2px 0 14px;font-weight:650}}.button{{display:inline-block;background:var(--mint);color:#08251e;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:800}}
footer{{border-top:1px solid var(--line);margin-top:30px;padding-top:18px;color:var(--muted);font-size:13px}}
</style></head><body><main>
<header><a class="brand" href="{BASE}">GLOBAL SUPPORT RADAR</a> · <a href="{BASE}ja/">日本語トップ</a> · <a href="{BASE}countries/jp/">日本の支援情報</a></header>
<p class="muted">日本の補助金・助成金・給付金情報 / JGrants API掲載情報</p>
<h1>{esc(title)}</h1>
<p><span class="badge">公式APIの受付期間候補・詳細確認が必要</span></p>
<section class="panel"><h2>公募情報</h2><dl>
<dt>受付開始</dt><dd>{esc(start or "公式APIに掲載なし")}</dd>
<dt>受付終了</dt><dd>{esc(end or "公式APIに掲載なし")}</dd>
<dt>対象分野</dt><dd>{esc("、".join(categories) or "公式ページで確認")}</dd>
<dt>補助上限額</dt><dd>{esc(amount_text)}</dd>
<dt>対象地域</dt><dd>{esc(record.get("target_area_original") or "公式ページで確認")}</dd>
<dt>実施機関</dt><dd>{esc(record.get("institution_name_original") or "公式ページで確認")}</dd>
</dl><a class="button" href="{esc(url)}" target="_blank" rel="noopener noreferrer">公式JGrantsページで条件を確認する ↗</a></section>
<section class="panel"><h2>申請前に必ず確認してください</h2>
<p>このページは日本政府のJGrants公開APIから取得した公募候補情報を整理したものです。API上の受付期間は、申請資格・予算残額・提出書類・現在の受付状態を保証しません。</p>
<ol><li>公式ページで募集状況と最新の締切を確認する。</li><li>対象者、対象地域、対象経費、補助率・上限額を確認する。</li><li>必要書類と電子申請の手順を実施機関の案内で確認する。</li><li>申請は必ず公式窓口から行う。</li></ol></section>
<p class="muted">データ更新日: {esc(generated)} · 元データ: Japan Digital Agency — JGrants</p>
<footer><a href="{BASE}countries/jp/programmes/">日本の公募一覧</a> · <a href="{BASE}methodology.html">データ確認方法</a> · <a href="{BASE}privacy.html">プライバシー</a>
<p>Global Support Radarは政府機関ではありません。掲載情報は参考情報であり、受給資格や採択を保証しません。</p></footer>
</main></body></html>
"""

def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc)
    today = now.date()
    records = []
    for row in payload.get("records", []):
        if not isinstance(row, dict):
            continue
        rid = safe_id(row.get("id"))
        if not rid or not row.get("title_original"):
            continue
        end = parse_date(row.get("acceptance_end"))
        if end is not None and end.date() < today:
            continue
        records.append(row)
    records.sort(key=lambda r: (str(r.get("acceptance_end") or "9999"), str(r.get("title_original") or "")))
    generated = today.isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    urls = []
    cards = []
    for row in records:
        rid = safe_id(row["id"])
        target = OUT / rid / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(row, generated), encoding="utf-8")
        page_url = f"{BASE}countries/jp/programmes/{rid}/"
        urls.append(page_url)
        cards.append(f'<li><a href="./{esc(rid)}/">{esc(row.get("title_original"))}</a>'
                     f'<br><small>受付終了: {esc(row.get("acceptance_end") or "公式ページで確認")}</small></li>')
    index = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow"><title>日本の補助金・助成金 公募一覧 | Global Support Radar</title>
<meta name="description" content="JGrants公開APIから取得した日本の補助金・助成金の受付期間候補一覧。最新条件は公式ページで確認できます。">
<link rel="canonical" href="{BASE}countries/jp/programmes/">
<style>body{{margin:0;background:#0b1220;color:#eef4ff;font:16px/1.7 system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:24px 18px}}a{{color:#64e2b8}}li{{padding:12px;border-bottom:1px solid #31435e}}small{{color:#b2c1d5}}</style></head><body><main>
<a href="{BASE}ja/">日本語トップ</a> · <a href="{BASE}countries/jp/">日本の支援情報</a>
<h1>日本の補助金・助成金 公募一覧</h1><p>JGrants公開APIから取得した受付期間候補です。申請条件・現在の受付状況は各公式ページで確認してください。</p>
<p>掲載件数: {len(records)} · 更新日: {generated}</p><ul>{''.join(cards) or '<li>現在、受付期間内の候補はありません。</li>'}</ul>
<p>公式情報: <a href="https://www.jgrants-portal.go.jp/">JGrants</a></p></main></body></html>"""
    (OUT / "index.html").write_text(index, encoding="utf-8")

    country_index = ROOT / "countries" / "jp" / "index.html"
    if country_index.exists():
        text = country_index.read_text(encoding="utf-8")
        marker = "GSR_JGRANTS_PROGRAMME_DIRECTORY"
        if marker not in text:
            block = f'<section class="notice"><h2>日本の最新公募候補（JGrants）</h2><p>受付期間内の候補: {len(records)}件。各募集条件は公式ページで確認してください。</p><p><a href="./programmes/">日本語の補助金・助成金一覧を開く →</a></p></section>\n'
            text = text.replace("</main>", block + "<!-- " + marker + " -->\n</main>")
            country_index.write_text(text, encoding="utf-8")

    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    existing = {node.find(f"{{{NS}}}loc").text for node in root.findall(f"{{{NS}}}url")
                if node.find(f"{{{NS}}}loc") is not None}
    for url in [f"{BASE}countries/jp/programmes/"] + urls:
        if url in existing:
            continue
        node = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(node, f"{{{NS}}}loc").text = url
        ET.SubElement(node, f"{{{NS}}}lastmod").text = generated
    tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)
    print(f"Generated {len(records)} current Japanese JGrants pages and added sitemap URLs.")

if __name__ == "__main__":
    main()
