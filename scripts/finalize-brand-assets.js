'use strict';
const fs=require('fs');const path=require('path');
module.exports=function finalizeBrandAssets(targetDir){
  const primaryPath=path.join(targetDir,'techgrity-logo.svg');
  const primary=fs.readFileSync(primaryPath,'utf8');
  const light=primary.replaceAll('#071D49','#FFFFFF');
  fs.writeFileSync(path.join(targetDir,'techgrity-logo-light.svg'),light);
  const mark=primary
    .replace('viewBox="0 0 1500 320"','viewBox="0 0 430 320"')
    .replace('<title id="title">Techgrity Systems</title>','<title id="title">Techgrity Systems TG monogram</title>')
    .replace('<desc id="desc">Techgrity Systems wordmark with a navy and teal TG monogram.</desc>','<desc id="desc">Techgrity Systems TG monogram.</desc>')
    .replace(/\s*<rect x="466"[\s\S]*?\/>/,'')
    .replace(/\s*<text[\s\S]*?<\/text>/g,'');
  fs.writeFileSync(path.join(targetDir,'techgrity-mark.svg'),mark);
};
