import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

_SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "mcp_server.py")

weather_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[_SERVER_SCRIPT],
        ),
        timeout=10,
    ),
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="weather_agent",
    instruction=(
        "You are a helpful weather assistant. Use the get_weather and "
        "get_forecast tools to answer questions about current conditions "
        "and forecasts."
    ),
    tools=[weather_toolset],
)
