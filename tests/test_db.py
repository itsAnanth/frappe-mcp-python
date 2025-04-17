import pytest
from db.client import DBClient
import os

db = DBClient(
    username=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE")
)

@pytest.mark.parametrize("query, expected", [
    
    ("SELECT * FROM users", True),
    ("SHOW TABLES", True),
    ("DESCRIBE users", True),
    ("DESC users", True),
    ("EXPLAIN SELECT * FROM users", True),
    
    # EDGE CASE: fails when using multiple queries, the trailing query being non-read only
    ("SELECT * FROM users; DROP TABLE users;", False),
    
    ("""SELECT 
    employee_name, 
    department, status 
    FROM 
        Employee 
    WHERE 
        status = 'Active'
    ORDER BY 
        employee_name ASC;""", True),
    
    ("""DELETE FROM Employee 
    WHERE status = 'Left';""", False),
    
    ("SELECT * FROM Employee; DROP TABLE Employee;", False),
    
    ("""
    SELECT employee_name, department FROM Employee WHERE status = 'Active';
    SELECT department, COUNT(*) FROM Employee GROUP BY department;""", True),
    
    ("""
    SELECT employee_name, department FROM Employee WHERE status = 'Active';
    DELETE FROM Employee WHERE status = 'Left';""", False),
])
def test_query(query, expected):
    assert db.is_read_only(query) == expected