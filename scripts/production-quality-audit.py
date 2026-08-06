from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import os
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE = os.environ.get("AUDIT_BASE_URL", "https://techgrity.co.zw").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "production-quality-audit"
SHOTS = OUT / "screenshots"
AXE = ROOT / "node_modules" / "axe-core" / "axe.min.js"
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
    "/industries/government-public-sector/", "/industries/education-research/",
    "/industries/telecommunications/", "/industries/energy-utilities-industrial/",
    "/industries/data-centres-technology/",
    "/industries/commerce-logistics-growing-organisations/",
    "/how-we-deliver/", "/company/", "/resources/", "/contact/",
    "/discuss-a-project/", "/privacy/", "/terms/", "/cookies/",
    "/404/", "/project-enquiry-received/",
    "/document-request-received/", "/form-error/",
]
REPRESENTATIVE = [
    "/", "/capabilities/", "/capabilities/digital-systems/software-ai-applications/",
    "/capabilities/infrastructure/data-centres-cloud/", "/industries/",
    "/resources/", "/contact/", "/discuss-a-project/", "/privacy/", "/404/",
]
VIEWPORTS = [(1440, 900, "desktop"), (390, 844, "mobile")]

findings: list[dict] = []
axe_records: list[dict] = []
browser_records: list[dict] = []
performance_records: list[dict] = []
static_records: list[dict] = []


def add(severity: str, code: str, detail, **context):
    findings.append({"severity": severity, "code": code, **context, "detail": detail})


def goto(page, route: str):
    response = page.goto(f"{BASE}{route}", wait_until="domcontentloaded", timeout=30_000)
    try:
        page.wait_for_load_state("networkidle", timeout=5_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(250)
    return response


def slug(route: str) -> str:
    return route.strip("/").replace("/", "-") or "home"


# Static deployment/source contracts that rendered-page checks cannot see.
site_js = (ROOT / "public" / "site.js").read_text()
forms_js = (ROOT / "api" / "_forms.js").read_text()
vercel = json.loads((ROOT / "vercel.json").read_text())
package = json.loads((ROOT / "package.json").read_text())
workflow = (ROOT / ".github" / "workflows" / "site-ci.yml").read_text()

if "+263 78 330 4307" in site_js or "tel:+263783304307" in site_js:
    add("high", "superseded-phone-in-form-fallback", "The client-side failure message still exposes the old telephone number.")
if "${cfg.subject} — ${ref}" in forms_js:
    add("high", "unencoded-nonascii-smtp-subject", "The raw SMTP Subject header uses an unencoded Unicode em dash, matching the observed mojibake.")
asset_headers = [h for h in vercel.get("headers", []) if h.get("source") == "/assets/(.*)"]
for rule in asset_headers:
    cache_values = [h.get("value", "") for h in rule.get("headers", []) if h.get("key", "").lower() == "cache-control"]
    if any("immutable" in value.lower() and "31536000" in value for value in cache_values):
        add("high", "immutable-cache-on-stable-asset-urls", {"source": rule.get("source"), "values": cache_values})
node_engine = package.get("engines", {}).get("node", "")
ci_node = "20" if "node-version: '20'" in workflow else "other"
static_records.append({"nodeEngine": node_engine, "ciNode": ci_node})
if node_engine == ">=20" or ci_node == "20":
    add("medium", "unbounded-or-mismatched-node-major", {"packageEngine": node_engine, "ciNode": ci_node, "productionNode": "24.x"})

with sync_playwright() as p:
    # Automated WCAG 2 A/AA checks in Chromium at desktop and mobile widths.
    chromium = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    for width, height, label in VIEWPORTS:
        context = chromium.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, bypass_csp=True)
        for route in ROUTES:
            page = context.new_page()
            try:
                goto(page, route)
                page.add_script_tag(path=str(AXE))
                result = page.evaluate("""async () => await axe.run(document, {
                  runOnly: {type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa']},
                  resultTypes: ['violations']
                })""")
                violations = []
                for violation in result.get("violations", []):
                    item = {
                        "id": violation.get("id"),
                        "impact": violation.get("impact"),
                        "help": violation.get("help"),
                        "helpUrl": violation.get("helpUrl"),
                        "nodes": [
                            {"target": node.get("target"), "summary": node.get("failureSummary")}
                            for node in violation.get("nodes", [])[:20]
                        ],
                        "nodeCount": len(violation.get("nodes", [])),
                    }
                    violations.append(item)
                    severity = "high" if item["impact"] in {"critical", "serious"} else "medium"
                    add(severity, "axe-" + str(item["id"]), item, route=route, viewport=label)
                axe_records.append({"route": route, "viewport": label, "violations": violations})
            except Exception as exc:
                add("critical", "axe-audit-exception", f"{type(exc).__name__}: {exc}", route=route, viewport=label)
            page.close()
        context.close()

    # Performance and layout-stability observations on representative journeys.
    for width, height, label in VIEWPORTS:
        context = chromium.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        context.add_init_script("""(() => {
          window.__qualityAudit={cls:0,lcp:0,longTasks:0};
          try { new PerformanceObserver(list => list.getEntries().forEach(e => { if(!e.hadRecentInput) window.__qualityAudit.cls += e.value; })).observe({type:'layout-shift',buffered:true}); } catch(e) {}
          try { new PerformanceObserver(list => { const entries=list.getEntries(); const last=entries[entries.length-1]; if(last) window.__qualityAudit.lcp=last.startTime; }).observe({type:'largest-contentful-paint',buffered:true}); } catch(e) {}
          try { new PerformanceObserver(list => { window.__qualityAudit.longTasks += list.getEntries().length; }).observe({type:'longtask',buffered:true}); } catch(e) {}
        })();""")
        for route in REPRESENTATIVE:
            page = context.new_page()
            try:
                goto(page, route)
                page.wait_for_timeout(1200)
                metrics = page.evaluate("""() => {
                  const nav=performance.getEntriesByType('navigation')[0]||{};
                  const resources=performance.getEntriesByType('resource');
                  return {
                    domContentLoaded:nav.domContentLoadedEventEnd||0,
                    loadEvent:nav.loadEventEnd||0,
                    transferBytes:resources.reduce((n,r)=>n+(r.transferSize||0),0),
                    encodedBytes:resources.reduce((n,r)=>n+(r.encodedBodySize||0),0),
                    resourceCount:resources.length,
                    cls:window.__qualityAudit?.cls||0,
                    lcp:window.__qualityAudit?.lcp||0,
                    longTasks:window.__qualityAudit?.longTasks||0
                  };
                }""")
                performance_records.append({"route": route, "viewport": label, **metrics})
                if metrics["cls"] > 0.25:
                    add("high", "excessive-layout-shift", metrics, route=route, viewport=label)
                elif metrics["cls"] > 0.1:
                    add("medium", "layout-shift-needs-improvement", metrics, route=route, viewport=label)
                if metrics["lcp"] > 4000:
                    add("medium", "slow-observed-lcp", metrics, route=route, viewport=label)
                if metrics["transferBytes"] > 4_000_000:
                    add("medium", "large-page-transfer", metrics, route=route, viewport=label)
            except Exception as exc:
                add("critical", "performance-audit-exception", f"{type(exc).__name__}: {exc}", route=route, viewport=label)
            page.close()
        context.close()
    chromium.close()

    # Representative rendering and interaction checks across all three browser engines.
    for browser_name, browser_type in [("chromium", p.chromium), ("firefox", p.firefox), ("webkit", p.webkit)]:
        browser = browser_type.launch(headless=True)
        for width, height, label in VIEWPORTS:
            context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
            for route in REPRESENTATIVE:
                page = context.new_page()
                errors: list[str] = []
                page.on("pageerror", lambda err, bag=errors: bag.append(str(err)))
                page.on("console", lambda msg, bag=errors: bag.append(msg.text) if msg.type == "error" else None)
                try:
                    response = goto(page, route)
                    before = page.evaluate("""() => ({
                      width:document.documentElement.clientWidth,
                      scrollWidth:document.documentElement.scrollWidth,
                      h1:document.querySelectorAll('h1').length
                    })""")
                    page.evaluate("window.scrollTo(0,document.documentElement.scrollHeight)")
                    page.wait_for_timeout(120)
                    header_visible = page.locator(".site-header").is_visible()
                    menu = None
                    if label == "mobile":
                        toggle = page.locator(".menu-toggle")
                        toggle.click()
                        page.wait_for_timeout(180)
                        menu = page.evaluate("""() => {
                          const n=document.querySelector('.primary-nav'), r=n.getBoundingClientRect();
                          return {open:n.classList.contains('open'),height:r.height,scrollHeight:n.scrollHeight,bottom:r.bottom,viewport:innerHeight};
                        }""")
                    record = {
                        "browser": browser_name, "route": route, "viewport": label,
                        "status": response.status, "overflow": before["scrollWidth"] > before["width"] + 1,
                        "h1": before["h1"], "headerVisibleAfterScroll": header_visible,
                        "menu": menu, "errors": errors,
                    }
                    browser_records.append(record)
                    if response.status != 200 or record["overflow"] or record["h1"] != 1 or not header_visible or errors:
                        add("high", "cross-browser-render-contract", record, browser=browser_name, route=route, viewport=label)
                    if menu and (not menu["open"] or menu["height"] < 250 or menu["bottom"] < menu["viewport"] - 4):
                        add("high", "cross-browser-mobile-menu-contract", record, browser=browser_name, route=route, viewport=label)
                        page.screenshot(path=str(SHOTS / f"{browser_name}-{slug(route)}-{label}.png"), full_page=False)
                except Exception as exc:
                    add("critical", "cross-browser-audit-exception", f"{type(exc).__name__}: {exc}", browser=browser_name, route=route, viewport=label)
                page.close()
            context.close()
        browser.close()

summary = {
    "baseUrl": BASE,
    "generatedAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "axeCells": len(axe_records),
    "crossBrowserCells": len(browser_records),
    "performanceCells": len(performance_records),
    "staticChecks": len(static_records),
    "findingCount": len(findings),
    "severityCounts": dict(Counter(f["severity"] for f in findings)),
    "findingCodes": dict(Counter(f["code"] for f in findings)),
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
(OUT / "findings.json").write_text(json.dumps(findings, indent=2))
(OUT / "axe.json").write_text(json.dumps(axe_records, indent=2))
(OUT / "cross-browser.json").write_text(json.dumps(browser_records, indent=2))
(OUT / "performance.json").write_text(json.dumps(performance_records, indent=2))
(OUT / "static.json").write_text(json.dumps(static_records, indent=2))
print(json.dumps(summary, indent=2))
