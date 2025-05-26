# MCP Server for National Weather Service

This project demonstrates a minimal Model Context Protocol (MCP) server that exposes the National Weather Service (NWS) API as a resource. It allows clients (including LLMs) to fetch current and forecast weather data via a standardized interface.

## Endpoints
- `/resources` — List available resources
- `/resources/{resource_id}` — Fetch weather data for a specified location

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the MCP server for the NWS weather resource:
   ```bash
   uvicorn mcp_nws.main:app --reload
   ```
3. Install Ollama with Llama 3.2
This uses [Ollama](https://ollama.com/) to run the Llama 3.2 model on your machine.
  - Follow the instructions for your platform at: https://ollama.com/download
  - Get the Llama 3.2 model:
    ```bash
    ollama pull llama3.2
    ```
  - Run Ollama:
    ```bash
    ollama serve # If it's not already running
    ollama run llama3.2
    ``` 
4. Run the App
    ```bash
    streamlit run app.py
    ```

## Usage

### What is a Model Context Protocol (MCP) Server?
A Model Context Protocol (MCP) server is an API that exposes external data or services in a standardized way, making it easier for AI models (like LLMs) and other clients to discover, query, and use those resources. MCPs are designed to provide structured access to real-world data, so that applications or intelligent agents can interact with them in a uniform manner.

This project demonstrates an MCP server that wraps the National Weather Service (NWS) API. It allows you (or an LLM) to:
- Discover available resources (what kinds of weather data are available)
- Query for current and forecast weather at a specific location

### Exposed Endpoints

#### 1. List Resources
- **Endpoint:** `GET /resources`
- **Description:** Returns a list of available resources. Each resource now includes an `examples` field with sample queries and descriptions for LLMs and users.

**Example curl:**
```bash
curl -X GET "http://localhost:8000/resources"
```

**Response:**
```json
{
  "resources": [
    {
      "id": "nws-weather",
      "name": "National Weather Service Weather",
      "description": "Get current and forecast weather for a given latitude and longitude.",
      "parameters": {
        "lat": "float",
        "lon": "float"
      },
      "examples": [
        {"query": "/resources/nws-weather?lat=42.36&lon=-71.06", "description": "Get weather for Boston, MA by coordinates."}
      ]
    },
    {
      "id": "nws-weather-by-name",
      "name": "National Weather Service Weather by Location Name",
      "description": "Get current and forecast weather for a given US location name (city, state, or zip).",
      "parameters": {
        "location": "str (US city, state, or zip)"
      },
      "examples": [
        {"query": "/resources/nws-weather-by-name?location=Boston,MA", "description": "Get weather for Boston, MA by name."}
      ]
    }
  ],
  "examples": [
    {"query": "/resources", "description": "List all available weather resources."}
  ]
}
```

#### 2. Get Weather Data
- **Endpoint:** `GET /resources/nws-weather?lat={LATITUDE}&lon={LONGITUDE}`
- **Description:** Returns current and forecast weather for the specified latitude and longitude.
- **Parameters:**
  - `lat`: Latitude of the location (e.g., 42.36)
  - `lon`: Longitude of the location (e.g., -71.06)
  - `date` (optional): ISO date (YYYY-MM-DD), 'today', 'tomorrow', or weekday name (e.g., 'Monday'). If provided, only forecast periods matching the date will be returned.

**Example curl:**
```bash
curl -X GET "http://localhost:8000/resources/nws-weather?lat=42.36&lon=-71.06"
```

**Example with date filtering:**
```bash
curl -X GET "http://localhost:8000/resources/nws-weather?lat=42.36&lon=-71.06&date=tomorrow"
```
**Response:**
A JSON object containing the location, resolved city/state, coordinates, units, current weather observation, forecast data, and status fields.

```json
{
  "location": "42.36,-71.06",
  "resolved_city": "Boston",
  "resolved_state": "MA",
  "lat": 42.36,
  "lon": -71.06,
  "units": {"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
  "current": {},
  "forecast": {
    "units": "us",
    "forecastGenerator": "BaselineForecastGenerator",
    "generatedAt": "2025-05-24T09:44:19+00:00",
    "updateTime": "2025-05-24T05:07:38+00:00",
    "validTimes": "2025-05-23T23:00:00+00:00/P8DT6H",
    "elevation": {
      "unitCode": "wmoUnit:m",
      "value": 3.9624
    },
    "periods": [
      {
        "number": 1,
        "name": "Overnight",
        "startTime": "2025-05-24T05:00:00-04:00",
        "endTime": "2025-05-24T06:00:00-04:00",
        "isDaytime": false,
        "temperature": 48,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": 3
        },
        "windSpeed": "6 mph",
        "windDirection": "W",
        "icon": "https://api.weather.gov/icons/land/night/bkn?size=medium",
        "shortForecast": "Mostly Cloudy",
        "detailedForecast": "Mostly cloudy, with a low around 48. West wind around 6 mph."
      },
      {
        "number": 2,
        "name": "Saturday",
        "startTime": "2025-05-24T06:00:00-04:00",
        "endTime": "2025-05-24T18:00:00-04:00",
        "isDaytime": true,
        "temperature": 62,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": 26
        },
        "windSpeed": "9 mph",
        "windDirection": "W",
        "icon": "https://api.weather.gov/icons/land/day/rain_showers,20/rain_showers,30?size=medium",
        "shortForecast": "Chance Rain Showers",
        "detailedForecast": "A chance of rain showers after 11am. Partly sunny, with a high near 62. West wind around 9 mph. Chance of precipitation is 30%."
      }
      // ... (additional periods omitted for brevity)
    ]
  }
}
```

#### 3. Get Weather Data by Location Name
- **Endpoint:** `GET /resources/nws-weather-by-name?location={LOCATION_NAME}`
- **Description:** Returns current and forecast weather for a given US location name (city, state, or zip). This endpoint geocodes the location name to latitude and longitude before querying the NWS.
- **Parameters:**
  - `location`: The US city, state, or zip code (e.g., `Boston, MA` or `90210`)
  - `date` (optional): ISO date (YYYY-MM-DD), 'today', 'tomorrow', or weekday name (e.g., 'Monday'). If provided, only forecast periods matching the date will be returned.

**Example curl:**
```bash
curl -X GET "http://localhost:8000/resources/nws-weather-by-name?location=Boston,MA"
```

**Example with date filtering:**
```bash
curl -X GET "http://localhost:8000/resources/nws-weather-by-name?location=Boston,MA&date=Friday"
```

**Example response:**
```json
{
  "location": "Boston,MA (42.3603,-71.0583)",
  "resolved_city": "Boston",
  "resolved_state": "MA",
  "lat": 42.3603,
  "lon": -71.0583,
  "units": {"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
  "current": { /* current weather observation */ },
  "forecast": {
    /* Only periods matching the requested date will be included if date is given */
    "periods": [
      {
        "number": 3,
        "name": "Friday",
        "startTime": "2025-05-30T06:00:00-04:00",
        "endTime": "2025-05-30T18:00:00-04:00",
        "isDaytime": true,
        "temperature": 72,
        "temperatureUnit": "F",
        "temperatureTrend": null,
        "windSpeed": "10 mph",
        "windDirection": "W",
        "icon": "...",
        "shortForecast": "Sunny",
        "detailedForecast": "Sunny, with a high near 72. West wind around 10 mph."
      }
      // ... (only matching periods)
    ]
  },
  "status": "ok",
  "message": ""
}
```

**Example error response:**
```json
{
  "location": "Boston,MA (0.0,0.0)",
  "resolved_city": "",
  "resolved_state": "",
  "lat": 0.0,
  "lon": 0.0,
  "units": {"temperature": "F", "wind_speed": "mph", "precipitation": "%", "distance": "mi"},
  "current": {},
  "forecast": {},
  "status": "error",
  "message": "Could not geocode location name."
}
```

### How can this MCP server be used?
- **By LLMs:** Language models can use tool/function-calling to query this server for up-to-date weather information and incorporate it into their responses.
- **By applications:** Any app can fetch weather data in a standardized way, abstracting away the complexity of the NWS API.

---

## Notes
- This is a learning/demo project for MCP and LLM integration.
- Uses FastAPI and the National Weather Service public API.
