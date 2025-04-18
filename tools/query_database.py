from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field
from mcp.types import (
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from collections.abc import Sequence
from db.client import DBClient
import json
from datetime import datetime, date


class ToolSchema(BaseModel):
    query: str = Field(..., description="A single SQL query to execute\nMust be a read-only query\nMust be a valid SQL query\nMulti Statement queries are not supported\nExample: 'SELECT * FROM tabEmployee'") 


def query_database(db_client: DBClient, arguments) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    output = db_client.execute_query(arguments['query'], tabulate_output=False)
    
    
    def json_serial(obj):
        """JSON serializer for objects not serializable by default"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    return [
        TextContent(
            type="text",
            text=json.dumps(output.result, indent=2, default=json_serial)
        )
    ]

exports = {
    "requires": ["db_client"],
    "tool_name": "query_database",
    "tool_schema": ToolSchema,
    "tool_description": "Execute a single Read-Only SQL query on the database",
    "tool_function": query_database
}