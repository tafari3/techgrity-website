'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
const errors=[],warnings=[];const manifest=JSON.parse(fs.readFileSync(path.join(dist,'route-manifest.json'),'utf8'));
const BRAND_AUTHORITY={repository:'tafari3/Techgrity-Brand-Identity-',commit:'418e15ec95a53d67810397fa6c12e5f54822e137',sourceSha256:'76d40c46a1a9a1fde6b5a1bf7af506f4639bf29da86d0a3741416a5c2f8eeb1f'};
const BRAND_ASSETS={
 'techgrity-horizontal-primary-1600.png':'69fc47babd46f4b6711c6264a33cbc9f2c84478325b28b4253a690b7889275cd',
 'techgrity-horizontal-reversed-1600.png':'da78093eaf7826709cd3c942d052b18813c3b294727a954014f3b2a858bbdb39',
 'techgrity-symbol-primary-512.png':'96b8b4900aa2e0b6c40ae82b70f49aa3a3f3a8535dafda7e34d5b75a49277ae9',
};
const PRIMARY='/assets/techgrity-horizontal-primary-1600.png',REVERSED='/assets/techgrity-horizontal-reversed-1600.png',SYMBOL='/assets/techgrity-symbol-primary-512.png';
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
 if(/2367 Lavenham Road|\+263 78 330 4307|tel:\+263783304307|techgrity-primary-horizontal-approved\.png|techgrity-logo\.svg|techgrity-logo-light\.svg|techgrity-mark\.svg/.test(html))errors.push(`${route}: contains superseded brand or contact data`);
 if(!html.includes(PRIMARY))errors.push(`${route}: missing founder-approved primary horizontal logo`);
 if(!html.includes(REVERSED))errors.push(`${route}: missing governed reversed footer logo`);
 if(!html.includes(SYMBOL))errors.push(`${route}: missing founder-approved TG symbol icon`);
 if(!html.includes('/polish.css'))errors.push(`${route}: missing final polish stylesheet`);
 if(/href="\/(digital-systems|infrastructure|technology-supply|delivery)\//.test(html))errors.push(`${route}: contains legacy route`);
 for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){const href=m[1];if(href.startsWith('mailto:')||href.startsWith('tel:')||href.startsWith('http')||href.startsWith('data:')||href==='#')continue;if(!localExists(href))errors.push(`${route}: broken local reference ${href}`)}
}
for(const route of ['/','/contact/']){const html=fs.readFileSync(routeToFile(route),'utf8');if(!html.includes('2367 Lavenham Drive'))errors.push(`${route}: verified head-office address missing`);if(!html.includes('+263 77 182 5554'))errors.push(`${route}: verified telephone missing`)}
const cssFiles=files.filter(f=>f.endsWith('.css'));for(const f of cssFiles){const css=fs.readFileSync(f,'utf8');let depth=0;for(const c of css){if(c==='{')depth++;if(c==='}')depth--;if(depth<0)break}if(depth!==0)errors.push(`${path.relative(dist,f)}: unbalanced braces (${depth})`);if(/var\(--[a-z0-9-]+\}/i.test(css))errors.push(`${path.relative(dist,f)}: malformed CSS var()`)}
const sitemap=fs.readFileSync(path.join(dist,'sitemap.xml'),'utf8');if((sitemap.match(/<url>/g)||[]).length!==31)errors.push('sitemap does not contain 31 URLs');
const assetHashes={};
for(const [filename,expected] of Object.entries(BRAND_ASSETS)){
 const asset=path.join(dist,'assets',filename);if(!fs.existsSync(asset)){errors.push(`missing founder-approved corporate asset: assets/${filename}`);continue}
 const digest=crypto.createHash('sha256').update(fs.readFileSync(asset)).digest('hex');assetHashes[`assets/${filename}`]=digest;if(digest!==expected)errors.push(`assets/${filename}: formal corporate derivative SHA-256 drift (${digest})`);
}
for(const stale of ['techgrity-logo.svg','techgrity-logo-light.svg','techgrity-mark.svg'])if(fs.existsSync(path.join(dist,'assets',stale)))errors.push(`superseded synthetic brand asset shipped: assets/${stale}`);
const sourceAsset=path.join(root,'public','assets','techgrity-primary-horizontal-approved.png');
const sourceDigest=crypto.createHash('sha256').update(fs.readFileSync(sourceAsset)).digest('hex');
if(sourceDigest!==BRAND_AUTHORITY.sourceSha256)errors.push(`founder-approved source master SHA-256 drift (${sourceDigest})`);
const provenance=JSON.parse(fs.readFileSync(path.join(dist,'assets','techgrity-corporate-provenance.json'),'utf8'));
if(provenance.identityRepository!==BRAND_AUTHORITY.repository||provenance.identityCommit!==BRAND_AUTHORITY.commit||provenance.approvedSourceSha256!==BRAND_AUTHORITY.sourceSha256)errors.push('corporate provenance does not match formal identity authority');
for(const [filename,expected] of Object.entries(BRAND_ASSETS))if(provenance.derivativeSha256?.[filename]!==expected)errors.push(`corporate provenance derivative pin drift: ${filename}`);
const webmanifest=JSON.parse(fs.readFileSync(path.join(dist,'site.webmanifest'),'utf8'));
if(webmanifest.icons?.length!==1||webmanifest.icons[0]?.src!==SYMBOL||webmanifest.icons[0]?.sizes!=='512x512'||webmanifest.icons[0]?.type!=='image/png')errors.push('web manifest does not use the founder-approved TG symbol');
if(errors.length){console.error(errors.map(x=>'ERROR: '+x).join('\n'));process.exit(1)}
console.log(JSON.stringify({publicRoutes:manifest.publicRoutes.length,systemRoutes:manifest.systemRoutes.length,htmlFiles:files.filter(f=>f.endsWith('.html')).length,uniqueTitles:titles.size,uniqueDescriptions:descs.size,brandAuthority:BRAND_AUTHORITY,brandAssetHashes:assetHashes,warnings},null,2));
