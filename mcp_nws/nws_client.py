import httpx
from typing import Optional, Dict, Any

NWS_API_BASE = "https://api.weather.gov"
NOMINATIM_API_BASE = "https://nominatim.openstreetmap.org/search"

async def geocode_location(location: str) -> Optional[Dict[str, float]]:
    """Geocode a location name to latitude and longitude using Nominatim."""
    params = {
        "q": location,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
        "countrycodes": "us"
    }
    headers = {"User-Agent": "mcp-nws-demo/1.0 (contact: example@example.com)"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(NOMINATIM_API_BASE, params=params, headers=headers)
        if resp.status_code == 200 and resp.json():
            data = resp.json()[0]
            address = data.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet") or address.get("municipality") or address.get("county") or ""
            state = address.get("state") or address.get("state_code") or ""
            return {"lat": float(data["lat"]), "lon": float(data["lon"]), "city": city, "state": state}
        return None

async def get_points(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    url = f"{NWS_API_BASE}/points/{lat},{lon}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return resp.json()
        return None

async def get_forecast(grid_id: str, grid_x: int, grid_y: int) -> Optional[Dict[str, Any]]:
    url = f"{NWS_API_BASE}/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return resp.json()
        return None

async def get_current_weather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    url = f"{NWS_API_BASE}/points/{lat},{lon}/observations/latest"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return resp.json()
        return None
