#!/usr/bin/env python3
"""Validate that the project's sitemap contains valid, existing local pages."""
from pathlib import Path
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://mokus91.github.io/global-support-radar/"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def validate_sitemap(xml_text, root=ROOT, base_url=BASE_URL):
    errors = []
    try:
        tree = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [f"Invalid XML: {exc}"]
    if tree.tag != "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset":
        return ["Root element is not a sitemap urlset."]
    seen = set()
    for node in tree.findall("sm:url/sm:loc", NS):
        url = (node.text or "").strip()
        if not url.startswith(base_url):
            errors.append(f"URL outside expected site: {url}")
            continue
        if url in seen:
            errors.append(f"Duplicate URL: {url}")
            continue
        seen.add(url)
        parsed_url = urlparse(url)
        base_path = urlparse(base_url).path
        relative = unquote(parsed_url.path[len(base_path):]).lstrip("/")
        if not relative:
            relative = "index.html"
        elif relative.endswith("/"):
            relative += "index.html"
        parts = PurePosixPath(relative).parts
        if not parts or any(part in ("", ".", "..") for part in parts) or "\\" in relative:
            errors.append(f"Unsafe sitemap path: {relative}")
            continue
        candidate = (root / Path(*parts)).resolve()
        root_resolved = root.resolve()
        if not candidate.is_relative_to(root_resolved):
            errors.append(f"Unsafe sitemap path: {relative}")
            continue
        if not candidate.is_file():
            errors.append(f"Missing local page: {relative}")
    if not seen:
        errors.append("Sitemap contains no valid URLs.")
    return errors


def main():
    errors = validate_sitemap((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    if errors:
        print("\n".join(errors))
        return 1
    print("Sitemap validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
