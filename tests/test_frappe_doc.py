import pytest
from Frappe.client import FrappeClient
from dotenv import load_dotenv
import os 
import json

"tests/test_frappe_doc.py"
load_dotenv()

client = FrappeClient(
    url="https://crm.axilume.com/"
)

client.login(os.environ.get("API_USERNAME"), os.environ.get("API_PASSWORD"))

@pytest.mark.parametrize("docType, expected", [
    ("ToDod", "Doctype data not found"),
    ("ToDo", [{'name': 'lffovcblli'}, {'name': '2n2at5bfn9'}, {'name': 'o4i9ffbqfc'}, {'name': 'nn774086h5'}])
])
def test_get_doc(docType, expected):
    doc = client.get_doc(docType)

    if isinstance(expected, str):
        assert doc == expected, f"Expected {expected}, but got {doc}"
    else:
        assert doc == expected, f"Expected {expected}, but got {doc}"
# print(client.get_doc('ToDo'))

