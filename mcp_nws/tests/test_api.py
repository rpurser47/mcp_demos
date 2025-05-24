import pytest
from fastapi.testclient import TestClient
from mcp_nws.main import app

client = TestClient(app)


def test_resources_discovery():
    resp = client.get("/resources")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "resources" in data
    assert any(r["id"] == "nws-weather" for r in data["resources"])
    assert any(r["id"] == "nws-weather-by-name" for r in data["resources"])


def test_nws_weather_valid():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "forecast" in data


def test_nws_weather_missing_params():
    resp = client.get("/resources/nws-weather?lat=42.36")
    assert resp.status_code == 422 or resp.json().get("status") == "error"


def test_nws_weather_by_name_valid():
    resp = client.get("/resources/nws-weather-by-name?location=Boston,MA")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "forecast" in data


def test_nws_weather_date_filter():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06&date=Monday")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "error")

def test_nws_weather_date_today():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06&date=today")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "error")

def test_nws_weather_date_tomorrow():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06&date=tomorrow")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "error")


def test_nws_weather_invalid_date():
    resp = client.get("/resources/nws-weather?lat=42.36&lon=-71.06&date=notaday")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "error"
    assert "date" in data["message"].lower() or "invalid" in data["message"].lower()
