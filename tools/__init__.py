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

from fastmcp import FastMCP
from Frappe.client import FrappeClient
from pydantic import ValidationError


def register_tools(app: FastMCP, requires) -> None:
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
                'tool': tool,
                'tool_description': tool.__doc__,
                'tool_schema': module.exports['tool_schema'],
                'tool_name': tool.__name__,
                'requires': module.exports['requires']
            }
            
            tools_map[tool.__name__] = tool_data
            
            app.tool()(tool)
            
            logger.info(f'[TOOL MANAGER] {tool_data["tool_name"]} registered')
            
            

    logger.info(f"[TOOL MANAGER] Loaded {len(tools_map)} tools")
    
    
    
__all__ = [
    "register_tools",
]