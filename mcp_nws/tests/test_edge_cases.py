import pytest
from fastapi.testclient import TestClient
from mcp_nws.main import app

client = TestClient(app)

# Test: /resources/nws-weather with location not found (simulate ocean or invalid lat/lon)
def test_nws_weather_location_not_found():
    resp = client.get("/resources/nws-weather?lat=0.0&lon=0.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert "location" in data["message"].lower()

# Test: /resources/nws-weather-by-name with location not found
def test_nws_weather_by_name_location_not_found():
    resp = client.get("/resources/nws-weather-by-name?location=NotARealPlace,ZZ")
    assert resp.status_code == 200 or resp.status_code == 422
    if resp.status_code == 200:
        data = resp.json()
        assert data["status"] == "error"

# Test: /resources/nws-weather with valid but out-of-range date (e.g., far future)
def test_nws_weather_out_of_range_date():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06&date=2099-12-31")
    assert resp.status_code == 200
    data = resp.json()
    # Either error or empty forecast
    assert data["status"] in ("ok", "error")
    if data["status"] == "ok":
        assert data["forecast"] == [] or data["forecast"] == {}

# Test: /resources/nws-weather-by-name with invalid date format
def test_nws_weather_by_name_invalid_date():
    resp = client.get("/resources/nws-weather-by-name?location=Boston,MA&date=bad-date")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert "date" in data["message"].lower() or "invalid" in data["message"].lower()

# Additional: /resources/nws-weather-by-name with missing location param
def test_nws_weather_by_name_missing_param():
    resp = client.get("/resources/nws-weather-by-name")
    assert resp.status_code == 422 or resp.json().get("status") == "error"
