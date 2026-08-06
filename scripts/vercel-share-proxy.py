#!/usr/bin/env python3
"""Bounded local proxy for auditing a protected Vercel preview."""

from __future__ import annotations

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
# Rotated audit-only share credential. This file is removed before merge.
SHARE_URL = "https://techgrity-systems-live-iy0yc3v8f-tafarac3-7447s-projects.vercel.app/?_vercel_share=r93dabgbwLPSF6gAktPdvt4JSpef0j0a"
EXPECTED_RELEASE_SHA = os.environ.get("EXPECTED_RELEASE_SHA", "").strip()
HOST = os.environ.get("AUDIT_PROXY_HOST", "127.0.0.1")
PORT = int(os.environ.get("AUDIT_PROXY_PORT", "4180"))

STABLE_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 "
    "TechgrityPreviewCertification/1.0"
)
FORWARDED_HEADERS = {
    "accept",
    "accept-language",
    "content-type",
    "if-modified-since",
    "if-none-match",
    "range",
}
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
PROTECTION_MARKERS = (
    b"vercel security checkpoint",
    b"authentication required",
    b"log in to vercel",
    b"/_vercel/sso-api",
    b"x-vercel-protection-bypass",
)

Response = tuple[int, str, tuple[tuple[str, str], ...], bytes, str]


class ProtectedPreview:
    """Serialize one server-side protection session and refresh it once on loss."""

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.cookies = CookieJar()
        self.opener = self._new_opener()
        self.access_headers: dict[str, str] = {}
        self.access_query_token: str | None = None

    def _new_opener(self) -> urllib.request.OpenerDirector:
        return urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )

    def _reset(self) -> None:
        self.cookies = CookieJar()
        self.opener = self._new_opener()
        self.access_headers = {}
        self.access_query_token = None

    @staticmethod
    def _share_token() -> str:
        parsed = urllib.parse.urlsplit(SHARE_URL)
        token = urllib.parse.parse_qs(parsed.query).get("_vercel_share", [""])[0]
        if not token:
            raise RuntimeError("Vercel share URL did not contain an access token")
        return token

    @staticmethod
    def _with_share_query(url: str, token: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        query = [(key, value) for key, value in query if key != "_vercel_share"]
        query.append(("_vercel_share", token))
        return urllib.parse.urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                urllib.parse.urlencode(query),
                parsed.fragment,
            )
        )

    def _authorized_url(self, url: str) -> str:
        if self.access_query_token:
            return self._with_share_query(url, self.access_query_token)
        return url

    def _open(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
        timeout: int = 60,
    ) -> Response:
        merged = {
            "Accept-Encoding": "identity",
            "User-Agent": STABLE_USER_AGENT,
        }
        if headers:
            merged.update(headers)
        request = urllib.request.Request(
            url,
            data=body,
            headers=merged,
            method=method,
        )
        try:
            response = self.opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error
        try:
            payload = response.read()
            return (
                int(getattr(response, "status", response.getcode())),
                str(getattr(response, "reason", "")),
                tuple(response.headers.items()),
                payload,
                response.geturl(),
            )
        finally:
            response.close()

    @staticmethod
    def _header(headers: tuple[tuple[str, str], ...], name: str) -> str:
        wanted = name.lower()
        return next((value for key, value in headers if key.lower() == wanted), "")

    @staticmethod
    def _protected(
        status: int,
        payload: bytes,
        final_url: str,
    ) -> bool:
        if status in {401, 403}:
            return True
        parsed = urllib.parse.urlsplit(final_url)
        path = parsed.path.lower()
        if "/_vercel/sso-api" in path:
            return True
        if parsed.netloc.endswith("vercel.com") and path.startswith("/login"):
            return True
        sample = payload[:131072].lower()
        return any(marker in sample for marker in PROTECTION_MARKERS)

    def _diagnose(self, label: str, response: Response) -> None:
        status, _, headers, payload, final_url = response
        parsed = urllib.parse.urlsplit(final_url)
        content_type = self._header(headers, "Content-Type").split(";", 1)[0]
        print(
            f"AUDIT_PROXY_AUTH_DIAGNOSTIC label={label} status={status} "
            f"host={parsed.netloc or 'none'} path={parsed.path or '/'} "
            f"content_type={content_type or 'none'} "
            f"protected={self._protected(status, payload, final_url)} "
            f"cookies={len(list(self.cookies))}",
            flush=True,
        )

    def _release_commit(self, response: Response) -> str | None:
        status, _, headers, payload, final_url = response
        if self._protected(status, payload, final_url):
            return None
        if status != 200 or "json" not in self._header(
            headers, "Content-Type"
        ).lower():
            return None
        try:
            release = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(release, dict):
            return None
        observed = str(release.get("commit", ""))
        if EXPECTED_RELEASE_SHA and observed != EXPECTED_RELEASE_SHA:
            raise RuntimeError("authenticated preview release SHA mismatch")
        return observed

    def _release_response(
        self,
        headers: dict[str, str] | None = None,
        *,
        url: str | None = None,
    ) -> Response:
        return self._open(
            "GET",
            url or f"{UPSTREAM}/release.json",
            headers or {"Accept": "application/json"},
            timeout=45,
        )

    def _authenticate_locked(self) -> None:
        self._reset()
        token = self._share_token()
        encoded_token = urllib.parse.quote(token, safe="")
        release_url = f"{UPSTREAM}/release.json"

        # The generated share URL is designed to redirect and set access state.
        # Applying its query parameter directly to the exact resource avoids
        # relying on an intermediary root-page response.
        query_response = self._release_response(
            url=self._with_share_query(release_url, token)
        )
        observed = self._release_commit(query_response)
        access_mode = "share-query"

        if observed is not None:
            self.access_query_token = token
        else:
            bootstrap_headers = {"Accept": "text/html,application/xhtml+xml"}
            for bootstrap_url in (
                SHARE_URL,
                f"{UPSTREAM}/_vercel/sso-api?_vercel_share={encoded_token}",
                SHARE_URL,
            ):
                self._open("GET", bootstrap_url, bootstrap_headers, timeout=45)

            cookie_response = self._release_response()
            observed = self._release_commit(cookie_response)
            access_mode = "cookie"

            if observed is None:
                bypass_headers = {
                    "Accept": "application/json",
                    "x-vercel-protection-bypass": token,
                    "x-vercel-set-bypass-cookie": "samesitenone",
                }
                bypass_response = self._release_response(bypass_headers)
                observed = self._release_commit(bypass_response)
                access_mode = "bypass"

                if observed is None:
                    self._diagnose("share-query", query_response)
                    self._diagnose("cookie", cookie_response)
                    self._diagnose("bypass", bypass_response)
                    raise RuntimeError(
                        "Vercel protection remained active after bounded bootstrap"
                    )

                self.access_headers = {
                    "x-vercel-protection-bypass": token,
                    "x-vercel-set-bypass-cookie": "samesitenone",
                }

        print(
            f"AUDIT_PROXY_AUTHENTICATED release={observed or 'unknown'} "
            f"mode={access_mode} cookies={len(list(self.cookies))}",
            flush=True,
        )

    def authenticate(self) -> None:
        with self.lock:
            self._authenticate_locked()

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: bytes | None,
    ) -> Response:
        with self.lock:
            authorized_headers = dict(self.access_headers)
            authorized_headers.update(headers)
            response = self._open(
                method,
                self._authorized_url(url),
                authorized_headers,
                body,
            )
            if not self._protected(response[0], response[3], response[4]):
                return response

            safe_path = urllib.parse.urlsplit(url).path or "/"
            print(
                f"AUDIT_PROXY_REAUTHENTICATE status={response[0]} path={safe_path}",
                flush=True,
            )
            self._authenticate_locked()
            authorized_headers = dict(self.access_headers)
            authorized_headers.update(headers)
            retry = self._open(
                method,
                self._authorized_url(url),
                authorized_headers,
                body,
            )
            if self._protected(retry[0], retry[3], retry[4]):
                raise RuntimeError(
                    "Vercel protection remained active after one bounded refresh"
                )
            return retry


preview = ProtectedPreview()


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("AUDIT_PROXY " + fmt % args + "\n")
        sys.stdout.flush()

    def _fail(self, message: str) -> None:
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
        target = f"{UPSTREAM}{parsed.path or '/'}"
        if parsed.query:
            target += f"?{parsed.query}"

        length = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(length) if length else None
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() in FORWARDED_HEADERS
        }
        headers["Accept-Encoding"] = "identity"

        try:
            status, reason, response_headers, payload, _ = preview.request(
                self.command,
                target,
                headers,
                body,
            )
        except Exception as error:
            safe_path = parsed.path or "/"
            print(
                f"AUDIT_PROXY_FAILURE path={safe_path} "
                f"error={type(error).__name__}: {error}",
                flush=True,
            )
            self._fail(str(error))
            return

        self.send_response(status, reason)
        for key, value in response_headers:
            if key.lower() in HOP_BY_HOP or key.lower() == "set-cookie":
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    do_GET = _proxy
    do_HEAD = _proxy
    do_POST = _proxy
    do_OPTIONS = _proxy


def main() -> None:
    preview.authenticate()
    server = ThreadingHTTPServer((HOST, PORT), ProxyHandler)
    server.daemon_threads = True
    print(f"AUDIT_PROXY_READY=http://{HOST}:{PORT} upstream={UPSTREAM}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
