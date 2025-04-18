import mariadb
from dotenv import load_dotenv
import sqlparse
from sqlparse.tokens import Keyword, DML, Whitespace
import logging
from contextlib import closing
from tabulate import tabulate
from pydantic import BaseModel

class QueryExecutionResult(BaseModel):
    status: bool
    result: list[dict] | str | None


logger = logging.getLogger("frappe-mcp-server")
logging.basicConfig(level=logging.DEBUG)
class DBClient:
    
    def __init__(self, host: str, username: str, password: str, database: str):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.READ_ONLY_KEYWORDS = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
        
        
    def is_read_only(self, query: str) -> str:
        # only allow readonly keywords
        READ_ONLY_KEYWORDS = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
        
        cleaned = sqlparse.format(query, strip_comments=True, strip_whitespace=True, strip_newlines=True)
        statements = sqlparse.parse(cleaned)
        
        logger.debug(f"Cleaned query: {cleaned}")
        

        # evaluate each statement, to handle multi-statement query
        for statement in statements:
            first_token = next((token for token in statement.tokens if token.ttype is not token.is_whitespace), None)
            
            # query is empty, invalid
            if first_token is None:
                return False
            
            # keyword is not a valid DML
            if (first_token.value.upper() not in READ_ONLY_KEYWORDS):
                return False
            
            tokens = cleaned.upper().split()
            blacklisted_keywords = (
                "INSERT", 
                "UPDATE", 
                "DELETE", 
                "REPLACE", 
                "CREATE", 
                "ALTER", 
                "DROP",
                "INTO",
                "TRUNCATE",
                "LOAD_FILE",
                "DUMPFILE",
                "OUTFILE"
            )
            
            # if any tokens are in blacklisted keywords, return false
            if any(token in tokens for token in blacklisted_keywords):
                return False
        
        return True
        
        
        
    def get_connection(self):
        print(self.username, self.password)
        try:  
            conn = mariadb.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                database=self.database
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None


        print("connected")
        return conn
    
    def execute_query(self, query: str, tabulate_output=True) -> QueryExecutionResult:
        
        # Check if the query is read-only
        if not self.is_read_only(query):
            return QueryExecutionResult(
                status=False,
                result=None
            )
    
        with closing(self.get_connection()) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                formatted_output = [dict(zip(columns, row)) for row in result]
                tabulated_output = tabulate(formatted_output, headers="keys", tablefmt="psql")
                
                return QueryExecutionResult(
                    status=True,
                    result=tabulated_output if tabulate_output else formatted_output
                )
                
            except mariadb.Error as e:
                return QueryExecutionResult(
                    status=False,
                    result=f"Error executing query: {e}"
                )
            