# modules/whois_lookup.py
from typing import Dict, Any, List, Optional
from datetime import datetime

# Пакет: pip install python-whois
try:
    import whois as whois_lib
except Exception:
    whois_lib = None


def _to_list(v) -> List[str]:
    if v is None:
        return []
    if isinstance(v, (list, tuple, set)):
        return [str(x) for x in v if x is not None]
    return [str(v)]


def _to_iso(dt) -> Optional[str]:
    """Приводим дату к ISO-строке. python-whois может отдавать list/None/str/datetime."""
    if dt is None:
        return None
    if isinstance(dt, (list, tuple)):
        # берём самую раннюю (обычно creation_date так и приходит списком)
        dt = min([x for x in dt if isinstance(x, datetime)], default=dt[0])
    if isinstance(dt, datetime):
        return dt.isoformat()
    try:
        # иногда приходит строка — возвращаем как есть
        return str(dt)
    except Exception:
        return None


def get_whois(domain_or_ip: str) -> Dict[str, Any]:
    """
    Возвращает ключевые поля WHOIS в нормализованном виде.
    Никогда не падает: ошибки кладём в {"error": "..."}.
    """
    if whois_lib is None:
        return {"error": "python-whois не установлен. Установи: pip install python-whois"}

    try:
        info = whois_lib.whois(domain_or_ip)

        name_servers = sorted([ns.lower() for ns in _to_list(getattr(info, "name_servers", []))])
        emails = sorted({e.lower() for e in _to_list(getattr(info, "emails", []))})

        out: Dict[str, Any] = {
            "domain": str(getattr(info, "domain_name", None)),
            "registrar": getattr(info, "registrar", None),
            "status": _to_list(getattr(info, "status", None)),
            "creation_date": _to_iso(getattr(info, "creation_date", None)),
            "updated_date": _to_iso(getattr(info, "updated_date", None)),
            "expiration_date": _to_iso(getattr(info, "expiration_date", None)),
            "name_servers": name_servers,
            "emails": list(emails),
        }
        return out
    except Exception as e:
        return {"error": str(e)}
