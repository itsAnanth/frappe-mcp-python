# Installation

`git clone https://github.com/itsAnanth/frappe-mcp-python`

`cd frappe-mcp-python`

`uv sync`

# Add Config file to Claude

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


# Launch Server

`uv run main2.py`


# Launch Test Server

`mcp dev main2.py`

Run the dev server with configuration:

- transport type: `stdio`
- command: `uv`
- arguments: `--directory "D:\internship\frappe-mcp-python" run main2.py`

