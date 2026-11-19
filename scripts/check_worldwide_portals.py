#!/usr/bin/env python3
"""Daily reachability check for country-specific official support portals.

A reachable URL is not proof that a programme is open or that an applicant qualifies.
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import json
import os
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "worldwide-national-support-sources.json"
OUTPUT = ROOT / "data" / "worldwide-portal-health.json"
TIMEOUT = 25
USER_AGENT = "GlobalSupportRadar-SourceMonitor/1.0 (+https://mokus91.github.io/global-support-radar/)"
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()


def check(record: dict) -> dict:
    req = urllib.request.Request(
        record["url"],
        headers={"User-Agent": USER_AGENT, "Range": "bytes=0-512", "Accept": "text/html,*/*"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT) as response:
            code = response.status
            final_url = response.geturl()
            response.read(512)
        state = "reachable" if 200 <= code < 400 else "http_error"
        return {"id": record["id"], "status": state, "http_status": code, "final_url": final_url}
    except urllib.error.HTTPError as exc:
        code = exc.code
        state = "restricted" if code in (401, 403, 429) else ("not_found" if code == 404 else "http_error")
        return {"id": record["id"], "status": state, "http_status": code, "final_url": exc.geturl()}
    except Exception as exc:
        return {"id": record["id"], "status": "connection_error", "error": type(exc).__name__}


def main() -> None:
    directory = json.loads(INPUT.read_text(encoding="utf-8"))
    records = directory.get("records", [])
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, records))
    output = {
        "schema_version": "1.0",
        "checked_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "records_count": len(results),
        "summary": {
            state: sum(1 for item in results if item["status"] == state)
            for state in sorted({item["status"] for item in results})
        },
        "note": "Reachability only. HTTP status does not confirm programme availability, eligibility or deadline.",
        "records": results,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checked": len(results), "summary": output["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
