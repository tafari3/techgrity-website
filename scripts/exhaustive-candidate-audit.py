from __future__ import annotations
import json, os, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE=os.environ.get('AUDIT_BASE_URL','http://127.0.0.1:4173').rstrip('/')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence'/'candidate-audit'; SHOTS=OUT/'screenshots'; SHOTS.mkdir(parents=True,exist_ok=True)
ROUTES=['/','/capabilities/','/capabilities/digital-systems/','/capabilities/digital-systems/software-ai-applications/','/capabilities/digital-systems/automation/','/capabilities/digital-systems/integration/','/capabilities/digital-systems/data-analytics/','/capabilities/digital-systems/cybersecurity-access/','/capabilities/infrastructure/','/capabilities/infrastructure/networks-fibre/','/capabilities/infrastructure/data-centres-cloud/','/capabilities/infrastructure/telecom-radio/','/capabilities/infrastructure/power-energy/','/capabilities/infrastructure/security-smart-facilities/','/capabilities/infrastructure/civil-technical-works/','/capabilities/technology-supply/','/industries/','/industries/government-public-sector/','/industries/education-research/','/industries/telecommunications/','/industries/energy-utilities-industrial/','/industries/data-centres-technology/','/industries/commerce-logistics-growing-organisations/','/how-we-deliver/','/company/','/resources/','/contact/','/discuss-a-project/','/privacy/','/terms/','/cookies/','/404/','/project-enquiry-received/','/document-request-received/','/form-error/']
VIEWPORTS=[(1672,941,'desktop-wide'),(1440,900,'desktop'),(1280,800,'desktop-compact'),(1024,900,'tablet-landscape'),(768,1024,'tablet-portrait'),(390,844,'mobile'),(320,568,'mobile-narrow')]
SHOT_ROUTES={'/','/capabilities/','/contact/','/resources/'}
results=[]; console=[]

def slug(route): return 'home' if route=='/' else re.sub(r'[^a-z0-9]+','-',route.strip('/').lower()).strip('-')

def goto(page,route):
    response=page.goto(BASE+route,wait_until='domcontentloaded',timeout=20000)
    try: page.wait_for_load_state('networkidle',timeout=3000)
    except PlaywrightTimeoutError: pass
    page.wait_for_timeout(80); return response

JS=r'''async () => {
 const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const max=Math.max(0,document.documentElement.scrollHeight-innerHeight);
 for(let y=0;y<=max;y+=Math.max(180,Math.floor(innerHeight*.42))){scrollTo(0,y);await sleep(35)} scrollTo(0,max);await sleep(100);
 const visible=el=>{const c=getComputedStyle(el),r=el.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>.01&&r.width>0&&r.height>0};
 const rgb=s=>{const m=String(s).match(/rgba?\((\d+)[, ]+(\d+)[, ]+(\d+)/);return m?[+m[1],+m[2],+m[3]]:null};
 const lum=a=>{const c=a.map(v=>v/255).map(v=>v<=.03928?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]};
 const ratio=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
 const contrast=[];
 for(const el of document.querySelectorAll('.section-dark .card h2,.section-dark .card h3,.section-dark .number-item b,.section-dark .number-item small,.section-dark .lifecycle strong,.section-dark .lifecycle small,.section-dark .check-list li')){
   if(!visible(el))continue; const fg=rgb(getComputedStyle(el).color); let n=el,bg=null;
   while(n&&!bg){const c=getComputedStyle(n);const x=rgb(c.backgroundColor);if(x&&c.backgroundColor!=='rgba(0, 0, 0, 0)'&&c.backgroundColor!=='transparent')bg=x;n=n.parentElement}
   if(fg&&bg&&ratio(fg,bg)<3)contrast.push({tag:el.tagName,cls:String(el.className||''),text:(el.innerText||'').trim().slice(0,90),ratio:+ratio(fg,bg).toFixed(2),color:getComputedStyle(el).color,background:bg});
 }
 const reveal=[...document.querySelectorAll('main .reveal')].filter(el=>{const c=getComputedStyle(el),t=(el.innerText||'').trim();return t.length>5&&(c.display==='none'||c.visibility==='hidden'||+c.opacity<.9||c.transform!=='none')}).map(el=>({cls:String(el.className||''),text:(el.innerText||'').replace(/\s+/g,' ').trim().slice(0,100),opacity:getComputedStyle(el).opacity,transform:getComputedStyle(el).transform}));
 const empty=[...document.querySelectorAll('.card,.number-item,.hero-board,.workspace-panel,.matrix-layer,.solution-point,.contact-detail')].filter(visible).filter(el=>{const c=getComputedStyle(el),r=el.getBoundingClientRect(),t=(el.innerText||'').trim();return r.width*r.height>9000&&t.length<2&&!el.querySelector('img,svg,video,canvas')&&c.backgroundImage==='none'}).map(el=>({tag:el.tagName,cls:String(el.className||''),w:Math.round(el.getBoundingClientRect().width),h:Math.round(el.getBoundingClientRect().height)}));
 const header=document.querySelector('.site-header'),hr=header?.getBoundingClientRect(),hc=header&&getComputedStyle(header);
 const result={scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,header:header?{position:hc.position,visible:hr.bottom>0,top:Math.round(hr.top),height:Math.round(hr.height)}:null,reveal,contrast,empty,broken:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),oldData:document.documentElement.innerHTML.match(/2367 Lavenham Road|\+263 78 330 4307|tel:\+263783304307|techgrity-primary-horizontal-approved\.png/g)||[],primaryLogo:document.querySelector('.brand img')?.getAttribute('src')||'',footerLogo:document.querySelector('.footer-brand img')?.getAttribute('src')||'',svgFavicon:!!document.querySelector('link[rel~="icon"][type="image/svg+xml"]'),icoFavicon:!!document.querySelector('link[rel~="icon"][href$="favicon.ico"]'),appleIcon:!!document.querySelector('link[rel="apple-touch-icon"]'),addressPresent:document.body.innerText.includes('2367 Lavenham Drive'),phonePresent:document.body.innerText.includes('+263 77 182 5554'),initialInvalid:document.querySelectorAll('[aria-invalid="true"],.field.invalid,.form-field.invalid').length};
 scrollTo(0,0);await sleep(40);return result;
}'''

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for w,h,label in VIEWPORTS:
        context=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
        for route in ROUTES:
            page=context.new_page(); findings=[]
            page.on('console',lambda msg,r=route,v=label: console.append({'route':r,'viewport':v,'type':msg.type,'text':msg.text}) if msg.type in {'error','warning'} else None)
            page.on('pageerror',lambda err,r=route,v=label: console.append({'route':r,'viewport':v,'type':'pageerror','text':str(err)}))
            try:
                response=goto(page,route); status=response.status; m=page.evaluate(JS)
                if status!=200: findings.append({'code':'status','detail':status})
                if m['scrollWidth']>m['clientWidth']+1: findings.append({'code':'overflow','detail':m['scrollWidth']-m['clientWidth']})
                if not m['header'] or m['header']['position'] not in {'sticky','fixed'} or not m['header']['visible']: findings.append({'code':'header-contract','detail':m['header']})
                for code in ['reveal','contrast','empty','broken','oldData']:
                    if m[code]: findings.append({'code':{'reveal':'hidden-reveal-content','contrast':'severe-contrast','empty':'empty-visual-container','broken':'broken-images','oldData':'superseded-brand-contact'}[code],'detail':m[code]})
                if m['primaryLogo']!='/assets/techgrity-logo.svg': findings.append({'code':'primary-logo','detail':m['primaryLogo']})
                if m['footerLogo']!='/assets/techgrity-logo-light.svg': findings.append({'code':'footer-logo','detail':m['footerLogo']})
                if not all([m['svgFavicon'],m['icoFavicon'],m['appleIcon']]): findings.append({'code':'favicon-pack','detail':{k:m[k] for k in ['svgFavicon','icoFavicon','appleIcon']}})
                if m['initialInvalid']: findings.append({'code':'initial-form-errors','detail':m['initialInvalid']})
                if route in {'/','/contact/'} and (not m['addressPresent'] or not m['phonePresent']): findings.append({'code':'verified-contact-facts','detail':{'address':m['addressPresent'],'phone':m['phonePresent']}})
                if route in SHOT_ROUTES and label in {'desktop','mobile'}: page.screenshot(path=str(SHOTS/f'{slug(route)}--{label}.png'),full_page=True)
                results.append({'route':route,'viewport':label,'status':status,'metrics':m,'findings':findings})
            except Exception as exc: results.append({'route':route,'viewport':label,'findings':[{'code':'exception','detail':f'{type(exc).__name__}: {exc}'}]})
            page.close()
        context.close()
    req=p.request.new_context(); unknown=req.get(BASE+'/definitely-not-a-real-route-20260730',fail_on_status_code=False).status; req.dispose(); browser.close()
findings=[{'route':x['route'],'viewport':x['viewport'],**f} for x in results for f in x['findings']]
if unknown!=404: findings.append({'route':'unknown','viewport':'request','code':'unknown-route-status','detail':unknown})
summary={'baseUrl':BASE,'generatedAtUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'cells':len(results),'routes':len(ROUTES),'viewports':len(VIEWPORTS),'findingCount':len(findings),'findingCodes':{},'consoleCount':len(console),'unknownRouteStatus':unknown}
for f in findings: summary['findingCodes'][f['code']]=summary['findingCodes'].get(f['code'],0)+1
(OUT/'summary.json').write_text(json.dumps(summary,indent=2));(OUT/'cells.json').write_text(json.dumps(results,indent=2));(OUT/'findings.json').write_text(json.dumps(findings,indent=2));(OUT/'console.json').write_text(json.dumps(console,indent=2))
print(json.dumps(summary,indent=2))
if findings or console: raise SystemExit(1)
