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


async def register_tools(app: Server, requires) -> None:
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
            tool = module.exports['tool']
            
            tool_data = {
                'tool_description': tool.__doc__,
                'tool_schema': module.exports['tool_schema'],
                'tool_name': tool.__name__
            }
            
            tools_map[tool.__name__] = tool_data
            logger.info(f'[TOOL MANAGER] {tool_data["tool_name"]} registered')

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

        required = [requires[require] for require in tool['requires'] if require in requires.keys()]
        result = tool['tool_function'](*required, arguments.dict())


        return result
    
    
__all__ = [
    "register_tools",
]