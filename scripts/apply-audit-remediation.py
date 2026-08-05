from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


# Remove superseded contact/address/logo data from source inputs rather than relying
# on the build normalizer to hide source drift.
text_extensions = {".js", ".html", ".css", ".json", ".md"}
source_roots = [ROOT / "src", ROOT / "public"]
source_replacements = {
    "+263 78 330 4307": "+263 77 182 5554",
    "+263783304307": "+263771825554",
    "2367 Lavenham Road": "2367 Lavenham Drive",
    "/assets/techgrity-primary-horizontal-approved.png": "/assets/techgrity-logo.svg",
}
for source_root in source_roots:
    for path in source_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in source_replacements.items():
            updated = updated.replace(old, new)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


# Responsive navigation: retain the actual document position while the page is
# locked, then restore it exactly when the overlay closes.
site_js = read("public/site.js")
site_js = replace_once(
    site_js,
    "  let menuReturnFocus = null;",
    """  let menuReturnFocus = null;
  let menuScrollY = 0;
  let menuLocked = false;

  const lockPageForMenu = () => {
    if (menuLocked) return;
    const body = document.body;
    menuScrollY = window.scrollY;
    const scrollbarGap = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    body.dataset.menuScrollY = String(menuScrollY);
    body.style.position = 'fixed';
    body.style.top = `-${menuScrollY}px`;
    body.style.left = '0';
    body.style.right = '0';
    body.style.width = '100%';
    if (scrollbarGap) body.style.paddingRight = `${scrollbarGap}px`;
    body.classList.add('menu-open');
    menuLocked = true;
  };

  const unlockPageForMenu = () => {
    const body = document.body;
    if (!menuLocked) {
      body.classList.remove('menu-open');
      return;
    }
    const restoreY = Number(body.dataset.menuScrollY || menuScrollY || 0);
    const root = document.documentElement;
    const previousScrollBehavior = root.style.scrollBehavior;
    body.classList.remove('menu-open');
    body.style.removeProperty('position');
    body.style.removeProperty('top');
    body.style.removeProperty('left');
    body.style.removeProperty('right');
    body.style.removeProperty('width');
    body.style.removeProperty('padding-right');
    delete body.dataset.menuScrollY;
    root.style.scrollBehavior = 'auto';
    window.scrollTo(0, restoreY);
    window.requestAnimationFrame(() => {
      root.style.scrollBehavior = previousScrollBehavior;
    });
    menuLocked = false;
  };""",
    "site.js menu state",
)
site_js = replace_once(
    site_js,
    "    document.body.classList.remove('menu-open');\n    closeDropdowns();",
    "    if (wasOpen) unlockPageForMenu();\n    else document.body.classList.remove('menu-open');\n    closeDropdowns();",
    "site.js close menu",
)
site_js = replace_once(
    site_js,
    "    document.body.classList.toggle('menu-open', open);",
    "    if (open) lockPageForMenu();\n    else unlockPageForMenu();",
    "site.js toggle menu lock",
)
site_js = replace_once(
    site_js,
    """  const clearFieldError = (field) => {
    field?.classList.remove('invalid');
    field?.querySelector('.field-error')?.remove();
    field?.querySelector('[aria-invalid="true"]')?.removeAttribute('aria-invalid');
  };""",
    """  const clearFieldError = (field) => {
    if (!field) return;
    const errorIds = Array.from(field.querySelectorAll('.field-error[id]'), (error) => error.id);
    field.querySelectorAll('[aria-describedby]').forEach((control) => {
      const tokens = String(control.getAttribute('aria-describedby') || '')
        .split(/\\s+/)
        .filter(Boolean)
        .filter((token) => !errorIds.includes(token));
      if (tokens.length) control.setAttribute('aria-describedby', tokens.join(' '));
      else control.removeAttribute('aria-describedby');
    });
    field.classList.remove('invalid');
    field.querySelectorAll('.field-error').forEach((error) => error.remove());
    field.querySelectorAll('[aria-invalid="true"]').forEach((control) => control.removeAttribute('aria-invalid'));
  };""",
    "site.js field cleanup",
)
write("public/site.js", site_js)


# Final CSS corrections are appended after all legacy/template rules so the
# responsive and accessibility contracts have one authoritative last word.
polish_path = ROOT / "public/polish.css"
polish = polish_path.read_text(encoding="utf-8")
marker = "/* === Final manual-audit remediation === */"
if marker in polish:
    raise RuntimeError("polish.css remediation marker already exists")
polish += r'''

/* === Final manual-audit remediation === */
:root{
  --slate-500:#596575;
}
.home-reference{
  --home-teal-dark:#007575;
  --home-muted:#596575;
}
.home-reference .home-site-header .primary-nav>a.active,
.home-reference .home-site-header .primary-nav>a:hover,
.home-reference .home-site-header .nav-dropdown>button:hover,
.home-reference .home-site-header .nav-dropdown>button[aria-expanded="true"],
.home-reference .home-pathway-copy em,
.home-reference .home-capabilities-intro>p{
  color:#007575!important;
}
.home-reference .section-heading>p,
.home-reference .contact-copy>.section-kicker,
.home-reference .contact-copy>p:nth-child(3),
.home-reference .contact-detail a,
.home-reference .contact-detail span,
.home-reference .form-note,
.form-field small,
.form-note{
  color:#596575!important;
}
.scope-label{color:#8a5b14!important}
.lifecycle li>span{color:#00686a!important}

/* Actual controls, not merely their surrounding cards, meet the 44px target. */
.breadcrumbs a{min-height:44px!important;padding-block:2px}
.card-link{min-height:44px!important;display:inline-flex!important;align-items:center;padding-block:10px}
.contact-detail a,
.contact-copy a[href^="mailto:"],
.contact-copy a[href^="tel:"]{min-height:44px;display:inline-flex;align-items:center;padding-block:10px}
.form-consent a{min-height:44px;display:inline-flex;align-items:center;padding-block:10px;margin-block:-10px}
@media(max-width:680px){
  main a[href^="#"]:not(.button){min-height:44px;display:flex;align-items:center;padding-block:8px}
}

/* The responsive overlay is viewport-bound, never header-bound. */
@media(max-width:1100px){
  .site-header,
  .home-reference .home-site-header{
    -webkit-backdrop-filter:none!important;
    backdrop-filter:none!important;
  }
  .home-reference .home-site-header .primary-nav{
    position:fixed!important;
    z-index:1002!important;
    top:76px!important;
    right:0!important;
    bottom:0!important;
    left:auto!important;
    width:min(430px,100vw)!important;
    height:auto!important;
    min-height:0!important;
    max-height:calc(100dvh - 76px)!important;
    padding:24px 28px 40px!important;
    overflow-x:hidden!important;
    overflow-y:auto!important;
    overscroll-behavior:contain;
    background:#fff!important;
    transform:translateX(105%)!important;
  }
  .home-reference .home-site-header .primary-nav.open{
    transform:translateX(0)!important;
  }
}
@media(max-width:720px){
  .home-reference .home-site-header .primary-nav{
    top:72px!important;
    max-height:calc(100dvh - 72px)!important;
    width:100vw!important;
  }
}
'''
polish_path.write_text(polish, encoding="utf-8")


# Correct malformed self-closing image output after the normalizer adds the
# inline footer asset style. The output remains valid HTML in every template.
build_js = read("scripts/build.js")
build_js = replace_once(
    build_js,
    " html=html.replace('<script src=\"/script.js\" defer></script>','<script src=\"/site.js\" defer></script>');\n return html;",
    " html=html.replace('<script src=\"/script.js\" defer></script>','<script src=\"/site.js\" defer></script>');\n html=html.replace(/<img([^>]*?)\\/\\s+style=/g,'<img$1 style=');\n return html;",
    "build.js final HTML cleanup",
)
write("scripts/build.js", build_js)


# SMTP headers must remain ASCII unless RFC 2047 encoding is applied.
forms_js = read("api/_forms.js")
subject_anchor = "subject: `${cfg.subject} — ${ref}`"
if forms_js.count(subject_anchor) != 1:
    raise RuntimeError(f"api/_forms.js subject anchor count: {forms_js.count(subject_anchor)}")
forms_js = forms_js.replace(subject_anchor, "subject: `${cfg.subject} - ${ref}`", 1)
write("api/_forms.js", forms_js)


# Stable asset names must revalidate after a deployment rather than remaining
# immutable in returning visitors' caches for one year.
vercel_path = ROOT / "vercel.json"
vercel = json.loads(vercel_path.read_text(encoding="utf-8"))
asset_rules = [rule for rule in vercel.get("headers", []) if rule.get("source") == "/assets/(.*)"]
if len(asset_rules) != 1:
    raise RuntimeError(f"Expected one asset cache rule, found {len(asset_rules)}")
asset_rules[0]["headers"] = [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]
vercel_path.write_text(json.dumps(vercel, indent=2) + "\n", encoding="utf-8")


# One Node major is authoritative for local development, CI and Vercel.
package_path = ROOT / "package.json"
package = json.loads(package_path.read_text(encoding="utf-8"))
package.setdefault("engines", {})["node"] = "20.x"
package["scripts"]["validate"] = "node scripts/validate.js && node scripts/validate-audit-remediation.js"
package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
write(".nvmrc", "20\n")
write(".node-version", "20\n")
for workflow in (ROOT / ".github/workflows").glob("*.yml"):
    text = workflow.read_text(encoding="utf-8")
    updated = re.sub(r"node-version:\s*(['\"]?)24(?:\.x)?\1", "node-version: '20'", text)
    if updated != text:
        workflow.write_text(updated, encoding="utf-8")


# Permanent regression guard for all defects corrected by this slice.
write(
    "scripts/validate-audit-remediation.js",
    r'''\'use strict\';
const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const errors=[];
const textExtensions=new Set(['.js','.html','.css','.json','.md']);
function walk(dir,files=[]){if(!fs.existsSync(dir))return files;for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);entry.isDirectory()?walk(file,files):files.push(file)}return files}
for(const dir of ['src','public']){
  for(const file of walk(path.join(root,dir))){
    if(!textExtensions.has(path.extname(file)))continue;
    const text=fs.readFileSync(file,'utf8');
    if(/\+263 78 330 4307|\+263783304307|2367 Lavenham Road|techgrity-primary-horizontal-approved\.png/.test(text))errors.push(`${path.relative(root,file)} contains superseded source data`);
  }
}
const siteJs=fs.readFileSync(path.join(root,'public','site.js'),'utf8');
if(!siteJs.includes('lockPageForMenu')||!siteJs.includes('unlockPageForMenu'))errors.push('site.js is missing scroll-preserving menu lock');
if(!siteJs.includes("control.removeAttribute('aria-describedby')"))errors.push('site.js is missing generated aria-describedby cleanup');
const forms=fs.readFileSync(path.join(root,'api','_forms.js'),'utf8');
if(forms.includes(' — '))errors.push('SMTP subject still contains an unencoded Unicode em dash');
const pkg=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
if(pkg.engines?.node!=='20.x')errors.push(`Node engine is not pinned to 20.x: ${pkg.engines?.node}`);
const vercel=JSON.parse(fs.readFileSync(path.join(root,'vercel.json'),'utf8'));
const assetRule=vercel.headers?.find(rule=>rule.source==='/assets/(.*)');
const cache=assetRule?.headers?.find(header=>header.key.toLowerCase()==='cache-control')?.value||'';
if(/immutable|max-age=31536000/.test(cache)||!cache.includes('must-revalidate'))errors.push(`Unsafe stable-asset cache policy: ${cache}`);
for(const file of walk(path.join(root,'dist')).filter(file=>file.endsWith('.html'))){
  const html=fs.readFileSync(file,'utf8');
  if(/<img[^>]*\/\s+style=/.test(html))errors.push(`${path.relative(root,file)} contains malformed self-closing image markup`);
}
const builtSiteJs=fs.readFileSync(path.join(root,'dist','site.js'),'utf8');
if(/\+263 78 330 4307|\+263783304307/.test(builtSiteJs))errors.push('built site.js contains superseded telephone data');
if(errors.length){console.error(errors.map(error=>`ERROR: ${error}`).join('\n'));process.exit(1)}
console.log(JSON.stringify({node:pkg.engines.node,assetCache:cache,sourceDrift:false,malformedImages:false},null,2));
'''.replace("\\'use strict\\';", "'use strict';"),
)

print("Applied F01-F10 audit remediation deterministically.")
