from __future__ import annotations

from http.cookiejar import CookieJar
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

UPSTREAM = os.environ["AUDIT_UPSTREAM_URL"].rstrip("/")
SHARE_URL = os.environ["VERCEL_SHARE_URL"]
HOST = os.environ.get("AUDIT_PROXY_HOST", "127.0.0.1")
PORT = int(os.environ.get("AUDIT_PROXY_PORT", "4180"))

cookie_jar = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Follow the temporary share URL once so Vercel sets its authentication cookie.
with opener.open(SHARE_URL, timeout=30) as response:
    response.read(1)
if not list(cookie_jar):
    raise RuntimeError("Vercel share URL did not establish an authentication cookie")

HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
    "content-encoding",
}
FORWARDED_REQUEST_HEADERS = {
    "accept",
    "accept-language",
    "content-type",
    "origin",
    "referer",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "user-agent",
}


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("AUDIT_PROXY " + fmt % args + "\n")
        sys.stdout.flush()

    def _proxy(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        upstream_url = f"{UPSTREAM}{parsed.path or '/'}"
        if parsed.query:
            upstream_url += f"?{parsed.query}"

        body = None
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length:
            body = self.rfile.read(length)

        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() in FORWARDED_REQUEST_HEADERS
        }
        # Avoid compressed upstream payloads so the proxy can provide a correct
        # Content-Length without needing brotli/gzip dependencies.
        headers["Accept-Encoding"] = "identity"
        headers["X-Forwarded-Host"] = urllib.parse.urlsplit(UPSTREAM).netloc
        headers["X-Forwarded-Proto"] = "https"

        request = urllib.request.Request(
            upstream_url,
            data=body,
            headers=headers,
            method=self.command,
        )
        try:
            response = opener.open(request, timeout=45)
        except urllib.error.HTTPError as error:
            response = error
        except Exception as error:
            payload = f"Preview proxy upstream failure: {type(error).__name__}: {error}\n".encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
            return

        payload = response.read()
        self.send_response(response.status)
        for key, value in response.headers.items():
            if key.lower() in HOP_BY_HOP or key.lower() == "set-cookie":
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    do_GET = _proxy
    do_HEAD = _proxy
    do_POST = _proxy
    do_OPTIONS = _proxy


server = ThreadingHTTPServer((HOST, PORT), ProxyHandler)
print(f"AUDIT_PROXY_READY=http://{HOST}:{PORT} upstream={UPSTREAM}", flush=True)
try:
    server.serve_forever()
finally:
    server.server_close()
