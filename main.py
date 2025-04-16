from mcp.server.fastmcp import FastMCP
from Frappe.client import FrappeClient
import os
from dotenv import load_dotenv

load_dotenv()

frappe_client = FrappeClient(
    url="https://crm.axilume.com/",
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

frappe_client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

server = FastMCP(
    name="frappe-mcp-server"
)

server.add_tool(
    frappe_client.get_doc,
    name="get_document",
    description=(
        "Get a document from Frappe"
        "Parameters: \n"
        " - doctype: DocType of the document to be returned\n"
        " - name: (optional) `name` of the document to be returned\n"
        " - filters: (optional) Filter by this dict if name is not set\n"
        " - fields: (optional) Fields to be returned, will return everything if not set\n"    
    )
)

if __name__ == "__main__":
    print("running")
    server.run(transport='stdio')