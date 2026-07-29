# Techgrity Systems Website Design-Stage Decision Log

**Status:** ACTIVE  
**Date opened:** 29 July 2026

## Purpose

This log records material design-stage decisions that affect multiple page families. Minor implementation details belong in pull requests or component documentation. Decisions that alter the visual system, master-template inventory, production sequence or factual boundaries belong here.

## Decisions

### D-001 — Homepage remains the visual benchmark

**Decision:** The visually approved homepage remains the controlling benchmark for brand character, navigation, typography, card treatment, imagery quality and responsive execution.

**Reason:** It is the only page already visually reconstructed and verified against an explicit reference.

**Consequence:** Internal pages may simplify the hero and adapt density, but may not introduce a conflicting brand direction.

### D-002 — One visual system, distinct divisional expression

**Decision:** Digital Systems and Infrastructure pages use the same logo, typography, navigation, component architecture and core palette. Digital pages are lighter and workflow-led; Infrastructure pages use more navy, technical photography and engineering structure.

**Reason:** The website must show one accountable company without flattening the meaningful difference between software and physical infrastructure.

### D-003 — Thirteen master templates, not thirty-one unrelated designs

**Decision:** The 31 public pages will be implemented through 13 approved master templates.

**Reason:** This provides consistency, faster implementation and maintainable page families while retaining page-specific content and imagery.

### D-004 — Desktop and mobile approval are inseparable

**Decision:** A master template cannot be approved from desktop artwork alone. A 390 px mobile composition is mandatory at the same approval stage.

**Reason:** The homepage proof showed that desktop collage and navigation decisions do not safely shrink without deliberate restructuring.

### D-005 — Images are communication assets, not decoration

**Decision:** Every production image requires a stated purpose, provenance, desktop and mobile crop, alternative-text decision and approval status.

**Reason:** The site must remain technically credible and must not accidentally imply clients, projects, partnerships or employees.

### D-006 — No implementation before family-level visual approval

**Decision:** Shared infrastructure may be prepared, but a public page family should not be fully implemented before its master template is approved.

**Reason:** Implementation must not harden unreviewed layouts or force design decisions through code.

### D-007 — File upload is off by default at launch

**Decision:** Project-enquiry attachments remain disabled unless secure file-type, size, malware scanning, storage, access, retention and deletion controls are approved and implemented.

**Reason:** Tender and project documents may contain sensitive information, and a superficial upload field creates material security and privacy risk.

### D-008 — Analytics is off until approved

**Decision:** No analytics or marketing tracker is included merely because it is common website practice.

**Reason:** Tool selection, event design, consent, privacy impact and operational ownership are unresolved.

### D-009 — Capability claims remain evidence-conscious

**Decision:** The website may describe what Techgrity designs, provides or can deliver, but representative imagery and solution patterns may not be presented as completed client evidence.

**Reason:** The launch architecture deliberately excludes fabricated projects, clients, certifications, partner status and performance claims.

### D-010 — Master-visual production order is fixed

**Decision:** Visual production follows four waves: corporate structure; capability detail systems; sector and delivery narrative; corporate evaluation and conversion.

**Reason:** Early templates establish shared components and prevent downstream redesign.

## Change rule

A new decision entry is required when a proposal would:

- change the 13-template model;
- change the divisional expression;
- introduce a new core colour, typeface or component language;
- alter the master-visual production sequence;
- enable a currently excluded integration such as file uploads or analytics;
- weaken a factual, accessibility, privacy or evidence boundary.

Each new entry must state the decision, reason, consequence, date and approving authority.