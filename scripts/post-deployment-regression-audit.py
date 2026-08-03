from __future__ import annotations

from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
import json
import os
import re
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE = os.environ.get("AUDIT_BASE_URL", "https://techgrity.co.zw").rstrip("/")
EXPECTED_SHA = os.environ.get("EXPECTED_RELEASE_SHA", "a729d9f1df31acd9835bad9ee7b78408bf3d9672")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "post-deployment-audit"
SHOTS = OUT / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)

ROUTES = [
    "/", "/capabilities/", "/capabilities/digital-systems/",
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
    "/capabilities/technology-supply/", "/industries/",
    "/industries/government-public-sector/",
    "/industries/education-research/", "/industries/telecommunications/",
    "/industries/energy-utilities-industrial/",
    "/industries/data-centres-technology/",
    "/industries/commerce-logistics-growing-organisations/",
    "/how-we-deliver/", "/company/", "/resources/", "/contact/",
    "/discuss-a-project/", "/privacy/", "/terms/", "/cookies/",
    "/404/", "/project-enquiry-received/",
    "/document-request-received/", "/form-error/",
]
PUBLIC_ROUTES = ROUTES[:31]
SYSTEM_ROUTES = ROUTES[31:]
MOBILE_WIDTHS = [(1024, 900, "tablet-landscape"), (768, 1024, "tablet-portrait"), (390, 844, "mobile"), (320, 568, "mobile-narrow")]
FORM_ROUTES = ["/", "/contact/", "/discuss-a-project/", "/resources/"]

findings: list[dict] = []
route_records: list[dict] = []
menu_records: list[dict] = []
form_records: list[dict] = []
api_records: list[dict] = []
console_messages: list[dict] = []


def add(severity: str, code: str, detail, *, route: str | None = None, viewport: str | None = None):
    findings.append({"severity": severity, "code": code, "route": route, "viewport": viewport, "detail": detail})


def goto(page, route: str):
    response = page.goto(f"{BASE}{route}", wait_until="domcontentloaded", timeout=30_000)
    try:
        page.wait_for_load_state("networkidle", timeout=5_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(180)
    return response


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    request = p.request.new_context(ignore_https_errors=False)

    release = request.get(f"{BASE}/release.json", fail_on_status_code=False)
    release_body = release.json() if release.status == 200 else {}
    if release.status != 200 or release_body.get("commit") != EXPECTED_SHA:
        add("critical", "release-sha-mismatch", {"status": release.status, "body": release_body})

    title_seen: dict[str, str] = {}
    description_seen: dict[str, str] = {}
    required_headers = ["strict-transport-security", "content-security-policy", "x-content-type-options", "referrer-policy", "permissions-policy"]

    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    for route in ROUTES:
        page = context.new_page()
        page.on("console", lambda msg, r=route: console_messages.append({"route": r, "type": msg.type, "text": msg.text}) if msg.type in {"error", "warning"} else None)
        page.on("pageerror", lambda err, r=route: console_messages.append({"route": r, "type": "pageerror", "text": str(err)}))
        expected_status = 404 if route == "/404/" else 200
        try:
            response = goto(page, route)
            status = response.status
            headers = response.headers
            raw = request.get(f"{BASE}{route}", fail_on_status_code=False).text()
            metrics = page.evaluate("""() => {
              const visible = el => { const s=getComputedStyle(el),r=el.getBoundingClientRect(); return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.01&&r.width>0&&r.height>0; };
              const canonical=document.querySelector('link[rel="canonical"]')?.href||'';
              const description=document.querySelector('meta[name="description"]')?.content||'';
              const ogUrl=document.querySelector('meta[property="og:url"]')?.content||'';
              const jsonLd=[...document.querySelectorAll('script[type="application/ld+json"]')].map(x=>x.textContent||'');
              return {title:document.title,description,canonical,ogUrl,lang:document.documentElement.lang,
                h1:document.querySelectorAll('h1').length,main:document.querySelectorAll('main').length,
                skipLink:Boolean(document.querySelector('a.skip-link[href="#main"]')),
                images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),
                duplicateIds:(ids=>[...new Set(ids.filter((id,i)=>ids.indexOf(id)!==i))])([...document.querySelectorAll('[id]')].map(x=>x.id).filter(Boolean)),
                unnamed:[...document.querySelectorAll('a[href],button,input,select,textarea')].filter(visible).filter(el=>!(el.getAttribute('aria-label')||el.getAttribute('title')||(el.innerText||'').trim()||el.getAttribute('alt'))).map(el=>({tag:el.tagName,cls:String(el.className||''),type:el.getAttribute('type')})),
                jsonLd};
            }""")
            record = {"route": route, "status": status, "headers": {k: headers.get(k) for k in required_headers}, "metrics": metrics}
            route_records.append(record)
            if status != expected_status:
                add("critical", "unexpected-status", {"expected": expected_status, "actual": status}, route=route)
            missing_headers = [h for h in required_headers if not headers.get(h)]
            if missing_headers:
                add("high", "missing-security-headers", missing_headers, route=route)
            if metrics["lang"] != "en" or metrics["h1"] != 1 or metrics["main"] != 1 or not metrics["skipLink"]:
                add("high", "document-semantic-contract", {k: metrics[k] for k in ["lang", "h1", "main", "skipLink"]}, route=route)
            if metrics["images"]:
                add("critical", "broken-images", metrics["images"], route=route)
            if metrics["duplicateIds"]:
                add("high", "duplicate-ids", metrics["duplicateIds"], route=route)
            if metrics["unnamed"]:
                add("high", "unnamed-interactive-controls", metrics["unnamed"], route=route)
            canonical_expected = f"{BASE}{route}"
            if metrics["canonical"] != canonical_expected or metrics["ogUrl"] != canonical_expected:
                add("medium", "canonical-og-mismatch", {"expected": canonical_expected, "canonical": metrics["canonical"], "ogUrl": metrics["ogUrl"]}, route=route)
            if route in PUBLIC_ROUTES and (not metrics["description"] or len(metrics["description"]) < 50):
                add("medium", "weak-meta-description", metrics["description"], route=route)
            if route in PUBLIC_ROUTES:
                if metrics["title"] in title_seen:
                    add("medium", "duplicate-title", {"other": title_seen[metrics["title"]], "title": metrics["title"]}, route=route)
                else:
                    title_seen[metrics["title"]] = route
                if metrics["description"] in description_seen:
                    add("medium", "duplicate-description", {"other": description_seen[metrics["description"]]}, route=route)
                else:
                    description_seen[metrics["description"]] = route
            for raw_json in metrics["jsonLd"]:
                try:
                    json.loads(raw_json)
                except Exception as exc:
                    add("high", "invalid-json-ld", str(exc), route=route)
            if re.search(r"<img\b[^>]*\s/\s+style=", raw, re.I):
                add("medium", "malformed-img-start-tag", "Self-closing slash appears before a later style attribute.", route=route)
        except Exception as exc:
            add("critical", "route-audit-exception", f"{type(exc).__name__}: {exc}", route=route)
        page.close()
    context.close()

    for width, height, label in MOBILE_WIDTHS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        for route in ROUTES:
            page = context.new_page()
            try:
                goto(page, route)
                toggle = page.locator(".menu-toggle")
                if not toggle.is_visible():
                    add("high", "mobile-menu-toggle-missing", True, route=route, viewport=label)
                    page.close()
                    continue
                toggle.click()
                page.wait_for_timeout(350)
                m = page.evaluate("""() => {
                  const nav=document.querySelector('.primary-nav'); const toggle=document.querySelector('.menu-toggle');
                  const r=nav.getBoundingClientRect(); const visible=el=>{const s=getComputedStyle(el),x=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.01&&x.width>0&&x.height>0};
                  const top=[...nav.children].map(el=>el.matches('a[href]')?el:el.matches('.nav-dropdown')?el.querySelector(':scope > button'):null).filter(Boolean);
                  const visibleTop=top.filter(visible).map(el=>(el.innerText||el.textContent||'').trim());
                  const first=top.filter(visible)[0];
                  return {open:nav.classList.contains('open'),expanded:toggle.getAttribute('aria-expanded'),rect:{top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height},
                    clientHeight:nav.clientHeight,scrollHeight:nav.scrollHeight,visibleTop,bodyLocked:document.body.classList.contains('menu-open'),firstFocused:document.activeElement===first};
                }""")
                page.screenshot(path=str(SHOTS / f"menu-{route.strip('/').replace('/','-') or 'home'}--{label}.png"), full_page=False)
                page.keyboard.press("Escape")
                page.wait_for_timeout(100)
                m["closedByEscape"] = toggle.get_attribute("aria-expanded") == "false"
                menu_records.append({"route": route, "viewport": label, **m})
                min_height = max(250, height - m["rect"]["top"] - 8)
                if not m["open"] or m["expanded"] != "true" or not m["bodyLocked"] or not m["closedByEscape"]:
                    add("high", "mobile-menu-state-contract", m, route=route, viewport=label)
                if len(m["visibleTop"]) < 8:
                    add("critical", "mobile-menu-items-hidden", m, route=route, viewport=label)
                if m["rect"]["height"] < min_height or m["rect"]["bottom"] < height - 4:
                    add("critical", "mobile-menu-collapsed-height", {"minimum": min_height, **m}, route=route, viewport=label)
                if not m["firstFocused"]:
                    add("medium", "mobile-menu-initial-focus", m, route=route, viewport=label)
            except Exception as exc:
                add("critical", "mobile-menu-audit-exception", f"{type(exc).__name__}: {exc}", route=route, viewport=label)
            page.close()
        context.close()

    for width, height, label in MOBILE_WIDTHS:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        for route in FORM_ROUTES:
            page = context.new_page()
            try:
                goto(page, route)
                form = page.locator("form[data-form]").first
                if form.count() != 1:
                    add("high", "canonical-form-missing", True, route=route, viewport=label)
                    page.close()
                    continue
                submit = form.locator('button[type="submit"]')
                submit.click()
                page.wait_for_timeout(100)
                first = form.locator('[aria-invalid="true"]').first
                before = first.count()
                if before:
                    described = first.get_attribute("aria-describedby") or ""
                    first.fill("Audit value")
                    page.wait_for_timeout(80)
                    stale = page.evaluate("""({selector, ids}) => ids.filter(id=>!document.getElementById(id)),""", {"selector": "", "ids": described.split()})
                else:
                    described = ""
                    stale = []
                record = {"route": route, "viewport": label, "invalidBefore": before, "ariaDescribedBy": described, "staleDescriptionIdsAfterCorrection": stale}
                form_records.append(record)
                if before < 1:
                    add("high", "empty-submit-not-rejected", record, route=route, viewport=label)
                if stale:
                    add("high", "stale-aria-describedby", record, route=route, viewport=label)
            except Exception as exc:
                add("critical", "form-audit-exception", f"{type(exc).__name__}: {exc}", route=route, viewport=label)
            page.close()
        context.close()

    def request_record(name: str, response, expected: int):
        item = {"name": name, "status": response.status, "expected": expected, "body": response.text()[:600]}
        api_records.append(item)
        if response.status != expected:
            add("high", "api-negative-contract", item)

    request_record("contact-get", request.get(f"{BASE}/api/contact", fail_on_status_code=False), 405)
    request_record("contact-wrong-content-type", request.post(f"{BASE}/api/contact", data="x", headers={"Content-Type": "text/plain"}, fail_on_status_code=False), 415)
    request_record("contact-empty-json", request.post(f"{BASE}/api/contact", data="{}", headers={"Content-Type": "application/json"}, fail_on_status_code=False), 400)
    request_record("project-empty-json", request.post(f"{BASE}/api/project", data="{}", headers={"Content-Type": "application/json"}, fail_on_status_code=False), 400)
    request_record("document-empty-json", request.post(f"{BASE}/api/document-request", data="{}", headers={"Content-Type": "application/json"}, fail_on_status_code=False), 400)
    request_record("contact-cross-site", request.post(f"{BASE}/api/contact", data="{}", headers={"Content-Type": "application/json", "Sec-Fetch-Site": "cross-site"}, fail_on_status_code=False), 403)

    manifest = request.get(f"{BASE}/site.webmanifest", fail_on_status_code=False)
    try:
        manifest_body = manifest.json()
    except Exception:
        manifest_body = {}
    purposes = [icon.get("purpose") for icon in manifest_body.get("icons", [])]
    if manifest.status != 200 or not purposes or any(p != "any" for p in purposes):
        add("medium", "manifest-icon-purpose", {"status": manifest.status, "icons": manifest_body.get("icons")})

    sitemap = request.get(f"{BASE}/sitemap.xml", fail_on_status_code=False)
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap.text()) if sitemap.status == 200 else []
    if sitemap.status != 200 or len(sitemap_urls) != len(PUBLIC_ROUTES) or len(set(sitemap_urls)) != len(PUBLIC_ROUTES):
        add("high", "sitemap-contract", {"status": sitemap.status, "count": len(sitemap_urls), "unique": len(set(sitemap_urls))})

    robots = request.get(f"{BASE}/robots.txt", fail_on_status_code=False)
    if robots.status != 200 or f"Sitemap: {BASE}/sitemap.xml" not in robots.text():
        add("medium", "robots-contract", {"status": robots.status, "body": robots.text()})

    unknown = request.get(f"{BASE}/definitely-not-real-post-deployment-audit", fail_on_status_code=False)
    if unknown.status != 404:
        add("critical", "unknown-route-not-404", unknown.status)

    request.dispose()
    browser.close()

for message in console_messages:
    add("high", "console-warning-or-error", message, route=message.get("route"))

summary = {
    "baseUrl": BASE,
    "expectedReleaseSha": EXPECTED_SHA,
    "generatedAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "routeCount": len(ROUTES),
    "routeSemanticCells": len(route_records),
    "mobileMenuCells": len(menu_records),
    "formCleanupCells": len(form_records),
    "apiNegativeCells": len(api_records),
    "findingCount": len(findings),
    "severityCounts": dict(Counter(f["severity"] for f in findings)),
    "findingCodes": dict(Counter(f["code"] for f in findings)),
    "consoleMessageCount": len(console_messages),
}

(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
(OUT / "findings.json").write_text(json.dumps(findings, indent=2))
(OUT / "routes.json").write_text(json.dumps(route_records, indent=2))
(OUT / "mobile-menus.json").write_text(json.dumps(menu_records, indent=2))
(OUT / "form-cleanup.json").write_text(json.dumps(form_records, indent=2))
(OUT / "api-negative-contracts.json").write_text(json.dumps(api_records, indent=2))
(OUT / "console.json").write_text(json.dumps(console_messages, indent=2))
print(json.dumps(summary, indent=2))
