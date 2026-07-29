# Techgrity Systems Visual and Functional Acceptance Checklist

**Status:** BASELINE COMPLETE  
**Version:** 1.0  
**Date:** 29 July 2026  
**Depends on:** all governing documents under `docs/`

## 1. Purpose

This checklist defines the minimum evidence required before the Techgrity Systems website, a page family or a production deployment may be declared complete. Passing source review alone is not sufficient. Acceptance requires direct visual, functional, accessibility, content, security, SEO and public-runtime evidence.

## 2. Acceptance status model

| Status | Meaning |
|---|---|
| `NOT STARTED` | no evidence exists |
| `IN PROGRESS` | work or evidence is incomplete |
| `PASS` | requirement is directly proven against the reviewed release |
| `FAIL` | requirement was tested and did not pass |
| `BLOCKED` | external fact, access, integration or approval is missing |
| `NOT APPLICABLE` | requirement does not apply and the reason is documented |

A release cannot be accepted with unresolved `FAIL` results. `BLOCKED` results require an explicit launch decision and must never be converted into an unsupported completion claim.

## 3. Evidence rules

Every acceptance record must identify:

- exact commit SHA;
- branch or pull request;
- deployment URL where runtime evidence is required;
- test date and timezone;
- tester or automated job;
- viewport, browser and device where relevant;
- evidence path or workflow artifact;
- pass, fail, blocked or not-applicable status;
- notes and defect reference where applicable.

Screenshots must show the tested page and viewport. Automated reports must remain retrievable. Evidence from an older commit does not prove a newer release unless the relevant output is demonstrably identical.

## 4. Planning and governance gate

- [ ] Locked 31-page sitemap remains unchanged or approved revisions are recorded.
- [ ] All five supporting system experiences are specified.
- [ ] All 13 master templates are represented.
- [ ] Page-by-page content specification covers every public route.
- [ ] Visual design system is approved.
- [ ] Image and art-direction brief is approved.
- [ ] SEO and metadata matrix is current.
- [ ] Functional and integration specification is current.
- [ ] Factual-information register is reviewed.
- [ ] No implementation silently changes a locked route, page name, division or navigation item.
- [ ] Every public claim is `CONFIRMED` or removed.

## 5. Master-visual approval gate

For each of the 13 master templates:

- [ ] Desktop visual exists at an approved reference width.
- [ ] Mobile visual exists at 390 px width.
- [ ] Tablet structural behaviour is defined.
- [ ] Page objective is understandable in the first viewport.
- [ ] H1, lead copy and primary CTA match the content specification.
- [ ] Navigation and footer remain consistent with the approved homepage.
- [ ] Colours, typography, spacing, radii and shadows match the visual system.
- [ ] Digital and Infrastructure expressions are distinct but clearly one brand.
- [ ] Photography follows the art-direction brief.
- [ ] Desktop and mobile crops are technically plausible.
- [ ] No image implies an unverified client, project, partner or employee.
- [ ] Diagrams have a complete text equivalent.
- [ ] No important text is embedded only inside an image.
- [ ] Accessibility concerns are resolved before implementation.
- [ ] Approval date, approver and reference assets are recorded.

Master templates:

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

## 6. Route and information-architecture gate

### Public pages

- [ ] `/`
- [ ] `/capabilities`
- [ ] `/industries`
- [ ] `/how-we-deliver`
- [ ] `/company`
- [ ] `/resources`
- [ ] `/contact`
- [ ] `/discuss-a-project`
- [ ] `/capabilities/digital-systems`
- [ ] `/capabilities/digital-systems/software-ai-applications`
- [ ] `/capabilities/digital-systems/automation`
- [ ] `/capabilities/digital-systems/integration`
- [ ] `/capabilities/digital-systems/data-analytics`
- [ ] `/capabilities/digital-systems/cybersecurity-access`
- [ ] `/capabilities/infrastructure`
- [ ] `/capabilities/infrastructure/networks-fibre`
- [ ] `/capabilities/infrastructure/data-centres-cloud`
- [ ] `/capabilities/infrastructure/telecom-radio`
- [ ] `/capabilities/infrastructure/power-energy`
- [ ] `/capabilities/infrastructure/security-smart-facilities`
- [ ] `/capabilities/infrastructure/civil-technical-works`
- [ ] `/capabilities/technology-supply`
- [ ] `/industries/government-public-sector`
- [ ] `/industries/education-research`
- [ ] `/industries/telecommunications`
- [ ] `/industries/energy-utilities-industrial`
- [ ] `/industries/data-centres-technology`
- [ ] `/industries/commerce-logistics-growing-organisations`
- [ ] `/privacy`
- [ ] `/terms`
- [ ] `/cookies`

### Supporting experiences

- [ ] custom 404 returns HTTP 404;
- [ ] project-enquiry confirmation is non-indexed;
- [ ] document-request confirmation is non-indexed;
- [ ] recoverable form-error experience is non-indexed;
- [ ] cookie preference interface matches actual storage behaviour.

### Navigation

- [ ] primary navigation order matches the locked architecture;
- [ ] Capabilities mega-menu contains all approved destinations and no extras;
- [ ] Industries menu contains exactly six sector routes plus overview;
- [ ] Discuss a Project remains the primary action;
- [ ] Resources provides the capability-statement route;
- [ ] breadcrumbs are present and correct on internal pages;
- [ ] active-page indication is accurate;
- [ ] footer destinations are complete and non-broken;
- [ ] no empty future section is publicly linked.

## 7. Content gate

For every public page:

- [ ] browser title matches the approved metadata matrix;
- [ ] meta description is unique and accurate;
- [ ] exactly one clear H1 is present;
- [ ] section order matches the content specification;
- [ ] final copy is grammatically correct and uses consistent terminology;
- [ ] calls to action use approved labels and correct routes;
- [ ] page answers a distinct buyer or evaluator question;
- [ ] examples are labelled as representative, not completed projects;
- [ ] no unsupported superlative appears;
- [ ] no invented client, project, certification, partner or scale claim appears;
- [ ] contact and company facts match the factual register;
- [ ] legal copy matches actual implementation;
- [ ] no placeholder, lorem ipsum, “coming soon” or draft note is public;
- [ ] no unfinished Techgrity product is exposed unless separately approved.

## 8. Visual fidelity gate

At each required viewport:

- [ ] page matches the approved master visual in hierarchy and composition;
- [ ] logo is the approved standalone asset and is not distorted;
- [ ] header and utility bar proportions are correct;
- [ ] hero image crop preserves the intended subject;
- [ ] hero text remains legible against imagery;
- [ ] typography sizes and line wraps remain intentional;
- [ ] section spacing follows the visual system;
- [ ] card sizes, borders, radii and shadows are consistent;
- [ ] CTA hierarchy is visually clear;
- [ ] icons use one consistent style;
- [ ] diagrams remain legible;
- [ ] no image is stretched, pixelated or incorrectly cropped;
- [ ] footer is complete and aligned;
- [ ] no horizontal page overflow exists;
- [ ] no content is obscured by sticky navigation;
- [ ] no unintended layout shift is visible;
- [ ] empty states and error states are designed, not browser defaults.

Required viewports:

- [ ] 390 × 844 mobile;
- [ ] 768 × 1024 tablet portrait;
- [ ] 1024 × 1366 tablet or compact desktop;
- [ ] 1440 × 900 desktop;
- [ ] 1672 × 941 reference desktop;
- [ ] 1920 × 1080 large desktop.

## 9. Responsive behaviour gate

- [ ] utility bar simplifies without awkward wrapping;
- [ ] mobile menu opens, closes and scrolls correctly;
- [ ] nested mobile navigation remains clear;
- [ ] split heroes stack in the approved order;
- [ ] homepage hero retains people and infrastructure meaning on mobile;
- [ ] cards reflow without tiny columns or truncated essential text;
- [ ] matrices convert to usable mobile structures;
- [ ] diagrams have mobile-specific layouts or accessible alternatives;
- [ ] forms become one column where appropriate;
- [ ] tables remain readable or deliberately scrollable;
- [ ] buttons meet touch-size expectations;
- [ ] zoom to 200% does not lose content or functionality;
- [ ] reflow at 320 CSS px remains usable where WCAG requires it.

## 10. Accessibility gate

### Automated checks

- [ ] no critical accessibility violations on representative pages;
- [ ] colour-contrast automation passes known text and controls;
- [ ] form labels and accessible names are detected;
- [ ] heading hierarchy contains no unexplained structural errors;
- [ ] landmarks are present;
- [ ] image alternatives are present or deliberately empty.

### Manual keyboard checks

- [ ] skip link works;
- [ ] all navigation is keyboard operable;
- [ ] dropdowns expose and close predictably;
- [ ] visible focus never disappears;
- [ ] focus order follows reading order;
- [ ] focus is restored after mobile menu or dialog closure;
- [ ] all form fields, checkboxes and buttons are usable;
- [ ] no keyboard trap exists;
- [ ] error summary and linked field errors work;
- [ ] cookie controls are fully keyboard usable.

### Screen-reader-oriented checks

- [ ] page title is meaningful;
- [ ] landmarks and headings support navigation;
- [ ] menus and expanders expose state;
- [ ] form instructions and errors are announced;
- [ ] success and failure status messages are announced appropriately;
- [ ] diagrams have a complete text alternative;
- [ ] repeated decorative images are hidden appropriately;
- [ ] link text makes sense outside surrounding paragraphs.

### Motion and sensory checks

- [ ] reduced-motion preference is honoured;
- [ ] no critical information relies on colour alone;
- [ ] no autoplay audio exists;
- [ ] animation does not flash or interfere with reading;
- [ ] hover is never the only way to reveal information.

## 11. Form and integration gate

### General enquiry

- [ ] valid submission succeeds through the server-side path;
- [ ] required fields are enforced client-side and server-side;
- [ ] invalid email is rejected safely;
- [ ] long or malformed input is handled safely;
- [ ] privacy consent is explicit and unchecked by default;
- [ ] bot trap and rate limits function;
- [ ] visitor sees an accessible confirmation;
- [ ] approved recipient receives the correctly formatted notification;
- [ ] no secret or provider detail is exposed;
- [ ] operational logs record outcome without full message content.

### Project enquiry

- [ ] all required fields and approved options exist;
- [ ] conditional fields behave correctly;
- [ ] hidden conditional values are not submitted accidentally;
- [ ] narrative-length limits are enforced;
- [ ] duplicate in-flight submission is prevented;
- [ ] valid request routes to the approved owner;
- [ ] safe reference identifier is returned;
- [ ] recoverable failure preserves safe entered values;
- [ ] direct contact fallback is available;
- [ ] file upload remains disabled unless the complete secure-upload gate passes.

### Document requests and downloads

- [ ] every displayed file exists;
- [ ] title, type, version and date are correct;
- [ ] direct downloads return the expected file and content type;
- [ ] request-only documents use the approved workflow;
- [ ] obsolete file URLs redirect or are removed safely;
- [ ] no “coming soon” document card is displayed;
- [ ] document request confirmation is non-indexed;
- [ ] download and request handling matches the Privacy Policy.

## 12. Security and privacy gate

- [ ] HTTPS is enforced;
- [ ] TLS certificate and chain validate publicly;
- [ ] HTTP redirects to the canonical HTTPS host;
- [ ] no credentials, private keys or secrets exist in repository or built assets;
- [ ] server-side input validation and sanitisation pass adversarial tests;
- [ ] request-size limits are enforced;
- [ ] rate limiting and abuse controls are active;
- [ ] security headers are present and do not break required functions;
- [ ] cookies use appropriate `Secure`, `HttpOnly` and `SameSite` attributes where applicable;
- [ ] consent behaviour matches actual non-essential storage;
- [ ] reject and change-preference options work;
- [ ] personal data is absent from URLs and analytics events;
- [ ] application logs redact or omit personal message content;
- [ ] retention periods and access ownership are approved;
- [ ] test data is removed from production systems;
- [ ] third-party dependencies and scripts are inventoried;
- [ ] file uploads are absent or fully secured and approved.

## 13. SEO gate

- [ ] all 31 public pages have unique final titles;
- [ ] all 31 public pages have unique final descriptions;
- [ ] canonical URLs use the approved HTTPS host;
- [ ] Open Graph metadata is complete;
- [ ] social images are approved and resolve successfully;
- [ ] structured data validates and contains only verified facts;
- [ ] breadcrumbs are represented correctly where structured data is used;
- [ ] XML sitemap contains only canonical indexable public pages;
- [ ] robots file references the sitemap and does not expose sensitive paths;
- [ ] confirmation and error pages use `noindex`;
- [ ] legacy redirects are permanent, one-hop and correct;
- [ ] internal links are descriptive and non-broken;
- [ ] no thin or duplicate capability page remains;
- [ ] informative images have accurate alt text and meaningful filenames.

## 14. Performance gate

Test representative homepage, capability, industry, Resources and form pages on production-equivalent delivery.

- [ ] Largest Contentful Paint target is at or below 2.5 seconds at the 75th percentile where measurable;
- [ ] Interaction to Next Paint target is at or below 200 ms at the 75th percentile;
- [ ] Cumulative Layout Shift is at or below 0.1;
- [ ] hero and other LCP images are correctly prioritised;
- [ ] below-the-fold images are lazy-loaded appropriately;
- [ ] responsive image variants are served;
- [ ] modern compressed formats are used;
- [ ] explicit image dimensions prevent layout shift;
- [ ] font loading avoids invisible text and severe shift;
- [ ] no unnecessary blocking third-party script exists;
- [ ] JavaScript is limited to required interactions;
- [ ] compression and caching are correctly configured;
- [ ] forms remain usable on throttled mobile network conditions;
- [ ] no page ships an unjustified large video or animation payload.

## 15. Browser and device gate

Verify current stable versions of:

- [ ] Chrome desktop;
- [ ] Edge desktop;
- [ ] Firefox desktop;
- [ ] Safari desktop;
- [ ] mobile Safari on iOS;
- [ ] Chrome on Android.

For each:

- [ ] page renders without material layout defects;
- [ ] navigation and dropdowns work;
- [ ] forms validate and submit;
- [ ] focus and keyboard behaviour remain usable;
- [ ] image formats and fallbacks load;
- [ ] sticky header, dialogs and mobile menu behave correctly;
- [ ] no console error indicates broken user functionality.

## 16. Content and asset integrity gate

- [ ] all images appear in the asset register;
- [ ] source, licence or generated provenance is recorded;
- [ ] desktop and mobile crops are approved;
- [ ] no visible unauthorised trademark exists;
- [ ] no representative image is labelled as a Techgrity project;
- [ ] all documents appear in the resource register;
- [ ] document versions and dates are current;
- [ ] broken-link scan passes;
- [ ] missing-asset scan passes;
- [ ] no source map, backup file, private document or development artefact is publicly exposed;
- [ ] favicon, manifest and social images are correct.

## 17. Build and release gate

- [ ] dependency installation is deterministic;
- [ ] production build succeeds from a clean checkout;
- [ ] linting and static validation pass;
- [ ] route and link checks pass;
- [ ] interaction tests pass;
- [ ] form integration tests pass against a controlled environment;
- [ ] accessibility automation passes the agreed threshold;
- [ ] final built output is tied to the reviewed commit;
- [ ] deployment configuration contains no plaintext secret;
- [ ] staging and production credentials are separated;
- [ ] rollback procedure is documented and tested where practical;
- [ ] release notes identify known limitations and resolved blockers.

## 18. Public deployment and commissioning gate

- [ ] DNS resolves from the public internet;
- [ ] production hostname serves the approved release;
- [ ] TLS validates publicly;
- [ ] canonical redirects behave correctly;
- [ ] all 31 public routes respond as expected;
- [ ] custom 404 responds with HTTP 404;
- [ ] forms route to real approved recipients;
- [ ] visitor acknowledgements, if enabled, deliver correctly;
- [ ] downloads work from the public site;
- [ ] cookie and privacy behaviour matches production scripts;
- [ ] monitoring detects route, TLS and form failures;
- [ ] alerts reach the approved operational owner;
- [ ] public visual screenshots are captured at required viewports;
- [ ] production performance evidence is recorded;
- [ ] no staging banner, test address, test analytics or synthetic content remains;
- [ ] the deployed commit SHA and deployment timestamp are recorded.

## 19. Completion decision

The website may be declared complete only when:

- all governing documentation is current;
- all master visuals are approved;
- all public and system routes pass;
- all factual blockers are resolved or omitted;
- responsive and accessibility evidence is complete;
- forms, documents and integrations work in production;
- SEO, security, privacy and performance gates pass;
- public DNS, TLS and monitoring are directly proven;
- the implementation visually matches approved references;
- no unsupported claim remains;
- an authorised final acceptance decision is recorded against the exact deployed release.

A merged pull request, successful build or attractive screenshot alone is not completion.