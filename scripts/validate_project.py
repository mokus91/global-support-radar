#!/usr/bin/env python3
"""Lightweight integrity checks for the Global Support Radar MVP."""
import datetime as dt
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
        country_code = source.get("country_code")
        if country_code is not None and not re.fullmatch(r"[A-Z]{2}", country_code):
            raise SystemExit(f"Invalid country_code in source-registry.json: {source.get('id')}")
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

    # Keep historical national portal leads visibly separate from verified live funding sources.
    historical = load_json(DATA / "un-national-portals.json")
    historical_records = historical.get("records", [])
    if len(historical_records) != 193 or historical.get("records_count") != 193:
        raise SystemExit("UN national portal directory must retain all 193 Member State leads")
    for row in historical_records:
        if row.get("status") != "historical-directory-lead" or row.get("verification_status") != "not-currently-verified":
            raise SystemExit("Historical UN portal leads must never be presented as currently verified")
        if not re.fullmatch(r"[A-Z]{2}", row.get("country_code", "")):
            raise SystemExit("Historical national portal lead has an invalid country code")
        parsed = urlparse(row.get("url", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            raise SystemExit("Historical national portal lead has an invalid HTTPS URL")

    worldwide = load_json(DATA / "worldwide-national-support-sources.json")
    worldwide_records = worldwide.get("records", [])
    worldwide_ids = [row.get("id") for row in worldwide_records]
    if len(worldwide_ids) != len(set(worldwide_ids)):
        raise SystemExit("Duplicate IDs in worldwide national support source directory")
    for row in worldwide_records:
        if not re.fullmatch(r"[A-Z]{2}", row.get("country_code", "")) and row.get("country_code") != "EU":
            raise SystemExit("Worldwide support source has an invalid country code")
        parsed = urlparse(row.get("url", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            raise SystemExit("Worldwide support source must use an HTTPS URL")

    feed_status = load_json(DATA / "feed-status.json")
    feeds = feed_status.get("feeds", [])
    if not isinstance(feeds, list) or not feeds:
        raise SystemExit("feed-status.json must contain a non-empty feeds list")
    try:
        checked_at = dt.datetime.fromisoformat(feed_status.get("checked_at", "").replace("Z", "+00:00"))
        if checked_at.tzinfo is None:
            raise ValueError("checked_at must include a timezone")
    except (TypeError, ValueError):
        raise SystemExit("feed-status.json must include a valid timezone-aware checked_at timestamp")
    filenames = [feed.get("file") for feed in feeds]
    if len(filenames) != len(set(filenames)):
        raise SystemExit("Duplicate feed filenames in feed-status.json")
    allowed_feed_statuses = {"checked", "checked-empty", "audit-summary", "temporarily-unavailable", "missing", "invalid-json"}
    for feed in feeds:
        filename = feed.get("file")
        if not filename or Path(filename).name != filename:
            raise SystemExit(f"Unsafe feed filename in feed-status.json: {filename}")
        if feed.get("status") not in allowed_feed_statuses:
            raise SystemExit(f"Unsupported feed status for {filename}: {feed.get('status')}")
        if feed.get("status") == "checked" and not isinstance(feed.get("records_count"), int):
            raise SystemExit(f"Checked feed must report an integer records_count: {filename}")
        if feed.get("status") == "checked-empty" and feed.get("records_count") != 0:
            raise SystemExit(f"Checked-empty feed must report zero records: {filename}")
        try:
            stamp = dt.datetime.fromisoformat(feed.get("checked_at", "").replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("checked_at must include a timezone")
        except (TypeError, ValueError):
            raise SystemExit(f"Feed must include a valid timezone-aware checked_at timestamp: {filename}")

    retry_policies = {
        "discover_eu_national_categories.py": ("for attempt in range(2)", "time.sleep(2)", "TIMEOUT = 9"),
        "discover_eu_national_agriculture.py": ("for attempt in range(2)", "time.sleep(1 * (attempt + 1))", "TIMEOUT = 12", "ThreadPoolExecutor(max_workers=6)"),
        "discover_eu_funding.py": ("for attempt in range(3)", "time.sleep(3 * (attempt + 1))", None),
    }
    for adapter, expected in retry_policies.items():
        adapter_text = (ROOT / "scripts" / adapter).read_text(encoding="utf-8")
        for required in expected:
            if required and required not in adapter_text:
                raise SystemExit(f"Expected bounded network retry policy is missing from {adapter}: {required}")
    eu_adapter = (ROOT / "scripts" / "discover_eu_funding.py").read_text(encoding="utf-8")
    if "max_pages = 100" not in eu_adapter or '"maximum_pages": max_pages' not in eu_adapter or "orderBy=ASC" not in eu_adapter:
        raise SystemExit("EU Funding & Tenders pagination cap or nearest-deadline sorting is missing")
    # Validate the adapter contract here, before live discovery runs. The
    # checked-in JSON may be an older snapshot at this stage of the workflow;
    # validate the newly generated feed again after discovery has completed.
    for key in ('"maximum_pages": max_pages', '"pagination_complete": pagination_complete', '"sort_order": "ASC"', '"pages_fetched": pages_fetched'):
        if key not in eu_adapter:
            raise SystemExit(f"EU Funding & Tenders adapter is missing output metadata: {key}")
    eu_feed = load_json(DATA / "eu-open-calls-discovery.json")
    eu_ids = [row.get("id") for row in eu_feed.get("records", [])]
    if len(eu_ids) != len(set(eu_ids)):
        raise SystemExit("Duplicate IDs in EU open-call discovery feed")
    if any(row.get("verification_status") != "unverified" for row in eu_feed.get("records", [])):
        raise SystemExit("EU discovery candidates must remain explicitly unverified")
    eu_adapter = (ROOT / "scripts" / "discover_eu_funding.py").read_text(encoding="utf-8")
    for required in ('"opportunity_type": opportunity_type', "procurement_candidate", "classification_basis"):
        if required not in eu_adapter:
            raise SystemExit(f"EU funding/procurement classification is missing: {required}")
    for row in eu_feed.get("records", []):
        if row.get("opportunity_type") not in (None, "funding_candidate", "procurement_candidate"):
            raise SystemExit("EU feed contains an unsupported opportunity_type")
    if "def classify_opportunity_type(" not in eu_adapter:
        raise SystemExit("EU opportunity classifier function is missing")
    # Guard against false positives: procurement as a grant topic is not a contract.
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("discover_eu_funding", ROOT / "scripts" / "discover_eu_funding.py")
    eu_module = module_from_spec(spec)
    spec.loader.exec_module(eu_module)
    if eu_module.classify_opportunity_type("Service request: improve access to information") != "procurement_candidate":
        raise SystemExit("Explicit EU service requests must be procurement candidates")
    if eu_module.classify_opportunity_type("Call for proposals for common procurement actions") != "funding_candidate":
        raise SystemExit("A grant call about procurement must remain a funding candidate")
    if eu_module.classify_opportunity_type("Open tender for equipment") != "procurement_candidate":
        raise SystemExit("Explicit open tender notices must be separated as procurement candidates")
    if eu_module.classify_opportunity_type("Procurement innovation grant for small businesses") != "funding_candidate":
        raise SystemExit("Procurement as a grant topic must remain a funding candidate")

    audit_script = (ROOT / "scripts" / "audit_opportunity_quality.py").read_text(encoding="utf-8")
    for required in ('"procurement_review_queue_count"', '"procurement_candidates"', 'opportunity_type") == "procurement_candidate":', 'continue'):
        if required not in audit_script:
            raise SystemExit(f"Procurement candidates are not separated from grant quality metrics: {required}")
    quality_dashboard = (ROOT / "quality.html").read_text(encoding="utf-8")
    if "Közbeszerzési / szolgáltatási jelöltek – nem támogatások" not in quality_dashboard:
        raise SystemExit("Separate procurement review panel is missing from quality dashboard")
    arc_adapter = (ROOT / "scripts" / "discover_au_arc_grants.py").read_text(encoding="utf-8")
    if "max_pages = 40" not in arc_adapter or '"maximum_pages": max_pages' not in arc_adapter or "pagination_complete" not in arc_adapter:
        raise SystemExit("Australian ARC pagination completeness tracking is missing")
    for required in ("time_budget_seconds = 180", '"collection_truncated": budget_exhausted or pages >= max_pages', "urlopen(req, timeout=12)"):
        if required not in arc_adapter:
            raise SystemExit(f"Australian ARC bounded runtime protection is missing: {required}")
    arc_feed = load_json(DATA / "au-arc-grants-discovery.json")
    # Older checked-in snapshots predate the pagination metadata. Validate
    # completeness only after that feed has been regenerated by this workflow.
    if "maximum_pages" in arc_feed and arc_feed.get("pages_fetched", 0) >= arc_feed["maximum_pages"] and arc_feed.get("pagination_complete") is not False:
        raise SystemExit("Australian ARC feed reached its page cap without an incomplete-pagination warning")

    health_script = ROOT / "scripts" / "check_published_site.py"
    health_workflow = ROOT / ".github" / "workflows" / "site-health.yml"
    if not health_script.is_file() or not health_workflow.is_file():
        raise SystemExit("Scheduled published-site health monitor is missing")
    health_text = health_script.read_text(encoding="utf-8")
    workflow_text = health_workflow.read_text(encoding="utf-8")
    for required in ("feed-status.json", "max_age_hours", "temporarily-unavailable", "records_count"):
        if required not in health_text:
            raise SystemExit(f"Published-site health check is missing: {required}")
    for required in ('cron: "17 */6 * * *"', "timeout-minutes: 5", "check_published_site.py"):
        if required not in workflow_text:
            raise SystemExit(f"Scheduled site-health workflow is missing: {required}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for required in ("feedHealthSection", "loadFeedStatus", "data/feed-status.json"):
        if required not in html:
            raise SystemExit(f"Missing feed-health dashboard component: {required}")
    main_search_feeds = ("jgrants-discovery.json", "chile-discovery.json", "spain-discovery.json", "us-grants-discovery.json", "ukri-discovery.json", "hu-nkfih-discovery.json", "eu-open-calls-discovery.json")
    for filename in main_search_feeds:
        if not (DATA / filename).is_file() or filename not in html:
            raise SystemExit(f"Main search feed missing or not wired: {filename}")
    for required in ("eligibilityMeta", "eligibility_verified===true", "function classifyOpportunity(row)", "verified-open", "source-listed-open", "opportunityState.key!==\"closed\"", "EU KÖZBESZERZÉSI / SZOLGÁLTATÁSI JELÖLT", "ELŐREJELZETT – MÉG NEM NYITOTT", "application window must not be treated as open"):
        if required not in html:
            raise SystemExit(f"Closed/withdrawn opportunity filtering is missing: {required}")

    for required in ("const merged=new Map()", "normalizeUrl", "titleKey(row)", "stableId=row.id||row.identifier", "unkeyed::", "liveListings=[...merged.values()]"):
        if required not in html:
            raise SystemExit(f"Cross-feed duplicate protection is missing: {required}")

    if "SAVED_KEY" not in html or "savedToggle" not in html:
        raise SystemExit("On-device saved opportunities feature is missing")
    if "notExpired" in html or "return notClosed&&" not in html:
        raise SystemExit("Main search must exclude expired/closed records using classifyOpportunity without undefined filter variables")

    for required in ("classifyOpportunity(row)", "opportunityState.key!==\"closed\"", "updatedMeta", "official_api_live_acceptance_candidate", "exportCurrentResults", "exportCsv", "exportSavedCalendar", "exportCalendar", "Date.parse(row._deadline)>=Date.now()", "loadMoreWrap", "visibleLimit", "staleAfterMs", "Check overdue", "syncSearchUrl", "restoreSearchUrl", "copySearchLink", "shareSearch", "manifest.webmanifest", "offlineNotice", "serviceWorker.register", "sw.js"):
        if required not in html:
            raise SystemExit(f"Main search quality feature is missing: {required}")

    for required_file in ("robots.txt", "sitemap.xml"):
        if not (ROOT / required_file).is_file():
            raise SystemExit(f"SEO discovery file is missing: {required_file}")

    updates_page = ROOT / "updates.html"
    if not updates_page.is_file():
        raise SystemExit("Public opportunity change-log page is missing")
    updates_text = updates_page.read_text(encoding="utf-8")
    for required in ("opportunity-changes.json", "closure not confirmed", "verification", "aria-live"):
        if required not in updates_text:
            raise SystemExit(f"Public change-log transparency safeguard is missing: {required}")

    if "<script>" not in updates_text or "</script>" not in updates_text:
        raise SystemExit("Public change-log page has no executable rendering script")
    updates_script = updates_text.split("<script>", 1)[1].split("</script>", 1)[0]
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as handle:
        handle.write(updates_script)
        handle.flush()
        result = subprocess.run(["node", "--check", handle.name], capture_output=True, text=True)
        if result.returncode:
            raise SystemExit(f"Public change-log JavaScript syntax error:\\n{result.stderr}")
    if 'href="./updates.html"' not in html:
        raise SystemExit("Homepage link to the public opportunity change log is missing")
    sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if "https://mokus91.github.io/global-support-radar/updates.html" not in sitemap_text:
        raise SystemExit("Public opportunity change-log page is missing from sitemap.xml")
    for required in ("sourceCoverageSummary", "Automated integrations", "sourceCoverageNote", "not currently open grants", "europe-national-portals.json", "official-national-portal", "nationalPortals", "27 national portals", "euFundingGuide", "eu-funding-guide-i18n", "shared-management", "implementing partners"):
        if required not in html:
            raise SystemExit(f"Source coverage transparency panel is missing: {required}")
    for required in ("MISSOC", "31 countries", "12 areas", "Open database", "Family benefits", "family-benefits/", "Minimum income", "Housing, rent and energy-cost support", "JRC147049", "2025 Minimum Income Report", "access-high-quality-social-services", "category===\"housing\"", "category===\"energy\"", "ASPIRE global social protection database", "140 countries", "ILO — global social protection database", "222 countries and territories", "23.9%", "222 ország és terület"):
        if required not in html:
            raise SystemExit(f"Comparative social protection directory is missing: {required}")
    for required in ("coverageMatrix", "Országonkénti lefedettség", "Checked feeds", "Historical portal lead", "un-national-portals.json", "worldwide-national-support-sources.json"):
        if required not in html:
            raise SystemExit(f"Country coverage matrix is missing: {required}")

    for required in ("trustPolicy", "trustPolicyTitle", "Official source", "Open status", "Eligibility & amount", "nem garantál támogatást"):
        if required not in html:
            raise SystemExit(f"Trust and verification policy panel is missing: {required}")

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

    opening_script_tags = len(re.findall(r"<script\b", html, re.I))
    closing_script_tags = len(re.findall(r"</script\s*>", html, re.I))
    if opening_script_tags != closing_script_tags:
        raise SystemExit(
            f"HTML script tag count mismatch: {opening_script_tags} opening, {closing_script_tags} closing"
        )

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
