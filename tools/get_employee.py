from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from collections.abc import Sequence
from Frappe.client import FrappeClient
import json
from main import frappe_client, db_client

class FilterCondition(BaseModel):
    field: str = Field(..., description="The field to filter on, e.g., 'description'")
    operator: str = Field(..., description="The operator to use, e.g., 'like'")
    value: str = Field(..., description="The value to compare against, e.g., '%John Doe%'")

class ToolSchema(BaseModel):
    name: str = Field(..., description="The name of the employee to retrieved")
    filters: Optional[List[FilterCondition]] = Field(None, description="List of optional filter conditions")
    fields: Optional[List[str]] = Field(None, description="List of optional fields to retrieve")

async def get_employee(arguments: ToolSchema) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """
        Get details of an employee from Frappe knowledge base
    """
    status, result = frappe_client.get_doc(
        doctype="Employee",
        filters=[
            ["employee_name", "like", f"%{arguments.name}%"],
            *(arguments.filters if arguments.filters else []),
        ],
    )
    
    context = None
    
    if status == False:
        context = "Some error occurred while fetching the document"
    elif len(result) == 0:
        context = f"No employee with name {arguments['name']} found"
    elif len(result) > 1:
        context = f"Multiple employees with name {arguments['name']} found"
    else:
        context = f"Employee with name {arguments['name']} found"
        
    return [
        TextContent(
            type="text",
            text=f"{context}\n\nData from frappe:\n\n{json.dumps(result, indent=2)}"
        )
    ]

exports = {
    "tool": get_employee,
    "requires": ["frappe_client"],
    "tool_schema": ToolSchema,
}