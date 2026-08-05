# Techgrity production manual visual audit — final route sign-off register

## Audit boundary

- Production origin: `https://techgrity.co.zw`
- Audited release: `a729d9f1df31acd9835bad9ee7b78408bf3d9672`
- Production state: unchanged during audit
- Browsers: Chromium, Firefox, WebKit
- Primary widths: 1672, 1440, 1280, 1024, 768, 390 and 320 pixels
- Audit result: complete; remediation required before approval

## Evidence completed

- 35 routes × 7 Chromium viewports: 245 full-page visual cells plus overlapping vertical scroll-state captures.
- 35 routes × Firefox/WebKit desktop and mobile: 140 cross-browser full-page cells.
- Total full-page route/browser/viewport inspections: 385.
- 35 routes × 2 responsive positions × 6 real-pointer browser/viewport combinations: 420 pointer interaction states.
- 35 routes × 4 desktop dropdowns × 3 browsers: 420 desktop dropdown states.
- Top, middle and bottom content; sticky header; every visible section; section transitions; image rendering; footer; cookie panel; forms; validation; console/network behavior; metadata; security headers; 404 and safe negative API paths were included.

## Status legend

- `PASS`: manually inspected with no route-specific defect in that audit dimension.
- `FAIL F01/F02`: affected by the corresponding confirmed shared navigation defect.
- `CROSS-CUTTING`: the route’s page body renders correctly, but the shared defect register prevents final approval.

## Route-by-route register

| # | Route | Desktop / scroll | Tablet | Mobile / narrow | Firefox / WebKit | Interaction | Result |
|---:|---|---|---|---|---|---|---|
| 1 | `/` | PASS | PASS | PASS | PASS | FAIL F01/F02 | CROSS-CUTTING |
| 2 | `/capabilities/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 3 | `/capabilities/digital-systems/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 4 | `/capabilities/digital-systems/software-ai-applications/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 5 | `/capabilities/digital-systems/automation/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 6 | `/capabilities/digital-systems/integration/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 7 | `/capabilities/digital-systems/data-analytics/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 8 | `/capabilities/digital-systems/cybersecurity-access/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 9 | `/capabilities/infrastructure/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 10 | `/capabilities/infrastructure/networks-fibre/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 11 | `/capabilities/infrastructure/data-centres-cloud/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 12 | `/capabilities/infrastructure/telecom-radio/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 13 | `/capabilities/infrastructure/power-energy/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 14 | `/capabilities/infrastructure/security-smart-facilities/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 15 | `/capabilities/infrastructure/civil-technical-works/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 16 | `/capabilities/technology-supply/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 17 | `/industries/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 18 | `/industries/government-public-sector/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 19 | `/industries/education-research/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 20 | `/industries/telecommunications/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 21 | `/industries/energy-utilities-industrial/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 22 | `/industries/data-centres-technology/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 23 | `/industries/commerce-logistics-growing-organisations/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 24 | `/how-we-deliver/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 25 | `/company/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 26 | `/resources/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 27 | `/contact/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 28 | `/discuss-a-project/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 29 | `/privacy/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 30 | `/terms/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 31 | `/cookies/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 32 | `/404/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 33 | `/project-enquiry-received/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 34 | `/document-request-received/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |
| 35 | `/form-error/` | PASS | PASS | PASS | PASS | FAIL F02 | CROSS-CUTTING |

## What passed on every route

- Header, opening viewport, all visible sections, section transitions and footer were inspected individually.
- Full-page and overlapping scroll evidence showed no missing section, blank content block, horizontal overflow, broken image, clipped content grid, footer collapse or browser-only page collapse.
- Chromium, Firefox and WebKit comparisons showed no additional route-specific rendering divergence.
- The five short system pages were inspected separately rather than inferred from a shared template.
- No route-specific console error, broken internal link, missing image or measurable layout shift was found.
- Desktop dropdowns open, render within the viewport, contain their expected links and close correctly in Chromium, Firefox and WebKit.
- Responsive menu state changes, body lock and Escape closure execute; the failures are panel geometry and scroll preservation, not a missing click handler.

## Final responsive-navigation evidence

The definitive matrix used a coordinate-level pointer tap on the already-visible sticky menu button. It did not use a synthetic DOM click or a Playwright locator click that could auto-scroll the target.

### F01 — homepage menu clipping

At 1024, 768, 390 and 320 pixels, the homepage responsive navigation has a rendered height of only 65 pixels. The same 65-pixel result occurs in Chromium, Firefox and WebKit. The internal-page menu uses the expected remaining viewport height; only the homepage-specific cascade clips the panel.

### F02 — scroll position loss

For every route at 390 and 320 pixels, the mid-page state had a non-zero scroll position. After a real pointer tap on the sticky menu button:

- the page moved to `scrollY = 0`;
- the menu opened at the top;
- Escape closed the menu;
- the page remained at `scrollY = 0` instead of restoring the previous position.

The same behavior was reproduced in Chromium, Firefox and WebKit. At tablet widths the same failure occurs on every route with enough content to scroll; the shortest system pages have no meaningful mid-page position at 768 pixels but reproduce the defect at mobile widths.

## Confirmed defect register

| ID | Severity | Scope | Confirmed defect |
|---|---|---|---|
| F01 | Critical | Homepage responsive navigation | The opened homepage menu is clipped to a 65-pixel panel at every responsive width and in Chromium, Firefox and WebKit. |
| F02 | High | Responsive navigation on all routes | Opening the sticky menu after scrolling forces the document to the top; closing the menu does not restore the previous position. |
| F03 | High | Forms | Clearing a validation error removes the visible message but leaves its deleted ID in `aria-describedby`. |
| F04 | High | Homepage and capability content | Several teal/muted text combinations, mobile delivery-step labels and the power-and-energy scope label fail WCAG contrast. |
| F05 | Medium | Breadcrumbs, card links, legal contents and contact links | Several interactive targets are below the preferred 44-pixel target size. |
| F06 | Medium | Homepage footer markup | Generated homepage footer logo markup contains malformed `<img ... / style="...">`; browsers recover, but the output is invalid. |
| F07 | High | SMTP presentation | The mail subject uses an unencoded Unicode em dash, matching the previously observed character corruption. |
| F08 | High | Production asset delivery | Stable unversioned asset URLs are marked immutable for one year, preventing reliable cache invalidation after releases. |
| F09 | Medium | Build reproducibility | Node is not pinned consistently between package metadata, CI and Vercel. |
| F10 | Medium | Source consistency | Source `site.js` retains the superseded telephone in its fallback message even though the build currently rewrites the deployed output. |

## Instrumentation corrections retained in the audit record

Two earlier interaction methods were rejected rather than used to support the final conclusion:

1. A synthetic `element.click()` preserved the scroll position but could leave the fixed panel geometrically outside the viewport.
2. A Playwright locator click auto-scrolled the target and therefore did not represent a user tapping the visible sticky header.

The final result is based on real pointer coordinates, a 1.5-second settled state, screenshot evidence, pre-open geometry, opened geometry, Escape closure and post-close geometry for every route.

## Audit conclusion

The page-by-page production audit is complete. The visual body of every route is structurally sound across the audited widths and browsers, but the release is **not approved as defect-free** because F01–F10 remain unresolved. F01 and F02 directly affect all responsive navigation journeys; F03, F04, F07 and F08 are also release-blocking quality defects.

## Merge and deployment gate

PR #16 must remain draft. No merge or production deployment is allowed until:

1. F01–F10 are corrected together on this PR;
2. a corrected preview is produced from the exact PR head;
3. the complete full-page, overlapping-scroll, real-pointer, dropdown, form, WCAG, cross-browser and delivery audit is repeated against that preview;
4. every route is marked `PASS` with zero unresolved findings;
5. exact-head CI and independent review are complete.
