'use strict';
const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const errors=[];
const textExtensions=new Set(['.js','.html','.css','.json','.md']);
const FORMAL_IDENTITY_COMMIT='418e15ec95a53d67810397fa6c12e5f54822e137';
const FORMAL_SOURCE_SHA='76d40c46a1a9a1fde6b5a1bf7af506f4639bf29da86d0a3741416a5c2f8eeb1f';
const FORMAL_ASSET_SHA={
  'techgrity-horizontal-primary-1600.png':'69fc47babd46f4b6711c6264a33cbc9f2c84478325b28b4253a690b7889275cd',
  'techgrity-horizontal-reversed-1600.png':'da78093eaf7826709cd3c942d052b18813c3b294727a954014f3b2a858bbdb39',
  'techgrity-symbol-primary-512.png':'96b8b4900aa2e0b6c40ae82b70f49aa3a3f3a8535dafda7e34d5b75a49277ae9',
};
function digest(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')}
function walk(dir,files=[]){if(!fs.existsSync(dir))return files;for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);entry.isDirectory()?walk(file,files):files.push(file)}return files}
for(const dir of ['src','public']){
  for(const file of walk(path.join(root,dir))){
    if(!textExtensions.has(path.extname(file)))continue;
    const text=fs.readFileSync(file,'utf8');
    if(/\+263 78 330 4307|\+263783304307|2367 Lavenham Road/.test(text))errors.push(`${path.relative(root,file)} contains superseded contact data`);
  }
}
const syntheticLogo=path.join(root,'public','assets','techgrity-logo.svg');
if(fs.existsSync(syntheticLogo))errors.push('prohibited live-text Techgrity logo derivative still exists in public assets');
for(const obsolete of ['scripts/write-brand-assets.js','scripts/finalize-brand-assets.js'])if(fs.existsSync(path.join(root,obsolete)))errors.push(`obsolete synthetic brand pipeline still exists: ${obsolete}`);
const exactMaster=path.join(root,'public','assets','techgrity-primary-horizontal-approved.png');
if(digest(exactMaster)!==FORMAL_SOURCE_SHA)errors.push(`founder-approved exact logo source drift: ${digest(exactMaster)}`);
const syncScript=fs.readFileSync(path.join(root,'scripts','sync-techgrity-corporate-assets.py'),'utf8');
for(const authority of [FORMAL_IDENTITY_COMMIT,FORMAL_SOURCE_SHA,'Pillow==12.2.0'.replace('Pillow==','')])if(!syncScript.includes(authority))errors.push(`formal brand sync is missing authority pin: ${authority}`);
for(const hash of Object.values(FORMAL_ASSET_SHA))if(!syncScript.includes(hash))errors.push(`formal brand sync is missing derivative SHA-256 pin: ${hash}`);
for(const forbidden of ['Arial','Helvetica','<text','vector reconstruction']){
  if((forbidden==='vector reconstruction'&&!syncScript.includes('no redraw, tracing, vector reconstruction or re-typesetting'))||(forbidden!=='vector reconstruction'&&syncScript.includes(forbidden)))errors.push(`formal brand sync violates no-reconstruction boundary: ${forbidden}`);
}
const buildJs=fs.readFileSync(path.join(root,'scripts','build.js'),'utf8');
for(const forbidden of ['writeBrandBinaryAssets','finalizeBrandAssets','#071D49','#0D9488'])if(buildJs.includes(forbidden))errors.push(`build.js still contains synthetic brand logic: ${forbidden}`);
for(const required of ['techgrity-horizontal-primary-1600.png','techgrity-horizontal-reversed-1600.png','techgrity-symbol-primary-512.png'])if(!buildJs.includes(required))errors.push(`build.js is missing formal corporate derivative: ${required}`);
const pkg=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
if(pkg.engines?.node!=='24.x')errors.push(`Node engine is not pinned to 24.x: ${pkg.engines?.node}`);
if(!pkg.scripts?.build?.includes('techgrity-corporate-render-requirements.txt')||!pkg.scripts?.build?.includes('sync-techgrity-corporate-assets.py'))errors.push('build command does not regenerate and verify formal Techgrity corporate derivatives');
const rendererRequirement=fs.readFileSync(path.join(root,'scripts','techgrity-corporate-render-requirements.txt'),'utf8').trim();
if(rendererRequirement!=='Pillow==12.2.0')errors.push(`corporate renderer is not pinned to Pillow 12.2.0: ${rendererRequirement}`);
const siteJs=fs.readFileSync(path.join(root,'public','site.js'),'utf8');
if(!siteJs.includes('lockPageForMenu')||!siteJs.includes('unlockPageForMenu'))errors.push('site.js is missing scroll-preserving menu lock');
if(!siteJs.includes('const focusWithoutScroll =')||!siteJs.includes('node.focus({preventScroll: true})'))errors.push('site.js is missing scroll-safe navigation focus');
for(const transfer of [
  'focusWithoutScroll(menuReturnFocus || menuButton)',
  'focusWithoutScroll(focusablesIn(nav)[0])',
  "focusWithoutScroll(dropdown.querySelector('.mega-menu a, .mini-menu a'))",
  'focusWithoutScroll(last)',
  'focusWithoutScroll(first)',
]){
  if(!siteJs.includes(transfer))errors.push(`site.js is missing scroll-safe navigation transfer: ${transfer}`);
}
for(const headerGuard of [
  "const siteHeader = document.querySelector('.site-header')",
  'const pinMenuHeader =',
  'body.style.paddingTop = `${headerHeight}px`',
  "siteHeader.style.position = 'fixed'",
  'const restoreMenuHeader =',
  'siteHeader.style.position = menuHeaderStyles.position',
]){
  if(!siteJs.includes(headerGuard))errors.push(`site.js is missing responsive menu header preservation: ${headerGuard}`);
}
const polishCss=fs.readFileSync(path.join(root,'public','polish.css'),'utf8');
for(const matrixGuard of [
  '@media(min-width:721px) and (max-width:1100px)',
  '.matrix{grid-template-columns:minmax(0,1fr);gap:42px}',
  '.matrix-board{width:100%;max-width:100%}',
  '.matrix-layer,.matrix-layer>*{min-width:0}',
]){
  if(!polishCss.includes(matrixGuard))errors.push(`polish.css is missing tablet architecture overflow protection: ${matrixGuard}`);
}
for(const closeIconGuard of [
  '.site-header:not(.home-site-header) .menu-toggle[aria-expanded="true"] span:nth-child(1)',
  'transform:translateY(8px) rotate(45deg)',
  '.site-header:not(.home-site-header) .menu-toggle[aria-expanded="true"] span:nth-child(2)',
  'opacity:0',
  '.site-header:not(.home-site-header) .menu-toggle[aria-expanded="true"] span:nth-child(3)',
  'transform:translateY(-8px) rotate(-45deg)',
]){
  if(!polishCss.includes(closeIconGuard))errors.push(`polish.css is missing truthful legacy menu close state: ${closeIconGuard}`);
}
for(const visualPolishGuard of [
  '@media(min-width:1101px)',
  '.industry-detail.telecommunications .page-hero h1',
  'font-size:min(5vw,64px)',
  'overflow-wrap:normal',
  '.cta-panel .button{flex:0 0 auto;white-space:nowrap}',
  '.breadcrumbs>*{display:none!important}',
  '.breadcrumbs>a:first-child{display:inline-flex!important}',
  '.breadcrumbs>span:nth-last-child(2){display:inline-flex!important;align-items:center}',
  '.breadcrumbs>span:last-child',
  'overflow:visible!important',
]){
  if(!polishCss.includes(visualPolishGuard))errors.push(`polish.css is missing final visual polish protection: ${visualPolishGuard}`);
}
if(!siteJs.includes("control.removeAttribute('aria-describedby')"))errors.push('site.js is missing generated aria-describedby cleanup');
const forms=fs.readFileSync(path.join(root,'api','_forms.js'),'utf8');
if(forms.includes(' — '))errors.push('SMTP subject still contains an unencoded Unicode em dash');
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
  if(html.includes('Legal registration details, exact address, leadership, partners and certifications remain omitted until formally approved.'))errors.push(`${path.relative(root,file)} contains contradictory company-information copy`);
  if(/techgrity-logo\.svg|techgrity-logo-light\.svg|techgrity-mark\.svg/.test(html))errors.push(`${path.relative(root,file)} references prohibited synthetic Techgrity logo output`);
}
for(const [filename,expected] of Object.entries(FORMAL_ASSET_SHA)){
  const asset=path.join(root,'dist','assets',filename);
  if(!fs.existsSync(asset)){errors.push(`built formal corporate asset missing: ${filename}`);continue}
  const actual=digest(asset);if(actual!==expected)errors.push(`built formal corporate asset drift: ${filename} ${actual}`);
}
for(const stale of ['techgrity-logo.svg','techgrity-logo-light.svg','techgrity-mark.svg'])if(fs.existsSync(path.join(root,'dist','assets',stale)))errors.push(`built output contains prohibited synthetic logo asset: ${stale}`);
const builtManifest=JSON.parse(fs.readFileSync(path.join(root,'dist','site.webmanifest'),'utf8'));
if(builtManifest.icons?.[0]?.src!=='/assets/techgrity-symbol-primary-512.png')errors.push('built manifest does not use formal TG symbol');
const builtSiteJs=fs.readFileSync(path.join(root,'dist','site.js'),'utf8');
if(/\+263 78 330 4307|\+263783304307/.test(builtSiteJs))errors.push('built site.js contains superseded telephone data');
if(errors.length){console.error(errors.map(error=>`ERROR: ${error}`).join('\n'));process.exit(1)}
console.log(JSON.stringify({node:pkg.engines.node,assetCache:cache,formalIdentityCommit:FORMAL_IDENTITY_COMMIT,formalSourceSha256:FORMAL_SOURCE_SHA,formalAssetSha256:FORMAL_ASSET_SHA,syntheticCorporateLogoRemoved:true,sourceDrift:false,malformedImages:false,scrollSafeNavigationFocus:true,responsiveMenuHeaderPinned:true,legacyMenuCloseIcon:true,tabletArchitectureOverflowProtected:true,desktopIndustryWordIntegrity:true,ctaActionNoWrap:true,mobileBreadcrumbsConcise:true,companyInformationCopyConsistent:true},null,2));
