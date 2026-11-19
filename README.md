# Global Support Radar

A multilingual discovery service for official government grants, benefits and public-support programmes.

**Live site:** https://mokus91.github.io/global-support-radar/

## Current implementation

- Mobile-friendly static website with Hungarian and English interface.
- Country selector covering ISO country codes.
- Ten support categories.
- Official-source registry and common programme-record JSON Schema.
- Scheduled discovery of potentially relevant EU public datasets through the official data.europa.eu Search API.
- Discovery output is stored in `data/discovery-index.json`.

## Important distinction

A dataset mentioning grants or subsidies is **not itself a verified grant**. The scheduled job only discovers catalogue datasets. It does not claim that a programme is open, that a visitor qualifies, or that an application is available. Discovered catalogue records must not be shown as live benefits until a separate adapter has inspected the original programme page and populated every required field.

The current demo cards are explicitly labelled as examples. The collector reports zero verified programmes until individual programme verification exists.

## Repository layout

- `index.html` — static frontend.
- `data/source-registry.json` — official discovery sources and coverage notes.
- `data/programme.schema.json` — normalized programme record contract.
- `data/discovery-index.json` — generated dataset discovery results.
- `scripts/discover_sources.py` — EU catalogue discovery client.
- `.github/workflows/source-discovery.yml` — daily scheduled workflow and manual run.
- `docs/architecture.md` — pipeline and verification rules.

## Run locally

Python 3.12 is sufficient; the collector uses only the standard library.

```bash
python scripts/discover_sources.py
```

## Verification rules before publishing a programme

1. The original publisher must be a government body, public authority, or explicitly identified official programme operator.
2. Store the original-language title and official application URL.
3. Confirm country/region, beneficiary group, support type and eligibility from the source.
4. Record amount/currency and opening/deadline dates only when explicitly stated.
5. Re-check status and page availability before marking a programme `open-and-current`.
6. Keep `last_verified_at`, source language and reuse/licence information.
7. Translation is an aid; the original official notice remains authoritative.

## Source scope

The EU portal API is used for dataset discovery only. ForeignAssistance.gov and UNDP Open.undp.org describe international development assistance and project spending; they are not general household-benefit directories. They must be presented in a separate development-finance context, not mixed into citizen benefit results.

## Roadmap

- Add country-specific official grant and benefit adapters with documented APIs or permitted feeds.
- Add original-page verification and expiry monitoring.
- Add multilingual summaries while preserving original source links.
- Add database-backed search, alerts and user accounts.
- Add privacy-by-design controls and transparent advertising/subscription options.

## Privacy and monetization

Do not collect sensitive eligibility information unless strictly necessary. Do not sell personal data. Clearly label sponsored placements, never rank a programme higher because it pays, and keep editorial verification independent from advertising or subscriptions.
