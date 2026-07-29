# Techgrity Systems Visual Design System

**Status:** LOCKED FOR MASTER-VISUAL PRODUCTION  
**Version:** 1.0  
**Date:** 29 July 2026  
**Depends on:** [`01-website-architecture.md`](01-website-architecture.md), [`02-master-website-specification.md`](02-master-website-specification.md), [`content-specification/README.md`](content-specification/README.md)

## 1. Purpose

This document converts the approved Techgrity Systems homepage direction and the locked website architecture into one reusable visual system for all 31 public pages, five supporting system experiences and 13 master page-template families.

The controlling direction is:

> **Warm corporate with engineering authority.**

The website must feel technically credible, accountable, locally grounded and calm. It must not resemble a small web-design agency, an equipment catalogue, a speculative AI start-up, a generic construction company or a stock-template corporate site.

## 2. Visual authority and change control

The approved homepage reference and its visually verified implementation establish the benchmark for:

- logo scale and placement;
- utility bar and navigation proportions;
- navy-and-teal brand balance;
- typography character;
- photographic treatment;
- card radius and shadow restraint;
- section density;
- CTA hierarchy;
- responsive quality.

New page visuals may extend this system but may not silently replace it. Any proposed new colour, typeface, component style, visual effect or layout convention must be justified against user clarity, accessibility, brand coherence, implementation cost and long-term maintenance.

## 3. Brand assets

### 3.1 Primary logo

Use the approved standalone horizontal Techgrity Systems logo. The logo must remain a real image or vector asset, never a screenshot crop, flattened header image or reconstructed wordmark.

Rules:

- preserve the original aspect ratio;
- use the full-colour logo on white, ivory and pale neutral backgrounds;
- use an approved reversed or monochrome version only after that asset exists;
- do not recolour individual logo elements;
- do not add shadows, glows, outlines or gradient effects;
- do not place the logo over visually noisy imagery without a controlled background treatment;
- do not combine the logo with unapproved taglines inside the logo lock-up.

### 3.2 Clear space

Minimum clear space around the logo is the height of the internal `T` crossbar or, where implementation needs a numerical rule, at least 12% of the rendered logo width on all sides.

### 3.3 Minimum rendered size

- desktop header: target 236–283 px wide depending on available navigation width;
- tablet header: 190–220 px wide;
- mobile header: 150–178 px wide;
- never render the full horizontal logo below 140 px wide.

A symbol-only treatment may be introduced later only from an approved source asset and only where the full wordmark cannot remain legible.

## 4. Colour system

### 4.1 Core palette

| Token | Value | Intended use |
|---|---|---|
| `navy-950` | `#011631` | deepest backgrounds, overlays and footer depth |
| `navy-900` | `#031A3F` | primary dark brand surface, utility bar and major engineering sections |
| `navy-800` | `#06285C` | secondary navy panels, diagrams and controlled variation |
| `ink-900` | `#06183C` | primary headings and high-emphasis text |
| `teal-700` | `#007575` | accessible body links and normal-size text on white |
| `teal-600` | `#008B8B` | primary interactive emphasis and dark teal accents |
| `teal-500` | `#009A9A` | primary brand fill for buttons, icons and large display accents |
| `cyan-400` | `#38B9C8` | limited display accent, especially hero emphasis |
| `teal-050` | `#E8F5F4` | soft teal backgrounds, hover states and low-emphasis panels |
| `slate-700` | `#5A6372` | body copy and secondary text |
| `slate-500` | `#6C7888` | metadata and tertiary text where contrast remains sufficient |
| `line-300` | `#DCE3EA` | borders, dividers and input outlines |
| `line-200` | `#E0E5EA` | subtle card borders |
| `ivory-050` | `#FBF8F3` | warm corporate section background |
| `warm-100` | `#F4EEE5` | restrained warm panels and editorial sections |
| `cool-050` | `#F7FAFC` | technical light background and data-oriented sections |
| `white` | `#FFFFFF` | cards, header and clean content surfaces |
| `success-600` | `#17795E` | success status and confirmed submission feedback |
| `danger-600` | `#A63838` | error status and destructive feedback |

### 4.2 Colour usage rules

- Navy carries corporate authority and engineering depth.
- Teal carries interaction, integration and digital-system emphasis.
- Cyan is a highlight, not a second primary colour.
- Warm ivory prevents the site from feeling sterile.
- White space must remain dominant on text-heavy and digital-system pages.
- Infrastructure pages may use more navy, but must retain sufficient light surfaces for readability.
- Do not use teal normal-size text on white unless the exact shade meets WCAG AA contrast. Use `teal-700` for body links and reserve `teal-500` for fills, icons, large text or dark-background accents.
- Avoid decorative gradients. Permitted gradients are limited to subtle navy depth, primary CTA variation and approved hero blending.

### 4.3 Approved gradients

Primary teal action:

```css
linear-gradient(135deg, #009A9A 0%, #008B8B 100%)
```

Dark corporate utility surface:

```css
linear-gradient(90deg, #031A3F 0%, #011A3B 54%, #011631 100%)
```

Gradients must never create glowing, neon or futuristic effects.

## 5. Typography

### 5.1 Typeface

Primary stack:

```css
Inter, "Segoe UI", Arial, sans-serif
```

Inter is the intended brand typeface. The implementation must self-host an appropriately licensed subset or use a privacy-reviewed delivery method. It must not depend on an uncontrolled third-party font request at launch.

### 5.2 Weight system

| Role | Weight |
|---|---:|
| body copy | 400–500 |
| navigation and controls | 600–700 |
| section labels | 750–820 |
| card headings | 700–760 |
| major headings | 750–820 |

Avoid ultra-light text and excessive use of 900-weight typography.

### 5.3 Type scale

Use fluid values with explicit minimum and maximum sizes.

| Token | Desktop target | Mobile target | Use |
|---|---:|---:|---|
| `display-1` | 64–84 px | 42–50 px | exceptional corporate landing statements |
| `hero-1` | 44–58 px | 34–42 px | standard page heroes |
| `heading-1` | 40–56 px | 32–40 px | major section headings |
| `heading-2` | 30–40 px | 27–34 px | section groups |
| `heading-3` | 22–28 px | 21–25 px | cards and content blocks |
| `body-lg` | 18–20 px | 17–18 px | hero and section lead copy |
| `body` | 16 px | 16 px | standard body copy |
| `body-sm` | 14 px | 14 px | metadata and support copy |
| `label` | 11–12 px | 11–12 px | uppercase section labels |

### 5.4 Typography behaviour

- Major headings use tight line height: 0.98–1.08.
- Body copy uses 1.55–1.75 line height.
- Use negative letter spacing only on large headings, typically `-0.02em` to `-0.05em`.
- Uppercase section labels use `0.08em` to `0.14em` tracking.
- Paragraph line length should usually remain between 55 and 78 characters.
- Do not centre long-form text. Centred typography is reserved for concise hero and CTA content.
- Avoid widows and orphaned single words in master visuals where line wrapping can be controlled.

## 6. Spacing system

Use an 8 px base rhythm with 4 px increments where fine control is required.

| Token | Value |
|---|---:|
| `space-1` | 4 px |
| `space-2` | 8 px |
| `space-3` | 12 px |
| `space-4` | 16 px |
| `space-5` | 20 px |
| `space-6` | 24 px |
| `space-8` | 32 px |
| `space-10` | 40 px |
| `space-12` | 48 px |
| `space-16` | 64 px |
| `space-18` | 72 px |
| `space-24` | 96 px |
| `space-26` | 104 px |
| `space-32` | 128 px |

Rules:

- standard major section padding: 96–104 px desktop, 72–80 px tablet, 56–64 px mobile;
- compact section padding: 64–72 px desktop, 48–56 px tablet, 40–48 px mobile;
- use larger spacing between conceptual groups than within a group;
- avoid filling whitespace with decorative content;
- internal detail pages may be denser than the homepage, but never cramped.

## 7. Grid and containers

### 7.1 Standard content container

- maximum width: 1240 px;
- desktop side margin: at least 40 px;
- mobile side margin: 20 px;
- wide photographic or matrix sections may extend to 1440–1580 px where the composition requires it;
- text columns should remain narrower than the full container.

### 7.2 Grid

Use a responsive 12-column desktop grid, 8-column tablet grid and 4-column mobile grid.

- desktop gutters: 24–32 px;
- tablet gutters: 20–24 px;
- mobile gutters: 16–20 px.

### 7.3 Breakpoints

Authoritative verification viewports remain:

- 390 × 844;
- 768 × 1024;
- 1024 × 1366;
- 1440 × 900;
- 1672 × 941;
- 1920 × 1080.

Implementation breakpoints should be content-led. Baseline ranges:

- compact mobile: below 480 px;
- mobile: below 720 px;
- tablet: 720–1024 px;
- compact desktop: 1025–1120 px;
- desktop: 1121–1480 px;
- wide desktop: above 1480 px.

## 8. Global shell

### 8.1 Utility bar

- dark navy surface;
- target height: 37–38 px desktop;
- concise approved strapline left;
- email, telephone and location right;
- 11–12 px type;
- utility links must remain interactive and keyboard accessible;
- on narrow mobile, collapse or omit secondary utility content rather than wrap into a tall banner.

### 8.2 Main header

- white background;
- desktop height: approximately 84–98 px;
- logo left, primary navigation right;
- active page shown with teal text or a restrained underline;
- primary CTA remains visually distinct;
- sticky behaviour is allowed only where it does not consume excessive viewport height;
- header shadow must be subtle and may be replaced by a fine border.

### 8.3 Navigation

- text-led, not icon-led;
- desktop navigation uses 14 px semibold text;
- Capabilities uses a structured three-column mega-menu;
- Industries uses a concise text menu;
- dropdowns must operate by keyboard and pointer;
- no hover-only information;
- mobile navigation uses explicit expandable groups and a visible project CTA.

### 8.4 Breadcrumbs

Internal pages use breadcrumbs between the header and hero or within the hero introduction.

- 13–14 px type;
- current page uses plain text;
- separators remain visually quiet;
- breadcrumbs must not replace the page H1.

## 9. Heroes

### 9.1 Homepage hero

The approved homepage hero remains the unique corporate benchmark:

- people and operational context on the left;
- digital or data-centre depth centrally;
- telecom tower and power context on the right;
- dark controlled overlay for legibility;
- centred headline and two CTAs;
- no text baked into imagery.

### 9.2 Internal-page hero

Internal heroes must be simpler than the homepage hero.

Permitted structures:

1. split copy and image;
2. full-width image with controlled navy overlay;
3. editorial copy block with technical diagram;
4. dark navy hero with one restrained photographic panel.

Requirements:

- H1 must remain legible at all viewports;
- show page purpose within the first viewport;
- include one primary CTA and no more than one secondary CTA;
- avoid stacking multiple decorative images;
- standard desktop height: 430–620 px depending on template;
- standard mobile height: content-led, usually 520–680 px when imagery is retained.

## 10. Buttons and links

### 10.1 Primary button

- teal fill or approved teal gradient;
- white text;
- minimum height: 48 px desktop, 48 px mobile;
- horizontal padding: 18–24 px;
- radius: 6–10 px;
- semibold or bold label;
- arrow may reinforce forward navigation;
- hover movement must not exceed 2 px.

### 10.2 Secondary button

- transparent or white surface;
- navy text on light backgrounds;
- white text on dark backgrounds;
- 1 px border;
- same minimum height as the primary action.

### 10.3 Text links

- use descriptive labels;
- normal-size links on white use `teal-700` or darker;
- underline on hover and keyboard focus unless another clear affordance exists;
- do not use “Learn more” repeatedly without context.

### 10.4 Focus state

All interactive elements require a visible focus ring, for example:

```css
outline: 3px solid rgba(56, 185, 200, 0.55);
outline-offset: 3px;
```

The focus treatment must remain visible on both light and dark surfaces.

## 11. Card system

### 11.1 General rules

- white or approved pale surface;
- 1 px border where separation is needed;
- radius: 12–20 px, with 14 px as the default corporate card radius;
- restrained shadow, never a floating glass effect;
- card content remains left aligned unless the card is a concise metric or lifecycle step;
- the whole card may be clickable only when its semantic role is one destination.

### 11.2 Division pathway cards

- prominent but not oversized;
- circular capability symbol;
- heading, concise scope and directional link;
- Digital Systems uses teal emphasis;
- Infrastructure uses navy emphasis;
- equal strategic weight.

### 11.3 Capability cards

- use relevant photography or restrained technical graphics;
- show one capability name and one clear destination;
- optional one-sentence scope on overview pages;
- no generic icon wall;
- no catalogue pricing or product-card treatment.

### 11.4 Industry cards

- imagery must depict the operating environment, not a decorative stereotype;
- include a challenge or outcome statement;
- show selected relevant capabilities without pretending to be a completed case study.

### 11.5 Document cards

- show document title, document family, file type, version or date and download/request action;
- displayed files must exist;
- no “coming soon” placeholders.

## 12. Diagrams and technical graphics

### 12.1 Visual language

Diagrams use:

- navy structural lines;
- teal active paths and integration points;
- pale neutral surfaces;
- simple geometric nodes;
- concise labels;
- no pseudo-3D, glowing circuits or science-fiction interfaces.

### 12.2 Required diagram families

- integrated capability layers;
- Discover-to-Support delivery lifecycle;
- system integration and data-flow diagrams;
- network and infrastructure topology abstractions;
- industry solution maps;
- responsibility, control and handover flows.

### 12.3 Accessibility

- diagrams require a text explanation;
- colour cannot be the only carrier of meaning;
- labels must remain readable at 200% zoom;
- complex diagrams may use an accessible data table or ordered list equivalent.

## 13. Form system

### 13.1 Fields

- visible label above every control;
- minimum control height: 48 px;
- input radius: 8–10 px;
- border: `line-300`;
- white background;
- 16 px input text to avoid mobile zoom behaviour;
- concise help text below the field where necessary.

### 13.2 States

Required states:

- default;
- hover where relevant;
- focus;
- filled;
- invalid;
- valid only where useful;
- disabled;
- submitting;
- success;
- recoverable failure.

Error messages use text and icon or shape, not colour alone. Entered information must remain available after a recoverable submission failure.

### 13.3 Form layout

- one column on mobile;
- one or two columns on desktop depending on field relationship;
- long narrative fields span the full form width;
- group related fields under clear legends or section headings;
- avoid an excessively long undifferentiated form.

## 14. Tables, matrices and specifications

- use tables only for real comparison or structured reference;
- provide row and column headers;
- avoid tiny text;
- on mobile, use stacked rows or a deliberately scrollable region with clear affordance;
- capability matrices may convert to grouped cards on narrow screens;
- zebra striping is optional and must remain subtle.

## 15. Icons

- use one consistent outline family or custom line style;
- standard stroke: approximately 1.75–2 px at 24 px size;
- default sizes: 20, 24, 32 and 48 px;
- icons support understanding but do not replace text;
- avoid dozens of small icons merely to fill space;
- do not mix unrelated icon styles.

## 16. Photography treatment

- technically plausible subjects;
- documentary or premium corporate realism;
- natural skin tones and credible work environments;
- controlled contrast and warm-neutral grading;
- navy overlays only when needed for text legibility;
- preserve real equipment geometry;
- avoid visible trademarks unless licensed and intentional;
- avoid staged handshakes, exaggerated smiling-office scenes and generic server-room portraits.

Detailed page-by-page direction is defined in [`04-image-art-direction-brief.md`](04-image-art-direction-brief.md).

## 17. Divisional expression

### 17.1 Digital Systems & AI

- white, ivory and cool-light surfaces dominate;
- teal is the principal accent;
- use people, workflows, interfaces, architecture and data-flow visuals;
- section transitions may be softer and more editorial;
- diagrams emphasise information, roles, controls and integration;
- never use robot imagery or unsupported futuristic interfaces.

### 17.2 Infrastructure & Engineering

- stronger use of navy panels and technical photography;
- more structured grids and specification blocks;
- wider architectural spacing;
- diagrams emphasise topology, physical systems, phases, testing and commissioning;
- imagery may show fibre, racks, towers, power, CCTV, technical rooms and controlled civil enabling works;
- do not turn every page into a construction-site gallery.

### 17.3 Technology Supply & Integration

- balanced digital and infrastructure expression;
- use specifications, bills of materials, sourcing, installation, commissioning and handover as the narrative;
- avoid product catalogue grids and shopping conventions.

## 18. Page-template design rules

### 18.1 Homepage

Preserve the approved composition and component hierarchy. Future refinement may improve implementation quality but must not redesign the page away from the approved reference.

### 18.2 Capabilities overview

Use a controlled capability matrix and integrated-system diagram. It must show relationships, not a wall of unrelated service tiles.

### 18.3 Digital Systems landing

Use a light, workflow-oriented hero, five capability routes, architecture diagram, system examples and a restrained support section.

### 18.4 Digital capability detail

Use one capability-specific hero, scope blocks, deliverable cards, integration diagram, delivery steps, related industries and final CTA.

### 18.5 Infrastructure landing

Use a strong technical hero, six capability categories, structured delivery blocks, commissioning narrative and industry relevance.

### 18.6 Infrastructure capability detail

Use strong technical photography, assessment-to-handover structure, equipment categories, integration points, testing and support.

### 18.7 Technology Supply & Integration

Use a requirement-to-handover process, specification examples, sourcing and partner coordination, commissioning and support. No e-commerce treatment.

### 18.8 Industries overview

Use six sector cards plus one integrated operating-layer diagram.

### 18.9 Industry detail

Use a sector-specific hero, challenge-to-solution structure, digital and infrastructure requirements, representative project patterns and delivery controls.

### 18.10 How We Deliver

Make the seven-stage lifecycle the visual spine. Support it with responsibilities, evidence, security, testing, commissioning and operational handover.

### 18.11 Company

Use an editorial corporate layout with clear division explanations, operating principles, local presence and only verified facts.

### 18.12 Resources

Use a document-centred layout with strong metadata, filters only if needed, direct downloads and an integrated request form.

### 18.13 Contact and enquiry forms

Use concise orientation, clear contact routes and highly usable forms. Do not bury key contact information below the form.

## 19. Motion and interaction

- motion must be purposeful and brief;
- standard transitions: 160–220 ms;
- hover lift: maximum 2 px;
- no parallax that harms legibility or performance;
- no autoplay video with sound;
- no looping decorative motion that competes with content;
- honour `prefers-reduced-motion` by removing non-essential animation and smooth scrolling.

## 20. Responsive behaviour

Responsive design must restructure, not merely shrink.

- utility content simplifies on mobile;
- desktop mega-menus become explicit accordion groups;
- split heroes stack with copy before imagery unless the approved composition requires another order;
- two-column cards become one column when minimum content width cannot be maintained;
- capability matrices become grouped cards or accessible horizontal regions;
- diagrams receive mobile-specific compositions;
- CTAs may become full width on compact mobile;
- card text must not truncate essential meaning;
- no horizontal page overflow is permitted.

## 21. Accessibility baseline

The visual system targets WCAG 2.2 Level AA.

Required:

- normal text contrast of at least 4.5:1;
- large text contrast of at least 3:1;
- visible keyboard focus;
- minimum 44 × 44 px pointer targets where practical;
- headings that preserve semantic order;
- no information conveyed by colour alone;
- sufficient text spacing and zoom reflow;
- alternative text decisions recorded in the image register;
- accessible menus, dialogs, accordions, forms and error states.

## 22. Performance constraints

- use responsive image sources and explicit dimensions;
- prefer AVIF or WebP with suitable fallback where required;
- reserve PNG for transparency, logos and graphics that need it;
- avoid decorative video on launch pages unless performance evidence justifies it;
- self-host or carefully control fonts;
- limit JavaScript to actual interaction requirements;
- prevent layout shift by reserving image and component space.

## 23. Implementation token baseline

```css
:root {
  --color-navy-950: #011631;
  --color-navy-900: #031a3f;
  --color-navy-800: #06285c;
  --color-ink-900: #06183c;
  --color-teal-700: #007575;
  --color-teal-600: #008b8b;
  --color-teal-500: #009a9a;
  --color-cyan-400: #38b9c8;
  --color-teal-050: #e8f5f4;
  --color-slate-700: #5a6372;
  --color-slate-500: #6c7888;
  --color-line-300: #dce3ea;
  --color-line-200: #e0e5ea;
  --color-ivory-050: #fbf8f3;
  --color-warm-100: #f4eee5;
  --color-cool-050: #f7fafc;
  --color-white: #ffffff;
  --color-success-600: #17795e;
  --color-danger-600: #a63838;
  --radius-control: 8px;
  --radius-card: 14px;
  --radius-panel: 20px;
  --shadow-card: 0 8px 20px rgba(3, 26, 69, 0.12);
  --shadow-panel: 0 24px 65px rgba(3, 26, 69, 0.14);
  --container-standard: 1240px;
  --container-wide: 1580px;
}
```

These tokens are a baseline. Implementation may add semantic aliases but may not alter the visual meaning without updating this document.

## 24. Design acceptance criteria

The visual system is correctly applied only when:

- the site is recognisably one Techgrity Systems experience;
- Digital Systems and Infrastructure remain distinct but related;
- the approved homepage continues to define the quality bar;
- page families reuse components without becoming repetitive;
- no page resembles an equipment catalogue, web-design agency or generic template;
- colour, type, spacing, imagery and controls remain consistent;
- all interactions are keyboard usable and visibly focused;
- all required viewports are visually verified;
- no unsupported visual claim, partner logo, certification badge or project evidence appears;
- implementation tokens and component behaviour remain documented.

## 25. Next controlled deliverable

The next governing document is the **Image and Art-Direction Brief**, which defines the exact image purpose, subject, composition, crop, technical constraints and alternative-text treatment for every master template and page family.