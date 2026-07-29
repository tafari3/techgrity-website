# Techgrity Systems Master-Visual Approval Register

**Status:** ACTIVE  
**Opened:** 29 July 2026

This register records the approval state of the 13 authoritative master page templates. Internal rendering and QA do not equal user design approval. A template becomes `APPROVED` only after the user has reviewed the designated desktop reference and explicitly accepted the design direction.

| # | Master template | Reference identity | Status | Approval date | Notes |
|---:|---|---|---|---|---|
| 1 | Homepage | existing verified desktop reference | `READY FOR USER REVIEW` | — | Technically rendered and checked; user has not yet reviewed it. |
| 2 | Capabilities overview | `visuals/wave-1-reference-manifest.md` | `READY FOR USER REVIEW` | — | Internal desktop/tablet/mobile QA passed; user review is desktop-only. |
| 3 | Digital Systems landing | `visuals/wave-1-reference-manifest.md` | `READY FOR USER REVIEW` | — | Internal desktop/tablet/mobile QA passed; user review is desktop-only. |
| 4 | Digital capability detail | not produced | `NOT STARTED` | — | Wave 2 |
| 5 | Infrastructure landing | `visuals/wave-1-reference-manifest.md` | `READY FOR USER REVIEW` | — | Internal desktop/tablet/mobile QA passed; user review is desktop-only. |
| 6 | Infrastructure capability detail | not produced | `NOT STARTED` | — | Wave 2 |
| 7 | Technology Supply & Integration | not produced | `NOT STARTED` | — | Wave 2 |
| 8 | Industries overview | not produced | `NOT STARTED` | — | Wave 3 |
| 9 | Industry detail | not produced | `NOT STARTED` | — | Wave 3 |
| 10 | How We Deliver | not produced | `NOT STARTED` | — | Wave 3 |
| 11 | Company | not produced | `NOT STARTED` | — | Wave 4 |
| 12 | Resources | not produced | `NOT STARTED` | — | Wave 4 |
| 13 | Contact and enquiry forms | not produced | `NOT STARTED` | — | Wave 4 |

## Wave 1 internal evidence

- internal QA report: [`../visuals/wave-1-qa-report.md`](../visuals/wave-1-qa-report.md);
- deterministic reference manifest: [`../visuals/wave-1-reference-manifest.md`](../visuals/wave-1-reference-manifest.md);
- prototype source: [`../visuals/prototypes/`](../visuals/prototypes/);
- review status correction: [`../visuals/wave-1-approval.md`](../visuals/wave-1-approval.md).

## User review protocol

The user will be shown exactly one desktop reference per master template. Mobile and tablet renders remain internal QA evidence and are not part of routine design approval unless the user specifically requests them.

## Status values

- `NOT STARTED`
- `DRAFT`
- `READY FOR USER REVIEW`
- `REVISION REQUIRED`
- `APPROVED`
- `SUPERSEDED`

Implementation authority exists only when the relevant template status is `APPROVED` after explicit user review.