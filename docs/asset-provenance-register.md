# Asset provenance register

**Project:** Global Support Radar  
**Repository:** `mokus91/global-support-radar`  
**Review date:** 2026-11-20  
**Purpose:** Track the origin and reuse rights for every visual asset. This is an evidence register, not a legal clearance.

## Current inventory

| Asset | Current observation | Origin evidence | Reuse status | Required action |
|---|---|---|---|---|
| `icon.svg` | Newly written 512×512 vector app icon; magnifier plus motif, project colour palette | Created as AI-assisted code output for this project on 2026-11-20; prior unverified SVG was replaced | Current asset source is documented; legal copyright status is not guaranteed solely by AI generation | Retain this source file and this dated record; review legal status before granting exclusive rights |
| `icon-maskable.svg` | Newly written 512×512 vector maskable PWA icon; central artwork stays within a conservative safe area | Created as AI-assisted code output for this project on 2026-11-20 | Current asset source is documented; legal copyright status is not guaranteed solely by AI generation | Retain this source file and this dated record; review legal status before granting exclusive rights |
| `icon-192.png` | Former PNG app icon | Owner confirms they did not personally create it; origin and licence unknown | Removed from active project on 2026-11-20 | Excluded from the current application and licence delivery |
| `icon-512-maskable.png` | Former PNG maskable app icon | Owner confirms they did not personally create it; origin and licence unknown | Removed from active project on 2026-11-20 | Excluded from the current application and licence delivery |

## Required record for each future asset

Record all of the following before adding an asset:
1. Exact repository path and SHA-256 checksum.
2. Creator's legal name or organisation.
3. Creation date and original editable/source file location.
4. Whether the asset is original, AI-assisted, commissioned, or downloaded.
5. If third-party material is involved: exact source URL, author, licence name/version, attribution text, commercial-use permission, modification permission, and date the terms were checked.
6. If commissioned: signed agreement identifying the transferable economic rights or licence scope.
7. Evidence location kept privately; do not publish personal data, signatures, invoices, or confidential contracts.

## Important safeguards

- Do not label an asset "owned exclusively" merely because it is stored in this repository.
- A public-domain or government-origin image can still have separate logo, trademark, database, privacy, or source-specific restrictions.
- AI-assisted generation does not by itself settle copyright ownership; record the tool terms and human creative contribution.
- If provenance cannot be established, replace the asset with a newly created, documented original asset or one under a clearly suitable licence.
- Keep signed declarations and private evidence outside this public repository.

## Current conclusion

The owner confirmed that they did not personally create the previous icons. The two PNG files were removed from the active application and replaced by documented SVG source files written for this project with AI assistance. The prior SVG content was replaced. This records the current files' provenance but does not guarantee copyright protection or exclusivity under applicable law.


## 2026-11-20 replacement implementation

The current app uses `icon.svg` and `icon-maskable.svg`. Both are self-contained vector files written directly for this project as AI-assisted development output. The PWA manifest and service-worker shell cache now reference these SVG files. The old PNG files were deleted from the current branch, and the homepage no longer advertises them as Apple-touch or social-preview images.

The ten translated landing pages were checked and contained no references to the removed PNG files. The homepage, manifest and service worker were updated. Browser installation, iOS home-screen appearance, maskable cropping and social-preview rendering still require device/browser testing. No claim is made that SVG icons provide a raster social preview; a separately documented raster export can be added later if needed.
