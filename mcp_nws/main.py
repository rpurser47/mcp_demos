from fastapi import FastAPI, Query, HTTPException
from mcp_nws.mcp_schema import MCPResource, MCPResourceList, MCPWeatherResponse
from mcp_nws.nws_client import get_points, get_forecast, get_current_weather, geocode_location

app = FastAPI(title="MCP NWS Server")

@app.get("/resources", response_model=MCPResourceList)
def list_resources():
    resources = [
        MCPResource(
            id="nws-weather",
            name="National Weather Service Weather",
            description="Get current and forecast weather for a given latitude and longitude.",
            parameters={"lat": "float", "lon": "float"},
            examples=[
                {"query": "/resources/nws-weather?lat=42.36&lon=-71.06", "description": "Get weather for Boston, MA by coordinates."}
            ]
        ),
        MCPResource(
            id="nws-weather-by-name",
            name="National Weather Service Weather by Location Name",
            description="Get current and forecast weather for a given US location name (city, state, or zip).",
            parameters={"location": "str (US city, state, or zip)"},
            examples=[
                {"query": "/resources/nws-weather-by-name?location=Boston,MA", "description": "Get weather for Boston, MA by name."}
            ]
        )
    ]
    resource_examples = [
        {"query": "/resources", "description": "List all available weather resources."}
    ]
    return MCPResourceList(resources=resources, examples=resource_examples)

@app.get("/resources/nws-weather", response_model=MCPWeatherResponse)
async def get_weather_resource(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    date: str = Query(None, description="Optional. ISO date 'YYYY-MM-DD', 'today', 'tomorrow', or weekday name 'Monday'-'Sunday'")
):
    print(f"[DEBUG] [MCP] Received request: /resources/nws-weather?lat={lat}&lon={lon}&date={date}")
    print(f"[DEBUG] /resources/nws-weather called with lat={lat}, lon={lon}, date={date}")
    print("[DEBUG] Calling get_points...")
    points = await get_points(lat, lon)
    print(f"[DEBUG] get_points result: {points}")
    if not points:
        return MCPWeatherResponse(
            location=f"{lat},{lon}",
            resolved_city="",
            resolved_state="",
            lat=lat,
            lon=lon,
            units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
            current={},
            forecast={},
            status="error",
            message="Location not found in NWS API."
        )
    grid_id = points["properties"]["gridId"]
    grid_x = points["properties"]["gridX"]
    grid_y = points["properties"]["gridY"]
    forecast = await get_forecast(grid_id, grid_x, grid_y)
    current = await get_current_weather(lat, lon)
    forecast_data = forecast["properties"] if forecast else {}
    if date and forecast_data.get("periods"):
        from datetime import datetime, timedelta
        import calendar
        now = datetime.now()
        date_lower = date.lower()
        target = None
        date_parse_error = False
        if date_lower == "today":
            target = now.date()
        elif date_lower == "tomorrow":
            target = (now + timedelta(days=1)).date()
        elif date_lower in [d.lower() for d in calendar.day_name]:
            days_ahead = (list(calendar.day_name).index(date_lower.capitalize()) - now.weekday()) % 7
            target = (now + timedelta(days=days_ahead)).date()
        else:
            try:
                target = datetime.strptime(date, "%Y-%m-%d").date()
            except Exception:
                date_parse_error = True
        if date_parse_error or target is None:
            return MCPWeatherResponse(
                location=f"{lat},{lon}",
                resolved_city="",
                resolved_state="",
                lat=lat,
                lon=lon,
                units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
                current=current["properties"] if current else {},
                forecast={},
                status="error",
                message="Invalid date parameter. Use ISO date, 'today', 'tomorrow', or weekday name."
            )
        filtered = [p for p in forecast_data["periods"] if datetime.fromisoformat(p["startTime"]).date() == target]
        if not filtered:
            return MCPWeatherResponse(
                location=f"{lat},{lon}",
                resolved_city="",
                resolved_state="",
                lat=lat,
                lon=lon,
                units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
                current=current["properties"] if current else {},
                forecast={},
                status="error",
                message=f"No forecast available for date: {date}"
            )
        forecast_data = {**forecast_data, "periods": filtered}
    return MCPWeatherResponse(
        location=f"{lat},{lon}",
        resolved_city="",
        resolved_state="",
        lat=lat,
        lon=lon,
        units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
        current=current["properties"] if current else {},
        forecast=forecast_data,
        status="ok",
        message=""
    )

@app.get("/resources/nws-weather-by-name", response_model=MCPWeatherResponse)
async def get_weather_by_name(
    location: str = Query(..., description="US city, state, or zip"),
    date: str = Query(None, description="Optional. ISO date 'YYYY-MM-DD', 'today', 'tomorrow', or weekday name 'Monday'-'Sunday'")
):
    print(f"[DEBUG] [MCP] Received request: /resources/nws-weather-by-name?location={location}&date={date}")
    print(f"[DEBUG] /resources/nws-weather-by-name called with location={location}, date={date}")
    print("[DEBUG] Calling geocode_location...")
    geo = await geocode_location(location)
    print(f"[DEBUG] geocode_location result: {geo}")
    if not geo:
        return MCPWeatherResponse(
            location=location,
            resolved_city="",
            resolved_state="",
            lat=0.0,
            lon=0.0,
            units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
            current={},
            forecast={},
            status="error",
            message="Could not geocode location name."
        )
    lat, lon = geo["lat"], geo["lon"]
    city = geo.get("city", "")
    state = geo.get("state", "")
    # Round to 4 decimal places to avoid NWS redirect
    lat = round(lat, 4)
    lon = round(lon, 4)
    points = await get_points(lat, lon)
    if not points:
        return MCPWeatherResponse(
            location=f"{location} ({lat},{lon})",
            resolved_city=city,
            resolved_state=state,
            lat=lat,
            lon=lon,
            units={"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
            current={},
            forecast={},
            status="error",
            message="Location not found in NWS API."
        )
    grid_id = points["properties"]["gridId"]
    grid_x = points["properties"]["gridX"]
    grid_y = points["properties"]["gridY"]
    forecast = await get_forecast(grid_id, grid_x, grid_y)
    current = await get_current_weather(lat, lon)
    units = {
        "temperature": "F",
        "wind_speed": "mph",
        "precipitation": "%",
        "distance": "mi"
    }
    forecast_data = forecast["properties"] if forecast else {}
    if date and forecast_data.get("periods"):
        from datetime import datetime, timedelta
        import calendar
        now = datetime.now()
        date_lower = date.lower()
        target = None
        date_parse_error = False
        if date_lower == "today":
            target = now.date()
        elif date_lower == "tomorrow":
            target = (now + timedelta(days=1)).date()
        elif date_lower in [d.lower() for d in calendar.day_name]:
            days_ahead = (list(calendar.day_name).index(date_lower.capitalize()) - now.weekday()) % 7
            target = (now + timedelta(days=days_ahead)).date()
        else:
            try:
                target = datetime.strptime(date, "%Y-%m-%d").date()
            except Exception:
                date_parse_error = True
        if date_parse_error or target is None:
            return MCPWeatherResponse(
                location=f"{location} ({lat},{lon})",
                resolved_city=city,
                resolved_state=state,
                lat=lat,
                lon=lon,
                units=units,
                current=current["properties"] if current else {},
                forecast={},
                status="error",
                message="Invalid date parameter. Use ISO date, 'today', 'tomorrow', or weekday name."
            )
        filtered = [p for p in forecast_data["periods"] if datetime.fromisoformat(p["startTime"]).date() == target]
        if not filtered:
            return MCPWeatherResponse(
                location=f"{location} ({lat},{lon})",
                resolved_city=city,
                resolved_state=state,
                lat=lat,
                lon=lon,
                units=units,
                current=current["properties"] if current else {},
                forecast={},
                status="error",
                message=f"No forecast available for date: {date}"
            )
        forecast_data = {**forecast_data, "periods": filtered}
    return MCPWeatherResponse(
        location=f"{location} ({lat},{lon})",
        resolved_city=city,
        resolved_state=state,
        lat=lat,
        lon=lon,
        units=units,
        current=current["properties"] if current else {},
        forecast=forecast_data,
        status="ok",
        message=""
    )
