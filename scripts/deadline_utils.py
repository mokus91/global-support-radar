"""Conservative parsing helpers for grant application deadlines."""
from __future__ import annotations

import datetime as dt


def parse_deadline(value: object) -> dt.datetime | None:
    """Parse a deadline; date-only values remain valid through that whole UTC day."""
    if value in (None, ""):
        return None
    text = str(value).strip()
    try:
        if len(text) == 10:
            day = dt.date.fromisoformat(text)
            return dt.datetime.combine(day, dt.time.max, tzinfo=dt.timezone.utc)
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except (TypeError, ValueError):
        return None
