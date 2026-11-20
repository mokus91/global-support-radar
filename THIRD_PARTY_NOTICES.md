# Third-party materials and source obligations

**Audit date:** 2026-11-20  
**Repository reviewed:** `mokus91/global-support-radar`

This register records an initial repository-level audit. It is not a legal certification, and it must be updated whenever dependencies, assets, APIs, datasets, or external sources change.

## 1. Frontend and bundled assets

- `index.html`: the page uses inline HTML, CSS, and JavaScript. The reviewed markup did not show a remotely hosted JavaScript framework, CSS framework, web-font stylesheet, or third-party image URL. Recheck when the frontend changes.
- Fonts: the CSS uses a system font stack (Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial). No bundled font file was found in the repository tree. Installed system fonts remain subject to the operating system's own terms.
- `icon.svg`, `icon-192.png`, `icon-512-maskable.png`: project icon assets are present. The SVG contains simple geometric shapes and colours. The PNG files' creation provenance and any source artwork have not yet been independently documented. Keep original editable source files and dated evidence; replace any asset whose provenance or licence cannot be established.
- `manifest.webmanifest`, `sw.js`, `robots.txt`, `sitemap.xml`: project configuration files; review any external URLs or copied material before reuse.

## 2. Build and automation dependencies

The GitHub Actions workflows reference these third-party actions by version tag:
- `actions/checkout@v4`
- `actions/setup-python@v5`
- `actions/github-script@v7`

The source-discovery workflow installs direct Python dependencies from `requirements-ci.txt` with exact versions and SHA-256 wheel hashes: `certifi==2026.10.23` (MPL-2.0) and `pycountry==26.2.16` (LGPL-2.1-only). These packages and their licences are not owned by this project. The lock file covers these direct wheels only; it is not a complete transitive dependency lock or a legal licence clearance. Retain the corresponding licence texts and review transitive dependencies before production/commercial operation.

No `package.json`, npm/yarn/pnpm lockfile, `requirements*.txt`, or `pyproject.toml` was present in the reviewed repository tree. This does not prove that the runtime has no transitive or platform-provided dependencies.

## 3. External data sources and APIs

The application links to or processes government portals, public datasets, APIs, RSS feeds, and other external sources. Examples include EU institutions, national governments, Grants.gov, UKRI, Japan JGrants, Chilean public agencies, Australian ARC, Canadian CIHR, and Hungarian public portals.

The project does not claim ownership of:
- government information, official notices, public records, or third-party datasets;
- third-party databases or their protected selection/arrangement;
- external API services, RSS feeds, websites, names, logos, or trademarks.

Before redistributing or commercially reusing any source material, check and record:
- the source's licence and terms of use;
- attribution and citation requirements;
- database rights and commercial reuse conditions;
- API rate limits, authentication, and access restrictions;
- privacy and personal-data restrictions;
- retention, caching, and redistribution conditions.

A publicly accessible government webpage or dataset is not automatically free of all reuse conditions. A successful HTTP response does not establish permission to scrape, republish, or commercially exploit its contents.

## 4. Required follow-up

1. Establish and document the original creator/source and licence for both PNG icons.
2. Retain the licence texts for pinned `certifi` and `pycountry` versions, and review any transitive dependencies.
3. Review the licence and security provenance of each GitHub Action; pin actions to immutable commit SHAs for a hardened production workflow.
4. Maintain a source-by-source register for every API, dataset, RSS feed, and linked portal, including the date its commercial reuse terms were checked.
5. Add notices or attribution where the applicable licence requires them.

## 5. Rights boundary

The project may claim rights only in its own original code, documentation, graphics, and qualifying original selection or arrangement of information, subject to applicable law and evidence of authorship. Third-party materials remain subject to their respective owners' rights, licences, and terms.
