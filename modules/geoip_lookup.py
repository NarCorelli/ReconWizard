# modules/geoip_lookup.py
import requests

def get_geoip(ip_or_domain: str):
    """
    Определяет страну, город, провайдера и координаты по IP или домену.
    Использует публичный API ip-api.com (ограничение ~45 запросов в минуту).
    """
    try:
        url = f"http://ip-api.com/json/{ip_or_domain}?fields=status,message,country,regionName,city,isp,org,query,lat,lon"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        if data.get("status") != "success":
            return {"error": data.get("message", "Unknown error")}

        return {
            "ip": data.get("query"),
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "organization": data.get("org"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
        }
    except Exception as e:
        return {"error": str(e)}
