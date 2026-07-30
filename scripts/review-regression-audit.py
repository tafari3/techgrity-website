from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("AUDIT_BASE_URL", "http://127.0.0.1:4173").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "candidate-audit" / "review-regressions.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

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

results: list[dict] = []
findings: list[dict] = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    for route in ROUTES:
        page = context.new_page()
        response = page.goto(f"{BASE}{route}", wait_until="domcontentloaded", timeout=20_000)
        page.wait_for_timeout(60)
        footer = page.evaluate(
            """() => [...document.querySelectorAll('.footer-column')].map((column, columnIndex) => {
              const links = [...column.querySelectorAll('a[href]')].map((link, linkIndex) => {
                const rect = link.getBoundingClientRect();
                const style = getComputedStyle(link);
                return {columnIndex, linkIndex, text:(link.textContent||'').trim(), display:style.display,
                  top:Math.round(rect.top), bottom:Math.round(rect.bottom), left:Math.round(rect.left), right:Math.round(rect.right),
                  width:Math.round(rect.width), height:Math.round(rect.height)};
              });
              return {columnIndex, links};
            })"""
        )
        route_findings = []
        for column in footer:
            links = column["links"]
            for link in links:
                if link["display"] not in {"block", "flex", "grid", "list-item"}:
                    route_findings.append({"code": "footer-link-not-block-level", "detail": link})
                if link["height"] < 44:
                    route_findings.append({"code": "footer-link-touch-target", "detail": link})
            for previous, current in zip(links, links[1:]):
                if current["top"] < previous["bottom"]:
                    route_findings.append({"code": "footer-link-overlap", "detail": {"previous": previous, "current": current}})
                if abs(current["top"] - previous["top"]) <= 2:
                    route_findings.append({"code": "footer-links-share-row", "detail": {"previous": previous, "current": current}})
        results.append({"route": route, "status": response.status if response else None, "columns": footer, "findings": route_findings})
        findings.extend({"route": route, **finding} for finding in route_findings)
        page.close()

    manifest_response = context.request.get(f"{BASE}/site.webmanifest", fail_on_status_code=False)
    manifest = manifest_response.json()
    icons = manifest.get("icons", [])
    if not icons:
        findings.append({"route": "/site.webmanifest", "code": "manifest-icons-missing", "detail": manifest})
    for icon in icons:
        purposes = set(str(icon.get("purpose", "any")).split())
        if "maskable" in purposes:
            findings.append({"route": "/site.webmanifest", "code": "tight-mark-advertised-maskable", "detail": icon})
        if purposes != {"any"}:
            findings.append({"route": "/site.webmanifest", "code": "unexpected-icon-purpose", "detail": icon})
    browser.close()

summary = {
    "routesChecked": len(results),
    "manifestStatus": manifest_response.status,
    "manifestIcons": icons,
    "findingCount": len(findings),
    "findings": findings,
    "routes": results,
}
OUT.write_text(json.dumps(summary, indent=2))
print(json.dumps({key: summary[key] for key in ["routesChecked", "manifestStatus", "manifestIcons", "findingCount"]}, indent=2))
if findings:
    raise SystemExit(1)
