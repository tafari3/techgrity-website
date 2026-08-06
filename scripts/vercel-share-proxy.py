#!/usr/bin/env python3
"""Bounded local proxy for auditing a protected Vercel preview.

The Vercel share credential and cookie remain server-side. Upstream requests use
one stable user agent because Vercel may bind protection cookies to request
identity. The shared cookie jar is serialized, and a protected response may
trigger one re-authentication attempt—never an unbounded retry loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from http.cookiejar import CookieJar
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

UPSTREAM = os.environ["AUDIT_UPSTREAM_URL"].rstrip("/")
SHARE_URL = os.environ["VERCEL_SHARE_URL"]
EXPECTED_RELEASE_SHA = os.environ.get("EXPECTED_RELEASE_SHA", "").strip()
HOST = os.environ.get("AUDIT_PROXY_HOST", "127.0.0.1")
PORT = int(os.environ.get("AUDIT_PROXY_PORT", "4180"))

UPSTREAM_ORIGIN = urllib.parse.urlsplit(UPSTREAM)
STABLE_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 "
    "TechgrityPreviewCertification/1.0"
)

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
    "if-modified-since",
    "if-none-match",
    "range",
}
PROTECTION_MARKERS = (
    b"vercel security checkpoint",
    b"authentication required",
    b"log in to vercel",
    b"/_vercel/sso-api",
    b"x-vercel-protection-bypass",
)


@dataclass(frozen=True)
class UpstreamResponse:
    status: int
    reason: str
    headers: tuple[tuple[str, str], ...]
    payload: bytes
    final_url: str

    def header(self, name: str) -> str:
        wanted = name.lower()
        for key, value in self.headers:
            if key.lower() == wanted:
                return value
        return ""


class PreviewSession:
    """Own and refresh the protected-preview cookie jar safely."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._cookie_jar = CookieJar()
        self._opener = self._build_opener(self._cookie_jar)

    @staticmethod
    def _build_opener(cookie_jar: CookieJar) -> urllib.request.OpenerDirector:
        return urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )

    @staticmethod
    def _request_headers(extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Accept-Encoding": "identity",
            "User-Agent": STABLE_USER_AGENT,
        }
        if extra:
            headers.update(extra)
        return headers

    def _open(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
        timeout: int = 60,
    ) -> UpstreamResponse:
        request = urllib.request.Request(
            url,
            data=body,
            headers=self._request_headers(headers),
            method=method,
        )
        try:
            response = self._opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error

        try:
            payload = response.read()
            response_headers = tuple(response.headers.items())
            status = int(getattr(response, "status", response.getcode()))
            reason = str(getattr(response, "reason", ""))
            final_url = response.geturl()
        finally:
            response.close()

        return UpstreamResponse(
            status=status,
            reason=reason,
            headers=response_headers,
            payload=payload,
            final_url=final_url,
        )

    @staticmethod
    def _looks_protected(response: UpstreamResponse) -> bool:
        if response.status in {401, 403}:
            return True

        parsed = urllib.parse.urlsplit(response.final_url)
        final_path = parsed.path.lower()
        if "/_vercel/sso-api" in final_path:
            return True
        if parsed.netloc.endswith("vercel.com") and final_path.startswith("/login"):
            return True

        sample = response.payload[:131072].lower()
        return any(marker in sample for marker in PROTECTION_MARKERS)

    @staticmethod
    def _release_payload(response: UpstreamResponse) -> dict[str, object]:
        content_type = response.header("Content-Type").lower()
        if response.status != 200 or "json" not in content_type:
            raise RuntimeError("release marker did not return JSON")
        try:
            payload = json.loads(response.payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError("release marker contained invalid JSON") from error
        if not isinstance(payload, dict):
            raise RuntimeError("release marker JSON was not an object")
        return payload

    def _authenticate_locked(self) -> None:
        self._cookie_jar = CookieJar()
        self._opener = self._build_opener(self._cookie_jar)

        share_response = self._open(
            "GET",
            SHARE_URL,
            headers={"Accept": "text/html,application/xhtml+xml"},
            timeout=45,
        )
        if share_response.status >= 400 or self._looks_protected(share_response):
            raise RuntimeError("Vercel share authentication did not open the preview")
        if not list(self._cookie_jar):
            raise RuntimeError("Vercel share authentication did not establish a cookie")

        release_response = self._open(
            "GET",
            f"{UPSTREAM}/release.json",
            headers={"Accept": "application/json"},
            timeout=45,
        )
        if self._looks_protected(release_response):
            raise RuntimeError("Vercel protection remained active after authentication")

        release = self._release_payload(release_response)
        observed_sha = str(release.get("commit", ""))
        if EXPECTED_RELEASE_SHA and observed_sha != EXPECTED_RELEASE_SHA:
            raise RuntimeError("authenticated preview release SHA mismatch")

        print(
            "AUDIT_PROXY_AUTHENTICATED "
            f"release={observed_sha or 'unknown'} cookies={len(list(self._cookie_jar))}",
            flush=True,
        )

    def authenticate(self) -> None:
        with self._lock:
            self._authenticate_locked()

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        body: bytes | None,
    ) -> UpstreamResponse:
        with self._lock:
            response = self._open(
                method,
                url,
                headers=headers,
                body=body,
            )
            if not self._looks_protected(response):
                return response

            safe_path = urllib.parse.urlsplit(url).path or "/"
            print(
                "AUDIT_PROXY_REAUTHENTICATE "
                f"status={response.status} path={safe_path}",
                flush=True,
            )
            self._authenticate_locked()
            retry = self._open(
                method,
                url,
                headers=headers,
                body=body,
            )
            if self._looks_protected(retry):
                raise RuntimeError(
                    "Vercel protection remained active after one bounded refresh"
                )
            return retry


preview_session = PreviewSession()


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("AUDIT_PROXY " + fmt % args + "\n")
        sys.stdout.flush()

    @staticmethod
    def _rewrite_request_header(name: str, value: str) -> str:
        if name.lower() == "origin":
            return f"{UPSTREAM_ORIGIN.scheme}://{UPSTREAM_ORIGIN.netloc}"
        if name.lower() == "referer":
            parsed = urllib.parse.urlsplit(value)
            suffix = urllib.parse.urlunsplit(("", "", parsed.path, parsed.query, ""))
            return f"{UPSTREAM}{suffix}"
        return value

    def _send_proxy_error(self, message: str) -> None:
        payload = f"Preview proxy failure: {message}\n".encode()
        self.send_response(502)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

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
            key: self._rewrite_request_header(key, value)
            for key, value in self.headers.items()
            if key.lower() in FORWARDED_REQUEST_HEADERS
        }
        headers["Accept-Encoding"] = "identity"

        try:
            response = preview_session.request(
                self.command,
                upstream_url,
                headers=headers,
                body=body,
            )
        except Exception as error:
            safe_path = parsed.path or "/"
            print(
                "AUDIT_PROXY_FAILURE "
                f"path={safe_path} error={type(error).__name__}: {error}",
                flush=True,
            )
            self._send_proxy_error(str(error))
            return

        self.send_response(response.status, response.reason)
        for key, value in response.headers:
            if key.lower() in HOP_BY_HOP or key.lower() == "set-cookie":
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(response.payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(response.payload)

    do_GET = _proxy
    do_HEAD = _proxy
    do_POST = _proxy
    do_OPTIONS = _proxy


def main() -> None:
    preview_session.authenticate()
    server = ThreadingHTTPServer((HOST, PORT), ProxyHandler)
    server.daemon_threads = True
    print(f"AUDIT_PROXY_READY=http://{HOST}:{PORT} upstream={UPSTREAM}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
