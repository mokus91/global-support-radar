#!/usr/bin/env python3
"""Discover currently accepting Japanese subsidies from the official JGrants API."""
import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("data/jgrants-discovery.json")
API = "https://api.jgrants-portal.go.jp/exp/v1/public/subsidies"
PORTAL = "https://www.jgrants-portal.go.jp/grants/view/"
KEYWORDS = ["事業", "農業", "子育て", "教育", "雇用", "エネルギー"]
CATEGORY_RULES = [
    ("agriculture", ["農業", "林業", "漁業", "農林水産", "畜産", "園芸", "農地"]),
    ("family", ["子育て", "出産", "保育", "児童", "ひとり親", "家族"]),
    ("education", ["教育", "学校", "大学", "奨学金", "学生", "研修", "人材育成"]),
    ("employment", ["雇用", "就職", "労働", "働き方", "人材確保", "賃上げ", "職業"]),
    ("energy", ["エネルギー", "省エネ", "脱炭素", "再エネ", "太陽光", "蓄電池", "電力", "地熱", "GX"]),
    ("healthcare", ["医療", "介護", "福祉", "病院", "看護", "健康"]),
    ("housing", ["住宅", "空き家", "リフォーム", "耐震", "住まい", "建築"]),
    ("social_support", ["生活困窮", "生活支援", "地域福祉", "障害者", "高齢者"]),
    ("transport", ["交通", "運輸", "鉄道", "バス", "自動車", "物流"]),
    ("business", ["中小企業", "小規模事業者", "事業者", "企業", "販路", "設備投資", "IT導入", "資金繰り", "創業", "経営", "生産性", "研究開発"]),
]

def fetch(keyword):
    params = urllib.parse.urlencode({
        "keyword": keyword,
        "sort": "acceptance_end_datetime",
        "order": "ASC",
        "acceptance": "1",
    })
    request = urllib.request.Request(
        API + "?" + params,
        headers={"Accept": "application/json", "User-Agent": "GlobalSupportRadar/1.0"},
    )
    context = ssl.create_default_context()
    try:
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    with urllib.request.urlopen(request, timeout=35, context=context) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("result", []) if isinstance(payload, dict) else []

def categories(item):
    text = " ".join(str(item.get(k, "")) for k in ("title", "institution_name", "use_purpose", "industry", "detail", "subsidy_catch_phrase", "target_area_search"))
    found = [category for category, words in CATEGORY_RULES if any(word in text for word in words)]
    return found or ["business"]

def main():
    unique = {}
    errors = []
    for keyword in KEYWORDS:
        try:
            for item in fetch(keyword):
                sid = str(item.get("id", "")).strip()
                title = str(item.get("title", "")).strip()
                if not sid or not title:
                    continue
                end = item.get("acceptance_end_datetime")
                if end:
                    try:
                        parsed = datetime.fromisoformat(str(end).replace("Z", "+00:00"))
                        if parsed.tzinfo is None:
                            parsed = parsed.replace(tzinfo=timezone.utc)
                        if parsed <= datetime.now(timezone.utc):
                            continue
                    except ValueError:
                        pass
                item_url = item.get("front_subsidy_detail_page_url") or (PORTAL + urllib.parse.quote(sid))
                maximum_amount = item.get("subsidy_max_limit")
                try:
                    maximum_amount_number = float(maximum_amount) if maximum_amount not in (None, "") else None
                except (TypeError, ValueError):
                    maximum_amount_number = None
                unique[sid] = {
                    "id": sid,
                    "country_code": "JP",
                    "country_en": "Japan",
                    "country_hu": "Japán",
                    "title_original": title,
                    "institution_name_original": item.get("institution_name", ""),
                    "description_original": item.get("subsidy_catch_phrase", ""),
                    "use_purpose_original": item.get("use_purpose", ""),
                    "industry_original": item.get("industry", ""),
                    "target_area_original": item.get("target_area_search", ""),
                    "maximum_amount_jpy": maximum_amount_number if maximum_amount_number and maximum_amount_number > 0 else None,\n                    "amount_maximum": maximum_amount_number if maximum_amount_number and maximum_amount_number > 0 else None,
                    "amount_currency": "JPY" if maximum_amount_number and maximum_amount_number > 0 else None,
                    "amount_type": "maximum_subsidy_limit" if maximum_amount_number and maximum_amount_number > 0 else None,
                    "amount_status": "published" if maximum_amount_number and maximum_amount_number > 0 else "not_published_or_zero_in_api",
                    "acceptance_start": item.get("acceptance_start_datetime"),
                    "acceptance_end": end,
                    "categories": categories(item),
                    "url": item_url,
                    "official_url": item_url,
                    "application_url": item_url,
                    "source_language": "ja",
                    "publisher": "Japan Digital Agency — JGrants",
                    "verification_status": "official_api_live_acceptance_candidate",
                    "status": "acceptance-open-api-filtered",
                    "source_api": API,
                }
        except Exception as exc:
            errors.append({"keyword": keyword, "error": str(exc)[:300]})
    records = sorted(unique.values(), key=lambda x: x.get("acceptance_end") or "9999")
    output = {
        "schema_version": "1.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "country_code": "JP",
        "source": "JGrants public API, operated by Japan Digital Agency",
        "source_url": "https://developers.digital.go.jp/documents/jgrants/api/",
        "attribution": "Source: JGrants (jGrants), Government of Japan. Verify eligibility and current details on the original programme page.",
        "records_count": len(records),
        "amount_currency": "JPY",
        "records": records,
        "query_errors": errors,
        "limitations": "The API search is keyword-based and the returned set is not a complete national inventory. Japanese source titles are retained in the original language; dates and eligibility must be checked at the publisher.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Saved {len(records)} unique currently accepting JGrants candidates; {len(errors)} keyword errors.")

if __name__ == "__main__":
    main()
