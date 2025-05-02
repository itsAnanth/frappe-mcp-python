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
from main import db_client

class ToolSchema(BaseModel):
    query: str = Field(..., description="A single SQL query to execute\nMust be a read-only query\nMust be a valid SQL query\nMulti Statement queries are not supported\nExample: 'SELECT * FROM tabEmployee'") 


async def query_database(arguments: ToolSchema) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
        Execute a single Read-Only SQL query on the database
        Gives output in JSON format as an array of objects
        Each object is a row in the result set
        Each key in the object is a column name
        Each value in the object is the value of the column for that row
    """    

    output = db_client.execute_query(arguments.query, tabulate_output=False)
    
    
    return [
        TextContent(
            type="text",
            text=json.dumps(output.result, indent=2)
        )
    ]

exports = {
    "tool": query_database,
    "requires": ["db_client"],
    "tool_schema": ToolSchema,
}