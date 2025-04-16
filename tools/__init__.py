import logging
from pathlib import Path
from collections.abc import Sequence
from typing import Any
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from mcp.server import (
    Server
)

from Frappe.client import FrappeClient
from pydantic import ValidationError


def register_tools(app: Server, frappe_client: FrappeClient) -> None:
    logger = logging.getLogger("frappe-mcp-server")
    logger.info("[TOOL MANAGER] Registering tools...")
    tools_map = {}
    root_dir = Path(__file__).parent
    for file in root_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue
        module_name = file.stem
        module = __import__(f"tools.{module_name}", fromlist=["*"])
        if hasattr(module, "exports"):
            tools_map[module.exports['tool_name']] = module.exports 
            logger.info(f'[TOOL MANAGER] {module.exports["tool_name"]} registered')

    logger.info(f"[TOOL MANAGER] Loaded {len(tools_map)} tools")
    
    @app.list_tools()
    async def list_tools() -> list[Tool]:
        logger.info("[TOOL MANAGER] Listing tools")
        """List available tools."""
        return [
            Tool(
                name=key,
                description=value['tool_description'],
                inputSchema=value['tool_schema'].model_json_schema()
            ) for key, value in tools_map.items()
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""
        if name not in tools_map.keys():
            raise ValueError(f"Unknown tool: {name}")

        tool = tools_map[name]
        try:
            arguments = tool['tool_schema'].model_validate(arguments)
        except ValidationError as e:
            raise ValueError(f"Invalid code arguments: {e}") from e

        result = tool['tool_function'](frappe_client, arguments.dict())
        logger.info(f"Execution: {result}")


        return result
    
    
__all__ = [
    "register_tools",
]