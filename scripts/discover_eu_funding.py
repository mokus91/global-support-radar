#!/usr/bin/env python3
"""Discover public EU Funding & Tenders call records; all results remain unverified."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/eu-funding-discovery.json"
URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA&text=*"
QUERY = {"bool": {"must": [
    {"terms": {"type": ["1", "2", "8"]}},
    {"terms": {"status": ["31094501", "31094502"]}}
]}}

def multipart(parts):
    boundary = "----GSR" + uuid.uuid4().hex
    chunks = []
    for name, value, content_type in parts:
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n'.encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            value.encode("utf-8"), b"\r\n"
        ])
    chunks.append(f"--{boundary}--\r\n".encode())
    return boundary, b"".join(chunks)

def collect():
    parts = [
        ("query", json.dumps(QUERY), "application/json"),
        ("languages", json.dumps(["en"]), "application/json"),
        ("displayLanguage", "en", "text/plain")
    ]
    boundary, body = multipart(parts)
    req = Request(URL, data=body, method="POST", headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; GlobalSupportRadar/0.1)",
        "Referer": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/"
    })
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    error = None
    payload = {}
    try:
        payload = collect()
    except Exception as exc:
        error = str(exc)[:500]
    # Preserve the raw official API response: do not infer deadlines, eligibility or status.
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_id": "eu-funding",
        "source_url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
        "purpose": "Official call discovery only. Every result requires individual page verification before publication.",
        "verification_status": "unverified",
        "error": error,
        "response": payload
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if error:
        print("EU Funding & Tenders discovery failed: " + error)
    else:
        print("EU Funding & Tenders API response saved for verification.")

if __name__ == "__main__":
    main()
