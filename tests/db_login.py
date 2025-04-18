from db.client import DBClient
from dotenv import load_dotenv 
import os
from tabulate import tabulate
load_dotenv()

db = DBClient(
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE")
)

output = db.execute_query("""
                          
                          show tables;
                          """, tabulate_output=False)
print(output.result)




# print(tabulate([], headers="keys", tablefmt="psql") == "")
