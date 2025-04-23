## Installation

### Clone and Install Dependencies

`git clone https://github.com/itsAnanth/frappe-mcp-python`

`cd frappe-mcp-python`

`uv sync`

### Add Config file to Claude

`%appdata%/claude/claude_desktop_config.json`

```
{
  "mcpServers": {
    "frappe-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\internship\\frappe-mcp-python",
        "run",
        "main2.py"
      ]
    }
  }
}

```


### Launch Server

`uv run main2.py`


### Launch Test Server

`mcp dev main2.py`

Run the dev server with configuration:

- transport type: `stdio`
- command: `uv`
- arguments: `--directory "D:\internship\frappe-mcp-python" run main2.py`


## Adding New Tools

The project uses a dynamic tool registration strategy in such a way that all python files under the `tools/` directory are read and registered. For a tool to be recognized it needs to follow a certain structure

### General Tool Structure 

```python
# my_tool.py

# import modules
from pydantic import BaseModel, Field
from typings import Optional
from mcp.types import (
    TextContent
)

class ToolSchema(BaseModel):
  # required arguments and their types
  name: str = Field(..., description="argument description")
  # for optional arguments, provide a default value for field, ... means its mandatory
  age: Optional[int] = Field(None, description="argument description")

def my_tool(clients, arguments):
  """ tool description in detail """

  # access arguments
  name = arguments['name']
  age = arguments['age']

  # perform operations
  output = None 

  return [
    TextContent(
        type="text",
        text=json.dumps(output.result, indent=2)
    )
  ]

exports = {
  "tool": my_tool,
  "tool_schema": ToolSchema,
  "requires": ['frappe_client', 'db_client']
}
```

**Tool Schema**

all necessary arguments required to call the tool must be provided here with proper description. Claude will read this schema and pass the necessary arguments in the `arguments` parameter of the function

In the above example, to access the arguments passed by claude use the `arguments` parameter

**Tool Description**

An in-depth description of the tool, its use case and other features can be defined as a doctype denote by triple quotes `""" description """` under the tool function, this will be used while registering the tool for claude

**Return Type of Tool**

Tools must return output wrapped in `TextContent` class for claude to read it

**Exports**

This is the most important part of the `tool` file, every file must have an export object for it to be recognized as a tool

- `tool`: the actual function
- `tool_schema`: the schema created that consists of arguments and descriptions
- `requires`: externals clients if needed (example, frappe_client, db_client)



