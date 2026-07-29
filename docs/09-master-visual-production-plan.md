# Techgrity Systems Master-Visual Production Plan

**Status:** READY FOR EXECUTION  
**Version:** 1.0  
**Date:** 29 July 2026  
**Depends on:** [`03-visual-design-system.md`](03-visual-design-system.md), [`04-image-art-direction-brief.md`](04-image-art-direction-brief.md), [`08-visual-functional-acceptance-checklist.md`](08-visual-functional-acceptance-checklist.md)

## 1. Purpose

This plan defines how the remaining 12 authoritative master-page visuals will be produced, reviewed and approved before implementation. It prevents visual work from becoming a disconnected series of page mock-ups and preserves the approved homepage as the controlling quality benchmark.

## 2. Governing principle

The website will be designed as one reusable system, not as 31 unrelated pages.

Each master visual must prove:

- page-family hierarchy;
- component reuse;
- desktop and mobile behaviour;
- image and diagram direction;
- content density;
- conversion path;
- accessibility considerations;
- relationship to the approved homepage.

## 3. Master visual inventory

The homepage is already the approved master template.

The remaining 12 master visuals are:

1. Capabilities overview;
2. Digital Systems landing;
3. Digital capability detail;
4. Infrastructure landing;
5. Infrastructure capability detail;
6. Technology Supply & Integration;
7. Industries overview;
8. Industry detail;
9. How We Deliver;
10. Company;
11. Resources;
12. Contact and enquiry forms.

## 4. Production sequence

### Wave 1 — Corporate structure

1. Capabilities overview;
2. Digital Systems landing;
3. Infrastructure landing.

Purpose: establish how the two specialist divisions and integrated delivery capability are expressed across internal pages.

### Wave 2 — Capability detail systems

4. Digital capability detail;
5. Infrastructure capability detail;
6. Technology Supply & Integration.

Purpose: prove the reusable structure for all capability pages, including scope, deliverables, diagrams, delivery stages, related industries and CTAs.

### Wave 3 — Sector and delivery narrative

7. Industries overview;
8. Industry detail;
9. How We Deliver.

Purpose: prove sector relevance, integrated solution maps and the Discover-to-Support lifecycle.

### Wave 4 — Corporate evaluation and conversion

10. Company;
11. Resources;
12. Contact and enquiry forms.

Purpose: complete corporate credibility, tender-document access and qualified enquiry flows.

## 5. Required output per master template

Every master template requires:

- one desktop composition at 1672 × 941 or a documented equivalent reference viewport;
- one mobile composition at 390 × 844;
- a tablet behaviour note at 768 × 1024 and 1024 × 1366;
- final section order and visible copy hierarchy;
- image subject and crop decisions;
- diagram or graphic specification;
- reusable component inventory;
- accessibility notes;
- implementation notes;
- approval status and date.

Long pages may use stitched full-page references in addition to the first-viewport frame. The first viewport remains mandatory because it proves proposition, page context and CTA hierarchy.

## 6. Review method

Each master visual will be reviewed against:

1. the locked page objective and section order;
2. the approved homepage visual benchmark;
3. the visual design system;
4. the image and art-direction brief;
5. desktop and mobile usability;
6. accessibility risks;
7. content realism and factual boundaries;
8. implementation feasibility;
9. reuse across every page in the family.

A visual is not approved merely because it is attractive. It must be structurally correct, technically plausible, reusable and implementable.

## 7. Approval statuses

| Status | Meaning |
|---|---|
| `DRAFT` | initial composition; not implementation authority |
| `REVIEW` | complete enough for structured comparison |
| `REVISION REQUIRED` | known material issues remain |
| `APPROVED` | desktop and mobile references accepted as implementation authority |
| `SUPERSEDED` | replaced by a later approved version |

Only `APPROVED` visuals may govern implementation.

## 8. Reference asset structure

Approved visual evidence should be stored under:

```text
visuals/
  homepage/
  capabilities-overview/
  digital-systems-landing/
  digital-capability-detail/
  infrastructure-landing/
  infrastructure-capability-detail/
  technology-supply/
  industries-overview/
  industry-detail/
  how-we-deliver/
  company/
  resources/
  contact-enquiry/
```

Each folder should contain, as applicable:

```text
README.md
reference-desktop.png
reference-mobile.png
reference-tablet-notes.md
asset-register.md
approval.md
```

Source design files may be stored or linked according to the selected design workflow, but exported approved references must remain versioned and reviewable in the repository.

## 9. Component decisions to prove during visual production

Across the 12 visuals, the following components must be finalised:

- internal-page utility bar and header behaviour;
- breadcrumb treatment;
- internal hero variants;
- section labels and heading hierarchy;
- capability matrix;
- division pathway cards;
- capability detail cards;
- industry cards;
- delivery lifecycle;
- architecture and solution diagrams;
- related-content navigation;
- credibility and evidence panels;
- document cards;
- form controls and validation states;
- final CTA system;
- corporate footer;
- 404 and confirmation-state treatment.

## 10. Copy and factual controls

Visual production may use approved content-specification copy. Where a fact remains blocked:

- use an explicit internal placeholder label;
- do not make the placeholder look like approved public copy;
- do not invent a number, address, partner, certification, client or project;
- record the dependency in the visual's README or approval file.

Visuals may use representative project patterns only when clearly framed as examples.

## 11. Image production controls

- no new image is accepted without a communication purpose;
- desktop and mobile crops must be produced together;
- infrastructure imagery receives technical plausibility review;
- representative people are not labelled as Techgrity employees;
- generated images are recorded as generated and never treated as project evidence;
- visible third-party brands require deliberate approval;
- all final assets enter the asset register.

## 12. Implementation handoff condition

A page family is ready for implementation only when:

- its master visual is `APPROVED`;
- desktop and mobile references exist;
- required components are identified;
- final copy and factual dependencies are clear;
- image assets and crops are approved or explicitly tracked;
- diagrams have text equivalents;
- responsive behaviour is documented;
- no unresolved visual issue would require redesigning the shared component system.

## 13. Completion condition for the visual stage

The visual stage is complete only when all 13 master templates, including the existing homepage, have:

- approved desktop and mobile references;
- recorded image and diagram decisions;
- reusable component mapping;
- accessibility notes;
- approval evidence;
- no unresolved conflict with the locked architecture or content specifications.

At that point, implementation may proceed as one controlled website build rather than page-by-page improvisation.