# modules/osint_profile.py
import requests
import re

def get_ssl_subdomains(domain):
    """Ищет поддомены через crt.sh"""
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {"error": "crt.sh request failed"}
        data = resp.json()
        subdomains = sorted(set(entry['name_value'] for entry in data))
        return {"subdomains": subdomains}
    except Exception as e:
        return {"error": str(e)}

def github_search(domain):
    """Ищет упоминания домена на GitHub"""
    try:
        url = f"https://api.github.com/search/code?q={domain}"
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {"error": f"GitHub API status {resp.status_code}"}
        result = resp.json()
        count = result.get("total_count", 0)
        return {"github_mentions": count}
    except Exception as e:
        return {"error": str(e)}

def hibp_warning(domain):
    """Выводит предупреждение о возможности утечек (без API-ключа)"""
    return {"hibp": f"Check {domain} on https://haveibeenpwned.com"}

def osint_profile(domain):
    """Собирает все OSINT-данные"""
    return {
        "ssl_subdomains": get_ssl_subdomains(domain),
        "github_search": github_search(domain),
        "hibp": hibp_warning(domain)
    }
