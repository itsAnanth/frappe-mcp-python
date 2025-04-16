from Frappe.client import FrappeClient
from dotenv import load_dotenv
import os 

load_dotenv()

client = FrappeClient(
    url="https://crm.axilume.com/",
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

# client.authenticate()
client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

# print(client.get_doc('ToDo', filters={"name": "lffovcblli"}))
print(client.get_doc('ToDo'))