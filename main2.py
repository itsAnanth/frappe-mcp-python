import os
import json
import logging
from collections.abc import Sequence
from typing import Any
from Frappe.client import FrappeClient
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frappe-mcp-server")

# frappe client
frappe_client = FrappeClient(
    url="https://crm.axilume.com/",
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)
frappe_client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

# Tool schema
class FilterCondition(BaseModel):
    field: str = Field(..., description="The field to filter on, e.g., 'description'")
    operator: str = Field(..., description="The operator to use, e.g., 'like'")
    value: str = Field(..., description="The value to compare against, e.g., '%John Doe%'")

class ToolSchema(BaseModel):
    doctype: str = Field(..., description="The name of the DocType, e.g., 'ToDo'")
    filters: Optional[List[FilterCondition]] = Field(..., description="List of filter conditions")
    fields: Optional[List[str]] = Field(None, description="List of fields to retrieve")
    name: Optional[str] = Field(None, description="The name of the document to retrieved")

app = Server("frapper-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_document",
            description="Get a document from Frappe",
            inputSchema=ToolSchema.model_json_schema()
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if name != "get_document":
        raise ValueError(f"Unknown tool: {name}")

    try:
        arguments = ToolSchema.model_validate(arguments)
    except ValidationError as e:
        raise ValueError(f"Invalid code arguments: {e}") from e

    result = frappe_client.get_doc(
        arguments.doctype,
        name=arguments.name,
        filters=[[condition.field, condition.operator, condition.value] for condition in arguments.filters],
        fields=arguments.fields
    )
    logger.info(f"Execution: {result}")


    return [
        TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )
    ]

async def main():
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
        
if __name__ == "__main__":
    import anyio
    anyio.run(main)
    
    # dat = {
    # "doctype": "ToDo",
    # "filters": [
    #     {
    #     "field": "description",
    #     "value": "%John Doe%",
    #     "operator": "like"
    #     }
    # ]
    # }
    
    # result = frappe_client.get_doc(
    #     dat["doctype"],
    #     name="nn774086h5"
    #     # filters=[[condition["field"], condition["operator"], condition["value"]] for condition in dat["filters"]],
    # )
    # print(result)