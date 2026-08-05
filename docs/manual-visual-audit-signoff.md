# Techgrity production manual visual audit — route sign-off register

## Audit boundary

- Production origin: `https://techgrity.co.zw`
- Audited release: `a729d9f1df31acd9835bad9ee7b78408bf3d9672`
- Production state: unchanged during audit
- Browsers: Chromium, Firefox, WebKit
- Primary widths: 1672, 1440, 1280, 1024, 768, 390, 320 pixels
- Evidence standard: full-page capture, overlapping vertical scroll captures, top/middle/bottom inspection, desktop/mobile comparison, Firefox/WebKit comparison, and explicit interaction-state evidence

## Status legend

- `PASS`: manually inspected with no route-specific visual defect.
- `CROSS-CUTTING`: route renders correctly, but one or more shared defects listed below affect the route or shared components.
- `PENDING-INTERACTION`: full-page and scroll inspection passed; corrected menu/dropdown evidence is still running.

## Route-by-route register

| # | Route | Desktop / scroll | Tablet | Mobile / narrow | Firefox / WebKit | Interaction | Result |
|---:|---|---|---|---|---|---|---|
| 1 | `/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 2 | `/capabilities/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 3 | `/capabilities/digital-systems/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 4 | `/capabilities/digital-systems/software-ai-applications/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 5 | `/capabilities/digital-systems/automation/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 6 | `/capabilities/digital-systems/integration/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 7 | `/capabilities/digital-systems/data-analytics/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 8 | `/capabilities/digital-systems/cybersecurity-access/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 9 | `/capabilities/infrastructure/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 10 | `/capabilities/infrastructure/networks-fibre/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 11 | `/capabilities/infrastructure/data-centres-cloud/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 12 | `/capabilities/infrastructure/telecom-radio/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 13 | `/capabilities/infrastructure/power-energy/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 14 | `/capabilities/infrastructure/security-smart-facilities/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 15 | `/capabilities/infrastructure/civil-technical-works/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 16 | `/capabilities/technology-supply/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 17 | `/industries/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 18 | `/industries/government-public-sector/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 19 | `/industries/education-research/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 20 | `/industries/telecommunications/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 21 | `/industries/energy-utilities-industrial/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 22 | `/industries/data-centres-technology/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 23 | `/industries/commerce-logistics-growing-organisations/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 24 | `/how-we-deliver/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 25 | `/company/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 26 | `/resources/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 27 | `/contact/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 28 | `/discuss-a-project/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 29 | `/privacy/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 30 | `/terms/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 31 | `/cookies/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 32 | `/404/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 33 | `/project-enquiry-received/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 34 | `/document-request-received/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |
| 35 | `/form-error/` | PASS | PASS | PASS | PASS | PENDING-INTERACTION | CROSS-CUTTING |

## What passed on every route

- Header, hero/opening viewport, all visible sections, section transitions and footer were inspected.
- Full-page and overlapping scroll captures showed no missing section, blank content block, horizontal overflow, broken image, clipped card grid, footer collapse or browser-only page collapse.
- Chromium, Firefox and WebKit full-page comparisons showed no new route-specific rendering divergence.
- The five short system pages were inspected separately rather than inferred from the shared template.
- No route-specific console error, broken internal link, missing image or measurable layout shift was found.

## Confirmed cross-cutting defect register

| ID | Severity | Scope | Confirmed defect |
|---|---|---|---|
| F01 | Critical | Homepage responsive navigation | The opened homepage menu is clipped to a narrow strip at responsive widths instead of exposing the complete navigation. |
| F02 | High | Responsive navigation / WebKit | Internal-page menus opened after scrolling can be positioned incorrectly in WebKit. |
| F03 | High | Forms | Clearing a validation error removes the visible message but leaves its deleted ID in `aria-describedby`. |
| F04 | High | Homepage and capability content | Several teal/muted text combinations and mobile delivery-step labels fail WCAG contrast. |
| F05 | Medium | Breadcrumbs, card links, legal contents and contact links | Several interactive targets are below the preferred 44-pixel target size. |
| F06 | Medium | Homepage footer markup | The generated homepage footer logo contains malformed `<img ... / style="...">` markup; browsers recover but source validity is incorrect. |
| F07 | High | SMTP presentation | The mail subject uses an unencoded Unicode em dash, matching the previously observed character corruption. |
| F08 | High | Production asset delivery | Stable unversioned asset URLs are marked immutable for one year, preventing safe cache invalidation after releases. |
| F09 | Medium | Build reproducibility | Node is not pinned consistently between package metadata, CI and Vercel. |
| F10 | Medium | Source consistency | Source `site.js` retains the superseded telephone in its fallback message even though the build currently rewrites the deployed output. |

## Interaction-evidence correction

The first interaction capture produced misleading `menu-top` images on some long pages. Those files are explicitly excluded from sign-off. A replacement matrix now:

- reloads every route for each interaction state;
- asserts `aria-expanded="true"` and the navigation `open` class;
- verifies a non-zero rendered menu area and top-level navigation content;
- records menu geometry, visible items, body lock and active focus;
- verifies Escape closes the menu;
- repeats desktop dropdowns in Chromium, Firefox and WebKit.

No interaction state will be marked passed until the replacement artifact has completed and been manually inspected.

## Merge and deployment gate

PR #16 must remain draft. No merge or production deployment is allowed until:

1. the corrected interaction matrix completes;
2. every interaction capture is manually signed off;
3. all confirmed defects are corrected together on this PR;
4. a corrected preview is produced;
5. the complete full-page, scroll and interaction inspection is repeated against that preview;
6. every route is marked `PASS` with zero unresolved findings.
