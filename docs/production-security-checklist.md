# Production security and owner-control checklist

**Project:** Global Support Radar  
**Review date:** 2026-11-20  
**Status:** Preparation checklist; not a certification.

## Verified repository facts

- Canonical repository currently reviewed: `mokus91/global-support-radar`.
- Repository visibility: public.
- Default branch: `main`.
- The repository includes a proprietary notice and ownership / third-party-rights documentation.
- The source-discovery workflow uses scheduled GitHub Actions and writes refreshed data to the repository.
- The current GitHub Pages site is deployed from the public repository.

## Do not change without explicit owner approval

- Do not make the repository private while relying on GitHub Free Pages; this can take the live site offline.
- Do not change DNS, hosting, billing, repository ownership, account email, or recovery methods.
- Do not delete the public site or its data.
- Do not publish identity documents, signed declarations, private contracts, API secrets, access tokens, or recovery codes.

## Owner actions to complete privately

- [ ] Enable multi-factor authentication on the GitHub account.
- [ ] Save recovery codes offline in a secure location.
- [ ] Verify the recovery email and phone are controlled by the owner.
- [ ] Download a full repository backup and keep a second encrypted copy outside GitHub.
- [ ] Verify that the owner controls the domain registrar and DNS, if a custom domain is registered.
- [ ] Keep hosting, analytics, advertising, payment, and business email accounts under owner-controlled credentials.
- [ ] Keep all API keys and deployment secrets in the provider's encrypted secret store, never in source files.
- [ ] Record all human contributors and obtain suitable written agreements where needed.
- [ ] Complete the asset and dependency licence registers before commercial launch.

## Technical hardening still required

- Review every workflow action and pin third-party Actions to immutable commit SHAs after checking publisher provenance.
- Review direct and transitive Python dependencies, preserve licence texts, and schedule controlled updates.
- Add a staging deployment and a documented rollback procedure before migrating away from GitHub Pages.
- Add monitoring for failed data refreshes and stale feeds; ensure alerts do not imply that a failed endpoint means a programme has closed.
- Review data-source terms individually before storing, translating, caching, or commercially redistributing records.
- Perform a privacy and security review before adding accounts, subscriptions, user profiles, or payment processing.

## Migration target

The intended architecture is a private, owner-controlled source repository plus a separate public deployment target. Migration should occur only after a full backup, a successful staging deployment, automated data-refresh verification, and a tested rollback. Keep the current public site online until the replacement is confirmed.

## Decision boundary

This checklist records technical controls and owner intentions. It does not prove copyright ownership, create legal exclusivity, or replace contracts with contributors or third-party providers. Any sale, licence, assignment, domain transfer, or paid-service activation remains subject to the owner's explicit decision.
