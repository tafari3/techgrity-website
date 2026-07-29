# Techgrity Systems SEO and Metadata Matrix

**Status:** BASELINE COMPLETE  
**Version:** 1.0  
**Date:** 29 July 2026  
**Depends on:** [`01-website-architecture.md`](01-website-architecture.md), [`content-specification/README.md`](content-specification/README.md)

## 1. Purpose

This document defines the canonical metadata baseline for every launch page. It is intended to prevent duplicate titles, thin descriptions, inconsistent URLs and unsupported structured-data claims.

All metadata remains subject to final copy QA and verified company facts before publication.

## 2. Global SEO rules

Every indexable page must include:

- one canonical URL on `https://techgrity.co.zw`;
- one unique browser title;
- one unique meta description;
- one clear H1;
- logical H2–H4 hierarchy;
- useful internal links;
- Open Graph title, description, URL and image;
- Twitter/X card metadata using the same factual content, regardless of whether Techgrity maintains an account;
- inclusion in `sitemap.xml`;
- appropriate `robots` handling;
- structured data only where supported by verified facts.

Rules:

- no keyword stuffing;
- no location stuffing;
- no fabricated “leading”, “best”, “number one” or scale claims;
- no repeated descriptions across capability pages;
- do not publish thin pages merely to target a phrase;
- representative project types must not be marked up as completed projects;
- search snippets must accurately describe visible page content;
- titles should generally remain within 45–65 characters where practical;
- descriptions should generally remain within 135–165 characters where practical;
- page titles use the separator `|` before `Techgrity Systems` where the brand is not already first.

## 3. Canonical and indexation rules

- preferred protocol: `https`;
- preferred host: `techgrity.co.zw`;
- canonical URLs use no trailing slash except the homepage unless the implementation platform requires a single consistent alternative;
- all HTTP, `www` and legacy variants redirect permanently to the canonical host and path;
- query-string variants for campaigns, forms or analytics canonicalise to the clean route where appropriate;
- confirmation and error pages are `noindex, follow`;
- cookie preference UI is not a separate indexable search page;
- XML sitemap includes only canonical, indexable public pages;
- legal pages remain indexable unless legal review directs otherwise;
- unpublished future sections must return 404 or remain inaccessible, not appear as empty indexable pages.

## 4. Structured-data baseline

### 4.1 Site-wide

Use only after factual fields are confirmed:

- `Organization` or a more specific appropriate organisation type;
- `WebSite`;
- `BreadcrumbList` on internal pages.

Potential organisation fields:

- legal name;
- approved trading name;
- canonical URL;
- approved logo URL;
- confirmed telephone;
- confirmed business email;
- verified postal or physical address;
- verified registration information where structurally appropriate;
- verified social profiles only.

Do not add:

- aggregate ratings;
- reviews;
- awards;
- certifications;
- employee counts;
- founding dates;
- partner relationships;
- service areas beyond approved wording;

unless verified and appropriate for the schema type.

### 4.2 Page-specific

- capability and industry pages: `WebPage` or `Service` only when service content and provider facts are complete;
- Resources: `CollectionPage`; individual downloadable documents may use `DigitalDocument` where useful;
- Contact: `ContactPage`;
- Company: `AboutPage`;
- legal pages: `WebPage`;
- enquiry form: `WebPage`; do not expose personal form submissions in structured data.

## 5. Social metadata

Each indexable page requires:

- `og:type=website`;
- canonical `og:url`;
- unique `og:title` and `og:description` aligned with the browser metadata;
- approved 1200 × 630 image;
- image width and height;
- useful image alternative text where supported;
- `twitter:card=summary_large_image`.

The social image must not contain unsupported client logos, certifications or claims.

## 6. Public-page metadata matrix

| # | Route | Browser title | Meta description | Primary search intent | Schema direction |
|---:|---|---|---|---|---|
| 1 | `/` | `Techgrity Systems | Digital Systems & Critical Infrastructure` | `Techgrity Systems designs and integrates software, AI, networks, data centres, telecommunications, power and technical infrastructure.` | Techgrity Systems; integrated technology company Zimbabwe | `WebPage`, `Organization`, `WebSite` |
| 2 | `/capabilities` | `Technology Capabilities | Techgrity Systems` | `Explore Techgrity capabilities across software, AI, automation, networks, fibre, data centres, telecoms, power and technical infrastructure.` | integrated technology capabilities | `CollectionPage`, `BreadcrumbList` |
| 3 | `/industries` | `Industries We Support | Techgrity Systems` | `See how Techgrity combines digital systems and infrastructure for government, education, telecoms, energy, technology and commerce.` | technology solutions by industry | `CollectionPage`, `BreadcrumbList` |
| 4 | `/how-we-deliver` | `How We Deliver Technology Projects | Techgrity Systems` | `Understand Techgrity's governed process from discovery and design through sourcing, integration, commissioning, handover and support.` | technology project delivery methodology | `WebPage`, `BreadcrumbList` |
| 5 | `/company` | `Company | Techgrity Systems Zimbabwe` | `Learn about Techgrity Systems, its Digital Systems and Infrastructure divisions, accountable delivery principles and Zimbabwe-based support.` | Techgrity Systems company Zimbabwe | `AboutPage`, `BreadcrumbList` |
| 6 | `/resources` | `Capability Statements & Resources | Techgrity Systems` | `Access Techgrity capability statements, delivery information, approved company documents and document-request options.` | Techgrity capability statement | `CollectionPage`, `BreadcrumbList` |
| 7 | `/contact` | `Contact Techgrity Systems` | `Contact Techgrity Systems in Harare for digital systems, infrastructure, technology supply and general business enquiries.` | contact Techgrity Systems | `ContactPage`, `BreadcrumbList` |
| 8 | `/discuss-a-project` | `Discuss a Technology Project | Techgrity Systems` | `Share your software, network, data-centre, telecom, power or integrated infrastructure requirement with Techgrity Systems.` | technology project enquiry Zimbabwe | `WebPage`, `BreadcrumbList` |
| 9 | `/capabilities/digital-systems` | `Digital Systems & AI | Techgrity Systems` | `Explore custom software, AI, automation, systems integration, data platforms and secure digital access for operational organisations.` | digital systems and AI Zimbabwe | `Service`, `BreadcrumbList` |
| 10 | `/capabilities/digital-systems/software-ai-applications` | `Software, AI & Enterprise Applications | Techgrity Systems` | `Techgrity designs custom software, governed AI solutions, web and mobile applications, enterprise platforms and institutional systems.` | custom software and AI solutions Zimbabwe | `Service`, `BreadcrumbList` |
| 11 | `/capabilities/digital-systems/automation` | `Workflow & Process Automation | Techgrity Systems` | `Digitise approvals, task routing, evidence, notifications, audit trails and reporting through controlled workflow automation.` | workflow and process automation Zimbabwe | `Service`, `BreadcrumbList` |
| 12 | `/capabilities/digital-systems/integration` | `Systems Integration | Techgrity Systems` | `Connect applications, APIs, identity services, legacy systems and data exchanges through governed systems integration.` | systems integration services Zimbabwe | `Service`, `BreadcrumbList` |
| 13 | `/capabilities/digital-systems/data-analytics` | `Data Platforms & Analytics | Techgrity Systems` | `Design data architecture, integration, dashboards, reporting, governance and decision-support platforms for operational visibility.` | data platforms and analytics Zimbabwe | `Service`, `BreadcrumbList` |
| 14 | `/capabilities/digital-systems/cybersecurity-access` | `Cybersecurity & Digital Access | Techgrity Systems` | `Strengthen identity, authentication, role-based access, auditability and security-conscious implementation across digital systems.` | identity access and cybersecurity Zimbabwe | `Service`, `BreadcrumbList` |
| 15 | `/capabilities/infrastructure` | `Infrastructure & Engineering | Techgrity Systems` | `Explore enterprise networks, fibre, data centres, telecoms, power, security, smart facilities and technical infrastructure delivery.` | ICT infrastructure and engineering Zimbabwe | `Service`, `BreadcrumbList` |
| 16 | `/capabilities/infrastructure/networks-fibre` | `Networks & Fibre | Techgrity Systems` | `Design and implement enterprise networks, fibre-optic infrastructure, structured cabling, wireless connectivity and network monitoring.` | network and fibre services Zimbabwe | `Service`, `BreadcrumbList` |
| 17 | `/capabilities/infrastructure/data-centres-cloud` | `Data Centres & Cloud | Techgrity Systems` | `Plan and integrate data-centre environments, servers, storage, virtualisation, backup, monitoring and hybrid cloud infrastructure.` | data centre and cloud infrastructure Zimbabwe | `Service`, `BreadcrumbList` |
| 18 | `/capabilities/infrastructure/telecom-radio` | `Telecom & Radio Infrastructure | Techgrity Systems` | `Deliver telecom, radio, microwave, backhaul, tower and base-station infrastructure with integration and commissioning controls.` | telecom and radio infrastructure Zimbabwe | `Service`, `BreadcrumbList` |
| 19 | `/capabilities/infrastructure/power-energy` | `Power & Energy Systems | Techgrity Systems` | `Improve technology resilience with UPS, backup power, solar, batteries, hybrid energy, distribution and power monitoring solutions.` | backup power and solar systems Zimbabwe | `Service`, `BreadcrumbList` |
| 20 | `/capabilities/infrastructure/security-smart-facilities` | `Security & Smart Facilities | Techgrity Systems` | `Integrate CCTV, physical access control, monitoring, sensors, alarms and smart-facility systems with operational technology.` | CCTV access control smart facilities Zimbabwe | `Service`, `BreadcrumbList` |
| 21 | `/capabilities/infrastructure/civil-technical-works` | `Civil & Technical Infrastructure | Techgrity Systems` | `Coordinate technical rooms, equipment shelters, foundations, pathways, mounting structures, site preparation and controlled fit-outs.` | technical civil works Zimbabwe | `Service`, `BreadcrumbList` |
| 22 | `/capabilities/technology-supply` | `Technology Supply & Integration | Techgrity Systems` | `Move from requirements and specifications to sourcing, installation, configuration, integration, commissioning and operational handover.` | technology supply and integration Zimbabwe | `Service`, `BreadcrumbList` |
| 23 | `/industries/government-public-sector` | `Technology for Government & Public Sector | Techgrity Systems` | `Explore accountable digital platforms, secure networks, data-centre infrastructure, communications, access control and power resilience.` | government technology solutions Zimbabwe | `Service` or `WebPage`, `BreadcrumbList` |
| 24 | `/industries/education-research` | `Technology for Education & Research | Techgrity Systems` | `Connect institutional platforms, campus networks, learning systems, research computing, access control and resilient infrastructure.` | education and research technology Zimbabwe | `Service` or `WebPage`, `BreadcrumbList` |
| 25 | `/industries/telecommunications` | `Technology for Telecommunications | Techgrity Systems` | `Support telecom operations with network infrastructure, radio and microwave systems, site power, field workflows and monitoring platforms.` | telecommunications infrastructure solutions | `Service` or `WebPage`, `BreadcrumbList` |
| 26 | `/industries/energy-utilities-industrial` | `Technology for Energy, Utilities & Industry | Techgrity Systems` | `Combine operational platforms, field workflows, connectivity, communications, monitoring, power resilience and technical facilities.` | technology for energy utilities industry | `Service` or `WebPage`, `BreadcrumbList` |
| 27 | `/industries/data-centres-technology` | `Technology for Data Centres & Technology Organisations` | `Integrate compute, storage, virtualisation, networks, power, monitoring, security, technical rooms and operational platforms.` | data centre technology solutions Zimbabwe | `Service` or `WebPage`, `BreadcrumbList` |
| 28 | `/industries/commerce-logistics-growing-organisations` | `Technology for Commerce, Logistics & Growing Organisations` | `Scale operations with software, mobile workflows, integration, connectivity, security, data visibility, power resilience and support.` | technology for logistics commerce and SMEs | `Service` or `WebPage`, `BreadcrumbList` |
| 29 | `/privacy` | `Privacy Policy | Techgrity Systems` | `Read how Techgrity Systems collects, uses, protects and retains personal information through its website and enquiry processes.` | Techgrity privacy policy | `WebPage`, `BreadcrumbList` |
| 30 | `/terms` | `Website Terms of Use | Techgrity Systems` | `Read the terms governing use of the Techgrity Systems website, its content, downloads, enquiries and external links.` | Techgrity terms of use | `WebPage`, `BreadcrumbList` |
| 31 | `/cookies` | `Cookie Policy | Techgrity Systems` | `Understand the cookies and similar technologies used by the Techgrity Systems website and how preferences can be managed.` | Techgrity cookie policy | `WebPage`, `BreadcrumbList` |

## 7. Supporting system pages

| Route or experience | Title | Robots | Canonical | Notes |
|---|---|---|---|---|
| `/404` | `Page Not Found | Techgrity Systems` | `noindex, follow` | self-canonical or omit canonical according to implementation |
| `/project-enquiry-received` | `Project Enquiry Received | Techgrity Systems` | `noindex, follow` | reachable only after a valid submission flow where practical |
| `/document-request-received` | `Document Request Received | Techgrity Systems` | `noindex, follow` | must not expose request data in URL or metadata |
| `/form-error` | `We Could Not Submit Your Request | Techgrity Systems` | `noindex, follow` | preserve recoverable form state where technically possible |
| cookie preference interface | not a standalone search page | not applicable | not applicable | use an accessible dialog, panel or dedicated non-indexed route if required |

## 8. Heading and content rules

- exactly one page H1 unless a documented framework constraint requires another accessible pattern;
- navigation logo text does not count as page heading;
- headings describe sections, not visual styling;
- do not skip levels for appearance;
- capability pages must contain enough distinct content to justify indexation;
- industry pages must answer sector-specific operating questions and not merely replace the industry name in generic copy;
- legal headings must reflect final reviewed legal content.

## 9. Internal-link framework

### Global

Every standard page links to:

- the most relevant capability or industry routes;
- `/how-we-deliver` where delivery controls matter;
- `/discuss-a-project` as the primary conversion route;
- `/resources` where capability statements support evaluation.

### Capability pages

Link to:

- capability landing page;
- two to four genuinely related capabilities;
- relevant industries;
- How We Deliver;
- project enquiry.

### Industry pages

Link to:

- Industries overview;
- relevant digital and infrastructure capabilities;
- How We Deliver;
- project enquiry.

Anchor text must describe the destination. Avoid repeated generic labels such as “click here”.

## 10. Image-search metadata

- informative images use concise, accurate alt text;
- decorative images use empty alt text;
- filenames describe page, role and subject;
- image captions are used only when they add information;
- do not claim a representative image is a Techgrity project;
- `ImageObject` markup is optional and only useful where image provenance and visible content justify it.

## 11. XML sitemap requirements

The generated sitemap must:

- contain the 31 canonical public URLs only;
- exclude confirmation, error, cookie-interface and future unpublished routes;
- use the canonical HTTPS host;
- include accurate `lastmod` values only when implementation can maintain them;
- omit fake change frequencies and priorities unless there is a reasoned operational use;
- update automatically or through a documented release step when routes change.

## 12. Robots requirements

`robots.txt` must:

- permit crawling of public assets required to render pages;
- reference the XML sitemap;
- not be used as a security control;
- not expose secret or sensitive paths;
- avoid blocking pages that carry `noindex` before crawlers can see the directive.

## 13. Redirect register baseline

Before launch, record all superseded routes from the prior website. At minimum, review and map likely legacy paths such as:

- `/digital-systems` → `/capabilities/digital-systems`;
- `/infrastructure` → `/capabilities/infrastructure`;
- `/technology-supply` → `/capabilities/technology-supply`;
- `/delivery` → `/how-we-deliver`.

Every redirect must be tested for one-hop behaviour, correct status and canonical destination. Unknown legacy paths must be discovered from the existing site, analytics if available and server logs where authorised.

## 14. SEO acceptance criteria

SEO is accepted only when:

- every indexable page has unique final metadata;
- all canonicals use the approved production host and route;
- sitemap and robots behaviour are correct;
- no supporting system page is accidentally indexable;
- structured data validates and contains only verified facts;
- headings are logical and page-specific;
- internal links are useful and non-broken;
- pages contain distinct substantive content;
- social cards render with approved images and text;
- redirects from superseded routes are complete and one hop;
- no metadata contains unsupported clients, partners, certifications, project outcomes or scale claims.

## 15. Final factual dependencies

Before production metadata is frozen, confirm:

- legal company name;
- approved company description;
- confirmed telephone and business email;
- approved public location or address;
- production canonical host and redirect policy;
- approved logo and social-sharing image URLs;
- whether any verified social profiles should appear in organisation data;
- whether service-area wording should be Zimbabwe, Southern Africa, Africa or another approved scope;
- final legal and privacy wording;
- final download names and publication dates.