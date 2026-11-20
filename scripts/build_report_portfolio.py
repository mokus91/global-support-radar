#!/usr/bin/env python3
"""Generate separate organization reports from a small, validated profile matrix."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generate_organization_report import filter_records, load_records, render


def load_profiles(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("profiles"), list):
        raise ValueError("Profile config must contain a profiles list")
    profiles = payload["profiles"]
    seen: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, dict):
            raise ValueError("Every profile must be an object")
        profile_id = profile.get("id")
        if not isinstance(profile_id, str) or not re.fullmatch(r"[a-z0-9-]{2,60}", profile_id):
            raise ValueError(f"Invalid profile id: {profile_id!r}")
        if profile_id in seen:
            raise ValueError(f"Duplicate profile id: {profile_id}")
        seen.add(profile_id)
        for key in ("country", "category"):
            value = profile.get(key)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{profile_id}: {key} must be a non-empty string or null")
    return profiles


def build_portfolio(data_dir: Path, config_path: Path, output_dir: Path, today=None) -> list[Path]:
    profiles = load_profiles(config_path)
    records = load_records(data_dir)
    generated = []
    current_day = today or datetime.now(timezone.utc).date()
    for profile in profiles:
        country, category = profile.get("country"), profile.get("category")
        selected = filter_records(records, country=country, category=category)
        report = render(selected, current_day, country=country, category=category)
        title = profile.get("title") or profile["id"]
        report = report.replace("# Szervezeti támogatásfigyelő riport",
                                f"# {title} – támogatásfigyelő riport", 1)
        output = output_dir / f"{profile['id']}.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        generated.append(output)
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--config", type=Path, default=Path("config/report-profiles.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/profiles"))
    args = parser.parse_args()
    outputs = build_portfolio(args.data_dir, args.config, args.output_dir)
    print(f"Generated {len(outputs)} profile reports:")
    for output in outputs:
        print(f"- {output}")


if __name__ == "__main__":
    main()
