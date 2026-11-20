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
| SVG icon | Owner confirms they did not personally create the project icons; the SVG's original creator/source is not established | Unverified provenance; not cleared for resale/licensing | Identify the original source and permission, or replace it with a newly documented project asset before including it in a paid delivery |
| PNG icons | Owner confirms they did not personally create the project icons; the source artwork/export history for `icon-192.png` and `icon-512-maskable.png` is not established | Unverified provenance; not cleared for resale/licensing | Identify source and permission or replace both; do not represent as exclusively owned meanwhile |
| Python dependencies | `certifi` and `pycountry` are pinned in `requirements-ci.txt`; register records MPL-2.0 and LGPL-2.1-only respectively | Third-party components identified, not fully cleared | Include applicable licence texts/notices, review package and transitive dependency obligations |
| GitHub Actions | Workflow uses `actions/checkout@v4`, `actions/setup-python@v5`, `actions/github-script@v7` tags | Version tags identified; immutable provenance not pinned | Review action licences/security and pin immutable commit SHAs before hardened commercial delivery |
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
2. Replace or document the PNG icons and SVG source.
3. Complete a source-by-source data/API reuse register and dependency notice bundle.
4. Review and pin GitHub Actions to immutable commit SHAs.
5. Prepare a clean, versioned delivery bundle with a file manifest and SHA-256 hashes.
6. Ask a Hungarian copyright lawyer to review the AI-assisted development disclosure, rights chain and customer licence before taking payment.
7. Only after these gates: approve the marketplace listing, price, payment setup and publication separately.

## Official references reviewed

- Hungarian Act LXXVI of 1999 on Copyright, consolidated text effective 2026-01-01: https://njt.jog.gov.hu/jogszabaly/1999-76-00-00
- European Commission IP Helpdesk, Europe FAQ on AI-generated outputs: https://intellectual-property-helpdesk.ec.europa.eu/regional-ip-helpdesks/european-ip-helpdesk/europe-frequently-asked-questions_en
- OpenAI Terms of Use, effective 2026-01-01: https://openai.com/policies/terms-of-use/

**Conclusion:** continue preparing the project for non-exclusive licensing, but do not publish a claim of exclusive ownership over every file or sell the current repository as a fully cleared, private, production-ready software package.
