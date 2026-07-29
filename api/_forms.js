'use strict';

const LIMIT_WINDOW_MS = 60_000;
const LIMIT_MAX = 8;
const buckets = new Map();

const configs = {
  contact: {
    required: ['name', 'email', 'category', 'message', 'privacyConsent'],
    max: {name: 100, email: 254, category: 100, message: 4000, organisation: 150, telephone: 40},
    subject: 'Website general enquiry',
    redirect: null,
  },
  project: {
    required: ['projectName', 'projectOrganisation', 'projectRole', 'projectEmail', 'projectTelephone', 'projectCountry', 'projectCategory', 'projectIndustry', 'projectLocation', 'projectDescription', 'expectedOutcomes', 'currentEnvironment', 'timescale', 'procurementStatus', 'privacyConsent'],
    max: {projectName: 100, projectOrganisation: 150, projectRole: 120, projectEmail: 254, projectTelephone: 40, projectCountry: 100, projectCategory: 120, projectIndustry: 120, projectLocation: 200, projectDescription: 8000, expectedOutcomes: 4000, currentEnvironment: 4000, timescale: 100, procurementStatus: 180},
    subject: 'Website project enquiry',
    redirect: '/project-enquiry-received/',
  },
  'document-request': {
    required: ['requestName', 'requestOrganisation', 'requestRole', 'requestEmail', 'requestCountry', 'document', 'reason', 'privacyConsent'],
    max: {requestName: 100, requestOrganisation: 150, requestRole: 120, requestEmail: 254, requestCountry: 100, document: 150, reason: 4000},
    subject: 'Website capability document request',
    redirect: '/document-request-received/',
  },
};

function response(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload));
}

function clean(value) {
  return String(value ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim();
}

function ipOf(req) {
  return String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
}

function rateLimit(ip) {
  const now = Date.now();
  const current = buckets.get(ip);
  if (!current || now - current.start > LIMIT_WINDOW_MS) {
    buckets.set(ip, {start: now, count: 1});
    return false;
  }
  current.count += 1;
  return current.count > LIMIT_MAX;
}

function reference(prefix) {
  return `TGS-${prefix}-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
}

async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let raw = '';
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 40_000) throw Object.assign(new Error('Request too large'), {status: 413});
  }
  try {
    return JSON.parse(raw || '{}');
  } catch {
    throw Object.assign(new Error('Invalid JSON'), {status: 400});
  }
}

function validate(type, input) {
  const cfg = configs[type];
  if (!cfg) return {error: 'Unsupported form'};
  if (clean(input.website)) return {silent: true};
  const data = {};
  for (const [key, value] of Object.entries(input)) data[key] = clean(value);
  const missing = cfg.required.filter((key) => !data[key] || data[key] === 'false');
  if (missing.length) return {error: 'Please review the required fields.', fields: missing};
  const emailKey = type === 'contact' ? 'email' : type === 'project' ? 'projectEmail' : 'requestEmail';
  if (!/^\S+@\S+\.\S+$/.test(data[emailKey])) return {error: 'Please provide a valid email address.', fields: [emailKey]};
  for (const [key, max] of Object.entries(cfg.max || {})) {
    if (data[key] && data[key].length > max) return {error: `${key} is too long.`, fields: [key]};
  }
  return {data, cfg};
}

function textBody(type, data, ref, req) {
  const lines = [
    `Reference: ${ref}`,
    `Form: ${type}`,
    `Received: ${new Date().toISOString()}`,
    `Source: ${req.headers.referer || 'not supplied'}`,
    '',
  ];
  for (const [key, value] of Object.entries(data)) {
    if (['website', 'privacyConsent', 'startedAt', 'formType'].includes(key)) continue;
    lines.push(`${key}: ${value}`);
  }
  return lines.join('\n');
}

function mailConfig() {
  const port = Number(process.env.SMTP_PORT || 465);
  return {
    host: process.env.SMTP_HOST,
    port,
    secure: String(process.env.SMTP_SECURE ?? (port === 465)).toLowerCase() === 'true',
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
    rejectUnauthorized: String(process.env.SMTP_REJECT_UNAUTHORIZED || 'true').toLowerCase() !== 'false',
  };
}

function smtpAddress(value) {
  const address = clean(value);
  if (!/^\S+@\S+\.\S+$/.test(address) || /[<>\r\n]/.test(address)) throw Object.assign(new Error('Invalid mail address'), {status: 503});
  return address;
}

function smtpMessage({from, to, replyTo, subject, text, ref}) {
  const headers = [
    `From: Techgrity Website <${from}>`,
    `To: ${to.join(', ')}`,
    `Reply-To: ${replyTo}`,
    `Subject: ${subject}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${ref.toLowerCase()}@techgrity.co.zw>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
  ];
  const safeText = String(text).replace(/\r?\n/g, '\r\n').replace(/^\./gm, '..');
  return `${headers.join('\r\n')}\r\n\r\n${safeText}\r\n.`;
}

async function smtpSend({from, to, replyTo, subject, text, ref}) {
  const tls = require('tls');
  const cfg = mailConfig();
  if (!cfg.secure) throw Object.assign(new Error('Only implicit TLS SMTP is supported.'), {status: 503});
  return new Promise((resolve, reject) => {
    const socket = tls.connect({host: cfg.host, port: cfg.port, servername: cfg.host, rejectUnauthorized: cfg.rejectUnauthorized});
    socket.setTimeout(20_000);
    let buffer = '';
    const waiters = [];
    const fail = (error) => { socket.destroy(); reject(Object.assign(error instanceof Error ? error : new Error(String(error)), {status: error?.status || 502})); };
    const processBuffer = () => {
      while (true) {
        const lines = buffer.split('\r\n');
        let end = -1;
        for (let i = 0; i < lines.length - 1; i += 1) {
          if (/^\d{3} /.test(lines[i])) { end = i; break; }
        }
        if (end < 0) return;
        const responseText = lines.slice(0, end + 1).join('\r\n');
        buffer = lines.slice(end + 1).join('\r\n');
        const waiter = waiters.shift();
        if (waiter) waiter(responseText);
      }
    };
    socket.on('data', (chunk) => { buffer += chunk.toString('utf8'); processBuffer(); });
    socket.on('error', fail);
    socket.on('timeout', () => fail(new Error('SMTP timeout')));
    const read = () => new Promise((res) => { waiters.push(res); processBuffer(); });
    const command = async (line, accepted) => {
      socket.write(`${line}\r\n`);
      const reply = await read();
      const code = Number(reply.slice(0, 3));
      if (!accepted.includes(code)) throw Object.assign(new Error(`SMTP command failed (${code})`), {status: 502});
      return reply;
    };
    (async () => {
      const greeting = await read();
      if (Number(greeting.slice(0, 3)) !== 220) throw new Error('SMTP greeting failed');
      await command('EHLO techgrity.co.zw', [250]);
      await command('AUTH LOGIN', [334]);
      await command(Buffer.from(cfg.user).toString('base64'), [334]);
      await command(Buffer.from(cfg.pass).toString('base64'), [235]);
      await command(`MAIL FROM:<${from}>`, [250]);
      for (const recipient of to) await command(`RCPT TO:<${recipient}>`, [250, 251]);
      await command('DATA', [354]);
      await command(smtpMessage({from, to, replyTo, subject, text, ref}), [250]);
      socket.write('QUIT\r\n');
      socket.end();
      resolve();
    })().catch(fail);
  });
}

async function sendEmail({type, data, cfg, ref, req}) {
  if (process.env.FORM_DRY_RUN === '1') return {dryRun: true};
  const mail = mailConfig();
  const recipients = String(process.env.ENQUIRY_TO_EMAIL || '').split(',').map((email) => email.trim()).filter(Boolean).map(smtpAddress);
  const from = smtpAddress(process.env.MAIL_FROM_EMAIL || mail.user || '');
  const replyTo = smtpAddress(data.email || data.projectEmail || data.requestEmail);
  if (!mail.host || !mail.user || !mail.pass || !recipients.length || !from) throw Object.assign(new Error('Enquiry delivery is not commissioned.'), {status: 503});
  await smtpSend({from, to: recipients, replyTo, subject: `${cfg.subject} — ${ref}`, text: textBody(type, data, ref, req), ref});
}

async function handle(req, res, type) {
  try {
    if (req.method !== 'POST') return response(res, 405, {ok: false, code: 'METHOD_NOT_ALLOWED', message: 'POST is required.'});
    if (String(req.headers['sec-fetch-site'] || '').toLowerCase() === 'cross-site') return response(res, 403, {ok: false, code: 'CROSS_SITE_REJECTED', message: 'The request could not be accepted.'});
    if (!String(req.headers['content-type'] || '').includes('application/json')) return response(res, 415, {ok: false, code: 'UNSUPPORTED_MEDIA_TYPE', message: 'JSON is required.'});
    if (rateLimit(ipOf(req))) return response(res, 429, {ok: false, code: 'RATE_LIMITED', message: 'Please wait before submitting again.'});
    const input = await readJson(req);
    const result = validate(type, input);
    if (result.silent) return response(res, 200, {ok: true, message: 'Your request has been received.'});
    if (result.error) return response(res, 400, {ok: false, code: 'VALIDATION_ERROR', message: result.error, fields: result.fields || []});
    const elapsed = Date.now() - Number(result.data.startedAt || 0);
    if (elapsed > 0 && elapsed < 1200) return response(res, 400, {ok: false, code: 'AUTOMATION_REJECTED', message: 'Please review and submit the form again.'});
    const ref = reference(type === 'project' ? 'PRJ' : type === 'contact' ? 'GEN' : 'DOC');
    await sendEmail({type, data: result.data, cfg: result.cfg, ref, req});
    const payload = {ok: true, reference: ref, message: 'Your request has been received.'};
    if (result.cfg.redirect) payload.redirect = result.cfg.redirect;
    return response(res, 200, payload);
  } catch (error) {
    return response(res, error.status || 500, {
      ok: false,
      code: error.status === 503 ? 'NOT_COMMISSIONED' : 'SUBMISSION_FAILED',
      message: error.status === 503 ? 'Secure enquiry delivery is not commissioned yet. Use the confirmed direct contact routes.' : 'The request could not be submitted safely.',
    });
  }
}

module.exports = {handle, validate, mailConfig};
