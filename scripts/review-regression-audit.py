from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("AUDIT_BASE_URL", "http://127.0.0.1:4173").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "candidate-audit" / "review-regressions.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

FORMAL_SYMBOL = "/assets/techgrity-symbol-primary-512.png"
FORMAL_SYMBOL_SHA256 = "96b8b4900aa2e0b6c40ae82b70f49aa3a3f3a8535dafda7e34d5b75a49277ae9"

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
            """() => {
              const visible = (el) => {
                const style = getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || 1) > 0.01 && rect.width > 0 && rect.height > 0;
              };
              return [...document.querySelectorAll('.footer-column')].filter(visible).map((column, columnIndex) => {
                const links = [...column.querySelectorAll('a[href]')].filter(visible).map((link, linkIndex) => {
                  const rect = link.getBoundingClientRect();
                  const style = getComputedStyle(link);
                  return {columnIndex, linkIndex, text:(link.textContent||'').trim(), display:style.display,
                    top:Math.round(rect.top), bottom:Math.round(rect.bottom), left:Math.round(rect.left), right:Math.round(rect.right),
                    width:Math.round(rect.width), height:Math.round(rect.height)};
                });
                return {columnIndex, links};
              });
            }"""
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
    if manifest_response.status != 200:
        findings.append({"route": "/site.webmanifest", "code": "manifest-status", "detail": manifest_response.status})
    if len(icons) != 1:
        findings.append({"route": "/site.webmanifest", "code": "manifest-icon-count", "detail": icons})
    for icon in icons:
        purposes = set(str(icon.get("purpose", "any")).split())
        if "maskable" in purposes:
            findings.append({"route": "/site.webmanifest", "code": "tight-mark-advertised-maskable", "detail": icon})
        if purposes != {"any"}:
            findings.append({"route": "/site.webmanifest", "code": "unexpected-icon-purpose", "detail": icon})
        if icon.get("src") != FORMAL_SYMBOL or icon.get("sizes") != "512x512" or icon.get("type") != "image/png":
            findings.append({"route": "/site.webmanifest", "code": "formal-symbol-manifest-contract", "detail": icon})

    symbol_response = context.request.get(f"{BASE}{FORMAL_SYMBOL}", fail_on_status_code=False)
    symbol_body = symbol_response.body()
    symbol_sha256 = hashlib.sha256(symbol_body).hexdigest()
    symbol_content_type = symbol_response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    symbol_evidence = {
        "path": FORMAL_SYMBOL,
        "status": symbol_response.status,
        "contentType": symbol_content_type,
        "bytes": len(symbol_body),
        "sha256": symbol_sha256,
        "expectedSha256": FORMAL_SYMBOL_SHA256,
    }
    if symbol_response.status != 200:
        findings.append({"route": FORMAL_SYMBOL, "code": "formal-symbol-status", "detail": symbol_evidence})
    if symbol_content_type != "image/png":
        findings.append({"route": FORMAL_SYMBOL, "code": "formal-symbol-content-type", "detail": symbol_evidence})
    if symbol_sha256 != FORMAL_SYMBOL_SHA256:
        findings.append({"route": FORMAL_SYMBOL, "code": "formal-symbol-sha256", "detail": symbol_evidence})
    browser.close()

summary = {
    "routesChecked": len(results),
    "manifestStatus": manifest_response.status,
    "manifestIcons": icons,
    "formalSymbol": symbol_evidence,
    "findingCount": len(findings),
    "findings": findings,
    "routes": results,
}
OUT.write_text(json.dumps(summary, indent=2))
print(json.dumps({key: summary[key] for key in ["routesChecked", "manifestStatus", "manifestIcons", "formalSymbol", "findingCount"]}, indent=2))
if findings:
    raise SystemExit(1)
