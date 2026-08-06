from __future__ import annotations

from pathlib import Path
import json
import os
import re
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("AUDIT_BASE_URL", "https://techgrity.co.zw").rstrip("/")
EXPECTED_RELEASE_SHA = os.environ.get(
    "EXPECTED_RELEASE_SHA", "a729d9f1df31acd9835bad9ee7b78408bf3d9672"
)
BROWSER_NAME = os.environ.get("AUDIT_BROWSER", "chromium")
VIEWPORT_LABEL = os.environ.get("AUDIT_VIEWPORT", "desktop")
CAPTURE_MODE = os.environ.get("AUDIT_CAPTURE_MODE", "scroll")

VIEWPORTS = {
    "desktop-wide": {"width": 1672, "height": 941},
    "desktop": {"width": 1440, "height": 900},
    "desktop-compact": {"width": 1280, "height": 720},
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
OUT = ROOT / "evidence" / "manual-visual" / BROWSER_NAME / VIEWPORT_LABEL
FULL = OUT / "full-page"
SCROLL = OUT / "scroll-states"
INTERACTIONS = OUT / "interaction-states"
for directory in (FULL, SCROLL, INTERACTIONS):
    directory.mkdir(parents=True, exist_ok=True)

records: list[dict] = []
errors: list[dict] = []


def slug(route: str) -> str:
    if route == "/":
        return "home"
    return re.sub(r"[^a-z0-9]+", "-", route.strip("/").lower()).strip("-") or "home"


def wait_for_settle(page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(450)


def save_viewport(page, destination: Path) -> None:
    page.screenshot(path=str(destination), type="jpeg", quality=92, full_page=False)


def capture_scroll_states(page, route_slug: str) -> list[dict]:
    metrics = page.evaluate(
        """() => ({
          scrollHeight: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
          clientHeight: document.documentElement.clientHeight,
          clientWidth: document.documentElement.clientWidth
        })"""
    )
    max_scroll = max(0, int(metrics["scrollHeight"] - metrics["clientHeight"]))
    if CAPTURE_MODE == "full-only":
        positions = [0, max_scroll // 2, max_scroll]
    else:
        step = max(1, int(metrics["clientHeight"] * 0.82))
        positions = list(range(0, max_scroll + 1, step))
        if not positions or positions[-1] != max_scroll:
            positions.append(max_scroll)

    states: list[dict] = []
    for index, y in enumerate(dict.fromkeys(positions)):
        page.evaluate("y => window.scrollTo(0, y)", y)
        page.wait_for_timeout(220)
        state = page.evaluate(
            """() => {
              const header = document.querySelector('.site-header');
              const rect = header?.getBoundingClientRect();
              const active = document.activeElement;
              return {
                scrollY: Math.round(window.scrollY),
                viewportHeight: window.innerHeight,
                viewportWidth: window.innerWidth,
                documentHeight: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
                header: header ? {
                  position: getComputedStyle(header).position,
                  top: Math.round(rect.top),
                  bottom: Math.round(rect.bottom),
                  height: Math.round(rect.height),
                  visible: rect.bottom > 0 && rect.top < window.innerHeight
                } : null,
                activeTag: active?.tagName || null
              };
            }"""
        )
        filename = f"{route_slug}--{index:02d}--y{state['scrollY']}.jpg"
        save_viewport(page, SCROLL / filename)
        states.append({"file": filename, **state})
    return states


def capture_navigation(page, route_slug: str) -> list[dict]:
    captures: list[dict] = []
    is_responsive = VIEWPORT["width"] <= 1100
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(150)

    if is_responsive:
        toggle = page.locator(".menu-toggle")
        if toggle.count() and toggle.is_visible():
            for position_name, y in (("top", 0), ("middle", page.evaluate("Math.max(0, (document.documentElement.scrollHeight - innerHeight) / 2)"))):
                page.evaluate("y => window.scrollTo(0, y)", y)
                page.wait_for_timeout(160)
                toggle.click()
                page.wait_for_timeout(260)
                state = page.evaluate(
                    """() => {
                      const nav=document.querySelector('.primary-nav');
                      const toggle=document.querySelector('.menu-toggle');
                      const rect=nav?.getBoundingClientRect();
                      const visible=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.01&&r.width>0&&r.height>0};
                      const top=[...nav.children].map(el=>el.matches('a[href]')?el:el.matches('.nav-dropdown')?el.querySelector(':scope > button'):null).filter(Boolean);
                      return {
                        scrollY: Math.round(window.scrollY),
                        expanded: toggle?.getAttribute('aria-expanded'),
                        navRect: rect ? {top:Math.round(rect.top),bottom:Math.round(rect.bottom),width:Math.round(rect.width),height:Math.round(rect.height)} : null,
                        visibleTopItems: top.filter(visible).map(el=>(el.innerText||el.textContent||'').trim()),
                        bodyLocked: document.body.classList.contains('menu-open')
                      };
                    }"""
                )
                filename = f"{route_slug}--menu-{position_name}.jpg"
                save_viewport(page, INTERACTIONS / filename)
                captures.append({"type": f"menu-{position_name}", "file": filename, **state})
                page.keyboard.press("Escape")
                page.wait_for_timeout(120)
    elif VIEWPORT_LABEL == "desktop":
        buttons = page.locator(".nav-dropdown > button")
        for index in range(buttons.count()):
            button = buttons.nth(index)
            label = re.sub(r"[^a-z0-9]+", "-", (button.inner_text() or f"dropdown-{index}").lower()).strip("-")
            button.click()
            page.wait_for_timeout(220)
            filename = f"{route_slug}--dropdown-{label}.jpg"
            save_viewport(page, INTERACTIONS / filename)
            captures.append({"type": "desktop-dropdown", "label": label, "file": filename})
            page.keyboard.press("Escape")
            page.wait_for_timeout(100)
    return captures


def capture_cookie_panel(page, route_slug: str) -> dict | None:
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(160)
    manage = page.locator("[data-cookie-manage]")
    if not manage.count():
        return None
    manage.evaluate("el => el.click()")
    page.wait_for_timeout(220)
    filename = f"{route_slug}--cookie-panel.jpg"
    save_viewport(page, INTERACTIONS / filename)
    state = page.evaluate(
        """() => {
          const panel=document.querySelector('[data-cookie-panel]');
          const r=panel?.getBoundingClientRect();
          return {hidden:panel?.hidden,rect:r?{top:Math.round(r.top),bottom:Math.round(r.bottom),left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),height:Math.round(r.height)}:null};
        }"""
    )
    page.keyboard.press("Escape")
    return {"type": "cookie-panel", "file": filename, **state}


def capture_form_validation(page, route_slug: str) -> dict | None:
    form = page.locator("form[data-form]").first
    if form.count() != 1:
        return None
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    form.scroll_into_view_if_needed()
    page.wait_for_timeout(180)
    submit = form.locator('button[type="submit"]')
    submit.click()
    page.wait_for_timeout(180)
    filename = f"{route_slug}--form-empty-validation.jpg"
    save_viewport(page, INTERACTIONS / filename)
    state = page.evaluate(
        """() => ({
          invalidCount: document.querySelectorAll('form[data-form] [aria-invalid="true"]').length,
          errorCount: document.querySelectorAll('form[data-form] .field-error').length,
          focusedId: document.activeElement?.id || document.activeElement?.name || null
        })"""
    )
    return {"type": "form-empty-validation", "file": filename, **state}


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
    try:
        release_json = json.loads(release_payload)
    except Exception:
        release_json = {}
    actual_release = release_json.get("commit")
    if actual_release != EXPECTED_RELEASE_SHA:
        raise RuntimeError(f"Release mismatch: expected {EXPECTED_RELEASE_SHA}, got {actual_release}")

    for route in ROUTES:
        route_slug = slug(route)
        page = context.new_page()
        console: list[dict] = []
        page.on("console", lambda message, r=route: console.append({"route": r, "type": message.type, "text": message.text}) if message.type in {"warning", "error"} else None)
        page.on("pageerror", lambda error, r=route: console.append({"route": r, "type": "pageerror", "text": str(error)}))
        started = time.time()
        record: dict = {
            "route": route,
            "slug": route_slug,
            "browser": BROWSER_NAME,
            "viewport": {"label": VIEWPORT_LABEL, **VIEWPORT},
        }
        try:
            response = page.goto(f"{BASE_URL}{route}", wait_until="domcontentloaded", timeout=35_000)
            wait_for_settle(page)
            record["status"] = response.status if response else None
            record["url"] = page.url
            record["title"] = page.title()
            record["loadSeconds"] = round(time.time() - started, 3)
            full_filename = f"{route_slug}--{BROWSER_NAME}--{VIEWPORT_LABEL}.jpg"
            page.screenshot(path=str(FULL / full_filename), type="jpeg", quality=92, full_page=True)
            record["fullPageFile"] = full_filename
            record["scrollStates"] = capture_scroll_states(page, route_slug)
            record["navigationStates"] = capture_navigation(page, route_slug)
            cookie = capture_cookie_panel(page, route_slug)
            record["cookieState"] = cookie
            form = capture_form_validation(page, route_slug)
            record["formState"] = form
            record["console"] = console
            record["finalMetrics"] = page.evaluate(
                """() => ({
                  scrollHeight: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
                  scrollWidth: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
                  clientWidth: document.documentElement.clientWidth,
                  clientHeight: document.documentElement.clientHeight,
                  h1Count: document.querySelectorAll('h1').length,
                  mainCount: document.querySelectorAll('main').length,
                  brokenImages: [...document.images].filter(img=>!img.complete||img.naturalWidth===0).map(img=>img.src)
                })"""
            )
        except Exception as exc:
            record["exception"] = f"{type(exc).__name__}: {exc}"
            errors.append({"route": route, "exception": record["exception"]})
        finally:
            records.append(record)
            page.close()

    context.close()
    browser.close()

manifest = {
    "baseUrl": BASE_URL,
    "expectedReleaseSha": EXPECTED_RELEASE_SHA,
    "browser": BROWSER_NAME,
    "viewport": {"label": VIEWPORT_LABEL, **VIEWPORT},
    "captureMode": CAPTURE_MODE,
    "routeCount": len(ROUTES),
    "recordCount": len(records),
    "errorCount": len(errors),
    "records": records,
    "errors": errors,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({k: manifest[k] for k in ["browser", "viewport", "captureMode", "routeCount", "recordCount", "errorCount"]}, indent=2))
if errors:
    raise SystemExit(f"Manual visual capture failed for {len(errors)} route(s).")
