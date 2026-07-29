'use strict';
const {spawn} = require('child_process');
const assert = require('assert');
const port = 4183;
const child = spawn(process.execPath, ['server.js'], {env: {...process.env, PORT: String(port), FORM_DRY_RUN: '1'}, stdio: ['ignore', 'pipe', 'inherit']});
let settled = false;
const stop = () => { if (!settled) { settled = true; child.kill('SIGTERM'); } };
const wait = new Promise((resolve, reject) => {
  const timer = setTimeout(() => reject(new Error('server did not start')), 8000);
  child.stdout.on('data', (chunk) => { if (String(chunk).includes('Techgrity site:')) { clearTimeout(timer); resolve(); } });
  child.on('exit', (code) => { if (!settled && code) reject(new Error(`server exited ${code}`)); });
});
(async () => {
  try {
    await wait;
    const base = `http://127.0.0.1:${port}`;
    let response = await fetch(`${base}/healthz`); assert.equal(response.status, 200); assert.equal((await response.json()).ok, true);
    response = await fetch(`${base}/company/`); assert.equal(response.status, 200); assert.match(await response.text(), /One company connecting/);
    response = await fetch(`${base}/does-not-exist`); assert.equal(response.status, 404);
    const payload = {name:'Synthetic User',email:'test@example.com',category:'General business enquiry',message:'Controlled server integration test.',privacyConsent:'on',startedAt:String(Date.now()-5000)};
    response = await fetch(`${base}/api/contact`, {method:'POST',headers:{'Content-Type':'application/json','Sec-Fetch-Site':'same-origin'},body:JSON.stringify(payload)});
    assert.equal(response.status, 200); const result = await response.json(); assert.equal(result.ok, true); assert.ok(!result.redirect);
    response = await fetch(`${base}/api/contact`, {method:'POST',headers:{'Content-Type':'application/json','Sec-Fetch-Site':'cross-site'},body:JSON.stringify(payload)});
    assert.equal(response.status, 403);
    console.log('server integration tests passed');
  } finally { stop(); }
})().catch((error) => { console.error(error); stop(); process.exitCode = 1; });
