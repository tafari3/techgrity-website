from pathlib import Path
from urllib.parse import urlparse, unquote
import json, hashlib, mimetypes, re, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
EVIDENCE = ROOT / 'evidence' / 'runtime'
EVIDENCE.mkdir(parents=True, exist_ok=True)
manifest = json.loads((DIST / 'route-manifest.json').read_text())
BASE = 'https://techgrity.test'
results = []
FULL_PAGE_EVIDENCE = os.environ.get('FULL_PAGE_EVIDENCE') == '1'
shots = {
    '/': 'home-desktop.png',
    '/capabilities/': 'capabilities-desktop.png',
    '/capabilities/digital-systems/software-ai-applications/': 'digital-detail-desktop.png',
    '/capabilities/infrastructure/networks-fibre/': 'infra-detail-desktop.png',
    '/industries/government-public-sector/': 'industry-detail-desktop.png',
    '/company/': 'company-desktop.png',
    '/resources/': 'resources-desktop.png',
    '/contact/': 'contact-desktop.png',
    '/privacy/': 'privacy-desktop.png',
    '/terms/': 'terms-desktop.png',
    '/cookies/': 'cookies-desktop.png',
}
full_shots = {
    '/': 'home-full.png',
    '/capabilities/digital-systems/software-ai-applications/': 'digital-detail-full.png',
    '/capabilities/infrastructure/networks-fibre/': 'infra-detail-full.png',
    '/company/': 'company-full.png',
    '/contact/': 'contact-full.png',
    '/privacy/': 'privacy-full.png',
}

def route_file(route: str) -> Path:
    return DIST / 'index.html' if route == '/' else DIST / route.strip('/') / 'index.html'

def install_static_route(context):
    def handler(route):
        parsed = urlparse(route.request.url)
        pathname = unquote(parsed.path)
        file = DIST / pathname.lstrip('/')
        if pathname.endswith('/'):
            file = file / 'index.html'
        elif not file.suffix and (file / 'index.html').exists():
            file = file / 'index.html'
        status = 200
        if not file.exists() or file.is_dir():
            status = 404
            file = DIST / '404' / 'index.html'
        mime = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
        route.fulfill(status=status, body=file.read_bytes(), content_type=mime)
    context.route('https://techgrity.test/**', handler)

def inline_local_assets(html: str) -> str:
    def style_repl(match):
        href = match.group(1)
        file = DIST / href.lstrip('/')
        return f'<style data-source="{href}">{file.read_text()}</style>' if file.exists() else match.group(0)
    def script_repl(match):
        src = match.group(1)
        file = DIST / src.lstrip('/')
        return f'<script data-source="{src}">{file.read_text()}</script>' if file.exists() else match.group(0)
    html = re.sub(r'<link\s+rel="stylesheet"\s+href="(/[^"]+)"\s*/?>', style_repl, html)
    html = re.sub(r'<script\s+src="(/[^"]+)"(?:\s+defer)?\s*>\s*</script>', script_repl, html)
    return html

def set_page_content(page, route: str):
    html = inline_local_assets(route_file(route).read_text())
    html = html.replace('</head>', f'<base href="{BASE}/"></head>', 1)
    page.set_content(html, wait_until='load', timeout=10000)
    try:
        page.wait_for_function("[...document.images].every(i => i.complete)", timeout=5000)
    except Exception:
        pass
    page.wait_for_timeout(120)

with sync_playwright() as p:
    launch_args={'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
    chromium_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium')
    if Path(chromium_path).exists():
        launch_args['executable_path']=chromium_path
    browser = p.chromium.launch(**launch_args)
    context = browser.new_context(viewport={'width': 1672, 'height': 941}, device_scale_factor=1)
    install_static_route(context)
    for route in manifest['publicRoutes'] + manifest['systemRoutes']:
        page = context.new_page()
        errors = []
        page.on('console', lambda msg, e=errors: e.append(f'console:{msg.type}:{msg.text}') if msg.type == 'error' else None)
        page.on('pageerror', lambda err, e=errors: e.append(f'pageerror:{err}'))
        set_page_content(page, route)
        metrics = page.evaluate("""() => { const cta=document.querySelector('.nav-cta'); const cs=cta?getComputedStyle(cta):null; return {scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,h1:document.querySelectorAll('h1').length,images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),title:document.title,navCta:cta?{text:cta.textContent.trim(),backgroundImage:cs.backgroundImage,backgroundColor:cs.backgroundColor,color:cs.color}:null}; }""")
        status = 404 if route == '/404/' else 200
        cta_ok = not metrics['navCta'] or (metrics['navCta']['text'] and (metrics['navCta']['backgroundImage'] != 'none' or metrics['navCta']['backgroundColor'] not in ('rgba(0, 0, 0, 0)','transparent')))
        passed = status in (200, 404) and metrics['scrollWidth'] <= metrics['clientWidth'] and metrics['h1'] == 1 and not metrics['images'] and cta_ok and not errors
        results.append({'route': route, 'status': status, 'viewport': '1672x941', 'metrics': metrics, 'errors': errors, 'passed': passed})
        if route in shots or (FULL_PAGE_EVIDENCE and route in full_shots):
            page.evaluate("() => { const p=document.querySelector('[data-cookie-panel]'); if(p) p.hidden=true; }")
        if route in shots:
            page.screenshot(path=str(EVIDENCE / shots[route]), full_page=False)
        if FULL_PAGE_EVIDENCE and route in full_shots:
            page.screenshot(path=str(EVIDENCE / full_shots[route]), full_page=True)
        page.close()
    context.close()

    mcontext = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    install_static_route(mcontext)
    for route, name in [('/', 'home-mobile.png'), ('/contact/', 'contact-mobile.png'), ('/discuss-a-project/', 'project-mobile.png')]:
        page = mcontext.new_page()
        errors = []
        page.on('console', lambda msg, e=errors: e.append(f'console:{msg.type}:{msg.text}') if msg.type == 'error' else None)
        page.on('pageerror', lambda err, e=errors: e.append(f'pageerror:{err}'))
        set_page_content(page, route)
        menu = page.locator('.menu-toggle')
        menu.click()
        page.wait_for_timeout(300)
        menu_open = page.locator('.primary-nav').evaluate("e=>e.classList.contains('open')")
        metrics = page.evaluate("""() => ({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,h1:document.querySelectorAll('h1').length,navRect:(()=>{const n=document.querySelector('.primary-nav').getBoundingClientRect();return {left:n.left,right:n.right,width:n.width}})()})""")
        passed = menu_open and metrics['scrollWidth'] <= metrics['clientWidth'] and metrics['h1'] == 1 and metrics['navRect']['right'] <= metrics['clientWidth'] + 1 and metrics['navRect']['left'] >= -1 and not errors
        results.append({'route': route, 'status': 200, 'viewport': '390x844', 'metrics': metrics, 'menuOpen': menu_open, 'errors': errors, 'passed': passed})
        page.screenshot(path=str(EVIDENCE / name), full_page=False)
        menu.click()
        page.wait_for_timeout(300)
        page.close()

    page = mcontext.new_page()
    set_page_content(page, '/contact/')
    page.locator('form[data-form="contact"] button[type="submit"]').click()
    page.wait_for_timeout(100)
    invalid = page.locator('.field.invalid').count()
    results.append({'route': '/contact/', 'test': 'client validation', 'invalidFields': invalid, 'passed': invalid >= 1})
    page.close()

    page = mcontext.new_page()
    set_page_content(page, '/contact/')
    page.evaluate("document.querySelector('[data-cookie-manage]').click()")
    page.wait_for_timeout(30)
    visible_before = page.locator('[data-cookie-panel]').is_visible()
    page.evaluate("document.querySelector('[data-cookie-reject]').click()")
    page.wait_for_timeout(30)
    visible_after = page.locator('[data-cookie-panel]').is_visible()
    results.append({'route': '/contact/', 'test': 'cookie preference controls', 'visibleBeforeChoice': visible_before, 'visibleAfterChoice': visible_after, 'passed': visible_before and not visible_after})
    page.close()
    mcontext.close()
    browser.close()

(EVIDENCE / 'browser-qa.json').write_text(json.dumps(results, indent=2))
failures = [r for r in results if not r['passed']]
with (EVIDENCE / 'SHA256SUMS.txt').open('w') as out:
    for file in sorted(EVIDENCE.glob('*.png')):
        out.write(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.name}\n")
print(json.dumps({'checks': len(results), 'passed': len(results)-len(failures), 'failed': len(failures), 'failures': failures}, indent=2))
raise SystemExit(1 if failures else 0)
