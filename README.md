# Global Support Radar

**Live site:** https://mokus91.github.io/global-support-radar/

A mobile-friendly Hungarian/English directory and discovery search for official public grants, benefits and support programmes.

## What is live now

- Responsive website with Hungarian and English interface.
- Country selector with ISO country codes. Selecting a country does **not** mean that every country's programmes are automatically indexed.
- Ten search categories: housing, family, agriculture, business, education, healthcare, energy, employment, social support and transport.
- Main search currently reads discovery records from three working official data connections:
  - European Commission Funding & Tenders Portal (EU)
  - Grants.gov (United States)
  - UKRI opportunity feed (United Kingdom)
- Separate Australian Research Council research-grant archive panel. These records are historical/discovery data and are not presented as open calls.
- Hungarian official starting points for family support, housing, agriculture, civil/community grants, scholarships and research/innovation calls.
- Automatic discovery of NKFIH grant-news items from its official RSS feed. These remain unverified news candidates, not confirmed open calls.
- 47 entries in the official source registry, with country/subject coverage notes.
- Daily automated refresh scheduled for 04:17 UTC; manual GitHub Actions run is also configured.
- Official source links are checked against allowed hostnames before being displayed.

## Important coverage and verification limits

This is a working MVP, **not yet a complete worldwide grants database**. The country selector is broader than the current automated data coverage. The live search is currently concentrated on EU, US and UK records. The Canadian CIHR RSS adapter is kept as a separate source panel rather than part of the main search; the latest successful retrieval returned zero items, which does not mean that Canada has no funding opportunities. Hungarian pages are mostly official starting points rather than a complete automated live grant feed. The NKFIH RSS adapter adds research/innovation grant-news candidates, but does not verify whether an item is still open.

Automatically discovered records are labelled **unverified candidates**. They are not a promise that an opportunity is open, that its deadline is current, or that a particular visitor is eligible. Some records have no deadline. Always open the official notice and confirm eligibility, dates, amounts and application procedure with the publisher.

Historical award databases, discovery-source directories and open calls are intentionally kept distinct. A past grant award or a dataset mentioning benefits is not a currently available support programme.

The site does not submit applications, make eligibility decisions, collect sensitive personal information, or guarantee funding.

## Repository layout

- `index.html` — responsive frontend and search/filter logic.
- `data/source-registry.json` — official source directory.
- `data/programme.schema.json` — normalized record schema and verification states.
- `data/*-discovery.json` — generated source discovery records.
- `scripts/` — official API/feed adapters.
- `.github/workflows/source-discovery.yml` — daily scheduled discovery and manual run.
- `docs/architecture.md` — architecture and verification principles.

## Automated discovery sources

| Source | Use | Important limitation |
| --- | --- | --- |
| EU Funding & Tenders | Calls and competitive opportunities | Candidate status must be checked on the official topic page |
| Grants.gov | Posted and forecast US federal opportunities | Many are restricted to eligible organisations; forecast items are not open calls |
| UKRI | Recent UKRI opportunity feed entries | Feed is not a complete listing and may omit deadlines |
| CIHR | Canadian health-research RSS notices | Latest successful retrieval returned zero items; narrow health-research coverage only |
| Australian ARC | Research grant records | Archive/discovery records, not a general Australian benefits feed |
| Hungarian official portals | FAIR, KAP, family/housing support, BGA, EMET and other official starting points | Most are direct links; NKFIH RSS imports unverified grant-news candidates only |

## Run locally

Python 3.12 is used by the discovery workflow. The Hungarian open-data and Canadian adapters use the `certifi` CA bundle installed by the workflow.

```bash
python -m pip install certifi
python scripts/discover_eu_funding.py
python scripts/discover_us_grants.py
python scripts/discover_ukri.py
python scripts/discover_au_arc_grants.py
python scripts/discover_ca_cihr.py
python scripts/discover_hu_open_data.py
python scripts/discover_hu_nkfih.py
```

## Verification policy

A record may only be marked `open-and-current` after its original official page has been checked for:
1. publisher authenticity and working official URL;
2. current application status and deadline;
3. country/region and eligible applicant groups;
4. support type, amount and currency where stated;
5. application route and conditions.

The current automated adapters perform **discovery**, not full page-by-page eligibility verification. Until that verification pipeline is implemented, records remain unverified.

## Privacy and monetization

The current MVP does not require accounts or personal eligibility profiles. Do not collect sensitive eligibility information unless strictly necessary. Never sell personal data. Any future sponsored placements must be clearly labelled and must not influence verification or organic ranking.
