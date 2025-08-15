# modules/http_probe.py
import hashlib
from urllib.parse import urljoin
from typing import Dict, Any, List

import requests


def _ensure_scheme(host_or_url: str) -> str:
    """Если схема не указана — подставляем http://"""
    if host_or_url.startswith(("http://", "https://")):
        return host_or_url
    return "http://" + host_or_url


def _summarize_cookies(resp: requests.Response) -> List[Dict[str, Any]]:
    out = []
    for c in resp.cookies:
        out.append({
            "name": c.name,
            "value": c.value,  # при желании можно маскировать
            "domain": c.domain,
            "path": c.path,
            "secure": bool(getattr(c, "secure", False)),
            "httponly": "httponly" in (resp.headers.get("Set-Cookie", "")).lower(),
            "samesite": None  # requests не даёт просто; можно разбирать Set-Cookie при желании
        })
    return out


def probe_http(target: str) -> Dict[str, Any]:
    """
    Делает запрос к целевому сайту, собирает:
    - status_code
    - headers (все)
    - key_headers: важные заголовки отдельно
    - cookies: краткая сводка куков
    - favicon_hash (SHA256 /favicon.ico)
    - final_url (после редиректов)
    Ошибки не роняют программу.
    """
    out: Dict[str, Any] = {
        "status_code": None,
        "final_url": None,
        "headers": {},
        "key_headers": {},
        "cookies": [],
        "favicon_hash": None
    }

    try:
        base = _ensure_scheme(target)

        # 1) Главная страница
        resp = requests.get(base, timeout=10, allow_redirects=True)
        out["status_code"] = resp.status_code
        out["final_url"] = resp.url
        out["headers"] = dict(resp.headers)

        # Важные заголовки (приводим к удобным ключам)
        h = {k.lower(): v for k, v in resp.headers.items()}
        out["key_headers"] = {
            "server": h.get("server"),
            "x_powered_by": h.get("x-powered-by"),
            "content_type": h.get("content-type"),
            "content_security_policy": h.get("content-security-policy"),
            "strict_transport_security": h.get("strict-transport-security"),
            "x_frame_options": h.get("x-frame-options"),
            "x_content_type_options": h.get("x-content-type-options"),
            "referrer_policy": h.get("referrer-policy"),
            "cache_control": h.get("cache-control"),
        }

        out["cookies"] = _summarize_cookies(resp)

        # 2) Favicon
        fav_url = urljoin(resp.url, "/favicon.ico")
        fav = requests.get(fav_url, timeout=10)
        if fav.ok and fav.content:
            out["favicon_hash"] = hashlib.sha256(fav.content).hexdigest()

    except Exception as e:
        out["error"] = str(e)

    return out
