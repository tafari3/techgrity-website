# Techgrity Systems Website Architecture

**Status:** LOCKED  
**Decision date:** 29 July 2026  
**Authority:** Techgrity Systems corporate website baseline  
**Change control:** Any change to the sitemap, URL hierarchy, primary navigation, division structure or master-template system must be recorded in this document before implementation.

## 1. Corporate positioning

Techgrity Systems will be presented as one accountable Zimbabwean technology and engineering company with two specialist divisions and one integrated delivery capability:

1. **Digital Systems & AI**
2. **Infrastructure & Engineering**
3. **Technology Supply & Project Delivery**

Primary positioning:

> **Digital systems. Critical infrastructure. One accountable partner.**

Supporting proposition:

> Techgrity Systems designs, builds, integrates and supports software platforms, networks, data centres, telecommunications, power systems and technical infrastructure for organisations across Zimbabwe and Africa.

The website must communicate breadth without appearing to be an unfocused general supplier, a small web-design agency, an equipment catalogue or a construction company.

## 2. Architecture decision

The launch website will use:

- one corporate domain: `techgrity.co.zw`;
- one shared brand, navigation and design system;
- 31 intentional public pages;
- supporting system pages that remain outside the main navigation;
- hierarchical capability URLs under `/capabilities/`;
- six focused industry sectors;
- 13 authoritative master page templates;
- no fabricated case studies, certifications, client logos, partner status, scale claims or project statistics.

Separate domains or disconnected divisional websites are explicitly rejected for launch.

## 3. Primary navigation

1. Home
2. Capabilities
3. Industries
4. How We Deliver
5. Company
6. Resources
7. Contact

Primary call to action:

- **Discuss a Project**

Secondary call to action:

- **Download Capability Statement**

Where a direct download is not appropriate, the secondary action must open the document request area within Resources.

## 4. Public sitemap

### 4.1 Core corporate pages

| # | Page | Canonical URL | Primary purpose |
|---:|---|---|---|
| 1 | Home | `/` | Present the full corporate proposition and route visitors into the two divisions. |
| 2 | Capabilities | `/capabilities` | Explain the complete capability portfolio and how the areas connect. |
| 3 | Industries | `/industries` | Present the six launch sectors and integrated sector solutions. |
| 4 | How We Deliver | `/how-we-deliver` | Explain the governed end-to-end delivery lifecycle. |
| 5 | Company | `/company` | Establish identity, operating principles, local presence and verifiable credibility. |
| 6 | Resources | `/resources` | Provide capability statements, corporate documents, policies and document requests. |
| 7 | Contact | `/contact` | Provide confirmed contact information and general enquiry routing. |
| 8 | Discuss a Project | `/discuss-a-project` | Capture qualified project requirements and route them to business development. |

### 4.2 Digital Systems & AI

| # | Page | Canonical URL |
|---:|---|---|
| 9 | Digital Systems & AI | `/capabilities/digital-systems` |
| 10 | Software, AI & Enterprise Applications | `/capabilities/digital-systems/software-ai-applications` |
| 11 | Workflow & Process Automation | `/capabilities/digital-systems/automation` |
| 12 | Systems Integration | `/capabilities/digital-systems/integration` |
| 13 | Data Platforms & Analytics | `/capabilities/digital-systems/data-analytics` |
| 14 | Cybersecurity & Digital Access | `/capabilities/digital-systems/cybersecurity-access` |

### 4.3 Infrastructure & Engineering

| # | Page | Canonical URL |
|---:|---|---|
| 15 | Infrastructure & Engineering | `/capabilities/infrastructure` |
| 16 | Networks & Fibre | `/capabilities/infrastructure/networks-fibre` |
| 17 | Data Centres & Cloud | `/capabilities/infrastructure/data-centres-cloud` |
| 18 | Telecom & Radio Infrastructure | `/capabilities/infrastructure/telecom-radio` |
| 19 | Power & Energy | `/capabilities/infrastructure/power-energy` |
| 20 | Security & Smart Facilities | `/capabilities/infrastructure/security-smart-facilities` |
| 21 | Civil & Technical Infrastructure | `/capabilities/infrastructure/civil-technical-works` |

### 4.4 Technology supply and project delivery

| # | Page | Canonical URL |
|---:|---|---|
| 22 | Technology Supply & Integration | `/capabilities/technology-supply` |

### 4.5 Industries

| # | Page | Canonical URL |
|---:|---|---|
| 23 | Government & Public Sector | `/industries/government-public-sector` |
| 24 | Education & Research | `/industries/education-research` |
| 25 | Telecommunications | `/industries/telecommunications` |
| 26 | Energy, Utilities & Industrial Operations | `/industries/energy-utilities-industrial` |
| 27 | Data Centres & Technology Organisations | `/industries/data-centres-technology` |
| 28 | Commerce, Logistics & Growing Organisations | `/industries/commerce-logistics-growing-organisations` |

### 4.6 Legal pages

| # | Page | Canonical URL |
|---:|---|---|
| 29 | Privacy Policy | `/privacy` |
| 30 | Terms of Use | `/terms` |
| 31 | Cookie Policy | `/cookies` |

## 5. Supporting system pages

These are required but must not appear in the primary navigation:

- `/404`
- `/project-enquiry-received`
- `/document-request-received`
- `/form-error`
- cookie-preference interface

The implementation must also include:

- `sitemap.xml`;
- `robots.txt`;
- canonical metadata;
- structured data appropriate to the verified company information;
- social-sharing metadata;
- redirects for superseded or legacy routes.

## 6. Capabilities mega-menu

### Digital Systems & AI

- Digital Systems overview
- Software, AI & Enterprise Applications
- Workflow & Process Automation
- Systems Integration
- Data Platforms & Analytics
- Cybersecurity & Digital Access

### Infrastructure & Engineering

- Infrastructure overview
- Networks & Fibre
- Data Centres & Cloud
- Telecom & Radio Infrastructure
- Power & Energy
- Security & Smart Facilities
- Civil & Technical Infrastructure

### Supply and delivery

- Technology Supply & Integration
- How We Deliver
- Discuss a Project

The mega-menu must remain structured and text-led. It must not become a dense grid of decorative service icons.

## 7. Industries menu

- Industries overview
- Government & Public Sector
- Education & Research
- Telecommunications
- Energy, Utilities & Industrial Operations
- Data Centres & Technology Organisations
- Commerce, Logistics & Growing Organisations

## 8. Master page templates

The 31 public pages will be produced from 13 authoritative master templates:

1. Homepage
2. Capabilities overview
3. Digital Systems landing
4. Digital capability detail
5. Infrastructure landing
6. Infrastructure capability detail
7. Technology Supply & Integration
8. Industries overview
9. Industry detail
10. How We Deliver
11. Company
12. Resources
13. Contact and enquiry forms

The homepage visual direction has already been established. The remaining master templates must be specified and approved before the corresponding page families are implemented.

## 9. Future-ready but unpublished sections

The technical architecture should permit these later sections without publishing empty pages at launch:

- `/projects`
- `/projects/{project-slug}`
- `/partners`
- `/insights`
- `/careers`
- `/certifications`

They may only be published when genuine, approved content exists.

## 10. Explicit launch exclusions

The launch website must not include:

- unfinished product pages;
- fabricated case studies or testimonials;
- fake project figures;
- unverified client, partner or certification logos;
- an equipment catalogue or e-commerce system;
- public pricing tables;
- an empty careers section;
- an empty news or insights section;
- generic AI robot imagery;
- invented office locations or unsupported claims about organisational scale.

## 11. Locked decision

This architecture is the controlling baseline for all subsequent content, design, development, QA and deployment work. Implementation must not silently add, remove, rename or relocate pages. Any proposed deviation must first be assessed for user clarity, tender relevance, SEO value, evidence requirements and maintenance cost, then recorded as an explicit revision to this document.
