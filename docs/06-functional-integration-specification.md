# Techgrity Systems Functional and Integration Specification

**Status:** BASELINE COMPLETE  
**Version:** 1.0  
**Date:** 29 July 2026  
**Depends on:** [`02-master-website-specification.md`](02-master-website-specification.md), [`03-visual-design-system.md`](03-visual-design-system.md), [`05-seo-metadata-matrix.md`](05-seo-metadata-matrix.md)

## 1. Purpose

This document defines the behaviour, data handling, integrations, failure modes and operational controls required for the Techgrity Systems website. It is implementation-technology neutral. The final stack may be selected later, but it must satisfy this contract.

## 2. Functional scope

Launch functionality includes:

- global utility bar, header, navigation and footer;
- accessible Capabilities mega-menu and Industries menu;
- responsive mobile navigation;
- breadcrumbs on internal pages;
- live links for all 31 public routes;
- internal related-content navigation;
- capability-statement downloads and controlled requests;
- general contact form;
- detailed project-enquiry form;
- document-request form within Resources;
- success, recoverable failure and 404 experiences;
- cookie preference controls where non-essential storage exists;
- canonical metadata, sitemap and robots behaviour;
- secure email or workflow routing for form submissions;
- operational logging without exposing personal information;
- deployment traceability and reproducible builds.

Explicitly excluded at launch unless separately approved:

- e-commerce;
- customer accounts;
- public pricing;
- CRM automation beyond controlled submission routing;
- public project, partner, careers or insights sections;
- general site search unless content volume proves it useful;
- chatbots or autonomous visitor-facing AI;
- unrestricted file uploads;
- third-party marketing trackers without privacy approval.

## 3. Global navigation behaviour

### 3.1 Desktop

- Home, Capabilities, Industries, How We Deliver, Company, Resources and Contact are visible.
- Discuss a Project is the primary header action.
- Capabilities opens a structured three-column menu.
- Industries opens a concise sector menu.
- dropdowns operate by pointer, keyboard and touch-capable desktop input;
- `Escape` closes the active menu;
- focus moves predictably and is never trapped;
- clicking outside closes an open menu;
- only one dropdown remains open at a time;
- current page or section is visibly indicated.

### 3.2 Mobile

- one explicit menu button exposes its expanded state through `aria-expanded`;
- navigation groups expand by activation, not hover;
- menu order matches desktop information architecture;
- Discuss a Project appears inside the menu as a strong action;
- body scrolling is controlled while a full-screen menu is open;
- closing the menu returns focus to the triggering control;
- no route is hidden only because of viewport size.

## 4. Links and routing

- all internal links use canonical routes;
- external links are clearly distinguishable where context requires;
- `mailto:` links use the approved business email;
- `tel:` links use an international-format number in the `href` and human-readable formatting in text;
- no link opens a new tab without a genuine user benefit and appropriate warning;
- redirects from legacy routes are permanent, one-hop and tested;
- unknown public routes render the custom 404 experience with HTTP 404 status;
- confirmation pages must not be reachable as evidence of submission without a corresponding successful server response where the architecture permits enforcement.

## 5. General contact form

### 5.1 Purpose

Capture a concise business enquiry that does not require the detailed project form.

### 5.2 Fields

| Field | Type | Required | Rules |
|---|---|---:|---|
| Name | text | yes | 2–100 characters |
| Organisation | text | no | maximum 150 characters |
| Work email | email | yes | valid syntax; maximum 254 characters |
| Telephone | tel | no | preserve international formatting; maximum 40 characters |
| Enquiry category | select | yes | approved category list |
| Message | textarea | yes | 20–4000 characters |
| Privacy consent | checkbox | yes | explicit unchecked default |
| Bot trap | hidden/honeypot | no user action | must remain absent or empty |

Approved categories:

- General business enquiry;
- Digital Systems & AI;
- Infrastructure & Engineering;
- Technology Supply & Integration;
- Capability statements and documents;
- Partnerships and specialist delivery;
- Other.

### 5.3 Submission outcome

On success:

- show an accessible success state or redirect to a non-indexed confirmation route;
- provide a reference identifier that does not expose internal sequence or personal data;
- state only a response expectation that Techgrity can operationally meet;
- avoid displaying submitted sensitive content on the confirmation page.

On recoverable failure:

- preserve entered data in the browser where safe;
- identify the error in plain language;
- move focus to the error summary;
- link summary errors to fields;
- provide retry and direct contact alternatives.

## 6. Discuss a Project form

### 6.1 Purpose

Capture enough information to qualify and route a digital, infrastructure or integrated project requirement without forcing the visitor to write a tender document.

### 6.2 Form sections

1. Contact and organisation;
2. Project classification;
3. Requirement and expected outcomes;
4. Environment, timing and procurement context;
5. Optional documents;
6. Consent and submission.

### 6.3 Fields

| Field | Type | Required | Validation and notes |
|---|---|---:|---|
| Name | text | yes | 2–100 characters |
| Organisation | text | yes | 2–150 characters |
| Role or job title | text | yes | 2–120 characters |
| Work email | email | yes | maximum 254 characters |
| Telephone | tel | yes | maximum 40 characters |
| Country | searchable select or text | yes | default may reflect locale but must remain editable |
| Project category | select | yes | approved list below |
| Industry | select | yes | six launch sectors plus Other |
| Project location | text | yes | city, province or country; maximum 200 characters |
| Project description | textarea | yes | 50–8000 characters |
| Expected outcomes | textarea | yes | 20–4000 characters |
| Current environment | textarea | yes | 20–4000 characters |
| Required timescale | select plus optional detail | yes | approved list below |
| Procurement or tender status | select | yes | approved list below |
| Approximate budget range | select | no | values must be approved before implementation |
| Required documents | multi-select | no | capability statements or related documents |
| File attachment | file | no | disabled until secure upload controls are approved |
| Privacy consent | checkbox | yes | explicit unchecked default |
| Bot trap | hidden/honeypot | no user action | must remain empty |

Project categories:

- Digital Systems & AI;
- Networks & Fibre;
- Data Centres & Cloud;
- Telecom & Radio;
- Power & Energy;
- Security & Smart Facilities;
- Civil & Technical Infrastructure;
- Technology Supply & Integration;
- Multiple or integrated capabilities;
- Not sure yet.

Industry options:

- Government & Public Sector;
- Education & Research;
- Telecommunications;
- Energy, Utilities & Industrial Operations;
- Data Centres & Technology Organisations;
- Commerce, Logistics & Growing Organisations;
- Other.

Timescale options:

- Immediate or urgent requirement;
- Within 1–3 months;
- Within 3–6 months;
- Within 6–12 months;
- More than 12 months;
- Early planning or feasibility stage.

Procurement status options:

- Early requirement definition;
- Budgeting or feasibility;
- Preparing specifications or tender documents;
- Active request for quotation;
- Active tender or procurement process;
- Approved project awaiting delivery partner;
- Existing environment requiring support or improvement;
- Other.

### 6.4 Conditional behaviour

- selecting Multiple or integrated capabilities may reveal a concise multi-select capability field;
- selecting Active tender may reveal an optional tender reference and closing date;
- selecting Other reveals a short text field;
- conditional fields must remain accessible and not rely on animation;
- hidden fields must not be required or submitted with stale values.

### 6.5 Attachment decision

File upload is **off by default** at launch until all of the following are approved:

- permitted file types;
- maximum file size and count;
- malware scanning method;
- storage location and retention;
- encryption and access control;
- deletion workflow;
- logging and incident response;
- privacy notice wording;
- safe handling of procurement-sensitive documents.

Until then, the form may request that documents be shared through a controlled follow-up channel after initial contact.

## 7. Document downloads and requests

### 7.1 Direct downloads

A document may be shown as directly downloadable only when:

- the file exists;
- publication is approved;
- title, type, version and date are correct;
- the file contains no confidential or outdated information;
- the URL is stable or redirected when superseded;
- accessibility has been reviewed;
- the document is recorded in the resource register.

### 7.2 Document request form

Fields:

- name;
- organisation;
- job title;
- work email;
- telephone;
- country;
- document required;
- reason for request;
- tender or procurement reference, optional;
- privacy consent.

Document options:

- Corporate Capability Statement;
- Digital Systems Capability Statement;
- Infrastructure Capability Statement;
- All capability statements.

### 7.3 Delivery model

The implementation must explicitly choose one model per document:

1. immediate public download;
2. immediate emailed download link after valid request;
3. manual review and controlled follow-up;
4. unavailable and therefore not displayed.

Do not simulate a download or display an empty placeholder.

## 8. Server-side submission contract

Every form endpoint must:

- accept HTTPS only;
- reject unsupported methods;
- enforce content-type and request-size limits;
- validate all fields server-side;
- normalise and sanitise content without corrupting legitimate names or organisations;
- reject bot-trap completion;
- apply rate limiting;
- use abuse detection appropriate to risk;
- avoid reflecting raw input in HTML responses;
- generate a non-sensitive reference identifier;
- route the submission through a server-side integration;
- return a stable, documented response shape;
- avoid leaking stack traces, provider responses or secrets;
- record operational outcome with minimised personal data.

Recommended response model:

```json
{
  "ok": true,
  "reference": "TGS-ENQ-XXXXXXXX",
  "message": "Your enquiry has been received."
}
```

Failure responses use appropriate HTTP status codes and a safe machine-readable code, for example:

```json
{
  "ok": false,
  "code": "VALIDATION_ERROR",
  "message": "Please review the highlighted fields."
}
```

## 9. Mail and workflow routing

### 9.1 Required decisions

Before integration, confirm:

- recipient mailbox for general enquiries;
- recipient mailbox for project enquiries;
- recipient mailbox or workflow for document requests;
- approved sender domain and address;
- SMTP or transactional mail provider;
- whether submissions also enter a CRM or ticket system;
- operational owner and escalation path.

### 9.2 Message content

Internal notification should include:

- form type;
- safe reference identifier;
- submission timestamp and timezone;
- submitted fields in readable sections;
- source page and approved campaign parameters where consent allows;
- abuse score or validation outcome where useful;
- no secrets, raw server logs or unnecessary browser fingerprinting.

### 9.3 Visitor acknowledgement

Automatic acknowledgements are optional and may be enabled only when:

- the sender domain is authenticated;
- content and response expectations are approved;
- bounce and abuse handling exist;
- acknowledgements do not expose internal recipients;
- duplicate sends are prevented.

## 10. Spam and abuse controls

Use layered controls:

- server-side validation;
- honeypot field;
- time-to-submit checks that do not block assistive technology users;
- per-IP and per-fingerprint rate limits with privacy review;
- request body limits;
- duplicate suppression;
- optional privacy-reviewed challenge only when passive controls are insufficient;
- monitoring of rejection and false-positive rates.

Do not rely only on client-side validation. Do not add a third-party CAPTCHA without documenting accessibility, privacy and regional availability implications.

## 11. Privacy and data minimisation

- collect only fields required for the stated purpose;
- disclose purpose, recipients, retention and user rights in the privacy notice;
- do not place personal data in URLs;
- do not log full message bodies in general application logs;
- restrict mailbox, storage and administration access;
- define retention periods before launch;
- delete test submissions before production acceptance;
- use production-like synthetic data for QA;
- do not use submissions for marketing unless separate lawful consent and process exist.

## 12. Cookies, storage and consent

### 12.1 Essential storage

Essential preferences may be stored without marketing consent where legally appropriate, including:

- cookie preference state;
- short-lived anti-abuse or security token;
- necessary form continuity state.

### 12.2 Non-essential storage

Analytics, advertising, personalisation or third-party embedded media may not load before the relevant consent decision where consent is required.

The preference interface must:

- explain categories in plain language;
- offer reject and accept choices with comparable prominence;
- allow granular configuration where multiple non-essential categories exist;
- remain keyboard and screen-reader usable;
- allow later withdrawal or change;
- record only the minimum necessary consent evidence;
- match the published Cookie Policy.

If no non-essential cookies or storage exist, do not display a performative consent banner. Still provide accurate policy wording.

## 13. Analytics

Analytics is off until an approved tool and measurement plan exist.

Potential events after approval:

- header project CTA selected;
- capability or industry route selected;
- capability statement downloaded;
- document request completed;
- general enquiry completed;
- project enquiry completed;
- email or telephone link selected.

Rules:

- never send form contents, names, email addresses or message text as analytics properties;
- avoid fingerprinting;
- respect consent and browser privacy signals where applicable;
- document event names and retention;
- do not convert analytics into unsupported public claims.

## 14. Search

General site search is not required at launch. It may be introduced later when content volume and user evidence justify it.

If introduced, it must:

- search canonical public content only;
- exclude legal confirmation and system pages from normal results;
- use accessible result markup;
- provide useful empty-state guidance;
- avoid indexing private documents;
- not depend on a privacy-invasive external service without review.

## 15. Accessibility interaction requirements

- menus, accordions, dialogs and forms work without a pointer;
- focus order follows visual and reading order;
- focus is restored after closing modal or mobile-menu experiences;
- status messages use appropriate live regions without excessive announcements;
- validation errors are programmatically associated with fields;
- accordions expose expanded state;
- form instructions do not rely on colour or position alone;
- loading states announce progress where necessary;
- timeout behaviour must not silently discard user work.

## 16. Security headers baseline

The production delivery layer should support:

- `Strict-Transport-Security` after HTTPS is proven;
- `Content-Security-Policy` tailored to actual assets and integrations;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy` appropriate to business and privacy requirements;
- `Permissions-Policy` restricting unused browser capabilities;
- frame protection through CSP `frame-ancestors`;
- secure, `HttpOnly` and appropriate `SameSite` attributes for cookies that require them.

Header values must be tested against the actual implementation. Do not copy a policy that breaks forms, fonts, images or required integrations.

## 17. Environment and secrets

- secrets exist only in approved environment configuration or secret stores;
- `.env` files containing secrets are never committed;
- repository examples use placeholders;
- production, staging and local environments use separate credentials;
- staging mail must not reach real recipients unless explicitly tested;
- public client code contains no SMTP password, API key or provider secret;
- key rotation and revocation procedures must be documented before production commissioning.

## 18. Logging and monitoring

Required operational signals:

- form endpoint availability;
- success and failure counts without message content;
- validation and abuse rejection counts;
- mail or workflow delivery outcome;
- unexpected server errors;
- deployment version;
- TLS and public-route availability;
- broken-download detection where practical.

Logging rules:

- redact personal data;
- avoid storing complete request bodies;
- apply access control and retention;
- distinguish user validation errors from infrastructure failures;
- alerts must route to an approved operational owner.

## 19. Performance behaviour

- reserve image dimensions to prevent layout shift;
- lazy-load below-the-fold media;
- do not lazy-load the primary LCP image where that delays rendering;
- preload only critical fonts or hero assets proven necessary;
- avoid JavaScript for static content;
- split or defer interaction code where useful;
- no blocking third-party marketing scripts at launch;
- forms must remain usable on slow or intermittent networks;
- duplicate submission must be prevented while a request is in flight.

## 20. Document and asset integrity

- downloads use stable URLs or controlled redirect aliases;
- file checksums may be recorded internally for release integrity;
- obsolete files are removed or redirected;
- no directory listing is exposed;
- asset names follow the art-direction convention;
- all production images have recorded provenance and approval;
- all public documents have recorded version and publication status.

## 21. Error and system experiences

### 21.1 404

Must:

- return HTTP 404;
- explain that the page could not be found;
- offer Home, Capabilities, Industries, Contact and Discuss a Project routes;
- not blame the visitor;
- remain visually consistent with the site.

### 21.2 Submission confirmation

Must:

- confirm only after server success;
- show a safe reference identifier;
- avoid repeating sensitive content;
- offer relevant next routes;
- be `noindex`.

### 21.3 Recoverable form failure

Must:

- preserve safe entered data;
- state what happened without exposing internals;
- provide retry and direct contact alternatives;
- be `noindex`.

### 21.4 Service outage

A controlled fallback should provide confirmed business email and telephone without making unsupported availability claims.

## 22. Build and deployment contract

The selected implementation must provide:

- deterministic dependency installation;
- reproducible production build;
- environment validation;
- automated route and link checks;
- linting and formatting where applicable;
- component or integration tests for navigation and forms;
- accessibility automation as a supporting check;
- production asset optimisation;
- versioned deployment output;
- rollback capability;
- deployment evidence linked to an exact commit.

No direct untracked server edits are allowed as the final source of truth.

## 23. Acceptance tests

Minimum functional proof:

1. every canonical public route returns success;
2. unknown route returns the custom 404 and HTTP 404;
3. desktop and mobile navigation expose every destination;
4. keyboard operation and focus restoration pass;
5. all internal links and downloads resolve;
6. general contact valid submission routes successfully;
7. general contact invalid submission shows associated errors;
8. project form valid submission routes successfully;
9. conditional project fields behave and submit correctly;
10. duplicate in-flight submission is prevented;
11. server-side validation rejects bypass attempts;
12. abuse controls reject synthetic spam without blocking valid test cases;
13. success and failure pages use correct indexation;
14. no secret appears in built assets or repository history;
15. cookies and analytics behaviour match policy and consent state;
16. logging records outcome without full personal content;
17. security headers are present and tested;
18. production deployment maps to an exact reviewed commit.

## 24. Outstanding integration decisions

These remain blockers for final implementation:

- implementation framework and hosting target;
- approved form endpoint architecture;
- recipient mailbox or workflow per form;
- approved mail provider and authenticated sender;
- document delivery model per capability statement;
- file-upload launch decision;
- retention periods;
- analytics decision and tool;
- cookie categories actually used;
- monitoring owner and alert route;
- final privacy and consent wording;
- production deployment and rollback procedure.

Unknown decisions must remain explicit dependencies rather than be hidden behind placeholder behaviour.