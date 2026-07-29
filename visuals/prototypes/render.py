from pathlib import Path
import base64,mimetypes,re,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).parent
page_name=sys.argv[1]
page_dir=root/page_name
html=(page_dir/'index.html').read_text()
shared=(root/'shared.css').read_text()
pagecss=(page_dir/f'{page_name}.css').read_text()
js=(root/'shared.js').read_text()
def inline_css_urls(css):
    def repl(m):
        raw=m.group(1).strip('"\'')
        if raw.startswith(('data:','http','#')): return m.group(0)
        p=(page_dir/raw).resolve()
        if not p.exists(): p=(root/raw).resolve()
        mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
        return 'url("data:%s;base64,%s")'%(mime,base64.b64encode(p.read_bytes()).decode())
    return re.sub(r'url\(([^)]+)\)',repl,css)
css=inline_css_urls(shared+'\n'+pagecss)
html=re.sub(r'<link rel="stylesheet" href="[^"]+">','',html)
html=html.replace('</head>',f'<style>{css}</style></head>')
for m in list(re.finditer(r'src="([^"]+)"',html)):
    raw=m.group(1)
    if raw.endswith('.js'): continue
    p=(page_dir/raw).resolve()
    if not p.exists(): p=(root/raw).resolve()
    mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    uri='data:%s;base64,%s'%(mime,base64.b64encode(p.read_bytes()).decode())
    html=html.replace(f'src="{raw}"',f'src="{uri}"')
html=re.sub(r'<script src="[^"]+"></script>',f'<script>{js}</script>',html)
out=root/'evidence';out.mkdir(exist_ok=True)
(out/f'{page_name}-inline.html').write_text(html)
viewports=[('desktop-1672x941',1672,941,False),('desktop-full',1672,941,True),('mobile-390x844',390,844,False),('mobile-full',390,844,True),('tablet-1024x1366',1024,1366,False)]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for suffix,w,h,full in viewports:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        pg.set_content(html,wait_until='load')
        pg.screenshot(path=str(out/f'{page_name}-{suffix}.png'),full_page=full)
        print(page_name,suffix,'scroll',pg.evaluate('document.documentElement.scrollWidth'),'client',pg.evaluate('document.documentElement.clientWidth'),'height',pg.evaluate('document.body.scrollHeight'))
        pg.close()
    b.close()
