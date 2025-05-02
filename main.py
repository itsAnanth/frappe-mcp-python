import os
import logging
from Frappe.client import FrappeClient
from dotenv import load_dotenv
from tools import register_tools
import logging


from Frappe.client import FrappeClient
from db.client import DBClient

from fastmcp import FastMCP



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

frappe_client.authenticate(os.environ.get("MCP_API_KEY"), os.environ.get("MCP_API_SECRET"))
# frappe_client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

requires = {
    "frappe_client": frappe_client,
    "db_client": db_client
}

app = FastMCP("frapper-mcp-server")



def main():
    register_tools(app, requires)
    logger.info("[SERVER MANAGER] launching server")

    app.run()
        
if __name__ == "__main__":
    main()

__all__ = ['frappe_client', 'db_client']