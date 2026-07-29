'use strict';
const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
const errors=[],warnings=[];const manifest=JSON.parse(fs.readFileSync(path.join(dist,'route-manifest.json'),'utf8'));
if(manifest.publicRoutes.length!==31)errors.push(`Expected 31 public routes, got ${manifest.publicRoutes.length}`);
if(manifest.systemRoutes.length!==4)errors.push(`Expected 4 system routes, got ${manifest.systemRoutes.length}`);
const titles=new Map(),descs=new Map();
const files=[];function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);e.isDirectory()?walk(p):files.push(p)}}walk(dist);
function routeToFile(route){return route==='/'?path.join(dist,'index.html'):path.join(dist,route.replace(/^\//,'').replace(/\/$/,''),'index.html')}
function localExists(href){const url=href.split('#')[0].split('?')[0];if(!url||!url.startsWith('/'))return true;if(url.startsWith('/api/'))return true;const direct=path.join(dist,url.replace(/^\//,''));return fs.existsSync(direct)&&fs.statSync(direct).isFile()||fs.existsSync(path.join(direct,'index.html'))}
for(const route of [...manifest.publicRoutes,...manifest.systemRoutes]){
 const file=routeToFile(route);if(!fs.existsSync(file)){errors.push(`Missing ${route}`);continue}const html=fs.readFileSync(file,'utf8');
 const h1=(html.match(/<h1\b/gi)||[]).length;if(h1!==1)errors.push(`${route}: expected 1 H1, got ${h1}`);
 const tm=html.match(/<title>([\s\S]*?)<\/title>/i);if(!tm)errors.push(`${route}: missing title`);else if(manifest.publicRoutes.includes(route)){const t=tm[1].trim();if(titles.has(t))errors.push(`${route}: duplicate title with ${titles.get(t)}`);titles.set(t,route)}
 const dm=html.match(/<meta name="description" content="([^"]*)"/i);if(!dm)errors.push(`${route}: missing description`);else if(manifest.publicRoutes.includes(route)){const d=dm[1].trim();if(descs.has(d))errors.push(`${route}: duplicate description with ${descs.get(d)}`);descs.set(d,route)}
 if(!html.includes('<link rel="canonical"'))errors.push(`${route}: missing canonical`);
 if(/TECHGRITY SYSTEMS \(PRIVATE\) LIMITED|2367 Lavenham|Westgate/i.test(html))errors.push(`${route}: contains unverified corporate detail`);
 if(/href="\/(digital-systems|infrastructure|technology-supply|delivery)\//.test(html))errors.push(`${route}: contains legacy route`);
 for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){const href=m[1];if(href.startsWith('mailto:')||href.startsWith('tel:')||href.startsWith('http')||href.startsWith('data:')||href==='#')continue;if(!localExists(href))errors.push(`${route}: broken local reference ${href}`)}
}
const cssFiles=files.filter(f=>f.endsWith('.css'));for(const f of cssFiles){const css=fs.readFileSync(f,'utf8');let depth=0;for(const c of css){if(c==='{')depth++;if(c==='}')depth--;if(depth<0)break}if(depth!==0)errors.push(`${path.relative(dist,f)}: unbalanced braces (${depth})`);if(/var\(--[a-z0-9-]+\}/i.test(css))errors.push(`${path.relative(dist,f)}: malformed CSS var()`)}
const sitemap=fs.readFileSync(path.join(dist,'sitemap.xml'),'utf8');if((sitemap.match(/<url>/g)||[]).length!==31)errors.push('sitemap does not contain 31 URLs');
const logo=path.join(dist,'assets','techgrity-primary-horizontal-approved.png');const crypto=require('crypto');const hash=crypto.createHash('sha256').update(fs.readFileSync(logo)).digest('hex');if(hash!=='76d40c46a1a9a1fde6b5a1bf7af506f4639bf29da86d0a3741416a5c2f8eeb1f')errors.push(`approved logo hash mismatch: ${hash}`);
if(errors.length){console.error(errors.map(x=>'ERROR: '+x).join('\n'));process.exit(1)}console.log(JSON.stringify({publicRoutes:manifest.publicRoutes.length,systemRoutes:manifest.systemRoutes.length,htmlFiles:files.filter(f=>f.endsWith('.html')).length,uniqueTitles:titles.size,uniqueDescriptions:descs.size,approvedLogoSha256:hash,warnings},null,2));
