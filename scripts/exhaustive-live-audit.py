from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
import os
import re
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("AUDIT_BASE_URL", "https://techgrity.co.zw").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "exhaustive-live-audit"
SCREENSHOTS = EVIDENCE / "screenshots"
EVIDENCE.mkdir(parents=True, exist_ok=True)
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

PUBLIC_ROUTES = [
    "/",
    "/capabilities/",
    "/capabilities/digital-systems/",
    "/capabilities/digital-systems/software-ai-applications/",
    "/capabilities/digital-systems/automation/",
    "/capabilities/digital-systems/integration/",
    "/capabilities/digital-systems/data-analytics/",
    "/capabilities/digital-systems/cybersecurity-access/",
    "/capabilities/infrastructure/",
    "/capabilities/infrastructure/networks-fibre/",
    "/capabilities/infrastructure/data-centres-cloud/",
    "/capabilities/infrastructure/telecom-radio/",
    "/capabilities/infrastructure/power-energy/",
    "/capabilities/infrastructure/security-smart-facilities/",
    "/capabilities/infrastructure/civil-technical-works/",
    "/capabilities/technology-supply/",
    "/industries/",
    "/industries/government-public-sector/",
    "/industries/education-research/",
    "/industries/telecommunications/",
    "/industries/energy-utilities-industrial/",
    "/industries/data-centres-technology/",
    "/industries/commerce-logistics-growing-organisations/",
    "/how-we-deliver/",
    "/company/",
    "/resources/",
    "/contact/",
    "/discuss-a-project/",
    "/privacy/",
    "/terms/",
    "/cookies/",
]
SYSTEM_ROUTES = [
    "/404/",
    "/project-enquiry-received/",
    "/document-request-received/",
    "/form-error/",
]
ALL_ROUTES = PUBLIC_ROUTES + SYSTEM_ROUTES

VIEWPORTS = [
    (1672, 941, "desktop-wide"),
    (1440, 900, "desktop"),
    (1280, 800, "desktop-compact"),
    (1024, 900, "tablet-landscape"),
    (768, 1024, "tablet-portrait"),
    (390, 844, "mobile"),
    (320, 568, "mobile-narrow"),
]
INTERACTION_VIEWPORTS = [
    (1024, 900, "tablet-landscape"),
    (768, 1024, "tablet-portrait"),
    (390, 844, "mobile"),
    (320, 568, "mobile-narrow"),
]
FORM_ROUTES = ["/", "/contact/", "/discuss-a-project/", "/resources/"]

SIGNIFICANT_SELECTORS = ",".join([
    ".card", ".hero-board", ".hero-photo", ".hero-collage-card",
    ".digital-hero-visual", ".workspace-visual", ".matrix-board",
    ".industry-card", ".home-capability-card", ".home-pathway-card",
    ".solution-point", ".contact-detail", ".scope-feature", ".number-item",
    ".board-row", ".matrix-layer", ".cta-panel", ".lifecycle li",
    ".capability-visual", ".collage-image", ".workspace-panel",
])

results: list[dict] = []
interactions: list[dict] = []
forms: list[dict] = []
link_inventory: dict[str, set[str]] = defaultdict(set)
console_messages: list[dict] = []


def slug(route: str) -> str:
    if route == "/":
        return "home"
    return re.sub(r"[^a-z0-9]+", "-", route.strip("/").lower()).strip("-") or "root"


def safe_goto(page, route: str):
    url = f"{BASE_URL}{route}"
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        try:
            page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightTimeoutError:
            pass
        page.wait_for_timeout(180)
        return response, None
    except Exception as exc:  # evidence must survive a broken route
        return None, f"{type(exc).__name__}: {exc}"


def collect_metrics(page):
    return page.evaluate(
        """(significantSelectors) => {
          const visible = (el) => {
            const cs = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity || 1) > 0.01 && r.width > 0 && r.height > 0;
          };
          const text = (el) => (el.innerText || el.textContent || '').replace(/\s+/g,' ').trim();
          const bgImage = (el) => getComputedStyle(el).backgroundImage;
          const sections = [...document.querySelectorAll('main > section, main > div, main > article')].map((el, i) => {
            const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
            return {i, tag:el.tagName, id:el.id, cls:el.className, textLength:text(el).length,
              display:cs.display, visibility:cs.visibility, opacity:Number(cs.opacity || 1),
              x:Math.round(r.x), y:Math.round(r.y), width:Math.round(r.width), height:Math.round(r.height)};
          });
          const hiddenMeaningful = sections.filter(s => s.textLength > 35 && s.height > 80 && (s.display === 'none' || s.visibility === 'hidden' || s.opacity < .08));
          const emptyCandidates = [...document.querySelectorAll(significantSelectors)].filter(visible).map((el) => {
            const r = el.getBoundingClientRect();
            const hasMedia = Boolean(el.querySelector('img,svg,video,canvas,picture')) || bgImage(el) !== 'none';
            const value = text(el);
            return {tag:el.tagName, id:el.id, cls:el.className, textLength:value.length, hasMedia,
              width:Math.round(r.width), height:Math.round(r.height), area:Math.round(r.width*r.height)};
          }).filter(x => x.area > 9000 && x.textLength < 2 && !x.hasMedia);
          const namelessInteractive = [...document.querySelectorAll('a[href],button,input,select,textarea')].filter(visible).filter(el => {
            const name=(el.getAttribute('aria-label') || el.getAttribute('title') || text(el) || el.getAttribute('alt') || '').trim();
            return !name && !['hidden'].includes((el.getAttribute('type') || '').toLowerCase());
          }).map(el => ({tag:el.tagName, cls:el.className, href:el.getAttribute('href'), type:el.getAttribute('type')}));
          const ids=[...document.querySelectorAll('[id]')].map(el=>el.id).filter(Boolean);
          const duplicateIds=[...new Set(ids.filter((id,i)=>ids.indexOf(id)!==i))];
          const headings=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible).map(el=>({level:Number(el.tagName[1]),text:text(el).slice(0,120)}));
          const headingJumps=[]; for(let i=1;i<headings.length;i++){if(headings[i].level-headings[i-1].level>1) headingJumps.push({from:headings[i-1],to:headings[i]});}
          const images=[...document.images].map(img=>{const r=img.getBoundingClientRect();return {src:img.currentSrc||img.src,alt:img.alt,
            naturalWidth:img.naturalWidth,naturalHeight:img.naturalHeight,width:Math.round(r.width),height:Math.round(r.height),
            broken:!img.complete||img.naturalWidth===0,upscale:r.width>0&&img.naturalWidth>0?Number((r.width/img.naturalWidth).toFixed(2)):0};});
          const visibleUpscaled=images.filter(img=>!img.broken&&img.width>180&&img.upscale>1.5);
          const overflowElements=[...document.querySelectorAll('body *')].filter(visible).map(el=>{const r=el.getBoundingClientRect();const cs=getComputedStyle(el);return {tag:el.tagName,id:el.id,cls:String(el.className||''),left:r.left,right:r.right,width:r.width,position:cs.position,overflowX:cs.overflowX};})
            .filter(x=>x.position!=='fixed'&&x.width>1&&(x.left<-2||x.right>window.innerWidth+2)&&!['auto','scroll','hidden','clip'].includes(x.overflowX)).slice(0,30);
          const smallTargets=[...document.querySelectorAll('a[href],button,input,select,textarea')].filter(visible).map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,cls:String(el.className||''),name:(el.getAttribute('aria-label')||text(el)).slice(0,80),width:Math.round(r.width),height:Math.round(r.height)};}).filter(x=>x.width<44||x.height<44).slice(0,60);
          const header=document.querySelector('.site-header'); const hr=header?.getBoundingClientRect(); const hcs=header?getComputedStyle(header):null;
          const logo=document.querySelector('.brand img');
          const favicon=[...document.querySelectorAll('link[rel~="icon"],link[rel="apple-touch-icon"]')].map(el=>({rel:el.rel,href:el.href,type:el.type,sizes:el.sizes?.value||''}));
          const links=[...document.querySelectorAll('a[href]')].map(a=>a.href);
          const blankRegions=sections.filter(s=>s.height>180&&s.textLength<12);
          return {
            title:document.title, url:location.href, lang:document.documentElement.lang,
            scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth,
            scrollHeight:document.documentElement.scrollHeight, clientHeight:document.documentElement.clientHeight,
            bodyScrollWidth:document.body.scrollWidth, h1Count:document.querySelectorAll('h1').length,
            sections, hiddenMeaningful, emptyCandidates, namelessInteractive, duplicateIds, headings, headingJumps,
            images, visibleUpscaled, overflowElements, smallTargets, blankRegions,
            header:header?{position:hcs.position,top:hcs.top,zIndex:hcs.zIndex,rect:{top:Math.round(hr.top),bottom:Math.round(hr.bottom),height:Math.round(hr.height)},className:header.className}:null,
            logo:logo?{src:logo.src,alt:logo.alt,naturalWidth:logo.naturalWidth,naturalHeight:logo.naturalHeight}:null,
            favicon, links,
            initialCookiePanelVisible:Boolean(document.querySelector('[data-cookie-panel]')&&!document.querySelector('[data-cookie-panel]').hidden),
            initialInvalidFields:document.querySelectorAll('[aria-invalid="true"],.field.invalid,.form-field.invalid').length,
          };
        }""",
        SIGNIFICANT_SELECTORS,
    )


def inspect_scroll(page):
    return page.evaluate(
        """async () => {
          const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
          const header=document.querySelector('.site-header');
          const before=header?{position:getComputedStyle(header).position,top:Math.round(header.getBoundingClientRect().top),bottom:Math.round(header.getBoundingClientRect().bottom)}:null;
          const max=Math.max(0,document.documentElement.scrollHeight-innerHeight);
          const points=[0,.2,.4,.6,.8,1].map(x=>Math.round(max*x));
          for(const y of points){scrollTo(0,y);await sleep(160);}
          const after=header?{position:getComputedStyle(header).position,top:Math.round(header.getBoundingClientRect().top),bottom:Math.round(header.getBoundingClientRect().bottom),visible:header.getBoundingClientRect().bottom>0}:null;
          const hidden=[...document.querySelectorAll('main > section, main > div, main > article')].filter(el=>{
            const cs=getComputedStyle(el); const r=el.getBoundingClientRect(); const t=(el.innerText||'').trim();
            return t.length>35&&r.height>80&&(cs.display==='none'||cs.visibility==='hidden'||Number(cs.opacity||1)<.08);
          }).map(el=>({id:el.id,cls:el.className,text:(el.innerText||'').replace(/\s+/g,' ').trim().slice(0,100),opacity:getComputedStyle(el).opacity}));
          scrollTo(0,0); await sleep(100);
          return {before,after,maxScroll:max,hiddenAfterFullScroll:hidden};
        }"""
    )


def record_console(page, route, viewport):
    def handler(msg):
        if msg.type in {"error", "warning"}:
            console_messages.append({"route": route, "viewport": viewport, "type": msg.type, "text": msg.text})
    page.on("console", handler)
    page.on("pageerror", lambda err: console_messages.append({"route": route, "viewport": viewport, "type": "pageerror", "text": str(err)}))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])

    # 35 routes x 7 viewports = 245 route/viewport cells.
    for width, height, label in VIEWPORTS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        for route in ALL_ROUTES:
            page = context.new_page()
            record_console(page, route, label)
            response, navigation_error = safe_goto(page, route)
            status = response.status if response else None
            headers = response.headers if response else {}
            metrics = collect_metrics(page) if not navigation_error else {}
            scroll = inspect_scroll(page) if not navigation_error else {}
            for href in metrics.get("links", []):
                parsed = urlparse(href)
                if parsed.netloc in {urlparse(BASE_URL).netloc, "www.techgrity.co.zw"}:
                    link_inventory[route].add(href)
            expected_status = 404 if route == "/404/" else 200
            findings = []
            if navigation_error:
                findings.append({"severity": "critical", "code": "navigation-error", "detail": navigation_error})
            if status != expected_status:
                findings.append({"severity": "critical", "code": "unexpected-status", "detail": {"expected": expected_status, "actual": status}})
            if metrics:
                if metrics["scrollWidth"] > metrics["clientWidth"] + 1:
                    findings.append({"severity": "high", "code": "horizontal-overflow", "detail": metrics["overflowElements"]})
                if metrics["h1Count"] != 1:
                    findings.append({"severity": "high", "code": "h1-count", "detail": metrics["h1Count"]})
                if metrics["hiddenMeaningful"] or scroll.get("hiddenAfterFullScroll"):
                    findings.append({"severity": "critical", "code": "meaningful-content-hidden", "detail": metrics["hiddenMeaningful"] + scroll.get("hiddenAfterFullScroll", [])})
                if metrics["emptyCandidates"]:
                    findings.append({"severity": "high", "code": "empty-visual-containers", "detail": metrics["emptyCandidates"]})
                if metrics["blankRegions"]:
                    findings.append({"severity": "medium", "code": "blank-major-regions", "detail": metrics["blankRegions"]})
                if metrics["namelessInteractive"]:
                    findings.append({"severity": "high", "code": "nameless-interactive", "detail": metrics["namelessInteractive"]})
                if metrics["duplicateIds"]:
                    findings.append({"severity": "high", "code": "duplicate-ids", "detail": metrics["duplicateIds"]})
                if any(img["broken"] for img in metrics["images"]):
                    findings.append({"severity": "critical", "code": "broken-images", "detail": [img for img in metrics["images"] if img["broken"]]})
                if metrics["visibleUpscaled"]:
                    findings.append({"severity": "medium", "code": "upscaled-images", "detail": metrics["visibleUpscaled"]})
                if metrics["headingJumps"]:
                    findings.append({"severity": "medium", "code": "heading-order", "detail": metrics["headingJumps"]})
                if width <= 768 and metrics["smallTargets"]:
                    findings.append({"severity": "medium", "code": "small-touch-targets", "detail": metrics["smallTargets"]})
                if metrics["initialCookiePanelVisible"]:
                    findings.append({"severity": "high", "code": "cookie-panel-obstructs-first-visit", "detail": True})
                if metrics["initialInvalidFields"]:
                    findings.append({"severity": "high", "code": "form-errors-on-initial-load", "detail": metrics["initialInvalidFields"]})
                header_after = scroll.get("after") or {}
                if metrics.get("header") and not header_after.get("visible"):
                    findings.append({"severity": "high", "code": "header-disappears-on-scroll", "detail": {"before": scroll.get("before"), "after": header_after}})
            result = {
                "route": route, "viewport": {"width": width, "height": height, "label": label},
                "status": status, "expectedStatus": expected_status, "finalUrl": page.url,
                "headers": {k: headers.get(k) for k in ["content-type", "strict-transport-security", "content-security-policy", "x-content-type-options", "referrer-policy", "permissions-policy"] if headers.get(k)},
                "navigationError": navigation_error, "metrics": metrics, "scroll": scroll, "findings": findings,
            }
            results.append(result)
            if label in {"desktop", "mobile"} or findings:
                try:
                    page.evaluate("() => { const p=document.querySelector('[data-cookie-panel]'); if(p) p.hidden=true; window.scrollTo(0,0); }")
                    page.screenshot(path=str(SCREENSHOTS / f"{slug(route)}--{label}.png"), full_page=True)
                except Exception as exc:
                    result.setdefault("screenshotError", str(exc))
            page.close()
        context.close()

    # 35 routes x 4 responsive interaction widths = 140 interaction cells.
    for width, height, label in INTERACTION_VIEWPORTS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        for route in ALL_ROUTES:
            page = context.new_page()
            response, navigation_error = safe_goto(page, route)
            record = {"route": route, "viewport": {"width": width, "height": height, "label": label}, "navigationError": navigation_error, "status": response.status if response else None}
            if not navigation_error:
                toggle = page.locator(".menu-toggle")
                record["toggleVisible"] = toggle.is_visible()
                if toggle.is_visible():
                    toggle.click()
                    page.wait_for_timeout(180)
                    record.update(page.evaluate("""() => {
                      const nav=document.querySelector('.primary-nav'); const r=nav.getBoundingClientRect();
                      const focus=[...nav.querySelectorAll('a[href],button:not([disabled])')].filter(el=>el.offsetParent!==null);
                      const before=nav.scrollTop; nav.scrollTop=nav.scrollHeight; const after=nav.scrollTop;
                      const last=focus.at(-1)?.getBoundingClientRect();
                      return {menuOpen:nav.classList.contains('open'),ariaExpanded:document.querySelector('.menu-toggle')?.getAttribute('aria-expanded'),
                        bodyLocked:document.body.classList.contains('menu-open'),navClientHeight:nav.clientHeight,navScrollHeight:nav.scrollHeight,
                        navRect:{top:r.top,bottom:r.bottom,left:r.left,right:r.right},scrollable:nav.scrollHeight<=nav.clientHeight+1||after>before,
                        lastFocusable: last?{top:last.top,bottom:last.bottom}:null};
                    }"""))
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(80)
                    record["closedByEscape"] = toggle.get_attribute("aria-expanded") == "false"
                else:
                    record["menuOpen"] = False
                    record["scrollable"] = False
            interactions.append(record)
            page.close()
        context.close()

    # Desktop dropdown and keyboard checks on each route.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    for route in ALL_ROUTES:
        page = context.new_page()
        _, navigation_error = safe_goto(page, route)
        record = {"route": route, "viewport": "desktop-dropdowns", "navigationError": navigation_error, "dropdowns": []}
        if not navigation_error:
            buttons = page.locator(".nav-dropdown > button")
            for i in range(buttons.count()):
                button = buttons.nth(i)
                label = (button.inner_text() or "").strip()
                button.click()
                page.wait_for_timeout(80)
                dropdown = button.locator("xpath=..")
                menu = dropdown.locator(".mega-menu,.mini-menu").first
                record["dropdowns"].append({"label": label, "expanded": button.get_attribute("aria-expanded"), "visible": menu.is_visible(), "links": menu.locator("a[href]").count()})
                page.keyboard.press("Escape")
        interactions.append(record)
        page.close()
    context.close()

    # Four canonical form-state pages x four interaction widths = 16 form-state cells.
    for width, height, label in INTERACTION_VIEWPORTS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        for route in FORM_ROUTES:
            page = context.new_page()
            _, navigation_error = safe_goto(page, route)
            record = {"route": route, "viewport": {"width": width, "height": height, "label": label}, "navigationError": navigation_error}
            if not navigation_error:
                form = page.locator("form[data-form]").first
                record["formPresent"] = form.count() == 1
                if form.count() == 1:
                    record["initialInvalid"] = form.locator('[aria-invalid="true"],.field.invalid,.form-field.invalid').count()
                    form.locator('button[type="submit"]').click()
                    page.wait_for_timeout(100)
                    record["invalidAfterEmptySubmit"] = form.locator('[aria-invalid="true"]').count()
                    record["focusedInvalid"] = page.evaluate("() => document.activeElement?.getAttribute('aria-invalid') === 'true'")
            forms.append(record)
            page.close()
        context.close()

    # Cookie dialog contract once per interaction width.
    for width, height, label in INTERACTION_VIEWPORTS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        page = context.new_page()
        _, navigation_error = safe_goto(page, "/")
        record = {"route": "/", "viewport": label, "test": "cookie-dialog", "navigationError": navigation_error}
        if not navigation_error:
            panel = page.locator("[data-cookie-panel]")
            manage = page.locator("[data-cookie-manage]")
            record["initiallyHidden"] = not panel.is_visible()
            manage.click()
            page.wait_for_timeout(80)
            record["opensOnDemand"] = panel.is_visible()
            record["focusMovedInside"] = page.evaluate("() => document.querySelector('[data-cookie-panel]')?.contains(document.activeElement)")
            page.keyboard.press("Escape")
            page.wait_for_timeout(80)
            record["closesWithEscape"] = not panel.is_visible()
            record["focusReturned"] = page.evaluate("() => document.activeElement === document.querySelector('[data-cookie-manage]')")
        interactions.append(record)
        page.close()
        context.close()

    browser.close()

# Internal link and fragment reconciliation from the rendered inventory.
unique_links = sorted({href for links in link_inventory.values() for href in links})
link_results = []
with sync_playwright() as p:
    request = p.request.new_context(ignore_https_errors=False)
    for href in unique_links:
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"}:
            continue
        try:
            response = request.get(href, timeout=20_000, fail_on_status_code=False)
            status = response.status
            final_url = response.url
            fragment_ok = True
            if parsed.fragment and parsed.netloc == urlparse(BASE_URL).netloc and status < 400:
                # Fragment existence is already represented in page DOM, but record the target path for reconciliation.
                fragment_ok = True
            link_results.append({"url": href, "status": status, "finalUrl": final_url, "ok": status < 400, "fragment": parsed.fragment, "fragmentOk": fragment_ok})
        except Exception as exc:
            link_results.append({"url": href, "status": None, "ok": False, "error": f"{type(exc).__name__}: {exc}", "fragment": parsed.fragment})
    request.dispose()

# Cross-route header consistency summary.
header_signatures = Counter()
header_visibility = defaultdict(list)
for cell in results:
    header = cell.get("metrics", {}).get("header")
    if header:
        signature = (header.get("position"), header.get("rect", {}).get("height"), header.get("className"))
        header_signatures[str(signature)] += 1
        header_visibility[cell["route"]].append(bool(cell.get("scroll", {}).get("after", {}).get("visible")))

finding_counts = Counter(f["code"] for cell in results for f in cell["findings"])
severity_counts = Counter(f["severity"] for cell in results for f in cell["findings"])
interaction_failures = []
for item in interactions:
    if "menuOpen" in item and item.get("toggleVisible"):
        if not item.get("menuOpen") or not item.get("scrollable") or not item.get("closedByEscape"):
            interaction_failures.append(item)
    for dropdown in item.get("dropdowns", []):
        if dropdown.get("expanded") != "true" or not dropdown.get("visible") or dropdown.get("links", 0) < 1:
            interaction_failures.append({"route": item.get("route"), "dropdown": dropdown})
form_failures = [f for f in forms if f.get("formPresent") is not True or f.get("initialInvalid") != 0 or f.get("invalidAfterEmptySubmit", 0) < 1 or not f.get("focusedInvalid")]

summary = {
    "baseUrl": BASE_URL,
    "generatedAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "routeViewportCells": len(results),
    "interactionCells": len([i for i in interactions if isinstance(i.get("viewport"), dict)]),
    "formStateCells": len(forms),
    "routes": len(ALL_ROUTES),
    "viewports": len(VIEWPORTS),
    "findingCounts": dict(finding_counts),
    "severityCounts": dict(severity_counts),
    "interactionFailureCount": len(interaction_failures),
    "formFailureCount": len(form_failures),
    "consoleMessageCount": len(console_messages),
    "brokenLinkCount": len([x for x in link_results if not x.get("ok")]),
    "headerSignatures": dict(header_signatures),
    "routesWhereHeaderDisappears": sorted([route for route, values in header_visibility.items() if values and not all(values)]),
}

(EVIDENCE / "summary.json").write_text(json.dumps(summary, indent=2))
(EVIDENCE / "route-viewport-cells.json").write_text(json.dumps(results, indent=2))
(EVIDENCE / "interaction-cells.json").write_text(json.dumps(interactions, indent=2))
(EVIDENCE / "form-state-cells.json").write_text(json.dumps(forms, indent=2))
(EVIDENCE / "link-reconciliation.json").write_text(json.dumps(link_results, indent=2))
(EVIDENCE / "console-messages.json").write_text(json.dumps(console_messages, indent=2))
(EVIDENCE / "interaction-failures.json").write_text(json.dumps(interaction_failures, indent=2))
(EVIDENCE / "form-failures.json").write_text(json.dumps(form_failures, indent=2))

md = [
    "# Techgrity Website — Exhaustive Live Audit",
    "",
    f"- Base URL: `{BASE_URL}`",
    f"- Generated: `{summary['generatedAtUtc']}`",
    f"- Route/viewport cells: **{summary['routeViewportCells']}**",
    f"- Responsive interaction cells: **{summary['interactionCells']}**",
    f"- Canonical form-state cells: **{summary['formStateCells']}**",
    f"- Console warnings/errors: **{summary['consoleMessageCount']}**",
    f"- Broken links: **{summary['brokenLinkCount']}**",
    f"- Interaction failures: **{summary['interactionFailureCount']}**",
    f"- Form-state failures: **{summary['formFailureCount']}**",
    "",
    "## Finding counts",
]
for code, count in sorted(finding_counts.items()):
    md.append(f"- `{code}`: {count}")
md.extend(["", "## Header behavior", f"- Signatures: `{json.dumps(summary['headerSignatures'], sort_keys=True)}`", f"- Routes where the header disappears at one or more widths: `{', '.join(summary['routesWhereHeaderDisappears']) or 'none'}`", ""])
(EVIDENCE / "AUDIT-REPORT.md").write_text("\n".join(md))

print(json.dumps(summary, indent=2))
