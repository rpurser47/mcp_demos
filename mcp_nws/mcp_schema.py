from pydantic import BaseModel, Field
from typing import List, Dict, Any

class MCPResource(BaseModel):
    id: str
    name: str
    description: str
    parameters: Dict[str, str] = {
        "lat": "float",
        "lon": "float",
        "date": "str (optional, ISO date 'YYYY-MM-DD', 'today', 'tomorrow', or weekday name 'Monday'-'Sunday')"
    }
    examples: list = Field(default_factory=list, description="Example queries or payloads for this resource.")

class MCPResourceList(BaseModel):
    resources: List[MCPResource]
    examples: list = Field(default_factory=list, description="Example queries or payloads for the resources list.")

from pydantic import Field

class MCPWeatherResponse(BaseModel):
    location: str = Field(..., description="User-provided or resolved location name.")
    resolved_city: str = Field(..., description="Resolved city name for the coordinates.")
    resolved_state: str = Field(..., description="Resolved state abbreviation for the coordinates.")
    lat: float = Field(..., description="Latitude used for NWS query (degrees, WGS84, 4 decimal places).")
    lon: float = Field(..., description="Longitude used for NWS query (degrees, WGS84, 4 decimal places).")
    units: dict = Field(..., description="Units for weather fields, e.g., temperature (F), wind speed (mph), precipitation (%).")
    current: Dict[str, Any] = Field(..., description="Current weather observation from NWS.")
    forecast: Dict[str, Any] = Field(..., description="Full NWS forecast data.")
    status: str = Field("ok", description="Status of the response, e.g., 'ok' or 'error'.")
    message: str = Field("", description="Additional information or error message.")
