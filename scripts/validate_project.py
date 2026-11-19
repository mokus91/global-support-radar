#!/usr/bin/env python3
"""Lightweight integrity checks for the Global Support Radar MVP."""
import json
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(path):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        relative = path.relative_to(ROOT)
        raise SystemExit(
            f"Invalid JSON in {relative} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def main():
    json_files = sorted(DATA.glob("*.json"))
    for path in json_files:
        load_json(path)

    registry = load_json(DATA / "source-registry.json")
    sources = registry.get("sources", [])
    ids = [source.get("id") for source in sources]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate source IDs in source-registry.json")
    for source in sources:
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise SystemExit(f"Invalid official source URL: {source.get('id')}")

    for path in sorted(DATA.glob("*discovery.json")):
        payload = load_json(path)
        records = payload.get("records")
        if records is None:
            continue
        if not isinstance(records, list):
            raise SystemExit(f"{path.name}: records must be a list")
        declared = payload.get("records_count")
        if declared is not None and declared != len(records):
            raise SystemExit(f"{path.name}: records_count does not match records length")
        for row in records:
            url = row.get("official_url")
            if url:
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                    raise SystemExit(f"{path.name}: invalid official_url: {url}")
            amount_status = row.get("amount_status")
            if amount_status:
                if amount_status not in ("published", "not_published", "not_published_or_zero_in_api", "source_field_untyped"):
                    raise SystemExit(f"{path.name}: unsupported amount_status: {amount_status}")
                currency = row.get("amount_currency")
                if amount_status == "published" and (not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency)):
                    raise SystemExit(f"{path.name}: published amount requires a three-letter currency code")
                for amount_key in ("amount_maximum", "total_call_budget", "maximum_amount_jpy"):
                    amount_value = row.get(amount_key)
                    if amount_value is not None and (not isinstance(amount_value, (int, float)) or isinstance(amount_value, bool) or amount_value < 0):
                        raise SystemExit(f"{path.name}: invalid non-negative numeric amount in {amount_key}")

    if not (DATA / "eu-funding-discovery.json").is_file():
        raise SystemExit("EU Funding & Tenders API audit file is missing")

    feed_status = load_json(DATA / "feed-status.json")
    feeds = feed_status.get("feeds", [])
    if not isinstance(feeds, list) or not feeds:
        raise SystemExit("feed-status.json must contain a non-empty feeds list")
    filenames = [feed.get("file") for feed in feeds]
    if len(filenames) != len(set(filenames)):
        raise SystemExit("Duplicate feed filenames in feed-status.json")
    for filename in filenames:
        if not filename or Path(filename).name != filename:
            raise SystemExit(f"Unsafe feed filename in feed-status.json: {filename}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for required in ("feedHealthSection", "loadFeedStatus", "data/feed-status.json"):
        if required not in html:
            raise SystemExit(f"Missing feed-health dashboard component: {required}")
    main_search_feeds = ("jgrants-discovery.json", "chile-discovery.json", "spain-discovery.json", "us-grants-discovery.json", "ukri-discovery.json", "hu-nkfih-discovery.json", "eu-open-calls-discovery.json")
    for filename in main_search_feeds:
        if not (DATA / filename).is_file() or filename not in html:
            raise SystemExit(f"Main search feed missing or not wired: {filename}")
    for required in ("function classifyOpportunity(row)", "verified-open", "source-listed-open", "opportunityState.key!==\"closed\""):
        if required not in html:
            raise SystemExit(f"Closed/withdrawn opportunity filtering is missing: {required}")

    for required in ("const merged=new Map()", "normalizeUrl", "titleKey(row)", "stableId=row.id||row.identifier", "unkeyed::", "liveListings=[...merged.values()]"):
        if required not in html:
            raise SystemExit(f"Cross-feed duplicate protection is missing: {required}")

    if "SAVED_KEY" not in html or "savedToggle" not in html:
        raise SystemExit("On-device saved opportunities feature is missing")
    for required in ("notExpired", "updatedMeta", "official_api_live_acceptance_candidate", "exportCurrentResults", "exportCsv", "exportSavedCalendar", "exportCalendar", "Date.parse(row._deadline)>=Date.now()", "loadMoreWrap", "visibleLimit", "staleAfterMs", "Check overdue", "syncSearchUrl", "restoreSearchUrl", "copySearchLink", "shareSearch", "manifest.webmanifest", "offlineNotice", "serviceWorker.register", "sw.js"):
        if required not in html:
            raise SystemExit(f"Main search quality feature is missing: {required}")

    for required_file in ("robots.txt", "sitemap.xml"):
        if not (ROOT / required_file).is_file():
            raise SystemExit(f"SEO discovery file is missing: {required_file}")
    for required in ("sourceCoverageSummary", "Automated integrations", "sourceCoverageNote", "not currently open grants"):
        if required not in html:
            raise SystemExit(f"Source coverage transparency panel is missing: {required}")

    if "schema.org" not in html or "SearchAction" not in html:
        raise SystemExit("Structured website/search metadata is missing")

    manifest = load_json(ROOT / "manifest.webmanifest")
    if manifest.get("start_url") != "./" or manifest.get("scope") != "./":
        raise SystemExit("PWA manifest must use the repository-relative GitHub Pages scope")
    if not (ROOT / "sw.js").is_file() or not (ROOT / "icon.svg").is_file():
        raise SystemExit("PWA service worker or SVG icon is missing")
    for icon_file in ("icon-192.png", "icon-512-maskable.png"):
        if not (ROOT / icon_file).is_file():
            raise SystemExit(f"PWA raster icon is missing: {icon_file}")
    icon_entries = manifest.get("icons", [])
    required_icons = {("./icon-192.png", "192x192", "any"), ("./icon-512-maskable.png", "512x512", "maskable")}
    actual_icons = {(icon.get("src"), icon.get("sizes"), icon.get("purpose")) for icon in icon_entries}
    if not required_icons.issubset(actual_icons):
        raise SystemExit("PWA manifest must declare 192px any and 512px maskable PNG icons")
    worker = (ROOT / "sw.js").read_text(encoding="utf-8")
    if 'url.pathname.endsWith(".json")' not in worker or 'url.pathname.includes("/data/")' not in worker:
        raise SystemExit("Service worker must never cache live JSON opportunity data")

    script_blocks = re.findall(r"<script\b([^>]*)>([\s\S]*?)</script>", html, re.I)
    javascript_index = 0
    jsonld_count = 0
    for attributes, script in script_blocks:
        if not script.strip():
            continue
        type_match = re.search(r"""\btype\s*=\s*["']([^"']+)["']""", attributes, re.I)
        script_type = type_match.group(1).strip().lower() if type_match else ""
        if script_type == "application/ld+json":
            try:
                jsonld = json.loads(script)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON-LD structured data at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
            if not isinstance(jsonld, (dict, list)):
                raise SystemExit("JSON-LD structured data must be a JSON object or array")
            jsonld_count += 1
            continue
        # Non-JavaScript script types are data blocks, not executable code.
        if script_type and script_type not in ("module", "text/javascript", "application/javascript"):
            continue
        javascript_index += 1
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as handle:
            handle.write(script)
            handle.flush()
            result = subprocess.run(["node", "--check", handle.name], capture_output=True, text=True)
            if result.returncode:
                raise SystemExit(f"Inline JavaScript {javascript_index} syntax error:\\n{result.stderr}")
    if jsonld_count == 0:
        raise SystemExit("JSON-LD structured website metadata is missing")

    print(f"Validation passed: {len(json_files)} JSON files, {len(sources)} official sources, inline JavaScript syntax OK.")


if __name__ == "__main__":
    main()
