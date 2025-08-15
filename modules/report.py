# modules/report.py
from typing import Any, Dict, List, Optional
import json

def _h2(s: str) -> str:
    return f"\n## {s}\n\n"

def _code(obj: Any) -> str:
    return "```\n" + json.dumps(obj, indent=2, ensure_ascii=False) + "\n```\n"

def write_markdown(
    path: str,
    target: str,
    ip_info: Dict[str, Any],
    dns_info: Dict[str, Any],
    whois_info: Dict[str, Any],
    headers: Dict[str, Any],
    favhash: Dict[str, Any],
    ports: Optional[List[Dict]] = None,
) -> None:
    parts: List[str] = []
    parts.append(f"# ReconWizard Report — {target}\n")

    parts.append(_h2("Summary"))
    summary = {
        "target": target,
        "ip": ip_info.get("ip") if isinstance(ip_info, dict) else None,
        "dns_A_count": len(dns_info.get("A", [])) if isinstance(dns_info, dict) else None,
        "http_status": headers.get("status") if isinstance(headers, dict) else None,
        "ports_found": len(ports) if ports else 0,
    }
    parts.append(_code(summary))

    parts.append(_h2("IP / DNS"))
    parts.append(_code({"ip_info": ip_info, "dns_info": dns_info}))

    parts.append(_h2("WHOIS"))
    parts.append(_code(whois_info))

    parts.append(_h2("HTTP"))
    parts.append(_code({"headers": headers, "favicon": favhash}))

    if ports is not None:
        parts.append(_h2("Ports (nmap -F)"))
        parts.append(_code(ports))

    parts.append(_h2("Manual next steps"))
    parts.append("- Проверить интересные заголовки (Server, X-Powered-By, Cookies)\n")
    parts.append("- Запустить полное сканирование портов при необходимости\n")
    parts.append("- Выполнить технологический fingerprint (Wappalyzer)\n")
    parts.append("- Проверить уязвимости по версиям сервисов (CVE)\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
