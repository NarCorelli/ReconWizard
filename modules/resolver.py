import socket
from typing import Dict, Any
import dns.resolver
from modules.utils import normalize_domain

def resolve_domain(target: str) -> Dict[str, Any]:
    domain = normalize_domain(target)
    out: Dict[str, Any] = {"domain": domain, "ip": None}
    try:
        out["ip"] = socket.gethostbyname(domain)
    except Exception as e:
        out["error"] = f"DNS resolve error: {e}"
    return out

def get_dns_records(target: str) -> Dict[str, Any]:
    domain = normalize_domain(target)
    res: Dict[str, Any] = {}
    for rtype in ["A", "AAAA", "MX", "NS", "TXT"]:
        try:
            answers = dns.resolver.resolve(domain, rtype, raise_on_no_answer=False)
            res[rtype] = [str(r) for r in answers]
        except Exception:
            res[rtype] = []
    return res
