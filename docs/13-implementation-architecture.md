# Techgrity Systems Website Implementation Architecture

**Status:** IMPLEMENTED BASELINE  
**Date:** 29 July 2026

## 1. Architecture decision

The production website uses a data-driven static-site architecture with serverless form endpoints.

This approach was selected because the launch site is primarily corporate content, requires strong performance and predictable SEO output, and contains only three controlled write workflows. It avoids maintaining 31 duplicated hand-written pages while keeping the generated output transparent and deployable on ordinary static hosting with serverless functions.

## 2. Sources of truth

- `src/content.js` — capability and industry page data;
- `src/templates.js` — shared shell, page families, forms, metadata and system pages;
- `src/homepage.html` — approved homepage source;
- `public/` — shared visual system, client interaction code and approved assets;
- `docs/` — architecture, content, design, factual and acceptance controls;
- `visuals/` — approved master prototypes and review evidence.

`dist/` is generated output and is not a source of truth.

## 3. Route generation

`scripts/build.js` generates:

- 31 canonical indexable public routes;
- four non-indexed system routes;
- shared assets;
- XML sitemap;
- robots file;
- route manifest.

Every page is generated with:

- one H1;
- unique title and description;
- canonical URL;
- Open Graph and social metadata;
- structured data appropriate to the page type;
- the shared header, navigation and footer;
- real internal destinations only.

## 4. Page-family model

The implementation maps the 31 routes to the 13 approved master templates:

1. Homepage;
2. Capabilities overview;
3. Digital Systems landing;
4. Digital capability detail;
5. Infrastructure landing;
6. Infrastructure capability detail;
7. Technology Supply & Integration;
8. Industries overview;
9. Industry detail;
10. How We Deliver;
11. Company;
12. Resources;
13. Contact and enquiry forms.

Shared templates do not remove page specificity. Each route receives its own proposition, content, hero subject, metadata, related capabilities and sector context.

## 5. Client interaction layer

`public/site.js` provides:

- accessible desktop dropdown and mobile navigation behaviour;
- Escape-key and focus-safe menu closure;
- client-side required-field and email validation;
- asynchronous form submission and accessible status messages;
- safe cookie-preference storage handling;
- current-year footer output.

Core page content remains available without client JavaScript.

## 6. Form architecture

Three POST endpoints exist:

- `/api/contact`;
- `/api/project`;
- `/api/document-request`.

The server-side handler provides:

- method and content-type enforcement;
- request-size limits;
- field validation and length limits;
- honeypot handling;
- basic rate limiting;
- time-to-submit abuse checks;
- control-character removal;
- non-sensitive reference identifiers;
- plain-text internal notifications;
- fail-closed behaviour when delivery is not commissioned;
- no-store JSON responses.

Live notification delivery uses the authenticated SMTP delivery through server-side secrets. No mail credential is exposed in public assets.

## 7. Document publication model

The Resources page distinguishes document families from published files. A real direct download may be added only when the file exists and its title, version, date, access model, public-release approval and accessibility status are recorded.

No placeholder download is generated.

## 8. Privacy and storage model

The current client stores only the visitor's cookie-preference choice under:

```text
techgrity-cookie-preference
```

No advertising or non-essential analytics technology is included in the implemented baseline. Public forms do not accept file attachments. Personal information is sent only through the dedicated server-side form endpoints.

## 9. Security baseline

The deployment configuration supplies:

- HTTPS-oriented delivery;
- Content Security Policy;
- frame-ancestor protection;
- content-type sniffing protection;
- referrer policy;
- permissions policy;
- immutable caching for versioned public assets.

Security headers must be re-tested on the real production hostname because platform behaviour and any later integrations may require a controlled policy change.

## 10. Test architecture

### Structural validation

`scripts/validate.js` verifies:

- exact public and system route counts;
- file existence;
- one H1 per route;
- unique public titles and descriptions;
- canonical metadata;
- internal references;
- no known unverified corporate details;
- CSS brace integrity;
- sitemap route count;
- approved logo SHA-256.

### Form validation

`scripts/test-forms.js` exercises valid, invalid and bot-trap payloads without sending email.

### Browser QA

`scripts/browser-qa.py` renders all routes in Chromium and verifies:

- horizontal overflow;
- H1 count;
- image loading;
- JavaScript errors;
- navigation CTA styling;
- mobile navigation geometry and operation;
- client form validation;
- cookie preference controls.

Representative desktop, mobile and full-page screenshots are generated as CI artifacts.

## 11. Deployment architecture

`vercel.json` defines a static build output in `dist/` and serverless API handlers under `api/`.

The same static output can be deployed elsewhere, but another platform must reproduce:

- canonical clean URLs and trailing-slash behaviour;
- API routes;
- security headers;
- environment-secret handling;
- immutable asset caching;
- custom 404 behaviour;
- rollback to an exact release.

## 12. Change control

A content or route change must update the structured source and regenerate output. Direct untracked editing of deployed HTML is not an accepted production workflow.

A material visual change must remain consistent with the approved template or receive a superseding review. A new public factual claim must be added to the factual-information register with supporting evidence.
