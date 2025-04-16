from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="frappe-mcp-server",
)

@mcp.tool()
def get_forecast(state: str) -> str:
    """Get the weather forecast for a given state in India."""
    return f"Weather forecast for {state} is very good!"


if __name__ == "__main__":
    print("Hello from frappe-mcp-python!")
    mcp.run(transport='stdio')
