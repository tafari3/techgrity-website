'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const {handle} = require('./api/_forms');

const root = path.resolve(__dirname, 'dist');
const port = Number(process.env.PORT || 4173);
const mime = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.webmanifest': 'application/manifest+json', '.ico': 'image/x-icon',
};
const apiRoutes = {'/api/contact': 'contact', '/api/project': 'project', '/api/document-request': 'document-request'};

function securityHeaders(res) {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.setHeader('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'");
}

function staticFile(pathname) {
  let file = path.join(root, pathname.replace(/^\//, ''));
  if (pathname.endsWith('/')) file = path.join(file, 'index.html');
  if (!path.extname(file) && fs.existsSync(path.join(file, 'index.html'))) file = path.join(file, 'index.html');
  return file;
}

const server = http.createServer(async (req, res) => {
  securityHeaders(res);
  const url = new URL(req.url, 'http://localhost');
  const pathname = decodeURIComponent(url.pathname);
  if (pathname === '/healthz') {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    return res.end(JSON.stringify({ok: true, service: 'techgrity-website'}));
  }
  if (apiRoutes[pathname]) return handle(req, res, apiRoutes[pathname]);
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.statusCode = 405;
    res.setHeader('Allow', 'GET, HEAD');
    return res.end('Method Not Allowed');
  }
  let file = staticFile(pathname);
  if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.statusCode = 404;
    file = path.join(root, '404', 'index.html');
  }
  const ext = path.extname(file);
  res.setHeader('Content-Type', mime[ext] || 'application/octet-stream');
  res.setHeader('Cache-Control', pathname.startsWith('/assets/') ? 'public, max-age=31536000, immutable' : 'public, max-age=0, must-revalidate');
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(file).on('error', () => { res.statusCode = 500; res.end('Internal Server Error'); }).pipe(res);
});

server.listen(port, '127.0.0.1', () => console.log(`Techgrity site: http://127.0.0.1:${port}`));
