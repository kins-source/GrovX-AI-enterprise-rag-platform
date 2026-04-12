import os
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from utils.logger import logger

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sales.db")
SQLITE_URL = f"sqlite:///{DB_PATH}"

_db = SQLDatabase.from_uri(SQLITE_URL)

@tool
def query_sales_database(query: str) -> str:
    """
    REQUIRED FOR ANY QUERY ABOUT NUMBERS, REVENUE, SALES, ORDERS, OR CUSTOMER COUNTS.
    You MUST execute this tool to get the answer. DO NOT GUESS OR EXPLAIN HOW TO DO IT.
    Provide a valid SQLite query string to this tool, and it will execute it and return the data.
    
    CRITICAL INSTRUCTIONS FOR SQL GENERATION:
    - For "revenue" or "total sales": Use `SELECT SUM(total_price) FROM orders;`
    - For "transactions", "total orders", or "orders count": Use `SELECT COUNT(*) FROM orders;`
    - For "average order value": Use `SELECT AVG(total_price) FROM orders;`
    
    Schema details:
    - customers: id, name, email, company
    - products: id, name, category, price
    - orders: id, customer_id, product_id, quantity, total_price, order_date
    """
    logger.info(f"Executing SQL Query: {query}")
    try:
        result = _db.run(query)
        return result
    except Exception as e:
        logger.error(f"SQL Query Failed: {e}")
        return f"Error executing query: {e}"
