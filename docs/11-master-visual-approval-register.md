# Techgrity Systems Master-Visual Approval Register

**Status:** ACTIVE  
**Opened:** 29 July 2026

This register records the approval state of the 13 authoritative master page templates. Internal rendering and QA do not equal user design approval. A template becomes `APPROVED` only after the user has reviewed the designated desktop reference and explicitly accepted the design direction.

| # | Master template | Reference identity | Status | Approval date | Notes |
|---:|---|---|---|---|---|
| 1 | Homepage | reviewed desktop reference | `APPROVED` | 29 July 2026 | User reviewed the desktop design and directed the programme to continue. |
| 2 | Capabilities overview | `visuals/wave-1-reference-manifest.md` | `APPROVED` | 29 July 2026 | User reviewed the desktop design; responsive QA remains internal evidence. |
| 3 | Digital Systems landing | `visuals/wave-1-reference-manifest.md` | `APPROVED` | 29 July 2026 | User reviewed the desktop design; responsive QA remains internal evidence. |
| 4 | Digital capability detail | revised Software, AI & Enterprise Applications desktop reference | `APPROVED` | 29 July 2026 | Revised hero uses a credible operations team and enterprise interface. Final implementation must use natural scrolling and proper section height rather than the condensed review-board height. |
| 5 | Infrastructure landing | `visuals/wave-1-reference-manifest.md` | `APPROVED` | 29 July 2026 | User reviewed the desktop design; responsive QA remains internal evidence. |
| 6 | Infrastructure capability detail | Networks & Fibre desktop reference | `APPROVED` | 29 July 2026 | Approved with two controls: final implementation uses natural page height; informational sub-capability tiles have no arrows, pointer affordance or fake links unless a real destination exists. |
| 7 | Technology Supply & Integration | not produced | `NOT STARTED` | — | Wave 2 |
| 8 | Industries overview | not produced | `NOT STARTED` | — | Wave 3 |
| 9 | Industry detail | not produced | `NOT STARTED` | — | Wave 3 |
| 10 | How We Deliver | not produced | `NOT STARTED` | — | Wave 3 |
| 11 | Company | not produced | `NOT STARTED` | — | Wave 4 |
| 12 | Resources | not produced | `NOT STARTED` | — | Wave 4 |
| 13 | Contact and enquiry forms | not produced | `NOT STARTED` | — | Wave 4 |

## Approval evidence

- Wave 1 user decision: [`review-decisions/2026-07-29-wave-1-user-approval.md`](review-decisions/2026-07-29-wave-1-user-approval.md);
- Wave 2 detail-template decision: [`review-decisions/2026-07-29-wave-2-detail-template-approval.md`](review-decisions/2026-07-29-wave-2-detail-template-approval.md);
- Wave 1 internal QA report: [`../visuals/wave-1-qa-report.md`](../visuals/wave-1-qa-report.md);
- Wave 1 deterministic reference manifest: [`../visuals/wave-1-reference-manifest.md`](../visuals/wave-1-reference-manifest.md);
- Wave 1 prototype source: [`../visuals/prototypes/`](../visuals/prototypes/).

## User review protocol

The user is shown one desktop reference per master template. Mobile and tablet renders remain internal QA evidence and are not part of routine design approval unless the user specifically requests them.

A condensed review board may show the complete page in one image, but it never defines the final implementation height. Production pages use natural document flow, proper section spacing and normal scrolling.

## Interaction-affordance rule

- Navigational cards may use arrows, hover/focus treatment and pointer behaviour only when they link to a real planned route or approved in-page destination.
- Informational cards must not use arrows, pointer cursors, misleading hover lift or link styling.
- No dead card, fake control or destination-less tile may appear in production.

## Status values

- `NOT STARTED`
- `DRAFT`
- `READY FOR USER REVIEW`
- `REVISION REQUIRED`
- `APPROVED`
- `SUPERSEDED`

Implementation authority exists only when the relevant template status is `APPROVED` after explicit user review.