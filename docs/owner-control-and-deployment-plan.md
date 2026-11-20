# Owner control and deployment plan

Last reviewed: 2026-11-20

## Purpose

This document records a practical route toward keeping the Global Support Radar source code, deployment, domain, and commercial decisions under the project owner's control. It is a technical checklist, not a legal opinion or proof of ownership.

## Verified current state

- The GitHub repository is public: `mokus91/global-support-radar`.
- The default branch is `main`.
- GitHub Pages is enabled and the public site is served from this repository.
- The latest Pages deployment checked on 2026-11-20 (commit `8fb5ad9c`) completed successfully.
- The repository has a proprietary notice, ownership/IP notes, third-party notices, and a rights evidence log.
- The repository being public means others can view and fork it under GitHub's platform terms. A proprietary notice does not technically disable those platform capabilities.
- No paid domain, separate private source repository, external hosting migration, payment provider, or ad network is verified by this audit.

## Recommended target architecture

1. **Private source of truth:** keep the canonical development repository private and owner-administered.
2. **Public deployment only:** publish the built website to a separate deployment target. Do not publish source secrets, API keys, private declarations, customer data, or credentials.
3. **Owner-controlled accounts:** the project owner should be the sole account owner/admin for Git hosting, domain registrar, hosting, analytics, advertising, payment processing, and any business email. Add a trusted recovery method controlled by the owner.
4. **Protected production branch:** require review for changes, restrict who can push to the production branch, and keep an auditable release history.
5. **Backups:** maintain encrypted offline copies of source, data, workflow definitions, and deployment configuration. Test restoration periodically.
6. **Release process:** validate data and code, run automated tests, deploy, then perform a public-site smoke test. Keep the previous known-good release available for rollback.

## Safe migration sequence

Do not make the current repository private as a first step. On the current GitHub Free setup that can disable the existing Pages deployment.

Instead:
- Create and verify a private source repository controlled by the owner.
- Copy the complete project history or make a documented source snapshot; verify all expected files and recent commits.
- Select a deployment provider that supports deploying from a private source repository on a plan whose terms permit the intended commercial use.
- Configure deployment credentials as encrypted repository secrets; never commit them.
- Deploy a staging copy and test the site, data refresh, PWA, SEO, and rollback.
- Only after the replacement deployment is verified, decide whether to retire the public source repository or leave it as a public read-only mirror.
- Keep the public site available during migration; do not switch DNS or remove Pages until the replacement is working.

## Owner decision rights checklist

The owner should personally control:
- repository organization and administrator access;
- domain registration and DNS;
- hosting and deployment accounts;
- billing, advertising, subscription, and payment accounts;
- access recovery and multifactor authentication;
- approval of any sale, assignment, license, partnership, or transfer.

Technical account control is not the same as legal ownership. Legal ownership also depends on who created or contributed code, graphics, text, databases, and other protected material, plus the terms governing third-party data and software.

## No-cost measures available now

- Keep dated commits and release notes.
- Keep the rights evidence log current.
- Preserve source archives and checksums in a secure location.
- Record the origin and license/terms for every external dependency, icon, image, dataset, and API.
- Keep private identity details and signed declarations outside this public repository.
- Enable multifactor authentication and save recovery codes securely.

## Items still requiring owner action or verification

- Confirm the legal person or business that will own the economic rights and commercial accounts.
- Identify and document any third-party contributors and obtain appropriate written rights grants where needed.
- Verify the origin and reuse rights for all image/icon assets and every external dataset/API.
- Choose whether to create a separate private source repository and select a commercial-use-compatible deployment provider.
- Have any final ownership assignment or commercial contract reviewed by a qualified Hungarian IP lawyer if certainty is required.

## Explicit limitations

This plan does not establish exclusive ownership, prevent copying of a public repository, register a trademark, guarantee global data coverage, or guarantee revenue. No account visibility, hosting, billing, DNS, or legal status was changed by writing this plan.
