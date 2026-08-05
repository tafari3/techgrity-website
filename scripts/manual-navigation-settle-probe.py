from __future__ import annotations

from pathlib import Path
import json
import os

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = "https://techgrity.co.zw"
EXPECTED_RELEASE_SHA = "a729d9f1df31acd9835bad9ee7b78408bf3d9672"
BROWSER_NAME = os.environ.get("AUDIT_BROWSER", "webkit")
VIEWPORT = {"width": 390, "height": 844}
ROUTES = ["/", "/capabilities/"]
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "manual-navigation-settle" / BROWSER_NAME
OUT.mkdir(parents=True, exist_ok=True)


def wait_for_settle(page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(500)


def sample(page, elapsed_ms: int) -> dict:
    return page.evaluate(
        """elapsed => {
          const nav=document.querySelector('.primary-nav');
          const toggle=document.querySelector('.menu-toggle');
          const rect=nav?.getBoundingClientRect();
          const toggleRect=toggle?.getBoundingClientRect();
          const style=nav ? getComputedStyle(nav) : null;
          return {
            elapsedMs: elapsed,
            scrollY: Math.round(window.scrollY),
            expanded: toggle?.getAttribute('aria-expanded'),
            openClass: nav?.classList.contains('open'),
            bodyLocked: document.body.classList.contains('menu-open'),
            toggleRect: toggleRect ? {
              top:Math.round(toggleRect.top), bottom:Math.round(toggleRect.bottom),
              left:Math.round(toggleRect.left), right:Math.round(toggleRect.right),
              width:Math.round(toggleRect.width), height:Math.round(toggleRect.height)
            } : null,
            rect: rect ? {
              top:Math.round(rect.top), bottom:Math.round(rect.bottom),
              left:Math.round(rect.left), right:Math.round(rect.right),
              width:Math.round(rect.width), height:Math.round(rect.height)
            } : null,
            style: style ? {
              transform:style.transform, transitionDuration:style.transitionDuration,
              position:style.position, visibility:style.visibility, opacity:style.opacity
            } : null,
            intersectsViewport: rect ? rect.right>0 && rect.left<innerWidth && rect.bottom>0 && rect.top<innerHeight : false
          };
        }""",
        elapsed_ms,
    )


records=[]
with sync_playwright() as playwright:
    browser=getattr(playwright, BROWSER_NAME).launch(headless=True)
    context=browser.new_context(viewport=VIEWPORT, device_scale_factor=1, color_scheme="light", locale="en-ZW")

    release=context.new_page()
    response=release.goto(f"{BASE_URL}/release.json", wait_until="domcontentloaded", timeout=30_000)
    payload=json.loads(release.locator("body").inner_text() if response else "{}")
    release.close()
    if payload.get("commit") != EXPECTED_RELEASE_SHA:
        raise RuntimeError(f"Release mismatch: {payload.get('commit')}")

    for route in ROUTES:
        for position in ("top", "middle"):
            page=context.new_page()
            response=page.goto(f"{BASE_URL}{route}", wait_until="domcontentloaded", timeout=35_000)
            wait_for_settle(page)
            if position == "middle":
                page.evaluate("window.scrollTo(0, Math.max(0, (document.documentElement.scrollHeight-innerHeight)/2))")
                page.wait_for_timeout(250)
            else:
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(150)

            before=sample(page, -1)
            toggle_rect=before.get("toggleRect")
            if not toggle_rect or toggle_rect["width"] <= 0 or toggle_rect["height"] <= 0:
                raise RuntimeError(f"{route} {position}: toggle unavailable")
            if not (toggle_rect["right"] > 0 and toggle_rect["left"] < VIEWPORT["width"] and toggle_rect["bottom"] > 0 and toggle_rect["top"] < VIEWPORT["height"]):
                raise RuntimeError(f"{route} {position}: sticky toggle is not in the viewport before tap: {toggle_rect}")

            click_x=(toggle_rect["left"]+toggle_rect["right"])/2
            click_y=(toggle_rect["top"]+toggle_rect["bottom"])/2
            page.mouse.click(click_x, click_y)

            timeline=[]
            previous=0
            for elapsed in (50, 250, 750, 1500):
                page.wait_for_timeout(elapsed-previous)
                timeline.append(sample(page, elapsed))
                previous=elapsed

            slug='home' if route=='/' else 'capabilities'
            filename=f"{slug}--{position}--settled.png"
            page.screenshot(path=str(OUT/filename), full_page=False)

            page.keyboard.press('Escape')
            page.wait_for_timeout(350)
            after_close=sample(page, 1850)

            records.append({
                "route":route,"position":position,"browser":BROWSER_NAME,
                "status":response.status if response else None,"file":filename,
                "before":before,"tap":{"x":click_x,"y":click_y},
                "timeline":timeline,"afterClose":after_close
            })
            page.close()

    context.close()
    browser.close()

summary={"browser":BROWSER_NAME,"viewport":VIEWPORT,"records":records}
(OUT/'manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
