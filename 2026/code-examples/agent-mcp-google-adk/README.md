# Agent ↔ MCP Server with Google ADK

Minimal example showing a Google Agent Development Kit (ADK) agent acting as an
**MCP client**: it connects to a Model Context Protocol (MCP) server over
stdio, discovers the server's tools, and lets the LLM call them.

## How it fits together

```
User query
   │
   ▼
LlmAgent (Gemini)  ──uses──▶  MCPToolset (ADK's MCP client)
                                     │
                                     │ MCP protocol (stdio / SSE / HTTP)
                                     ▼
                              MCP Server (mcp_server.py)
                                 - get_weather
                                 - get_forecast
```

- `mcp_server.py` — a standalone MCP server (built with `FastMCP`) that
  exposes two tools: `get_weather` and `get_forecast`.
- `agent.py` — an ADK `LlmAgent` whose `tools` list includes an
  `MCPToolset`. The toolset spawns `mcp_server.py` as a subprocess, performs
  the MCP handshake, and converts the server's tool schemas into function
  declarations the Gemini model can call.
- `main.py` — runs the agent programmatically with `InMemoryRunner` and
  prints the conversation.

The agent never calls the MCP server's tools directly. It asks the model to
pick a tool; `MCPToolset` forwards that call to the MCP server over the
connection, gets the result back, and returns it to the model as a function
response.

## Setup

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your-gemini-api-key"   # or configure Vertex AI credentials
```

## Run

Programmatically:

```bash
python main.py
```

Or with the ADK CLI/dev UI (run from the parent of this directory, and note
that the ADK CLI uses the folder name as the agent name):

```bash
adk run agent-mcp-google-adk
adk web
```

## Connecting to a remote MCP server instead

Swap `StdioConnectionParams` for `SseConnectionParams` (or
`StreamableHTTPConnectionParams`) to talk to an MCP server exposed over
HTTP instead of spawning a local subprocess:

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

remote_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="https://example.com/mcp/sse",
        headers={"Authorization": f"Bearer {api_token}"},
    ),
)
```

Everything else — how the agent discovers and calls tools — stays the same;
only the transport changes.
