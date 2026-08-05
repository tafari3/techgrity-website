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
    "desktop": {"width": 1440, "height": 900},
    "tablet-landscape": {"width": 1024, "height": 768},
    "tablet-portrait": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
    "mobile-narrow": {"width": 320, "height": 568},
}

ROUTES = [
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
    "/404/",
    "/project-enquiry-received/",
    "/document-request-received/",
    "/form-error/",
]

VIEWPORT = VIEWPORTS[VIEWPORT_LABEL]
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "manual-interaction-recapture" / BROWSER_NAME / VIEWPORT_LABEL
OUT.mkdir(parents=True, exist_ok=True)


def slug(route: str) -> str:
    if route == "/":
        return "home"
    return re.sub(r"[^a-z0-9]+", "-", route.strip("/").lower()).strip("-") or "home"


def wait_for_settle(page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(350)


def open_page(context, route: str):
    page = context.new_page()
    response = page.goto(f"{BASE_URL}{route}", wait_until="domcontentloaded", timeout=35_000)
    wait_for_settle(page)
    if response is None:
        raise RuntimeError(f"No response for {route}")
    return page, response.status


def inspect_mobile_menu(page, route: str, position_name: str) -> dict:
    if position_name == "middle":
        page.evaluate(
            "window.scrollTo(0, Math.max(0, (document.documentElement.scrollHeight - innerHeight) / 2))"
        )
        page.wait_for_timeout(220)
    else:
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(180)

    toggle = page.locator(".menu-toggle")
    if toggle.count() != 1 or not toggle.is_visible():
        raise RuntimeError(f"{route} {position_name}: visible menu toggle not found")

    toggle.evaluate("element => element.click()")
    page.wait_for_function(
        """() => {
          const toggle=document.querySelector('.menu-toggle');
          const nav=document.querySelector('.primary-nav');
          return toggle?.getAttribute('aria-expanded')==='true' && nav?.classList.contains('open');
        }""",
        timeout=4_000,
    )
    page.wait_for_timeout(260)

    state = page.evaluate(
        """() => {
          const nav=document.querySelector('.primary-nav');
          const toggle=document.querySelector('.menu-toggle');
          if (!nav || !toggle) return null;
          const rect=nav.getBoundingClientRect();
          const style=getComputedStyle(nav);
          const visible=(element)=>{
            const itemStyle=getComputedStyle(element);
            const itemRect=element.getBoundingClientRect();
            return itemStyle.display!=='none' && itemStyle.visibility!=='hidden' &&
              Number(itemStyle.opacity || 1) > .01 && itemRect.width > 0 && itemRect.height > 0 &&
              itemRect.bottom > 0 && itemRect.top < innerHeight;
          };
          const topItems=[...nav.children].map((element)=>
            element.matches('a[href]') ? element :
            element.matches('.nav-dropdown') ? element.querySelector(':scope > button') : null
          ).filter(Boolean);
          return {
            scrollY: Math.round(window.scrollY),
            expanded: toggle.getAttribute('aria-expanded'),
            navOpenClass: nav.classList.contains('open'),
            bodyLocked: document.body.classList.contains('menu-open'),
            navRect: {
              top: Math.round(rect.top),
              bottom: Math.round(rect.bottom),
              left: Math.round(rect.left),
              right: Math.round(rect.right),
              width: Math.round(rect.width),
              height: Math.round(rect.height)
            },
            navStyle: {
              display: style.display,
              visibility: style.visibility,
              opacity: style.opacity,
              overflowY: style.overflowY,
              position: style.position
            },
            allTopItems: topItems.map((element)=>(element.innerText || element.textContent || '').trim()),
            visibleTopItems: topItems.filter(visible).map((element)=>(element.innerText || element.textContent || '').trim()),
            activeText: (document.activeElement?.innerText || document.activeElement?.textContent || '').trim()
          };
        }"""
    )
    if not state:
        raise RuntimeError(f"{route} {position_name}: menu state could not be read")
    if state["expanded"] != "true" or not state["navOpenClass"]:
        raise RuntimeError(f"{route} {position_name}: menu did not remain open")
    if state["navRect"]["width"] <= 0 or state["navRect"]["height"] <= 0:
        raise RuntimeError(f"{route} {position_name}: open menu has no rendered area")
    if not state["allTopItems"]:
        raise RuntimeError(f"{route} {position_name}: open menu has no top-level items")

    filename = f"{slug(route)}--menu-{position_name}.png"
    page.screenshot(path=str(OUT / filename), full_page=False)
    state["file"] = filename

    page.keyboard.press("Escape")
    page.wait_for_function(
        "document.querySelector('.menu-toggle')?.getAttribute('aria-expanded')==='false'",
        timeout=4_000,
    )
    return state


def inspect_desktop_dropdowns(page, route: str) -> list[dict]:
    records: list[dict] = []
    buttons = page.locator(".nav-dropdown > button")
    for index in range(buttons.count()):
        button = buttons.nth(index)
        label = re.sub(r"[^a-z0-9]+", "-", (button.inner_text() or f"dropdown-{index}").lower()).strip("-")
        button.evaluate("element => element.click()")
        page.wait_for_timeout(220)
        state = page.evaluate(
            """(index) => {
              const button=document.querySelectorAll('.nav-dropdown > button')[index];
              const dropdown=button?.closest('.nav-dropdown');
              const panel=dropdown?.querySelector('.mega-menu, .mini-menu');
              const rect=panel?.getBoundingClientRect();
              const style=panel ? getComputedStyle(panel) : null;
              return {
                expanded: button?.getAttribute('aria-expanded'),
                openClass: dropdown?.classList.contains('open'),
                panelRect: rect ? {top:Math.round(rect.top),bottom:Math.round(rect.bottom),left:Math.round(rect.left),right:Math.round(rect.right),width:Math.round(rect.width),height:Math.round(rect.height)} : null,
                panelStyle: style ? {display:style.display,visibility:style.visibility,opacity:style.opacity} : null,
                linkCount: panel?.querySelectorAll('a[href]').length || 0
              };
            }""",
            index,
        )
        if state["expanded"] != "true" or not state["openClass"] or not state["panelRect"]:
            raise RuntimeError(f"{route} {label}: desktop dropdown did not open")
        filename = f"{slug(route)}--dropdown-{label}.png"
        page.screenshot(path=str(OUT / filename), full_page=False)
        records.append({"label": label, "file": filename, **state})
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
    return records


records: list[dict] = []
errors: list[dict] = []

with sync_playwright() as playwright:
    browser_type = getattr(playwright, BROWSER_NAME)
    browser = browser_type.launch(headless=True)
    context = browser.new_context(
        viewport=VIEWPORT,
        device_scale_factor=1,
        color_scheme="light",
        locale="en-ZW",
        reduced_motion="no-preference",
    )

    release_page = context.new_page()
    release_response = release_page.goto(f"{BASE_URL}/release.json", wait_until="domcontentloaded", timeout=30_000)
    release_payload = release_page.locator("body").inner_text() if release_response else ""
    release_page.close()
    release_json = json.loads(release_payload)
    actual_release = release_json.get("commit")
    if actual_release != EXPECTED_RELEASE_SHA:
        raise RuntimeError(f"Release mismatch: expected {EXPECTED_RELEASE_SHA}, got {actual_release}")

    for route in ROUTES:
        record: dict = {"route": route, "browser": BROWSER_NAME, "viewport": {"label": VIEWPORT_LABEL, **VIEWPORT}}
        try:
            if VIEWPORT["width"] <= 1100:
                states = []
                for position_name in ("top", "middle"):
                    page, status = open_page(context, route)
                    try:
                        state = inspect_mobile_menu(page, route, position_name)
                        states.append({"position": position_name, **state})
                    finally:
                        page.close()
                record["status"] = status
                record["mobileMenus"] = states
            else:
                page, status = open_page(context, route)
                try:
                    record["status"] = status
                    record["desktopDropdowns"] = inspect_desktop_dropdowns(page, route)
                finally:
                    page.close()
        except Exception as exc:
            record["exception"] = f"{type(exc).__name__}: {exc}"
            errors.append({"route": route, "exception": record["exception"]})
        records.append(record)

    context.close()
    browser.close()

manifest = {
    "baseUrl": BASE_URL,
    "expectedReleaseSha": EXPECTED_RELEASE_SHA,
    "browser": BROWSER_NAME,
    "viewport": {"label": VIEWPORT_LABEL, **VIEWPORT},
    "routeCount": len(ROUTES),
    "recordCount": len(records),
    "errorCount": len(errors),
    "records": records,
    "errors": errors,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({key: manifest[key] for key in ["browser", "viewport", "routeCount", "recordCount", "errorCount"]}, indent=2))
if errors:
    raise SystemExit(f"Interaction recapture failed for {len(errors)} route(s).")
