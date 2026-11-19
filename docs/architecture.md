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

The GitHub Actions workflow runs once daily and queries two official EU services: the data.europa.eu dataset catalogue and the European Commission Funding & Tenders public Search API. Outputs are saved as discovery candidates. It does **not** yet verify each individual call page, determine visitor eligibility, translate notices, or send alerts. A catalogue record is not a programme record. The distinction is deliberate to prevent false or misleading benefit claims.

## Adapter requirements

Every future adapter must:
- use a publisher-documented API, feed or permitted public page;
- obey rate limits and reuse/licence terms;
- preserve original source URL and language;
- avoid guessing dates, amounts or eligibility;
- emit errors and last-success timestamps;
- never promote a record to `open-and-current` based only on a search result or dataset title.


## Current official discovery adapters

- `scripts/discover_sources.py` calls the documented read-only data.europa.eu Search API using GET query parameters.
- `scripts/discover_eu_funding.py` calls the European Commission Funding & Tenders public Search API. Its query is restricted to selected grant/topic types and open/forthcoming status codes documented by the portal API guide.
- Both outputs remain explicitly `unverified`. The Funding & Tenders response is preserved as raw JSON because field mappings and each call's original detail URL must be checked before normalization.
- The daily GitHub Actions workflow refreshes both JSON discovery files. A successful API response is not equivalent to a verified, currently available grant.
