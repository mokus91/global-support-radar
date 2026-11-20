# Global Support Radar — preliminary rights and licensing audit

**Review date:** 2026-11-20  
**Repository:** `mokus91/global-support-radar`  
**Status:** preliminary technical/documentary review; not a legal opinion or a certification of ownership.

## Executive summary

The project can continue toward a carefully limited, non-exclusive licence, but it is **not ready for an unconditional commercial licence listing**. The human owner supplied the concept, product direction, requirements, and development decisions; ChatGPT assisted with implementation and generated code and documentation. The project should therefore be described transparently as a human-directed, AI-assisted software project.

OpenAI's Terms of Use effective 2026-01-01 state that, as between the user and OpenAI and to the extent permitted by applicable law, the user owns Output and OpenAI assigns any rights it may have in that Output. The same terms state that outputs may not be unique. This contractual allocation does not itself determine whether a particular output qualifies for copyright protection under Hungarian or EU law, nor does it grant rights in third-party content.

## Findings and actions

| Area | Finding | Status | Required action before licensing |
|---|---|---|---|
| Human project direction | Owner states that the concept and requirements came from them; AI assisted implementation | Disclosed; evidence should be preserved | Keep dated requirements, conversations, review/acceptance notes and original human-created materials privately |
| AI-generated code and text | OpenAI terms allocate Output to the user as between user and OpenAI, subject to applicable law; copyright protection remains a separate legal question | Needs legal review | Do not claim every AI-generated line is exclusively copyright-protected; have counsel review the licence scope |
| Other human contributors | No additional contributor is identified in the owner's statement in this conversation | Not independently verified | Confirm privately whether any designer, developer, translator, contractor or other person contributed |
| SVG icons | The previous unverified SVG was replaced with `icon.svg` and `icon-maskable.svg`, written as AI-assisted project assets on 2026-11-20 | Current asset source is documented; AI generation does not itself guarantee copyright protection or exclusivity | Keep provenance records; test PWA/browser rendering; obtain legal review before promising exclusive rights |
| PNG icons | Previous `icon-192.png` and `icon-512-maskable.png` had unknown origin and were removed from the active repository on 2026-11-20 | No longer referenced by the current manifest or service-worker shell | Keep excluded from any licence delivery; check historical commits only if a full archival cleanup is required |
| Python dependencies | `certifi==2026.10.23` (MPL-2.0) and `pycountry==26.2.16` (LGPL-2.1-only) are version- and wheel-hash-pinned in `requirements-ci.txt`; PyPI metadata confirms the stated licence expressions | Direct packages identified; licence texts/notices and transitive dependency review remain incomplete | Retain the exact licence texts/notices and review package contents, data licensing and transitive dependencies before commercial delivery |
| GitHub Actions | Detected checkout, setup-python, github-script and upload-artifact workflow references are now pinned to immutable commit SHAs | SHA pinning completed on 2026-11-20; action licence/security review remains ongoing | Preserve the pins and update only after reviewing target releases, compatibility and security notes |
| External data and APIs | Government, EU, UN and other sources are linked to or queried | Source-specific terms not comprehensively checked | Maintain per-source commercial reuse, attribution, database-right, API and caching review |
| Public repository | Repository is public and may be viewed/forked under GitHub terms | Known commercial limitation | Do not promise secrecy or exclusive source access; plan private source delivery and separate hosting only after owner approval |
| Product readiness | README describes an MVP with incomplete geographic coverage and unverified opportunity leads | Beta/MVP | Describe limits clearly; no guarantees of completeness, eligibility, accuracy, revenue or uptime |

## Important legal distinction

Hungary's Act LXXVI of 1999 protects qualifying original works, including computer programs and their documentation. The statutory test concerns individual, original character deriving from intellectual activity. A product idea, general function, business model, factual data, or feature wish-list is not automatically protected expression.

The OpenAI Terms of Use effective 2026-01-01 allocate Output to the user as between the user and OpenAI, to the extent permitted by applicable law. They also warn that outputs may be similar or non-unique. This does not turn every generated output into a copyright-protected work, establish exclusive rights against all third parties, or clear third-party materials.

## Recommended licensing boundary

Until a Hungarian intellectual-property lawyer reviews the project, any customer licence should be limited to:
- project materials and human-authored contributions for which the owner can substantiate the relevant rights;
- AI-assisted outputs only to the extent they can lawfully be licensed and are not third-party output or third-party material;
- no government data, external database, logo, trademark, API, third-party package, image or icon beyond the relevant source licence;
- no promise that the public GitHub source is confidential or exclusive.

A non-exclusive licence can preserve the owner's ability to license the same verified rights to other customers. The final contract must identify the exact files/version and exclude all third-party materials and unverified assets.

## Next steps in order

1. Owner privately confirms the contributor history and preserves dated project instructions and review evidence.
2. Icon replacement is complete at source level; verify PWA installation and rendering on real devices.
3. Complete a source-by-source data/API reuse register and dependency notice bundle.
4. GitHub Actions SHA pinning is complete; keep pins updated only through deliberate security and compatibility review.
5. Prepare a clean, versioned delivery bundle with a file manifest and SHA-256 hashes.
6. Ask a Hungarian copyright lawyer to review the AI-assisted development disclosure, rights chain and customer licence before taking payment.
7. Only after these gates: approve the marketplace listing, price, payment setup and publication separately.

## Official references reviewed

- Hungarian Act LXXVI of 1999 on Copyright, consolidated text effective 2026-01-01: https://njt.jog.gov.hu/jogszabaly/1999-76-00-00
- European Commission IP Helpdesk, Europe FAQ on AI-generated outputs: https://intellectual-property-helpdesk.ec.europa.eu/regional-ip-helpdesks/european-ip-helpdesk/europe-frequently-asked-questions_en
- OpenAI Terms of Use, effective 2026-01-01: https://openai.com/policies/terms-of-use/

**Conclusion:** continue preparing the project for non-exclusive licensing, but do not publish a claim of exclusive ownership over every file or sell the current repository as a fully cleared, private, production-ready software package.


## 2026-11-20 follow-up: automation and dependency review

The ten workflow files under `.github/workflows/` were inspected for third-party `uses:` references. The detected actions were pinned to immutable commit SHAs:
- checkout v4.4.0 — `11d5960a326750d5838078e36cf38b85af677262`
- setup-python v5.5.0 — `a26af69be951a213d495a4c3e4e4022e16d87065`
- github-script v7.1.0 — `f28e40c7f34bde8b3046d885e986cb6290c5673b`
- upload-artifact v4 release line — `ea165f8d65b6e75b540449e92b4886f43607fa02`

The pinning changes only the action reference format and preserves the corresponding release commits. The workflows have not been executed as part of this documentation/code review; a successful live run must still be confirmed in GitHub Actions.

The direct Python dependency versions and SHA-256 hashes were checked against the repository lock file and public package metadata. This confirms the declared direct-package versions and licence expressions, not the full transitive dependency graph or all licence obligations. Licence texts/notices and a transitive dependency inventory remain outstanding.

The `source-discovery.yml` workflow has write permissions because it commits refreshed discovery indexes and may open an issue on failure. The beta feedback statistics workflow has contents-write permission to update an aggregate JSON file. These permissions appear consistent with their stated jobs, but should be revisited if either workflow is expanded. The `organization-report-production.yml` workflow uses `workflow_run` but checks out the default repository revision rather than executing an untrusted pull-request checkout; continue to avoid introducing untrusted PR code into privileged workflows.


## 2026-11-20 follow-up: icon replacement

The two unknown-origin PNG app icons were deleted from the current branch. The previous SVG was replaced. New self-contained vector files `icon.svg` and `icon-maskable.svg` were written for the project with AI assistance and recorded in the asset provenance register. The PWA manifest now references the new SVG files; the service worker shell cache was bumped from v2 to v3 and now precaches the SVG icons. The homepage's Apple-touch and social-preview references to the unknown PNGs were removed.

The ten translated landing pages (ar, de, en, es, fr, hi, it, pt, ru, zh-cn) were checked and did not contain references to the retired PNG files. The source-level update is complete, but no real-device PWA install test or social-platform preview test has been performed. A raster social-preview asset may be added later with its own documented provenance if needed.
