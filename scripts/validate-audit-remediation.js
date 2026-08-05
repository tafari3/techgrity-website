'use strict';
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
if(pkg.engines?.node!=='24.x')errors.push(`Node engine is not pinned to 24.x: ${pkg.engines?.node}`);
for(const versionFile of ['.nvmrc','.node-version']){
  const version=fs.readFileSync(path.join(root,versionFile),'utf8').trim();
  if(version!=='24')errors.push(`${versionFile} is not pinned to Node 24: ${version}`);
}
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
