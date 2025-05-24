import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from mcp_nws.main import app

client = TestClient(app)

# Simulate get_points returning None (NWS API failure or invalid lat/lon)
def test_nws_weather_points_none():
    with patch('mcp_nws.main.get_points', return_value=None):
        resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "error"
        assert "location" in data["message"].lower()

# Simulate get_forecast returning None (NWS API forecast failure)
def test_nws_weather_forecast_none():
    with patch('mcp_nws.main.get_points') as mock_points, \
         patch('mcp_nws.main.get_forecast', return_value=None):
        mock_points.return_value = {
            "properties": {"gridId": "BOX", "gridX": 70, "gridY": 76}
        }
        resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["forecast"] == {}

# Simulate get_current_weather returning None (NWS API current obs failure)
def test_nws_weather_current_none():
    with patch('mcp_nws.main.get_points') as mock_points, \
         patch('mcp_nws.main.get_forecast') as mock_forecast, \
         patch('mcp_nws.main.get_current_weather', return_value=None):
        mock_points.return_value = {
            "properties": {"gridId": "BOX", "gridX": 70, "gridY": 76}
        }
        mock_forecast.return_value = {"properties": {"periods": []}}
        resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["current"] == {}

# Simulate geocode_location returning None (location name not found)
def test_nws_weather_by_name_geocode_none():
    with patch('mcp_nws.main.geocode_location', return_value=None):
        resp = client.get("/resources/nws-weather-by-name?location=NotARealPlace,ZZ")
        assert resp.status_code == 200 or resp.status_code == 422
        if resp.status_code == 200:
            data = resp.json()
            assert data["status"] == "error"
            assert "location" in data["message"].lower()
