# Wave 1 Master-Visual QA Report

**Status:** PASS  
**Date:** 29 July 2026  
**Scope:** Capabilities overview, Digital Systems landing, Infrastructure landing  
**Production method:** Actual HTML, CSS and JavaScript prototypes rendered in Chromium with Playwright. No generated page image was used as the design source.

## Viewports tested

- 1672 × 941 desktop first viewport;
- full-page desktop capture;
- 1024 × 1366 tablet;
- 390 × 844 mobile first viewport;
- full-page mobile capture.

## Automated results

| Master template | Viewport | Horizontal overflow | H1 count | Images loaded | Mobile menu | Browser errors |
|---|---|---|---:|---|---|---|
| Capabilities overview | Desktop | PASS | 1 | PASS | N/A | PASS |
| Capabilities overview | Tablet | PASS | 1 | PASS | PASS | PASS |
| Capabilities overview | Mobile | PASS | 1 | PASS | PASS | PASS |
| Digital Systems landing | Desktop | PASS | 1 | PASS | N/A | PASS |
| Digital Systems landing | Tablet | PASS | 1 | PASS | PASS | PASS |
| Digital Systems landing | Mobile | PASS | 1 | PASS | PASS | PASS |
| Infrastructure landing | Desktop | PASS | 1 | PASS | N/A | PASS |
| Infrastructure landing | Tablet | PASS | 1 | PASS | PASS | PASS |
| Infrastructure landing | Mobile | PASS | 1 | PASS | PASS | PASS |

## Visual review

### Capabilities overview

- communicates the three-part operating model in the first viewport;
- gives Digital Systems and Infrastructure equal strategic weight;
- presents Technology Supply & Integration as the connecting delivery capability;
- uses structured capability matrices rather than an unrelated icon wall;
- retains the approved Techgrity utility bar, navigation, typography, navy, teal, ivory, card and CTA language;
- remains readable and structurally coherent on mobile.

### Digital Systems landing

- uses the approved lighter, workflow-led divisional expression;
- presents five distinct digital capability routes;
- uses human operational imagery and system architecture rather than robots or speculative interfaces;
- maintains credible institutional positioning rather than web-agency styling;
- remains readable and structurally coherent on mobile.

### Infrastructure landing

- uses stronger navy, technical photography and engineering structure;
- presents all six infrastructure capability categories;
- communicates assessment, design, integration, commissioning and support rather than construction or catalogue positioning;
- retains visual continuity with the approved homepage and Digital Systems page;
- remains readable and structurally coherent on mobile.

## Correction made during QA

Tablet horizontal overflow was found in the first render because desktop navigation remained active at 1024 px. The mobile-navigation breakpoint was moved to 1100 px, the three templates were re-rendered, and overflow and menu behaviour were re-tested successfully.

## Acceptance conclusion

**PASS — Wave 1 master visuals are suitable as implementation authority.**

The source prototypes, desktop/mobile/tablet references and approval records must remain tied to the exact branch and pull request that introduces them.