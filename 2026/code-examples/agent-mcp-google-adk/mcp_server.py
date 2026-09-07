from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-service")

_FAKE_WEATHER = {
    "san francisco": "62°F, foggy",
    "new york": "75°F, sunny",
    "london": "58°F, rainy",
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    return _FAKE_WEATHER.get(city.lower(), f"No weather data available for {city}.")


@mcp.tool()
def get_forecast(city: str, days: int = 3) -> str:
    """Return a short-range forecast summary for a city."""
    return f"{days}-day forecast for {city}: mild with a chance of showers."


if __name__ == "__main__":
    mcp.run(transport="stdio")
