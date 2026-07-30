'use strict';
const fs=require('fs');const path=require('path');
const root=path.resolve(__dirname,'..');const dist=path.join(root,'dist');
const {digitalCapabilities,infrastructureCapabilities,industries}=require('../src/content');
const T=require('../src/templates');
const writeBrandBinaryAssets=require('./write-brand-assets');
const PHONE_DISPLAY='+263 77 182 5554';
const PHONE_HREF='+263771825554';
const ADDRESS='2367 Lavenham Drive, Westgate, Harare, Zimbabwe';
const ADDRESS_LINES='2367 Lavenham Drive<br>Westgate, Harare<br>Zimbabwe';
const ICON_LINKS='<link rel="icon" href="/assets/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="/assets/techgrity-mark.svg"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png"><link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">';
function rm(p){fs.rmSync(p,{recursive:true,force:true})}
function copy(src,dst){fs.mkdirSync(dst,{recursive:true});for(const ent of fs.readdirSync(src,{withFileTypes:true})){const a=path.join(src,ent.name),b=path.join(dst,ent.name);ent.isDirectory()?copy(a,b):fs.copyFileSync(a,b)}}
function routeDir(route){return route==='/'?dist:path.join(dist,route.replace(/^\//,'').replace(/\/$/,''))}
function normaliseHtml(input){
 let html=input;
 html=html.replaceAll('href="/contact/">Discuss a Project','href="/discuss-a-project/">Discuss a Project');
 html=html.replaceAll('TECHGRITY SYSTEMS (PRIVATE) LIMITED','Techgrity Systems');
 html=html.replaceAll('2367 Lavenham Road, Westgate, Harare, Zimbabwe',ADDRESS);
 html=html.replaceAll('2367 Lavenham Road<br />Westgate, Harare<br />Zimbabwe',ADDRESS_LINES);
 html=html.replaceAll('2367 Lavenham Road<br>Westgate, Harare<br>Zimbabwe',ADDRESS_LINES);
 html=html.replaceAll('tel:+263783304307',`tel:${PHONE_HREF}`);
 html=html.replaceAll('+263 78 330 4307',PHONE_DISPLAY);
 html=html.replaceAll('/assets/techgrity-primary-horizontal-approved.png','/assets/techgrity-logo.svg');
 html=html.replace(/(<div class="footer-brand">\s*<img src=")\/assets\/techgrity-logo\.svg("[^>]*>)/g,'$1/assets/techgrity-logo-light.svg$2');
 html=html.replace(/<link rel="icon"[^>]*>/g,'');
 html=html.replace(/<link rel="apple-touch-icon"[^>]*>/g,'');
 html=html.replace('<link rel="manifest" href="/site.webmanifest">',`${ICON_LINKS}<link rel="manifest" href="/site.webmanifest">`);
 html=html.replace('<link rel="manifest" href="/site.webmanifest" />',`${ICON_LINKS}<link rel="manifest" href="/site.webmanifest" />`);
 if(!html.includes('/polish.css')){
   html=html.replace('</head>','<link rel="stylesheet" href="/polish.css"></head>');
 }
 html=html.replace('<b>Location</b><small>Harare, Zimbabwe</small>',`<b>Head office</b><small>${ADDRESS}</small>`);
 html=html.replace('<span>Harare, Zimbabwe</span><a href="/resources/">',`<span>${ADDRESS_LINES}</span><a href="/resources/">`);
 html=html.replace('<script src="/script.js" defer></script>','<script src="/site.js" defer></script>');
 return html;
}
function writeRoute(route,html){const dir=routeDir(route);fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'index.html'),normaliseHtml(html))}
rm(dist);copy(path.join(root,'public'),dist);writeBrandBinaryAssets(path.join(dist,'assets'));
let home=fs.readFileSync(path.join(root,'src/homepage.html'),'utf8');
home=home.replace('href="/contact/#documents">Capability statements','href="/resources/">Capability statements');
home=home.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/,`<script type="application/ld+json">${JSON.stringify({'@context':'https://schema.org','@type':'Organization',name:'Techgrity Systems',legalName:'TECHGRITY SYSTEMS (PRIVATE) LIMITED',url:'https://techgrity.co.zw/',logo:'https://techgrity.co.zw/assets/techgrity-logo.svg',email:'business@techgrity.co.zw',telephone:PHONE_DISPLAY,address:{'@type':'PostalAddress',streetAddress:'2367 Lavenham Drive',addressLocality:'Westgate, Harare',addressCountry:'ZW'},areaServed:['Zimbabwe','Africa'],description:'Techgrity Systems delivers digital systems, critical infrastructure and integrated technology solutions.'})}</script>`);
writeRoute('/',home);
const pages=[];
function add(route,html,indexable=true){writeRoute(route,html);pages.push({route,indexable})}
add('/capabilities/',T.capabilitiesOverview());
add('/capabilities/digital-systems/',T.capabilityLanding('digital'));
for(const item of digitalCapabilities)add(`/capabilities/digital-systems/${item.slug}/`,T.capabilityDetail(item,'digital'));
add('/capabilities/infrastructure/',T.capabilityLanding('infrastructure'));
for(const item of infrastructureCapabilities)add(`/capabilities/infrastructure/${item.slug}/`,T.capabilityDetail(item,'infrastructure'));
add('/capabilities/technology-supply/',T.technologySupply());
add('/industries/',T.industriesOverview());
for(const industry of industries)add(`/industries/${industry.slug}/`,T.industryDetail(industry));
add('/how-we-deliver/',T.howWeDeliver());
add('/company/',T.company());
add('/resources/',T.resources());
add('/contact/',T.contact());
add('/discuss-a-project/',T.discussProject());
add('/privacy/',T.legalPage('privacy'));
add('/terms/',T.legalPage('terms'));
add('/cookies/',T.legalPage('cookies'));
add('/404/',T.systemPage('404'),false);
add('/project-enquiry-received/',T.systemPage('project-enquiry-received'),false);
add('/document-request-received/',T.systemPage('document-request-received'),false);
add('/form-error/',T.systemPage('form-error'),false);
const siteJs=path.join(dist,'site.js');if(fs.existsSync(siteJs)){let js=fs.readFileSync(siteJs,'utf8');js=js.replaceAll('tel:+263783304307',`tel:${PHONE_HREF}`).replaceAll('+263 78 330 4307',PHONE_DISPLAY);fs.writeFileSync(siteJs,js)}
const publicRoutes=['/',...pages.filter(p=>p.indexable).map(p=>p.route)];
const sitemap=`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${publicRoutes.map(r=>`  <url><loc>https://techgrity.co.zw${r}</loc></url>`).join('\n')}\n</urlset>\n`;
fs.writeFileSync(path.join(dist,'sitemap.xml'),sitemap);
fs.writeFileSync(path.join(dist,'robots.txt'),'User-agent: *\nAllow: /\nSitemap: https://techgrity.co.zw/sitemap.xml\n');
fs.writeFileSync(path.join(dist,'route-manifest.json'),JSON.stringify({publicRoutes,systemRoutes:pages.filter(p=>!p.indexable).map(p=>p.route)},null,2));
console.log(`Built ${publicRoutes.length} public routes and ${pages.filter(p=>!p.indexable).length} system routes.`);
