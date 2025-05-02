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
from main import db_client, frappe_client

class FilterCondition(BaseModel):
    field: str = Field(..., description="The field to filter on, e.g., 'description'")
    operator: str = Field(..., description="The operator to use, e.g., 'like'")
    value: str = Field(..., description="The value to compare against, e.g., '%John Doe%'")

class ToolSchema(BaseModel):
    doctype: str = Field(..., description="The name of the DocType, e.g., 'ToDo'")
    filters: Optional[List[FilterCondition]] = Field(None, description="List of optional filter conditions")
    fields: Optional[List[str]] = Field(None, description="List of optional fields to retrieve")
    name: Optional[str] = Field(None, description="The optional name of the document to retrieved")

async def get_document(arguments: ToolSchema) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
        Get a document from Frappe knowledge base
    """
    status, result = frappe_client.get_doc(**arguments.dict())
    
    return [
        TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )
    ]

exports = {
    "tool": get_document,
    "requires": ["frappe_client"],
    "tool_schema": ToolSchema,

}