from __future__ import annotations

from pathlib import Path
import json
import os
import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = "https://techgrity.co.zw"
EXPECTED_RELEASE_SHA = "a729d9f1df31acd9835bad9ee7b78408bf3d9672"
BROWSER_NAME = os.environ.get("AUDIT_BROWSER", "chromium")
VIEWPORT_LABEL = os.environ.get("AUDIT_VIEWPORT", "mobile")
VIEWPORTS = {
    "tablet-landscape": {"width": 1024, "height": 768},
    "tablet-portrait": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
    "mobile-narrow": {"width": 320, "height": 568},
}
VIEWPORT = VIEWPORTS[VIEWPORT_LABEL]
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
    "/discuss-a-project/", "/privacy/", "/terms/", "/cookies/", "/404/",
    "/project-enquiry-received/", "/document-request-received/", "/form-error/",
]
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "manual-pointer-navigation" / BROWSER_NAME / VIEWPORT_LABEL
OUT.mkdir(parents=True, exist_ok=True)


def slug(route: str) -> str:
    return "home" if route == "/" else re.sub(r"[^a-z0-9]+", "-", route.strip("/").lower()).strip("-")


def settle(page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(400)


def snapshot(page) -> dict:
    return page.evaluate(
        """() => {
          const nav=document.querySelector('.primary-nav');
          const toggle=document.querySelector('.menu-toggle');
          const nr=nav?.getBoundingClientRect();
          const tr=toggle?.getBoundingClientRect();
          const visible=(el)=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.01&&r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth};
          const items=nav?[...nav.children].map(el=>el.matches('a[href]')?el:el.matches('.nav-dropdown')?el.querySelector(':scope > button'):null).filter(Boolean):[];
          return {
            scrollY:Math.round(window.scrollY),
            expanded:toggle?.getAttribute('aria-expanded')||null,
            navOpenClass:Boolean(nav?.classList.contains('open')),
            bodyLocked:document.body.classList.contains('menu-open'),
            toggleRect:tr?{top:Math.round(tr.top),bottom:Math.round(tr.bottom),left:Math.round(tr.left),right:Math.round(tr.right),width:Math.round(tr.width),height:Math.round(tr.height)}:null,
            navRect:nr?{top:Math.round(nr.top),bottom:Math.round(nr.bottom),left:Math.round(nr.left),right:Math.round(nr.right),width:Math.round(nr.width),height:Math.round(nr.height)}:null,
            intersectsViewport:nr?nr.bottom>0&&nr.top<innerHeight&&nr.right>0&&nr.left<innerWidth:false,
            allTopItems:items.map(el=>(el.innerText||el.textContent||'').trim()),
            visibleTopItems:items.filter(visible).map(el=>(el.innerText||el.textContent||'').trim()),
            activeText:(document.activeElement?.innerText||document.activeElement?.textContent||'').trim()
          };
        }"""
    )


def pointer_tap(page, rect: dict) -> dict:
    x=(rect["left"]+rect["right"])/2
    y=(rect["top"]+rect["bottom"])/2
    page.mouse.click(x,y)
    return {"x":round(x,1),"y":round(y,1)}


records=[]
errors=[]
with sync_playwright() as playwright:
    browser=getattr(playwright,BROWSER_NAME).launch(headless=True)
    context=browser.new_context(viewport=VIEWPORT,device_scale_factor=1,color_scheme="light",locale="en-ZW")
    release=context.new_page()
    response=release.goto(f"{BASE_URL}/release.json",wait_until="domcontentloaded",timeout=30_000)
    payload=json.loads(release.locator("body").inner_text() if response else "{}")
    release.close()
    if payload.get("commit")!=EXPECTED_RELEASE_SHA:
        raise RuntimeError(f"Release mismatch: {payload.get('commit')}")

    for route in ROUTES:
        route_record={"route":route,"browser":BROWSER_NAME,"viewport":{"label":VIEWPORT_LABEL,**VIEWPORT},"states":[]}
        try:
            for position in ("top","middle"):
                page=context.new_page()
                response=page.goto(f"{BASE_URL}{route}",wait_until="domcontentloaded",timeout=35_000)
                settle(page)
                if position=="middle":
                    page.evaluate("window.scrollTo(0,Math.max(0,(document.documentElement.scrollHeight-innerHeight)/2))")
                    page.wait_for_timeout(250)
                else:
                    page.evaluate("window.scrollTo(0,0)")
                    page.wait_for_timeout(150)
                before=snapshot(page)
                rect=before.get("toggleRect")
                if not rect or rect["width"]<=0 or rect["height"]<=0:
                    raise RuntimeError(f"{route} {position}: no rendered toggle")
                if not (rect["right"]>0 and rect["left"]<VIEWPORT["width"] and rect["bottom"]>0 and rect["top"]<VIEWPORT["height"]):
                    raise RuntimeError(f"{route} {position}: toggle outside viewport: {rect}")
                tap=pointer_tap(page,rect)
                page.wait_for_timeout(1500)
                opened=snapshot(page)
                filename=f"{slug(route)}--{position}--open.png"
                page.screenshot(path=str(OUT/filename),full_page=False)
                page.keyboard.press("Escape")
                page.wait_for_timeout(350)
                closed=snapshot(page)
                route_record["states"].append({"position":position,"status":response.status if response else None,"file":filename,"tap":tap,"before":before,"opened":opened,"closed":closed})
                page.close()
        except Exception as exc:
            route_record["exception"]=f"{type(exc).__name__}: {exc}"
            errors.append({"route":route,"exception":route_record["exception"]})
        records.append(route_record)
    context.close()
    browser.close()

summary={"baseUrl":BASE_URL,"expectedReleaseSha":EXPECTED_RELEASE_SHA,"browser":BROWSER_NAME,"viewport":{"label":VIEWPORT_LABEL,**VIEWPORT},"routeCount":len(ROUTES),"recordCount":len(records),"errorCount":len(errors),"records":records,"errors":errors}
(OUT/"manifest.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps({key:summary[key] for key in ("browser","viewport","routeCount","recordCount","errorCount")},indent=2))
if errors:
    raise SystemExit(f"Pointer navigation capture failed for {len(errors)} route(s).")
