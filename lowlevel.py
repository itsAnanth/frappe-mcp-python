from typing import Any
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from Frappe.client import FrappeClient
from dotenv import load_dotenv
import os 
from tools.document_tools import DOCUMENT_TOOLS


import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

load_dotenv()

client = FrappeClient(
    url="https://crm.axilume.com/",
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

# client.authenticate()
client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

server = Server(
    name="frappe-mcp-server",
)

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name=tool["name"],
            description=tool["description"],
            input_schema=tool["inputSchema"],
        )
        
        for tool in DOCUMENT_TOOLS
    ]
    
@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "get_document":
        result = client.get_doc(arguments.get('doctype'), name=arguments.get('name'), filters=arguments.get('filters'), fields=arguments.get('fields'))
        print("DEBUG", result)
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Tool not found: {name}")


# @mcp.tool()
# def get_forecast(state: str) -> str:
#     """Get the weather forecast for a given state in India."""
#     return f"Weather forecast for {state} is very good!"


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


# if __name__ == "__main__":
#     import asyncio
#     import anyio

#     anyio.run(run)
