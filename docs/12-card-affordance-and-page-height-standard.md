# Techgrity Systems Card Affordance and Page-Height Standard

**Status:** LOCKED  
**Date:** 29 July 2026

## 1. Purpose

This standard prevents visual review boards from distorting implementation height and prevents informational content from being mistaken for navigation.

## 2. Review-board height versus production height

A desktop approval image may compress or scale a complete long page so the full content architecture can be reviewed in one frame. That image does not define the final browser height.

Production requirements:

- pages use natural document flow and vertical scrolling;
- desktop heroes normally retain approximately 560–650 px of content-led height unless the approved template requires another value;
- standard sections retain the spacing defined by the visual design system;
- cards, labels and body copy are never reduced merely to fit a single screenshot;
- first-viewport evidence and full-page evidence are generated separately during implementation QA;
- the opening viewport must still communicate proposition, page context and primary CTA clearly.

## 3. Navigational card contract

A card may appear clickable only when it has a real destination.

Required:

- semantic anchor or appropriate interactive element;
- valid planned route or approved in-page target;
- keyboard focus;
- visible focus state;
- useful accessible name;
- arrow, pointer cursor and hover treatment allowed;
- entire-card activation only when the card has one unambiguous destination.

## 4. Informational card contract

An informational card communicates scope, a process stage, a deliverable or an attribute without taking the user elsewhere.

Required:

- no arrow or directional cue;
- no pointer cursor;
- no fake hover lift or interactive colour shift;
- no `role=button`, tabindex or click handler;
- no link-styled heading unless the heading itself is a real link;
- visual styling must distinguish it from navigational cards.

## 5. Current application

### Homepage capability tiles

These remain navigational because real detail pages are planned for:

- Software, AI & Enterprise Applications;
- Networks & Fibre;
- Data Centres & Cloud;
- Telecom & Radio Infrastructure;
- Power & Energy;
- Civil & Technical Infrastructure.

### Networks & Fibre sub-capability tiles

The following remain informational within the Networks & Fibre page and do not create six additional pages:

- Enterprise networking;
- Fibre-optic infrastructure;
- Structured cabling;
- Wireless and microwave connectivity;
- Network monitoring and optimisation;
- Network security foundations.

Their arrows and link-like behaviour must be removed in implementation.

## 6. Acceptance tests

- every element with an arrow resolves to a real destination or approved in-page target;
- every pointer cursor corresponds to a real interactive element;
- keyboard tab order includes only actual controls and links;
- no dead tile or placeholder destination exists;
- long pages retain normal readable scale and documented section spacing;
- full-page screenshots are evidence, not layout constraints.
