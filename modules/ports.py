# modules/ports.py
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def _nmap_available() -> bool:
    return shutil.which("nmap") is not None

def scan_ports(target: str) -> Dict:
    """
    Быстрый скан портов через nmap.
    - Если nmap не установлен — не падаем, возвращаем понятное сообщение.
    - Если всё ок — вернём список открытых портов с сервисами.
    """
    if not _nmap_available():
        return {"error": "nmap не установлен. Поставь: macOS `brew install nmap`, Linux `sudo apt install nmap`."}

    # -F: быстрый пресет; -T4: быстрее; -oX: отчёт в XML
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        xml_path = tmp.name

    cmd = ["nmap", "-F", "-T4", "-oX", xml_path, target]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"open_ports": _parse_nmap_xml(xml_path)}
    except Exception as e:
        return {"error": f"nmap error: {e}"}

def _parse_nmap_xml(xml_path: str) -> List[Dict]:
    results: List[Dict] = []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for host in root.findall("host"):
            ports_el = host.find("ports")
            if ports_el is None:
                continue
            for port in ports_el.findall("port"):
                portid = port.get("portid")
                proto = port.get("protocol")
                state_el = port.find("state")
                state = state_el.get("state") if state_el is not None else None
                service_el = port.find("service")
                service = service_el.get("name") if service_el is not None else None
                product = service_el.get("product") if service_el is not None else None
                version = service_el.get("version") if service_el is not None else None

                if state == "open":
                    results.append({
                        "port": portid,
                        "protocol": proto,
                        "service": service,
                        "product": product,
                        "version": version,
                    })
    except Exception:
        # молча — вернём то, что смогли
        pass
    # сортируем по номеру порта
    try:
        results.sort(key=lambda x: int(x["port"]))
    except Exception:
        pass
    return results
