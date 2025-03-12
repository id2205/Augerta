import sys
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    filename='test_script.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Log Python and SQLite versions
logging.info(f"Python version: {sys.version}")
logging.info(f"SQLite version: {sqlite3.sqlite_version}")

# Test database operations
try:
    from rooster.data_manager import init_db
    init_db()
    
    conn = sqlite3.connect('rooster/stock_data.db')
    tables = [table[0] for table in conn.execute('SELECT name FROM sqlite_master WHERE type="table"')]
    logging.info(f"Tables in database: {tables}")
    conn.close()
except Exception as e:
    logging.error(f"Database error: {str(e)}")
