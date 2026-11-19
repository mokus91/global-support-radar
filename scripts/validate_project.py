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
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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
        if parsed.scheme != "https" or not parsed.netloc:
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
            if url and urlparse(url).scheme != "https":
                raise SystemExit(f"{path.name}: non-HTTPS official_url: {url}")

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    inline_scripts = re.findall(r"<script(?:\\s[^>]*)?>([\\s\\S]*?)</script>", html, re.I)
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
