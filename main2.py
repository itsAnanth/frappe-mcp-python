import os
import logging
from Frappe.client import FrappeClient
from dotenv import load_dotenv
from mcp.server import Server
from tools import register_tools
import logging

from mcp.server import (
    Server
)

from Frappe.client import FrappeClient
from db.client import DBClient



# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frappe-mcp-server")

# frappe client
frappe_client = FrappeClient(
    url=os.environ.get("API_URL"),
)

db_client = DBClient(
    host=os.environ.get("DB_HOST"),
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    database=os.environ.get("DB_DATABASE")
)

frappe_client.authenticate(os.environ.get("API_KEY"), os.environ.get("API_SECRET"))
# frappe_client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

requires = {
    "frappe_client": frappe_client,
    "db_client": db_client
}

app = Server("frapper-mcp-server")



async def main():
    await register_tools(app, requires)
    from mcp.server.stdio import stdio_server
    logger.info("[SERVER MANAGER] launching server")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
