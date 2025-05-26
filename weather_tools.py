def get_weather(location: str = None, lat: float = None, lon: float = None, date: str = None):
    """Call the MCP server to get weather data by name or coordinates."""
    import requests
    print(f"[DEBUG][Tool] get_weather called with location={location}, lat={lat}, lon={lon}, date={date}")
    if location:
        params = {"location": location}
        if date:
            params["date"] = date
        url = "http://localhost:8000/resources/nws-weather-by-name"
    elif lat is not None and lon is not None:
        params = {"lat": lat, "lon": lon}
        if date:
            params["date"] = date
        url = "http://localhost:8000/resources/nws-weather"
    else:
        return {"status": "error", "message": "Must provide location name or lat/lon."}
    try:
        resp = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG][Tool] MCP server response: {resp.text}")
        return resp.json()
    except Exception as e:
        print(f"[ERROR][Tool] MCP call failed: {e}")
        return {"status": "error", "message": str(e)}
