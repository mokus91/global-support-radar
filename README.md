# Global Support Radar

**Live site:** https://mokus91.github.io/global-support-radar/

A mobile-friendly Hungarian/English directory and discovery search for official public grants, benefits and support programmes.

## What is live now

- Responsive website with Hungarian and English interface.
- Country selector covering the ISO country-code list, localized into Hungarian or English.
- Worldwide support finder for every country selection, linking to the UN national e-government portal directory (193 UN Member States), ILO social-protection country profiles and the World Bank ASPIRE database (about 140 countries).
- The worldwide finder is a global official-source navigator, not a claim that individual benefit programmes are already indexed or that live automated feeds exist for every country.
- Ten search categories: housing, family, agriculture, business, education, healthcare, energy, employment, social support and transport.
- Main search currently reads discovery records from three working official data connections:
  - European Commission Funding & Tenders Portal (EU)
  - Grants.gov (United States)
  - UKRI opportunity feed (United Kingdom)
- Separate Australian Research Council research-grant archive panel. These records are historical/discovery data and are not presented as open calls.
- Hungarian official starting points for family support, maternity allowance, family allowance, GYES/GYET, housing, local social support, large-family gas discount, agriculture, civil/community grants, scholarships and research/innovation calls.
- Curated Hungarian household-support directory with eight official information entries, including direct GYES and GYET pages.
- Browser-only Hungarian support guide: users can optionally select broad household circumstances to see which official benefit pages may be relevant. Answers are processed locally and are not sent to the server or stored. It distinguishes central benefits from municipality-specific assistance and does not claim eligibility or current availability.
- Automatic discovery of NKFIH grant-news items from its official RSS feed. These remain unverified news candidates, not confirmed open calls.
- 68 entries in the official source registry, with country/subject coverage notes.
- Official European Commission directory of national EU-funding portals for all 27 EU Member States; the worldwide finder displays the selected country's portal, or all 27 when no country is selected. These are shared-management EU-fund portals, not a complete household-benefit catalogue.
- Six additional EU-wide official category directories for social inclusion/employment/education, agriculture/CAP, business finance and direct EU calls; relevant links are filtered by the selected support category.
- Country-specific European Commission/MISSOC social security guides for all 27 EU Member States, filtered by selected country and family/social/employment/healthcare categories.
- Official SME funding and support directories, including the European Commission Access to Finance and SME support tools.
- Verified national business funding databases for France and Germany; other EU countries continue to use their national EU funding portal until a dedicated national business database is verified.
- `data/europe-category-directories.json` — official EU-wide category-specific support and finance directories.
- `data/eu-social-protection-country-pages.json` — official MISSOC/European Commission country guides for all 27 EU Member States.
- `data/eu-national-business-funding.json` — verified national business funding databases for France and Germany.
- `data/eu-aid-award-transparency.json` — official EU and national registers of aid already awarded (not open applications).
- Daily automated refresh scheduled for 04:17 UTC; manual GitHub Actions run is also configured.
- Official source links are checked against allowed hostnames before being displayed.

## Important coverage and verification limits

This is a working MVP, **not yet a complete worldwide grants database**. The country selector and worldwide source navigator can be used globally, but they do not imply a complete country-by-country benefits catalogue. The country selector is broader than the current automated data coverage. The live automated search is currently concentrated on EU, US and UK records. The global finder provides official navigation resources for other countries rather than inventing local programme listings. The Canadian CIHR RSS adapter is kept as a separate source panel rather than part of the main search; the latest successful retrieval returned zero items, which does not mean that Canada has no funding opportunities. Hungarian pages are mostly official starting points rather than a complete automated live grant/benefit feed. A curated household-support directory links to eight official information pages, but does not calculate eligibility or assert that a benefit is currently open. Municipal assistance varies by local decree. The NKFIH RSS adapter adds research/innovation grant-news candidates, but does not verify whether an item is still open. The NKFIH RSS adapter adds research/innovation grant-news candidates, but does not verify whether an item is still open.

Automatically discovered records are labelled **unverified candidates**. They are not a promise that an opportunity is open, that its deadline is current, or that a particular visitor is eligible. Some records have no deadline. Always open the official notice and confirm eligibility, dates, amounts and application procedure with the publisher.

Historical award databases, discovery-source directories and open calls are intentionally kept distinct. A past grant award or a dataset mentioning benefits is not a currently available support programme.

The site does not submit applications, make eligibility decisions, collect sensitive personal information, or guarantee funding.

## Repository layout

- `index.html` — responsive frontend and search/filter logic.
- `data/source-registry.json` — official source directory (68 entries).
- `data/europe-national-portals.json` — European Commission-listed national funding portals for all 27 EU Member States.
- `data/global-support-directory.json` — worldwide official government portal and social-protection reference directories.
- `data/hu-household-support.json` — curated Hungarian household-support information directory (not a live eligibility feed).
- Browser-only support guide in `index.html` — preliminary suggestions only; no personal answers are transmitted or saved.
- `data/programme.schema.json` — normalized record schema and verification states.
- `data/*-discovery.json` — generated source discovery records, including daily EU CAP Network agriculture call leads in `data/eu-cap-network-discovery.json`.
- `scripts/` — official API/feed adapters.
- `.github/workflows/source-discovery.yml` — daily scheduled discovery and manual run.
- `docs/architecture.md` — architecture and verification principles.

## Automated discovery sources

| Source | Use | Important limitation |
| --- | --- | --- |
| EU Funding & Tenders | Calls and competitive opportunities | Candidate status must be checked on the official topic page |
| EU CAP Network | Agriculture, forestry and rural innovation call leads | Daily page monitoring; every lead remains unverified until checked on the original call page |
| Grants.gov | Posted and forecast US federal opportunities | Many are restricted to eligible organisations; forecast items are not open calls |
| UKRI | Recent UKRI opportunity feed entries | Feed is not a complete listing and may omit deadlines |
| CIHR | Canadian health-research RSS notices | Latest successful retrieval returned zero items; narrow health-research coverage only |
| Australian ARC | Research grant records | Archive/discovery records, not a general Australian benefits feed |
| Hungarian official portals | FAIR, KAP, family and maternity benefits, housing, municipal social assistance, energy discounts, BGA, EMET and NKFIH | Household benefits are curated official information links; NKFIH RSS imports unverified news candidates. No nationwide automated entitlement check exists. |

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
