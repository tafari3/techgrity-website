'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),os=require('os');
const writeBrandBinaryAssets=require('./write-brand-assets');
const finalizeBrandAssets=require('./finalize-brand-assets');
const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
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
 if(/2367 Lavenham Road|\+263 78 330 4307|tel:\+263783304307|techgrity-primary-horizontal-approved\.png/.test(html))errors.push(`${route}: contains superseded brand or contact data`);
 if(!html.includes('/assets/techgrity-logo.svg'))errors.push(`${route}: missing transparent primary logo`);
 if(!html.includes('/assets/techgrity-mark.svg'))errors.push(`${route}: missing SVG favicon`);
 if(!html.includes('/polish.css'))errors.push(`${route}: missing final polish stylesheet`);
 if(/href="\/(digital-systems|infrastructure|technology-supply|delivery)\//.test(html))errors.push(`${route}: contains legacy route`);
 for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){const href=m[1];if(href.startsWith('mailto:')||href.startsWith('tel:')||href.startsWith('http')||href.startsWith('data:')||href==='#')continue;if(!localExists(href))errors.push(`${route}: broken local reference ${href}`)}
}
for(const route of ['/','/contact/']){const html=fs.readFileSync(routeToFile(route),'utf8');if(!html.includes('2367 Lavenham Drive'))errors.push(`${route}: verified head-office address missing`);if(!html.includes('+263 77 182 5554'))errors.push(`${route}: verified telephone missing`)}
const cssFiles=files.filter(f=>f.endsWith('.css'));for(const f of cssFiles){const css=fs.readFileSync(f,'utf8');let depth=0;for(const c of css){if(c==='{')depth++;if(c==='}')depth--;if(depth<0)break}if(depth!==0)errors.push(`${path.relative(dist,f)}: unbalanced braces (${depth})`);if(/var\(--[a-z0-9-]+\}/i.test(css))errors.push(`${path.relative(dist,f)}: malformed CSS var()`)}
const sitemap=fs.readFileSync(path.join(dist,'sitemap.xml'),'utf8');if((sitemap.match(/<url>/g)||[]).length!==31)errors.push('sitemap does not contain 31 URLs');
const primary=fs.readFileSync(path.join(dist,'assets','techgrity-logo.svg'),'utf8');
const light=fs.readFileSync(path.join(dist,'assets','techgrity-logo-light.svg'),'utf8');
const mark=fs.readFileSync(path.join(dist,'assets','techgrity-mark.svg'),'utf8');
if(!/<text[^>]*>TECHGRITY<\/text>/.test(primary)||!/<text[^>]*>SYSTEMS<\/text>/.test(primary))errors.push('primary logo does not contain the complete TECHGRITY SYSTEMS wordmark');
if(primary.includes('fill="#FFFFFF"')||primary.includes('fill="#fff"'))errors.push('primary logo contains an unintended white filled panel');
if(!light.includes('fill="#FFFFFF"')||!/<text[^>]*>SYSTEMS<\/text>/.test(light))errors.push('light footer logo is incomplete');
if(!mark.includes('viewBox="0 0 430 320"')||/<text[^>]*>TECHGRITY<\/text>/.test(mark))errors.push('favicon mark is not the isolated TG monogram');
const expectedDir=fs.mkdtempSync(path.join(os.tmpdir(),'techgrity-brand-'));
try{
 fs.copyFileSync(path.join(root,'public','assets','techgrity-logo.svg'),path.join(expectedDir,'techgrity-logo.svg'));
 writeBrandBinaryAssets(expectedDir);finalizeBrandAssets(expectedDir);
 const rels=['techgrity-logo.svg','techgrity-logo-light.svg','techgrity-mark.svg','favicon.ico','favicon-16x16.png','favicon-32x32.png','apple-touch-icon.png'];
 const assetHashes={};
 for(const rel of rels){const actual=path.join(dist,'assets',rel),expected=path.join(expectedDir,rel);if(!fs.existsSync(actual)){errors.push(`missing brand asset: assets/${rel}`);continue}const ah=crypto.createHash('sha256').update(fs.readFileSync(actual)).digest('hex');const eh=crypto.createHash('sha256').update(fs.readFileSync(expected)).digest('hex');assetHashes[`assets/${rel}`]=ah;if(ah!==eh)errors.push(`assets/${rel}: generated output differs from deterministic source`)}
 if(errors.length){console.error(errors.map(x=>'ERROR: '+x).join('\n'));process.exitCode=1}else console.log(JSON.stringify({publicRoutes:manifest.publicRoutes.length,systemRoutes:manifest.systemRoutes.length,htmlFiles:files.filter(f=>f.endsWith('.html')).length,uniqueTitles:titles.size,uniqueDescriptions:descs.size,brandAssetHashes:assetHashes,warnings},null,2));
}finally{fs.rmSync(expectedDir,{recursive:true,force:true})}
if(process.exitCode)process.exit(process.exitCode);
