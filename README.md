# Techgrity Systems Website

Production website source for **Techgrity Systems**.

> **Digital systems. Critical infrastructure. One accountable partner.**

The site is generated from structured page data and reusable templates so that all 31 public routes share one controlled navigation, visual system, metadata model and acceptance process.

## Current implementation

- 31 canonical public pages;
- four non-indexed supporting system pages;
- approved 13-template visual system;
- responsive desktop, tablet and mobile layouts;
- accessible navigation, mega-menus, forms and cookie preferences;
- general enquiry, project enquiry and capability-document request endpoints;
- unique metadata, canonical URLs, structured data, XML sitemap and robots file;
- deterministic build, structural validation, form validation and Chromium browser QA;
- Vercel-ready static output and serverless form handlers.

## Repository structure

```text
src/                 structured content and HTML templates
public/              shared CSS, JavaScript and approved assets
api/                 server-side enquiry endpoints
scripts/             build, validation, form tests and browser QA
docs/                architecture, content, design and acceptance controls
visuals/             approved master prototypes and review evidence
.github/workflows/   continuous integration
dist/                generated output; not committed
```

## Local development

```bash
npm ci && npm test && python3 scripts/browser-qa.py
```

To serve the generated site locally:

```bash
npm run build && npm run serve
```

The server listens on `http://127.0.0.1:4173` by default.

## Enquiry delivery

The form endpoints fail closed until live mail delivery is commissioned. Configure these server-side environment variables:

```text
SMTP_HOST
SMTP_PORT
SMTP_SECURE
SMTP_USER
SMTP_PASS
MAIL_FROM_EMAIL
ENQUIRY_TO_EMAIL
```

`FORM_DRY_RUN=1` is for controlled local or CI testing only and must not be enabled in production.

## Build outputs

`npm run build` creates `dist/` with:

- all public and system routes;
- shared assets;
- `sitemap.xml`;
- `robots.txt`;
- `route-manifest.json`.

Generated output and runtime screenshots are deliberately excluded from Git. CI regenerates and validates them from the reviewed source.

## Publication boundaries

The site must not publish invented legal details, exact addresses, clients, projects, partners, certifications, statistics or downloadable documents. Capability statements appear as downloadable resources only after the real files, versions and publication approvals exist.

Production completion requires deployed-route, DNS, TLS, form-delivery, document, monitoring, accessibility, security, performance and visual evidence against the exact release commit.
