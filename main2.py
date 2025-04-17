import os
import logging
from Frappe.client import FrappeClient
from dotenv import load_dotenv
from mcp.server import Server
from tools import register_tools



# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frappe-mcp-server")

# frappe client
frappe_client = FrappeClient(
    url="https://crm.axilume.com/"
)
frappe_client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))
app = Server("frapper-mcp-server")



async def main():
    register_tools(app, frappe_client)
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
        logger.info("[SERVER MANAGER] launched server")
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
