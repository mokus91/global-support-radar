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
    main_search_feeds = ("jgrants-discovery.json", "chile-discovery.json", "spain-discovery.json", "us-grants-discovery.json", "ukri-discovery.json")
    for filename in main_search_feeds:
        if not (DATA / filename).is_file() or filename not in html:
            raise SystemExit(f"Main search feed missing or not wired: {filename}")
    if "SAVED_KEY" not in html or "savedToggle" not in html:
        raise SystemExit("On-device saved opportunities feature is missing")
    for required in ("notExpired", "updatedMeta", "official_api_live_acceptance_candidate", "exportCurrentResults", "exportCsv", "exportSavedCalendar", "exportCalendar", "Date.parse(row._deadline)>=Date.now()", "loadMoreWrap", "visibleLimit", "syncSearchUrl", "restoreSearchUrl", "copySearchLink", "shareSearch"):
        if required not in html:
            raise SystemExit(f"Main search quality feature is missing: {required}")

    inline_scripts = re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", html, re.I)
    for index, script in enumerate((item for item in inline_scripts if item.strip()), start=1):
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as handle:
            handle.write(script)
            handle.flush()
            result = subprocess.run(["node", "--check", handle.name], capture_output=True, text=True)
            if result.returncode:
                raise SystemExit(f"Inline JavaScript {index} syntax error:\\n{result.stderr}")

    print(f"Validation passed: {len(json_files)} JSON files, {len(sources)} official sources, inline JavaScript syntax OK.")


if __name__ == "__main__":
    main()
