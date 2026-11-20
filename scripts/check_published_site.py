#!/usr/bin/env python3
"""Check the published GitHub Pages site and its public discovery feeds."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import time


def open_with_retry(url: str):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "GlobalSupportRadar-HealthCheck/1.0"},
    )
    delays = (0, 2, 5, 10)
    last_error = None
    for attempt, delay in enumerate(delays, start=1):
        if delay:
            time.sleep(delay)
        try:
            response = urllib.request.urlopen(request, timeout=20)
            if response.status < 200 or response.status >= 300:
                response.close()
                raise RuntimeError(f"HTTP {response.status}: {url}")
            return response
        except Exception as exc:
            last_error = exc
            print(f"Retry {attempt}/{len(delays)} failed for {url}: {exc}")
    raise RuntimeError(f"Request failed after {len(delays)} attempts: {url}: {last_error}")


def fetch_json(url: str):
    with open_with_retry(url) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--max-age-hours", type=int, default=30)
    args = parser.parse_args()

    base = args.base_url.rstrip("/") + "/"
    errors: list[str] = []
    warnings: list[str] = []

    try:
        with open_with_retry(base):
            pass
        print("OK: published homepage responds")
    except Exception as exc:
        print(f"ERROR: published homepage is unavailable: {exc}")
        return 1

    try:
        manifest = fetch_json(urllib.parse.urljoin(base, "data/feed-status.json"))
    except Exception as exc:
        print(f"ERROR: feed status manifest cannot be loaded: {exc}")
        return 1

    try:
        checked_at = dt.datetime.fromisoformat(
            manifest.get("checked_at", "").replace("Z", "+00:00")
        )
        if checked_at.tzinfo is None:
            raise ValueError("timestamp has no timezone")
        age = dt.datetime.now(dt.timezone.utc) - checked_at.astimezone(dt.timezone.utc)
        age_hours = age.total_seconds() / 3600
        print(f"Feed manifest age: {age_hours:.1f} hours")
        if age_hours < -1:
            errors.append("feed manifest timestamp is more than one hour in the future")
        elif age_hours > args.max_age_hours:
            errors.append(
                f"feed manifest is stale ({age_hours:.1f}h; limit {args.max_age_hours}h)"
            )
    except (TypeError, ValueError) as exc:
        errors.append(f"invalid feed manifest timestamp: {exc}")

    feeds = manifest.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        errors.append("feed manifest has no feed entries")
        feeds = []

    for feed in feeds:
        filename = feed.get("file", "")
        if not filename or filename != filename.split("/")[-1] or not filename.endswith(".json"):
            errors.append(f"unsafe feed filename: {filename!r}")
            continue
        status = feed.get("status")
        if status in {"missing", "invalid-json"}:
            errors.append(f"{filename}: manifest status is {status}")
        elif status == "temporarily-unavailable":
            warnings.append(f"{filename}: upstream source temporarily unavailable")
        elif status not in {"checked", "checked-empty", "audit-summary"}:
            errors.append(f"{filename}: unsupported status {status!r}")

        try:
            payload = fetch_json(urllib.parse.urljoin(base, "data/" + filename))
        except Exception as exc:
            errors.append(f"{filename}: public feed cannot be loaded: {exc}")
            continue

        records = payload.get("records")
        if records is not None and not isinstance(records, list):
            errors.append(f"{filename}: records is not a list")
            continue
        declared = feed.get("records_count")
        if status in {"checked", "checked-empty"} and isinstance(records, list) and isinstance(declared, int) and declared != len(records):
            errors.append(
                f"{filename}: manifest says {declared} records but feed contains {len(records)}"
            )
        if status == "checked-empty" and declared != 0:
            errors.append(f"{filename}: checked-empty feed must declare zero records")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Health check failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Health check passed: {len(feeds)} feeds inspected, {len(warnings)} upstream warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
