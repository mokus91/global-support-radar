# Data pipeline and verification architecture

## Pipeline

1. **Source registry** records the publisher, jurisdiction, source type, documented access method and limitations.
2. **Discovery adapters** query documented APIs/feeds and save candidate datasets or programme links as unverified.
3. **Normalization** maps only supported facts into `data/programme.schema.json`.
4. **Verification** checks the original official programme page, eligibility, dates and application destination.
5. **Publication** exposes only records that pass the publication rules; expired/withdrawn records are removed from active search but retained for audit.
6. **Monitoring** rechecks open records on a schedule and records the verification timestamp.

## Status meanings

- `unverified`: discovered, not checked against the original programme notice.
- `official-page-checked`: official page inspected, but current availability is not confirmed.
- `open-and-current`: official page confirms the programme is currently open or ongoing.
- `closed`, `expired`, `withdrawn`: not available for new applications.

## Current automation boundary

The GitHub Actions workflow runs once daily and refreshes the EU catalogue discovery index. It does **not** currently harvest individual grants, translate notices, verify eligibility, or send alerts. A catalogue record is not a programme record. The distinction is deliberate to prevent false or misleading benefit claims.

## Adapter requirements

Every future adapter must:
- use a publisher-documented API, feed or permitted public page;
- obey rate limits and reuse/licence terms;
- preserve original source URL and language;
- avoid guessing dates, amounts or eligibility;
- emit errors and last-success timestamps;
- never promote a record to `open-and-current` based only on a search result or dataset title.
