import os
import re

def ensure_dir(path: str) -> None:
    """Создаёт директорию, если её нет."""
    os.makedirs(path, exist_ok=True)
    print(f"[+] Папка '{path}' готова.")

def normalize_domain(domain: str) -> str:
    """Очищает домен от протокола, пробелов, слэшей и путей."""
    if not isinstance(domain, str):
        return ""
    domain = domain.strip().lower()
    domain = re.sub(r'^https?://', '', domain)
    domain = domain.split('/')[0]
    return domain