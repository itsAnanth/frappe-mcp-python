from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from collections.abc import Sequence
import json
from db.client import DBClient


class ToolSchema(BaseModel):
    query: str = Field(..., description="SQL query to execute\nMust be a read-only query\nMust be a valid SQL query") 


def query_database(db_client: DBClient, arguments) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    output = db_client.execute_query(arguments['query'])
    
    return [
        TextContent(
            type="text",
            text=output.result
        )
    ]

exports = {
    "requires": ["db_client"],
    "tool_name": "query_database",
    "tool_schema": ToolSchema,
    "tool_description": "Execute a Read-Only SQL query on the database",
    "tool_function": query_database
}