from __future__ import annotations

from pathlib import Path
import json
import os
import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("AUDIT_BASE_URL", "https://techgrity.co.zw").rstrip("/")
EXPECTED_RELEASE_SHA = os.environ.get(
    "EXPECTED_RELEASE_SHA", "a729d9f1df31acd9835bad9ee7b78408bf3d9672"
)
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


def set_scroll_position(page, position: str) -> dict:
    setup = page.evaluate(
        """(position) => new Promise((resolve) => {
          const root = document.documentElement;
          const previousInlineScrollBehavior = root.style.scrollBehavior;
          root.style.scrollBehavior = 'auto';
          const target = position === 'middle'
            ? Math.max(0, Math.round((root.scrollHeight - innerHeight) / 2))
            : 0;
          window.scrollTo({top: target, left: 0, behavior: 'auto'});
          requestAnimationFrame(() => requestAnimationFrame(() => {
            const actual = Math.round(window.scrollY);
            root.style.scrollBehavior = previousInlineScrollBehavior;
            resolve({target, actual, previousInlineScrollBehavior});
          }));
        })""",
        position,
    )
    samples = []
    for _ in range(4):
        samples.append(round(page.evaluate("window.scrollY")))
        page.wait_for_timeout(50)
    setup["samples"] = samples
    if max(samples) - min(samples) > 1:
        raise RuntimeError(f"{position}: scroll baseline did not settle: {samples}")
    if abs(samples[-1] - setup["actual"]) > 1:
        raise RuntimeError(
            f"{position}: scroll baseline changed after setup: {setup['actual']} -> {samples[-1]}"
        )
    return setup


def mark_scroll_anchor(page, token: str) -> dict:
    return page.evaluate(
        """(token) => {
          document.querySelectorAll('[data-audit-scroll-anchor]').forEach((node) => {
            node.removeAttribute('data-audit-scroll-anchor');
          });
          const headerBottom = document.querySelector('header')?.getBoundingClientRect().bottom || 0;
          const y = Math.min(innerHeight - 24, Math.max(headerBottom + 24, Math.round(innerHeight * 0.58)));
          const x = Math.min(innerWidth - 24, Math.max(24, Math.round(innerWidth * 0.32)));
          const usable = (node) => {
            if (!node || node === document.body || node === document.documentElement) return false;
            if (!node.closest('main')) return false;
            const style = getComputedStyle(node);
            const rect = node.getBoundingClientRect();
            return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
          };
          let node = document.elementFromPoint(x, y);
          while (node && !usable(node)) node = node.parentElement;
          if (!usable(node)) {
            const candidates = [...document.querySelectorAll('main h1, main h2, main h3, main p, main li, main article, main section, main div')]
              .filter(usable)
              .map((candidate) => ({candidate, rect: candidate.getBoundingClientRect()}))
              .filter(({rect}) => rect.bottom >= y && rect.top <= y)
              .sort((a, b) => (a.rect.width * a.rect.height) - (b.rect.width * b.rect.height));
            node = candidates[0]?.candidate || [...document.querySelectorAll('main h1, main h2, main h3, main p, main section')].find(usable);
          }
          if (!node) throw new Error('Unable to select a visible page anchor');
          node.setAttribute('data-audit-scroll-anchor', token);
          const rect = node.getBoundingClientRect();
          return {
            token,
            tag: node.tagName,
            id: node.id || null,
            text: (node.innerText || node.textContent || '').trim().slice(0, 120),
            top: Math.round(rect.top),
            left: Math.round(rect.left),
            sample: {x, y}
          };
        }""",
        token,
    )


def snapshot(page) -> dict:
    return page.evaluate(
        """() => {
          const nav=document.querySelector('.primary-nav');
          const toggle=document.querySelector('.menu-toggle');
          const anchor=document.querySelector('[data-audit-scroll-anchor]');
          const nr=nav?.getBoundingClientRect();
          const tr=toggle?.getBoundingClientRect();
          const ar=anchor?.getBoundingClientRect();
          const body=document.body;
          const visible=(el)=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.01&&r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth};
          const items=nav?[...nav.children].map(el=>el.matches('a[href]')?el:el.matches('.nav-dropdown')?el.querySelector(':scope > button'):null).filter(Boolean):[];
          return {
            scrollY:Math.round(window.scrollY),
            expanded:toggle?.getAttribute('aria-expanded')||null,
            navOpenClass:Boolean(nav?.classList.contains('open')),
            bodyLocked:body.classList.contains('menu-open'),
            bodyDatasetScrollY:body.dataset.menuScrollY ?? null,
            bodyInlineStyles:{
              position:body.style.position||'',
              top:body.style.top||'',
              left:body.style.left||'',
              right:body.style.right||'',
              width:body.style.width||'',
              paddingRight:body.style.paddingRight||''
            },
            toggleRect:tr?{top:Math.round(tr.top),bottom:Math.round(tr.bottom),left:Math.round(tr.left),right:Math.round(tr.right),width:Math.round(tr.width),height:Math.round(tr.height)}:null,
            navRect:nr?{top:Math.round(nr.top),bottom:Math.round(nr.bottom),left:Math.round(nr.left),right:Math.round(nr.right),width:Math.round(nr.width),height:Math.round(nr.height)}:null,
            anchorRect:ar?{top:Math.round(ar.top),bottom:Math.round(ar.bottom),left:Math.round(ar.left),right:Math.round(ar.right),width:Math.round(ar.width),height:Math.round(ar.height)}:null,
            anchorToken:anchor?.getAttribute('data-audit-scroll-anchor')||null,
            intersectsViewport:nr?nr.bottom>0&&nr.top<innerHeight&&nr.right>0&&nr.left<innerWidth:false,
            allTopItems:items.map(el=>(el.innerText||el.textContent||'').trim()),
            visibleTopItems:items.filter(visible).map(el=>(el.innerText||el.textContent||'').trim()),
            activeText:(document.activeElement?.innerText||document.activeElement?.textContent||'').trim(),
            activeIsMenuToggle:document.activeElement===toggle
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
                scroll_setup=set_scroll_position(page,position)
                anchor=mark_scroll_anchor(page,f"{slug(route)}--{position}")
                before=snapshot(page)
                if abs(before.get("scrollY",0)-scroll_setup["samples"][-1])>1:
                    raise RuntimeError(
                        f"{route} {position}: baseline changed before pointer tap: "
                        f"{scroll_setup['samples'][-1]} -> {before.get('scrollY',0)}"
                    )
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
                page.wait_for_timeout(500)
                closed=snapshot(page)
                route_record["states"].append({"position":position,"status":response.status if response else None,"file":filename,"tap":tap,"scrollSetup":scroll_setup,"anchor":anchor,"before":before,"opened":opened,"closed":closed})
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
