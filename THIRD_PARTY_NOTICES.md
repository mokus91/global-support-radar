# Third-party materials and source obligations

**Audit date:** 2026-11-20  
**Repository reviewed:** `mokus91/global-support-radar`

This register records an initial repository-level audit. It is not a legal certification, and it must be updated whenever dependencies, assets, APIs, datasets, or external sources change.

## 1. Frontend and bundled assets

- `index.html`: the page uses inline HTML, CSS, and JavaScript. The reviewed markup did not show a remotely hosted JavaScript framework, CSS framework, web-font stylesheet, or third-party image URL. Recheck when the frontend changes.
- Fonts: the CSS uses a system font stack (Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial). No bundled font file was found in the repository tree. Installed system fonts remain subject to the operating system's own terms.
- `icon.svg`, `icon-192.png`, `icon-512-maskable.png`: project icon assets are present. The owner confirms they did not personally create these icons. Their original creator/source and commercial reuse permissions are unverified. Do not represent them as owner-created or include them as owner-owned assets in a paid delivery unless the source and permission are established; otherwise replace them with documented assets.
- `manifest.webmanifest`, `sw.js`, `robots.txt`, `sitemap.xml`: project configuration files; review any external URLs or copied material before reuse.

## 2. Build and automation dependencies

The GitHub Actions workflows use these third-party actions, pinned to immutable commit SHAs:
- `actions/checkout` pinned to commit `11d5960a326750d5838078e36cf38b85af677262` (v4.4.0)
- `actions/setup-python` pinned to commit `a26af69be951a213d495a4c3e4e4022e16d87065` (v5.5.0)
- `actions/github-script` pinned to commit `f28e40c7f34bde8b3046d885e986cb6290c5673b` (v7.1.0)
- `actions/upload-artifact` pinned to commit `ea165f8d65b6e75b540449e92b4886f43607fa02` (v4 release line)

All workflow references found in `.github/workflows/` were changed from movable version tags to immutable commit SHAs on 2026-11-20. The version labels above are human-readable release references; the commit SHA is the actual pin. This improves reproducibility but does not replace ongoing security and licence review.

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
3. The current GitHub Action references have been pinned to immutable commit SHAs. Still review each action's licence, transitive dependencies, security advisories and compatibility before production; update pins deliberately when adopting newer releases.
4. Maintain a source-by-source register for every API, dataset, RSS feed, and linked portal, including the date its commercial reuse terms were checked.
5. Add notices or attribution where the applicable licence requires them.

## 5. Rights boundary

The project may claim rights only in its own original code, documentation, graphics, and qualifying original selection or arrangement of information, subject to applicable law and evidence of authorship. Third-party materials remain subject to their respective owners' rights, licences, and terms.
