from Frappe.client import FrappeClient
from dotenv import load_dotenv
import os 
import json

load_dotenv()

client = FrappeClient(
    url="https://crm.axilume.com/"
)


# client.authenticate()
client.authenticate(os.environ.get("MCP_API_KEY"), os.environ.get("MCP_API_SECRET"))

# client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))
# dat = client.get_doc('Employee', name="HR-EMP-00001")

# with open('out.json', 'w', encoding='utf-8') as f:
#     json.dump(dat, f, ensure_ascii=False, indent=4)
# print(client.get_doc('ToDo', filters={"name": "lffovcblli"}))
# print(len(client.get_doc('DocType', filters=[["module", "=", "HR"]])))
stat, dat = client.get_doc('DocType/Leave Application')
# print(dat)
fields = dat['fields']
print([f['fieldname'] for f in fields if f['fieldtype'] not in ('Section Break', 'Column Break', 'HTML')])

with open('out.json', 'w', encoding='utf-8') as f:
    json.dump(dat, f, ensure_ascii=False, indent=4)



