# Techgrity Systems Website Documentation

This directory is the authoritative source of truth for the Techgrity Systems corporate website programme.

## Controlling documents

| Document | Status | Purpose |
|---|---|---|
| [`01-website-architecture.md`](01-website-architecture.md) | **Locked** | Defines the 31-page sitemap, URL hierarchy, navigation, master templates and launch exclusions. |
| [`02-master-website-specification.md`](02-master-website-specification.md) | **Baseline** | Defines business, user, design, content, functional, accessibility, SEO, security, performance and acceptance requirements. |
| [`content-specification/README.md`](content-specification/README.md) | **Baseline complete** | Defines the content role, message hierarchy, section order, CTAs, imagery requirements, factual dependencies and acceptance criteria for all 31 public pages and five supporting system experiences. |
| [`03-visual-design-system.md`](03-visual-design-system.md) | **Locked for master visuals** | Defines colour, type, spacing, grid, components, responsive behaviour, divisional expression and implementation tokens. |
| [`04-image-art-direction-brief.md`](04-image-art-direction-brief.md) | **Locked for master visuals** | Defines image purpose, technical accuracy, page-by-page subjects, crops, provenance, alt text and approval rules. |
| [`05-seo-metadata-matrix.md`](05-seo-metadata-matrix.md) | **Baseline complete** | Defines titles, descriptions, canonicals, indexation, structured data, social metadata, sitemap and redirect requirements. |
| [`06-functional-integration-specification.md`](06-functional-integration-specification.md) | **Baseline complete** | Defines navigation, forms, document handling, mail routing, privacy, cookies, security, monitoring and deployment behaviour. |
| [`07-factual-information-register.md`](07-factual-information-register.md) | **Active control register** | Records confirmed, provisional, blocked, omitted and future facts and controls all public claims. |
| [`08-visual-functional-acceptance-checklist.md`](08-visual-functional-acceptance-checklist.md) | **Baseline complete** | Defines evidence required for master visuals, implementation, accessibility, forms, SEO, security, performance and production commissioning. |
| [`09-master-visual-production-plan.md`](09-master-visual-production-plan.md) | **In execution** | Defines production waves, required desktop/mobile outputs, review method, asset structure and implementation handoff conditions for all 13 master templates. |
| [`10-design-stage-decision-log.md`](10-design-stage-decision-log.md) | **Active** | Records material cross-page design, integration and evidence-boundary decisions. |
| [`11-master-visual-approval-register.md`](11-master-visual-approval-register.md) | **Active** | Records the exact review and approval state of every master template. |

## Programme status

### Completed planning baseline

- 31-page public sitemap locked;
- five supporting system experiences specified;
- 13 master page-template families defined;
- exact page-by-page content specifications complete;
- visual design system complete;
- image and art-direction brief complete;
- SEO and metadata baseline complete;
- functional and integration contract complete;
- factual-information control register established;
- visual and functional acceptance checklist complete;
- master-visual production sequence and approval method defined;
- design-stage decision logging established.

### Master-visual production

The homepage is the approved visual benchmark.

Wave 1 has been produced and moved to `REVIEW`:

1. Capabilities overview;
2. Digital Systems landing;
3. Infrastructure landing.

Each Wave 1 template has desktop, tablet, mobile and full-page rendered references, an internal visual-QA record, an approval record and a prototype asset register. Stakeholder approval and repository binary-reference import remain required before any template changes to `APPROVED`.

### Next controlled stage

After Wave 1 approval, produce Wave 2:

1. Digital capability detail;
2. Infrastructure capability detail;
3. Technology Supply & Integration.

Then continue with:

4. Industries overview;
5. Industry detail;
6. How We Deliver;
7. Company;
8. Resources;
9. Contact and enquiry forms.

Every master template requires approved desktop and mobile compositions before the corresponding page family moves into implementation. The production and approval rules are defined in [`09-master-visual-production-plan.md`](09-master-visual-production-plan.md).

## Later controlled deliverables

1. final factual-input decisions;
2. final production copy and legal review;
3. implementation architecture and deployment plan;
4. implementation and integration tests;
5. responsive, accessibility, SEO, security and performance evidence;
6. public deployment and commissioning evidence.

## Governance rule

Planning, visuals, implementation and public claims must remain aligned with the locked architecture and approved specifications. Unknown facts must be recorded as dependencies and must not be invented in public content. A merged pull request, successful build or attractive screenshot does not by itself prove website completion.